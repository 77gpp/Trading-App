import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from loguru import logger
import Calibrazione

class AgnoMacroExpert:
    """Strategist Macroeconomico V5 (Configurable & Free)."""
    
    def __init__(self):
        self.api_key = Calibrazione.GEMINI_API_KEY
        self.model_id = Calibrazione.MODEL_MACRO_EXPERT
        self.db_path = Calibrazione.DATABASE_PATH
        self.macro_file = os.path.join(Calibrazione.MACRO_LIBRARY_DIR, "macro_fundamentals.md")
        
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
        
        content = ""
        if os.path.exists(self.macro_file):
            with open(self.macro_file, "r") as f:
                content = f.read()
        
        # Otteniamo il modello (Groq/Qwen o Gemini)
        llm_model = get_model(self.model_id)
        
        self.agent = Agent(
            name="Macro Strategist",
            model=llm_model,
            description="Sei un Senior Macro Strategist. Hai accesso ai fondamentali macro, alle news web e ai dati finanziari real-time.",
            tools=[DuckDuckGoTools(), YFinanceTools(enable_stock_price=True, enable_analyst_recommendations=True, enable_company_info=False)],
            instructions=[
                "Analizza lo scenario globale basandoti sui fondamentali forniti nel contesto, sulle news web e sui dati finanziari real-time.",
                f"CONTESTO MACRO ESTRATTO DALLA LIBRERIA:\n{content[:5000]}...",
                "Utilizza il tool DuckDuckGo per cercare notizie recenti sull'asset richiesto (es. 'Gold news today').",
                "Utilizza il tool YFinance per ottenere il prezzo attuale e la tendenza dell'asset (es. ticker 'GC=F' per l'Oro).",
                "IMPONI SEMPRE un'analisi volumetrica approfondita (VSA/Wyckoff) come filtro primario per il Team Tecnico.",
                "Segui un ragionamento a 4 step: Prezzo/Volumi -> News/Dati -> Analisi Indicatori -> Sintesi Sentiment.",
                "Fornisci sempre un bias chiaro: Risk-On (Bullish) o Risk-Off (Bearish).",
            ],
            db=self.storage,
            num_history_messages=3,
            markdown=True,
        )
        logger.success(f"[AGNO] Agente Macro Expert pronto con modello: {llm_model.id}")

    def analizza(self, query="Analizza l'attuale scenario globale"):
        """Esegue l'analisi macro strategica."""
        logger.info(f"[AGNO MACRO] Esecuzione analisi: {query}")
        response = self.agent.run(query)
        return response.content
