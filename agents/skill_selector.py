"""
agents/skill_selector.py — Agente Selezionatore di Strumenti Tecnici.

Questo agente ha il compito di:
1. Leggere la tabella degli strumenti grafici disponibili (hardcoded, sempre aggiornata)
2. Leggere un sommario delle skill presenti nella skills_library
3. Basandosi sul contesto macro (asset analizzato, sentiment, tipo di mercato),
   scegliere quali strumenti tecnici usare e perché
4. Restituire una struttura JSON con i tool scelti per ciascun gruppo (Pattern, Trend, SR)
"""

import os
import json
import re
from loguru import logger
import Calibrazione

# ------------------------------------------------------------------
# CATALOGO COMPLETO DEGLI STRUMENTI DISPONIBILI NEL GRAFICO
# Questi ID devono corrispondere ESATTAMENTE ai case in computeOverlayData() di chart.js
# ------------------------------------------------------------------
AVAILABLE_TOOLS = {
    "pattern": [
        # --- Candele Singole ---
        {"id": "pattern_doji",           "name": "Doji (Indecisione)",            "desc": "Candela con apertura=chiusura, segnala indecisione e possibile inversione"},
        {"id": "pattern_hammer",         "name": "Hammer / Hanging Man",          "desc": "Corpo piccolo con ombra lunga, potente segnale di inversione al supporto/resistenza"},
        {"id": "pattern_pin_bar",        "name": "Pin Bar (Rejection)",           "desc": "Ombra molto lunga che mostra rifiuto del prezzo, usata in Price Action pura"},
        {"id": "pattern_marubozu",       "name": "Marubozu (Impulso Puro)",       "desc": "Candela senza ombre, indica forza/debolezza estrema e pressione istituzionale"},
        # --- Candele Doppie ---
        {"id": "pattern_engulfing",      "name": "Bullish/Bearish Engulfing",     "desc": "Inversione a 2 candele, corpo della seconda ingloba la prima, molto affidabile"},
        {"id": "pattern_harami",         "name": "Harami (Inside Bar Candle)",    "desc": "Candela 'figlia' contenuta nella 'madre', pausa del trend e potenziale inversione"},
        {"id": "pattern_tweezer",        "name": "Tweezer Top/Bottom",            "desc": "Due candele con max/min identici, forte resistenza o supporto psicologico"},
        # --- Candele Triple ---
        {"id": "pattern_morning_star",   "name": "Morning/Evening Star",          "desc": "Pattern a 3 candele di inversione, tra i più affidabili della letteratura giapponese"},
        {"id": "pattern_three_candles",  "name": "Tre Soldati/Tre Corvi",         "desc": "Tre candele consecutive nella stessa direzione, segnale forte di continuazione"},
        {"id": "pattern_inside_bar",     "name": "Inside Bar (Compressione)",     "desc": "La candela corrente è contenuta in quella precedente, breakout imminente"},
        # --- Formazioni Chartistiche ---
        {"id": "pattern_engulfing",      "name": "Bullish/Bearish Engulfing",     "desc": "Pattern a 2 candele, confermato con volume - Joe Ross"},
        {"id": "pattern_powerbar",       "name": "Power Bars (Joe Ross)",         "desc": "Barre di impulso con range eccezionale, indicano partecipazione istituzionale"},
        {"id": "pattern_triangle",       "name": "Triangoli (Asc/Desc/Sim)",      "desc": "Pattern di consolidamento con target misurato pari alla base del triangolo"},
        {"id": "pattern_wedge",          "name": "Wedge Rising/Falling",          "desc": "Cuneo di inversione, molto frequente in mercati ciclici come Oro e Indici"},
        {"id": "pattern_flag",           "name": "Flag / Pennant",                "desc": "Consolidamento rettangolare post-impulso, target = misura del palo della bandiera"},
        {"id": "pattern_double_top",     "name": "Double Top/Bottom (M/W)",       "desc": "Pattern di inversione classico di John Murphy, confermato dal breakout del neckline"},
        {"id": "pattern_head_shoulders", "name": "Head and Shoulders",            "desc": "Pattern di inversione più famoso dell'analisi tecnica, alta probabilità con volume calante"},
    ],
    "trend": [
        # --- Medie Mobili Semplici ---
        {"id": "sma_10",      "name": "SMA 10",            "desc": "Media di brevissimo termine per scalper e day trader"},
        {"id": "sma_20",      "name": "SMA 20",            "desc": "Base delle Bollinger Bands, supporto/resistenza dinamica in trend forti"},
        {"id": "sma_50",      "name": "SMA 50",            "desc": "La più seguita dagli istituzionali per identificare il trend primario"},
        {"id": "sma_100",     "name": "SMA 100",           "desc": "Filtro di medio termine per eliminare il rumore di breve"},
        {"id": "sma_200",     "name": "SMA 200",           "desc": "La barriera definitiva: sopra = bull market, sotto = bear market"},
        # --- Medie Esponenziali ---
        {"id": "ema_9",       "name": "EMA 9",             "desc": "Usata dai trader di breve per segnali di entrata veloci"},
        {"id": "ema_20",      "name": "EMA 20",            "desc": "Reattiva ai movimenti, ottima in mercati veloci come Crypto e Forex"},
        {"id": "ema_50",      "name": "EMA 50",            "desc": "Media del trader swing per eccellenza, usata con EMA 200"},
        {"id": "ema_100",     "name": "EMA 100",           "desc": "Zona di equilibrio tra breve e lungo termine"},
        {"id": "ema_200",     "name": "EMA 200",           "desc": "Versione dinamica e reattiva della barriera di lungo termine"},
        # --- Canali e Bande ---
        {"id": "bollinger_upper", "name": "Bollinger Band Superiore", "desc": "Zona di ipercomprato dinamica, 2 deviazioni standard sopra SMA 20"},
        {"id": "bollinger_lower", "name": "Bollinger Band Inferiore", "desc": "Zona di ipervenduto dinamica, 2 deviazioni standard sotto SMA 20"},
        {"id": "bollinger_mid",   "name": "Bollinger Band Media",     "desc": "SMA 20, linea di regressione verso la media (mean reversion)"},
        {"id": "keltner_upper",   "name": "Keltner Channel Superiore","desc": "Canale basato su ATR, identificare squeeze di volatilità con Bollinger"},
        {"id": "keltner_lower",   "name": "Keltner Channel Inferiore","desc": "Supporto dinamico ATR-based, ottimo per mercati con trend forti"},
        # --- Indicatori di Trend ---
        {"id": "supertrend",  "name": "SuperTrend (ATR-based)",  "desc": "Segnali automatici Compra/Vendi con stop loss integrato basato su ATR"},
        {"id": "ichimoku_cloud_upper", "name": "Ichimoku Senkou A", "desc": "Bordo superiore della nuvola Ichimoku, resistenza/supporto futura"},
        {"id": "ichimoku_cloud_lower", "name": "Ichimoku Senkou B", "desc": "Bordo inferiore della nuvola Ichimoku, livello di equilibrio di lungo termine"},
        {"id": "ichimoku_kijun",       "name": "Ichimoku Kijun Sen","desc": "Linea di base Ichimoku (26 periodi), segnale con incrocio Tenkan"},
        {"id": "atr_upper",   "name": "ATR Band Superiore",      "desc": "Banda superiore basata su ATR, utile per trailing stop e target dinamici"},
        {"id": "atr_lower",   "name": "ATR Band Inferiore",      "desc": "Banda inferiore basata su ATR, utile per trailing stop e target dinamici"},
    ],
    "sr": [
        # --- Livelli Matematici ---
        {"id": "pivot_points",        "name": "Pivot Points Giornalieri",    "desc": "PP, R1, R2, S1, S2 calcolati su OHLC del periodo precedente"},
        {"id": "pivot_weekly",        "name": "Pivot Points Settimanali",    "desc": "Livelli pivot calcolati su base settimanale, più duraturi e significativi"},
        {"id": "fib_retracement",     "name": "Fibonacci Retracement",       "desc": "Livelli 23.6%, 38.2%, 50%, 61.8%, 78.6% per ingressi in correzione"},
        {"id": "fib_extension",       "name": "Fibonacci Extension",         "desc": "Target di prezzo post-breakout: 127.2%, 161.8%, 200%, 261.8%"},
        # --- Livelli Psicologici ---
        {"id": "psych_levels",        "name": "Livelli Psicologici",         "desc": "Numeri tondi (es. 3000, 2500) con alta concentrazione di ordini istituzionali"},
        {"id": "psych_levels_fine",   "name": "Livelli Semi-Psicologici",    "desc": "Numeri a semidecina (500, 250) ugualmente seguiti dallo smart money"},
        # --- Supporti e Resistenze Dinamici ---
        {"id": "dynamic_support",     "name": "Supporto Dinamico (Swing)",   "desc": "Linea di supporto tracciata sui minimi di swing significativi"},
        {"id": "dynamic_resistance",  "name": "Resistenza Dinamica (Swing)", "desc": "Linea di resistenza tracciata sui massimi di swing significativi"},
        {"id": "supply_zone",         "name": "Supply Zone (Distribuzione)", "desc": "Area di prezzo dove storicamente i venditori istituzionali sono entrati"},
        {"id": "demand_zone",         "name": "Demand Zone (Accumulazione)", "desc": "Area di prezzo dove storicamente gli acquirenti istituzionali hanno assorbito"},
        # --- Canali di Prezzo ---
        {"id": "linear_regression",   "name": "Canale di Regressione",       "desc": "Canale lineare mediato statisticamente, identifica la tendenza 'matematica'"},
        {"id": "donchian_upper",      "name": "Donchian Channel Superiore",  "desc": "Massimo degli ultimi N periodi, usato nei sistemi Turtle Traders"},
        {"id": "donchian_lower",      "name": "Donchian Channel Inferiore",  "desc": "Minimo degli ultimi N periodi, breakout = segnale di entrata Turtle"},
        {"id": "vwap",                "name": "VWAP (Volume Weighted)",      "desc": "Prezzo medio ponderato sul volume, punto di equilibrio giornaliero istituzionale"},
    ]
}

# Colori di default per ogni strumento
DEFAULT_COLORS = {
    # Pattern
    "pattern_doji":           "#ffa502",
    "pattern_hammer":         "#00d4aa",
    "pattern_pin_bar":        "#ff9f43",
    "pattern_marubozu":       "#3f8ef5",
    "pattern_engulfing":      "#ff9f43",
    "pattern_harami":         "#ee5a24",
    "pattern_tweezer":        "#fd9644",
    "pattern_morning_star":   "#00d4aa",
    "pattern_three_candles":  "#3f8ef5",
    "pattern_inside_bar":     "#fd9644",
    "pattern_powerbar":       "#f53b57",
    "pattern_triangle":       "#ee5a24",
    "pattern_wedge":          "#ff6b81",
    "pattern_flag":           "#fd9644",
    "pattern_double_top":     "#a29bfe",
    "pattern_head_shoulders": "#e84393",
    # Trend
    "sma_10":             "#ffffff",
    "sma_20":             "#ffffff",
    "sma_50":             "#ffffff",
    "sma_100":            "#ffffff",
    "sma_200":            "#ffffff",
    "ema_9":              "#ffffff",
    "ema_20":             "#ffffff",
    "ema_50":             "#ffffff",
    "ema_100":            "#ffffff",
    "ema_200":            "#ffffff",
    "bollinger_upper":    "rgba(255,255,255,0.8)",
    "bollinger_lower":    "rgba(255,255,255,0.8)",
    "bollinger_mid":      "rgba(255,255,255,0.5)",
    "keltner_upper":      "rgba(255,255,255,0.7)",
    "keltner_lower":      "rgba(255,255,255,0.7)",
    "supertrend":         "#ffffff",
    "ichimoku_cloud_upper":  "rgba(255,255,255,0.5)",
    "ichimoku_cloud_lower":  "rgba(255,255,255,0.4)",
    "ichimoku_kijun":        "#ffffff",
    "atr_upper":          "rgba(255,255,255,0.6)",
    "atr_lower":          "rgba(255,255,255,0.6)",
    # SR
    "pivot_points":       "#ffffff",
    "pivot_weekly":       "#ffffff",
    "fib_retracement":    "#ffffff",
    "fib_extension":      "#ffffff",
    "psych_levels":       "#ffffff",
    "psych_levels_fine":  "#ffffff",
    "dynamic_support":    "#ffffff",
    "dynamic_resistance": "#ffffff",
    "supply_zone":        "rgba(255,255,255,0.25)",
    "demand_zone":        "rgba(255,255,255,0.25)",
    "linear_regression":  "#ffffff",
    "donchian_upper":     "rgba(255,255,255,0.7)",
    "donchian_lower":     "rgba(255,255,255,0.7)",
    "vwap":               "#ffffff",
}



class SkillSelector:
    """
    Seleziona gli strumenti di analisi più adatti al contesto corrente.

    Produce due output distinti:
    - chosen_tools: strumenti grafici per il frontend (pattern/trend/sr overlay)
    - techniques: tecniche nominate dai libri per vincolare gli agenti specialisti
    """

    def __init__(self):
        self.skills_dir = Calibrazione.SKILLS_LIBRARY_DIR
        self._skill_summaries = None   # Cache sommari libri
        self._technique_catalog = None # Cache tecniche estratte dai SKILL.md

    def _load_technique_catalog(self) -> dict:
        """
        Estrae i nomi delle tecniche direttamente dai SKILL.md leggendo i titoli ## .
        Opera solo sui 6 libri tecnici (Calibrazione.TECHNICAL_SKILLS_DIRS).
        Restituisce {label_libro: [lista_nomi_tecniche]}.
        """
        if self._technique_catalog is not None:
            return self._technique_catalog

        # Mappa directory → etichetta leggibile
        BOOK_LABELS = {
            "encyclopedia_of_chart_patterns":        "Thomas Bulkowski — Encyclopedia of Chart Patterns",
            "encyclopedia-of-chart-patterns":         "Thomas Bulkowski — Encyclopedia of Chart Patterns",
            "japanese_candlestick_charting":          "Steve Nison — Japanese Candlestick Charting",
            "japanese-candlestick-charting":          "Steve Nison — Japanese Candlestick Charting",
            "joe_ross_daytrading":                    "Joe Ross — Day Trading",
            "joe-ross-daytrading":                    "Joe Ross — Day Trading",
            "larry_williams_long_term_secrets":       "Larry Williams — Long-Term Secrets to Short-Term Trading",
            "larry-williams-long-term-secrets":       "Larry Williams — Long-Term Secrets to Short-Term Trading",
            "murphy_analisi_tecnica":                 "John Murphy — Analisi Tecnica dei Mercati Finanziari",
            "murphy-analisi-tecnica":                 "John Murphy — Analisi Tecnica dei Mercati Finanziari",
            "technical_analysis_multiple_timeframes": "Brian Shannon — Technical Analysis Using Multiple Timeframes",
            "technical-analysis-multiple-timeframes": "Brian Shannon — Technical Analysis Using Multiple Timeframes",
        }

        catalog = {}
        for skill_dir_path in Calibrazione.TECHNICAL_SKILLS_DIRS:
            skill_file = os.path.join(skill_dir_path, "SKILL.md")
            if not os.path.exists(skill_file):
                logger.warning(f"[SKILL SELECTOR] SKILL.md non trovato: {skill_file}")
                continue

            dir_name = os.path.basename(skill_dir_path)
            label = BOOK_LABELS.get(dir_name, dir_name)
            techniques = []

            try:
                with open(skill_file, "r", encoding="utf-8", errors="ignore") as f:
                    frontmatter_done = False
                    dash_count = 0
                    for line in f:
                        stripped = line.strip()
                        # Salta il frontmatter YAML (tra i due ---)
                        if stripped == "---":
                            dash_count += 1
                            if dash_count == 2:
                                frontmatter_done = True
                            continue
                        if not frontmatter_done:
                            continue
                        # Estrae solo i titoli di secondo livello (## TecnicaNome)
                        # Esclude ### (sottosezioni) e titoli generici come "SKILLS ESTRATTE"
                        if stripped.startswith("## ") and not stripped.startswith("### "):
                            name = stripped[3:].strip()
                            if name and "skill" not in name.lower() and len(name) < 80:
                                techniques.append(name)
            except Exception as e:
                logger.warning(f"[SKILL SELECTOR] Errore lettura tecniche da {skill_file}: {e}")

            if techniques:
                catalog[label] = techniques
                logger.debug(f"[SKILL SELECTOR] {label}: {len(techniques)} tecniche trovate")

        self._technique_catalog = catalog
        return catalog

    def _load_skill_summaries(self) -> str:
        """
        Legge i file SKILL.md e ne estrae un sommario (max 800 char per libro).
        Usato come contesto aggiuntivo nel prompt del selettore.
        """
        if self._skill_summaries is not None:
            return self._skill_summaries

        summaries = []
        for skill_dir_path in Calibrazione.TECHNICAL_SKILLS_DIRS:
            skill_file = os.path.join(skill_dir_path, "SKILL.md")
            if not os.path.exists(skill_file):
                continue
            try:
                with open(skill_file, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(800)
                dir_name = os.path.basename(skill_dir_path)
                summaries.append(f"[{dir_name}]:\n{content.strip()}")
            except Exception as e:
                logger.warning(f"[SKILL SELECTOR] Errore lettura {skill_file}: {e}")

        self._skill_summaries = "\n---\n".join(summaries)
        return self._skill_summaries

    def _build_catalog_text(self) -> str:
        """Costruisce la rappresentazione testuale del catalogo strumenti grafici."""
        lines = ["STRUMENTI DISPONIBILI NEL GRAFICO (usa SOLO questi ID):"]
        for group, tools in AVAILABLE_TOOLS.items():
            lines.append(f"\n[{group.upper()}]")
            for t in tools:
                lines.append(f"  - ID: {t['id']} | Nome: {t['name']} | Uso: {t['desc']}")
        return "\n".join(lines)

    def _build_technique_catalog_text(self) -> str:
        """
        Costruisce il testo del catalogo tecniche per il prompt.
        Formato: [Libro]: Tecnica1, Tecnica2, ...
        """
        catalog = self._load_technique_catalog()
        if not catalog:
            return "Nessuna tecnica trovata nelle Skill."

        lines = ["TECNICHE DISPONIBILI DALLE SKILL (seleziona ESCLUSIVAMENTE da questa lista):"]
        for book_label, techniques in catalog.items():
            techs_str = " | ".join(techniques)
            lines.append(f"\n[{book_label}]:\n  {techs_str}")
        return "\n".join(lines)

    def select_tools(self, nome_asset: str, macro_sentiment: str, data_dict: dict) -> dict:
        """
        Analizza il contesto e produce due selezioni complementari:

        1. chosen_tools (pattern/trend/sr): strumenti grafici per il frontend
        2. techniques: tecniche nominate dai libri per vincolare gli agenti specialisti

        Args:
            nome_asset:      Il ticker (es. "GC=F", "AAPL")
            macro_sentiment: Testo del sentiment macro prodotto dall'AgnoMacroExpert
            data_dict:       Dizionario con i dati OHLCV multi-timeframe

        Returns:
            Dict con: pattern · trend · sr · summary · raw_skills_used ·
                      techniques · skills_guidance · success
        """
        logger.info(f"[SKILL SELECTOR] Selezione strumenti e tecniche per {nome_asset}...")

        catalog_text    = self._build_catalog_text()
        technique_text  = self._build_technique_catalog_text()

        try:
            last_1d = data_dict["1d"].tail(5).to_string() if "1d" in data_dict else "N/D"
        except Exception:
            last_1d = "N/D"

        prompt = f"""Sei un Analista Tecnico Senior. Analizza il contesto e produci due selezioni:

ASSET: {nome_asset}

SENTIMENT MACRO:
{macro_sentiment[:1200]}

DATI RECENTI (ultime 5 candele 1D):
{last_1d}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PARTE A — STRUMENTI GRAFICI (per il frontend)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{catalog_text}

Regole per la Parte A:
- Usa SOLO gli ID esatti del catalogo grafico (nessun ID inventato)
- Il campo "reason" deve essere breve: max 10 parole
- Commodity (Oro, Oil): SMA lente + Fibonacci + Zone S/D + Price Action
- Crypto: EMA veloci + SuperTrend + Bollinger
- Forex: EMA + Ichimoku + Pivot settimanali
- Sentiment BEARISH: privilegia resistenze e pattern ribassisti
- Sentiment BULLISH: privilegia supporti e pattern rialzisti

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PARTE B — TECNICHE DAGLI SKILL BOOK (per gli agenti)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{technique_text}

Regole per la Parte B:
- Seleziona SOLO tecniche presenti nel catalogo qui sopra (nome ESATTO dal catalogo)
- Assegna ogni tecnica al dominio corretto: pattern · trend · sr · volume
- OBIETTIVO: selezionare il MAGGIOR NUMERO POSSIBILE di tecniche rilevanti — idealmente 8-15 per dominio
- Non essere avaro: più tecniche selezionate = analisi più solida e multidimensionale
- Cerca di coprire TUTTI i libri del catalogo: ogni libro deve contribuire almeno con 2-3 tecniche
- Sentiment BEARISH: privilegia tecniche di inversione ribassista, divergenze negative, segnali di distribuzione
- Sentiment BULLISH: privilegia tecniche di inversione rialzista, continuazione, segnali di accumulazione
- Il campo "book" deve contenere il nome esatto del libro di provenienza dal catalogo
- Il campo "reason" deve essere breve: max 10 parole

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT — Rispondi SOLO con JSON valido (nessun testo fuori, niente markdown):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{{
  "pattern": [
    {{"id": "pattern_engulfing", "name": "Bullish/Bearish Engulfing", "reason": "...", "color": ""}},
    {{"id": "pattern_pin_bar", "name": "Pin Bar", "reason": "...", "color": ""}}
  ],
  "trend": [
    {{"id": "sma_200", "name": "SMA 200", "reason": "...", "color": ""}},
    {{"id": "ema_50", "name": "EMA 50", "reason": "...", "color": ""}}
  ],
  "sr": [
    {{"id": "fib_retracement", "name": "Fibonacci Retracement", "reason": "...", "color": ""}},
    {{"id": "supply_zone", "name": "Supply Zone", "reason": "...", "color": ""}}
  ],
  "techniques": {{
    "pattern": [
      {{"name": "NOME_ESATTO_DAL_CATALOGO", "book": "Steve Nison — Japanese Candlestick Charting", "reason": "..."}},
      {{"name": "NOME_ESATTO_DAL_CATALOGO", "book": "Thomas Bulkowski — Encyclopedia of Chart Patterns", "reason": "..."}}
    ],
    "trend": [
      {{"name": "NOME_ESATTO_DAL_CATALOGO", "book": "John Murphy — Analisi Tecnica dei Mercati Finanziari", "reason": "..."}}
    ],
    "sr": [
      {{"name": "NOME_ESATTO_DAL_CATALOGO", "book": "John Murphy — Analisi Tecnica dei Mercati Finanziari", "reason": "..."}}
    ],
    "volume": [
      {{"name": "NOME_ESATTO_DAL_CATALOGO", "book": "Larry Williams — Long-Term Secrets to Short-Term Trading", "reason": "..."}}
    ]
  }},
  "summary": "Selezione per {nome_asset} — {macro_sentiment[:60]}...",
  "raw_skills_used": ["Steve Nison", "Thomas Bulkowski", "John Murphy"]
}}"""

        try:
            from agents.model_factory import get_model
            # Usiamo un modello senza thinking mode per output JSON puro.
            # Qwen3 usa troppi token per il blocco <think> e tronca il JSON.
            llm = get_model(Calibrazione.MODEL_SKILL_SELECTOR, temperature=Calibrazione.TEMPERATURE_SKILL_SELECTOR)

            from agno.agent import Agent
            selector_agent = Agent(
                model=llm,
                description="Sei un analista tecnico che seleziona strumenti di analisi in base al contesto.",
                instructions=["Rispondi SOLO con JSON valido, senza markdown extra."],
                markdown=False,
            )

            response = selector_agent.run(prompt)
            raw = response.content if response.content else ""
            raw = raw.strip()

            # Log diagnostico — mostriamo i primi 500 caratteri della risposta
            logger.debug(f"[SKILL SELECTOR] Risposta grezza AI (primi 500 char): {raw[:500]}")

            if not raw:
                logger.error(f"[SKILL SELECTOR] L'AI ha prodotto una risposta VUOTA.")
                return {"success": False, "error": "AI_EMPTY_RESPONSE", "summary": "L'AI non ha prodotto nessuna risposta."}

            # 1. Rimuoviamo i blocchi markdown residui
            raw = re.sub(r'^```(?:json)?\s*', '', raw, flags=re.MULTILINE)
            raw = re.sub(r'\s*```$', '', raw, flags=re.MULTILINE)

            # 2. Rimuoviamo il blocco <think>...</think> se il tag è chiuso
            raw = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL)

            # 3. Se il blocco <think> non è chiuso (risposta troncata nel mezzo del pensiero),
            #    cerchiamo direttamente il primo '{' e prendiamo tutto da lì in poi.
            #    Questo è il fix principale per Qwen3 su Groq che taglia la risposta.
            first_brace = raw.find('{')
            if first_brace == -1:
                logger.error(f"[SKILL SELECTOR] Nessun JSON trovato nella risposta AI.")
                return {"success": False, "error": "AI_NO_JSON", "summary": "Nessun blocco JSON trovato nella risposta."}
            raw = raw[first_brace:]

            # 4. Tentiamo il parsing — se il JSON è troncato, json.loads fallirà
            #    ma almeno avremo tagliato il blocco <think> non chiuso
            
            chosen = json.loads(raw)

            # Validazione: assicuriamoci che gli ID esistano nel catalogo
            chosen = self._validate_and_fallback(chosen)

            n_pat = len(chosen.get('techniques', {}).get('pattern', []))
            n_trd = len(chosen.get('techniques', {}).get('trend', []))
            n_sr  = len(chosen.get('techniques', {}).get('sr', []))
            n_vol = len(chosen.get('techniques', {}).get('volume', []))
            logger.success(
                f"[SKILL SELECTOR] Tecniche selezionate dai libri per {nome_asset}: "
                f"pattern={n_pat}, trend={n_trd}, sr={n_sr}, volume={n_vol}"
            )
            return chosen

        except json.JSONDecodeError as e:
            logger.warning(f"[SKILL SELECTOR] JSON non valido dall'AI ({e}). Raw: '{raw[:300] if 'raw' in dir() else 'N/A'}'. Segnalo fallimento.")
            return {"success": False, "error": "AI_JSON_ERROR", "summary": f"L'AI non ha prodotto un formato JSON valido: {e}"}

        except Exception as e:
            logger.error(f"[SKILL SELECTOR] Errore: {e}. Segnalo fallimento.")
            return {"success": False, "error": "AI_SYSTEM_ERROR", "summary": str(e)}


    def _validate_and_fallback(self, chosen: dict) -> dict:
        """
        Valida il JSON restituito dall'AI:
        - Rimuove ID grafici non presenti nel catalogo (pattern/trend/sr)
        - Valida le tecniche dai libri (techniques): scarta quelle con nome vuoto
        - Costruisce skills_guidance dai techniques validati
        """
        all_valid_ids = {t["id"]: t for group in AVAILABLE_TOOLS.values() for t in group}
        result = {"success": True}

        # ── Parte A: strumenti grafici (frontend) ──────────────────────────────
        for group in ("pattern", "trend", "sr"):
            valid_items = []
            for item in chosen.get(group, []):
                if not isinstance(item, dict):
                    continue
                tool_id = item.get("id")
                if tool_id not in all_valid_ids:
                    logger.warning(f"[SKILL SELECTOR] ID grafico non valido rimosso: {tool_id!r}")
                    continue

                static_info = all_valid_ids[tool_id]

                # Colore: forza bianco se mancante o nero
                color_val = str(item.get("color", "")).lower().strip()
                is_black = color_val in {"#000", "#000000", "black", "null", "none", "",
                                         "rgb(0,0,0)", "rgba(0,0,0,1)", "rgba(0,0,0,0)"}
                if is_black:
                    logger.warning(f"[SKILL SELECTOR] Colore nero scartato per {tool_id}, forzato bianco.")
                item["color"] = "#ffffff" if (is_black or not item.get("color")) else item["color"]
                if not item.get("color"):
                    item["color"] = DEFAULT_COLORS.get(tool_id, "#ffffff")

                item.setdefault("desc", static_info.get("desc", ""))
                item.setdefault("name", static_info.get("name", ""))
                valid_items.append(item)

            result[group] = valid_items

        # ── Parte B: tecniche dai libri (per gli agenti) ──────────────────────
        raw_techniques = chosen.get("techniques", {})
        validated_techniques = {}
        for domain in ("pattern", "trend", "sr", "volume"):
            valid_techs = []
            for item in raw_techniques.get(domain, []):
                if not isinstance(item, dict):
                    continue
                name = item.get("name", "").strip()
                book = item.get("book", "").strip()
                if name and book:
                    valid_techs.append({"name": name, "book": book,
                                        "reason": item.get("reason", "")})
                else:
                    logger.warning(f"[SKILL SELECTOR] Tecnica scartata (nome/libro mancante): {item}")
            validated_techniques[domain] = valid_techs

        result["techniques"]      = validated_techniques
        result["summary"]         = chosen.get("summary", "Selezione AI per questo asset.")
        result["raw_skills_used"] = chosen.get("raw_skills_used", [])
        result["skills_guidance"] = self._build_skills_guidance(validated_techniques)
        return result

    def _build_skills_guidance(self, techniques: dict) -> dict:
        """
        Converte le tecniche selezionate dai libri in istruzioni vincolanti per ogni specialista.

        Args:
            techniques: dict {domain: [{"name": ..., "book": ..., "reason": ...}]}

        Returns:
            dict {domain: str} — istruzioni da iniettare nel prompt di ogni specialista
        """
        def format_technique_list(domain: str) -> str:
            items = techniques.get(domain, [])
            if not items:
                return ""
            lines = []
            for t in items:
                lines.append(f'  • "{t["name"]}" — {t["book"]}')
            return "\n".join(lines)

        guidance = {}

        # ── Pattern Analyst ────────────────────────────────────────────────────
        techs = format_technique_list("pattern")
        if techs:
            guidance["pattern"] = (
                "Hai accesso alle Skill estratte da Nison, Bulkowski e Joe Ross.\n"
                "Le seguenti tecniche sono state selezionate come PRIORITARIE per questo asset/contesto — "
                "devi analizzarle TUTTE, anche quelle che sembrano meno evidenti nei dati:\n"
                f"{techs}\n"
                "Dopo aver analizzato TUTTE le tecniche elencate, puoi integrare con ulteriori pattern "
                "presenti nelle tue Skill (libri caricati) che ritieni rilevanti per arricchire l'analisi. "
                "Per ogni tecnica consulta le Skill per le regole di validità esatte "
                "e il calcolo del target con il metodo Bulkowski dove applicabile."
            )
        else:
            guidance["pattern"] = ""

        # ── Trend Analyst ──────────────────────────────────────────────────────
        techs = format_technique_list("trend")
        if techs:
            guidance["trend"] = (
                "Hai accesso alle Skill estratte da Murphy, Shannon e Larry Williams.\n"
                "Le seguenti tecniche sono state selezionate come PRIORITARIE — "
                "devi analizzarle TUTTE, anche quelle che sembrano meno evidenti nei dati:\n"
                f"{techs}\n"
                "Dopo aver analizzato TUTTE le tecniche elencate, puoi integrare con altri indicatori "
                "presenti nelle tue Skill che ritieni utili per completare il quadro. "
                "Per ogni tecnica consulta le Skill per le regole operative precise "
                "(criteri di incrocio, analisi top-down, segnali di momentum)."
            )
        else:
            guidance["trend"] = ""

        # ── SR Analyst ─────────────────────────────────────────────────────────
        techs = format_technique_list("sr")
        if techs:
            guidance["sr"] = (
                "Hai accesso alle Skill estratte da Murphy, Bulkowski e Larry Williams.\n"
                "Le seguenti tecniche sono state selezionate come PRIORITARIE — "
                "devi analizzarle TUTTE per costruire la mappa completa dei livelli:\n"
                f"{techs}\n"
                "Dopo aver analizzato TUTTE le tecniche elencate, puoi integrare con altri metodi S/R "
                "presenti nelle tue Skill per aumentare il numero di livelli identificati. "
                "Per ogni tecnica consulta le Skill per i criteri di identificazione precisi "
                "e il calcolo del punteggio di confluenza."
            )
        else:
            guidance["sr"] = ""

        # ── Volume Analyst ─────────────────────────────────────────────────────
        techs_vol = format_technique_list("volume")
        # Elenca i nomi delle tecniche degli altri specialisti per il contesto di validazione
        pat_names = " · ".join(t["name"] for t in techniques.get("pattern", [])[:3])
        trd_names = " · ".join(t["name"] for t in techniques.get("trend", [])[:2])
        sr_names  = " · ".join(t["name"] for t in techniques.get("sr", [])[:2])

        vol_base = (
            "Hai accesso alle Skill estratte da Tom Williams (VSA), Wyckoff e Larry Williams.\n"
            "Il tuo ruolo è VALIDARE i segnali degli altri specialisti:\n"
            f"  • Pattern Analyst ha rilevato: {pat_names or 'pattern generici'}\n"
            f"  • Trend Analyst ha applicato: {trd_names or 'indicatori di trend'}\n"
            f"  • SR Analyst ha mappato: {sr_names or 'livelli S/R'}\n"
        )
        if techs_vol:
            vol_base += (
                "Le seguenti tecniche VSA/Wyckoff sono state selezionate come PRIORITARIE — "
                "devi analizzarle TUTTE, senza eccezzioni:\n"
                f"{techs_vol}\n"
                "Dopo aver analizzato TUTTE le tecniche elencate, integra con altri segnali VSA/Wyckoff "
                "presenti nelle tue Skill che ritieni rilevanti per una validazione completa.\n"
            )
        else:
            pass  # nessuna tecnica selezionata: il Volume Agent usa le Skill liberamente
        vol_base += (
            "Per ogni tecnica consulta le Skill per i criteri esatti (sforzo vs risultato, "
            "fasi Wyckoff, segnali VSA: No Demand, No Supply, Climax, Spring, Upthrust).\n"
            "REGOLA ASSOLUTA: se i volumi NON confermano i segnali tecnici degli altri specialisti, "
            "devi dichiarare RISCHIO ELEVATO indipendentemente dalla qualità del segnale grafico."
        )
        guidance["volume"] = vol_base

        return guidance
