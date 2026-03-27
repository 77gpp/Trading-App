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

# --- CONFIGURAZIONE STORAGE LOCALE ---
STORAGE_LOCATION = "local"
DATABASE_PATH = "storage/memory/trading_system.db"

# --- ATTIVAZIONE AGENTI (Metti True per attivare, False per disattivare) ---
AGENT_MACRO_ENABLED = True      # Analisi Notizie e Sentiment Globale

AGENT_PATTERN_ENABLED = True    # Analisi Pattern Candele (Joe Ross/Nison)
AGENT_TREND_ENABLED = True      # Analisi Trend e Medie Mobili
AGENT_SR_ENABLED = True         # Analisi Supporti e Resistenze
AGENT_VOLUME_ENABLED = True     # Analisi Volumi (Wyckoff/VSA)

# --- PERCORSI LIBRERIE ---
SKILLS_LIBRARY_DIR = "skills_library"
MACRO_LIBRARY_DIR = "macro_library"
BOOKS_DIR = "data/books"

# --- API KEYS ---
# Assicurati di aggiungere GROQ_API_KEY nel tuo file .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
