import os
import re
import json
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
        self.model = get_model(Calibrazione.MODEL_TECH_ORCHESTRATOR, temperature=Calibrazione.TEMPERATURE_TECH_ORCHESTRATOR, agent_name="tech_orchestrator")
        
        # Inizializziamo l'Agente Agno per il routing
        self.router_agent = Agent(
            model=self.model,
            description="Esperto in scoring e selezione di skill di trading.",
            instructions=[
                "Analizza il profilo MTF e il contesto macro fornito.",
                "Assegna un punteggio di rilevanza da 1 a 10 a OGNI skill disponibile.",
                "Includi nella selezione TUTTE le skill con punteggio >= 5 per massimizzare la coverage dell'analisi.",
                "Escludi solo le skill con punteggio <= 3, chiaramente non pertinenti al contesto corrente.",
                "Rispondi ESCLUSIVAMENTE con JSON valido, senza testo aggiuntivo prima o dopo.",
                "Usa l'italiano per i campi 'why'.",
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
        """
        Seleziona tutte le skill rilevanti assegnando uno score a ciascuna.

        Strategia:
        - Legge la preview di ogni SKILL.md per dare all'LLM contesto reale
        - Chiede un punteggio 1-10 per ogni skill
        - Include TUTTE le skill con score >= 5 (massima coverage)
        - Fallback deterministico: se il parsing JSON fallisce usa tutte le skill
        """
        logger.info("[ORCHESTRATOR] Scoring skill con coverage massima basato su macro sentiment...")

        if not os.path.exists(self.library_dir):
            return "Libreria non trovata."

        # 1. Costruzione catalogo con preview SKILL.md (descr. + inizio contenuto)
        skill_catalog = []
        for d in sorted(os.listdir(self.library_dir)):
            subdir = os.path.join(self.library_dir, d)
            skill_md = os.path.join(subdir, "SKILL.md")
            if os.path.isdir(subdir) and os.path.exists(skill_md):
                try:
                    with open(skill_md, "r", encoding="utf-8") as f:
                        preview = f.read(1200)
                except Exception:
                    preview = f"Skill: {d}"
                skill_catalog.append({"name": d, "preview": preview})

        if not skill_catalog:
            return "Nessuna skill trovata nelle sottocartelle."

        all_skill_names = [s["name"] for s in skill_catalog]

        # 2. Costruzione catalogo testuale per il prompt
        catalog_text = ""
        for s in skill_catalog:
            catalog_text += f"\n\n=== SKILL: {s['name']} ===\n{s['preview'][:700]}\n"

        prompt = f"""CONTESTO MACRO (output del Macro Strategist):
{str(macro_context)[:2000]}

PROFILO TECNICO MTF:
{str(mtf_profile)[:800]}

Hai {len(skill_catalog)} skill disponibili. Assegna uno score di rilevanza (1-10) a ciascuna.
Includi nella selezione TUTTE le skill con score >= 5 per massimizzare la coverage.
Escludi solo quelle con score <= 3, chiaramente non pertinenti al contesto corrente.

SKILL DISPONIBILI:
{catalog_text}

Rispondi SOLO con JSON valido (nessun testo aggiuntivo):
{{
  "selected": [
    {{"name": "nome_skill", "score": 8, "why": "Motivo breve in italiano"}}
  ],
  "excluded": [
    {{"name": "nome_skill", "score": 2, "why": "Perché non pertinente"}}
  ]
}}"""

        try:
            response = self.router_agent.run(prompt)
            content = response.content.strip()

            # Estrai il blocco JSON dalla risposta (tollerante a testo residuo)
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                data = json.loads(json_match.group())
                selected = data.get("selected", [])
                if selected:
                    skill_names = [s["name"] for s in selected]
                    logger.info(
                        f"[ORCHESTRATOR] {len(skill_names)}/{len(skill_catalog)} skill selezionate "
                        f"(score>=5): {skill_names}"
                    )
                    lines = [f"SKILL SELEZIONATE ({len(skill_names)}/{len(skill_catalog)}):"]
                    for s in selected:
                        lines.append(f"- {s['name']} (score {s['score']}/10): {s.get('why', '')}")
                    return "\n".join(lines)
        except Exception as e:
            logger.error(f"[ORCHESTRATOR] Errore parsing skill router: {e}")

        # Fallback deterministico: usa tutte le skill disponibili
        logger.warning("[ORCHESTRATOR] Fallback: utilizzo di tutte le skill disponibili.")
        return "TUTTE LE SKILL DISPONIBILI (fallback):\n" + "\n".join(f"- {n}" for n in all_skill_names)

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
