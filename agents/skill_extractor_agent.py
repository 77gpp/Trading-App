import os
import json
import time
from dotenv import load_dotenv
from loguru import logger
import google.generativeai as genai

# Caricamento delle variabili d'ambiente dal file .env
load_dotenv()

class SkillExtractorAgent:
    """
    Agente dedicato all'estrazione di regole di trading (Skill)
    direttamente da un documento/libro usando Gemini File API.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("Nessuna GEMINI_API_KEY trovata. Controlla le variabili d'ambiente.")
        else:
            genai.configure(api_key=self.api_key)
            
        # Modello consigliato per documenti complessi
        self.model_name = "gemini-2.5-flash"  # O gemini-1.5-pro a seconda del tier

    def upload_book(self, filepath: str):
        """
        Carica un file (es. PDF) su Gemini File Store.
        Restituisce un oggetto file di Gemini che contiene URI e nome.
        """
        logger.info(f"Inizio upload del file '{filepath}' su Gemini File API...")
        try:
            sample_file = genai.upload_file(path=filepath)
            logger.info(f"File caricato con successo. URI: {sample_file.uri}")
            
            # Attendiamo che il file venga processato (se è molto grande)
            while sample_file.state.name == "PROCESSING":
                logger.debug("Il file è in elaborazione. Attendo 10 secondi...")
                time.sleep(10)
                # Dobbiamo aggiornare l'oggetto per ottenere il nuovo stato
                sample_file = genai.get_file(sample_file.name)
                
            if sample_file.state.name == "FAILED":
                raise ValueError("Elaborazione del file fallita da parte di Gemini.")
                
            return sample_file
            
        except Exception as e:
            logger.error(f"Errore durante l'upload del file: {e}")
            raise

    def extract_skills_da_file(self, gemini_file) -> str:
        """
        Invia un prompt agentico al modello allegando il file caricato,
        richiedendo l'astrazione e l'estrazione delle Skill in formato Markdown testuale.
        Restituisce l'output testuale direttamente formattato.
        """
        logger.info(f"Avvio estrazione agentica delle Skill (in formato MD) per il file URI {gemini_file.uri}")
        
        prompt = """
        Sei un esperto sviluppatore di sistemi di trading quantitativo ed intelligenza artificiale.
        Il tuo compito è analizzare il libro/documento allegato ed estrarre TUTTE le tecniche di trading,
        pattern grafici (es. candele giapponesi), regole o indicazioni logiche menzionate. 
        Menzionale TUTTE, non importi alcun limite artificiale al numero di pattern da scansionare.

        Devi restituire l'estrazione ESCLUSIVAMENTE copiando ed applicando l'esatto formato Markdown qui sotto per OGNI skill (ripeti il modulo per ognuna). 
        Non includere altra grammatica colloquiale prima o dopo. Non usare un array JSON. Solo intestazioni Markdown come segue:

        ## [Nome Originale o Standard della Tecnica/Pattern]
        **Libro/File Originale:** [Inserisci il titolo del libro e aggiungi l'URI qui tra parentesi]
        **Contesto/Pagina:** [La citazione, il capitolo o la pagina in cui se ne parla]
        **Descrizione:** [Una descrizione chiara di come funziona e che scopo ha]
        **Logica Tecnica/Pseudocodice:** [Le regole puramente tecniche per l'implementazione in codice]
        
        ---
        """
        
        # Inizializziamo il modello, garantendo una risposta testuale fluida e senza vincoli JSON (così da scongiurare gli errori syntax length-limit)
        model = genai.GenerativeModel(model_name=self.model_name)
        
        try:
            response = model.generate_content([gemini_file, prompt])
            logger.info("Estrazione completata dall'Agent Gemini.")
            return response.text
            
        except Exception as e:
            logger.error(f"Errore durante l'estrazione: {e}")
            return ""

    def save_skills_as_markdown(self, markdown_content: str, source_book_name: str, output_dir: str = "../skills_library"):
        """
        Salva la stringa Markdown nativa generata da Gemini in un solo grande file corrispondente al nome del volume.
        """
        if not markdown_content.strip():
            logger.warning("Nessun contenuto Markdown fornito, salto il salvataggio.")
            return

        target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), output_dir))
        os.makedirs(target_dir, exist_ok=True)
        
        safe_name = "".join(c if c.isalnum() or c == " " else "_" for c in source_book_name).replace(" ", "_").lower()
        filename = os.path.join(target_dir, f"{safe_name}.md")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# SKILLS ESTRATTE: {source_book_name}\n\n")
            f.write(markdown_content)
        
        logger.info(f"Salvato con successo L'UNICO FILE AGGREGATO in: {filename}")

if __name__ == "__main__":
    # Esempio basilare di utilizzo se eseguito direttamente (test)
    print("Test Agent Estrattore Skill (Necessita di GEMINI_API_KEY configurata e file dummy.pdf in directory)")
    # agent = SkillExtractorAgent()
    # gemini_f = agent.upload_book("../data/esempio_libro.pdf")
    # extracted = agent.extract_skills_da_file(gemini_f)
    # se estratte: agent.save_skills_as_markdown(extracted)
