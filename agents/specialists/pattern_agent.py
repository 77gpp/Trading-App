import os
import google.generativeai as genai
from loguru import logger

class PatternAgent:
    """Specialista in Pattern Recognition (Candlestick e Formazioni Grafiche)."""
    
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def analizza(self, data_summary, context_skills=""):
        """Esegue l'analisi dei pattern sui dati forniti."""
        logger.info("[PATTERN AGENT] Analisi in corso...")
        
        prompt = f"""
        SEI UN ESPERTO DI PATTERN RECOGNITION (TIPO THOMAS BULKOWSKI O STEVE NISON).
        Analizza i seguenti dati OHLCV e cerca pattern di inversione o continuazione:
        
        DATI MERCATO:
        {data_summary}
        
        SKILL DI RIFERIMENTO:
        {context_skills}
        
        DOCUMENTA:
        1. Pattern Candlestick rilevati (es: Engulfing, Pin Bar, Doji).
        2. Formazioni grafiche in sviluppo (es: Double Top, Cup and Handle).
        3. Affidabilità del pattern nel contesto attuale.
        
        Rispondi in italiano.
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            return f"### Analisi Pattern\n{response.text}"
        except Exception as e:
            logger.error(f"Errore PatternAgent: {e}")
            return "Errore nell'analisi dei pattern."
