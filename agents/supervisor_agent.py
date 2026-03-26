import os
import sys
from dotenv import load_dotenv
from loguru import logger
import settings

# Import dei componenti Agno V5
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.agno_macro_expert import AgnoMacroExpert
from agents.agno_technical_team import AgnoTechnicalTeam

load_dotenv()

class SupervisorAgent:
    """
    Controller Multi-Agente V5 (Configurable & SQLite Storage).
    Utilizza Agno SDK e Google Gemini.
    """
    
    def __init__(self):
        # 1. Caricamento Impostazioni Centralizzate
        self.api_key = settings.GEMINI_API_KEY
        self.storage_location = settings.STORAGE_LOCATION
        self.db_path = settings.DATABASE_PATH
        
        # 2. Inizializzazione Sotto-Agenti
        self.macro_expert = AgnoMacroExpert()
        self.tech_team = AgnoTechnicalTeam()
        
        logger.success(f"[AGNO SUPERVISOR] Sistema V5 inizializzato con storage {self.storage_location}.")

    def analizza_asset(self, data_dict, nome_asset):
        """
        Master Flow V5 (Settings-Driven).
        """
        logger.info(f"\n{'='*60}\nAVVIO ANALISI V5 (CONFIGURABILE) su {nome_asset}\n{'='*60}")
        
        # 1. Step 1: Analisi Macro (The Strategist)
        # Sfrutta la memoria e la conoscenza fondamentali macro
        macro_sentiment = self.macro_expert.analizza()
        
        # 2. Step 2: Analisi Tecnica Coordinata (Team Analysts)
        # Sfrutta le skill tecniche e il sentiment macro
        # Usiamo 1h e 4h per il sommario tecnico
        ctx_summary = f"""
        TIMEFRAME 1H (Ultime 50 candele):
        {data_dict["1h"].tail(50).to_string()}
        
        TIMEFRAME 1D (Ultime 50 candele):
        {data_dict["1d"].tail(50).to_string()}
        """
        
        report_definitivo = self.tech_team.analizza_asset(ctx_summary, macro_sentiment)
        
        return report_definitivo

if __name__ == "__main__":
    from data_fetcher import DataFetcher
    
    def test_v5():
        supervisore = SupervisorAgent()
        data = DataFetcher.get_mtf_data("BTC/USD", days=10)
        report = supervisore.analizza_asset(data, "BTC/USD")
        print("\n--- REPORT TRADING V5 (CONFIGURABILE) ---")
        print(report)

    test_v5()
