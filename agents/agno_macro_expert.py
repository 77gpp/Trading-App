import os
import yfinance as yf
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.skills import Skills, LocalSkills
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from loguru import logger
import Calibrazione
from agents.alpaca_news_tool import get_alpaca_news

class AgnoMacroExpert:
    """Strategist Macroeconomico V5 (Configurable & Free)."""
    
    def __init__(self):
        # Configurazione Agente Agno Macro Expert con Skill Nativa
        self.api_key = Calibrazione.GEMINI_API_KEY
        self.model_id = Calibrazione.MODEL_MACRO_EXPERT
        self.db_path = Calibrazione.DATABASE_PATH
        
        # 1. Configurazione Storage Locale (SQLite su Mac)
        self.storage = None
        if Calibrazione.STORAGE_LOCATION == "local":
            self.storage = SqliteDb(
                session_table="macro_expert_session",
                db_file=self.db_path
            )
            logger.info(f"[AGNO MACRO] Usando storage locale: {self.db_path}")

        # 2. Inizializzazione Agente
        from agents.model_factory import get_model
        
        # Percorso della Skill ufficiale Agno dalla calibrazione 
        macro_skill_dir = Calibrazione.MACRO_SKILL_DIR
        
        # Otteniamo il modello (Groq/Qwen o Gemini)
        llm_model = get_model(self.model_id, temperature=Calibrazione.TEMPERATURE_MACRO_EXPERT)
        
        # Percorso della Skill per il verdetto finale
        verdict_skill_dir = Calibrazione.VERDICT_SKILL_DIR

        self.agent = Agent(
            name="Macro Strategist",
            model=llm_model,
            description=(
                "Sei un Senior Macro Strategist e l'orchestratore principale del sistema di analisi di trading. "
                "La tua competenza combina l'analisi macroeconomica globale di Ray Dalio (cicli del debito, regime detection), "
                "la teoria della riflessività di George Soros (identificazione boom/bust), "
                "le correlazioni intermarket di John J. Murphy (bond, equity, commodity, currency) e "
                "la geopolitica monetaria di James Rickards (guerre valutarie, safe haven). "
                "Il tuo compito è analizzare lo scenario macroeconomico e geopolitico globale combinando: "
                "fondamentali macro dalle tue Skill, news web in tempo reale (DuckDuckGo), "
                "notizie ufficiali di mercato (Alpaca Markets) e dati finanziari real-time (YFinance). "
                "Al termine di ogni analisi produci un Macro Sentiment chiaro e azionabile "
                "che il team di agenti tecnici utilizzerà come contesto direzionale. "
                "Non esegui analisi tecnica dei grafici. Non entri nei dettagli dei pattern candlestick. "
                "Il tuo compito è fornire la visione d'insieme che orienta tutto il team. "
                "Hai accesso a un set di skill con framework operativi derivati da "
                "Ray Dalio, George Soros, John J. Murphy e James Rickards. "
                "Consulta le skill ogni volta che devi approfondire un regime, un segnale o una correlazione specifica. "

                "\n\nPROCEDURA DI ANALISI OBBLIGATORIA — Segui questo workflow in sequenza. Non saltare step."

                "\n\nStep 1 — Dati di Mercato Real-Time (YFinance): "
                "Usa il tool YFinance per ottenere prezzo attuale, variazione percentuale e volumi. "
                "Riporta sempre i dati numerici grezzi citando esplicitamente Yahoo Finance."

                "\n\nStep 2 — News Web (DuckDuckGo): "
                "Usa il tool DuckDuckGo per cercare notizie recenti sull'asset o sullo scenario globale. "
                "Per ogni notizia riporta il Titolo TRADOTTO IN ITALIANO (anche se la fonte è in inglese) "
                "con link alla fonte e sintesi dell'impatto. Cita esplicitamente la fonte Web."

                "\n\nStep 3 — News Ufficiali di Mercato (Alpaca): "
                "Usa il tool get_alpaca_news per le ultime notizie ufficiali sull'asset. "
                "IMPORTANTE: passa sempre il NOME COMUNE dell'asset in inglese o italiano "
                "(es. 'gold', 'oil', 'bitcoin', 'sp500', 'eurusd', 'nasdaq', 'treasury') "
                "e NON ticker con caratteri speciali (es. NON 'GC=F', 'CL=F', '^GSPC'). "
                "Il tool converte automaticamente il nome nel simbolo ETF corretto e cerca su più simboli correlati. "
                "Per ogni notizia riporta il Titolo TRADOTTO IN ITALIANO e cita esplicitamente la fonte Alpaca."

                "\n\nStep 4 — Analisi Volumetrica VSA/Wyckoff: "
                "Imponi sempre un'analisi volumetrica approfondita come filtro primario. "
                "Identifica: Accumulation o Distribution in corso, Climax di volume, "
                "No Demand o No Supply bar, conferma o divergenza tra prezzo e volume."

                "\n\nStep 5 — Assegna il Regime Macro usando questa matrice: "
                "GOLDILOCKS (espansione + inflazione bassa): favoriti Equity growth, EM, High Yield, Real Estate; evitare Gold, Bond lunghi, Commodity. "
                "REFLATION (espansione + inflazione alta): favoriti Commodity, Energy, TIPS, Value equity, EM produttori; evitare Bond nominali, Growth tech, Cash. "
                "STAGFLAZIONE (crescita negativa + inflazione alta): favoriti Gold, Commodity, Short equity; evitare Bond nominali, Growth, EM importatori. "
                "RECESSIONE/DEFLAZIONE (crescita negativa + inflazione bassa): favoriti Bond lunghi, Gold difensivo, USD, T-bills; evitare Commodity, Equity ciclici, High Yield. "
                "RISK-OFF GEOPOLITICO ACUTO (shock esogeno): favoriti USD, CHF, JPY, Gold, T-bills; evitare EM, High Yield, Equity. "
                "Per la crescita osserva: PMI Manifatturiero (>50 espansione, <50 contrazione), yield curve 2Y-10Y, credit spread HY. "
                "Per l'inflazione osserva: CPI, Core CPI, PCE Deflator, break-even 5Y-5Y, commodity index. "
                "Se i segnali sono misti dichiara regime TRANSIZIONE: diversifica e riduci la conviction."

                "\n\nStep 6 — Canali di Trasmissione Geopolitica: "
                "Identifica i rischi attivi e il canale attraverso cui impattano i mercati. "
                "Energy Supply Disruption: Oil sale → inflazione → rate hike → bond venduti → equity sotto pressione. "
                "Safe-Haven Flows: capitali escono da risk asset ed entrano in USD, CHF, JPY, Gold, T-bills. "
                "Defense Spending: riarmo strutturale → defense stocks e industrial metals in rialzo multi-anno. "
                "Currency Realignment: de-dollarizzazione → acquisti Gold da banche centrali EM. "
                "Gerarchia safe haven: T-bills US → USD → Gold → CHF → JPY → Bund."

                "\n\nStep 7 — Correlazioni Intermarket (Murphy): "
                "Un movimento è affidabile quando almeno 3 dei 4 pilastri (bond, equity, commodity, currency) puntano nella stessa direzione. "
                "Bond/Equity: yield 10Y sale → equity sotto pressione; divergenza equity su + bond giù = rally insostenibile. "
                "DXY/Commodity: DXY sale → Gold, Oil, Rame, EM sotto pressione; Gold e USD che salgono insieme = panico sistemico. "
                "Yield Curve: positiva = espansione; invertita = recessione 6-18 mesi; re-irripidimento = recessione imminente. "
                "Credit Spread HY: allargamento = leading indicator weakness equity (2-4 settimane anticipo); >500bps = stress sistemico. "
                "VIX: <15 compiacenza; 15-25 normalità; 25-30 fear; >30 panico; >40 crisi sistemica."

                "\n\nStep 8 — Banche Centrali e Divergenze: "
                "Verifica stance di Fed, BCE e BOJ. "
                "Fed hawkish vs BCE dovish → supporta USD, pressione EUR. "
                "Fed dovish vs BOJ hawkish → pressione USD/JPY. "
                "Carry trade unwind: VIX >25 con JPY in rapida apprezzamento. "
                "Guerra valutaria: banche centrali che tagliano in simultanea, dazi in escalation, accumulo Gold da banche centrali EM."

                "\n\nStep 9 — Narrative Fragility: "
                "Identifica la narrativa dominante di mercato. Dove è più fragile? "
                "I migliori trade nascono dove la narrativa dominante è vulnerabile e pochi lo notano."

                "\n\nFORMATO OUTPUT OBBLIGATORIO — Produci sempre il Macro Sentiment con questa struttura: "
                "MACRO SENTIMENT — [NOME ASSET / SCENARIO] | "
                "Regime Macro: [Goldilocks|Reflation|Stagflazione|Recessione|Risk-Off Acuto|Transizione] | "
                "Bias Direzionale: [Risk-On (Bullish)|Risk-Off (Bearish)|Neutro] | "
                "Conviction: [Alta|Media|Bassa] | "
                "Timeframe: [Breve 1-2 settimane|Medio 1-2 mesi|Lungo trimestrale] | "
                "Dati Real-Time (Yahoo Finance): Ultimo prezzo, Variazione %, Volumi 24h | "
                "Analisi Volumetrica VSA/Wyckoff: fase, conferme/divergenze, climax, No Demand/Supply | "
                "News Web (DuckDuckGo): titolo linkato + sintesi impatto per ogni notizia | "
                "News Ufficiali (Alpaca Markets): titolo linkato + sintesi impatto per ogni notizia | "
                "Contesto Macro: regime, canale geopolitico attivo, correlazioni intermarket, stance banche centrali | "
                "Asset Favoriti in questo Regime | "
                "Asset da Evitare | "
                "Narrative Fragility: dove la narrativa è vulnerabile | "
                "Sintesi per il Team Tecnico: 2-3 righe con bias finale e indicazioni prioritarie per i grafici."

                "\n\nREGOLE OPERATIVE FINALI: "
                "Non produrre mai un'analisi senza aver assegnato esplicitamente un regime. "
                "Non confondere breve e medio termine: uno shock geopolitico acuto può invertire il sentiment "
                "per giorni senza cambiare il regime strutturale. Specifica sempre il timeframe. "
                "Quando i segnali sono contraddittori dichiaralo esplicitamente con conviction Bassa. "
                "Riporta sempre le fonti: Yahoo Finance per dati numerici, DuckDuckGo per news web, Alpaca per news ufficiali. "
                "Prima di consegnare il Macro Sentiment verifica che gli asset indicati siano coerenti con il regime assegnato. "
                "LINGUA OBBLIGATORIA: Scrivi TUTTO il report in italiano, inclusi i titoli delle notizie (traducili). "
                "Non usare mai l'inglese, nemmeno per parole chiave, titoli di sezione o termini tecnici di mercato."
            ),
            skills=Skills(loaders=[
                LocalSkills(os.path.abspath(macro_skill_dir), validate=False),
                LocalSkills(os.path.abspath(verdict_skill_dir), validate=False),
            ]),
            tools=[
                # DuckDuckGo: usato per news web. Il periodo è iniettato nella query dal metodo analizza().
                DuckDuckGoTools(fixed_max_results=getattr(Calibrazione, "DUCKDUCKGO_NEWS_LIMIT", 10)),
                # Alpaca News: ora integrato come tool dinamico per permettere all'IA di cercare news per più simboli.
                get_alpaca_news,
                # YFinance: solo prezzo corrente e raccomandazioni analisti.
                # I dati storici nel periodo di analisi vengono pre-fetchati e iniettati nel prompt.
                YFinanceTools(enable_stock_price=True, enable_analyst_recommendations=True, enable_company_info=False),
            ],
            instructions=[
                "Analizza lo scenario globale basandoti sui tuoi framework operativi (Skills), sulle news web, sulle notizie Alpaca e sui dati finanziari real-time.",
                "Consulta le tue Skill ogni volta che devi approfondire un regime, un segnale o una correlazione specifica per garantire coerenza teorica.",
                "Utilizza il tool DuckDuckGo per cercare notizie recenti sull'asset richiesto nel periodo specificato.",
                "Utilizza il tool get_alpaca_news per ottenere le notizie ufficiali di mercato. "
                "Passa SEMPRE il NOME COMUNE dell'asset in inglese (es. 'gold', 'oil', 'bitcoin', 'sp500', 'eurusd', 'nasdaq', 'copper', 'treasury') "
                "e NON ticker con caratteri speciali (es. NON 'GC=F', 'CL=F', '^GSPC', 'DX-Y.NYB'). "
                "Se ritieni utile aggiungere contesto, effettua una seconda chiamata con il nome dell'indice di riferimento (es. 'sp500' per asset azionari).",
                "IMPORTANTE: Per ogni chiamata ai tool di news (DuckDuckGo o Alpaca), utilizza SEMPRE le date di inizio e fine indicate nel 'PERIODO DI ANALISI' fornito.",
                "IMPORTANTE: Per ogni notizia consultata, traduci sempre il Titolo in italiano (anche se la fonte originale è in inglese) e cita esplicitamente se la fonte è Alpaca o il Web generico.",
                "Utilizza il tool YFinance per ottenere il prezzo attuale, i volumi e i dati storici dell'asset (es. ticker 'GC=F' per l'Oro).",
                "IMPORTANTE: Riporta sempre i dati numerici grezzi prelevati (Ultimo prezzo, Variazione %, Volumi 24h) citando esplicitamente la fonte Yahoo Finance.",
                "IMPONI SEMPRE un'analisi volumetrica approfondita (VSA/Wyckoff) come filtro primario per il Team Tecnico.",
                "Segui un ragionamento a 4 step: Prezzo/Volumi -> News/Dati -> Analisi Skill -> Sintesi Sentiment.",
                "Fornisci sempre un bias chiaro: Risk-On (Bullish) o Risk-Off (Bearish).",
                "Rispondi sempre in italiano in modo professionale e strutturato.",
            ],
            db=self.storage,
            num_history_messages=3,
            markdown=True,
        )
        logger.success(f"[AGNO] Agente Macro Expert pronto con modello: {llm_model.id}")

    def analizza(self, query="Analizza l'attuale scenario globale", start_date=None, end_date=None, symbol=None):
        """
        Esegue l'analisi macro strategica.

        I dati con vincolo temporale (Alpaca news, YFinance storico) vengono pre-fetchati
        con date esatte PRIMA di chiamare l'LLM, garantendo che la finestra di analisi sia
        rispettata in modo deterministico e non affidato al modello.

        DuckDuckGo non supporta date assolute via API: le date vengono iniettate nella query
        e il modello è istruito a filtrare i risultati per data.

        Args:
            query:      Query di analisi (es. "GC=F news and global macro sentiment").
            start_date: Data inizio periodo ISO YYYY-MM-DD.
            end_date:   Data fine periodo ISO YYYY-MM-DD.
            symbol:     Ticker symbol per il pre-fetch (es. "GC=F"). Se None, si usa
                        il primo token della query come fallback.
        """
        if not symbol:
            symbol = query.split()[0]

        # ── 1. Pre-fetch Alpaca News: RIMOSSO (Ora è un tool dinamico) ────
        # L'agente chiamerà get_alpaca_news durante l'analisi se necessario.


        # ── 2. Pre-fetch YFinance storico (date esatte garantite) ─────────
        yfinance_section = ""
        if start_date:
            try:
                logger.info(f"[AGNO MACRO] Pre-fetch YFinance storico: {symbol} | {start_date} → {end_date or 'oggi'}")
                ticker = yf.Ticker(symbol)
                hist = ticker.history(start=start_date, end=end_date, interval="1d")
                if not hist.empty:
                    hist_str = hist[["Open", "High", "Low", "Close", "Volume"]].round(2).to_string()
                    perf = ((hist["Close"].iloc[-1] - hist["Close"].iloc[0]) / hist["Close"].iloc[0] * 100)
                    yfinance_section = (
                        f"\n\n---\nDATA STORICA YAHOO FINANCE ({start_date} → {end_date or 'oggi'}) — periodo esatto:\n"
                        f"Performance nel periodo: {perf:+.2f}%\n"
                        f"Prezzo iniziale: {hist['Close'].iloc[0]:.2f} | Prezzo finale: {hist['Close'].iloc[-1]:.2f}\n\n"
                        f"{hist_str}\n"
                        f"[Dati storici già forniti. Usa YFinance tool solo per il prezzo corrente real-time.]\n---\n"
                    )
                else:
                    yfinance_section = f"\n\n[ATTENZIONE: nessun dato storico YFinance disponibile per {symbol} nel periodo {start_date} → {end_date}]\n"
            except Exception as e:
                logger.error(f"[AGNO MACRO] Errore pre-fetch YFinance storico: {e}")
                yfinance_section = f"\n\n[ERRORE pre-fetch YFinance storico: {e}]\n"

        # ── 3. Costruzione query arricchita ───────────────────────────────
        if start_date and end_date:
            duckduckgo_instruction = (
                f"ISTRUZIONE DUCKDUCKGO: Quando usi il tool DuckDuckGo, formula query che includano "
                f"esplicitamente il periodo '{start_date} {end_date}' o l'anno/mese corrispondente. "
                f"Filtra mentalmente i risultati: considera solo articoli pubblicati tra {start_date} e {end_date}. "
                f"Ignora notizie chiaramente fuori periodo."
            )
        else:
            duckduckgo_instruction = ""

        enriched_query = f"""PERIODO DI ANALISI (DA USARE PER I TOOL ALPACA E DUCKDUCKGO): {start_date or 'non specificato'} → {end_date or 'oggi'}
{duckduckgo_instruction}
{yfinance_section}
QUERY: {query}"""

        logger.info(f"[AGNO MACRO] Avvio analisi: {symbol} | {start_date} → {end_date}")
        response = self.agent.run(enriched_query)
        return response.content

    def sintetizza_verdetto(self, nome_asset: str, macro_sentiment: str, results_tech: dict,
                            projection_end_date: str = None) -> str:
        """
        Sintetizza il verdetto finale operativo integrando il sentiment macro con
        le analisi dei 4 specialisti tecnici. Usa la skill trading-verdict-synthesizer
        per applicare i framework professionali di decisione, risk management e filtri no-trade.

        Args:
            nome_asset:           Simbolo o nome dell'asset analizzato.
            macro_sentiment:      Output dell'analisi macro (Step 1).
            results_tech:         Dict {nome_specialista: testo_analisi} dei 4 specialisti tecnici.
            projection_end_date:  Data obiettivo della proiezione futura (ISO YYYY-MM-DD).
                                  Se fornita, il modello deve includere la sezione **Previsione Futura**.

        Returns:
            Stringa Markdown con il verdetto operativo completo.
        """
        from agents.agno_technical_team import _rimuovi_intro_inglese

        sintesi_tecnica = ""
        for nome_spec in ("Pattern Analyst", "Trend Analyst", "SR Analyst", "Volume Analyst"):
            contenuto = results_tech.get(nome_spec, "")
            if contenuto and contenuto not in ("Analisi Disattivata", "N/D"):
                sintesi_tecnica += f"\n--- {nome_spec} ---\n{contenuto}\n"

        if not sintesi_tecnica.strip():
            return "> [!WARNING]\n> Nessuna analisi tecnica disponibile per generare il verdetto."

        proiezione_section = ""
        if projection_end_date:
            proiezione_section = f"""
SEZIONE OBBLIGATORIA — PREVISIONE FUTURA:
Dopo "**Gestione Rischio**" devi includere SEMPRE questa sezione con valori numerici reali:

**Previsione Futura** (al {projection_end_date}):
- **Bias Proiezione**: [Bullish / Bearish / Neutrale] — [motivazione in 1 frase]
- **Prezzo Centrale**: [prezzo numerico stimato alla data {projection_end_date}]
- **Entry Proiezione**: [prezzo di ingresso ottimale per operare nella direzione della proiezione]
- **Stop Loss Proiezione**: [prezzo che invaliderebbe la proiezione]
- **Target Proiezione**: [prezzo obiettivo da raggiungere entro {projection_end_date}]
- Scenario Rialzista: [prezzo massimo atteso entro {projection_end_date}]
- Scenario Ribassista: [prezzo minimo atteso entro {projection_end_date}]

Tutti i valori devono essere prezzi numerici espliciti (es. 3200, non "intorno ai massimi").
Basa la previsione su: bias macro, struttura di mercato, momentum e livelli S/R chiave.
"""

        query = f"""
ASSET: {nome_asset}

SENTIMENT MACRO (tua analisi precedente):
{macro_sentiment}

ANALISI TEAM TECNICO:
{sintesi_tecnica}

Ora consulta la tua skill 'trading-verdict-synthesizer' e produci il VERDETTO FINALE operativo in DUE SEZIONI SEPARATE.

══════════════════════════════════════
SEZIONE 1 — SETUP CORRENTE (SEMPRE OBBLIGATORIA)
══════════════════════════════════════
Applica il decision framework professionale (no-trade filters, confluence score) e scrivi NELL'ORDINE ESATTO:

**Bias Primario**: [Bullish / Bearish / Neutrale / NO TRADE] — [motivazione]
**Struttura di Mercato**: [struttura HH+HL / LH+LL / laterale su 1D e 4H]
**Confluenza**: [score 1-5] — [fattori]
**Entry Suggerita**: [PREZZO NUMERICO] — [tipo] — [condizione di trigger]
**Stop Loss**: [PREZZO NUMERICO] — [metodologia] — [motivazione]
**Target 1**: [PREZZO NUMERICO] — [metodo] — [R:R]
**Target 2**: [PREZZO NUMERICO] — [metodo] — [R:R]
**Gestione Rischio**:
- R:R minimo raggiunto: [Sì/No — ratio]
- Qualità del setup: [Alta/Media/Bassa]
- Raccomandazione dimensionamento: [% capitale]

> [!IMPORTANT]
> [confluenza macro+tecnica, segnale VSA, fattore di rischio, cosa invaliderebbe il trade]
{proiezione_section}
IMPORTANTE:
- Rispondi ESCLUSIVAMENTE in italiano.
- La Sezione 1 è SEMPRE obbligatoria. I campi **Entry Suggerita**, **Stop Loss**, **Target 1**, **Target 2** sono il setup CORRENTE e devono contenere prezzi numerici reali.
- I campi "Entry Proiezione", "Stop Loss Proiezione", "Target Proiezione" appartengono SOLO alla Sezione 2 (Previsione Futura) e non sostituiscono quelli della Sezione 1.
- Inizia direttamente con '**Bias Primario**:'.
"""
        logger.info(f"[AGNO MACRO] Generazione verdetto finale per {nome_asset} (proiezione al {projection_end_date or 'N/D'})...")
        response = self.agent.run(query)
        return _rimuovi_intro_inglese(response.content, marker="**Bias Primario**")
