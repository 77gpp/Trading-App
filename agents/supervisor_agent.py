import os
import sys
import time
from dotenv import load_dotenv
from loguru import logger
import Calibrazione

# Import dei componenti Agno V5
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.agno_macro_expert import AgnoMacroExpert
from agents.agno_macro_expert import AgnoMacroExpert
from agents.agno_technical_team import AgnoTechnicalTeam
from agents.context_expander_agent import ContextExpanderAgent

load_dotenv()

class SupervisorAgent:
    """
    Controller Multi-Agente V5 (Ibrido: Gemini + Qwen).
    Gestisce il flusso tra:
    - Analisi Macro (Qwen)
    - Ricerca Libri/Knowledge (Gemini Agentic Search)
    - Team Tecnico (Qwen)
    """
    
    def __init__(self):
        # 1. Caricamento Impostazioni Centralizzate
        self.provider = Calibrazione.LLM_PROVIDER
        self.storage_location = Calibrazione.STORAGE_LOCATION
        self.db_path = Calibrazione.DATABASE_PATH
        
        # 2. Inizializzazione Sotto-Agenti
        self.macro_expert = AgnoMacroExpert()
        self.tech_team = AgnoTechnicalTeam()
        self.knowledge_expert = ContextExpanderAgent() # Bibliotecario Gemini
        
        logger.success(f"[AGNO SUPERVISOR] Sistema V5 IBRIDO pronto (Gemini + Qwen).")

    def analizza_asset(self, data_dict, nome_asset):
        """
        Master Flow V5 (Modalità Sequenziale Salva-Quota).
        """
        logger.info(f"\n{'='*60}\nAVVIO ANALISI SEQUENZIALE su {nome_asset}\n{'='*60}")
        
        # 1. Step 1: Analisi Macro (The Strategist)
        if Calibrazione.AGENT_MACRO_ENABLED:
            try:
                query_macro = f"{nome_asset} news and global macro sentiment for the last {Calibrazione.MACRO_ANALYSIS_DAYS} days"
                macro_sentiment = self.macro_expert.analizza(query_macro)
            except Exception as e:
                logger.warning(f"Errore durante l'analisi macro (tool): {e}. Procedo con sentiment neutrale.")
                macro_sentiment = "Il sistema di ricerca news ha avuto un problema tecnico. Procedi basandoti esclusivamente sui dati tecnici OHLCV e sulla tua conoscenza generale."
            
            logger.info(f"Sentiment Macro ottenuto. Attesa 25s di sicurezza...")
            time.sleep(25)
        else:
            logger.info("[SUPERVISORE] Analisi Macro disattivata in Calibrazione.py. Salto lo Step 1.")
            macro_sentiment = "Analisi Macro Saltata (Bias Neutrale)"

        # 2. Step 2: Ricerca Profonda nei Libri (Knowledge Expansion via Gemini)
        logger.info(f"[SUPERVISORE] Interrogazione Biblioteca Gemini per {nome_asset}...")
        try:
            query_knowledge = f"Quali sono le migliori strategie di trading e i pattern più affidabili descritti nei libri per l'asset {nome_asset} in un mercato con sentiment {macro_sentiment}?"
            knowledge_context = self.knowledge_expert.search_knowledge(query_knowledge)
        except Exception as e:
            logger.error(f"Errore nella ricerca libri: {e}")
            knowledge_context = "Nessuna conoscenza specifica estratta dai libri per questa sessione."
        
        # Preparazione dati per i tecnici (semplificati per risparmiare token)
        ctx_summary = f"""
        CONTESTO STRATEGICO (DAI LIBRI):
        {knowledge_context}
        
        DATI 1H (ultime candele):
        {data_dict["1h"].tail(20).to_string()}
        
        DATI 1D (ultime candele):
        {data_dict["1d"].tail(Calibrazione.MACRO_ANALYSIS_DAYS).to_string()}
        """
        
        # 3. Step 3: Analisi Tecnica Sequenziale (Qwen)
        results_tech = {}
        
        # Elenco agenti da interrogare (se attivi)
        specialisti = [
            ("Pattern Analyst", Calibrazione.AGENT_PATTERN_ENABLED),
            ("Trend Analyst", Calibrazione.AGENT_TREND_ENABLED),
            ("SR Analyst", Calibrazione.AGENT_SR_ENABLED),
            ("Volume Analyst", Calibrazione.AGENT_VOLUME_ENABLED)
        ]

        logger.info(f"Inizio analisi tecnica sequenziale (4 specialisti) con contesto ibrido...")
        for nome, attivo in specialisti:
            if attivo:
                logger.info(f"Interrogazione {nome}...")
                results_tech[nome] = self.tech_team.analizza_specialista(nome, ctx_summary, macro_sentiment)
                logger.info(f"Risposta {nome} ricevuta. Attesa 25s...")
                time.sleep(25)
            else:
                results_tech[nome] = "Analisi Disattivata"

        # 4. Step 4: Sintesi Finale (Orchestrazione nel Supervisor)
        logger.info("Generazione verdetto finale...")
        
        report_definitivo = f"""
# REPORT TRADING AI (IBRIDO GEMINI+QWEN): {nome_asset}

## 📖 CONTESTO DALLA LIBRERIA (Strategie Master)
{knowledge_context}

## 🌎 ANALISI MACROECONOMICA E NEWS (FONDAMENTALI)
{macro_sentiment}

## 📊 RISULTATI TEAM TECNICO
- **Trend**: {results_tech.get('Trend Analyst', 'N/D')}
- **Volumi**: {results_tech.get('Volume Analyst', 'N/D')}
- **Pattern**: {results_tech.get('Pattern Analyst', 'N/D')}
- **S/R**: {results_tech.get('SR Analyst', 'N/D')}

## 🚀 VERDETTO FINALE
L'analisi combinata è basata sugli agenti attualmente ATTIVI nel sistema. 
(Configurazione personalizzata in Calibrazione.py)
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
