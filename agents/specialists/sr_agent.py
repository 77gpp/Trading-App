"""
agents/specialists/sr_agent.py — Specialista in Supporti, Resistenze e Zone Chiave.

Agente Agno V2 che analizza livelli di prezzo critici usando le Skill estratte
dai libri di Murphy, Bulkowski e Williams (Pivot Points, Fibonacci, Supply & Demand),
caricate direttamente dalla cartella skills_library/sr_analyst/.
"""

import os
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.skills import Skills, LocalSkills
from loguru import logger
import Calibrazione
from agents.model_factory import get_model


class SRAgent:
    """
    Specialista in Supporti, Resistenze, Zone di Supply & Demand e Fibonacci.

    Costruito secondo il framework Agno ufficiale con:
    - skills=[SR_SKILL_DIR]: Accesso alle skill estratte da Murphy, Bulkowski, Williams
    - Storage SQLite locale per la memoria della sessione
    - Metodo analizza() sincrono, coerente con gli altri agenti del team
    """

    def __init__(self):
        logger.info("[SR AGENT] Inizializzazione...")

        # --- 1. Modello AI ---
        llm = get_model(Calibrazione.MODEL_TECH_SPECIALISTS, temperature=Calibrazione.TEMPERATURE_TECH_SPECIALISTS)

        # --- 2. Storage locale opzionale ---
        storage = None
        if Calibrazione.STORAGE_LOCATION == "local":
            storage = SqliteDb(
                session_table="sr_agent_session",
                db_file=Calibrazione.DATABASE_PATH
            )

        # --- 3. Caricamento Skills Agno dai 6 libri tecnici ---
        skills = Skills(loaders=[LocalSkills(os.path.abspath(d), validate=False) for d in Calibrazione.TECHNICAL_SKILLS_DIRS])

        # --- 4. Creazione Agente Agno ---
        self.agent = Agent(
            name="SR Analyst",
            model=llm,
            description=(
                "Sei un esperto di Analisi dei Livelli di Prezzo nei mercati finanziari. "
                "La tua competenza copre i supporti e resistenze classici di John Murphy, "
                "la logica delle Supply & Demand Zones istituzionali, "
                "i Fibonacci Retracement e Extension (38.2%, 61.8%, 161.8%), "
                "i Pivot Points giornalieri e settimanali, "
                "il VWAP istituzionale e il Donchian Channel dei Turtle Traders. "
                "Il tuo compito è mappare tutti i livelli di prezzo chiave nel contesto "
                "del mercato analizzato, identificare le zone ad alta confluenza "
                "(dove 2+ livelli di origine diversa si sovrappongono) e fornire "
                "una struttura precisa di supporti e resistenze per il team. "
                "Non analizzi pattern candlestick (ci pensa il Pattern Analyst). "
                "Non analizzi la direzione del trend (ci pensa il Trend Analyst). "
                "Il tuo focus è esclusivamente la MAPPA DEI LIVELLI DI PREZZO."
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
                "Dopo averle analizzate tutte, puoi integrare con altri metodi di identificazione S/R "
                "presenti nelle Skill caricate (Murphy, Bulkowski, Williams) che ritieni utili.",
                "Per ogni tecnica consulta le tue Skill per i criteri di identificazione precisi "
                "e il calcolo del punteggio di confluenza.",
                "Analizza i livelli su TUTTI i timeframe: inizia dai livelli di lungo "
                "termine (mensili/settimanali) e scendi fino ai livelli intraday.",
                "Identifica almeno 3 livelli di SUPPORTO e 3 di RESISTENZA significativi, "
                "ordinandoli per importanza e distanza dal prezzo corrente.",
                "Per ogni livello indica: origine (tecnica applicata + libro), "
                "numero di tocchi, e punteggio di confluenza (1-5 punti).",
                "Identifica le ZONE DI CONFLUENZA (punteggio ≥ 3): queste sono le zone "
                "dove il prezzo ha la massima probabilità di reagire.",
                "Rispetta il Sentiment Macro: in bias BEARISH evidenzia le resistenze; "
                "in bias BULLISH evidenzia i supporti come zone di opportunità.",
                "Fornisci la struttura S/R in formato tabellare (Markdown) per massima leggibilità.",
                "Concludi con il livello più critico del momento e il motivo per cui "
                "è strategicamente rilevante per il trading nelle prossime sessioni.",
                "Rispondi in italiano in modo professionale e strutturato.",
            ],
            skills=skills,
            db=storage,
            num_history_messages=3,
            markdown=True,
        )
        logger.success(f"[SR AGENT] Pronto con modello: {llm.id} | Skills: {len(Calibrazione.TECHNICAL_SKILLS_DIRS)} libri caricati")

    def analizza(self, data_summary: str, macro_sentiment: str = "Neutrale", skills_guidance: str = "") -> str:
        """
        Esegue l'analisi dei supporti e resistenze sui dati OHLCV forniti.

        Args:
            data_summary:    Stringa con i dati OHLCV multi-timeframe del mercato.
            macro_sentiment: Il sentiment macro dell'AgnoMacroExpert.
            skills_guidance: Istruzione su quali livelli/tecniche dai libri privilegiare.

        Returns:
            Stringa Markdown con la mappa completa dei livelli di prezzo.
        """
        logger.info("[SR AGENT] Avvio analisi supporti e resistenze...")

        focus_section = f"\nFOCUS SKILLS (tecniche OBBLIGATORIE — analizzale TUTTE, poi integra con altre Skill):\n{skills_guidance}\n" if skills_guidance else ""

        prompt = f"""
DATI MERCATO (OHLCV Multi-Timeframe):
{data_summary}

SENTIMENT MACRO DA RISPETTARE (fornito dall'agente Macro Strategist):
{macro_sentiment}
{focus_section}
Esegui la mappatura completa di tutti i livelli di prezzo chiave.
Identifica zone di confluenza, Fibonacci, Supply & Demand Zones, Pivot Points e VWAP.
PRIMA SEZIONE OBBLIGATORIA: '## 🛠️ STRUMENTI UTILIZZATI' con ogni tecnica su riga separata nel formato: ✅ NomeTecnica — nota / ❌ NomeTecnica — non rilevato
Poi usa tabelle Markdown per i livelli S/R.
"""
        try:
            response = self.agent.run(prompt)
            return response.content if response.content else "Errore: risposta vuota dall'agente."
        except Exception as e:
            logger.error(f"[SR AGENT] Errore durante l'analisi: {e}")
            return f"❌ Errore nell'analisi dei supporti e resistenze: {e}"
