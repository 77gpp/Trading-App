import os
import asyncio
from loguru import logger
from agno.agent import Agent

# Import dei componenti necessari
from agents.model_factory import get_model
from agents.context_expander_agent import ContextExpanderAgent
from agents.specialists.pattern_agent import PatternAgent
from agents.specialists.trend_agent import TrendAgent
from agents.specialists.sr_agent import SRAgent
from agents.specialists.volume_agent import VolumeAgent

import Calibrazione

class OrchestratorAgent:
    """
    Manager/Planner del Multi-Agent Trading Desk (V3).
    Si occupa di:
    1. Decomporre il task in sub-operazioni.
    2. Funzionare da Skill Router (selezione intelligente .md).
    3. Servire il contesto espanso (PDF) se necessario.
    4. Sincronizzare gli specialisti in asyncio.
    """
    
    def __init__(self, api_key=None):
        # Usiamo il model_factory per ottenere il modello corretto (Qwen o Gemini)
        self.model = get_model(Calibrazione.MODEL_TECH_ORCHESTRATOR, temperature=Calibrazione.TEMPERATURE_TECH_ORCHESTRATOR)
        
        # Inizializziamo l'Agente Agno per il routing
        self.router_agent = Agent(
            model=self.model,
            description="Esperto in routing di trading skill.",
            instructions=[
                "Analizza il profilo MTF e il contesto macro fornito.",
                "Seleziona le 3 skill (file .md) più rilevanti dalla lista fornita.",
                "Rispondi in italiano."
            ]
        )
        
        # Inizializzazione specialisti e strumenti
        self.expander = ContextExpanderAgent()
        self.pattern_expert = PatternAgent()
        self.trend_expert = TrendAgent()
        self.sr_expert = SRAgent()
        self.volume_expert = VolumeAgent()
        self.library_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills_library")

    async def _skill_router(self, mtf_profile, macro_context):
        """Seleziona le skill più rilevanti analizzando i file .md (Semantic Router)."""
        logger.info("[ORCHESTRATOR] Routing delle skill più rilevanti con Qwen/Groq...")
        
        if not os.path.exists(self.library_dir):
            return "Libreria non trovata."
            
        # Scansione sottocartelle (ogni cartella è una skill in formato Agno)
        all_skills = []
        if os.path.exists(self.library_dir):
            for d in os.listdir(self.library_dir):
                subdir = os.path.join(self.library_dir, d)
                if os.path.isdir(subdir) and os.path.exists(os.path.join(subdir, "SKILL.md")):
                    all_skills.append(d)
        
        if not all_skills:
            return "Nessuna skill trovata nelle sottocartelle."

        # Prendiamo i nomi delle cartelle (che rappresentano i libri) per la selezione
        skills_summary = "\n".join(all_skills)
            
        prompt = f"""
        CONTESTO GLOBALE: {macro_context}
        PROFILO MTF: {mtf_profile}
        
        SELEZIONA LE 3 SKILL PIÙ RILEVANTI TRA QUESTE:
        {skills_summary}
        
        Indica solo il nome del file e l'argomento.
        """
        
        try:
            # Esecuzione tramite Agno Agent
            response = self.router_agent.run(prompt)
            return response.content
        except Exception as e:
            logger.error(f"Errore Router: {e}")
            return "Errore nel routing delle skill."

    async def pianifica_ed_esegui(self, data_mtf, macro_context, mtf_profile):
        """Coordina l'esecuzione parallela degli specialisti."""
        logger.info("[ORCHESTRATOR] Pianificazione ed Esecuzione Parallela...")
        
        # 1. Routing delle skill
        relevant_skills = await self._skill_router(mtf_profile, macro_context)
        
        # 2. Esecuzione Parallela (Analyst Executor Agents)
        data_summary_1h = data_mtf["1h"].tail(50).to_string()
        
        tasks = [
            self.pattern_expert.analizza(data_summary_1h, relevant_skills),
            self.trend_expert.analizza(data_summary_1h, relevant_skills),
            self.sr_expert.analizza(data_summary_1h, relevant_skills),
            self.volume_expert.analizza(data_summary_1h, relevant_skills)
        ]
        
        # Sincronizzazione asyncio
        results = await asyncio.gather(*tasks)
        
        logger.success("[ORCHESTRATOR] Analisi di tutti gli specialisti completata con Qwen/Groq.")
        return results
