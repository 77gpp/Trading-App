import os
from loguru import logger
from agno.agent import Agent
from agents.model_factory import get_model

class VolumeAgent:
    """Specialista in Analisi dei Volumi e Volume Profile."""
    
    def __init__(self, model_id=None):
        # Usiamo il model_factory per ottenere il modello corretto
        self.model = get_model(model_id)
        
        # Inizializziamo l'Agente Agno
        self.agent = Agent(
            model=self.model,
            description="Esperto in Volume Analysis Trading.",
            instructions=[
                "Sei un maestro di VSA (Volume Spread Analysis - tipo Wyckoff o Tom Williams).",
                "Analizza i volumi sui dati forniti.",
                "Usa le skill di riferimento fornite per affinare l'analisi.",
                "Rispondi in italiano in modo professionale."
            ]
        )

    async def analizza(self, data_summary, context_skills=""):
        """Esegue l'analisi dei volumi."""
        logger.info("[VOLUME AGENT] Analisi in corso con Qwen/Groq...")
        
        prompt = f"""
        Analizza i volumi sui dati forniti:
        
        DATI MERCATO:
        {data_summary}
        
        SKILL DI RIFERIMENTO:
        {context_skills}
        
        DOCUMENTA:
        1. Relazione Sforzo vs Risultato (Volume vs Spread barra).
        2. Segnali di Accumulazione o Distribuzione.
        3. Livelli di Volume Profile significativi (POC, VA).
        """
        
        try:
            # Esecuzione tramite Agno Agent
            response = self.agent.run(prompt)
            return f"### Analisi Volumi\n{response.content}"
        except Exception as e:
            logger.error(f"Errore VolumeAgent: {e}")
            return "Errore nell'analisi dei volumi."
