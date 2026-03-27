import os
from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb
from loguru import logger
import settings

class AgnoTechnicalTeam:
    """Team di esperti V5 (Configurable & Free)."""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_desk = settings.MODEL_TECH_ORCHESTRATOR
        self.model_specialists = settings.MODEL_TECH_SPECIALISTS
        self.db_path = settings.DATABASE_PATH
        self.skills_dir = settings.SKILLS_LIBRARY_DIR
        
        # 1. Configurazione Storage Locale (Condiviso per il Team)
        self.storage = None
        if settings.STORAGE_LOCATION == "local":
            self.storage = SqliteDb(
                session_table="technical_team_session",
                db_file=self.db_path
            )

        # 2. Caricamento Sommario Skills (File Search Bridge)
        # Leggiamo i primi 5000 caratteri di ogni file MD per dare il "Router"
        all_skills = ""
        if os.path.exists(self.skills_dir):
            for f in os.listdir(self.skills_dir)[:3]: # Limitiamo per token budget
                if f.endswith(".md"):
                    with open(os.path.join(self.skills_dir, f), "r") as f_in:
                        all_skills += f"\n--- {f} ---\n{f_in.read()[:2000]}\n"
        
        # 3. Definizione Agenti Specialisti
        self.pattern_expert = Agent(
            name="Pattern Analyst",
            model=Gemini(id=self.model_specialists, api_key=self.api_key),
            description="Esperto in Candlestick e Chart Patterns.",
            instructions=[f"ANALIZZA PATTERN USANDO QUESTE SKILL:\n{all_skills[:3000]}"],
        )
        
        self.trend_expert = Agent(
            name="Trend Analyst",
            model=Gemini(id=self.model_specialists, api_key=self.api_key),
            description="Esperto in Trend e Momentum.",
            instructions=[f"ANALIZZA TREND USANDO QUESTE SKILL:\n{all_skills[:3000]}"],
        )
        
        self.sr_expert = Agent(
            name="SR Analyst",
            model=Gemini(id=self.model_specialists, api_key=self.api_key),
            description="Esperto in Supporti e Resistenze.",
        )
        
        self.volume_expert = Agent(
            name="Volume Analyst",
            model=Gemini(id=self.model_specialists, api_key=self.api_key),
            description="Maestro di VSA e Wyckoff. Analizza lo Sforzo vs Risultato.",
            instructions=[
                "Esegui un'analisi volumetrica profonda usando VSA (Volume Spread Analysis).",
                "Cerca segnali di Accumulazione e Distribuzione di Wyckoff.",
                "Valuta Sforzo vs Risultato: se il volume è alto ma il prezzo non si muove, c'è assorbimento?",
                "Identifica Climax, No Demand, No Supply e Test dei minimi/massimi.",
            ],
        )
        
        # 4. Creazione Team Desk (Capo Team)
        active_members = []
        if settings.AGENT_PATTERN_ENABLED: active_members.append(self.pattern_expert)
        if settings.AGENT_TREND_ENABLED: active_members.append(self.trend_expert)
        if settings.AGENT_SR_ENABLED: active_members.append(self.sr_expert)
        if settings.AGENT_VOLUME_ENABLED: active_members.append(self.volume_expert)
        
        if not active_members:
            logger.warning("[AGNO TEAM] Attenzione: Nessun agente tecnico attivo in settings.py!")

        self.team = Team(
            name="Technical Trading Desk",
            members=active_members,
            model=Gemini(id=self.model_desk, api_key=self.api_key),
            description="Sei il Capo del Trading Desk. Coordini gli esperti tecnici con focus primario sui VOLUMI.",
            instructions=[
                "Ricevi i dati OHLCV e interroga gli specialisti tecnici.",
                "Usa il Macro Sentiment ricevuto come bussola direzionale.",
                "L'Analisi Volumetrica del 'Volume Analyst' è il filtro finale: se i volumi non confermano il trend, segnalalo come RISCHIO ELEVATO.",
                "Fornisci il verdetto finale con Ingresso, Stop e Target, giustificandolo con la convalida volumetrica.",
            ],
            db=self.storage,
            num_history_messages=3,
            markdown=True,
        )
        logger.success(f"[AGNO] Team Tecnico pronto con modelli: {self.model_desk}/{self.model_specialists}")

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
        """
        
        response = agente.run(query)
        return response.content

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
