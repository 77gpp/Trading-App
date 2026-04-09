import os
from dotenv import load_dotenv

load_dotenv()

# --- PROVIDER SELEZIONATO (Scegli tra 'gemini' o 'qwen') ---
LLM_PROVIDER = "qwen" 

# --- CONFIGURAZIONE MODELLI ---
# Gemini si occupa della ricerca intelligente nei libri (Agentic Search)
MODEL_KNOWLEDGE_SEARCH = "gemini-2.0-flash"

# Qwen su Groq si occupa dell'analisi e del ragionamento
MODEL_MACRO_EXPERT = "qwen/qwen3-32b"
MODEL_TECH_ORCHESTRATOR = "qwen/qwen3-32b"
MODEL_TECH_SPECIALISTS = "qwen/qwen3-32b"
# Modello per Skill Selector: senza thinking mode, ottimizzato per output JSON puro
MODEL_SKILL_SELECTOR = "llama-3.3-70b-versatile"

# --- THINKING MODE (solo per modelli Qwen 3 su Groq) ---
# True  = il modello ragiona in profondità prima di rispondere (più lento, analisi più ricca)
# False = ragionamento disabilitato (risposta diretta, più veloce, testo senza preamble inglese)
# Nota: il post-processing rimuove il preamble inglese anche con thinking attivo,
#       ma disabilitarlo elimina il problema alla radice.
QWEN_THINKING_ENABLED = True

# --- CONFIGURAZIONE TEMPERATURE ---
# 0.0 = Determinismo (nessuna casualità, ideale per estrazione dati e selezione tool)
# 0.7 = Default (bilanciato tra logica e creatività linguistica, ideale per report)
TEMPERATURE_KNOWLEDGE_SEARCH = 0.0   # Ricerca nei libri: precisione massima
TEMPERATURE_MACRO_EXPERT = 0.7       # Analisi Macro: deve saper argomentare
TEMPERATURE_TECH_ORCHESTRATOR = 0.7  # Orchestrator: gestione team equilibrata
TEMPERATURE_TECH_SPECIALISTS = 0.7   # Specialisti (Pattern, SR, etc.): analisi tecnica
TEMPERATURE_SKILL_SELECTOR = 0.0     # Scelta Strumenti: stabilità e ripetibilità

# --- CONFIGURAZIONE STORAGE LOCALE ---
STORAGE_LOCATION = "local"
DATABASE_PATH = "storage/memory/trading_system.db"

# --- ATTIVAZIONE AGENTI (Metti True per attivare, False per disattivare) ---
AGENT_MACRO_ENABLED = True      # Analisi Notizie e Sentiment Globale
DEFAULT_PROJECTION_DAYS = 5    # Giorni di proiezione futura predefiniti (es. 30 giorni)
ALPACA_NEWS_LIMIT = 5000         # Numero massimo di notizie da scaricare da Alpaca Markets
DUCKDUCKGO_NEWS_LIMIT = 5000    # Numero massimo di risultati di ricerca da DuckDuckGo

# --- ANALISI TECNICA: PERIODI (Numero di Candele) ---
TECH_SHORT_TERM_CANDLES = 100    # Breve Termine (Grafico 1h) - es. ultime 100 ore
TECH_MID_TERM_CANDLES = 100      # Medio Termine (Grafico 4h) - es. ultime 100 candele da 4 ore
TECH_LONG_TERM_CANDLES = 60      # Lungo Termine (Grafico 1d) - es. ultimi 60 giorni di borsa

AGENT_PATTERN_ENABLED = True    # Analisi Pattern Candele (Joe Ross/Nison)
AGENT_TREND_ENABLED = True      # Analisi Trend e Medie Mobili
AGENT_SR_ENABLED = True         # Analisi Supporti e Resistenze
AGENT_VOLUME_ENABLED = True     # Analisi Volumi (Wyckoff/VSA)

# --- PERCORSI LIBRERIE ---
SKILLS_LIBRARY_DIR = "skills_library"

# Skill per l'agente Macro Strategist
MACRO_SKILL_DIR = os.path.join(SKILLS_LIBRARY_DIR, "macro-strategist")

# Skill professionale per la sintesi del verdetto finale
# Contiene: decision-framework, risk-management, no-trade-filters
VERDICT_SKILL_DIR = os.path.join(SKILLS_LIBRARY_DIR, "trading-verdict-synthesizer")

# Skill per gli agenti del Technical Trading Desk:
# tutti e 4 gli specialisti (Pattern, Trend, SR, Volume) condividono gli stessi 6 libri.
# Ogni cartella contiene un SKILL.md con frontmatter Agno + contenuto del libro.
TECHNICAL_SKILLS_DIRS = [
    os.path.join(SKILLS_LIBRARY_DIR, "encyclopedia_of_chart_patterns"),         # Bulkowski
    os.path.join(SKILLS_LIBRARY_DIR, "japanese_candlestick_charting"),           # Nison
    os.path.join(SKILLS_LIBRARY_DIR, "joe_ross_daytrading"),                     # Joe Ross
    os.path.join(SKILLS_LIBRARY_DIR, "larry_williams_long_term_secrets"),        # L. Williams
    os.path.join(SKILLS_LIBRARY_DIR, "murphy_analisi_tecnica"),                  # Murphy
    os.path.join(SKILLS_LIBRARY_DIR, "technical_analysis_multiple_timeframes"),  # B. Shannon
]

MACRO_LIBRARY_DIR = "macro_library"
BOOKS_DIR = "data/books"

# --- API KEYS ---
# Assicurati di aggiungere GROQ_API_KEY nel tuo file .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
