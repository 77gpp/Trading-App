import os
from loguru import logger
from agno.agent import Agent
from agents.model_factory import get_model

class SRAgent:
    """Specialista in Supporti, Resistenze e Zone di Liquidità."""
    
    def __init__(self, model_id=None):
        # Usiamo il model_factory per ottenere il modello corretto
        self.model = get_model(model_id)
        
        # Inizializziamo l'Agente Agno
        self.agent = Agent(
            model=self.model,
            description="Esperto in Supporti e Resistenze Trading.",
            instructions=[
                "Sei un trader istituzionale esperto di livelli di prezzo (Supporti/Resistenze/Supply & Demand).",
                "Analizza i livelli critici sui dati forniti.",
                "Usa le skill di riferimento fornite per affinare l'analisi.",
                "Rispondi in italiano in modo professionale."
            ]
        )

    async def analizza(self, data_summary, context_skills=""):
        """Esegue l'analisi di supporti e resistenze."""
        logger.info("[SR AGENT] Analisi in corso con Qwen/Groq...")
        
        prompt = f"""
        Analizza i livelli critici sui dati forniti:
        
        DATI MERCATO:
        {data_summary}
        
        SKILL DI RIFERIMENTO:
        {context_skills}
        
        DOCUMENTA:
        1. Livelli di Supporto e Resistenza Statici.
        2. Zone di Supply & Demand (Offerta e Domanda).
        3. Livelli di Rintracciamento Fibonacci significativi.
        """
        
        try:
            # Esecuzione tramite Agno Agent
            response = self.agent.run(prompt)
            return f"### Analisi Supporti & Resistenze\n{response.content}"
        except Exception as e:
            logger.error(f"Errore SRAgent: {e}")
            return "Errore nell'analisi dei supporti."
