import google.generativeai as genai
from loguru import logger

class SynthesisAgent:
    """
    Agente di Sintesi Finale.
    Raccoglie le analisi degli specialisti e crea il report finale.
    """
    
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def genera_report_finale(self, asset_name, macro_context, mtf_profile, specialist_results):
        """Aggrega tutti i report in una sintesi coerente."""
        logger.info("[SYNTHESIS AGENT] Generazione del verdetto finale...")
        
        # Unione dei risultati degli specialisti
        specialist_text = "\n\n".join(specialist_results)
        
        prompt = f"""
        SEI IL CHIEF INVESTMENT OFFICER (CIO) DI UN FONDO DI TRADING.
        Ecco le analisi degli esperti per l'asset: {asset_name}.
        
        CONTESTO GLOBALE (MACRO):
        {macro_context}
        
        PROFILO TECNICO MTF:
        {mtf_profile}
        
        DETTAGLI SPECIALISTICI:
        {specialist_text}
        
        IL TUO COMPITO:
        1. Identificare CONFLITTI tra gli specialisti (es: Trend Long ma Volumi Short).
        2. Risolvere i conflitti e dare un BIAS DIREZIONALE finale (BUY / SELL / WAIT).
        3. Definire Punti di Ingresso, Stop Loss e Target basandoti sui report.
        4. Scrivere una sintesi iper-professionale per il trader.
        
        Rispondi in italiano con formato Markdown.
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Errore SynthesisAgent: {e}")
            return "Errore nella generazione del report finale."
