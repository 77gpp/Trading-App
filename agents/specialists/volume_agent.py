import os
import google.generativeai as genai
from loguru import logger

class VolumeAgent:
    """Specialista in Analisi dei Volumi e Volume Profile."""
    
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def analizza(self, data_summary, context_skills=""):
        """Esegue l'analisi dei volumi."""
        logger.info("[VOLUME AGENT] Analisi in corso...")
        
        prompt = f"""
        SEI UN MAESTRO DI VSA (VOLUME SPREAD ANALYSIS - TIPO WYCKOFF O TOM WILLIAMS).
        Analizza i volumi sui dati forniti:
        
        DATI MERCATO:
        {data_summary}
        
        SKILL DI RIFERIMENTO:
        {context_skills}
        
        DOCUMENTA:
        1. Relazione Sforzo vs Risultato (Volume vs Spread barra).
        2. Segnali di Accumulazione o Distribuzione.
        3. Livelli di Volume Profile significativi (POC, VA).
        
        Rispondi in italiano.
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            return f"### Analisi Volumi\n{response.text}"
        except Exception as e:
            logger.error(f"Errore VolumeAgent: {e}")
            return "Errore nell'analisi dei volumi."
