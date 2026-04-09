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
          "TECH_SHORT_TERM_CANDLES": 100,
          "TECH_MID_TERM_CANDLES":   100,
          "TECH_LONG_TERM_CANDLES":  60,
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
            "1h": df_1h.tail(Calibrazione.TECH_SHORT_TERM_CANDLES),
            "4h": df_4h.tail(Calibrazione.TECH_MID_TERM_CANDLES),
            "1d": df_1d.tail(Calibrazione.TECH_LONG_TERM_CANDLES)
        }

        # 3. Proiezione statistica futura
        projection = _compute_projection(df_1d, projection_days)

        # EARLY EXIT: Controllo prima dell'analisi AI reale
        if job_id in CANCELLED_JOBS:
            logger.info(f"[BACKTEST THREAD] Job {job_id} interrotto prima del SupervisorAgent.")
            return

        # 4. Calcolo Volume Profile per l'analisi e visualizzazione
        vol_profile = calculate_volume_profile(df_1d)

        # Arricchiamo il riepilogo dati per l'AI con informazioni sul POC
        volume_context = f"\nVOLUME PROFILE ANALYSIS:\n- Point of Control (POC): {vol_profile['poc']}\n- Max Volume Level: {vol_profile['max_volume']}\n"
        
        # 5. Esecuzione Analisi AI tramite SupervisorAgent (passando contesto volumi e periodo scelto)
        from agents.supervisor_agent import SupervisorAgent
        supervisore = SupervisorAgent()
        report_markdown, chosen_tools = supervisore.analizza_asset(
            data_dict, 
            symbol, 
            start_date=start, 
            end_date=end,
            context_extra=volume_context
        )

        # 6. Estraiamo metriche chiave dal report (entry, SL, TP)
        trade_setup = _extract_trade_setup(report_markdown)

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
        "TECH_SHORT_TERM_CANDLES":  "TECH_SHORT_TERM_CANDLES",
        "TECH_MID_TERM_CANDLES":    "TECH_MID_TERM_CANDLES",
        "TECH_LONG_TERM_CANDLES":   "TECH_LONG_TERM_CANDLES",
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


def _compute_projection(df_1d, days: int) -> dict:
    """
    Calcola la proiezione statistica del prezzo.
    Restituisce i dati per disegnare la linea tratteggiata sul grafico.
    """
    import numpy as np

    closes = df_1d["Close"].values.flatten().astype(float)
    if len(closes) < 5:
        return {}

    # Trend lineare semplice sugli ultimi 20 giorni
    n         = min(20, len(closes))
    last_vals = closes[-n:]
    x         = list(range(n))
    
    # np.polyfit restituisce un array [pendenza, intercetta], li estraiamo singolarmente
    coeffs = np.polyfit(x, last_vals, 1)
    m = float(coeffs[0])
    b = float(coeffs[1])
    
    std_dev   = float(np.std(last_vals))
    last_price = float(closes[-1])

    last_dt = df_1d.index[-1].to_pydatetime()
    projection_candles = []

    for i in range(1, days + 1):
        proj_dt    = last_dt + timedelta(days=i)
        proj_price = last_price + m * i
        projection_candles.append({
            "time":  int(proj_dt.timestamp()),
            "value": round(proj_price, 4),
            "upper": round(proj_price + std_dev * 1.5, 4),
            "lower": round(proj_price - std_dev * 1.5, 4)
        })

    return {
        "candles":     projection_candles,
        "trend":       "bullish" if m > 0 else "bearish",
        "slope":       round(m, 4),
        "last_price":  round(last_price, 4),
        "upper_bound": round(last_price + std_dev * 1.5, 4),
        "lower_bound": round(last_price - std_dev * 1.5, 4)
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
        "entry":         None,
        "stop_loss":     None,
        "take_profit_1": None,
        "take_profit_2": None,
        "direction":     "unknown",
        "parse_error":   False,
        "parse_error_msg": ""
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
        # Ferma al prossimo campo markdown (es. "**Stop Loss**", "**Target 1**")
        next_field = re.search(r'\n\s*\*\*[A-ZÀÈÉÌÒÙ]', area)
        if next_field:
            area = area[:next_field.start()]
        # Scansiona tutti i numeri: salta quelli seguiti da %
        for nm in re.finditer(num, area):
            suffix = area[nm.end(): nm.end() + 2].strip()
            if not suffix.startswith('%'):
                return nm.group(1)
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
    # Il sintetizzatore scrive "**Bias Primario**: Bullish" (markdown bold),
    # quindi usiamo [^A-Za-z\n]* per saltare i caratteri non-lettera come "**: ".
    bias_match = re.search(r'Bias\s+Primario[^A-Za-z\n]*([A-Za-z]+)', search_text, re.IGNORECASE)
    if bias_match:
        bias_val = bias_match.group(1).lower()
        if bias_val in ("bullish", "rialzista", "long", "buy", "positivo"):
            setup["direction"] = "bullish"
        elif bias_val in ("bearish", "ribassista", "short", "sell", "negativo"):
            setup["direction"] = "bearish"
        elif bias_val in ("neutrale", "neutral", "sideways", "laterale"):
            setup["direction"] = "neutral"
        else:
            setup["direction"] = "unknown"
            logger.warning(f"[EXTRACT] Valore 'Bias Primario' non riconosciuto: '{bias_match.group(1)}'")
    else:
        logger.warning("[EXTRACT] Riga 'Bias Primario' non trovata nel VERDETTO FINALE.")

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

    return setup
