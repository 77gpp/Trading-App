import os
from google import genai
from loguru import logger
import Calibrazione

class ContextExpanderAgent:
    """
    Agente di Ricerca Intelligente nei Libri (Gemini Agentic File Search).
    Carica i PDF su Google Cloud e permette ricerche semantiche veloci.
    """

    def __init__(self):
        self.api_key = Calibrazione.GEMINI_API_KEY
        self.model_id = Calibrazione.MODEL_KNOWLEDGE_SEARCH
        self.books_dir = Calibrazione.BOOKS_DIR

        self.client = genai.Client(api_key=self.api_key) if self.api_key else None
        self.uploaded_files = {}  # Cache locale dei file caricati

    def _sync_books(self):
        """Sincronizza i libri locali con Gemini File API."""
        logger.info("[KNOWLEDGE] Mirroring dei libri su Gemini File API...")

        if not self.client:
            logger.error("[KNOWLEDGE] Client Gemini non inizializzato: API key mancante.")
            return

        if not os.path.exists(self.books_dir):
            logger.error(f"Cartella libri non trovata: {self.books_dir}")
            return

        # Recuperiamo la lista dei file già presenti su Gemini per evitare duplicati
        existing_remote_files = {f.display_name: f for f in self.client.files.list()}

        for filename in os.listdir(self.books_dir):
            if filename.endswith(".pdf"):
                path = os.path.join(self.books_dir, filename)

                if filename in existing_remote_files:
                    logger.debug(f"Libro '{filename}' già presente su Gemini.")
                    self.uploaded_files[filename] = existing_remote_files[filename]
                else:
                    logger.info(f"Caricamento nuovo libro: {filename}...")
                    g_file = self.client.files.upload(
                        file=path,
                        config={"display_name": filename}
                    )
                    self.uploaded_files[filename] = g_file

        logger.success(f"[KNOWLEDGE] {len(self.uploaded_files)} libri pronti per la ricerca.")

    def search_knowledge(self, query):
        """Esegue una ricerca semantica nei libri caricati."""
        logger.info(f"[KNOWLEDGE] Ricerca intelligente nei libri: '{query}'...")

        if not self.client:
            return "Errore: API key Gemini non configurata."

        if not self.uploaded_files:
            self._sync_books()

        if not self.uploaded_files:
            return "Nessun libro caricato."

        # Prendiamo i primi 5 file per non superare i limiti di contesto se necessario
        files_to_use = list(self.uploaded_files.values())[:5]

        prompt = f"""
        SEI UN ESPERTO DI TRADING CHE ACCEDE ALLA SUA LIBRERIA PERSONALE.
        Cerca nei documenti allegati la risposta alla seguente domanda:

        DOMANDA: {query}

        REGOLE:
        1. Cita il nome del libro da cui provengono le informazioni.
        2. Sii sintetico ma tecnico.
        3. Se non trovi nulla di specifico, dì che la libreria non contiene riferimenti a questo tema.

        Rispondi in italiano.
        """

        try:
            contents = files_to_use + [prompt]
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=contents
            )
            return response.text
        except Exception as e:
            logger.error(f"Errore ricerca Gemini: {e}")
            return f"Errore durante la ricerca nei libri: {e}"
