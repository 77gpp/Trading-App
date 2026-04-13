"""
agents/specialists/pattern_agent.py — Specialista in Pattern Recognition.

Agente Agno V2 che analizza candlestick e formazioni grafiche usando le Skill
estratte dai libri di Steve Nison, Thomas Bulkowski e Joe Ross, caricate
direttamente dalla cartella skills_library/pattern_analyst/.
"""

import os
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.skills import Skills, LocalSkills
from loguru import logger
import Calibrazione
from agents.model_factory import get_model


class PatternAgent:
    """
    Specialista in Pattern Recognition (Candlestick e Formazioni Grafiche).
    
    Costruito secondo il framework Agno ufficiale con:
    - skills=[PATTERN_SKILL_DIR]: Accesso alle skill estratte da Nison, Bulkowski, Joe Ross
    - Storage SQLite locale per la memoria della sessione
    - Metodo analizza() sincrono, coerente con gli altri agenti del team
    """

    def __init__(self):
        logger.info("[PATTERN AGENT] Inizializzazione...")

        # --- 1. Modello AI (dal factory, supporta Gemini o Qwen/Groq) ---
        llm = get_model(Calibrazione.MODEL_TECH_SPECIALISTS, temperature=Calibrazione.TEMPERATURE_TECH_SPECIALISTS)

        # --- 2. Storage locale opzionale ---
        storage = None
        if Calibrazione.STORAGE_LOCATION == "local":
            storage = SqliteDb(
                session_table="pattern_agent_session",
                db_file=Calibrazione.DATABASE_PATH
            )

        # --- 3. Caricamento Skills Agno dai 6 libri tecnici ---
        skills = Skills(loaders=[LocalSkills(os.path.abspath(d), validate=False) for d in Calibrazione.TECHNICAL_SKILLS_DIRS])

        # --- 4. Creazione Agente Agno ---
        self.agent = Agent(
            name="Pattern Analyst",
            model=llm,
            description=(
                "Sei un esperto mondiale di Pattern Recognition nei mercati finanziari. "
                "La tua competenza integra la tradizione giapponese delle candele (Steve Nison), "
                "la statistica dei pattern grafici (Thomas Bulkowski — Encyclopedia of Chart Patterns) "
                "e i sistemi operativi di Joe Ross (1-2-3 Pattern, Hook of Ross, Power Bars). "
                "Il tuo compito è analizzare i dati OHLCV forniti, identificare tutti i pattern "
                "rilevanti e fornire una valutazione dell'affidabilità di ogni segnale nel "
                "contesto del sentiment macro ricevuto. "
                "Non fai previsioni di prezzo esatte — identifichi configurazioni di mercato "
                "con alta probabilità statistica di sviluppi specifici."
            ),
            instructions=[
                "Inizia SEMPRE la tua risposta con la sezione '🛠️ STRUMENTI UTILIZZATI' "
                "elencando le tecniche specifiche che hai applicato con il libro di provenienza.",
                "VINCOLO FONDAMENTALE: se la sezione 'FOCUS SKILLS' è presente nel prompt, "
                "devi analizzare TUTTE le tecniche elencate in essa (sono obbligatorie, non opzionali). "
                "Dopo averle analizzate tutte, puoi integrare con altri pattern e tecniche "
                "presenti nelle Skill caricate (libri di Nison, Bulkowski, Joe Ross) che ritieni utili.",
                "Per ogni tecnica applicata consulta le tue Skill per verificare le regole di "
                "validità esatte e calcolare il target con il metodo del libro di riferimento.",
                "Analizza i dati OHLCV su tutti i timeframe disponibili, partendo dal più lungo.",
                "Per ogni pattern identificato documenta: nome, libro di provenienza, posizione "
                "nel grafico, affidabilità stimata (%), e indicazione operativa (LONG/SHORT/NEUTRO).",
                "Applica sempre il filtro volumetrico: un pattern senza conferma di volume "
                "ha affidabilità BASSA — dichiaralo esplicitamente.",
                "Rispetta il Sentiment Macro ricevuto: se il macro è BEARISH, dai peso "
                "maggiore ai pattern ribassisti e tratta quelli rialzisti come potenziali "
                "rimbalzi tecnici di breve termine.",
                "Concludi con una sintesi operativa: segnale dominante, R/R stimato, "
                "livelli di Stop Loss e Target calcolati secondo la metodologia del libro.",
                "Rispondi in italiano in modo professionale e strutturato.",
            ],
            skills=skills,
            db=storage,
            num_history_messages=3,
            markdown=True,
        )
        logger.success(f"[PATTERN AGENT] Pronto con modello: {llm.id} | Skills: {len(Calibrazione.TECHNICAL_SKILLS_DIRS)} libri caricati")

    def analizza(self, data_summary: str, macro_sentiment: str = "Neutrale", skills_guidance: str = "") -> str:
        """
        Esegue l'analisi dei pattern sui dati OHLCV forniti.

        Args:
            data_summary:    Stringa con i dati OHLCV multi-timeframe del mercato.
            macro_sentiment: Il sentiment macro dell'AgnoMacroExpert (usato come contesto).
            skills_guidance: Istruzione su quali pattern/tecniche dai libri privilegiare.

        Returns:
            Stringa Markdown con l'analisi completa dei pattern.
        """
        logger.info("[PATTERN AGENT] Avvio analisi pattern...")

        focus_section = f"\nFOCUS SKILLS (tecniche OBBLIGATORIE — analizzale TUTTE, poi integra con altre Skill):\n{skills_guidance}\n" if skills_guidance else ""

        prompt = f"""
DATI MERCATO (OHLCV Multi-Timeframe):
{data_summary}

SENTIMENT MACRO DA RISPETTARE (fornito dall'agente Macro Strategist):
{macro_sentiment}
{focus_section}
Esegui un'analisi completa dei pattern candlestick e delle formazioni grafiche.
Inizia con la sezione '🛠️ STRUMENTI UTILIZZATI' e procedi come da istruzioni.
"""
        try:
            response = self.agent.run(prompt)
            return response.content if response.content else "Errore: risposta vuota dall'agente."
        except Exception as e:
            logger.error(f"[PATTERN AGENT] Errore durante l'analisi: {e}")
            return f"❌ Errore nell'analisi dei pattern: {e}"
