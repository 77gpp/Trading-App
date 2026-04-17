"""
agents/specialists/volume_agent.py — Specialista in Analisi Volumetrica VSA/Wyckoff.

Agente Agno V2 che analizza i volumi usando le Skill estratte dai libri di
Tom Williams (VSA), Richard Wyckoff e Larry Williams, caricate direttamente
dalla cartella skills_library/volume_analyst/.

RUOLO CRITICO: È il FILTRO FINALE del team. Se i volumi non confermano
il segnale tecnico degli altri agenti, il verdetto è RISCHIO ELEVATO.
"""

import os
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.skills import Skills, LocalSkills
from loguru import logger
import Calibrazione
from agents.model_factory import get_model


class VolumeAgent:
    """
    Specialista in Analisi dei Volumi, VSA (Volume Spread Analysis) e Wyckoff.

    Costruito secondo il framework Agno ufficiale con:
    - skills=[VOLUME_SKILL_DIR]: Accesso alle skill estratte da Williams, Wyckoff, Ross
    - Storage SQLite locale per la memoria della sessione
    - Metodo analizza() sincrono, coerente con gli altri agenti del team

    NOTA: Il Volume Analyst è il filtro finale del Technical Trading Desk.
    """

    def __init__(self):
        logger.info("[VOLUME AGENT] Inizializzazione...")

        # --- 1. Modello AI ---
        llm = get_model(Calibrazione.MODEL_TECH_SPECIALISTS, temperature=Calibrazione.TEMPERATURE_TECH_SPECIALISTS, agent_name="tech_specialists")

        # --- 2. Storage locale opzionale ---
        storage = None
        if Calibrazione.STORAGE_LOCATION == "local":
            storage = SqliteDb(
                session_table="volume_agent_session",
                db_file=Calibrazione.DATABASE_PATH
            )

        # --- 3. Caricamento Skills Agno dai 6 libri tecnici ---
        skills = Skills(loaders=[LocalSkills(os.path.abspath(d), validate=False) for d in Calibrazione.TECHNICAL_SKILLS_DIRS])

        # --- 4. Creazione Agente Agno ---
        self.agent = Agent(
            name="Volume Analyst",
            model=llm,
            description=(
                "Sei un Maestro di Volume Spread Analysis (VSA) e dell'analisi di Wyckoff. "
                "La tua competenza si basa su Tom Williams (Master the Markets — VSA), "
                "Richard Wyckoff (le 4 fasi del ciclo di mercato: Accumulazione, Markup, "
                "Distribuzione, Markdown) e Larry Williams (analisi volumetrica operativa). "
                "Il tuo ruolo nel team è il più critico: sei il FILTRO FINALE. "
                "Il tuo compito è verificare se il volume CONFERMA o DIVERGE dai segnali "
                "tecnici degli altri specialisti (pattern, trend, S/R). "
                "Principio fondamentale: Il volume misura lo SFORZO. Il prezzo misura il RISULTATO. "
                "Se Sforzo ≠ Risultato, il mercato sta mentendo. Dichiaralo sempre. "
                "Se i volumi non confermano il segnale, devi dichiarare RISCHIO ELEVATO "
                "indipendentemente da cosa dicono gli altri agenti."
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
                "Dopo averle analizzate tutte, puoi integrare con altri segnali VSA/Wyckoff "
                "presenti nelle Skill caricate (Tom Williams, Wyckoff, Larry Williams) che ritieni utili.",
                "Per ogni tecnica consulta le tue Skill per i criteri esatti di identificazione.",
                "Analizza il volume degli ultimi 5-20 periodi su ogni timeframe disponibile.",
                "Applica la legge di Sforzo vs Risultato: le candele ad alto volume "
                "producono movimenti ampi nella stessa direzione? Se no → ALERT di assorbimento.",
                "Identifica la FASE WYCKOFF attiva: Accumulazione / Markup / Distribuzione / Markdown.",
                "Verifica il Volume Profile se i dati lo permettono: indica la posizione "
                "rispetto a POC, VAH, VAL e zone HVN/LVN.",
                "IL VERDETTO VOLUMETRICO È OBBLIGATORIO e deve contenere:",
                "  • Fase Wyckoff attiva",
                "  • Segnale VSA dominante (tecnica dal libro applicata)",
                "  • CONFERMA o DIVERGENZA rispetto ai segnali degli altri specialisti",
                "  • Livello di RISCHIO: NORMALE / ELEVATO",
                "REGOLA ASSOLUTA: se i volumi DIVERGONO dai segnali tecnici degli altri specialisti "
                "→ dichiarare RISCHIO ELEVATO e spiegare perché il segnale è inaffidabile.",
                "Rispetta il Sentiment Macro come contesto aggiuntivo.",
                "Rispondi in italiano in modo professionale e strutturato.",
            ],
            skills=skills,
            db=storage,
            num_history_messages=3,
            markdown=True,
        )
        logger.success(f"[VOLUME AGENT] Pronto con modello: {llm.id} | Skills: {len(Calibrazione.TECHNICAL_SKILLS_DIRS)} libri caricati")

    def analizza(self, data_summary: str, macro_sentiment: str = "Neutrale",
                 skills_guidance: str = "", other_analyses: dict = None) -> str:
        """
        Esegue l'analisi volumetrica VSA/Wyckoff sui dati OHLCV forniti.

        Args:
            data_summary:    Stringa con i dati OHLCV multi-timeframe del mercato.
            macro_sentiment: Il sentiment macro dell'AgnoMacroExpert.
            skills_guidance: Istruzione su quali segnali degli altri specialisti validare.
            other_analyses:  Dict {nome_agente: testo_analisi} degli altri 3 specialisti.
                             Permette al Volume Agent di validare i segnali effettivi, non solo i nomi.

        Returns:
            Stringa Markdown con l'analisi volumetrica completa e il verdetto finale.
        """
        logger.info("[VOLUME AGENT] Avvio analisi volumetrica VSA/Wyckoff...")

        focus_section = f"\nFOCUS SKILLS (tecniche OBBLIGATORIE — analizzale TUTTE, poi integra con altre Skill):\n{skills_guidance}\n" if skills_guidance else ""

        # Sezione con i segnali effettivi degli altri specialisti da validare
        other_section = ""
        if other_analyses:
            parts = []
            for nome, testo in other_analyses.items():
                if testo and testo not in ("Analisi Disattivata", "N/D"):
                    # Tronca a 1500 char per non saturare il contesto
                    estratto = testo[:1500] + ("…" if len(testo) > 1500 else "")
                    parts.append(f"=== {nome} ===\n{estratto}")
            if parts:
                other_section = (
                    "\n\nANALISI DEGLI ALTRI SPECIALISTI (da validare con i volumi):\n"
                    + "\n\n".join(parts)
                    + "\n\nIL TUO COMPITO: per ciascun segnale sopra, verifica se il volume CONFERMA o DIVERGE. "
                    "Se i volumi non confermano → dichiarare RISCHIO ELEVATO per quel segnale.\n"
                )

        prompt = f"""
DATI MERCATO (OHLCV Multi-Timeframe — incluso Volume):
{data_summary}

SENTIMENT MACRO DA RISPETTARE (fornito dall'agente Macro Strategist):
{macro_sentiment}
{focus_section}{other_section}
Esegui un'analisi volumetrica profonda usando VSA e il framework di Wyckoff.
Segui la checklist in 6 passi della tua Skill: Volume assoluto → Sforzo vs Risultato →
Chiusura nel range → Segnali VSA → Fase Wyckoff → Volume Profile.
Il Verdetto Volumetrico finale è OBBLIGATORIO: Fase Wyckoff + Segnale VSA + CONFERMA/DIVERGENZA + RISCHIO.
PRIMA SEZIONE OBBLIGATORIA: '## 🛠️ STRUMENTI UTILIZZATI' con ogni tecnica su riga separata nel formato: ✅ NomeTecnica — nota / ❌ NomeTecnica — non rilevato
"""
        try:
            response = self.agent.run(prompt)
            return response.content if response.content else "Errore: risposta vuota dall'agente."
        except Exception as e:
            logger.error(f"[VOLUME AGENT] Errore durante l'analisi: {e}")
            return f"❌ Errore nell'analisi volumetrica: {e}"
