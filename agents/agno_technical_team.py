import os
import re
from agno.agent import Agent
from agno.team import Team
from agno.db.sqlite import SqliteDb
from loguru import logger
import Calibrazione


def _rimuovi_intro_inglese(testo: str, marker: str | None = None) -> str:
    """
    Rimuove i blocchi di ragionamento in inglese che i modelli Qwen/Groq
    producono prima dell'analisi vera (es. 'Okay, let's start...').

    Strategia in cascata:
    1. Se `marker` è specificato, cerca quella stringa esatta e taglia tutto prima.
    2. Altrimenti cerca il primo heading/emoji italiano noto (🛠️, ##, **Bias).
    3. Fallback: rimuove righe iniziali che contengono parole-spia inglesi.
    """
    if not testo:
        return testo

    righe = testo.splitlines()

    # --- Passo 1: marker esplicito ---
    if marker:
        for i, riga in enumerate(righe):
            if marker in riga:
                return "\n".join(righe[i:]).strip()

    # --- Passo 2: prima riga che inizia con marcatore italiano noto ---
    MARCATORI = re.compile(
        r"^(🛠️|##|###|####|\*\*Bias|\*\*Strumenti|---)",
        re.UNICODE,
    )
    for i, riga in enumerate(righe):
        stripped = riga.strip()
        if stripped and MARCATORI.match(stripped):
            return "\n".join(righe[i:]).strip()

    # --- Passo 3: fallback — salta righe con parole-spia inglesi ---
    INGLESE = re.compile(
        r"\b(okay|let'?s|first|now|looking|i need|i will|i must|i want|the user"
        r"|next|finally|putting|starting|checking|trying|understand|going to"
        r"|also|then|wait|need to|here|so |this |these |those |they |there )\b",
        re.IGNORECASE,
    )
    for i, riga in enumerate(righe):
        stripped = riga.strip()
        if not stripped:
            continue
        if not INGLESE.search(stripped):
            return "\n".join(righe[i:]).strip()

    return testo


class AgnoTechnicalTeam:
    """Team di esperti V5 (Configurable & Free)."""
    
    def __init__(self):
        self.api_key = Calibrazione.GEMINI_API_KEY
        self.model_desk = Calibrazione.MODEL_TECH_ORCHESTRATOR
        self.model_specialists = Calibrazione.MODEL_TECH_SPECIALISTS
        self.db_path = Calibrazione.DATABASE_PATH
        self.skills_dir = Calibrazione.SKILLS_LIBRARY_DIR
        
        # 1. Configurazione Storage Locale (Condiviso per il Team)
        self.storage = None
        if Calibrazione.STORAGE_LOCATION == "local":
            self.storage = SqliteDb(
                session_table="technical_team_session",
                db_file=self.db_path
            )

        # 2. Caricamento Sommario Skills (File Search Bridge per l'Orchestratore)
        all_skills = ""
        if os.path.exists(self.skills_dir):
            count = 0
            for d in sorted(os.listdir(self.skills_dir)):
                if count >= 3: break  # Limitiamo per token budget
                subdir = os.path.join(self.skills_dir, d)
                skill_md = os.path.join(subdir, "SKILL.md")
                if os.path.isdir(subdir) and os.path.exists(skill_md):
                    with open(skill_md, "r", encoding="utf-8", errors="ignore") as f_in:
                        all_skills += f"\n--- {d} ---\n{f_in.read()[:2000]}\n"
                        count += 1
        
        # 3. Definizione Agenti Specialisti
        from agents.model_factory import get_model
        
        # Carichiamo i modelli tramite factory (Qwen/Groq o Gemini)
        llm_specialists = get_model(self.model_specialists, temperature=Calibrazione.TEMPERATURE_TECH_SPECIALISTS)
        llm_desk = get_model(self.model_desk, temperature=Calibrazione.TEMPERATURE_TECH_ORCHESTRATOR)
        
        LINGUA = (
            "LINGUA OBBLIGATORIA: Italiano. "
            "Scrivi TUTTO in italiano — analisi, ragionamenti, titoli, note. "
            "Non usare mai l'inglese, nemmeno per frasi introduttive o note interne. "
            "Non iniziare mai con 'Okay', 'Let me', 'First' o qualsiasi parola inglese."
        )
        STRUTTURA = (
            "STRUTTURA OBBLIGATORIA: la tua risposta deve iniziare ESATTAMENTE con la riga "
            "'🛠️ STRUMENTI UTILIZZATI' — nessuna parola o frase prima di essa."
        )

        self.pattern_expert = Agent(
            name="Pattern Analyst",
            model=llm_specialists,
            description="Esperto in Candlestick e Chart Patterns.",
            instructions=[
                LINGUA,
                STRUTTURA,
                "Nella sezione '🛠️ STRUMENTI UTILIZZATI' elenca i pattern specifici cercati (es. Engulfing, Triangoli, Testa e Spalle).",
                "Analizza i pattern grafici basandoti sulle tue skill caricate dai libri di Bulkowski, Nison e Joe Ross.",
                "Struttura la risposta in sezioni markdown con titoli in italiano.",
            ],
        )

        self.trend_expert = Agent(
            name="Trend Analyst",
            model=llm_specialists,
            description="Esperto in Trend e Momentum.",
            instructions=[
                LINGUA,
                STRUTTURA,
                "Nella sezione '🛠️ STRUMENTI UTILIZZATI' elenca gli indicatori di trend applicati (es. SMA, EMA, Trendline, SuperTrend).",
                "Analizza il trend e il momentum basandoti sulle tue skill caricate dai libri di Murphy, Larry Williams e Brian Shannon.",
                "Struttura la risposta in sezioni markdown con titoli in italiano.",
            ],
        )

        self.sr_expert = Agent(
            name="SR Analyst",
            model=llm_specialists,
            description="Esperto in Supporti e Resistenze.",
            instructions=[
                LINGUA,
                STRUTTURA,
                "Nella sezione '🛠️ STRUMENTI UTILIZZATI' elenca i metodi usati (es. Pivot Points, Livelli Psicologici, Aree Supply/Demand).",
                "Struttura la risposta in sezioni markdown con titoli in italiano.",
            ],
        )

        self.volume_expert = Agent(
            name="Volume Analyst",
            model=llm_specialists,
            description="Maestro di VSA e Wyckoff. Analizza lo Sforzo vs Risultato.",
            instructions=[
                LINGUA,
                STRUTTURA,
                "Nella sezione '🛠️ STRUMENTI UTILIZZATI' elenca i concetti VSA applicati (es. No Demand, Climax, SOS, Wyckoff Phases).",
                "Esegui un'analisi volumetrica profonda usando VSA (Volume Spread Analysis).",
                "Cerca segnali di Accumulazione e Distribuzione di Wyckoff.",
                "Valuta Sforzo vs Risultato: se il volume è alto ma il prezzo non si muove, c'è assorbimento?",
                "Identifica Climax, No Demand, No Supply e Test dei minimi/massimi.",
                "Struttura la risposta in sezioni markdown con titoli in italiano.",
            ],
        )
        
        # 4. Creazione Team Desk (Capo Team)
        active_members = []
        if Calibrazione.AGENT_PATTERN_ENABLED: active_members.append(self.pattern_expert)
        if Calibrazione.AGENT_TREND_ENABLED: active_members.append(self.trend_expert)
        if Calibrazione.AGENT_SR_ENABLED: active_members.append(self.sr_expert)
        if Calibrazione.AGENT_VOLUME_ENABLED: active_members.append(self.volume_expert)
        
        if not active_members:
            logger.warning("[AGNO TEAM] Attenzione: Nessun agente tecnico attivo in Calibrazione.py!")
 
        self.team = Team(
            name="Technical Trading Desk",
            members=active_members,
            model=llm_desk,
            description="Sei il Capo del Trading Desk. Coordini gli esperti tecnici con focus primario sui VOLUMI.",
            instructions=[
                LINGUA,
                "Ricevi i dati OHLCV e interroga gli specialisti tecnici.",
                "Usa il Macro Sentiment ricevuto come bussola direzionale.",
                "L'Analisi Volumetrica del 'Volume Analyst' è il filtro finale: se i volumi non confermano il trend, segnalalo come RISCHIO ELEVATO.",
                "Fornisci il verdetto finale con Ingresso, Stop e Target, giustificandolo con la convalida volumetrica.",
                "Struttura la risposta in sezioni markdown con titoli in italiano.",
            ],
            db=self.storage,
            num_history_messages=3,
            markdown=True,
        )
        logger.success(f"[AGNO] Team Tecnico pronto con modelli: {llm_desk.id}/{llm_specialists.id}")

    def analizza_specialista(self, nome_specialista, data_summary, macro_sentiment="Neutrale"):
        """Esegue l'analisi di un singolo esperto (Modalità Sequenziale per risparmio quota)."""
        logger.info(f"[AGNO TEAM] Interrogazione specialistica: {nome_specialista}")
        
        # Cerchiamo l'agente corretto nel team
        agente = next((m for m in self.team.members if m.name == nome_specialista), None)
        if not agente:
            return f"Errore: Specialista {nome_specialista} non trovato."

        query = f"""
        DATI MERCATO:
        {data_summary}

        SENTIMENT MACRO DA RISPETTARE:
        {macro_sentiment}

        Esegui la tua analisi tecnica specifica come {nome_specialista}.
        IMPORTANTE: Rispondi ESCLUSIVAMENTE in italiano. Non usare parole inglesi. Non iniziare con 'Okay' o frasi introduttive in inglese.
        Inizia direttamente con la sezione '🛠️ STRUMENTI UTILIZZATI'.
        """
        
        response = agente.run(query)
        return _rimuovi_intro_inglese(response.content, marker="🛠️ STRUMENTI UTILIZZATI")

    def analizza_asset(self, data_summary, macro_sentiment="Neutrale"):
        # Metodo originale mantenuto per compatibilità
        logger.info(f"[AGNO TEAM] Avvio analisi con Sentiment Macro: {macro_sentiment}")
        
        query = f"""
        DATI MERCATO ATTUALI:
        {data_summary}
        
        DIREZIONE MACRO (MOLTO IMPORTANTE):
        {macro_sentiment}
        
        Esegui l'analisi coordinata e fornisci il verdetto unificato.
        """
        
        response = self.team.run(query)
        return response.content
