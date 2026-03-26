import os
import google.generativeai as genai
from loguru import logger

class SRAgent:
    """Specialista in Supporti, Resistenze e Zone di Liquidità."""
    
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def analizza(self, data_summary, context_skills=""):
        """Esegue l'analisi di supporti e resistenze."""
        logger.info("[SR AGENT] Analisi in corso...")
        
        prompt = f"""
        SEI UN TRADER ISTITUZIONALE ESPERTO DI LIVELLI DI PREZZO (SUPPORTI/RESISTENZE/SUPPLY & DEMAND).
        Analizza i livelli critici sui dati forniti:
        
        DATI MERCATO:
        {data_summary}
        
        SKILL DI RIFERIMENTO:
        {context_skills}
        
        DOCUMENTA:
        1. Livelli di Supporto e Resistenza Statici.
        2. Zone di Supply & Demand (Offerta e Domanda).
        3. Livelli di Rintracciamento Fibonacci significativi.
        
        Rispondi in italiano.
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            return f"### Analisi Supporti & Resistenze\n{response.text}"
        except Exception as e:
            logger.error(f"Errore SRAgent: {e}")
            return "Errore nell'analisi dei supporti."
