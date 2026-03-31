import os
from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from loguru import logger
import Calibrazione
from agents.alpaca_news_tool import get_alpaca_news

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
            description="Sei un Senior Macro Strategist. Hai accesso ai fondamentali macro, alle news web (DuckDuckGo), alle news ufficiali Alpaca Markets e ai dati finanziari real-time.",
            tools=[
                DuckDuckGoTools(fixed_max_results=getattr(Calibrazione, "DUCKDUCKGO_NEWS_LIMIT", 10)), 
                YFinanceTools(enable_stock_price=True, enable_analyst_recommendations=True, enable_company_info=False),
                get_alpaca_news
            ],
            instructions=[
                "Analizza lo scenario globale basandoti sui fondamentali forniti nel contesto, sulle news web, sulle notizie Alpaca e sui dati finanziari real-time.",
                f"CONTESTO MACRO ESTRATTO DALLA LIBRERIA:\n{content[:5000]}...",
                f"Utilizza il tool DuckDuckGo per cercare notizie recenti degli ultimi {Calibrazione.MACRO_ANALYSIS_DAYS} giorni sull'asset richiesto.",
                f"Utilizza il tool get_alpaca_news per ottenere le ultime notizie ufficiali di mercato per lo specifico simbolo dall'API di Alpaca Markets.",
                "IMPORTANTE: Per ogni notizia consultata, riporta sempre il Titolo (linkabile all'URL della fonte se disponibile) e cita esplicitamente se la fonte è Alpaca o il Web generico.",
                f"Utilizza il tool YFinance per ottenere il prezzo attuale, i volumi e i dati degli ultimi {Calibrazione.MACRO_ANALYSIS_DAYS} giorni (es. ticker 'GC=F' per l'Oro).",
                "IMPORTANTE: Riporta sempre i dati numerici grezzi prelevati (Ultimo prezzo, Variazione %, Volumi 24h) citando esplicitamente la fonte Yahoo Finance.",
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
