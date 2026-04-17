"""
agents/skill_selector.py — Agente Selezionatore di Strumenti Tecnici.

Questo agente ha il compito di:
1. Leggere la tabella degli strumenti grafici disponibili (hardcoded, sempre aggiornata)
2. Leggere un sommario delle skill presenti nella skills_library
3. Basandosi sul contesto macro (asset analizzato, sentiment, tipo di mercato),
   scegliere quali strumenti tecnici usare e perché
4. Restituire una struttura JSON con i tool scelti per ciascun gruppo (Pattern, Trend, SR, Oscillator)
"""

import os
import json
import re
from loguru import logger
import Calibrazione

# ------------------------------------------------------------------
# CATALOGO COMPLETO DEGLI STRUMENTI DISPONIBILI NEL GRAFICO
# Questi ID devono corrispondere ESATTAMENTE ai case in computeOverlayData() di chart.js
# ------------------------------------------------------------------
AVAILABLE_TOOLS = {
    "pattern": [
        # --- Candele Singole (Nison) ---
        {"id": "pattern_doji",               "name": "Doji (Indecisione)",              "desc": "Candela con apertura=chiusura, segnala indecisione e possibile inversione"},
        {"id": "pattern_gravestone_doji",    "name": "Gravestone Doji",                 "desc": "Doji con ombra superiore lunga e open/close vicini al minimo, segnale ribassista"},
        {"id": "pattern_dragonfly_doji",     "name": "Dragonfly Doji",                  "desc": "Doji con ombra inferiore lunga e open/close vicini al massimo, segnale rialzista"},
        {"id": "pattern_long_legged_doji",   "name": "Long-Legged Doji",                "desc": "Doji con entrambe le ombre lunghe, massima indecisione, spesso segnala inversione"},
        {"id": "pattern_spinning_top",       "name": "Spinning Top",                    "desc": "Corpo piccolo con ombre simmetriche, indecisione, precede spesso inversioni"},
        {"id": "pattern_hammer",             "name": "Hammer / Hanging Man",            "desc": "Corpo piccolo con ombra lunga inferiore, potente segnale di inversione"},
        {"id": "pattern_inverted_hammer",    "name": "Inverted Hammer / Shooting Star", "desc": "Corpo piccolo con ombra superiore lunga, segnale di inversione dipendente dal contesto"},
        {"id": "pattern_shooting_star",      "name": "Shooting Star",                   "desc": "Ombra superiore ≥2× corpo, apre in uptrend, segnale ribassista Nison"},
        {"id": "pattern_marubozu",           "name": "Marubozu (Impulso Puro)",         "desc": "Candela senza ombre, indica forza/debolezza estrema e pressione istituzionale"},
        {"id": "pattern_belt_hold",          "name": "Belt-Hold Lines",                 "desc": "Candela senza ombra sul lato del trend precedente, forte segnale di inversione"},
        {"id": "pattern_pin_bar",            "name": "Pin Bar (Rejection)",             "desc": "Ombra molto lunga che mostra rifiuto del prezzo, usata in Price Action pura"},
        # --- Candele Doppie (Nison) ---
        {"id": "pattern_engulfing",          "name": "Bullish/Bearish Engulfing",       "desc": "Inversione a 2 candele, corpo della seconda ingloba la prima, molto affidabile"},
        {"id": "pattern_harami",             "name": "Harami (Inside Bar Candle)",      "desc": "Candela 'figlia' contenuta nella 'madre', pausa del trend e potenziale inversione"},
        {"id": "pattern_harami_cross",       "name": "Harami Cross",                    "desc": "Harami con seconda candela doji, segnale di inversione più forte dell'harami classico"},
        {"id": "pattern_tweezer",            "name": "Tweezer Top/Bottom",              "desc": "Due candele con max/min identici, forte resistenza o supporto psicologico"},
        {"id": "pattern_dark_cloud_cover",   "name": "Dark Cloud Cover",                "desc": "Candela rialzista + ribassista che chiude oltre metà della prima, segnale di distribuzione"},
        {"id": "pattern_piercing_line",      "name": "Piercing Pattern",                "desc": "Candela ribassista + rialzista che chiude oltre metà della prima, segnale di accumulazione"},
        {"id": "pattern_counterattack",      "name": "Counterattack Lines",             "desc": "Due candele opposte che chiudono allo stesso livello, inversione a livello critico"},
        {"id": "pattern_upside_gap_two_crows","name": "Upside-Gap Two Crows",           "desc": "3 candele: rialzista + gap up + 2 corvi ribassisti, segnale di esaurimento del rialzo"},
        # --- Candele Triple (Nison) ---
        {"id": "pattern_morning_star",       "name": "Morning/Evening Star",            "desc": "Pattern a 3 candele di inversione, tra i più affidabili della letteratura giapponese"},
        {"id": "pattern_morning_doji_star",  "name": "Morning Doji Star",               "desc": "Come Morning Star ma la candela centrale è un doji, segnale più forte"},
        {"id": "pattern_evening_doji_star",  "name": "Evening Doji Star",               "desc": "Come Evening Star ma la candela centrale è un doji, segnale più forte"},
        {"id": "pattern_three_candles",      "name": "Tre Soldati/Tre Corvi",           "desc": "Tre candele consecutive nella stessa direzione, segnale forte di continuazione"},
        {"id": "pattern_tasuki_gap",         "name": "Tasuki Gap",                      "desc": "Gap tra 2 candele + terza che riempie parzialmente il gap, continuazione del trend"},
        {"id": "pattern_rising_three_methods","name": "Rising/Falling Three Methods",   "desc": "Candela lunga + 3 piccole interne + candela lunga, classico pattern di continuazione"},
        {"id": "pattern_three_mountain_top", "name": "Three Mountain Top",              "desc": "Triplo massimo giapponese: tre picchi allo stesso livello, forte resistenza confermata"},
        # --- Formazioni Chartistiche ---
        {"id": "pattern_inside_bar",         "name": "Inside Bar (Compressione)",       "desc": "La candela corrente è contenuta in quella precedente, breakout imminente"},
        {"id": "pattern_powerbar",           "name": "Power Bars (Joe Ross)",           "desc": "Barre di impulso con range eccezionale, indicano partecipazione istituzionale"},
        {"id": "pattern_triangle",           "name": "Triangoli (Asc/Desc/Sim)",        "desc": "Pattern di consolidamento con target misurato pari alla base del triangolo"},
        {"id": "pattern_wedge",              "name": "Wedge Rising/Falling",            "desc": "Cuneo di inversione, molto frequente in mercati ciclici come Oro e Indici"},
        {"id": "pattern_flag",               "name": "Flag / Pennant",                  "desc": "Consolidamento rettangolare post-impulso, target = misura del palo della bandiera"},
        {"id": "pattern_double_top",         "name": "Double Top/Bottom (M/W)",         "desc": "Pattern di inversione classico di John Murphy, confermato dal breakout del neckline"},
        {"id": "pattern_head_shoulders",     "name": "Head and Shoulders",              "desc": "Pattern di inversione più famoso dell'analisi tecnica, alta probabilità con volume calante"},
        # --- Pattern Joe Ross (TLOC - La Legge dei Grafici) ---
        {"id": "pattern_1_2_3_top",          "name": "1-2-3 Top (Ross)",               "desc": "Punto 1=max, punto 2=ritracciamento, punto 3=rimbalzo < punto 1. Base di TLOC"},
        {"id": "pattern_1_2_3_bottom",       "name": "1-2-3 Bottom (Ross)",            "desc": "Punto 1=min, punto 2=rimbalzo, punto 3=ritracciamento > punto 1. Base di TLOC"},
        {"id": "pattern_ledge",              "name": "Ledge (Ross)",                   "desc": "Congestione ristretta di 4+ barre con range compresso, breakout imminente"},
        {"id": "pattern_trading_range",      "name": "Trading Range (Ross)",           "desc": "Congestione ampia con oscillazione laterale, entrata al breakout dei bordi"},
        {"id": "pattern_ross_hook",          "name": "Ross Hook",                      "desc": "Prima barra che viola il punto 3 del 1-2-3, il segnale di entrata principale di Ross"},
        {"id": "pattern_traders_trick",      "name": "Traders Trick Entry (TTE)",      "desc": "Entrata anticipata prima del Ross Hook, richiede conferma di direzione"},
        # --- Pattern Larry Williams ---
        {"id": "pattern_oops",               "name": "Oops Pattern (Williams)",        "desc": "Gap di apertura oltre il range di ieri + rientro nel range → inversione intraday"},
        {"id": "pattern_smash_day",          "name": "Smash Day Reversal",             "desc": "Barra con range eccezionale che chiude agli estremi opposti, esaurimento del movimento"},
        {"id": "pattern_outside_day",        "name": "Outside Day",                    "desc": "Barra che ingloba completamente la precedente (high>prev high AND low<prev low)"},
        {"id": "pattern_volatility_breakout","name": "Volatility Breakout (Williams)", "desc": "Breakout basato su ATR × fattore, segnale di momentum istituzionale"},
        {"id": "pattern_short_term_pivot",   "name": "Short-Term Pivot (Williams)",    "desc": "Pivot a 5 barre (2 barre più basse/alte a destra e sinistra), swing point Williams"},
    ],
    "trend": [
        # --- Medie Mobili Semplici ---
        {"id": "sma_10",               "name": "SMA 10",                     "desc": "Media di brevissimo termine per scalper e day trader"},
        {"id": "sma_20",               "name": "SMA 20",                     "desc": "Base delle Bollinger Bands, supporto/resistenza dinamica in trend forti"},
        {"id": "sma_50",               "name": "SMA 50",                     "desc": "La più seguita dagli istituzionali per identificare il trend primario"},
        {"id": "sma_100",              "name": "SMA 100",                    "desc": "Filtro di medio termine per eliminare il rumore di breve"},
        {"id": "sma_200",              "name": "SMA 200",                    "desc": "La barriera definitiva: sopra = bull market, sotto = bear market"},
        # --- Medie Esponenziali ---
        {"id": "ema_9",                "name": "EMA 9",                      "desc": "Usata dai trader di breve per segnali di entrata veloci"},
        {"id": "ema_20",               "name": "EMA 20",                     "desc": "Reattiva ai movimenti, ottima in mercati veloci come Crypto e Forex"},
        {"id": "ema_50",               "name": "EMA 50",                     "desc": "Media del trader swing per eccellenza, usata con EMA 200"},
        {"id": "ema_100",              "name": "EMA 100",                    "desc": "Zona di equilibrio tra breve e lungo termine"},
        {"id": "ema_200",              "name": "EMA 200",                    "desc": "Versione dinamica e reattiva della barriera di lungo termine"},
        # --- Canali e Bande ---
        {"id": "bollinger_upper",      "name": "Bollinger Band Superiore",   "desc": "Zona di ipercomprato dinamica, 2 deviazioni standard sopra SMA 20"},
        {"id": "bollinger_lower",      "name": "Bollinger Band Inferiore",   "desc": "Zona di ipervenduto dinamica, 2 deviazioni standard sotto SMA 20"},
        {"id": "bollinger_mid",        "name": "Bollinger Band Media",       "desc": "SMA 20, linea di regressione verso la media (mean reversion)"},
        {"id": "keltner_upper",        "name": "Keltner Channel Superiore",  "desc": "Canale basato su ATR, identificare squeeze di volatilità con Bollinger"},
        {"id": "keltner_lower",        "name": "Keltner Channel Inferiore",  "desc": "Supporto dinamico ATR-based, ottimo per mercati con trend forti"},
        # --- Indicatori di Trend ---
        {"id": "supertrend",           "name": "SuperTrend (ATR-based)",     "desc": "Segnali automatici Compra/Vendi con stop loss integrato basato su ATR"},
        {"id": "ichimoku_cloud_upper", "name": "Ichimoku Senkou A",          "desc": "Bordo superiore della nuvola Ichimoku, resistenza/supporto futura"},
        {"id": "ichimoku_cloud_lower", "name": "Ichimoku Senkou B",          "desc": "Bordo inferiore della nuvola Ichimoku, livello di equilibrio di lungo termine"},
        {"id": "ichimoku_kijun",       "name": "Ichimoku Kijun Sen",         "desc": "Linea di base Ichimoku (26 periodi), segnale con incrocio Tenkan"},
        {"id": "ichimoku_tenkan",      "name": "Ichimoku Tenkan Sen",        "desc": "Linea di conversione Ichimoku (9 periodi), incrocio con Kijun = segnale di entrata"},
        {"id": "atr_upper",            "name": "ATR Band Superiore",         "desc": "Banda superiore basata su ATR, utile per trailing stop e target dinamici"},
        {"id": "atr_lower",            "name": "ATR Band Inferiore",         "desc": "Banda inferiore basata su ATR, utile per trailing stop e target dinamici"},
    ],
    "sr": [
        # --- Livelli Matematici ---
        {"id": "pivot_points",         "name": "Pivot Points Giornalieri",   "desc": "PP, R1, R2, S1, S2 calcolati su OHLC del periodo precedente"},
        {"id": "pivot_weekly",         "name": "Pivot Points Settimanali",   "desc": "Livelli pivot calcolati su base settimanale, più duraturi e significativi"},
        {"id": "fib_retracement",      "name": "Fibonacci Retracement",      "desc": "Livelli 23.6%, 38.2%, 50%, 61.8%, 78.6% per ingressi in correzione"},
        {"id": "fib_extension",        "name": "Fibonacci Extension",        "desc": "Target di prezzo post-breakout: 127.2%, 161.8%, 200%, 261.8%"},
        # --- Livelli Psicologici ---
        {"id": "psych_levels",         "name": "Livelli Psicologici",        "desc": "Numeri tondi (es. 3000, 2500) con alta concentrazione di ordini istituzionali"},
        {"id": "psych_levels_fine",    "name": "Livelli Semi-Psicologici",   "desc": "Numeri a semidecina (500, 250) ugualmente seguiti dallo smart money"},
        # --- Supporti e Resistenze Dinamici ---
        {"id": "dynamic_support",      "name": "Supporto Dinamico (Swing)",  "desc": "Linea di supporto tracciata sui minimi di swing significativi"},
        {"id": "dynamic_resistance",   "name": "Resistenza Dinamica (Swing)","desc": "Linea di resistenza tracciata sui massimi di swing significativi"},
        {"id": "supply_zone",          "name": "Supply Zone (Distribuzione)","desc": "Area di prezzo dove storicamente i venditori istituzionali sono entrati"},
        {"id": "demand_zone",          "name": "Demand Zone (Accumulazione)","desc": "Area di prezzo dove storicamente gli acquirenti istituzionali hanno assorbito"},
        # --- Canali di Prezzo ---
        {"id": "linear_regression",    "name": "Canale di Regressione",      "desc": "Canale lineare mediato statisticamente, identifica la tendenza 'matematica'"},
        {"id": "donchian_upper",       "name": "Donchian Channel Superiore", "desc": "Massimo degli ultimi N periodi, usato nei sistemi Turtle Traders"},
        {"id": "donchian_lower",       "name": "Donchian Channel Inferiore", "desc": "Minimo degli ultimi N periodi, breakout = segnale di entrata Turtle"},
        {"id": "vwap",                 "name": "VWAP (Volume Weighted)",     "desc": "Prezzo medio ponderato sul volume, punto di equilibrio giornaliero istituzionale"},
    ],
    "oscillator": [
        # --- Oscillatori (pannello separato sotto il grafico) ---
        {"id": "rsi",          "name": "RSI 14",                    "desc": "Relative Strength Index: ipercomprato >70, ipervenduto <30. Nison+Murphy"},
        {"id": "macd_line",    "name": "MACD Line (12-26-9)",       "desc": "Differenza EMA12-EMA26, segnali di incrocio con signal line. Murphy"},
        {"id": "macd_signal",  "name": "MACD Signal",               "desc": "EMA 9 della MACD Line, segnale di acquisto/vendita al crossover"},
        {"id": "stochastic_k", "name": "Stochastic %K (14)",        "desc": "Posizione del close nel range degli ultimi 14 periodi. Nison"},
        {"id": "stochastic_d", "name": "Stochastic %D (3)",         "desc": "SMA(3) di %K, la linea di segnale dello Stochastic"},
        {"id": "williams_r",   "name": "Williams %R (14)",          "desc": "Indicatore momentum inverso: -100=ipervenduto, 0=ipercomprato. Larry Williams"},
        {"id": "mao",          "name": "MAO (Moving Avg Oscillator)","desc": "SMA12 - SMA26: momentum oscillator (Nison Cap.14). Positivo = trend rialzista, negativo = ribassista"},
    ],
}

# ------------------------------------------------------------------
# COLORI DI DEFAULT PER OGNI STRUMENTO
# Usati come fallback se l'AI non ne specifica uno valido
# ------------------------------------------------------------------
DEFAULT_COLORS = {
    # Pattern — Nison candele singole
    "pattern_doji":                "#ffa502",
    "pattern_gravestone_doji":     "#ff4757",
    "pattern_dragonfly_doji":      "#00d4aa",
    "pattern_long_legged_doji":    "#ffd32a",
    "pattern_spinning_top":        "#a29bfe",
    "pattern_hammer":              "#00d4aa",
    "pattern_inverted_hammer":     "#74b9ff",
    "pattern_shooting_star":       "#ff4757",
    "pattern_marubozu":            "#3f8ef5",
    "pattern_belt_hold":           "#fd79a8",
    "pattern_pin_bar":             "#ff9f43",
    # Pattern — Nison candele doppie
    "pattern_engulfing":           "#ff9f43",
    "pattern_harami":              "#ee5a24",
    "pattern_harami_cross":        "#e17055",
    "pattern_tweezer":             "#fd9644",
    "pattern_dark_cloud_cover":    "#ff4757",
    "pattern_piercing_line":       "#00d4aa",
    "pattern_counterattack":       "#a29bfe",
    "pattern_upside_gap_two_crows":"#d63031",
    # Pattern — Nison candele triple
    "pattern_morning_star":        "#00d4aa",
    "pattern_morning_doji_star":   "#55efc4",
    "pattern_evening_doji_star":   "#e84393",
    "pattern_three_candles":       "#3f8ef5",
    "pattern_tasuki_gap":          "#fdcb6e",
    "pattern_rising_three_methods":"#74b9ff",
    "pattern_three_mountain_top":  "#ff4757",
    # Pattern — Formazioni chartistiche
    "pattern_inside_bar":          "#fd9644",
    "pattern_powerbar":            "#f53b57",
    "pattern_triangle":            "#ee5a24",
    "pattern_wedge":               "#ff6b81",
    "pattern_flag":                "#fd9644",
    "pattern_double_top":          "#a29bfe",
    "pattern_head_shoulders":      "#e84393",
    # Pattern — Joe Ross
    "pattern_1_2_3_top":           "#ff4757",
    "pattern_1_2_3_bottom":        "#00d4aa",
    "pattern_ledge":               "#ffd32a",
    "pattern_trading_range":       "#74b9ff",
    "pattern_ross_hook":           "#f9ca24",
    "pattern_traders_trick":       "#6c5ce7",
    # Pattern — Larry Williams
    "pattern_oops":                "#00d4aa",
    "pattern_smash_day":           "#ff4757",
    "pattern_outside_day":         "#fd79a8",
    "pattern_volatility_breakout": "#f9ca24",
    "pattern_short_term_pivot":    "#a29bfe",
    # Volume
    "volume_vsa":                  "#3f8ef5",
    # Trend — SMA
    "sma_10":                      "#dfe6e9",
    "sma_20":                      "#dfe6e9",
    "sma_50":                      "#f9ca24",
    "sma_100":                     "#74b9ff",
    "sma_200":                     "#ff9f43",
    # Trend — EMA
    "ema_9":                       "#55efc4",
    "ema_20":                      "#00d4aa",
    "ema_50":                      "#fdcb6e",
    "ema_100":                     "#74b9ff",
    "ema_200":                     "#e17055",
    # Trend — Bande
    "bollinger_upper":             "rgba(116,185,255,0.8)",
    "bollinger_lower":             "rgba(116,185,255,0.8)",
    "bollinger_mid":               "rgba(116,185,255,0.5)",
    "keltner_upper":               "rgba(253,203,110,0.7)",
    "keltner_lower":               "rgba(253,203,110,0.7)",
    # Trend — Indicatori
    "supertrend":                  "#00d4aa",
    "ichimoku_cloud_upper":        "rgba(85,239,196,0.5)",
    "ichimoku_cloud_lower":        "rgba(255,118,117,0.4)",
    "ichimoku_kijun":              "#74b9ff",
    "ichimoku_tenkan":             "#fd79a8",
    "atr_upper":                   "rgba(253,203,110,0.6)",
    "atr_lower":                   "rgba(253,203,110,0.6)",
    # SR
    "pivot_points":                "#dfe6e9",
    "pivot_weekly":                "#b2bec3",
    "fib_retracement":             "#f9ca24",
    "fib_extension":               "#fd9644",
    "psych_levels":                "rgba(255,255,255,0.6)",
    "psych_levels_fine":           "rgba(255,255,255,0.4)",
    "dynamic_support":             "#00d4aa",
    "dynamic_resistance":          "#ff4757",
    "supply_zone":                 "rgba(255,71,87,0.25)",
    "demand_zone":                 "rgba(0,212,170,0.25)",
    "linear_regression":           "#a29bfe",
    "donchian_upper":              "rgba(116,185,255,0.7)",
    "donchian_lower":              "rgba(116,185,255,0.7)",
    "vwap":                        "#f9ca24",
    # Oscillatori
    "rsi":                         "#74b9ff",
    "macd_line":                   "#00d4aa",
    "macd_signal":                 "#ff9f43",
    "stochastic_k":                "#a29bfe",
    "stochastic_d":                "#fd79a8",
    "williams_r":                  "#f9ca24",
    "mao":                         "#55efc4",
}

# ------------------------------------------------------------------
# MAPPATURA LIBRO → DOMINI TECNICI (Deterministico, no LLM)
#
# Indica a quali specialisti (pattern/trend/sr/volume) ogni libro
# contribuisce conoscenza. Usato per costruire la skills_guidance
# in modo deterministico e completo, senza dipendere dall'LLM.
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# BOOK_DOMAIN_MAP — Profondo, basato sul contenuto reale di ogni libro.
#
# Ogni libro viene assegnato a TUTTI i domini che tratta in modo
# substantivo. La mappatura riflette i capitoli effettivi dei testi,
# non una semplificazione. Aggiornare questo dict quando si aggiungono
# nuovi libri alla skills_library.
#
# Domini:
#   pattern    → Pattern candlestick, formazioni chartistiche, entrate operative
#   trend      → Medie mobili, indicatori di trend, analisi multi-timeframe
#   sr         → Supporti/resistenze, livelli S/R dinamici e statici
#   oscillator → RSI, MACD, Stochastic, %R, MAO, divergenze, conferme
# ------------------------------------------------------------------
BOOK_DOMAIN_MAP: dict[str, list[str]] = {

    # ── Steve Nison — Japanese Candlestick Charting ─────────────────
    # Cap. 1-11:  analisi delle candele singole, doppie, triple → pattern
    # Cap. 12-14: utilizzo di RSI, Stochastic, MACD, MAO come conferme
    #             obbligatorie ai segnali candlestick → oscillator
    "Steve Nison — Japanese Candlestick Charting": ["pattern", "oscillator"],

    # ── Thomas Bulkowski — Encyclopedia of Chart Patterns ───────────
    # Parte 1-3:  ~74 pattern grafici con statistiche di breakout e target → pattern
    # Appendici:  conferme con RSI, MACD, volume → oscillator
    # (Target misurati sono derivati dal pattern, non S/R indipendente)
    "Thomas Bulkowski — Encyclopedia of Chart Patterns": ["pattern", "oscillator"],

    # ── Joe Ross — Day Trading (La Legge dei Grafici — TLOC) ────────
    # Parte 1-4:  1-2-3 Top/Bottom, Ross Hook, Ledge, Trading Range, entrate → pattern
    # Appendici:  Conferme con oscillatori e momentum → oscillator
    # (Livelli di entrata TLOC sono derivati dal pattern, non S/R indipendente)
    "Joe Ross — Day Trading": ["pattern", "oscillator"],

    # ── Larry Williams — Long-Term Secrets to Short-Term Trading ────
    # Cap. 1-5:   Swing highs/lows come S/R operativi, livelli psicologici → sr
    # Cap. 6-9:   Momentum, trend di breve e conferme di prezzo → trend
    # Cap. 10-14: Williams %R, MACD, pattern Oops, Smash Day → oscillator
    "Larry Williams — Long-Term Secrets to Short-Term Trading": ["trend", "sr", "oscillator"],

    # ── John Murphy — Analisi Tecnica dei Mercati Finanziari ────────
    # Cap. 1-5:   Fondamenti AT, trend, medie mobili → trend
    # Cap. 6-8:   Pattern grafici di inversione e continuazione → pattern
    # Cap. 9-10:  Supporti, resistenze, canali, Fibonacci → sr
    # Cap. 11-14: Oscillatori (RSI, MACD, Stochastic, divergenze) → oscillator
    # Cap. 15-16: Analisi volumetrica e Open Interest → (volume, trattato da Shannon)
    "John Murphy — Analisi Tecnica dei Mercati Finanziari": ["pattern", "trend", "sr", "oscillator"],

    # ── Brian Shannon — Technical Analysis Using Multiple Timeframes ─
    # Cap. 1-4:   Allineamento del trend su più timeframe → trend
    # Cap. 5-7:   Identificazione VWAP, S/R e livelli chiave MTF → sr
    # Cap. 8:     Uso di RSI e MACD per conferma MTF → oscillator
    "Brian Shannon — Technical Analysis Using Multiple Timeframes": ["trend", "sr", "oscillator"],
}

# ------------------------------------------------------------------
# TECHNIQUE_OVERLAY_MAP — Keyword → Overlay ID (chart.js)
#
# Per ogni tecnica estratta dai SKILL.md (heading ##), se il nome
# contiene la keyword (word-boundary, case-insensitive), viene
# associata all'overlay ID in computeOverlayData() di chart.js.
#
# Regole di ordinamento:
#   1. Le keyword PIÙ SPECIFICHE vengono PRIMA (es. "morning doji star"
#      prima di "doji") per evitare match prematuri sul termine generico.
#   2. Tecniche senza match → overlay_id=None (badge informativo,
#      nessun rendering grafico, ma comunque passata all'agente).
# ------------------------------------------------------------------

TECHNIQUE_OVERLAY_MAP: list[tuple[str, str]] = [
    # ── Doji variants (più specifici prima) ──────────────────────────
    ("morning doji star",           "pattern_morning_doji_star"),
    ("evening doji star",           "pattern_evening_doji_star"),
    ("gravestone doji",             "pattern_gravestone_doji"),
    ("dragonfly doji",              "pattern_dragonfly_doji"),
    ("long-legged doji",            "pattern_long_legged_doji"),
    ("long legged doji",            "pattern_long_legged_doji"),
    # ── Stars ────────────────────────────────────────────────────────
    ("morning star",                "pattern_morning_star"),
    ("evening star",                "pattern_morning_star"),
    ("star (stelle)",               "pattern_morning_star"),
    # ── Doji generico (dopo le varianti specifiche) ──────────────────
    ("doji",                        "pattern_doji"),
    # ── Hammer family ────────────────────────────────────────────────
    ("hanging man",                 "pattern_hammer"),
    ("inverted hammer",             "pattern_inverted_hammer"),
    ("shooting star",               "pattern_shooting_star"),
    ("hammer",                      "pattern_hammer"),
    # ── Single candles ───────────────────────────────────────────────
    ("spinning top",                "pattern_spinning_top"),
    ("marubozu",                    "pattern_marubozu"),
    ("belt-hold",                   "pattern_belt_hold"),
    ("belt hold",                   "pattern_belt_hold"),
    ("pin bar",                     "pattern_pin_bar"),
    ("power bar",                   "pattern_powerbar"),
    ("power bars",                  "pattern_powerbar"),
    ("inside bar",                  "pattern_inside_bar"),
    # ── Double candles ───────────────────────────────────────────────
    ("harami cross",                "pattern_harami_cross"),
    ("harami",                      "pattern_harami"),
    ("engulfing",                   "pattern_engulfing"),
    ("tweezer tops",                "pattern_tweezer"),
    ("tweezer bottoms",             "pattern_tweezer"),
    ("tweezer",                     "pattern_tweezer"),
    ("dark cloud",                  "pattern_dark_cloud_cover"),
    ("piercing",                    "pattern_piercing_line"),
    ("counterattack",               "pattern_counterattack"),
    ("upside-gap two crows",        "pattern_upside_gap_two_crows"),
    ("upside gap two crows",        "pattern_upside_gap_two_crows"),
    # ── Triple candles ───────────────────────────────────────────────
    ("three black crows",           "pattern_three_candles"),
    ("three advancing white",       "pattern_three_candles"),
    ("three white soldiers",        "pattern_three_candles"),
    ("tre soldati",                 "pattern_three_candles"),
    ("tre corvi",                   "pattern_three_candles"),
    ("tasuki gap",                  "pattern_tasuki_gap"),
    ("rising three methods",        "pattern_rising_three_methods"),
    ("falling three methods",       "pattern_rising_three_methods"),
    ("three mountain top",          "pattern_three_mountain_top"),
    ("three mountain",              "pattern_three_mountain_top"),
    ("three river",                 "pattern_three_mountain_top"),
    # ── Chart patterns (Bulkowski / Murphy) ──────────────────────────
    ("head-and-shoulders bottoms",  "pattern_head_shoulders"),
    ("head-and-shoulders tops",     "pattern_head_shoulders"),
    ("head and shoulders",          "pattern_head_shoulders"),
    ("testa e spalle",              "pattern_head_shoulders"),
    ("double bottoms",              "pattern_double_top"),
    ("double tops",                 "pattern_double_top"),
    ("doppio top",                  "pattern_double_top"),
    ("doppio bottom",               "pattern_double_top"),
    ("double top",                  "pattern_double_top"),
    ("double bottom",               "pattern_double_top"),
    ("triangoli",                   "pattern_triangle"),
    ("triangle",                    "pattern_triangle"),
    ("wedge",                       "pattern_wedge"),
    ("flags",                       "pattern_flag"),
    ("flag",                        "pattern_flag"),
    # ── Ross patterns (TLOC) ─────────────────────────────────────────
    ("formazione 1-2-3 massimo",    "pattern_1_2_3_top"),
    ("massimo 1-2-3",               "pattern_1_2_3_top"),
    ("1-2-3 massimo",               "pattern_1_2_3_top"),
    ("1-2-3 top",                   "pattern_1_2_3_top"),
    ("formazione 1-2-3 minimo",     "pattern_1_2_3_bottom"),
    ("minimo 1-2-3",                "pattern_1_2_3_bottom"),
    ("1-2-3 minimo",                "pattern_1_2_3_bottom"),
    ("1-2-3 bottom",                "pattern_1_2_3_bottom"),
    ("ledge pattern",               "pattern_ledge"),
    ("ledge",                       "pattern_ledge"),
    ("trading range pattern",       "pattern_trading_range"),
    ("trading range",               "pattern_trading_range"),
    ("ross hook",                   "pattern_ross_hook"),
    ("uncino di ross",              "pattern_ross_hook"),
    ("traders trick",               "pattern_traders_trick"),
    ("trader's trick",              "pattern_traders_trick"),
    # ── Williams patterns ────────────────────────────────────────────
    ("smash day",                   "pattern_smash_day"),
    ("oops! pattern",               "pattern_oops"),
    ("oops pattern",                "pattern_oops"),
    ("outside day",                 "pattern_outside_day"),
    ("volatility breakout",         "pattern_volatility_breakout"),
    ("swing points as trend change","pattern_short_term_pivot"),
    ("short-term high/low",         "pattern_short_term_pivot"),
    ("short-term pivot",            "pattern_short_term_pivot"),
    # ── SR indicators ────────────────────────────────────────────────
    ("fibonacci",                   "fib_retracement"),
    ("ritracciamento percentuale",  "fib_retracement"),
    ("retracement percentages",     "fib_retracement"),
    ("pivot points",                "pivot_points"),
    ("pivot settimanale",           "pivot_weekly"),
    ("vwap",                        "vwap"),
    ("donchian channel",            "donchian_upper"),
    ("donchian",                    "donchian_upper"),
    ("supply zone",                 "supply_zone"),
    ("demand zone",                 "demand_zone"),
    ("livelli psicologici",         "psych_levels"),
    ("supporto e resistenza",       "dynamic_support"),
    ("support and resistance",      "dynamic_support"),
    ("supporto diventa resistenza", "dynamic_support"),
    ("swing",                       "dynamic_support"),
    # ── Oscillatori (Murphy, Williams, Nison) ────────────────────────
    ("williams %r",                 "williams_r"),
    ("williams r",                  "williams_r"),
    ("%r",                          "williams_r"),
    ("stochastic",                  "stochastic_k"),
    ("macd",                        "macd_line"),
    ("rsi",                         "rsi"),
    ("mao",                         "mao"),
    # ── Trend indicators ─────────────────────────────────────────────
    ("bollinger",                   "bollinger_upper"),
    ("keltner",                     "keltner_upper"),
    ("ichimoku",                    "ichimoku_kijun"),
    ("supertrend",                  "supertrend"),
    ("linear regression",           "linear_regression"),
    ("regressione lineare",         "linear_regression"),
    ("medie mobili",                "sma_20"),
    ("media mobile",                "sma_20"),
    ("moving average",              "sma_20"),
    # ── Volume ───────────────────────────────────────────────────────
    ("volume spread analysis",      "volume_vsa"),
    ("vsa",                         "volume_vsa"),
    ("volume analysis",             "volume_vsa"),
    ("volume (volume analysis)",    "volume_vsa"),
]


def _find_overlay_id(technique_name: str) -> str | None:
    """
    Cerca nella TECHNIQUE_OVERLAY_MAP la prima keyword che matcha il nome
    della tecnica (word-boundary, case-insensitive). Restituisce l'overlay_id
    o None se la tecnica non ha rappresentazione visiva sul grafico.

    Usa re.search con \b per evitare falsi positivi da substring parziali
    (es. "swing" non deve matchare "swing trading framework" con dynamic_support
    se il contesto è puramente concettuale).
    """
    name_lower = technique_name.lower()
    for keyword, overlay_id in TECHNIQUE_OVERLAY_MAP:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, name_lower):
            return overlay_id
    return None


class SkillSelector:
    """
    Seleziona gli strumenti di analisi più adatti al contesto corrente.

    Produce due output distinti:
    - chosen_tools:         strumenti grafici per il frontend (overlay chart.js)
    - skills_guidance:      istruzioni vincolanti per ogni agente specialista,
                            costruite deterministicamente dai SKILL.md (nome + body
                            di ogni tecnica, nessun limite di quantità)
    - techniques_per_domain: struttura {domain: {libro: [{name, body, overlay_id}]}}
                             per il bridge frontend tecnica ↔ overlay grafico

    Miglioramenti v2:
    - BOOK_DOMAIN_MAP profondo: tutti e 4 i domini coperti correttamente
    - Estrazione integrale: nome + body di ogni tecnica, zero cap
    - Word-boundary regex in _find_overlay_id (no false positive)
    - _verify_coverage: audit di copertura totale con warning espliciti
    - Dead code rimosso: _load_skill_summaries, _build_technique_catalog_text
    - Cache con force_reload per sviluppo iterativo
    """

    # Mappa directory-name → etichetta leggibile (chiave di BOOK_DOMAIN_MAP)
    BOOK_LABELS: dict[str, str] = {
        "encyclopedia_of_chart_patterns":         "Thomas Bulkowski — Encyclopedia of Chart Patterns",
        "encyclopedia-of-chart-patterns":          "Thomas Bulkowski — Encyclopedia of Chart Patterns",
        "japanese_candlestick_charting":           "Steve Nison — Japanese Candlestick Charting",
        "japanese-candlestick-charting":           "Steve Nison — Japanese Candlestick Charting",
        "joe_ross_daytrading":                     "Joe Ross — Day Trading",
        "joe-ross-daytrading":                     "Joe Ross — Day Trading",
        "larry_williams_long_term_secrets":        "Larry Williams — Long-Term Secrets to Short-Term Trading",
        "larry-williams-long-term-secrets":        "Larry Williams — Long-Term Secrets to Short-Term Trading",
        "murphy_analisi_tecnica":                  "John Murphy — Analisi Tecnica dei Mercati Finanziari",
        "murphy-analisi-tecnica":                  "John Murphy — Analisi Tecnica dei Mercati Finanziari",
        "technical_analysis_multiple_timeframes":  "Brian Shannon — Technical Analysis Using Multiple Timeframes",
        "technical-analysis-multiple-timeframes":  "Brian Shannon — Technical Analysis Using Multiple Timeframes",
    }

    def __init__(self):
        self.skills_dir        = Calibrazione.SKILLS_LIBRARY_DIR
        self._technique_catalog = None  # Cache: {book_label: [{name, body}]}

    # ------------------------------------------------------------------
    # LETTURA SKILL.md — Estrazione nome + body di ogni tecnica
    # ------------------------------------------------------------------

    def _load_technique_catalog(self, force_reload: bool = False) -> dict:
        """
        Estrae da ogni SKILL.md il nome (## heading) e il body (testo
        sotto l'heading fino al prossimo ##) per ogni tecnica.

        Differenze rispetto alla v1:
        - Nessun limite di quantità (rimosso il cap a 30)
        - Viene estratto il body completo (troncato a 400 char) oltre al nome
        - force_reload=True invalida la cache (utile in sviluppo)
        - Warning esplicito se il libro non è in BOOK_DOMAIN_MAP

        Returns:
            {book_label: [{"name": str, "body": str}, ...]}
        """
        if self._technique_catalog is not None and not force_reload:
            return self._technique_catalog

        catalog: dict[str, list[dict]] = {}

        for skill_dir_path in Calibrazione.TECHNICAL_SKILLS_DIRS:
            skill_file = os.path.join(skill_dir_path, "SKILL.md")
            if not os.path.exists(skill_file):
                logger.warning(f"[SKILL SELECTOR] SKILL.md non trovato: {skill_file}")
                continue

            dir_name   = os.path.basename(skill_dir_path)
            book_label = self.BOOK_LABELS.get(dir_name, dir_name)

            # Avvisa se il libro non è mappato — tecnica mai assegnata a nessun agente
            if book_label not in BOOK_DOMAIN_MAP:
                logger.warning(
                    f"[SKILL SELECTOR] Libro non in BOOK_DOMAIN_MAP: '{book_label}' "
                    f"(dir: {dir_name}). Aggiungilo per assegnarlo agli agenti."
                )

            techniques: list[dict] = []

            try:
                with open(skill_file, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                frontmatter_done = False
                dash_count       = 0
                current_name: str | None = None
                current_body_lines: list[str] = []

                def _flush_technique():
                    """
                    Salva la tecnica corrente nel catalogo.

                    Campi prodotti:
                    - body: testo completo della tecnica (per frontend/tooltip)
                    - desc: solo la riga **Descrizione:** (per skills_guidance agli agenti,
                            compatta e adatta ai limiti di contesto del modello)
                    """
                    if current_name:
                        body = " ".join(
                            l.strip() for l in current_body_lines if l.strip()
                        ).strip()
                        # Estrai solo la sezione **Descrizione:** per la guidance compatta.
                        # Cerca il valore dopo "**Descrizione:**" fino al prossimo "**" o fine.
                        desc_match = re.search(
                            r'\*\*Descrizione:\*\*\s*(.+?)(?=\*\*[A-Z]|$)',
                            body,
                            re.DOTALL | re.IGNORECASE,
                        )
                        if desc_match:
                            desc = re.sub(r'\s+', ' ', desc_match.group(1)).strip()
                        else:
                            # Fallback: prime 300 char del body se Descrizione non trovata
                            desc = body[:300].strip()
                        techniques.append({"name": current_name, "body": body, "desc": desc})

                for line in lines:
                    stripped = line.strip()

                    # ── Gestione frontmatter YAML ─────────────────────
                    # Contiamo solo i "---" che appaiono come riga isolata.
                    # Usiamo == per evitare di matchare separatori orizzontali
                    # dentro il corpo del testo (es. "--- fine ---").
                    if stripped == "---" and not frontmatter_done:
                        dash_count += 1
                        if dash_count == 2:
                            frontmatter_done = True
                        continue
                    if not frontmatter_done:
                        continue

                    # ── Nuovo heading di tecnica (## TecnicaNome) ─────
                    if line.startswith("## ") and not line.startswith("### "):
                        _flush_technique()  # salva la tecnica precedente
                        candidate = line[3:].strip()
                        # Salta heading generici o di struttura
                        if (
                            candidate
                            and "skill" not in candidate.lower()
                            and len(candidate) < 80
                        ):
                            current_name       = candidate
                            current_body_lines = []
                        else:
                            current_name       = None
                            current_body_lines = []
                        continue

                    # ── Accumula il body della tecnica corrente ───────
                    if current_name is not None:
                        # Interrompe l'accumulo se incontra un heading di qualsiasi livello
                        # (### o superiore) che segna l'inizio di una sottosezione lunga
                        if line.startswith("#"):
                            # Non flushiamo — continuiamo ad accumulare: i ### sono
                            # sottosezioni della stessa tecnica (es. "### Regole di validità")
                            pass
                        current_body_lines.append(line)

                # Salva l'ultima tecnica del file
                _flush_technique()

            except Exception as e:
                logger.error(f"[SKILL SELECTOR] Errore lettura {skill_file}: {e}")

            if techniques:
                catalog[book_label] = techniques
                logger.debug(
                    f"[SKILL SELECTOR] '{book_label}': {len(techniques)} tecniche estratte"
                )
            else:
                logger.warning(
                    f"[SKILL SELECTOR] Nessuna tecnica trovata in {skill_file}. "
                    f"Verifica che i heading ## siano presenti e il frontmatter sia corretto."
                )

        self._technique_catalog = catalog
        return catalog

    # ------------------------------------------------------------------
    # COVERAGE CHECK — Audit di copertura totale
    # ------------------------------------------------------------------

    def _verify_coverage(self, catalog: dict) -> None:
        """
        Verifica che ogni libro e ogni tecnica siano assegnati ad almeno
        un agente. Emette warning espliciti per ogni gap trovato.

        Questo metodo non modifica nulla — è puro audit con logging.
        Da chiamare dopo _load_technique_catalog().

        Verifica inoltre la coerenza semantica tra il nome/desc della tecnica
        e il dominio assegnato (pattern/trend/sr/oscillator).
        """
        all_domains = ("pattern", "trend", "sr", "oscillator")
        uncovered_books:      list[str] = []
        uncovered_techniques: list[tuple[str, str]] = []  # (book, tech_name)
        incoherent_assignments: list[tuple[str, str, str]] = []  # (book, domain, tech_name)

        # Regex keywords per validare coerenza
        domain_keywords = {
            "pattern": r"(pattern|candela|candle|engulfing|harami|doji|hammer|star|formation|formazione|breakout|chart|head.*shoulder|testa.*spalle|double|triangle|wedge|flag|1-2-3|ross|inside|pin|dark cloud|piercing|shooting|morning|evening|tweezer|counterattack|gap|oops|smash|outside|volatility)",
            "trend": r"(moving.*average|media.*mobile|sma|ema|trend|momentum|bollinger|band|channel|keltner|ichimoku|supertrend|atr|slope|direction|uptrend|downtrend|rialzo|ribasso|equilibrium|convergence|divergence|incrocio|multiframe|mtf|alignment|tenkan|kijun|senkou)",
            "sr": r"(support|resistance|supporto|resistenza|livello|pivot|fibonacci|fib|psych|psychological|zone|area|supply|demand|accumulation|distribution|vwap|donchian|swing|high.*low|max.*min|confluence|confluenza|target|entry|entrata)",
            "oscillator": r"(rsi|macd|stochastic|williams|%r|momentum|oscill|divergence|convergence|ipercomprato|ipervenduto|overbought|oversold|signal|segnale|histogram|confirmation|conferma|volume|mao|crossover)",
        }

        for book_label, techniques in catalog.items():
            domains_for_book = BOOK_DOMAIN_MAP.get(book_label, [])

            # Libro non mappato = tutte le sue tecniche sono orfane
            if not domains_for_book:
                uncovered_books.append(book_label)
                for tech in techniques:
                    uncovered_techniques.append((book_label, tech["name"]))
                continue

            # Verifica che il libro sia mappato ad almeno un dominio valido
            for domain in domains_for_book:
                if domain not in all_domains:
                    logger.warning(
                        f"[SKILL SELECTOR] Dominio sconosciuto '{domain}' "
                        f"in BOOK_DOMAIN_MAP per '{book_label}'"
                    )

                # Verifica coerenza semantica per ogni tecnica del dominio
                for tech in techniques:
                    combined_text = f"{tech['name']} {tech.get('desc', '')}".lower()
                    keywords = domain_keywords.get(domain, [])
                    if keywords and not re.search(keywords, combined_text):
                        incoherent_assignments.append((book_label, domain, tech["name"]))

        if uncovered_books:
            logger.warning(
                f"[SKILL SELECTOR] LIBRI SENZA AGENTE: {uncovered_books}. "
                f"Aggiungerli a BOOK_DOMAIN_MAP per includerne le tecniche."
            )
        if uncovered_techniques:
            logger.warning(
                f"[SKILL SELECTOR] {len(uncovered_techniques)} tecniche non assegnate "
                f"ad alcun agente. Dettaglio: "
                + "; ".join(f"[{b}] {n}" for b, n in uncovered_techniques[:10])
                + (" ..." if len(uncovered_techniques) > 10 else "")
            )
        if incoherent_assignments:
            logger.warning(
                f"[SKILL SELECTOR] {len(incoherent_assignments)} ASSEGNAMENTI POTENZIALMENTE INCOERENTI "
                f"(nome/desc non matcha dominio). Dettaglio: "
                + "; ".join(f"[{d}] {n}" for b, d, n in incoherent_assignments[:5])
                + (" ..." if len(incoherent_assignments) > 5 else "")
            )

        if not uncovered_books and not uncovered_techniques and not incoherent_assignments:
            logger.debug("[SKILL SELECTOR] Coverage check OK — tutte le tecniche assegnate e coerenti.")

    # ------------------------------------------------------------------
    # SKILLS GUIDANCE — Istruzioni deterministiche per ogni specialista
    # ------------------------------------------------------------------

    def _build_skills_guidance(
        self,
        catalog: dict,
        asset_type: str | None = None,
    ) -> dict[str, str]:
        """
        Costruisce le istruzioni vincolanti (FOCUS SKILLS) per ogni specialista.

        DETERMINISTICO: include nome + body di TUTTE le tecniche del catalogo
        per ogni libro rilevante per il dominio. Non dipende dall'LLM.

        Args:
            catalog:    output di _load_technique_catalog()
            asset_type: "commodity" | "crypto" | "forex" | "equity" | None
                        Usato solo per aggiungere un'enfasi contestuale
                        in cima alla guidance — non esclude mai tecniche.

        Returns:
            dict {domain: str} con domini: pattern, trend, sr, oscillator
        """
        def _asset_hint(domain: str) -> str:
            """Aggiunge una riga di enfasi contestuale per asset_type."""
            if not asset_type:
                return ""
            hints = {
                "commodity": {
                    "pattern": "ENFASI: mercato commodity — privilegia pattern di inversione su livelli psicologici e zone S/D.",
                    "trend":   "ENFASI: commodity — SMA lente (50/200), SuperTrend, Bollinger per volatilità stagionale.",
                    "sr":      "ENFASI: commodity — livelli psicologici tondi, Fibonacci su swing di lungo periodo, zone S/D.",
                    "oscillator": "ENFASI: commodity — RSI per divergenze di lungo, MACD per conferma trend primario.",
                },
                "crypto": {
                    "pattern": "ENFASI: crypto — pattern di momentum (Ross Hook, 1-2-3, Power Bars) su timeframe breve.",
                    "trend":   "ENFASI: crypto — EMA veloci (9/20/50), SuperTrend, Bollinger squeeze per volatilità estrema.",
                    "sr":      "ENFASI: crypto — livelli psicologici tondi (10.000, 50.000), VWAP intraday, supply/demand zones.",
                    "oscillator": "ENFASI: crypto — Stochastic e %R per mercato ipercomprato/ipervenduto frequente, MACD per divergenze.",
                },
                "forex": {
                    "pattern": "ENFASI: forex — pattern Nison e inside bar su livelli Pivot settimanali.",
                    "trend":   "ENFASI: forex — EMA + Ichimoku (Kijun/Tenkan), analisi MTF Shannon su H1/H4/D1.",
                    "sr":      "ENFASI: forex — Pivot Points settimanali, livelli psicologici (pips tondi), VWAP.",
                    "oscillator": "ENFASI: forex — MACD per momentum direzionale, RSI per gestione del rischio.",
                },
                "equity": {
                    "pattern": "ENFASI: equity — pattern di inversione Murphy (H&S, Double Top) con conferma volume.",
                    "trend":   "ENFASI: equity — SMA 50/200, analisi top-down Shannon su weekly/daily.",
                    "sr":      "ENFASI: equity — Fibonacci sui massimi storici, pivot annuali, livelli earnings gap.",
                    "oscillator": "ENFASI: equity — RSI mensile per divergenze di lungo, MACD weekly per trend.",
                },
            }
            return hints.get(asset_type, {}).get(domain, "")

        def _build_sections(domain: str) -> str:
            """
            Costruisce il blocco testuale con tutte le tecniche di tutti
            i libri assegnati al dominio.

            Usa il campo `desc` (solo la riga Descrizione) per mantenere
            la guidance compatta e compatibile con i limiti di contesto del
            modello. Il body completo è disponibile in techniques_per_domain
            per i tooltip del frontend.

            Formato:
              [Nome Libro]:
                1. NomeTecnica — descrizione operativa
                2. ...
            """
            sections: list[str] = []
            for book_label, book_techs in catalog.items():
                if domain not in BOOK_DOMAIN_MAP.get(book_label, []):
                    continue
                lines: list[str] = []
                for i, tech in enumerate(book_techs, start=1):
                    name = tech["name"]
                    desc = tech.get("desc", tech.get("body", "")[:300]).strip()
                    if desc:
                        lines.append(f"  {i}. {name} — {desc}")
                    else:
                        lines.append(f"  {i}. {name}")
                if lines:
                    sections.append(f"[{book_label}]:\n" + "\n".join(lines))
            return "\n\n".join(sections)

        guidance: dict[str, str] = {}

        # ── Pattern Analyst ────────────────────────────────────────────────────
        # Libri assegnati: Nison, Bulkowski, Ross, Murphy
        sections = _build_sections("pattern")
        hint     = _asset_hint("pattern")
        guidance["pattern"] = (
            "FOCUS SKILLS — Tecniche OBBLIGATORIE dai libri assegnati al tuo dominio.\n"
            "Devi analizzare TUTTE le tecniche elencate. Per quelle non rilevabili "
            "nei dati correnti, documentalo esplicitamente ('Non rilevato').\n"
            + (f"\n{hint}\n" if hint else "") +
            f"\n{sections}\n\n"
            "REGOLA: per ogni pattern trovato, riporta: nome, validità (criteri Nison/Bulkowski), "
            "target misurato (metodo Bulkowski dove disponibile), "
            "e il pattern Joe Ross / Larry Williams corrispondente se applicabile."
        ) if sections else ""

        # ── Trend Analyst ──────────────────────────────────────────────────────
        # Libri assegnati: Williams, Murphy, Shannon
        sections = _build_sections("trend")
        hint     = _asset_hint("trend")
        guidance["trend"] = (
            "FOCUS SKILLS — Tecniche OBBLIGATORIE dai libri assegnati al tuo dominio.\n"
            "Devi analizzare TUTTE le tecniche elencate. Per quelle non applicabili "
            "ai dati correnti, documentalo esplicitamente ('Non applicabile').\n"
            + (f"\n{hint}\n" if hint else "") +
            f"\n{sections}\n\n"
            "REGOLA: per ogni indicatore di trend, riporta: direzione, forza, "
            "allineamento MTF (Shannon: weekly → daily → intraday), "
            "e i criteri di incrocio/divergenza operativa."
        ) if sections else ""

        # ── SR Analyst ─────────────────────────────────────────────────────────
        # Libri assegnati: Bulkowski, Ross, Williams, Murphy, Shannon
        sections = _build_sections("sr")
        hint     = _asset_hint("sr")
        guidance["sr"] = (
            "FOCUS SKILLS — Tecniche OBBLIGATORIE dai libri assegnati al tuo dominio.\n"
            "Devi costruire la MAPPA COMPLETA dei livelli S/R usando TUTTE le tecniche "
            "elencate. Per ogni livello riporta la fonte (libro) e il punteggio di "
            "confluenza (quante tecniche diverse convergono sullo stesso livello).\n"
            + (f"\n{hint}\n" if hint else "") +
            f"\n{sections}\n\n"
            "REGOLA: un livello con confluenza ≥3 tecniche diverse è un livello CRITICO. "
            "Usa le statistiche Bulkowski per stimare la probabilità di tenuta. "
            "Usa i livelli TLOC (Ross) per identificare le zone di congestione operative."
        ) if sections else ""

        # ── Oscillator Analyst ─────────────────────────────────────────────────
        # Libri assegnati: Nison (cap.12-14), Williams (%R, MACD, Oops), Murphy (cap.11-14)
        sections = _build_sections("oscillator")
        hint     = _asset_hint("oscillator")
        guidance["oscillator"] = (
            "FOCUS SKILLS — Tecniche OBBLIGATORIE dai libri assegnati al tuo dominio.\n"
            "Il tuo ruolo è CONFERMARE o INVALIDARE i segnali degli altri specialisti "
            "attraverso gli oscillatori. Devi analizzare TUTTI gli oscillatori elencati.\n"
            + (f"\n{hint}\n" if hint else "") +
            f"\n{sections}\n\n"
            "REGOLA NISON: ogni segnale candlestick deve essere confermato da almeno "
            "un oscillatore. Un pattern non confermato da oscillatori ha affidabilità RIDOTTA.\n"
            "REGOLA DIVERGENZE: le divergenze rialziste/ribassiste tra prezzo e oscillatore "
            "sono il segnale più affidabile — hanno precedenza su qualsiasi altro segnale.\n"
            "REGOLA WILLIAMS %R: zone -80/-100 = ipervenduto operativo, 0/-20 = ipercomprato.\n"
            "REGOLA MAO (Nison Cap.14): MAO positivo = trend rialzista confermato, "
            "negativo = ribassista. Crossover zero = cambio di momentum primario."
        ) if sections else ""

        return guidance

    # ------------------------------------------------------------------
    # COSTRUZIONE CATALOGO GRAFICO — solo per il prompt LLM
    # ------------------------------------------------------------------

    def _build_catalog_text(self) -> str:
        """Costruisce la rappresentazione testuale del catalogo strumenti grafici."""
        lines = ["STRUMENTI DISPONIBILI NEL GRAFICO (usa SOLO questi ID):"]
        for group, tools in AVAILABLE_TOOLS.items():
            lines.append(f"\n[{group.upper()}]")
            for t in tools:
                lines.append(f"  - ID: {t['id']} | Nome: {t['name']} | Uso: {t['desc']}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # SELEZIONE PRINCIPALE
    # ------------------------------------------------------------------

    def select_tools(self, nome_asset: str, macro_sentiment: str, data_dict: dict) -> dict:
        """
        Analizza il contesto e produce due selezioni complementari:

        1. chosen_tools (pattern/trend/sr/oscillator): strumenti grafici per il frontend
        2. skills_guidance: istruzioni vincolanti con nome + body di TUTTE le tecniche
           dei libri rilevanti, per ogni agente specialista

        Args:
            nome_asset:      Il ticker (es. "GC=F", "AAPL", "BTC-USD")
            macro_sentiment: Testo del sentiment macro prodotto dall'AgnoMacroExpert
            data_dict:       Dizionario con i dati OHLCV multi-timeframe

        Returns:
            Dict con: pattern · trend · sr · oscillator · summary ·
                      raw_skills_used · skills_guidance · techniques_per_domain · success
        """
        logger.info(f"[SKILL SELECTOR] Selezione strumenti per {nome_asset}...")

        # ── Rileva asset type per enfasi contestuale ───────────────────────────
        ticker_upper = nome_asset.upper()
        if any(x in ticker_upper for x in ["GC=F", "CL=F", "SI=F", "HG=F", "NG=F", "ZW=F", "ZC=F", "ZS=F"]):
            asset_type = "commodity"
        elif any(x in ticker_upper for x in ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOGE", "-USD", "-USDT"]):
            asset_type = "crypto"
        elif any(x in ticker_upper for x in ["=X", "EUR", "GBP", "JPY", "CHF", "AUD", "CAD", "NZD"]):
            asset_type = "forex"
        else:
            asset_type = "equity"
        logger.debug(f"[SKILL SELECTOR] Asset type rilevato: {asset_type}")

        # ── Carica catalogo e verifica copertura ──────────────────────────────
        catalog = self._load_technique_catalog()
        self._verify_coverage(catalog)

        catalog_text = self._build_catalog_text()

        try:
            last_1d = data_dict["1d"].tail(5).to_string() if "1d" in data_dict else "N/D"
        except Exception:
            last_1d = "N/D"

        prompt = f"""Sei un Analista Tecnico Senior. Analizza il contesto e produci la selezione degli strumenti grafici.

ASSET: {nome_asset}
TIPO ASSET: {asset_type}

SENTIMENT MACRO:
{macro_sentiment[:1200]}

DATI RECENTI (ultime 5 candele 1D):
{last_1d}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRUMENTI GRAFICI DA SELEZIONARE (per il frontend)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{catalog_text}

Regole di selezione:
- Usa SOLO gli ID esatti del catalogo (nessun ID inventato)
- Il campo "reason" deve essere breve: max 10 parole
- Il campo "color" deve essere un colore HEX chiaro e ben visibile su sfondo SCURO. Non usare mai nero (#000, #000000, "black") né colori scuri. Usa colori come "#f9ca24" (giallo), "#74b9ff" (blu), "#ff9f43" (arancio), "#00d4aa" (verde acqua), "#ff6b81" (rosa), "#a29bfe" (viola).

OBIETTIVO: seleziona TUTTI gli strumenti necessari per un'analisi completa che copra ogni punto:
- PATTERN: tutti i pattern candlestick e chartistici rilevabili nel contesto corrente
- TREND: tutti gli indicatori di trend e medie mobili utili per identificare direzione e forza
- SR: tutti i livelli di supporto/resistenza, Fibonacci, pivot e zone S/D significativi
- OSCILLATOR: TUTTI gli oscillatori del catalogo che forniscono conferma o divergenza

Non c'è un limite massimo al numero di strumenti — seleziona tutto ciò che contribuisce all'analisi.

Adatta la selezione al contesto:
- asset type "{asset_type}": scegli gli strumenti più rilevanti per questo tipo di mercato
- BEARISH: includi resistenze, pattern ribassisti (dark_cloud_cover, shooting_star, 1_2_3_top, outside_day, smash_day), Williams %R, MAO
- BULLISH: includi supporti, pattern rialzisti (piercing_line, morning_star, 1_2_3_bottom, oops), RSI, Stochastic
- PATTERN JOE ROSS: includi 1_2_3_top/bottom, ross_hook, ledge in trend chiari
- PATTERN LARRY WILLIAMS: includi oops e volatility_breakout in mercati volatili con gap

Rispondi SOLO con JSON valido, nessun testo fuori dal JSON:
{{
  "pattern":   [{{"id": "...", "color": "...", "reason": "..."}}],
  "trend":     [{{"id": "...", "color": "...", "reason": "..."}}],
  "sr":        [{{"id": "...", "color": "...", "reason": "..."}}],
  "oscillator":[{{"id": "...", "color": "...", "reason": "..."}}],
  "summary":   "Sintesi della selezione in 2 righe"
}}"""

        raw = ""
        try:
            from agents.model_factory import get_model
            from agno.agent import Agent
            llm = get_model(
                Calibrazione.MODEL_SKILL_SELECTOR,
                temperature=Calibrazione.TEMPERATURE_SKILL_SELECTOR,
                agent_name="skill_selector"
            )
            selector_agent = Agent(
                model=llm,
                description="Sei un analista tecnico che seleziona strumenti di analisi in base al contesto.",
                instructions=["Rispondi SOLO con JSON valido, senza markdown, senza blocchi ```json."],
                markdown=False,
            )
            response = selector_agent.run(prompt)
            raw = response.content if hasattr(response, "content") else str(response)

            # Estrai il blocco JSON dalla risposta
            json_match = re.search(r'\{[\s\S]*\}', raw)
            if json_match:
                raw = json_match.group(0)

            # Tenta il parse diretto
            try:
                chosen = json.loads(raw)
            except json.JSONDecodeError:
                # Fallback: json_repair
                try:
                    from json_repair import repair_json
                    raw    = repair_json(raw)
                    chosen = json.loads(raw)
                except Exception as repair_err:
                    logger.error(f"[SKILL SELECTOR] json_repair fallito: {repair_err}")
                    chosen = {}

            return self._validate_and_fallback(chosen, catalog, asset_type)

        except Exception as e:
            logger.error(f"[SKILL SELECTOR] Errore selezione strumenti: {e}. Raw: {raw[:300]}")
            return self._validate_and_fallback({}, catalog, asset_type)

    # ------------------------------------------------------------------
    # VALIDAZIONE E FALLBACK
    # ------------------------------------------------------------------

    def _validate_and_fallback(
        self,
        chosen: dict,
        catalog: dict,
        asset_type: str | None = None,
    ) -> dict:
        """
        Valida il JSON restituito dall'AI:
        - Normalizza alias ID comuni
        - Rimuove ID non presenti nel catalogo grafico
        - Forza colori leggibili su sfondo scuro
        - Costruisce skills_guidance con nome + body (deterministico)
        - Costruisce techniques_per_domain con overlay_id (deterministico)
        - Esegue _verify_coverage per audit finale

        Args:
            chosen:     JSON restituito dall'LLM (può essere parziale o vuoto)
            catalog:    output di _load_technique_catalog()
            asset_type: "commodity" | "crypto" | "forex" | "equity" | None
        """
        all_valid_ids = {t["id"]: t for group in AVAILABLE_TOOLS.values() for t in group}
        result: dict  = {"success": True}

        # Normalizzazione alias generati dall'AI
        ID_ALIASES: dict[str, str] = {
            "pattern_bullish_engulfing":  "pattern_engulfing",
            "pattern_bearish_engulfing":  "pattern_engulfing",
            "pattern_morning_star_doji":  "pattern_morning_doji_star",
            "pattern_evening_star_doji":  "pattern_evening_doji_star",
            "pattern_hammer_inverted":    "pattern_inverted_hammer",
            "pattern_star_shooting":      "pattern_shooting_star",
            "pattern_bullish_harami":     "pattern_harami",
            "pattern_bearish_harami":     "pattern_harami",
        }

        # ── Parte A: strumenti grafici (frontend) ──────────────────────────────
        for group in ("pattern", "trend", "sr", "oscillator"):
            valid_items: list[dict] = []
            for item in chosen.get(group, []):
                if not isinstance(item, dict):
                    continue

                tool_id = item.get("id")

                # 1. Normalizzazione alias
                if tool_id in ID_ALIASES:
                    logger.debug(f"[SKILL SELECTOR] Alias normalizzato: {tool_id!r} -> {ID_ALIASES[tool_id]!r}")
                    tool_id    = ID_ALIASES[tool_id]
                    item["id"] = tool_id

                # 2. Controllo whitelist
                if tool_id not in all_valid_ids:
                    logger.warning(f"[SKILL SELECTOR] ID non valido rimosso: {tool_id!r}")
                    continue

                static_info = all_valid_ids[tool_id]

                # 3. Colore: fallback se mancante, nero o stringa invalida
                color_val = str(item.get("color", "")).lower().strip()
                is_invalid = color_val in {
                    "#000", "#000000", "black", "null", "none", "",
                    "rgb(0,0,0)", "rgba(0,0,0,1)", "rgba(0,0,0,0)",
                }
                item["color"] = (
                    DEFAULT_COLORS.get(tool_id, "#ffffff")
                    if (is_invalid or not item.get("color"))
                    else item["color"]
                )

                # 4. Completa i campi statici se mancanti
                item.setdefault("desc", static_info.get("desc", ""))
                item.setdefault("name", static_info.get("name", ""))
                valid_items.append(item)

            result[group] = valid_items

        # ── Parte B: metadata ─────────────────────────────────────────────────
        result["summary"]         = chosen.get("summary", "Selezione per questo asset.")
        result["raw_skills_used"] = list(BOOK_DOMAIN_MAP.keys())

        # ── Parte C: skills_guidance deterministica ───────────────────────────
        # Costruita con nome + body di ogni tecnica, tutti i libri del dominio.
        result["skills_guidance"] = self._build_skills_guidance(catalog, asset_type)

        # ── Parte D: techniques_per_domain ────────────────────────────────────
        # Struttura per il bridge frontend tecnica ↔ overlay grafico.
        # Ogni tecnica include: name, body (per tooltip), overlay_id (per chart.js).
        # Copre tutti e 4 i domini: pattern, trend, sr, oscillator.
        techniques_per_domain: dict = {}
        for domain in ("pattern", "trend", "sr", "oscillator"):
            books_for_domain: dict = {}
            for book_label, book_techs in catalog.items():
                if domain in BOOK_DOMAIN_MAP.get(book_label, []):
                    books_for_domain[book_label] = [
                        {
                            "name":       t["name"],
                            "body":       t.get("body", ""),
                            "overlay_id": _find_overlay_id(t["name"]),
                        }
                        for t in book_techs
                    ]
            techniques_per_domain[domain] = books_for_domain

        result["techniques_per_domain"] = techniques_per_domain
        return result
