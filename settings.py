import os
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURAZIONE MODELLI LLM (Economici ed Efficienti) ---
MODEL_MACRO_EXPERT = "gemini-2.0-flash"
MODEL_TECH_ORCHESTRATOR = "gemini-2.0-flash"
MODEL_TECH_SPECIALISTS = "gemini-2.0-flash"

# --- CONFIGURAZIONE STORAGE LOCALE ---
STORAGE_LOCATION = "local"
DATABASE_PATH = "storage/memory/trading_system.db"

# --- PERCORSI LIBRERIE ---
SKILLS_LIBRARY_DIR = "skills_library"
MACRO_LIBRARY_DIR = "macro_library"
BOOKS_DIR = "data/books"

# --- API KEYS ---
# Vengono lette dal file .env (assicurati che sia presente GEMINI_API_KEY)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
