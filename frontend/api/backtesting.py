"""
api/backtesting.py — Endpoint Flask per il Backtesting AI.

Questo modulo gestisce il flusso principale del backtesting:
1. POST /api/backtest/run    → Avvia l'analisi in background (restituisce un job_id)
2. GET  /api/backtest/status → Controlla lo stato (running/done) e recupera il report
3. POST /api/backtest/projection → Calcola la proiezione statistica futura

L'analisi viene eseguita in un thread separato per non bloccare il server.
Un dizionario in memoria (JOBS) mantiene lo stato di ogni analisi avviata.
"""

import sys
import os
import uuid
import threading
import json
import time
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT_DIR)

from flask import Blueprint, request, jsonify
from loguru import logger
from .data import calculate_volume_profile
import Calibrazione

backtesting_bp = Blueprint("backtesting", __name__)

# ------------------------------------------------------------------
# Storage in-memory degli job avviati
# job_id → {status, report, error, started_at, config}
# ------------------------------------------------------------------
JOBS: dict = {}
CANCELLED_JOBS: set = set()

# ------------------------------------------------------------------
# ENDPOINT 1: Avvio Analisi Backtesting
# ------------------------------------------------------------------
@backtesting_bp.route("/run", methods=["POST"])
def run_backtest():
    """
    Body JSON:
      {
        "symbol":           "GC=F",
        "start":            "2025-01-01",
        "end":              "2025-03-28",
        "projection_days":  Calibrazione.DEFAULT_PROJECTION_DAYS,
        "interval":         "1d",
        "calibrazione": {
          "LLM_PROVIDER":            "qwen",
          "MACRO_ANALYSIS_DAYS":     10,
          "ALPACA_NEWS_LIMIT":       15,
          "DUCKDUCKGO_NEWS_LIMIT":   10,
          "AGENT_MACRO_ENABLED":     true,
          "AGENT_PATTERN_ENABLED":   true,
          "AGENT_TREND_ENABLED":     true,
          "AGENT_SR_ENABLED":        true,
          "AGENT_VOLUME_ENABLED":    true
        }
      }
    
    Restituisce:
      { "job_id": "uuid-...", "status": "started" }
    """
    body = request.get_json()
    if not body:
        return jsonify({"error": "Body JSON richiesto"}), 400

    symbol          = body.get("symbol", "GC=F")
    start           = body.get("start", "")
    end             = body.get("end", "")
    projection_days = int(body.get("projection_days", Calibrazione.DEFAULT_PROJECTION_DAYS))
    interval        = body.get("interval", "1d")
    calibrazione    = body.get("calibrazione", {})

    if not start or not end:
        return jsonify({"error": "Parametri start e end obbligatori"}), 400

    job_id = str(uuid.uuid4())
    JOBS[job_id] = {
        "status":     "running",
        "report":     None,
        "error":      None,
        "started_at": datetime.now().isoformat(),
        "config": {
            "symbol":          symbol,
            "start":           start,
            "end":             end,
            "projection_days": projection_days,
            "interval":        interval
        }
    }

    # Avvio analisi in thread separato
    thread = threading.Thread(
        target=_run_analysis_thread,
        args=(job_id, symbol, start, end, projection_days, calibrazione),
        daemon=True
    )
    thread.start()

    logger.info(f"[BACKTEST] Job {job_id} avviato per {symbol} ({start}→{end})")
    return jsonify({"job_id": job_id, "status": "started"})


# ------------------------------------------------------------------
# ENDPOINT 2: Stato del Job
# ------------------------------------------------------------------
@backtesting_bp.route("/status/<job_id>", methods=["GET"])
def get_status(job_id: str):
    """
    Restituisce lo stato corrente del job:
      - running : analisi in corso (il frontend mostra il loader)
      - done    : analisi completata (il frontend mostra il report)
      - error   : qualcosa è andato storto
    """
    if job_id not in JOBS:
        return jsonify({"error": "Job non trovato"}), 404

    job = JOBS[job_id]
    response = {
        "job_id": job_id,
        "status": job["status"],
    }

    if job["status"] == "done":
        response["report"]       = job["report"]
        response["projection"]   = job.get("projection", {})
        response["config"]       = job["config"]
        response["trade_setup"]  = job.get("trade_setup", {})
        response["chosen_tools"] = job.get("chosen_tools", {})

    if job["status"] == "error":
        response["error"] = job["error"]

    return jsonify(response)


# ------------------------------------------------------------------
# ENDPOINT 2.5: Cancellazione Job
# ------------------------------------------------------------------
@backtesting_bp.route("/cancel/<job_id>", methods=["POST"])
def cancel_job(job_id: str):
    """
    Inserisce il job nella lista dei cancellati.
    """
    if job_id not in JOBS:
        return jsonify({"error": "Job non trovato"}), 404
    
    if JOBS[job_id]["status"] not in ["running"]:
         return jsonify({"info": "Il job non è in esecuzione", "status": JOBS[job_id]["status"]})

    CANCELLED_JOBS.add(job_id)
    JOBS[job_id]["status"] = "cancelled"
    
    logger.warning(f"[BACKTEST] Job {job_id} annullato dall'utente.")
    return jsonify({"job_id": job_id, "status": "cancelled"})


# ------------------------------------------------------------------
# ENDPOINT 3: Proiezione Statistica (Lightweight, no AI)
# ------------------------------------------------------------------
@backtesting_bp.route("/projection", methods=["POST"])
def get_projection():
    """
    Calcola una proiezione statistica del prezzo usando:
    - Media mobile esponenziale (EMA) per la direzione
    - Deviazione standard per le bande di confidenza
    
    Body JSON:
      { "symbol": "GC=F", "end": "2025-03-28", "days": 30, "interval": "1d" }
    
    Restituisce:
      { "projection": [{time, value, upper, lower}, ...] }
    """
    body   = request.get_json()
    symbol = body.get("symbol", "GC=F")
    end    = body.get("end", "")
    days   = int(body.get("days", Calibrazione.DEFAULT_PROJECTION_DAYS))

    try:
        import yfinance as yf
        import numpy as np
        import pandas as pd

        # Scarichiamo gli ultimi 90 giorni per calcolare la proiezione
        df = yf.download(symbol, period="90d", interval="1d", auto_adjust=True)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        closes = df["Close"].values.flatten().astype(float)
        if len(closes) < 10:
            return jsonify({"error": "Dati insufficienti per la proiezione"}), 400

        # Calcolo EMA a 20 periodi
        alpha   = 2 / (20 + 1)
        ema     = closes[-1]
        ema_arr = []
        for c in closes[-20:]:
            ema = alpha * c + (1 - alpha) * ema
            ema_arr.append(ema)

        last_ema   = ema_arr[-1]
        trend_step = (ema_arr[-1] - ema_arr[0]) / len(ema_arr)
        std_dev    = float(np.std(closes[-20:]))

        # Ultima data dei dati
        last_dt = df.index[-1].to_pydatetime()

        projection = []
        for i in range(1, days + 1):
            proj_dt    = last_dt + timedelta(days=i)
            proj_price = last_ema + trend_step * i
            projection.append({
                "time":  int(proj_dt.timestamp()),
                "value": round(float(proj_price), 4),
                "upper": round(float(proj_price + std_dev * 1.5), 4),
                "lower": round(float(proj_price - std_dev * 1.5), 4)
            })

        return jsonify({"projection": projection})

    except Exception as e:
        logger.error(f"[PROJECTION] Errore: {e}")
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------------------
# LISTA JOB (per debug)
# ------------------------------------------------------------------
@backtesting_bp.route("/jobs", methods=["GET"])
def list_jobs():
    """Restituisce la lista di tutti i job e il loro stato."""
    return jsonify({
        jid: {
            "status":     j["status"],
            "started_at": j["started_at"],
            "config":     j["config"]
        } for jid, j in JOBS.items()
    })


# ------------------------------------------------------------------
# FUNZIONE INTERNA: Thread di Analisi
# ------------------------------------------------------------------
def _run_analysis_thread(job_id: str, symbol: str, start: str, end: str, 
                          projection_days: int, calibrazione_override: dict):
    """
    Eseguita in un thread separato. Chiama i moduli esistenti del progetto:
    1. DataFetcher → scarica i dati OHLCV per il periodo
    2. SupervisorAgent → esegue l'analisi AI completa
    3. Genera la proiezione futura
    """
    try:
        import Calibrazione
        
        # Sovrascriviamo la calibrazione con i parametri scelti dall'utente in UI
        _apply_calibrazione_override(calibrazione_override)

        logger.info(f"[BACKTEST THREAD] Avvio analisi {symbol} ({start}→{end})")

        # 1. Download dati storici nel periodo selezionato
        import yfinance as yf
        import pandas as pd

        df_1d = yf.download(symbol, start=start, end=end, interval="1d", auto_adjust=True)
        
        # EARLY EXIT: Controllo se cancellato
        if job_id in CANCELLED_JOBS:
            logger.info(f"[BACKTEST THREAD] Job {job_id} interrotto prima del download 1h.")
            return

        df_1h = yf.download(symbol, start=start, end=end, interval="1h", auto_adjust=True)

        if isinstance(df_1d.columns, pd.MultiIndex):
            df_1d.columns = df_1d.columns.get_level_values(0)
        if isinstance(df_1h.columns, pd.MultiIndex):
            df_1h.columns = df_1h.columns.get_level_values(0)

        # Costruzione 4h
        df_4h = df_1h.resample("4h").agg({
            "Open": "first", "High": "max",
            "Low": "min", "Close": "last", "Volume": "sum"
        }).dropna()

        data_dict = {
            "1h": df_1h,
            "4h": df_4h,
            "1d": df_1d
        }

        # 3. Proiezione statistica iniziale (fallback, verrà sostituita da quella AI se disponibile)
        projection = _compute_projection(df_1d, projection_days)

        # Calcola la data obiettivo della proiezione futura
        projection_end_date = (
            datetime.strptime(end, "%Y-%m-%d").date() + timedelta(days=projection_days)
        ).isoformat()

        # EARLY EXIT: Controllo prima dell'analisi AI reale
        if job_id in CANCELLED_JOBS:
            logger.info(f"[BACKTEST THREAD] Job {job_id} interrotto prima del SupervisorAgent.")
            return

        # 4. Calcolo Volume Profile per l'analisi e visualizzazione
        vol_profile = calculate_volume_profile(df_1d)

        # Arricchiamo il riepilogo dati per l'AI con informazioni sul POC
        volume_context = f"\nVOLUME PROFILE ANALYSIS:\n- Point of Control (POC): {vol_profile['poc']}\n- Max Volume Level: {vol_profile['max_volume']}\n"

        # 5. Esecuzione Analisi AI tramite SupervisorAgent
        from agents.supervisor_agent import SupervisorAgent
        supervisore = SupervisorAgent()
        report_markdown, chosen_tools = supervisore.analizza_asset(
            data_dict,
            symbol,
            start_date=start,
            end_date=end,
            context_extra=volume_context,
            projection_end_date=projection_end_date
        )

        # 6. Estraiamo metriche chiave dal report (entry, SL, TP, previsione futura AI)
        trade_setup = _extract_trade_setup(report_markdown)

        # 7. Se il modello ha prodotto una previsione AI, sostituiamo la proiezione statistica.
        #    Validazione di plausibilità: se il prezzo estratto devia >40% dall'ultimo prezzo
        #    storico è quasi certamente un artefatto del parsing (es. "14" da una data).
        # Usa Prezzo Centrale come ancora primaria; se mancante, usa Target Proiezione come fallback
        # (il modello spesso produce solo "Target Proiezione" senza "Prezzo Centrale" esplicito)
        ai_price_raw = trade_setup.get("ai_forecast_price") or trade_setup.get("ai_forecast_tp")
        if ai_price_raw:
            last_p = projection.get("last_price", 0)
            if last_p and abs(ai_price_raw - last_p) / last_p > 0.40:
                logger.warning(
                    f"[BACKTEST THREAD] ai_forecast_price={ai_price_raw} non plausibile "
                    f"(last_price={last_p}, deviazione {abs(ai_price_raw - last_p) / last_p:.0%}). "
                    "Probabile errore di parsing dalla data nel verdetto. Mantengo proiezione statistica."
                )
            else:
                logger.info(f"[BACKTEST THREAD] Previsione AI trovata: {ai_price_raw} — ricalcolo proiezione ancorata.")
                projection = _compute_projection(
                    df_1d, projection_days,
                    ai_price=ai_price_raw,
                    ai_upper=trade_setup.get("ai_forecast_upper"),
                    ai_lower=trade_setup.get("ai_forecast_lower"),
                )

        JOBS[job_id].update({
            "status":         "done",
            "report":         report_markdown,
            "projection":     projection,
            "volume_profile": vol_profile,
            "trade_setup":    trade_setup,
            "chosen_tools":   chosen_tools
        })

        logger.success(f"[BACKTEST THREAD] Job {job_id} completato!")

    except Exception as e:
        logger.error(f"[BACKTEST THREAD] Errore nel job {job_id}: {e}")
        JOBS[job_id].update({
            "status": "error",
            "error":  str(e)
        })


def _apply_calibrazione_override(override: dict):
    """Sovrascrive temporaneamente i parametri di Calibrazione con quelli dell'UI."""
    import Calibrazione
    mapping = {
        "LLM_PROVIDER":             "LLM_PROVIDER",
        "QWEN_THINKING_ENABLED":    "QWEN_THINKING_ENABLED",
        "DEFAULT_PROJECTION_DAYS":  "DEFAULT_PROJECTION_DAYS",
        "ALPACA_NEWS_LIMIT":        "ALPACA_NEWS_LIMIT",
        "DUCKDUCKGO_NEWS_LIMIT":    "DUCKDUCKGO_NEWS_LIMIT",
        "AGENT_MACRO_ENABLED":      "AGENT_MACRO_ENABLED",
        "AGENT_PATTERN_ENABLED":    "AGENT_PATTERN_ENABLED",
        "AGENT_TREND_ENABLED":      "AGENT_TREND_ENABLED",
        "AGENT_SR_ENABLED":         "AGENT_SR_ENABLED",
        "AGENT_VOLUME_ENABLED":     "AGENT_VOLUME_ENABLED",
        "TEMPERATURE_KNOWLEDGE_SEARCH": "TEMPERATURE_KNOWLEDGE_SEARCH",
        "TEMPERATURE_MACRO_EXPERT":     "TEMPERATURE_MACRO_EXPERT",
        "TEMPERATURE_TECH_ORCHESTRATOR": "TEMPERATURE_TECH_ORCHESTRATOR",
        "TEMPERATURE_TECH_SPECIALISTS":  "TEMPERATURE_TECH_SPECIALISTS",
        "TEMPERATURE_SKILL_SELECTOR":    "TEMPERATURE_SKILL_SELECTOR",
    }
    for ui_key, cal_key in mapping.items():
        if ui_key in override:
            setattr(Calibrazione, cal_key, override[ui_key])


def _compute_projection(df_1d, days: int,
                        ai_price: float = None,
                        ai_upper: float = None,
                        ai_lower: float = None) -> dict:
    """
    Calcola la proiezione del prezzo per i prossimi `days` giorni.

    Modalità AI-anchored (quando ai_price è fornito):
      La linea parte dall'ultimo prezzo storico e converge linearmente verso
      il prezzo AI previsto all'ultimo giorno. Le bande usano ai_upper/ai_lower
      se disponibili, altrimenti ±1.5σ sul prezzo AI target.

    Modalità statistica (fallback, quando ai_price è None):
      Regressione lineare sui 20 giorni precedenti + bande ±1.5σ.
    """
    import numpy as np

    closes = df_1d["Close"].values.flatten().astype(float)
    if len(closes) < 5:
        return {}

    last_price = float(closes[-1])
    last_dt    = df_1d.index[-1].to_pydatetime()
    std_dev    = float(np.std(closes[-min(20, len(closes)):]))
    projection_candles = []

    if ai_price is not None and days > 0:
        # Interpolazione lineare dal prezzo attuale al prezzo AI target
        price_step = (ai_price - last_price) / days
        upper_target = ai_upper if ai_upper else ai_price + std_dev * 1.5
        lower_target = ai_lower if ai_lower else ai_price - std_dev * 1.5
        upper_step = (upper_target - (last_price + std_dev * 1.5)) / days
        lower_step = (lower_target - (last_price - std_dev * 1.5)) / days

        for i in range(1, days + 1):
            proj_dt    = last_dt + timedelta(days=i)
            proj_price = last_price + price_step * i
            projection_candles.append({
                "time":  int(proj_dt.timestamp()),
                "value": round(proj_price, 4),
                "upper": round((last_price + std_dev * 1.5) + upper_step * i, 4),
                "lower": round((last_price - std_dev * 1.5) + lower_step * i, 4),
            })
        trend = "bullish" if ai_price > last_price else "bearish"
        slope = round((ai_price - last_price) / days, 4)
        ai_anchored = True
    else:
        # Fallback statistico: regressione lineare sugli ultimi 20 giorni
        n      = min(20, len(closes))
        coeffs = np.polyfit(range(n), closes[-n:], 1)
        m      = float(coeffs[0])

        for i in range(1, days + 1):
            proj_dt    = last_dt + timedelta(days=i)
            proj_price = last_price + m * i
            projection_candles.append({
                "time":  int(proj_dt.timestamp()),
                "value": round(proj_price, 4),
                "upper": round(proj_price + std_dev * 1.5, 4),
                "lower": round(proj_price - std_dev * 1.5, 4),
            })
        trend = "bullish" if m > 0 else "bearish"
        slope = round(m, 4)
        ai_anchored = False

    return {
        "candles":     projection_candles,
        "trend":       trend,
        "slope":       slope,
        "last_price":  round(last_price, 4),
        "ai_anchored": ai_anchored,
        "upper_bound": round(projection_candles[-1]["upper"], 4) if projection_candles else None,
        "lower_bound": round(projection_candles[-1]["lower"], 4) if projection_candles else None,
    }


def _extract_trade_setup(report_markdown: str) -> dict:
    """
    Estrae i livelli di Entry, Stop Loss e Take Profit dal VERDETTO FINALE del report AI.
    Non usa nessun fallback statistico: se un valore non è trovato nel testo,
    viene lasciato a None e il campo parse_error viene impostato a True con
    un messaggio che descrive esattamente cosa manca.
    """
    import re

    # Struttura iniziale: tutti i valori a None (nessun fallback)
    setup = {
        "entry":                None,
        "stop_loss":            None,
        "take_profit_1":        None,
        "take_profit_2":        None,
        "direction":            "unknown",
        "ai_forecast_price":    None,   # Prezzo Centrale previsto alla data di proiezione
        "ai_forecast_upper":    None,   # Scenario rialzista AI
        "ai_forecast_lower":    None,   # Scenario ribassista AI
        "ai_forecast_entry":    None,   # Entry Proiezione
        "ai_forecast_sl":       None,   # Stop Loss Proiezione
        "ai_forecast_tp":       None,   # Target Proiezione
        "ai_forecast_bias":     None,   # Bias Proiezione (bullish/bearish/neutral)
        "parse_error":          False,
        "parse_error_msg":      ""
    }

    def _parse_number(s: str) -> float:
        """
        Converte una stringa numerica in float gestendo sia la notazione italiana
        (punto come separatore delle migliaia, virgola come decimale: 4.850,50)
        sia quella anglosassone (virgola come migliaia, punto come decimale: 4,850.50).

        CASO CRITICO: "3.100" in italiano = 3100 (migliaia), NON 3.1 (decimale).
        Regola: un singolo punto seguito da esattamente 3 cifre = separatore delle migliaia.
        """
        s = s.strip().lstrip("$€ ")
        # Se contiene sia punto che virgola, identifica quale è il decimale
        if "." in s and "," in s:
            if s.rfind(".") > s.rfind(","):
                # Stile anglosassone: 4,850.50 → rimuovi virgole
                return float(s.replace(",", ""))
            else:
                # Stile italiano: 4.850,50 → rimuovi punti, sostituisci virgola con punto
                return float(s.replace(".", "").replace(",", "."))
        elif "," in s:
            # Solo virgola: potrebbe essere decimale italiano (4850,50) o migliaia US (4,850)
            parts = s.split(",")
            if len(parts) == 2 and len(parts[1]) <= 2:
                # Probabile decimale: 4850,50
                return float(s.replace(",", "."))
            else:
                # Migliaia: 4,850 → rimuovi virgola
                return float(s.replace(",", ""))
        elif "." in s:
            parts = s.split(".")
            if len(parts) > 2:
                # Più di un punto → tutti separatori delle migliaia: "3.100.000" → 3100000
                return float(s.replace(".", ""))
            if (len(parts) == 2 and len(parts[1]) == 3
                    and parts[1].isdigit() and parts[0].isdigit()):
                # Singolo punto con ESATTAMENTE 3 cifre decimali → migliaia italiane:
                # "3.100" → 3100, "2.980" → 2980, "3.300" → 3300
                return float(parts[0] + parts[1])
            # Decimale normale: "3.10" → 3.10, "3.5" → 3.5
            return float(s)
        else:
            return float(s)

    # Pattern numerico: cifre con separatori opzionali (es. 4.850, 4,850, 4850)
    num = r'\$?\s*([\d][.\d]*[\d](?:[,.][\d]+)?|[\d]+(?:[,.][\d]+)?)'

    def _find_price_after_label(text, label_re, window=500):
        """
        Trova il label nel testo e restituisce il primo numero che NON sia
        una percentuale (seguito da %) nell'area di testo successiva.

        Questo approccio è robusto rispetto a:
        - Testo descrittivo prima del prezzo ("ritracciamento del 61.8% a 3.050")
        - Prezzi su righe separate dal label
        - Em dash e altra punteggiatura tra label e valore

        La ricerca si ferma alla prossima intestazione di campo markdown **Campo
        per evitare di catturare numeri appartenenti al campo successivo.
        """
        m = re.search(label_re, text, re.IGNORECASE)
        if not m:
            return None
        area = text[m.end(): m.end() + window]
        # Ferma al prossimo campo markdown su nuova riga (es. "\n**Stop Loss**" o "\n- **Entry**")
        next_field = re.search(r'\n\s*(?:-\s*)?\*\*[A-Za-zÀ-ÿ]', area)
        if next_field:
            area = area[:next_field.start()]
        # Scansiona tutti i numeri: salta quelli che fanno parte di una data YYYY-MM-DD
        # (preceduti da '-') o seguiti da %, : (ratio R:R) o - (separatore data).
        for nm in re.finditer(num, area):
            if nm.start() > 0 and area[nm.start() - 1] == '-':
                continue  # Preceduto da '-': componente di data (es. "14" in "2026-04-14")
            suffix = area[nm.end(): nm.end() + 2].strip()
            if suffix.startswith('%') or suffix.startswith(':') or suffix.startswith('-'):
                continue
            val = nm.group(1)
            # Salta valori < 10: sono ratio (1:2.5), score (1-5), non prezzi.
            # IMPORTANTE: usa _parse_number() e NON float() diretto, altrimenti
            # prezzi italiani come "3.200" (= 3200, oro) vengono letti come 3.2 < 10
            # e scartati erroneamente.
            try:
                if _parse_number(val) < 10:
                    continue
            except ValueError:
                pass
            return val
        return None

    # ── Localizza la sezione VERDETTO FINALE ─────────────────────────────────
    verdetto_match = re.search(
        r'(?:VERDETTO\s+FINALE[^#\n]*|🚀\s*VERDETTO\s+FINALE[^#\n]*)(.+)',
        report_markdown, re.IGNORECASE | re.DOTALL
    )
    if not verdetto_match:
        setup["parse_error"] = True
        setup["parse_error_msg"] = (
            "Sezione VERDETTO FINALE non trovata nel report. "
            "Il sintetizzatore potrebbe non aver prodotto output o aver usato un titolo diverso."
        )
        logger.error(f"[EXTRACT] {setup['parse_error_msg']}")
        return setup

    search_text = verdetto_match.group(0)

    # ── Estrazione Entry ──────────────────────────────────────────────────────
    entry_label = r'(?:[Ee]ntry\s+[Ss]uggerita|[Ee]ntry\s+[Cc]onsigliata|[Ee]ntry|[Ii]ngresso\s+[Ss]uggerit\w*)'
    raw = _find_price_after_label(search_text, entry_label)
    if raw:
        try:
            setup["entry"] = round(_parse_number(raw), 4)
        except ValueError as e:
            logger.error(f"[EXTRACT] Impossibile parsare Entry '{raw}': {e}")
    else:
        logger.warning("[EXTRACT] Campo 'Entry Suggerita' non trovato nel VERDETTO FINALE.")

    # ── Estrazione Stop Loss ──────────────────────────────────────────────────
    sl_label = r'(?:[Ss]top\s*[Ll]oss|[Ss]top)'
    raw = _find_price_after_label(search_text, sl_label)
    if raw:
        try:
            setup["stop_loss"] = round(_parse_number(raw), 4)
        except ValueError as e:
            logger.error(f"[EXTRACT] Impossibile parsare Stop Loss '{raw}': {e}")
    else:
        logger.warning("[EXTRACT] Campo 'Stop Loss' non trovato nel VERDETTO FINALE.")

    # ── Estrazione Target 1 ───────────────────────────────────────────────────
    tp1_label = r'(?:[Tt]arget\s*1|[Tt]ake\s*[Pp]rofit\s*1|[Tt][Pp]1|[Oo]biettivo\s*1)'
    raw = _find_price_after_label(search_text, tp1_label)
    if raw:
        try:
            setup["take_profit_1"] = round(_parse_number(raw), 4)
        except ValueError as e:
            logger.error(f"[EXTRACT] Impossibile parsare Target 1 '{raw}': {e}")
    else:
        logger.warning("[EXTRACT] Campo 'Target 1' non trovato nel VERDETTO FINALE.")

    # ── Estrazione Target 2 ───────────────────────────────────────────────────
    tp2_label = r'(?:[Tt]arget\s*2|[Tt]ake\s*[Pp]rofit\s*2|[Tt][Pp]2|[Oo]biettivo\s*2)'
    raw = _find_price_after_label(search_text, tp2_label)
    if raw:
        try:
            setup["take_profit_2"] = round(_parse_number(raw), 4)
        except ValueError as e:
            logger.error(f"[EXTRACT] Impossibile parsare Target 2 '{raw}': {e}")
    else:
        logger.warning("[EXTRACT] Campo 'Target 2' non trovato nel VERDETTO FINALE.")

    # ── Estrazione direzione (Bias Primario) ──────────────────────────────────
    # Approccio keyword-based: trova la label, poi cerca la keyword di direzione
    # nei successivi 200 caratteri. Più robusto di [^A-Za-z\n]* che si fermava
    # alla prima lettera, catturando parole parentetiche come "(Setup Corrente)".
    m_bias_label = re.search(r'Bias\s+Primario', search_text, re.IGNORECASE)
    if m_bias_label:
        bias_area = search_text[m_bias_label.start(): m_bias_label.start() + 200]
        m_bias_kw = re.search(
            r'\b(Bullish|Bearish|Neutrale|Neutral|Rialzista|Ribassista|NO\s*TRADE|Long|Short)\b',
            bias_area, re.IGNORECASE
        )
        if m_bias_kw:
            bias_val = m_bias_kw.group(1).lower()
            logger.info(f"[EXTRACT] Bias Primario raw: '{bias_val}'")
            if any(w in bias_val for w in ("bullish", "rialzista", "long", "buy", "positivo", "rialzo")):
                setup["direction"] = "bullish"
            elif any(w in bias_val for w in ("bearish", "ribassista", "short", "sell", "negativo", "ribasso")):
                setup["direction"] = "bearish"
            elif any(w in bias_val for w in ("neutrale", "neutral", "no trade", "wait")):
                setup["direction"] = "neutral"
            else:
                setup["direction"] = "unknown"
                logger.warning(f"[EXTRACT] Valore 'Bias Primario' non riconosciuto: '{bias_val}'")
        else:
            logger.warning(
                f"[EXTRACT] Keyword direzione non trovata dopo 'Bias Primario'. "
                f"Testo area: {bias_area[:100]!r}"
            )
    else:
        logger.warning("[EXTRACT] Riga 'Bias Primario' non trovata nel VERDETTO FINALE.")

    # ── Estrazione Previsione Futura AI ──────────────────────────────────────
    # Cerca il prezzo centrale all'interno della sezione Previsione Futura.
    # Il label "Prezzo Centrale" evita di matchare la data nella riga header
    # (es. "**Previsione Futura** (al 2026-04-14):" dove "2026" sarebbe catturato).
    forecast_label = r'(?:[Pp]rezzo\s+[Cc]entrale|[Pp]revisione\s+[Cc]entrale|[Pp]rezzo\s+[Pp]revisto)'
    raw = _find_price_after_label(search_text, forecast_label)
    if raw:
        try:
            setup["ai_forecast_price"] = round(_parse_number(raw), 4)
            logger.info(f"[EXTRACT] ai_forecast_price estratto: {setup['ai_forecast_price']}")
        except ValueError as e:
            logger.error(f"[EXTRACT] Impossibile parsare Prezzo Centrale '{raw}': {e}")
    else:
        logger.info("[EXTRACT] Campo 'Prezzo Centrale' (proiezione) non presente nel verdetto (opzionale).")

    # Entry Proiezione
    raw = _find_price_after_label(search_text, r'[Ee]ntry\s+[Pp]roiezione')
    if raw:
        try:
            setup["ai_forecast_entry"] = round(_parse_number(raw), 4)
            logger.info(f"[EXTRACT] ai_forecast_entry estratto: {setup['ai_forecast_entry']}")
        except ValueError:
            pass

    # Stop Loss Proiezione
    raw = _find_price_after_label(search_text, r'[Ss]top\s+[Ll]oss\s+[Pp]roiezione')
    if raw:
        try:
            setup["ai_forecast_sl"] = round(_parse_number(raw), 4)
            logger.info(f"[EXTRACT] ai_forecast_sl estratto: {setup['ai_forecast_sl']}")
        except ValueError:
            pass

    # Target Proiezione
    raw = _find_price_after_label(search_text, r'[Tt]arget\s+[Pp]roiezione')
    if raw:
        try:
            setup["ai_forecast_tp"] = round(_parse_number(raw), 4)
            logger.info(f"[EXTRACT] ai_forecast_tp estratto: {setup['ai_forecast_tp']}")
        except ValueError:
            pass

    # Bias Proiezione
    bias_proj_match = re.search(
        r'[Bb]ias\s+[Pp]roiezione[^A-Za-z\n]*([A-Za-z]+(?:\s+[A-Za-z]+)?)',
        search_text, re.IGNORECASE
    )
    if bias_proj_match:
        bpv = bias_proj_match.group(1).strip().lower()
        if any(w in bpv for w in ("bullish", "rialzista", "long", "buy", "rialzo")):
            setup["ai_forecast_bias"] = "bullish"
        elif any(w in bpv for w in ("bearish", "ribassista", "short", "sell", "ribasso")):
            setup["ai_forecast_bias"] = "bearish"
        else:
            setup["ai_forecast_bias"] = "neutral"
        logger.info(f"[EXTRACT] ai_forecast_bias estratto: {setup['ai_forecast_bias']}")

    upper_label = r'[Ss]cenario\s+[Rr]ialzista'
    raw = _find_price_after_label(search_text, upper_label)
    if raw:
        try:
            setup["ai_forecast_upper"] = round(_parse_number(raw), 4)
        except ValueError:
            pass

    lower_label = r'[Ss]cenario\s+[Rr]ibassista'
    raw = _find_price_after_label(search_text, lower_label)
    if raw:
        try:
            setup["ai_forecast_lower"] = round(_parse_number(raw), 4)
        except ValueError:
            pass

    # ── Segnala i campi mancanti ──────────────────────────────────────────────
    missing = [k for k in ("entry", "stop_loss", "take_profit_1") if setup[k] is None]
    if setup["direction"] == "unknown":
        missing.append("direction")
    if missing:
        setup["parse_error"] = True
        setup["parse_error_msg"] = (
            f"Campi non estratti dal VERDETTO FINALE: {', '.join(missing)}. "
            "Verifica che il sintetizzatore abbia usato le etichette corrette "
            "('Entry Suggerita', 'Stop Loss', 'Target 1', 'Bias Primario')."
        )
        logger.error(f"[EXTRACT] {setup['parse_error_msg']}")
        # Log del testo grezzo per diagnostica: mostra i primi 800 char del VERDETTO
        logger.warning(
            f"[EXTRACT] Testo VERDETTO FINALE (primi 800 char):\n{search_text[:800]}"
        )

    return setup
