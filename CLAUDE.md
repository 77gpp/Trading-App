# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

```bash
# Activate virtual environment first (always)
source .venv/bin/activate

# CLI analysis (runs full pipeline on GC=F Gold Futures)
python3 app.py

# Web interface with backtesting UI (http://localhost:5001)
python3 frontend/app_web.py

# Test a single agent directly
python3 agents/supervisor_agent.py
```

## Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root with:
```
GEMINI_API_KEY=      # Google Gemini (knowledge/book search via ContextExpanderAgent)
GROQ_API_KEY=        # Groq LPU (Qwen inference for all analysis agents)
ALPACA_API_KEY=      # Alpaca Markets (live news feed)
ALPACA_SECRET_KEY=   # Alpaca authentication
```

## Central Configuration: `Calibrazione.py`

**All system behavior is controlled from this single file.** Never hardcode model names, paths, or flags elsewhere.

Key controls:
- `LLM_PROVIDER`: `'qwen'` (Groq) or `'gemini'`
- `MODEL_*`: Model ID per role (macro expert, tech orchestrator, specialists, skill selector)
- `AGENT_*_ENABLED`: Boolean flags to activate/deactivate each specialist agent
- `TECH_*_CANDLES`: Number of candles fed to technical agents per timeframe
- `TEMPERATURE_*`: Per-role temperature (0.0 for JSON/tool calls, 0.7 for reports)
- `TECHNICAL_SKILLS_DIRS`: List of skill library directories loaded by all 4 technical specialists

## Architecture

The system is a **sequential multi-agent pipeline** orchestrated by `SupervisorAgent`:

```
DataFetcher (Yahoo Finance OHLCV: 1h, 4h, 1d)
    ↓
SupervisorAgent (agents/supervisor_agent.py) — master flow controller
    ├── Step 1: AgnoMacroExpert → macro sentiment + news (Groq/Qwen + DuckDuckGo + Alpaca + YFinance)
    ├── Step 1.5: SkillSelector → AI picks which trading books to apply for this asset
    ├── Knowledge search: ContextExpanderAgent → Gemini searches skills_library/ PDFs
    └── Steps 2-5: AgnoTechnicalTeam.analizza_specialista() called 4× sequentially
        ├── Pattern Analyst (candlestick patterns — Nison, Bulkowski, Ross)
        ├── Trend Analyst (moving averages, momentum — Murphy, Shannon, Williams)
        ├── SR Analyst (support/resistance, Fibonacci, pivots)
        └── Volume Analyst ← FINAL VALIDATOR: vetoes signals if volumes diverge
```

**25-second sleep between each LLM call** — intentional for API rate limit compliance. Do not remove.

### Two parallel implementations of the technical team

Both exist and are in use:
- `agents/agno_technical_team.py` — used by `SupervisorAgent` via `analizza_specialista()`. Agents defined inline without `skills=` (simpler, faster).
- `agents/specialists/*.py` — standalone agent classes with full `skills=skill_dirs` loaded from `Calibrazione.TECHNICAL_SKILLS_DIRS`. Used independently or via `OrchestratorAgent`.

### Skills Library (`skills_library/`)

Each subfolder is an Agno-format skill: must contain a `SKILL.md` file with Agno frontmatter. The content of these files is the extracted knowledge from trading books. All 4 technical specialists share all 6 book skills. The macro strategist has its own skill in `macro_library/`.

### Model routing (`agents/model_factory.py`)

Always use `get_model(model_id, temperature=...)` to instantiate models. This factory handles the `LLM_PROVIDER` switch between Gemini and Groq/Qwen transparently.

### Web Frontend (`frontend/`)

Flask app on port 5001. API endpoints split into:
- `frontend/api/backtesting.py` — runs background analysis jobs with threading, exposes `/api/backtest/*`
- `frontend/api/data.py` — OHLCV + news retrieval, exposes `/api/data/*`

### Language

All agent instructions include `"Rispondi sempre in italiano"`. The full report must be in Italian. When adding new agents or modifying instructions, always include this directive.
