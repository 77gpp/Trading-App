import os
from loguru import logger
from agno.agent import Agent
from agents.model_factory import get_model

class TrendAgent:
    """Specialista in Trend e Momentum (Medie Mobili, RSI, MACD)."""
    
    def __init__(self, model_id=None):
        # Usiamo il model_factory per ottenere il modello corretto
        self.model = get_model(model_id)
        
        # Inizializziamo l'Agente Agno
        self.agent = Agent(
            model=self.model,
            description="Esperto in Trend e Momentum Trading.",
            instructions=[
                "Sei un analista tecnico esperto di trend (tipo John Murphy o Martin Pring).",
                "Analizza i trend e lo slancio del prezzo sui dati forniti.",
                "Usa le skill di riferimento fornite per affinare l'analisi.",
                "Rispondi in italiano in modo professionale."
            ]
        )

    async def analizza(self, data_summary, context_skills=""):
        """Esegue l'analisi di trend e momentum."""
        logger.info("[TREND AGENT] Analisi in corso con Qwen/Groq...")
        
        prompt = f"""
        Analizza i trend e lo slancio del prezzo sui dati forniti:
        
        DATI MERCATO:
        {data_summary}
        
        SKILL DI RIFERIMENTO:
        {context_skills}
        
        DOCUMENTA:
        1. Direzione del Trend (Primario, Secondario, Terziario).
        2. Analisi del Momentum (Ipercomprato/Ipervenduto, Divergenze).
        3. Livelli di stop-loss logici per il trend attuale.
        """
        
        try:
            # Esecuzione tramite Agno Agent
            response = self.agent.run(prompt)
            return f"### Analisi Trend & Momentum\n{response.content}"
        except Exception as e:
            logger.error(f"Errore TrendAgent: {e}")
            return "Errore nell'analisi del trend."
