import os
import sys
import time
from dotenv import load_dotenv
import google.generativeai as genai
from loguru import logger

# Aggiungiamo il path per poter importare i moduli dalle altre cartelle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

class SupervisorAgent:
    """
    L'Orchestratore Centrale dell'IA (Hybrid Agent).
    Prende i dati di mercato crudi (il dataframe), cerca le regole di trading 
    dell'autore specificato (tramite il sistema Agentic File Search in Markdown)
    e chiede a Gemini di valutare la situazione tecnica di mercato.
    """
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("Nessuna GEMINI_API_KEY trovata per il Supervisor Agent. Controlla il .env.")
        else:
            genai.configure(api_key=self.api_key)
            
        self.model_name = "gemini-2.5-flash"
        logger.info("[SUPERVISOR AGENT] Agente Supervisore pronto e connesso con Gemini API.")
        
    def _get_skill_file(self, autore: str):
        """Cerca il file markdown delle skill dell'autore."""
        target_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills_library")
        # normalizziamo il nome
        safe_name = "".join(c if c.isalnum() or c == " " else "_" for c in autore).replace(" ", "_").lower()
        
        # Possibili varianti
        expected_path = os.path.join(target_dir, f"{safe_name}.md")
        if os.path.exists(expected_path):
            return expected_path
            
        # Fallback nel caso il file si chiami in modo diverso e l'utente passa solo l'autore parziale
        for filename in os.listdir(target_dir):
            if filename.endswith(".md") and safe_name in filename.lower():
                return os.path.join(target_dir, filename)
                
        return None

    def analizza_asset(self, dataframe, nome_asset, autore="Libro Tecnico"):
        logger.info(f"\n[SUPERVISOR AGENT] Avvio Analisi Avanzata su {nome_asset}...")
        
        # 1. Preparazione dei dati di mercato
        # Prendiamo gli ultimi 30 giorni per dare a Gemini un contesto della Price Action recente
        recent_data = dataframe.tail(30).to_string()
        
        # 2. Ricerca del "Libro" (il file MD estratto precedentemente)
        skill_file_path = self._get_skill_file(autore)
        
        # Se non trova il file specifico dell'autore, usa il primo file .md che trova
        if not skill_file_path:
            logger.warning(f"File markdown per {autore} non trovato. Provo ad usare il primo file skill disponibile nella libreria.")
            target_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills_library")
            md_files = [f for f in os.listdir(target_dir) if f.endswith(".md")]
            if md_files:
                skill_file_path = os.path.join(target_dir, md_files[0])
            else:
                return "Errore: NESSUN file Skill MD è stato trovato nella libreria. Estrai prima le skill dal documento."
            
        logger.info(f"Trovato file regole (Skill MD): {skill_file_path}")
        
        # 3. Caricamento in Gemini tramite File API
        logger.info("Upload del file skill su Gemini File API in corso...")
        try:
            gemini_file = genai.upload_file(path=skill_file_path, mime_type="text/plain")
            
            # Attendiamo processo completato
            while gemini_file.state.name == "PROCESSING":
                time.sleep(2)
                gemini_file = genai.get_file(gemini_file.name)
                
            if gemini_file.state.name == "FAILED":
                raise ValueError("Errore durante l'elaborazione del file su Gemini.")
        except Exception as e:
            logger.error(f"Impossibile caricare il file su Gemini: {e}")
            return "Errore di connessione a Gemini."
            
        # 4. Formulazione della query 'Intelligente'
        prompt = f"""
        Sei un Analista Finanziario Senior e un Supervisore AI. Il tuo obiettivo è applicare ESATTAMENTE 
        le strategie di trading che ti fornisco tramite il documento allegato (che contiene le regole estratte dal libro).
        
        Ecco i recenti dati di mercato (Price Action degli ultimi 30 giorni) per l'asset {nome_asset}:
        
        ```text
        {recent_data}
        ```
        
        Il tuo compito è analizzare questi dati grezzi e CONFRONTARLI RIGOROSAMENTE con le regole di trading estratte dal libro/documento allegato.
        
        Fornisci un'analisi strutturata in cui:
        1. **Valutazione della Price Action**: Leggi i dati e riassumi la tendenza in atto (rialzista, ribassista, laterale).
        2. **Applicazione delle Skill**: Dici all'utente analiticamente quali pattern o cautele descritte nel documento allegato si applicano all'attuale situazione dei prezzi (es. l'allineamento dei time-frame o figure specifiche).
        3. **Conclusione Strategica**: Termina in modo chiaro con un verdetto operativo finale (Buy/Hold/Sell/Osservare) spiegando sinteticamente il "perché".
        
        Rispondi in italiano con tono professionale, analitico e formattando tutto in Markdown.
        """
        
        # 5. Esecuzione query ibrida
        logger.info("Avvio analisi IA (Price Action cruda + File Regole via Agentic Search)...")
        model = genai.GenerativeModel(model_name=self.model_name)
        try:
            response = model.generate_content([gemini_file, prompt])
            sintesi_ai = response.text
        except Exception as e:
            logger.error(f"Errore generazione: {e}")
            sintesi_ai = f"Errore durante la generazione Hybrid AI: {e}"
        finally:
            # Pulizia su cloud Gemini
            try:
                genai.delete_file(gemini_file.name)
                logger.info("File temporaneo rimosso da Gemini Store.")
            except Exception as d:
                logger.error(f"Errore nella rimozione file cloud: {d}")
                pass
                
        # 6. Output Finale Ibrido
        report_finale = (
            f"\n{'='*70}\n"
            f"   🧠 RISPOSTA IBRIDA: ANALISI IA AVANZATA SU {nome_asset} \n"
            f"{'='*70}\n\n"
            f"--- 📊 FASE 1: DATI DI INPUT ---\n"
            f"Analisi basata sulla Price Action degli ultimi 30 periodi.\n\n"
            f"--- 📖 FASE 2: RISPOSTA GEMINI (Agentic File Search + Dati) ---\n"
            f"{sintesi_ai}\n\n"
            f"{'='*70}\n"
        )
        
        return report_finale

if __name__ == "__main__":
    # Piccolo test stand-alone
    import pandas as pd
    import numpy as np
    
    print("Avvio test stand-alone...")
    date_rng = pd.date_range(start='2020-01-01', end='2020-12-31', freq='D')
    df_dummy = pd.DataFrame(date_rng, columns=['Date'])
    df_dummy['Close'] = np.random.randint(100, 200, size=(len(date_rng)))
    df_dummy['Open'] = df_dummy['Close'] - np.random.randint(-5, 5, size=(len(date_rng)))
    df_dummy['High'] = df_dummy[['Open', 'Close']].max(axis=1) + np.random.randint(1, 10, size=(len(date_rng)))
    df_dummy['Low'] = df_dummy[['Open', 'Close']].min(axis=1) - np.random.randint(1, 10, size=(len(date_rng)))
    df_dummy['Volume'] = np.random.randint(1000, 2000, size=(len(date_rng)))
    
    # Testiamo il Supervisore cercando le regole dal file presente "murphy"
    sup = SupervisorAgent()
    print(sup.analizza_asset(df_dummy, "ASSET_TEST", "murphy"))
