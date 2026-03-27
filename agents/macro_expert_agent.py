import os
import sys
from loguru import logger
from agno.agent import Agent
import settings

# Aggiungiamo il path per poter importare i moduli dalle altre cartelle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.model_factory import get_model

class MacroExpertAgent:
    """
    Agente Senior Macroeconomico (Macro Strategist).
    Centralizza l'analisi su indicatori, politica monetaria e forza del dollaro (DXY).
    Utilizza il file Master Skill 'macro_fundamentals.md' come base di conoscenza.
    """
    
    def __init__(self, model_id=None):
        # Usiamo il model_factory per ottenere il modello corretto
        self.model = get_model(model_id)
            
        # Modello ottimizzato per analisi e ragionamento logico
        self.master_skill_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
            "macro_library", 
            "macro_fundamentals.md"
        )
        
        # Inizializzazione Agente Agno
        self.agent = Agent(
            model=self.model,
            name="Macro Strategist Senior",
            description="Senior Macro Strategist di un Hedge Fund.",
            instructions=[
                "Analizza lo scenario globale applicando le logiche macroeconomiche fornite.",
                "Segui un ragionamento a 3 step: Indicatori/Salute -> Correlazioni Dollaro -> Verdetto Sentiment.",
                "Rispondi in italiano con tono professionale e tagliente."
            ]
        )
        logger.info(f"[MACRO EXPERT] Inizializzato con file master: {os.path.basename(self.master_skill_file)}")

    def analizza_scenario_globale(self):
        """
        Analisi avanzata dello scenario macroeconomico globale.
        Carica il file master delle skill e produce un report di alto livello.
        """
        logger.info("[MACRO EXPERT] Generazione analisi macroeconomica profonda con Qwen/Groq...")
        
        if not os.path.exists(self.master_skill_file):
            logger.error("File master macro_fundamentals.md non trovato!")
            return "Errore: Libreria macro mancante."

        try:
            # 1. Caricamento Master Skill File come testo (per Qwen/Groq)
            with open(self.master_skill_file, "r") as f:
                content = f.read()

            # 2. Prompt Analitico Senior
            prompt = f"""
            Il tuo obiettivo è analizzare il mercato globale usando ESATTAMENTE le logiche 
            contenute nel file 'MASTER FILE: COMPETENZE MACROECONOMICHE GLOBALI' qui di seguito:
            
            --- INIZIO COMPETENZE ---
            {content[:8000]}
            --- FINE COMPETENZE ---
            
            Esegui un'analisi in 3 step:
            
            **Step 1: Lettura Indicatori e Salute Economica**
            Identifica le attuali tendenze di PIL, Inflazione (CPI) e Occupazione (NFP) applicando le logiche del file.
            
            **Step 2: Dinamiche del Dollaro (DXY)**
            Analizza la forza del Dollaro. È in una fase di Safe Haven? Sta pesando sulle Commodities?
            
            **Step 3: Sintesi e Verdetto Globale**
            Riassumi lo scenario come: 
            - Risk-On (Bullish per Azionario, Bearish per Gold/DXY) 
            - Risk-Off (Bearish per Azionario, Bullish per Gold/DXY)
            - Stagflazione (Pericolo Shock Energetico)
            
            Fornisci un verdetto operativo finale.
            """
            
            response = self.agent.run(prompt)
            logger.info("[MACRO EXPERT] Analisi completata con successo.")
            
            return response.content

        except Exception as e:
            logger.error(f"Errore durante l'analisi macro esperta: {e}")
            return f"Errore: {e}"

if __name__ == "__main__":
    # Test stand-alone dell'agente macro
    macro = MacroExpertAgent()
    print("\n" + "="*50)
    print("TEST AGENTE MACRO SENIOR")
    print("="*50 + "\n")
    report = macro.analizza_scenario_globale()
    print(report)
