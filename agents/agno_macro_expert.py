import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb
from loguru import logger
import settings

class AgnoMacroExpert:
    """Strategist Macroeconomico V5 (Configurable & Free)."""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_id = settings.MODEL_MACRO_EXPERT
        self.db_path = settings.DATABASE_PATH
        self.macro_file = os.path.join(settings.MACRO_LIBRARY_DIR, "macro_fundamentals.md")
        
        # 1. Configurazione Storage Locale (SQLite su Mac)
        self.storage = None
        if settings.STORAGE_LOCATION == "local":
            self.storage = SqliteDb(
                session_table="macro_expert_session",
                db_file=self.db_path
            )
            logger.info(f"[AGNO MACRO] Usando storage locale: {self.db_path}")

        # 2. Inizializzazione Agente
        # Usiamo le istruzioni come 'Base di Conoscenza' se il file è piccolo, 
        # o carichiamo il file come contesto per l'Agentic File Search.
        content = ""
        if os.path.exists(self.macro_file):
            with open(self.macro_file, "r") as f:
                content = f.read()
        
        self.agent = Agent(
            name="Macro Strategist",
            model=Gemini(id=self.model_id, api_key=self.api_key),
            description="Sei un Senior Macro Strategist. Hai accesso ai fondamentali macro del sistema.",
            instructions=[
                "Analizza lo scenario globale basandoti sui fondamentali forniti nel contesto.",
                f"CONTESTO MACRO ESTRATTO DALLA LIBRERIA:\n{content[:5000]}...", # Limitiamo per sicurezza nel prompt, ma Gemini regge molto di più
                "Segui un ragionamento a 3 step: Analisi Indicatori -> Analisi Dollaro -> Sintesi Sentiment.",
                "Fornisci sempre un bias chiaro: Risk-On (Bullish) o Risk-Off (Bearish).",
            ],
            db=self.storage,
            num_history_messages=3,
            markdown=True,
        )
        logger.success(f"[AGNO] Agente Macro Expert pronto con modello: {self.model_id}")

    def analizza(self, query="Analizza l'attuale scenario globale"):
        """Esegue l'analisi macro strategica."""
        logger.info(f"[AGNO MACRO] Esecuzione analisi: {query}")
        response = self.agent.run(query)
        return response.content
