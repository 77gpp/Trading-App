# Skills Architecture Diagram

## Data Flow: Dall'Estrazione all'Agente

```
┌─────────────────────────────────────────────────────────────────┐
│                    6 SKILL.md FILES (485 Tecniche)              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ Nison (64)       │  │ Bulkowski (74)   │  │ Ross (263)   │  │
│  │ ────────────── │ │ ─────────────── │ │ ────────────── │  │
│  │ ## Hammer      │ │ ## H&S           │ │ ## 1-2-3 Top   │  │
│  │ **Descrizione..│ │ **Descrizione..│ │ **Descrizione..│  │
│  │ **Logica..     │ │ **Logica..     │ │ **Logica..     │  │
│  │ ...            │ │ ...            │ │ ...            │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ Williams (28)    │  │ Murphy (38)      │  │ Shannon (18) │  │
│  │ ────────────── │ │ ─────────────── │ │ ────────────── │  │
│  │ ## SMA 50      │ │ ## Fibonacci     │ │ ## MTF Align   │  │
│  │ **Descrizione..│ │ **Descrizione..│ │ **Descrizione..│  │
│  │ **Logica..     │ │ **Logica..     │ │ **Logica..     │  │
│  │ ...            │ │ ...            │ │ ...            │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    SkillSelector._load_technique_catalog()
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              CATALOG (485 tekniche, 3 campi)                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  {                                                               │
│    "Steve Nison": [                                              │
│      {                                                           │
│        "name": "Hammer",                                        │
│        "body": "Un pattern di inversione rialzista... [FULL]",  │
│        "desc": "Corpo piccolo ombra lunga... [SUMMARY]"        │
│      },                                                          │
│      { "name": "Doji", ... },                                   │
│      ...                                                         │
│    ],                                                            │
│    "Thomas Bulkowski": [ ... ],                                  │
│    ...                                                           │
│  }                                                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    BOOK_DOMAIN_MAP (Hardcoded)
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DOMAIN ASSIGNMENT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  BOOK_DOMAIN_MAP = {                                            │
│    "Steve Nison": ["pattern", "oscillator"],                   │
│    "Thomas Bulkowski": ["pattern", "oscillator"],              │
│    "Joe Ross": ["pattern", "oscillator"],                      │
│    "Larry Williams": ["trend", "sr", "oscillator"],            │
│    "John Murphy": ["pattern", "trend", "sr", "oscillator"],    │
│    "Brian Shannon": ["trend", "sr", "oscillator"]              │
│  }                                                               │
│                                                                  │
│  → Nison's 64 techs → pattern ✓ + oscillator ✓                 │
│  → Bulkowski's 74 techs → pattern ✓ + oscillator ✓             │
│  → Ross's 263 techs → pattern ✓ + oscillator ✓                 │
│  → Williams's 28 techs → trend ✓ + sr ✓ + oscillator ✓         │
│  → Murphy's 38 techs → ALL 4 DOMAINS ✓                         │
│  → Shannon's 18 techs → trend ✓ + sr ✓ + oscillator ✓          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
           _build_skills_guidance(catalog, asset_type)
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│          SKILLS GUIDANCE (4 Agent-Specific Prompts)             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ PATTERN ANALYST GUIDANCE                                   │ │
│ ├────────────────────────────────────────────────────────────┤ │
│ │ FOCUS SKILLS — Techniche OBBLIGATORIE:                     │ │
│ │ [Steve Nison]:                                             │ │
│ │   1. Hammer — Corpo piccolo ombra lunga...                │ │
│ │   2. Doji — Candela con apertura=chiusura...              │ │
│ │   ... (64 techniques)                                      │ │
│ │                                                             │ │
│ │ [Thomas Bulkowski]:                                        │ │
│ │   1. Head and Shoulders — Pattern inversione...            │ │
│ │   ... (74 techniques)                                      │ │
│ │                                                             │ │
│ │ [Joe Ross]:                                                │ │
│ │   1. 1-2-3 Top — Punto 1=max, punto 2=ritracciamento...   │ │
│ │   ... (263 techniques)                                     │ │
│ │                                                             │ │
│ │ [John Murphy]:                                             │ │
│ │   1. Pattern inversione — ...                              │ │
│ │   ... (38 techniques, solo pattern subset)                 │ │
│ │                                                             │ │
│ │ REGOLA: Analizza TUTTE le tecniche. Per non rilevate,     │ │
│ │         documenta "Non rilevato". Target = Murphy stats.   │ │
│ └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ TREND ANALYST GUIDANCE                                     │ │
│ ├────────────────────────────────────────────────────────────┤ │
│ │ FOCUS SKILLS — Techniche OBBLIGATORIE:                     │ │
│ │ [Larry Williams]:                                          │ │
│ │   1. SMA 50 — Media di brevissimo termine...              │ │
│ │   ... (28 techniques)                                      │ │
│ │                                                             │ │
│ │ [John Murphy]:                                             │ │
│ │   1. Moving Averages — Fondamenti trend...                │ │
│ │   ... (38 techniques, solo trend subset)                   │ │
│ │                                                             │ │
│ │ [Brian Shannon]:                                           │ │
│ │   1. MTF Alignment — Allineamento su H1/H4/D1...          │ │
│ │   ... (18 techniques)                                      │ │
│ │                                                             │ │
│ │ REGOLA: Analizza allineamento MTF. Riporta direzione,      │ │
│ │         forza, cross-over operativi.                       │ │
│ └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ SR ANALYST GUIDANCE                                        │ │
│ ├────────────────────────────────────────────────────────────┤ │
│ │ FOCUS SKILLS — Techniche OBBLIGATORIE:                     │ │
│ │ [Larry Williams]:                                          │ │
│ │   1. Swing Points — Minimi/massimi significativi...       │ │
│ │   ... (28 techniques)                                      │ │
│ │                                                             │ │
│ │ [John Murphy]:                                             │ │
│ │   1. Fibonacci Retracement — Livelli 23.6%, 38.2%...      │ │
│ │   ... (38 techniques, solo sr subset)                      │ │
│ │                                                             │ │
│ │ [Brian Shannon]:                                           │ │
│ │   1. VWAP — Prezzo medio ponderato volume...              │ │
│ │   ... (18 techniques)                                      │ │
│ │                                                             │ │
│ │ REGOLA: Mappa COMPLETA S/R. Usa confluenza (≥3 metodi     │ │
│ │         = livello CRITICO). Stima probabilità Bulkowski.   │ │
│ └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ VOLUME ANALYST GUIDANCE (Oscillator)                       │ │
│ ├────────────────────────────────────────────────────────────┤ │
│ │ FOCUS SKILLS — Techniche OBBLIGATORIE:                     │ │
│ │ [Steve Nison]:                                             │ │
│ │   1. RSI 14 — Ipercomprato >70, ipervenduto <30...        │ │
│ │   2. MACD — Incrocio signal line = entrata...              │ │
│ │   3. MAO — MAO positivo = trend rialzista...              │ │
│ │                                                             │ │
│ │ [Thomas Bulkowski]:                                        │ │
│ │   1. RSI Confirmation — (appendix)                         │ │
│ │                                                             │ │
│ │ [Joe Ross]:                                                │ │
│ │   1. Momentum Confirmation — (oscillator use)              │ │
│ │                                                             │ │
│ │ [Larry Williams]:                                          │ │
│ │   1. Williams %R — -80/-100 ipervenduto, 0/-20 comprато   │ │
│ │   2. MACD — (same as Nison)                                │ │
│ │                                                             │ │
│ │ [John Murphy]:                                             │ │
│ │   1. RSI Divergence — Divergenza prezzo vs RSI...          │ │
│ │   2. MACD — (extended)                                     │ │
│ │   3. Stochastic — (same as Nison)                          │ │
│ │                                                             │ │
│ │ [Brian Shannon]:                                           │ │
│ │   1. RSI on MTF — Conferm multi-timeframe...               │ │
│ │   2. MACD — (MTF context)                                  │ │
│ │                                                             │ │
│ │ REGOLA NISON: Pattern non confermato da oscillatore        │ │
│ │              = affidabilità RIDOTTA. Priorità a divergenze.│ │
│ └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                  supervisor_agent.py
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│           4 SPECIALISTI TECNICI (PARALLELO/SEQUENZIALE)         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Pattern Analyst.analizza(data, macro_sentiment,                │
│      skills_guidance=guidance["pattern"])                       │
│    ↓                                                             │
│    Analizza TUTTE le 439 tecniche. Per ciascuna:                │
│    - Rilevata? → (nome, validità, target)                      │
│    - Non rilevata? → "Non rilevato"                            │
│                                                                  │
│  Trend Analyst.analizza(data, macro_sentiment,                  │
│      skills_guidance=guidance["trend"])                         │
│    ↓                                                             │
│    Analizza TUTTE le 84 tecniche di trend.                      │
│    → Direzione, forza, allineamento MTF, crossover              │
│                                                                  │
│  SR Analyst.analizza(data, macro_sentiment,                     │
│      skills_guidance=guidance["sr"])                            │
│    ↓                                                             │
│    Analizza TUTTE le 84 tecniche S/R.                           │
│    → Mappa completa, confluenza, probabilità tenuta             │
│                                                                  │
│  Volume Analyst.analizza(data, macro_sentiment,                 │
│      skills_guidance=guidance["oscillator"],                    │
│      other_analyses={Pattern, Trend, SR results})               │
│    ↓                                                             │
│    Analizza TUTTE le 485 tecniche oscillator.                   │
│    → CONFERMA o INVALIDATE segnali degli altri                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    VERDETTO FINALE                              │
├─────────────────────────────────────────────────────────────────┤
│ Sintesi: trading-verdict-synthesizer.py                          │
│ Integra i 4 risultati specialisti → Raccomandazione operativa   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Audit Loop (Parte del CI/CD)

```
┌──────────────────────────┐
│  Developer modifica      │
│  - SKILL.md              │
│  - BOOK_DOMAIN_MAP       │
└──────────────────────────┘
        ↓
┌──────────────────────────────────────────────┐
│ python3 agents/audit_skills_mapping.py       │
├──────────────────────────────────────────────┤
│                                              │
│ Verifica:                                    │
│ 1. Tutte le 485 tecniche estratte? ✓        │
│ 2. Nessuna orfana? ✓                        │
│ 3. Coerenza semantica? ✓ (88% + cross-OK)   │
│                                              │
└──────────────────────────────────────────────┘
        ↓
     EXIT 0?
     /      \
   YES      NO
   /          \
  ↓            ↓
 PASS      FIX BUG
  ↓            ↓
DEPLOY     RETRY
```

---

## Key Statistics

```
Extraction Coverage:
├─ Total Techniques: 485
├─ Extracted: 485 ✓ 100%
├─ Orphaned: 0 ✓ 0%
└─ Coverage: 100% ✓

Domain Distribution:
├─ Pattern: 439 techniques (4 books)
├─ Trend: 84 techniques (3 books)
├─ SR: 84 techniques (3 books)
└─ Oscillator: 485 techniques (6 books, all contribute)

Book Assignment:
├─ Nison: pattern + oscillator
├─ Bulkowski: pattern + oscillator
├─ Ross: pattern + oscillator
├─ Williams: trend + sr + oscillator
├─ Murphy: pattern + trend + sr + oscillator
└─ Shannon: trend + sr + oscillator

Semantic Coherence:
├─ Perfect Name Match: 88.6% (428/485)
├─ Cross-Domain Teaching: 11.4% (57/485) — EXPECTED
└─ Functional Coverage: 100% ✓
```

---

**Generated:** 2026-04-15 | **Audit Status:** ✅ PASSED
