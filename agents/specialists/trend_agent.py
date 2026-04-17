"""
agents/specialists/trend_agent.py — Specialista in Trend e Momentum.

Agente Agno V2 che analizza trend direzionale e momentum usando le Skill
estratte dai libri di John Murphy, Brian Shannon e Larry Williams,
caricate direttamente dalla cartella skills_library/trend_analyst/.
"""

import os
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.skills import Skills, LocalSkills
from loguru import logger
import Calibrazione
from agents.model_factory import get_model


class TrendAgent:
    """
    Specialista in Trend e Momentum (Medie Mobili, RSI, MACD, Multi-Timeframe).

    Costruito secondo il framework Agno ufficiale con:
    - skills=[TREND_SKILL_DIR]: Accesso alle skill estratte da Murphy, Shannon, Williams
    - Storage SQLite locale per la memoria della sessione
    - Metodo analizza() sincrono, coerente con gli altri agenti del team
    """

    def __init__(self):
        logger.info("[TREND AGENT] Inizializzazione...")

        # --- 1. Modello AI ---
        llm = get_model(Calibrazione.MODEL_TECH_SPECIALISTS, temperature=Calibrazione.TEMPERATURE_TECH_SPECIALISTS, agent_name="tech_specialists")

        # --- 2. Storage locale opzionale ---
        storage = None
        if Calibrazione.STORAGE_LOCATION == "local":
            storage = SqliteDb(
                session_table="trend_agent_session",
                db_file=Calibrazione.DATABASE_PATH
            )

        # --- 3. Caricamento Skills Agno dai 6 libri tecnici ---
        skills = Skills(loaders=[LocalSkills(os.path.abspath(d), validate=False) for d in Calibrazione.TECHNICAL_SKILLS_DIRS])

        # --- 4. Creazione Agente Agno ---
        self.agent = Agent(
            name="Trend Analyst",
            model=llm,
            description=(
                "Sei un esperto di Trend Analysis e Momentum applicati ai mercati finanziari. "
                "La tua competenza integra l'analisi classica del trend di John Murphy "
                "(medie mobili, MACD, RSI, trendline), l'analisi multi-timeframe di Brian Shannon "
                "(allineamento top-down da weekly a 1H) e l'analisi del momentum di Larry Williams "
                "(%R, divergenze, overbought/oversold). "
                "Il tuo compito è determinare la direzione del trend su ogni timeframe, "
                "valutare il momentum corrente, identificare eventuali divergenze e "
                "fornire stop loss logici basati sulla struttura del mercato. "
                "Non esegui analisi di pattern grafici (ci pensa il Pattern Analyst). "
                "Non entri nei dettagli di supporti e resistenze statici (ci pensa il SR Analyst). "
                "Il tuo focus è esclusivamente la DIREZIONE e la FORZA del trend."
            ),
            instructions=[
                "Inizia SEMPRE la tua risposta con la sezione '## 🛠️ STRUMENTI UTILIZZATI'. "
                "Per OGNI tecnica della FOCUS SKILLS valutata, produci UNA RIGA nel formato ESATTO: "
                "'✅ NomeTecnica — breve nota operativa' se la tecnica è presente nei dati correnti, "
                "'❌ NomeTecnica — non rilevato' se la tecnica non è applicabile ai dati correnti. "
                "Elenca almeno le tecniche principali di ogni libro della FOCUS SKILLS. "
                "Poi prosegui con l'analisi dettagliata.",
                "VINCOLO FONDAMENTALE: se la sezione 'FOCUS SKILLS' è presente nel prompt, "
                "devi analizzare TUTTE le tecniche elencate in essa (sono obbligatorie, non opzionali). "
                "Dopo averle analizzate tutte, puoi integrare con altri indicatori e metodi "
                "presenti nelle Skill caricate (Murphy, Shannon, Williams) che ritieni utili.",
                "Per ogni tecnica applicata consulta le tue Skill per le regole operative precise "
                "(criteri di incrocio, segnali di momentum, procedura top-down).",
                "Analizza il trend su 3 livelli: Primario (1D/1W), Secondario (4H), Terziario (1H).",
                "Documenta esplicitamente la struttura: stai vedendo HH+HL (uptrend), "
                "LH+LL (downtrend), o una struttura mista (laterale/inversione)?",
                "Verifica il momentum con le tecniche selezionate: esistono divergenze da segnalare?",
                "Rispetta il Sentiment Macro ricevuto: usa il bias macro come filtro direzionale.",
                "Fornisci stop loss logici basati sulla struttura di mercato (ultimo swing HH/HL o LH/LL).",
                "Concludi con un verdetto chiaro: TREND BULLISH / BEARISH / LATERALE + "
                "timeframe di riferimento + livello di confidence (Alto/Medio/Basso).",
                "Rispondi in italiano in modo professionale e strutturato.",
            ],
            skills=skills,
            db=storage,
            num_history_messages=3,
            markdown=True,
        )
        logger.success(f"[TREND AGENT] Pronto con modello: {llm.id} | Skills: {len(Calibrazione.TECHNICAL_SKILLS_DIRS)} libri caricati")

    def analizza(self, data_summary: str, macro_sentiment: str = "Neutrale", skills_guidance: str = "") -> str:
        """
        Esegue l'analisi del trend e del momentum sui dati OHLCV forniti.

        Args:
            data_summary:    Stringa con i dati OHLCV multi-timeframe del mercato.
            macro_sentiment: Il sentiment macro dell'AgnoMacroExpert.
            skills_guidance: Istruzione su quali indicatori/tecniche dai libri privilegiare.

        Returns:
            Stringa Markdown con l'analisi completa del trend e momentum.
        """
        logger.info("[TREND AGENT] Avvio analisi trend e momentum...")

        focus_section = f"\nFOCUS SKILLS (tecniche OBBLIGATORIE — analizzale TUTTE, poi integra con altre Skill):\n{skills_guidance}\n" if skills_guidance else ""

        prompt = f"""
DATI MERCATO (OHLCV Multi-Timeframe):
{data_summary}

SENTIMENT MACRO DA RISPETTARE (fornito dall'agente Macro Strategist):
{macro_sentiment}
{focus_section}
Esegui un'analisi completa del trend e del momentum.
Segui la procedura top-down (Weekly → Daily → 4H → 1H) come da Skill.
PRIMA SEZIONE OBBLIGATORIA: '## 🛠️ STRUMENTI UTILIZZATI' con ogni tecnica su riga separata nel formato: ✅ NomeTecnica — nota / ❌ NomeTecnica — non rilevato
"""
        try:
            response = self.agent.run(prompt)
            return response.content if response.content else "Errore: risposta vuota dall'agente."
        except Exception as e:
            logger.error(f"[TREND AGENT] Errore durante l'analisi: {e}")
            return f"❌ Errore nell'analisi del trend: {e}"
