import os
import google.generativeai as genai
from loguru import logger

class TrendAgent:
    """Specialista in Trend e Momentum (Medie Mobili, RSI, MACD)."""
    
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def analizza(self, data_summary, context_skills=""):
        """Esegue l'analisi di trend e momentum."""
        logger.info("[TREND AGENT] Analisi in corso...")
        
        prompt = f"""
        SEI UN ANALISTA TECNICO ESPERTO DI TREND (TIPO JOHN MURPHY O MARTIN PRING).
        Analizza i trend e lo slancio del prezzo sui dati forniti:
        
        DATI MERCATO:
        {data_summary}
        
        SKILL DI RIFERIMENTO:
        {context_skills}
        
        DOCUMENTA:
        1. Direzione del Trend (Primario, Secondario, Terziario).
        2. Analisi del Momentum (Ipercomprato/Ipervenduto, Divergenze).
        3. Livelli di stop-loss logici per il trend attuale.
        
        Rispondi in italiano.
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            return f"### Analisi Trend & Momentum\n{response.text}"
        except Exception as e:
            logger.error(f"Errore TrendAgent: {e}")
            return "Errore nell'analisi del trend."
