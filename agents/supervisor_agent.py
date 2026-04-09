import os
import sys
import time
import datetime
from dotenv import load_dotenv
from loguru import logger
import Calibrazione

# Import dei componenti Agno V5
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.agno_macro_expert import AgnoMacroExpert
from agents.context_expander_agent import ContextExpanderAgent
from agents.skill_selector import SkillSelector
from agents.specialists.pattern_agent import PatternAgent
from agents.specialists.trend_agent import TrendAgent
from agents.specialists.sr_agent import SRAgent
from agents.specialists.volume_agent import VolumeAgent

load_dotenv()

class SupervisorAgent:
    """
    Controller Multi-Agente V5 (Ibrido: Gemini + Qwen).
    Gestisce il flusso tra:
    - Analisi Macro (Qwen) — guida strategica per tutto il team
    - Selezione Skill (Llama) — sceglie quali tecniche dai libri applicare
    - Ricerca Libri/Knowledge (Gemini Agentic Search)
    - 4 Specialisti Tecnici Standalone (Qwen) — ognuno con le proprie Skill
    - Verdetto Finale (Qwen) — sintesi operativa con Bias, Entry, SL, TP
    """

    def __init__(self):
        self.provider = Calibrazione.LLM_PROVIDER
        self.storage_location = Calibrazione.STORAGE_LOCATION
        self.db_path = Calibrazione.DATABASE_PATH

        # Agenti di alto livello
        self.macro_expert   = AgnoMacroExpert()
        self.knowledge_expert = ContextExpanderAgent()

        # 4 Specialisti Tecnici Standalone (con Skill dai libri)
        self.pattern_agent = PatternAgent()
        self.trend_agent   = TrendAgent()
        self.sr_agent      = SRAgent()
        self.volume_agent  = VolumeAgent()

        logger.success("[AGNO SUPERVISOR] Sistema V5 IBRIDO pronto (Gemini + Qwen).")

    def analizza_asset(self, data_dict, nome_asset, start_date=None, end_date=None, context_extra=""):
        """
        Master Flow V5 (Modalità Sequenziale Salva-Quota).
        Restituisce una tupla (report_markdown, chosen_tools).

        Flusso:
          1. MacroExpert → sentiment macro e guida strategica
          1.5 SkillSelector → sceglie strumenti e produce skills_guidance per specialista
          2. ContextExpander → ricerca conoscenza nei libri (Gemini)
          3. 4 Specialisti tecnici standalone → analisi con Skill e guidance
          4. Verdetto Finale → sintesi operativa
        """
        logger.info(f"\n{'='*60}\nAVVIO ANALISI SEQUENZIALE su {nome_asset}\nPeriodo: {start_date} -> {end_date}\n{'='*60}")

        # ── Step 1: Analisi Macro ─────────────────────────────────────
        if Calibrazione.AGENT_MACRO_ENABLED:
            query_macro = f"{nome_asset} news and global macro sentiment"
            macro_sentiment = self.macro_expert.analizza(query_macro, start_date=start_date, end_date=end_date, symbol=nome_asset)
            logger.info("Sentiment Macro ottenuto. Attesa 25s...")
            time.sleep(25)
        else:
            logger.info("[SUPERVISORE] Analisi Macro disattivata. Salto lo Step 1.")
            macro_sentiment = "ANALISI MACRO DISATTIVATA — bias direzionale non disponibile."

        # ── Step 1.5: Selezione Strumenti e Skills Guidance ──────────
        logger.info(f"[SUPERVISORE] Selezione strumenti tecnici per {nome_asset}...")
        skill_selector = SkillSelector()
        chosen_tools = skill_selector.select_tools(nome_asset, macro_sentiment, data_dict)
        if not chosen_tools.get("success", True):
            raise RuntimeError(
                f"[SUPERVISORE] Selezione strumenti AI fallita: {chosen_tools.get('error', 'Unknown error')}. "
                "Verifica la risposta del modello SkillSelector nei log."
            )
        logger.success("[SUPERVISORE] Strumenti selezionati con successo.")

        # ── Step 2: Ricerca Biblioteca Gemini ────────────────────────
        logger.info(f"[SUPERVISORE] Interrogazione Biblioteca Gemini per {nome_asset}...")
        query_knowledge = (
            f"Quali sono le migliori strategie di trading e i pattern più affidabili "
            f"descritti nei libri per l'asset {nome_asset} in un mercato con sentiment {macro_sentiment}?"
        )
        knowledge_context = self.knowledge_expert.search_knowledge(query_knowledge)

        # ── Preparazione contesto dati (1H + 4H + 1D) ───────────────
        df_4h_str = ""
        if "4h" in data_dict and data_dict["4h"] is not None and not data_dict["4h"].empty:
            df_4h_str = (
                f"DATI 4H (ultime {Calibrazione.TECH_MID_TERM_CANDLES} candele):\n"
                f"{data_dict['4h'].tail(Calibrazione.TECH_MID_TERM_CANDLES).to_string()}"
            )

        ctx_summary = f"""PERIODO ANALISI: dal {start_date or 'N/D'} al {end_date or 'N/D'}

CONTESTO STRATEGICO (DAI LIBRI):
{knowledge_context}

GUIDA MACRO (dal Macro Strategist — usa questa come bussola direzionale):
{macro_sentiment}

DATI 1H (ultime {Calibrazione.TECH_SHORT_TERM_CANDLES} candele):
{data_dict["1h"].tail(Calibrazione.TECH_SHORT_TERM_CANDLES).to_string()}

{df_4h_str}

DATI 1D (intero periodo selezionato — {len(data_dict["1d"])} giorni):
{data_dict["1d"].to_string()}

{context_extra}"""

        # ── Step 3: Analisi Tecnica Sequenziale (4 Specialisti) ──────
        skills_guidance = chosen_tools.get("skills_guidance", {})

        specialist_config = [
            ("Pattern Analyst", Calibrazione.AGENT_PATTERN_ENABLED, self.pattern_agent, "pattern"),
            ("Trend Analyst",   Calibrazione.AGENT_TREND_ENABLED,   self.trend_agent,   "trend"),
            ("SR Analyst",      Calibrazione.AGENT_SR_ENABLED,       self.sr_agent,      "sr"),
            ("Volume Analyst",  Calibrazione.AGENT_VOLUME_ENABLED,   self.volume_agent,  "volume"),
        ]

        results_tech = {}
        logger.info("Inizio analisi tecnica sequenziale (4 specialisti)...")

        for nome, attivo, agente, guidance_key in specialist_config:
            if not attivo:
                results_tech[nome] = "Analisi Disattivata"
                continue

            guidance = skills_guidance.get(guidance_key, "")
            logger.info(f"Interrogazione {nome}...")
            try:
                if nome == "Volume Analyst":
                    # Il Volume Agent è il filtro finale: gli passiamo i risultati
                    # effettivi degli altri 3 specialisti già completati, così può
                    # validare i segnali reali (non solo i nomi delle tecniche selezionate).
                    altri_risultati = {
                        k: v for k, v in results_tech.items()
                        if v not in ("Analisi Disattivata", "N/D", "")
                    }
                    results_tech[nome] = agente.analizza(
                        ctx_summary, macro_sentiment,
                        skills_guidance=guidance,
                        other_analyses=altri_risultati
                    )
                else:
                    results_tech[nome] = agente.analizza(ctx_summary, macro_sentiment, skills_guidance=guidance)
            except Exception as e:
                logger.error(f"[SUPERVISORE] Errore {nome}: {e}")
                results_tech[nome] = f"❌ Errore durante l'analisi: {e}"

            logger.info(f"Risposta {nome} ricevuta. Attesa 25s...")
            time.sleep(25)

        # ── Step 4: Verdetto Finale (Macro Expert + Skill Synthesizer) ───
        logger.info("Generazione verdetto finale (MacroExpert + trading-verdict-synthesizer)...")
        verdetto_finale = self.macro_expert.sintetizza_verdetto(nome_asset, macro_sentiment, results_tech)
        logger.info("Verdetto generato. Attesa 25s...")
        time.sleep(25)

        # ── Assemblaggio Report Finale ────────────────────────────────
        if chosen_tools.get("success"):
            skills_list = ", ".join(chosen_tools.get("raw_skills_used", [])) or "Skills Library"
            tools_section = f"**Fonti di conoscenza applicate:** {skills_list}\n\n{chosen_tools['summary']}"
        else:
            tools_section = (
                f"> [!CAUTION]\n"
                f"> **FALLIMENTO SELEZIONE DINAMICA AI**: L'intelligenza artificiale non è riuscita a "
                f"personalizzare gli strumenti tecnici per {nome_asset} "
                f"({chosen_tools.get('error', 'Unknown Error')})."
            )

        specialist_map = [
            ("Pattern Analyst", "🔍"),
            ("Trend Analyst",   "📈"),
            ("SR Analyst",      "🎯"),
            ("Volume Analyst",  "🌊"),
        ]
        tech_sections = ""
        for nome_spec, emoji in specialist_map:
            contenuto = results_tech.get(nome_spec, "")
            if contenuto and contenuto not in ("Analisi Disattivata", "N/D"):
                tech_sections += f"\n### {emoji} {nome_spec}\n{contenuto}\n"

        oggi = datetime.date.today().strftime("%d/%m/%Y")

        report_definitivo = f"""# REPORT TRADING AI: {nome_asset} — {oggi}

Questo report è il risultato dell'analisi coordinata dal **SupervisorAgent V5**, integrando dati macroeconomici, notizie real-time e l'analisi tecnica specialistica di 4 agenti IA con accesso alle Skill dai libri di trading.

---

## 🌎 ANALISI MACROECONOMICA E NEWS

{macro_sentiment}

---

## 📖 CONTESTO DALLA LIBRERIA (Strategie Master)

{knowledge_context}

---

## 🛠️ STRUMENTI SELEZIONATI DALL'AI

{tools_section}

---

## 📊 ANALISI TEAM TECNICO
{tech_sections}
---

## 🚀 VERDETTO FINALE E SETUP

{verdetto_finale}
"""

        return report_definitivo, chosen_tools


if __name__ == "__main__":
    from data_fetcher import DataFetcher

    def test_v5():
        supervisore = SupervisorAgent()
        data = DataFetcher.get_mtf_data("GC=F", days=60)
        report, _ = supervisore.analizza_asset(data, "GC=F")
        print("\n--- REPORT TRADING V5 ---")
        print(report)

    test_v5()
