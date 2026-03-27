import os
import sys
import time
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
        Master Flow V5 (Modalità Sequenziale Salva-Quota).
        """
        logger.info(f"\n{'='*60}\nAVVIO ANALISI SEQUENZIALE su {nome_asset}\n{'='*60}")
        
        # 1. Step 1: Analisi Macro (The Strategist)
        if settings.AGENT_MACRO_ENABLED:
            try:
                query_macro = f"{nome_asset} news and global macro sentiment today"
                macro_sentiment = self.macro_expert.analizza(query_macro)
            except Exception as e:
                logger.warning(f"Errore durante l'analisi macro (tool): {e}. Procedo con sentiment neutrale.")
                macro_sentiment = "Il sistema di ricerca news ha avuto un problema tecnico. Procedi basandoti esclusivamente sui dati tecnici OHLCV e sulla tua conoscenza generale."
            
            logger.info(f"Sentiment Macro ottenuto. Attesa 25s di sicurezza...")
            time.sleep(25)
        else:
            logger.info("[SUPERVISORE] Analisi Macro disattivata in settings.py. Salto lo Step 1.")
            macro_sentiment = "Analisi Macro Saltata (Bias Neutrale)"

        # Preparazione dati per i tecnici (semplificati per risparmiare token)
        ctx_summary = f"""
        DATI 1H (ultime candele):
        {data_dict["1h"].tail(20).to_string()}
        
        DATI 1D (ultime candele):
        {data_dict["1d"].tail(10).to_string()}
        """
        
        # 2. Step 2: Analisi Tecnica Sequenziale
        results_tech = {}
        
        # Elenco agenti da interrogare (se attivi)
        specialisti = [
            ("Pattern Analyst", settings.AGENT_PATTERN_ENABLED),
            ("Trend Analyst", settings.AGENT_TREND_ENABLED),
            ("SR Analyst", settings.AGENT_SR_ENABLED),
            ("Volume Analyst", settings.AGENT_VOLUME_ENABLED)
        ]

        logger.info(f"Inizio analisi tecnica sequenziale (4 specialisti)...")
        for nome, attivo in specialisti:
            if attivo:
                logger.info(f"Interrogazione {nome}...")
                results_tech[nome] = self.tech_team.analizza_specialista(nome, ctx_summary, macro_sentiment)
                logger.info(f"Risposta {nome} ricevuta. Attesa 25s...")
                time.sleep(25)
            else:
                results_tech[nome] = "Analisi Disattivata"

        # 3. Step 3: Sintesi Finale (Orchestrazione nel Supervisor)
        logger.info("Generazione verdetto finale...")
        
        report_definitivo = f"""
# REPORT TRADING AI: {nome_asset}

## 🌎 ANALISI MACROECONOMICA
{macro_sentiment}

## 📊 RISULTATI TEAM TECNICO
- **Trend**: {results_tech.get('Trend Analyst', 'N/D')}
- **Volumi**: {results_tech.get('Volume Analyst', 'N/D')}
- **Pattern**: {results_tech.get('Pattern Analyst', 'N/D')}
- **S/R**: {results_tech.get('SR Analyst', 'N/D')}

## 🚀 VERDETTO FINALE
L'analisi combinata è basata sugli agenti attualmente ATTIVI nel sistema. 
(Configurazione personalizzata in settings.py)
        """
        
        return report_definitivo

if __name__ == "__main__":
    from data_fetcher import DataFetcher
    
    def test_v5():
        supervisore = SupervisorAgent()
        # Usiamo Oro per il test
        data = DataFetcher.get_mtf_data("GC=F", days=60)
        report = supervisore.analizza_asset(data, "GC=F")
        print("\n--- REPORT TRADING V5 (SEQUENZIALE) ---")
        print(report)

    test_v5()
