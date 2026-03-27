import os
from loguru import logger
from agno.agent import Agent
from agents.model_factory import get_model

class PatternAgent:
    """Specialista in Pattern Recognition (Candlestick e Formazioni Grafiche)."""
    
    def __init__(self, model_id=None):
        # Usiamo il model_factory per ottenere il modello corretto
        self.model = get_model(model_id)
        
        # Inizializziamo l'Agente Agno
        self.agent = Agent(
            model=self.model,
            description="Esperto in Pattern Recognition Trading.",
            instructions=[
                "Sei un esperto di pattern recognition (tipo Thomas Bulkowski o Steve Nison).",
                "Analizza i dati OHLCV alla ricerca di pattern di inversione o continuazione.",
                "Usa le skill di riferimento fornite per affinare l'analisi.",
                "Rispondi in italiano in modo professionale."
            ]
        )

    async def analizza(self, data_summary, context_skills=""):
        """Esegue l'analisi dei pattern sui dati forniti."""
        logger.info("[PATTERN AGENT] Analisi in corso con Qwen/Groq...")
        
        prompt = f"""
        Analizza i seguenti dati OHLCV e cerca pattern di inversione o continuazione:
        
        DATI MERCATO:
        {data_summary}
        
        SKILL DI RIFERIMENTO:
        {context_skills}
        
        DOCUMENTA:
        1. Pattern Candlestick rilevati (es: Engulfing, Pin Bar, Doji).
        2. Formazioni grafiche in sviluppo (es: Double Top, Cup and Handle).
        3. Affidabilità del pattern nel contesto attuale.
        """
        
        try:
            # Esecuzione tramite Agno Agent
            response = self.agent.run(prompt)
            return f"### Analisi Pattern\n{response.content}"
        except Exception as e:
            logger.error(f"Errore PatternAgent: {e}")
            return "Errore nell'analisi dei pattern."
