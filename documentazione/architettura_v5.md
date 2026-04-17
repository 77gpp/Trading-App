# ARCHITETTURA V5 — Trading Multi-Agent Desk

## Organigramma degli Agenti

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              SUPERVISOR AGENT                                        │
│                     agents/supervisor_agent.py · SupervisorAgent                    │
│                  Controller del flusso — non analizza, coordina                     │
└────────┬───────────────────┬──────────────────────┬──────────────────┬─────────────┘
         │                   │                      │                  │
         ▼ Step 1 + Step 4   ▼ Step 1.5             ▼ Step 2           ▼ Step 3
┌─────────────────┐ ┌─────────────────┐  ┌──────────────────┐  ┌──────────────────────┐
│  MACRO EXPERT   │ │ SKILL SELECTOR  │  │ CONTEXT EXPANDER │  │  TECHNICAL DESK      │
│ AgnoMacroExpert │ │  SkillSelector  │  │ContextExpander   │  │  (4 specialisti)     │
│                 │ │                 │  │      Agent       │  │                      │
│ Modello: *      │ │ Modello: *      │  │ Modello: *       │  │ Modello: *           │
│ (selezionabile) │ │ (selezionabile) │  │ (selezionabile)  │  │ (selezionabile)      │
│ Temp: 0.7       │ │ Temp: 0.0       │  │ Temp: 0.0        │  │ Temp: 0.7            │
│                 │ │                 │  │                  │  │                      │
│ Tools:          │ │ Input:          │  │ Input:           │  ├──────────────────────┤
│ · DuckDuckGo    │ │ · macro_sent.   │  │ · query semantica│  │ 🔍 PATTERN ANALYST   │
│ · YFinance      │ │ · data_dict     │  │ Output:          │  │ PatternAgent         │
│ · AlpacaNews    │ │ Output:         │  │ · knowledge_ctx  │  │ agents/specialists/  │
│                 │ │ · chosen_tools  │  │ (dai PDF Gemini) │  │ pattern_agent.py     │
│ Skills:         │ │ · skills_guid.  │  │                  │  ├──────────────────────┤
│ · macro-strat.  │ │                 │  │                  │  │ 📈 TREND ANALYST     │
│ · verdict-synth.│ │ Catalogo:       │  │                  │  │ TrendAgent           │
│                 │ │ · 17 pattern    │  │                  │  │ agents/specialists/  │
│ Step 1 Output:  │ │ · 22 trend      │  │                  │  │ trend_agent.py       │
│ · macro_sent.   │ │ · 14 SR tools   │  │                  │  ├──────────────────────┤
│                 │ │                 │  │                  │  │ 🎯 SR ANALYST        │
│ Step 4 Output:  │ │                 │  │                  │  │ SRAgent              │
│ · verdetto fin. │ │                 │  │                  │  │ agents/specialists/  │
│   Bias/Entry/   │ │                 │  │                  │  │ sr_agent.py          │
│   SL/TP         │ └─────────────────┘  └──────────────────┘  ├──────────────────────┤
└─────────────────┘                                             │ 🌊 VOLUME ANALYST    │
         ▲                                                      │ VolumeAgent          │
         │ sintetizza_verdetto()                                │ agents/specialists/  │
         │ riceve: macro_sent. + 4 analisi tech.               │ volume_agent.py      │
         └──────────────────────────────────────────────────── │ (FILTRO FINALE)      │
                                                                └──────────────────────┘
```

> **Nota sulla selezione dei modelli**: Tutti gli agenti usano modelli configurabili tramite `Calibrazione.py`.
> Con `LLM_PROVIDER = "gemma4"` (default), tutti gli agenti usano Gemma 4 locale su `http://localhost:8080`.
> Con `LLM_PROVIDER = "qwen"` o `"gemini"`, usano i modelli remoti specificati in `Calibrazione.py`.

---

## Flusso di Esecuzione Sequenziale

Il sistema esegue ogni step in sequenza con **25 secondi di pausa** tra ogni chiamata LLM, per rispettare i rate limit delle API Groq (token/minuto).

```
DataFetcher.get_mtf_data()
   │  Dati OHLCV: 1H · 4H · 1D (Yahoo Finance)
   │  Configurati da: TECH_SHORT_TERM_CANDLES / TECH_MID_TERM_CANDLES / TECH_LONG_TERM_CANDLES
   ▼
SupervisorAgent.analizza_asset()
   │
   ├─ [Step 1] AgnoMacroExpert.analizza()
   │     ├─ YFinance: prezzi real-time, variazione %, volumi 24h
   │     ├─ DuckDuckGo: news web, FED/BCE, sentiment retail
   │     ├─ AlpacaNewsTool: notizie istituzionali certificate
   │     ├─ Skill: macro-strategist (framework Dalio/Soros/Murphy/Rickards)
   │     └─ → macro_sentiment (testo Markdown con Regime/Bias/Conviction)
   │     [attesa 25s]
   │
   ├─ [Step 1.5] SkillSelector.select_tools()
   │     ├─ Legge: skill_summaries (primi 1500 char di ogni SKILL.md)
   │     ├─ Input: nome_asset · macro_sentiment · ultimi 5 candles 1D
   │     ├─ Output JSON: chosen_tools {pattern[], trend[], sr[], summary}
   │     └─ → skills_guidance {pattern:"...", trend:"...", sr:"...", volume:"..."}
   │           (istruzioni in linguaggio naturale su cosa cercare nei libri)
   │
   ├─ [Step 2] ContextExpanderAgent.search_knowledge()
   │     ├─ Gemini File API: ricerca semantica nei PDF dei libri
   │     └─ → knowledge_context (estratti rilevanti per l'asset analizzato)
   │
   ├─ [Preparazione ctx_summary]
   │     Contiene: periodo · knowledge_context · macro_sentiment · OHLCV 1H+4H+1D
   │
   ├─ [Step 3a] PatternAgent.analizza(ctx_summary, macro_sentiment, skills_guidance["pattern"])
   │     ├─ Skills: 6 libri tecnici (Nison · Bulkowski · Ross · Williams · Murphy · Shannon)
   │     ├─ Focus: pattern selezionati da SkillSelector (es. Engulfing, Pin Bar, H&S)
   │     └─ → results_tech["Pattern Analyst"]
   │     [attesa 25s]
   │
   ├─ [Step 3b] TrendAgent.analizza(ctx_summary, macro_sentiment, skills_guidance["trend"])
   │     ├─ Skills: 6 libri tecnici
   │     ├─ Focus: indicatori selezionati (es. SMA 200, EMA 50, Bollinger)
   │     └─ → results_tech["Trend Analyst"]
   │     [attesa 25s]
   │
   ├─ [Step 3c] SRAgent.analizza(ctx_summary, macro_sentiment, skills_guidance["sr"])
   │     ├─ Skills: 6 libri tecnici
   │     ├─ Focus: livelli selezionati (es. Fibonacci, Pivot settimanali, Supply Zone)
   │     └─ → results_tech["SR Analyst"]
   │     [attesa 25s]
   │
   ├─ [Step 3d] VolumeAgent.analizza(ctx_summary, macro_sentiment, skills_guidance["volume"], other_analyses)
   │     ├─ Skills: 6 libri tecnici
   │     ├─ Ruolo: FILTRO FINALE — valida i segnali effettivi degli altri 3 specialisti
   │     ├─ Input extra: other_analyses = output reali di Pattern, Trend, SR (non solo nomi)
   │     ├─ Framework: VSA (Tom Williams) + Wyckoff
   │     └─ → results_tech["Volume Analyst"]  ← dichiara RISCHIO ELEVATO se volumi divergono
   │     [attesa 25s]
   │
   ├─ [Step 4] AgnoMacroExpert.sintetizza_verdetto(nome_asset, macro_sentiment, results_tech)
   │     ├─ Stesso agente del Step 1 — usa la memoria contestuale dell'analisi macro
   │     ├─ Skill aggiuntiva: trading-verdict-synthesizer (decision framework professionale)
   │     │     ├─ references/decision-framework.md (7 fasi: struttura → Wyckoff → S/R → entry → confluenza)
   │     │     ├─ references/risk-management.md (sizing, SL hierarchy, TP multi-livello, R:R minimo)
   │     │     └─ references/no-trade-filters.md (14 filtri: 5 assoluti, 5 forti, 4 contestuali)
   │     ├─ Applica: no-trade filters → confluence score → livelli di prezzo degli specialisti
   │     └─ → verdetto_finale: Bias Primario · Entry · SL · Target 1 · Target 2
   │           (oppure: NO TRADE con motivazione e cosa osservare)
   │     [attesa 25s]
   │
   └─ Assemblaggio report Markdown definitivo
         Struttura: MACRO · LIBRARY · TOOLS · TEAM TECNICO · VERDETTO
```

---

## File del Progetto

### Configurazione Centrale

| File | Ruolo |
|------|-------|
| `Calibrazione.py` | Unica sorgente di verità per tutti i parametri: modelli, temperature, candle count, path, flag attivazione agenti, thinking mode |

### Agenti

| File | Classe | Ruolo |
|------|--------|-------|
| `agents/supervisor_agent.py` | `SupervisorAgent` | Controller del flusso master. Non analizza: coordina, passa contesto, assembla il report |
| `agents/agno_macro_expert.py` | `AgnoMacroExpert` | **Doppio ruolo**: (1) analisi macroeconomica globale con DuckDuckGo + Alpaca + YFinance + Skill macro; (2) sintesi del verdetto finale con Skill trading-verdict-synthesizer |
| `agents/context_expander_agent.py` | `ContextExpanderAgent` | Ricerca semantica nei PDF dei libri via Gemini File API |
| `agents/skill_selector.py` | `SkillSelector` | Sceglie gli strumenti tecnici più adatti al contesto. Produce `chosen_tools` e `skills_guidance` |
| `agents/model_factory.py` | `get_model()` | Factory unica per istanziare LLM (Gemma 4 locale, Groq/Qwen, o Gemini). Configurabile da `Calibrazione.LLM_PROVIDER` |
| `agents/agno_technical_team.py` | — | Mantiene `_rimuovi_intro_inglese()` (helper post-processing). Il Team inline non è più usato dal Supervisor |
| `agents/alpaca_news_tool.py` | `get_alpaca_news()` | Tool custom per l'API Alpaca Markets (notizie istituzionali) |

### Specialisti Tecnici Standalone

| File | Classe | Dominio | Skills consultate |
|------|--------|---------|-------------------|
| `agents/specialists/pattern_agent.py` | `PatternAgent` | Candlestick e formazioni grafiche | Nison · Bulkowski · Ross |
| `agents/specialists/trend_agent.py` | `TrendAgent` | Trend, medie mobili, momentum | Murphy · Shannon · Williams |
| `agents/specialists/sr_agent.py` | `SRAgent` | Supporti, resistenze, Fibonacci, Supply/Demand | Murphy · Bulkowski · Williams |
| `agents/specialists/volume_agent.py` | `VolumeAgent` | VSA, Wyckoff, Volume Profile — FILTRO FINALE con accesso agli output reali degli altri 3 | Williams (VSA) · Wyckoff · Ross |

### Skills Library (Agno LocalSkills)

Ogni sottocartella contiene un `SKILL.md` con frontmatter Agno valido e il contenuto estratto dal libro.
Tutti gli specialisti tecnici condividono **tutti e 6 i libri** — la selezione di cosa consultare è guidata dalle istruzioni nel prompt (`skills_guidance`).

| Directory | Skill Name | Agente | Contenuto |
|-----------|-----------|--------|-----------|
| `skills_library/macro-strategist/` | `macro-strategist` | AgnoMacroExpert | 10 framework macro operativi (Dalio · Soros · Murphy · Rickards) |
| `skills_library/trading-verdict-synthesizer/` | `trading-verdict-synthesizer` | AgnoMacroExpert | Decision framework professionale: 7 fasi, 14 no-trade filters, risk management, confluence scoring |
| `skills_library/encyclopedia_of_chart_patterns/` | `encyclopedia-of-chart-patterns` | 4 specialisti | Statistiche complete su oltre 40 pattern grafici (Bulkowski) |
| `skills_library/japanese_candlestick_charting/` | `japanese-candlestick-charting` | 4 specialisti | Tutte le candele (singole, doppie, triple) con regole di validità (Nison) |
| `skills_library/joe_ross_daytrading/` | `joe-ross-daytrading` | 4 specialisti | 1-2-3 Pattern, Hook of Ross, Power Bars (Joe Ross) |
| `skills_library/larry_williams_long_term_secrets/` | `larry-williams-long-term-secrets` | 4 specialisti | %R, pivot points, timing operativo (Larry Williams) |
| `skills_library/murphy_analisi_tecnica/` | `murphy-analisi-tecnica` | 4 specialisti | Trend, medie mobili, RSI/MACD, Fibonacci, intermarket (Murphy) |
| `skills_library/technical_analysis_multiple_timeframes/` | `technical-analysis-multiple-timeframes` | 4 specialisti | Analisi top-down, allineamento multi-timeframe, VWAP (Brian Shannon) |

> **Nota tecnica**: le directory usano underscore (`_`) mentre i `name` nel frontmatter usano hyphen (`-`). Lo
> schema Agno richiede match esatto directory=name, ma il parametro `validate=False` in `LocalSkills`
> bypassa questo controllo senza impatto funzionale sul caricamento delle skill.

### Frontend Web

| File | Ruolo |
|------|-------|
| `frontend/app_web.py` | Entry point Flask su porta 5001 |
| `frontend/api/backtesting.py` | Endpoint `/api/backtest/*` — lancia job in background (threading), gestisce status, estrae Entry/SL/TP dal report |
| `frontend/api/data.py` | Endpoint `/api/data/*` — OHLCV, notizie, configurazione |
| `frontend/templates/backtesting.html` | UI principale con grafico, box calibrazione, report |
| `frontend/static/js/backtesting.js` | Logica client: polling job, rendering grafico, invio calibrazione |

### Storage

| File/Cartella | Contenuto |
|---------------|-----------|
| `storage/memory/trading_system.db` | SQLite — sessioni agenti (memoria conversazionale tra run) |
| `data/books/` | PDF originali dei libri (sorgente per Gemini File API) |

---

## Logica delle Skills Guidance

Il `SkillSelector` non si limita a scegliere quali indicatori mostrare sul grafico. Produce anche `skills_guidance`: un dizionario con istruzioni in linguaggio naturale per ogni specialista, che viene iniettato nel prompt sotto la sezione `FOCUS SKILLS`.

```python
skills_guidance = {
    "pattern": "Hai a disposizione Nison, Bulkowski e Ross. "
               "Concentra l'analisi su: Engulfing, Pin Bar, Head & Shoulders. "
               "Verifica regole di validità e target (metodo Bulkowski).",

    "trend":   "Hai a disposizione Murphy, Shannon e Williams. "
               "Applica: SMA 200, EMA 50, Bollinger Bands. "
               "Procedura top-down come da Skill.",

    "sr":      "Hai a disposizione Murphy, Bulkowski e Williams. "
               "Identifica: Fibonacci retracement, Pivot settimanali, Supply Zone.",

    "volume":  "Valida i segnali dei colleghi (Pattern: Engulfing, Trend: SMA 200, SR: Fibonacci). "
               "Usa VSA e Wyckoff. Se divergenza → RISCHIO ELEVATO."
}
```

Questo è il meccanismo che connette la selezione AI degli strumenti con l'effettiva consultazione dei libri da parte degli agenti.

---

## Gerarchia Decisionale e Pesi

```
1. MACRO EXPERT ─── Bussola Direzionale ────────────────── PESO: CONTESTO OBBLIGATORIO
      │
      │  Imposta il "perimetro d'azione": se BEARISH, gli specialisti cercano
      │  conferme ribassiste e trattano i segnali rialzisti come rimbalzi.
      │
      ▼
2. SKILL SELECTOR ── Guida alla Conoscenza ─────────────── PESO: DIREZIONALE
      │
      │  Sceglie quali tecniche dai libri applicare per questo specifico asset
      │  nel contesto macro corrente. Orienta il focus degli specialisti.
      │
      ▼
3. PATTERN ANALYST ─ Identificazione Segnali ───────────── PESO: ANALITICO BASE
4. TREND ANALYST ─── Struttura Direzionale ─────────────── PESO: ANALITICO BASE
5. SR ANALYST ─────── Mappa Livelli di Prezzo ───────────── PESO: ANALITICO BASE
      │
      │  I tre specialisti lavorano in isolamento: nessuno vede il lavoro
      │  degli altri. Questo preserva l'obiettività dell'analisi tecnica.
      │
      ▼
6. VOLUME ANALYST ── Filtro Finale (VETO) ──────────────── PESO: MASSIMO
      │
      │  Legge tutti i dati OHLCV con focus sui volumi E gli output reali
      │  degli altri 3 specialisti. Se lo SFORZO (volume) non corrisponde
      │  al RISULTATO (movimento prezzo) → RISCHIO ELEVATO.
      │  Questo veto sovrascrive qualsiasi segnale degli altri specialisti.
      │
      ▼
7. MACRO EXPERT (sintetizza_verdetto) ── Verdetto Operativo ── OUTPUT FINALE
         Applica: no-trade filters → confluence score → livelli degli specialisti
         Output: Bias Primario · Entry · Stop Loss · Target 1 · Target 2
                 oppure: NO TRADE con motivazione e catalizzatori da monitorare
```

---

## Configurazione Centrale (Calibrazione.py)

Tutti i parametri di sistema si trovano in un unico file. Non esistono valori hardcoded negli agenti.

```
LLM_PROVIDER              → 'gemma4' (locale), 'qwen' (Groq), o 'gemini' (Google)
QWEN_THINKING_ENABLED     → True = thinking mode attivo (più lento, più profondo)
                            False = risposta diretta (più veloce, no preamble inglese)

MODEL_MACRO_EXPERT        → Modello per AgnoMacroExpert (Step 1 + Step 4)
MODEL_TECH_SPECIALISTS    → Modello per i 4 specialisti
MODEL_SKILL_SELECTOR      → Modello per SkillSelector (Llama, no thinking mode)
MODEL_KNOWLEDGE_SEARCH    → Modello per ContextExpander (Gemini)

TEMPERATURE_*             → 0.0 per output JSON/strutturati, 0.7 per report narrativi

TECH_SHORT_TERM_CANDLES   → Candele 1H passate agli specialisti
TECH_MID_TERM_CANDLES     → Candele 4H passate agli specialisti
TECH_LONG_TERM_CANDLES    → Candele 1D passate agli specialisti

AGENT_MACRO_ENABLED       → Attiva/disattiva AgnoMacroExpert
AGENT_PATTERN_ENABLED     → Attiva/disattiva PatternAgent
AGENT_TREND_ENABLED       → Attiva/disattiva TrendAgent
AGENT_SR_ENABLED          → Attiva/disattiva SRAgent
AGENT_VOLUME_ENABLED      → Attiva/disattiva VolumeAgent

TECHNICAL_SKILLS_DIRS     → Lista path delle 6 directory skill tecniche
MACRO_SKILL_DIR           → Path della skill macro-strategist
VERDICT_SKILL_DIR         → Path della skill trading-verdict-synthesizer
```

---

## Estrazione Entry/SL/TP per il Frontend

Il backend (`frontend/api/backtesting.py`) analizza il report Markdown finale con `_extract_trade_setup()` per estrarre i valori da mostrare nelle card dell'UI (DIREZIONE · ENTRY · STOP LOSS · TAKE PROFIT).

**Logica di estrazione:**
1. Cerca la sezione `VERDETTO FINALE` nel report (non tutto il documento — evita falsi match nelle sezioni degli specialisti)
2. Applica regex per trovare `Entry Suggerita`, `Stop Loss`, `Target 1`, `Target 2`
3. Parser numerico che gestisce sia notazione italiana (4.850,50) che anglosassone ($4,850.50)
4. La **direzione** viene letta dalla riga `Bias Primario: Bullish/Bearish` (regex che salta il bold markdown `**`)
5. Se l'estrazione fallisce → restituisce `parse_error: True` con messaggio descrittivo che indica quale campo manca

---

## Rimozione Preamble Inglese (Qwen3 Thinking)

Qwen3 in thinking mode produce ragionamento interno in inglese prima della risposta italiana. Il sistema usa una funzione di post-processing a cascata (`_rimuovi_intro_inglese` in `agno_technical_team.py`):

```
1. Marker esplicito: cerca la stringa di apertura attesa (es. "**Bias Primario**", "🛠️ STRUMENTI UTILIZZATI")
   → taglia tutto il testo che precede
2. Heading italiano: cerca il primo heading/emoji noto (🛠️ · ## · **Bias · ---)
   → taglia da lì in poi
3. Fallback: scorre riga per riga saltando quelle con "spy words" inglesi
   (okay, let's, first, looking, i need, ...)
```

Il thinking mode può essere disabilitato da `Calibrazione.QWEN_THINKING_ENABLED = False`,
che inietta `{"enable_thinking": False}` nei `request_params` di Groq per i modelli Qwen3.
