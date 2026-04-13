import os
import re
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


def _smart_sleep(error_message: str, fallback: int = 30) -> None:
    """
    Legge il tempo di attesa reale dal messaggio di errore Groq (rate limit)
    e aspetta esattamente il necessario + 2s di margine.

    Groq restituisce messaggi del tipo:
      "Please try again in 27.345s"
      "Please try again in 1m30s"

    Se il tempo non è estraibile, usa il valore fallback (default 30s).
    """
    # Pattern "in 27.345s"
    match_s = re.search(r"try again in ([\d.]+)s", error_message)
    if match_s:
        wait = float(match_s.group(1)) + 2
        logger.info(f"[RATE LIMIT] Attesa smart: {wait:.1f}s (da errore Groq)")
        time.sleep(wait)
        return

    # Pattern "in 1m30s" o "in 2m5.5s"
    match_ms = re.search(r"try again in (\d+)m([\d.]+)s", error_message)
    if match_ms:
        wait = int(match_ms.group(1)) * 60 + float(match_ms.group(2)) + 2
        logger.info(f"[RATE LIMIT] Attesa smart: {wait:.1f}s (da errore Groq)")
        time.sleep(wait)
        return

    # Fallback
    logger.info(f"[RATE LIMIT] Tempo non estraibile — attesa fallback: {fallback}s")
    time.sleep(fallback)


def _call_with_retry(fn, *args, max_retries: int = 3, fallback: int = 30, **kwargs):
    """
    Esegue fn(*args, **kwargs) con retry automatico in caso di rate limit Groq.
    Se Groq risponde con 429/rate-limit, legge il tempo reale da _smart_sleep
    e riprova. Dopo max_retries tentativi falliti rilancia l'eccezione.
    """
    for attempt in range(1, max_retries + 1):
        try:
            result = fn(*args, **kwargs)
            return result
        except Exception as e:
            err_str = str(e).lower()
            is_rate_limit = (
                "rate_limit" in err_str or
                "rate limit" in err_str or
                "429" in err_str or
                "try again in" in err_str or
                "too many requests" in err_str
            )
            if is_rate_limit and attempt < max_retries:
                logger.warning(f"[RATE LIMIT] Tentativo {attempt}/{max_retries} — {e}")
                _smart_sleep(str(e), fallback=fallback)
            else:
                raise


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

    def analizza_asset(self, data_dict, nome_asset, start_date=None, end_date=None, context_extra="", projection_end_date=None):
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
            macro_sentiment = _call_with_retry(
                self.macro_expert.analizza,
                query_macro,
                start_date=start_date,
                end_date=end_date,
                symbol=nome_asset
            )
            logger.success("Sentiment Macro ottenuto.")
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
        # Strategia di compressione per rispettare il context window del LLM
        # mantenendo la copertura dell'INTERO periodo su tutti i timeframe:
        #
        # - 1D raw:   intero periodo (60 giorni ≈ 60 righe, sempre compatto) → LUNGO TERMINE
        # - 4H:       aggregazione settimanale per il periodo completo (≈ 9 righe)
        #             + ultimi 90 raw per il dettaglio recente (~15 giorni)   → MEDIO TERMINE
        # - 1H:       aggregazione giornaliera per il periodo completo (≈ 60 righe)
        #             + ultime 72 raw per il dettaglio intraday recente (~3gg) → BREVE TERMINE

        df_1h_all = data_dict["1h"]
        df_4h_all = data_dict["4h"] if ("4h" in data_dict and data_dict["4h"] is not None and not data_dict["4h"].empty) else None
        df_1d_all = data_dict["1d"]

        # --- 4H: aggregazione settimanale (periodo completo) + raw recenti ---
        df_4h_str = ""
        if df_4h_all is not None and not df_4h_all.empty:
            df_4h_weekly = df_4h_all.resample("W").agg(
                {"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"}
            ).dropna()
            df_4h_recent = df_4h_all.tail(90)
            df_4h_str = (
                f"DATI 4H — MEDIO TERMINE ({len(df_4h_all)} candele totali nel periodo):\n"
                f"Riepilogo Settimanale — intero periodo ({len(df_4h_weekly)} settimane):\n"
                f"{df_4h_weekly.to_string()}\n\n"
                f"Dettaglio Raw Recente (ultime {len(df_4h_recent)} candele 4H ~{len(df_4h_recent)//6} giorni):\n"
                f"{df_4h_recent.to_string()}"
            )

        # --- 1H: aggregazione giornaliera (periodo completo) + raw recenti ---
        df_1h_daily = df_1h_all.resample("D").agg(
            {"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"}
        ).dropna()
        df_1h_recent = df_1h_all.tail(72)

        ctx_summary = f"""PERIODO ANALISI: dal {start_date or 'N/D'} al {end_date or 'N/D'}

CONTESTO STRATEGICO (DAI LIBRI):
{knowledge_context}

GUIDA MACRO (dal Macro Strategist — usa questa come bussola direzionale):
{macro_sentiment}

DATI 1H — BREVE TERMINE ({len(df_1h_all)} candele totali nel periodo):
Riepilogo Giornaliero — intero periodo ({len(df_1h_daily)} giorni):
{df_1h_daily.to_string()}

Dettaglio Raw Recente (ultime {len(df_1h_recent)} candele 1H ~3 giorni):
{df_1h_recent.to_string()}

{df_4h_str}

DATI 1D — LUNGO TERMINE ({len(df_1d_all)} giorni — intero periodo selezionato):
{df_1d_all.to_string()}

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
                    altri_risultati = {
                        k: v for k, v in results_tech.items()
                        if v not in ("Analisi Disattivata", "N/D", "")
                    }
                    results_tech[nome] = _call_with_retry(
                        agente.analizza,
                        ctx_summary, macro_sentiment,
                        skills_guidance=guidance,
                        other_analyses=altri_risultati
                    )
                else:
                    results_tech[nome] = _call_with_retry(
                        agente.analizza,
                        ctx_summary, macro_sentiment,
                        skills_guidance=guidance
                    )
                logger.success(f"Risposta {nome} ricevuta.")
            except Exception as e:
                logger.error(f"[SUPERVISORE] Errore {nome}: {e}")
                results_tech[nome] = f"❌ Errore durante l'analisi: {e}"

        # ── Classificazione tecniche applicate vs. consultate ─────────────
        _domain_to_specialist = {
            "pattern": "Pattern Analyst",
            "trend":   "Trend Analyst",
            "sr":      "SR Analyst",
            "volume":  "Volume Analyst",
        }
        _techniques_pd = chosen_tools.get("techniques_per_domain", {})
        applied_per_domain: dict = {}

        for _domain, _specialist in _domain_to_specialist.items():
            _text = results_tech.get(_specialist, "")
            if not isinstance(_text, str) or not _text:
                applied_per_domain[_domain] = []
                continue
            _text_lower = _text.lower()
            _applied: list[str] = []
            for _book_techs in _techniques_pd.get(_domain, {}).values():
                for _tech in _book_techs:
                    _name = _tech["name"] if isinstance(_tech, dict) else str(_tech)
                    _clean = re.sub(r'\s*\([^)]*\)', '', _name.lower()).strip()
                    if _clean in _text_lower:
                        _applied.append(_name)
            applied_per_domain[_domain] = _applied

        chosen_tools["applied_techniques_per_domain"] = applied_per_domain
        logger.info(
            f"[SUPERVISORE] Tecniche applicate — "
            + ", ".join(f"{d}: {len(applied_per_domain[d])}" for d in _domain_to_specialist)
        )

        # ── Step 4: Verdetto Finale (Macro Expert + Skill Synthesizer) ───
        logger.info("Generazione verdetto finale (MacroExpert + trading-verdict-synthesizer)...")
        verdetto_finale = _call_with_retry(
            self.macro_expert.sintetizza_verdetto,
            nome_asset, macro_sentiment, results_tech,
            projection_end_date=projection_end_date
        )
        logger.success("Verdetto finale generato.")

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
