import os
import sys
import time
from dotenv import load_dotenv
import google.generativeai as genai
from loguru import logger

# Aggiungiamo il path per poter importare i moduli dalle altre cartelle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

class MacroExpertAgent:
    """
    Agente Senior Macroeconomico (Macro Strategist).
    Centralizza l'analisi su indicatori, politica monetaria e forza del dollaro (DXY).
    Utilizza il file Master Skill 'macro_fundamentals.md' come base di conoscenza.
    """
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("Nessuna GEMINI_API_KEY trovata per il Macro Expert Agent.")
        else:
            genai.configure(api_key=self.api_key)
            
        # Modello ottimizzato per analisi e ragionamento logico
        self.model_name = "gemini-1.5-flash" 
        self.master_skill_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
            "macro_library", 
            "macro_fundamentals.md"
        )
        logger.info(f"[MACRO EXPERT] Inizializzato con file master: {os.path.basename(self.master_skill_file)}")

    def analizza_scenario_globale(self):
        """
        Analisi avanzata dello scenario macroeconomico globale.
        Carica il file master delle skill e produce un report di alto livello.
        """
        logger.info("[MACRO EXPERT] Generazione analisi macroeconomica profonda...")
        
        if not os.path.exists(self.master_skill_file):
            logger.error("File master macro_fundamentals.md non trovato!")
            return "Errore: Libreria macro mancante."

        try:
            # 1. Caricamento Master Skill File su Gemini File API
            logger.info("Sincronizzazione 'Cervello Macro' con Gemini...")
            g_file = genai.upload_file(path=self.master_skill_file, mime_type="text/plain")
            while g_file.state.name == "PROCESSING":
                time.sleep(1)
                g_file = genai.get_file(g_file.name)

            # 2. Prompt Analitico Senior
            prompt = """
            AGISCI COME UN MACRO STRATEGIST DI UN HEDGE FUND.
            Il tuo obiettivo è analizzare il mercato globale usando ESATTAMENTE le logiche 
            contenute nel file 'MASTER FILE: COMPETENZE MACROECONOMICHE GLOBALI' allegato.
            
            Esegui un'analisi in 3 step:
            
            **Step 1: Lettura Indicatori e Salute Economica**
            Identifica le attuali tendenze di PIL, Inflazione (CPI) e Occupazione (NFP) basandoti
            sulla tua conoscenza aggiornata ed applicando le logiche del file (es. impatto inflazione sul Dollaro).
            
            **Step 2: Dinamiche del Dollaro (DXY)**
            Analizza la forza del Dollaro. È in una fase di Safe Haven? Sta pesando sulle Commodities?
            Applica le correlazioni descritte nella Sezione 3 del file.
            
            **Step 3: Sintesi e Verdetto Globale**
            Riassumi lo scenario come: 
            - Risk-On (Bullish per Azionario, Bearish per Gold/DXY) 
            - Risk-Off (Bearish per Azionario, Bullish per Gold/DXY)
            - Stagflazione (Pericolo Shock Energetico)
            
            Fornisci un verdetto operativo per il SupervisorAgent.
            Rispondi in italiano con tono professionale e tagliente.
            """
            
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content([g_file, prompt])
            
            analisi_finale = response.text
            
            # Pulizia immediata
            genai.delete_file(g_file.name)
            logger.info("[MACRO EXPERT] Analisi completata con successo.")
            
            return analisi_finale

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

if __name__ == "__main__":
    macro = MacroExpertAgent()
    print(macro.analizza_scenario_globale())
