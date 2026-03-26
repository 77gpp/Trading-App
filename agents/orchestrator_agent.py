import os
import asyncio
import google.generativeai as genai
from loguru import logger

# Import dei componenti necessari
from agents.context_expander_agent import ContextExpanderAgent
from agents.specialists.pattern_agent import PatternAgent
from agents.specialists.trend_agent import TrendAgent
from agents.specialists.sr_agent import SRAgent
from agents.specialists.volume_agent import VolumeAgent

class OrchestratorAgent:
    """
    Manager/Planner del Multi-Agent Trading Desk (V3).
    Si occupa di:
    1. Decomporre il task in sub-operazioni.
    2. Funzionare da Skill Router (selezione intelligente .md).
    3. Servire il contesto espanso (PDF) se necessario.
    4. Sincronizzare gli specialisti in asyncio.
    """
    
    def __init__(self, api_key):
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Inizializzazione specialisti e strumenti
        self.expander = ContextExpanderAgent()
        self.pattern_expert = PatternAgent(api_key)
        self.trend_expert = TrendAgent(api_key)
        self.sr_expert = SRAgent(api_key)
        self.volume_expert = VolumeAgent(api_key)
        self.library_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills_library")

    async def _skill_router(self, mtf_profile, macro_context):
        """Seleziona le skill più rilevanti analizzando i file .md (Semantic Router)."""
        logger.info("[ORCHESTRATOR] Routing delle skill più rilevanti...")
        
        if not os.path.exists(self.library_dir):
            return "Libreria non trovata."
            
        all_skill_files = [f for f in os.listdir(self.library_dir) if f.endswith(".md")]
        if not all_skill_files:
            return "Nessuna skill trovata."

        # Prendiamo le intestazioni dei file per la selezione
        skills_summary = "\n".join(all_skill_files[:5]) 
            
        prompt = f"""
        CONTESTO GLOBALE: {macro_context}
        PROFILO MTF: {mtf_profile}
        
        SELEZIONA LE 3 SKILL PIÙ RILEVANTI TRA QUESTE:
        {skills_summary}
        
        Indica solo il nome del file e l'argomento.
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Errore Router: {e}")
            return "Errore nel routing delle skill."

    async def pianifica_ed_esegui(self, data_mtf, macro_context, mtf_profile):
        """Coordina l'esecuzione parallela degli specialisti."""
        logger.info("[ORCHESTRATOR] Pianificazione ed Esecuzione Parallela...")
        
        # 1. Routing delle skill
        relevant_skills = await self._skill_router(mtf_profile, macro_context)
        
        # 2. Esecuzione Parallela (Analyst Executor Agents)
        # Usiamo i dati 1h per gli specialisti (ultime 50 candele)
        data_summary_1h = data_mtf["1h"].tail(50).to_string()
        
        tasks = [
            self.pattern_expert.analizza(data_summary_1h, relevant_skills),
            self.trend_expert.analizza(data_summary_1h, relevant_skills),
            self.sr_expert.analizza(data_summary_1h, relevant_skills),
            self.volume_expert.analizza(data_summary_1h, relevant_skills)
        ]
        
        # Sincronizzazione asyncio
        results = await asyncio.gather(*tasks)
        
        logger.success("[ORCHESTRATOR] Analisi di tutti gli specialisti completata.")
        return results
