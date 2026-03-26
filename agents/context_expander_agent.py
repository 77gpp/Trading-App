import os
import pypdf
from loguru import logger

class ContextExpanderAgent:
    """
    Agente che espande il contesto leggendo le pagine dei PDF originali.
    Mappa i nomi abbreviati dei libri sui file fisici in data/books/.
    """
    
    def __init__(self, books_dir="data/books"):
        self.books_dir = books_dir
        # Mappatura tra nomi nelle skill MD e file PDF reali
        self.book_map = {
            "Daytrading": "Joe Ross - Daytrading (Merged Clean).pdf",
            "Encyclopedia Of Chart Patterns": "Encyclopedia Of Chart Patterns, 2nd Edition.pdf",
            "Japanese Candlestick Charting": "Japanese Candlestick Charting Techniques 2nd edition 2001.pdf",
            "Long-Term Secrets": "Long-Term Secrets to Short-Term Trading 1999.pdf",
            "Murphy": "Murphy - Analisi Tecnica Dei Mercati Finanziari.pdf",
            "Multiple Timeframes": "Technical Analysis Using Multiple Timeframes - Understand Market Structure and Profit from Trend Alignment.pdf"
        }

    def expand_context(self, book_name, page_number):
        """Estrae il testo di una pagina specifica da un PDF."""
        logger.info(f"[CONTEXT EXPANDER] Ricerca pagina {page_number} del libro '{book_name}'...")
        
        # Risoluzione nome file
        pdf_name = None
        for key in self.book_map:
            if key.lower() in book_name.lower():
                pdf_name = self.book_map[key]
                break
        
        if not pdf_name:
            logger.warning(f"Libro '{book_name}' non trovato nella mappa.")
            return f"Contesto non disponibile per {book_name}."

        pdf_path = os.path.join(self.books_dir, pdf_name)
        if not os.path.exists(pdf_path):
            logger.error(f"File PDF non trovato: {pdf_path}")
            return f"Errore: File PDF {pdf_name} non trovato."

        try:
            reader = pypdf.PdfReader(pdf_path)
            # pypdf usa indici 0-based, le pagine dei libri sono 1-based (solitamente)
            page_idx = int(page_number) - 1
            if page_idx < 0 or page_idx >= len(reader.pages):
                return f"Pagina {page_number} fuori intervallo."
            
            page = reader.pages[page_idx]
            text = page.extract_text()
            logger.success(f"[CONTEXT EXPANDER] Pagina {page_number} estratta con successo ({len(text)} caratteri).")
            return text
        except Exception as e:
            logger.error(f"Errore estrazione PDF: {e}")
            return f"Errore durante la lettura del PDF: {e}"
