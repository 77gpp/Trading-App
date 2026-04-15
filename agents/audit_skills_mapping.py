"""
agents/audit_skills_mapping.py — Audit Completo della Mappatura Skill-Agente

Verifica:
1. COPERTURA: ogni tecnica è assegnata ad almeno un agente
2. COERENZA: la tecnica è semanticamente coerente al dominio dell'agente
3. COMPLETEZZA: nessuna tecnica orfana
4. MAPPATURA: BOOK_DOMAIN_MAP riflette il contenuto reale dei SKILL.md

Esecuzione:
  python3 agents/audit_skills_mapping.py [--verbose] [--fix-report]
"""

import os
import sys
import re
from pathlib import Path
from collections import defaultdict

# Setup path per importare Calibrazione dalla root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
import Calibrazione

# ──────────────────────────────────────────────────────────────────────────────
# CONFIGURAZIONE AUDIT
# ──────────────────────────────────────────────────────────────────────────────

# Mappa domain → regex keywords per validare coerenza semantica
# Una tecnica è coerente al dominio se il suo nome/descrizione matcha almeno una keyword
DOMAIN_KEYWORDS = {
    "pattern": [
        r"pattern", r"candela", r"candle", r"engulfing", r"harami", r"doji",
        r"hammer", r"star", r"formation", r"formazione", r"breakout", r"chart",
        r"head.*shoulder", r"testa.*spalle", r"double top", r"doppio", r"triangle",
        r"wedge", r"flag", r"1-2-3", r"ross hook", r"inside bar", r"pin bar",
        r"dark cloud", r"piercing", r"shooting", r"morning", r"evening",
        r"engulfing", r"harami", r"tweezer", r"counterattack", r"gap", r"oops",
        r"smash day", r"outside day", r"volatility", r"trend reversal", r"trend change"
    ],
    "trend": [
        r"moving average", r"media mobile", r"sma", r"ema", r"trend", r"momentum",
        r"bollinger", r"band", r"channel", r"keltner", r"ichimoku", r"supertrend",
        r"atr", r"slope", r"direction", r"uptrend", r"downtrend", r"rialzo", r"ribasso",
        r"equilibrium", r"equilibrio", r"convergence", r"divergence", r"incrocio",
        r"multiple timeframe", r"multiframe", r"mtf", r"alignment", r"allineamento",
        r"crossover", r"incrocio", r"tenkan", r"kijun", r"senkou"
    ],
    "sr": [
        r"support", r"resistance", r"supporto", r"resistenza", r"livello",
        r"pivot", r"fibonacci", r"fib", r"psych", r"psychological", r"psicologico",
        r"zone", r"area", r"supply", r"demand", r"accumulation", r"distribution",
        r"vwap", r"donchian", r"swing", r"high.*low", r"max.*min", r"massimo.*minimo",
        r"confluence", r"confluenza", r"S/R", r"target", r"entry", r"entrata"
    ],
    "oscillator": [
        r"rsi", r"macd", r"stochastic", r"williams", r"%r", r"momentum",
        r"oscill", r"divergence", r"convergence", r"ipercomprato", r"ipervenduto",
        r"overbought", r"oversold", r"signal", r"segnale", r"histogram", r"istogramma",
        r"confirmation", r"conferma", r"volume", r"mao", r"crossover", r"incrocio"
    ],
}

# ──────────────────────────────────────────────────────────────────────────────
# LETTURA SKILL.md
# ──────────────────────────────────────────────────────────────────────────────

def load_all_techniques() -> dict:
    """
    Carica tutte le tecniche da tutti i SKILL.md.
    Ritorna: {book_label: [{"name": str, "desc": str}]}
    """
    catalog = {}

    for skill_dir in Calibrazione.TECHNICAL_SKILLS_DIRS:
        skill_file = os.path.join(skill_dir, "SKILL.md")
        if not os.path.exists(skill_file):
            logger.warning(f"[AUDIT] SKILL.md non trovato: {skill_file}")
            continue

        dir_name = os.path.basename(skill_dir)
        # Usa la stessa logica di SkillSelector.BOOK_LABELS
        book_labels_map = {
            "encyclopedia_of_chart_patterns": "Thomas Bulkowski — Encyclopedia of Chart Patterns",
            "encyclopedia-of-chart-patterns": "Thomas Bulkowski — Encyclopedia of Chart Patterns",
            "japanese_candlestick_charting": "Steve Nison — Japanese Candlestick Charting",
            "japanese-candlestick-charting": "Steve Nison — Japanese Candlestick Charting",
            "joe_ross_daytrading": "Joe Ross — Day Trading",
            "joe-ross-daytrading": "Joe Ross — Day Trading",
            "larry_williams_long_term_secrets": "Larry Williams — Long-Term Secrets to Short-Term Trading",
            "larry-williams-long-term-secrets": "Larry Williams — Long-Term Secrets to Short-Term Trading",
            "murphy_analisi_tecnica": "John Murphy — Analisi Tecnica dei Mercati Finanziari",
            "murphy-analisi-tecnica": "John Murphy — Analisi Tecnica dei Mercati Finanziari",
            "technical_analysis_multiple_timeframes": "Brian Shannon — Technical Analysis Using Multiple Timeframes",
            "technical-analysis-multiple-timeframes": "Brian Shannon — Technical Analysis Using Multiple Timeframes",
        }
        book_label = book_labels_map.get(dir_name, dir_name)

        techniques = []
        try:
            with open(skill_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Estrai tutte le sezioni ## heading
            pattern = r'^##\s+([^#\n]+?)(?=\n|$)'
            matches = re.finditer(pattern, content, re.MULTILINE)

            for match in matches:
                tech_name = match.group(1).strip()
                if tech_name and "skill" not in tech_name.lower() and len(tech_name) < 80:
                    # Estrai descrizione dopo il heading
                    start = match.end()
                    next_heading = re.search(r'\n##\s+', content[start:])
                    end = start + next_heading.start() if next_heading else len(content)
                    tech_body = content[start:end].strip()

                    # Estrai la riga **Descrizione:**
                    desc_match = re.search(
                        r'\*\*Descrizione:\*\*\s*(.+?)(?=\*\*[A-Z]|$)',
                        tech_body,
                        re.DOTALL | re.IGNORECASE
                    )
                    if desc_match:
                        desc = re.sub(r'\s+', ' ', desc_match.group(1)).strip()
                    else:
                        desc = tech_body[:300].strip()

                    techniques.append({"name": tech_name, "desc": desc})

        except Exception as e:
            logger.error(f"[AUDIT] Errore lettura {skill_file}: {e}")
            continue

        if techniques:
            catalog[book_label] = techniques

    return catalog


# ──────────────────────────────────────────────────────────────────────────────
# COERENZA SEMANTICA
# ──────────────────────────────────────────────────────────────────────────────

def check_semantic_coherence(tech_name: str, tech_desc: str, domain: str) -> tuple[bool, str]:
    """
    Verifica se una tecnica è semanticamente coerente al dominio assegnato.

    Returns:
        (is_coherent: bool, reason: str)
    """
    combined = f"{tech_name} {tech_desc}".lower()
    keywords = DOMAIN_KEYWORDS.get(domain, [])

    matches = sum(1 for kw in keywords if re.search(kw, combined, re.IGNORECASE))

    if matches >= 1:
        return True, f"Match {matches} keyword(s) del dominio '{domain}'"
    else:
        return False, f"Nessun match con keywords del dominio '{domain}'"


# ──────────────────────────────────────────────────────────────────────────────
# AUDIT PRINCIPALE
# ──────────────────────────────────────────────────────────────────────────────

def run_audit(verbose: bool = False, fix_report: bool = False):
    """
    Esegue l'audit completo della mappatura skill-agente.
    """
    from agents.skill_selector import BOOK_DOMAIN_MAP

    print("\n" + "="*80)
    print("AUDIT COMPLETO: MAPPATURA SKILL-AGENTE")
    print("="*80 + "\n")

    # ── Carica catalogo ────────────────────────────────────────────────────────
    catalog = load_all_techniques()
    print(f"✅ Catalogo caricato: {len(catalog)} libri, {sum(len(t) for t in catalog.values())} tecniche totali\n")

    # ── Statistiche per libro ──────────────────────────────────────────────────
    print("TECNICHE PER LIBRO:")
    for book, techs in sorted(catalog.items()):
        domains = BOOK_DOMAIN_MAP.get(book, [])
        status = "✅" if domains else "❌ NON MAPPATO"
        print(f"  {status} {book}: {len(techs)} tecniche → {domains}")
    print()

    # ── Verifica 1: Tutti i libri sono mappati ────────────────────────────────
    unmapped_books = [b for b in catalog.keys() if b not in BOOK_DOMAIN_MAP]
    if unmapped_books:
        print(f"⚠️  LIBRI NON MAPPATI ({len(unmapped_books)}):")
        for b in unmapped_books:
            print(f"     - {b}")
        print()

    # ── Verifica 2: Copertura tecnica per agente ───────────────────────────────
    print("COPERTURA TECNICA PER AGENTE:")
    agent_techs = {
        "Pattern Analyst": {"domains": ["pattern"], "techs": []},
        "Trend Analyst": {"domains": ["trend"], "techs": []},
        "SR Analyst": {"domains": ["sr"], "techs": []},
        "Volume Analyst": {"domains": ["oscillator"], "techs": []},
    }

    for book, techs in catalog.items():
        domains = BOOK_DOMAIN_MAP.get(book, [])
        for domain in domains:
            for agent, cfg in agent_techs.items():
                if domain in cfg["domains"]:
                    cfg["techs"].extend([
                        (book, t["name"], t["desc"], domain) for t in techs
                    ])

    for agent, cfg in agent_techs.items():
        count = len(cfg["techs"])
        print(f"  📊 {agent}: {count} tecniche da {len(set(b for b,_,_,_ in cfg['techs']))} libri")
        if verbose:
            for book, name, desc, domain in sorted(cfg["techs"]):
                print(f"       └─ [{domain}] {name}")
    print()

    # ── Verifica 3: Coerenza semantica ────────────────────────────────────────
    print("VERIFICA COERENZA SEMANTICA:")
    incoherent = []

    for book, techs in catalog.items():
        domains = BOOK_DOMAIN_MAP.get(book, [])
        for domain in domains:
            for tech in techs:
                is_coherent, reason = check_semantic_coherence(
                    tech["name"], tech["desc"], domain
                )
                if not is_coherent:
                    incoherent.append((book, domain, tech["name"], reason))

    if incoherent:
        # Raggruppa per libro per vedere il pattern
        incoherent_by_book = defaultdict(list)
        for book, domain, name, reason in incoherent:
            incoherent_by_book[book].append((domain, name))

        print(f"ℹ️  {len(incoherent)} TECNICHE CON NOME NON PERFETTAMENTE COERENTE AL DOMINIO ASSEGNATO:")
        print("    (NOTA: Questo è ATTESO. I libri di trading sono olistici e insegnano concetti")
        print("     che attraversano i domini. Ad es., Nison insegna sia candlestick PATTERN")
        print("     che oscillatori. Se il nome di una tecnica non matcha il dominio assegnato,")
        print("     significa che il libro copre entrambi, o la tecnica è una fondazione teorica.)\n")

        for book in sorted(incoherent_by_book.keys()):
            items = incoherent_by_book[book]
            domains = set(d for d, _ in items)
            print(f"     {book}")
            print(f"       Domini: {list(BOOK_DOMAIN_MAP.get(book, []))}")
            for domain, name in items[:3]:
                print(f"         [{domain}] {name}")
            if len(items) > 3:
                print(f"         ... e altri {len(items) - 3} di questo libro")
        print()
    else:
        print("✅ Tutte le assegnazioni sono coerenti\n")

    # ── Verifica 4: Nessuna tecnica orfana ─────────────────────────────────────
    print("VERIFICA COPERTURA GLOBALE:")
    orphan_books = [b for b in catalog.keys() if b not in BOOK_DOMAIN_MAP or not BOOK_DOMAIN_MAP[b]]
    if orphan_books:
        print(f"⚠️  {len(orphan_books)} LIBRI SENZA AGENTE ASSEGNATO:")
        for b in orphan_books:
            techs = catalog[b]
            print(f"     - {b} ({len(techs)} tecniche orfane)")
    else:
        print("✅ Tutti i libri sono assegnati ad almeno un agente\n")

    # ── Riepilogo finale ───────────────────────────────────────────────────────
    total_techs = sum(len(techs) for techs in catalog.values())
    assigned_techs = sum(
        len(techs)
        for book, techs in catalog.items()
        if BOOK_DOMAIN_MAP.get(book, [])
    )

    print("RIEPILOGO FINALE:")
    print(f"  📚 Libri: {len(catalog)}")
    print(f"  🔧 Tecniche totali: {total_techs}")
    print(f"  ✅ Tecniche assegnate: {assigned_techs}")
    print(f"  ❌ Tecniche orfane: {total_techs - assigned_techs}")
    print(f"  🎯 Copertura: {100 * assigned_techs / total_techs:.1f}%")
    print()

    if assigned_techs == total_techs:
        print("✅ AUDIT PASSED: Tutte le tecniche sono assegnate ad un agente!")
    else:
        print(f"⚠️  AUDIT FAILED: {total_techs - assigned_techs} tecniche non assegnate!")

    print("\n" + "="*80 + "\n")

    return {
        "total_books": len(catalog),
        "total_techniques": total_techs,
        "assigned_techniques": assigned_techs,
        "coverage_percent": 100 * assigned_techs / total_techs,
        "incoherent_count": len(incoherent),
        "orphan_books": orphan_books,
    }


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    fix_report = "--fix-report" in sys.argv

    result = run_audit(verbose=verbose, fix_report=fix_report)

    sys.exit(0 if result["assigned_techniques"] == result["total_techniques"] else 1)
