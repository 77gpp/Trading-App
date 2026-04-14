"""
agents/skill_selector.py — Agente Selezionatore di Strumenti Tecnici.

Questo agente ha il compito di:
1. Leggere la tabella degli strumenti grafici disponibili (hardcoded, sempre aggiornata)
2. Leggere un sommario delle skill presenti nella skills_library
3. Basandosi sul contesto macro (asset analizzato, sentiment, tipo di mercato),
   scegliere quali strumenti tecnici usare e perché
4. Restituire una struttura JSON con i tool scelti per ciascun gruppo (Pattern, Trend, SR)
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
        {"id": "pattern_doji",              "name": "Doji (Indecisione)",            "desc": "Candela con apertura=chiusura, segnala indecisione e possibile inversione"},
        {"id": "pattern_gravestone_doji",   "name": "Gravestone Doji",               "desc": "Doji con ombra superiore lunga e open/close vicini al minimo, segnale ribassista"},
        {"id": "pattern_dragonfly_doji",    "name": "Dragonfly Doji",                "desc": "Doji con ombra inferiore lunga e open/close vicini al massimo, segnale rialzista"},
        {"id": "pattern_long_legged_doji",  "name": "Long-Legged Doji",              "desc": "Doji con entrambe le ombre lunghe, massima indecisione, spesso segnala inversione"},
        {"id": "pattern_spinning_top",      "name": "Spinning Top",                  "desc": "Corpo piccolo con ombre simmetriche, indecisione, precede spesso inversioni"},
        {"id": "pattern_hammer",            "name": "Hammer / Hanging Man",          "desc": "Corpo piccolo con ombra lunga inferiore, potente segnale di inversione"},
        {"id": "pattern_inverted_hammer",   "name": "Inverted Hammer / Shooting Star","desc": "Corpo piccolo con ombra superiore lunga, segnale di inversione dipendente dal contesto"},
        {"id": "pattern_shooting_star",     "name": "Shooting Star",                 "desc": "Ombra superiore ≥2× corpo, apre in uptrend, segnale ribassista Nison"},
        {"id": "pattern_marubozu",          "name": "Marubozu (Impulso Puro)",       "desc": "Candela senza ombre, indica forza/debolezza estrema e pressione istituzionale"},
        {"id": "pattern_belt_hold",         "name": "Belt-Hold Lines",               "desc": "Candela senza ombra sul lato del trend precedente, forte segnale di inversione"},
        {"id": "pattern_pin_bar",           "name": "Pin Bar (Rejection)",           "desc": "Ombra molto lunga che mostra rifiuto del prezzo, usata in Price Action pura"},
        # --- Candele Doppie (Nison) ---
        {"id": "pattern_engulfing",         "name": "Bullish/Bearish Engulfing",     "desc": "Inversione a 2 candele, corpo della seconda ingloba la prima, molto affidabile"},
        {"id": "pattern_harami",            "name": "Harami (Inside Bar Candle)",    "desc": "Candela 'figlia' contenuta nella 'madre', pausa del trend e potenziale inversione"},
        {"id": "pattern_harami_cross",      "name": "Harami Cross",                  "desc": "Harami con seconda candela doji, segnale di inversione più forte dell'harami classico"},
        {"id": "pattern_tweezer",           "name": "Tweezer Top/Bottom",            "desc": "Due candele con max/min identici, forte resistenza o supporto psicologico"},
        {"id": "pattern_dark_cloud_cover",  "name": "Dark Cloud Cover",              "desc": "Candela rialzista + ribassista che chiude oltre metà della prima, segnale di distribuzione"},
        {"id": "pattern_piercing_line",     "name": "Piercing Pattern",              "desc": "Candela ribassista + rialzista che chiude oltre metà della prima, segnale di accumulazione"},
        {"id": "pattern_counterattack",     "name": "Counterattack Lines",           "desc": "Due candele opposte che chiudono allo stesso livello, inversione a livello critico"},
        {"id": "pattern_upside_gap_two_crows","name": "Upside-Gap Two Crows",        "desc": "3 candele: rialzista + gap up + 2 corvi ribassisti, segnale di esaurimento del rialzo"},
        # --- Candele Triple (Nison) ---
        {"id": "pattern_morning_star",      "name": "Morning/Evening Star",          "desc": "Pattern a 3 candele di inversione, tra i più affidabili della letteratura giapponese"},
        {"id": "pattern_morning_doji_star", "name": "Morning Doji Star",             "desc": "Come Morning Star ma la candela centrale è un doji, segnale più forte"},
        {"id": "pattern_evening_doji_star", "name": "Evening Doji Star",             "desc": "Come Evening Star ma la candela centrale è un doji, segnale più forte"},
        {"id": "pattern_three_candles",     "name": "Tre Soldati/Tre Corvi",         "desc": "Tre candele consecutive nella stessa direzione, segnale forte di continuazione"},
        {"id": "pattern_tasuki_gap",        "name": "Tasuki Gap",                    "desc": "Gap tra 2 candele + terza che riempie parzialmente il gap, continuazione del trend"},
        {"id": "pattern_rising_three_methods","name": "Rising/Falling Three Methods","desc": "Candela lunga + 3 piccole interne + candela lunga, classico pattern di continuazione"},
        {"id": "pattern_three_mountain_top","name": "Three Mountain Top",            "desc": "Triplo massimo giapponese: tre picchi allo stesso livello, forte resistenza confermata"},
        # --- Formazioni Chartistiche ---
        {"id": "pattern_inside_bar",        "name": "Inside Bar (Compressione)",     "desc": "La candela corrente è contenuta in quella precedente, breakout imminente"},
        {"id": "pattern_powerbar",          "name": "Power Bars (Joe Ross)",         "desc": "Barre di impulso con range eccezionale, indicano partecipazione istituzionale"},
        {"id": "pattern_triangle",          "name": "Triangoli (Asc/Desc/Sim)",      "desc": "Pattern di consolidamento con target misurato pari alla base del triangolo"},
        {"id": "pattern_wedge",             "name": "Wedge Rising/Falling",          "desc": "Cuneo di inversione, molto frequente in mercati ciclici come Oro e Indici"},
        {"id": "pattern_flag",              "name": "Flag / Pennant",                "desc": "Consolidamento rettangolare post-impulso, target = misura del palo della bandiera"},
        {"id": "pattern_double_top",        "name": "Double Top/Bottom (M/W)",       "desc": "Pattern di inversione classico di John Murphy, confermato dal breakout del neckline"},
        {"id": "pattern_head_shoulders",    "name": "Head and Shoulders",            "desc": "Pattern di inversione più famoso dell'analisi tecnica, alta probabilità con volume calante"},
        # --- Pattern Joe Ross (TLOC - La Legge dei Grafici) ---
        {"id": "pattern_1_2_3_top",         "name": "1-2-3 Top (Ross)",             "desc": "Punto 1=max, punto 2=ritracciamento, punto 3=rimbalzo < punto 1. Base di TLOC"},
        {"id": "pattern_1_2_3_bottom",      "name": "1-2-3 Bottom (Ross)",          "desc": "Punto 1=min, punto 2=rimbalzo, punto 3=ritracciamento > punto 1. Base di TLOC"},
        {"id": "pattern_ledge",             "name": "Ledge (Ross)",                 "desc": "Congestione ristretta di 4+ barre con range compresso, breakout imminente"},
        {"id": "pattern_trading_range",     "name": "Trading Range (Ross)",         "desc": "Congestione ampia con oscillazione laterale, entrata al breakout dei bordi"},
        {"id": "pattern_ross_hook",         "name": "Ross Hook",                    "desc": "Prima barra che viola il punto 3 del 1-2-3, il segnale di entrata principale di Ross"},
        {"id": "pattern_traders_trick",     "name": "Traders Trick Entry (TTE)",    "desc": "Entrata anticipata prima del Ross Hook, richiede conferma di direzione"},
        # --- Pattern Larry Williams ---
        {"id": "pattern_oops",              "name": "Oops Pattern (Williams)",      "desc": "Gap di apertura oltre il range di ieri + rientro nel range → inversione intraday"},
        {"id": "pattern_smash_day",         "name": "Smash Day Reversal",           "desc": "Barra con range eccezionale che chiude agli estremi opposti, esaurimento del movimento"},
        {"id": "pattern_outside_day",       "name": "Outside Day",                  "desc": "Barra che ingloba completamente la precedente (high>prev high AND low<prev low)"},
        {"id": "pattern_volatility_breakout","name": "Volatility Breakout (Williams)","desc": "Breakout basato su ATR × fattore, segnale di momentum istituzionale"},
        {"id": "pattern_short_term_pivot",  "name": "Short-Term Pivot (Williams)",  "desc": "Pivot a 5 barre (2 barre più basse/alte a destra e sinistra), swing point Williams"},
        # --- Volume Analysis ---
        {"id": "volume_vsa",                "name": "VSA Volume Analysis",          "desc": "Colorazione barre volume per deviazione dalla media: rosso=estremo, arancio=alto, blu=sopra media"},
    ],
    "trend": [
        # --- Medie Mobili Semplici ---
        {"id": "sma_10",      "name": "SMA 10",            "desc": "Media di brevissimo termine per scalper e day trader"},
        {"id": "sma_20",      "name": "SMA 20",            "desc": "Base delle Bollinger Bands, supporto/resistenza dinamica in trend forti"},
        {"id": "sma_50",      "name": "SMA 50",            "desc": "La più seguita dagli istituzionali per identificare il trend primario"},
        {"id": "sma_100",     "name": "SMA 100",           "desc": "Filtro di medio termine per eliminare il rumore di breve"},
        {"id": "sma_200",     "name": "SMA 200",           "desc": "La barriera definitiva: sopra = bull market, sotto = bear market"},
        # --- Medie Esponenziali ---
        {"id": "ema_9",       "name": "EMA 9",             "desc": "Usata dai trader di breve per segnali di entrata veloci"},
        {"id": "ema_20",      "name": "EMA 20",            "desc": "Reattiva ai movimenti, ottima in mercati veloci come Crypto e Forex"},
        {"id": "ema_50",      "name": "EMA 50",            "desc": "Media del trader swing per eccellenza, usata con EMA 200"},
        {"id": "ema_100",     "name": "EMA 100",           "desc": "Zona di equilibrio tra breve e lungo termine"},
        {"id": "ema_200",     "name": "EMA 200",           "desc": "Versione dinamica e reattiva della barriera di lungo termine"},
        # --- Canali e Bande ---
        {"id": "bollinger_upper", "name": "Bollinger Band Superiore", "desc": "Zona di ipercomprato dinamica, 2 deviazioni standard sopra SMA 20"},
        {"id": "bollinger_lower", "name": "Bollinger Band Inferiore", "desc": "Zona di ipervenduto dinamica, 2 deviazioni standard sotto SMA 20"},
        {"id": "bollinger_mid",   "name": "Bollinger Band Media",     "desc": "SMA 20, linea di regressione verso la media (mean reversion)"},
        {"id": "keltner_upper",   "name": "Keltner Channel Superiore","desc": "Canale basato su ATR, identificare squeeze di volatilità con Bollinger"},
        {"id": "keltner_lower",   "name": "Keltner Channel Inferiore","desc": "Supporto dinamico ATR-based, ottimo per mercati con trend forti"},
        # --- Indicatori di Trend ---
        {"id": "supertrend",  "name": "SuperTrend (ATR-based)",  "desc": "Segnali automatici Compra/Vendi con stop loss integrato basato su ATR"},
        {"id": "ichimoku_cloud_upper", "name": "Ichimoku Senkou A", "desc": "Bordo superiore della nuvola Ichimoku, resistenza/supporto futura"},
        {"id": "ichimoku_cloud_lower", "name": "Ichimoku Senkou B", "desc": "Bordo inferiore della nuvola Ichimoku, livello di equilibrio di lungo termine"},
        {"id": "ichimoku_kijun",       "name": "Ichimoku Kijun Sen","desc": "Linea di base Ichimoku (26 periodi), segnale con incrocio Tenkan"},
        {"id": "atr_upper",          "name": "ATR Band Superiore",       "desc": "Banda superiore basata su ATR, utile per trailing stop e target dinamici"},
        {"id": "atr_lower",          "name": "ATR Band Inferiore",       "desc": "Banda inferiore basata su ATR, utile per trailing stop e target dinamici"},
        {"id": "ichimoku_tenkan",    "name": "Ichimoku Tenkan Sen",      "desc": "Linea di conversione Ichimoku (9 periodi), incrocio con Kijun = segnale di entrata"},
    ],
    "sr": [
        # --- Livelli Matematici ---
        {"id": "pivot_points",        "name": "Pivot Points Giornalieri",    "desc": "PP, R1, R2, S1, S2 calcolati su OHLC del periodo precedente"},
        {"id": "pivot_weekly",        "name": "Pivot Points Settimanali",    "desc": "Livelli pivot calcolati su base settimanale, più duraturi e significativi"},
        {"id": "fib_retracement",     "name": "Fibonacci Retracement",       "desc": "Livelli 23.6%, 38.2%, 50%, 61.8%, 78.6% per ingressi in correzione"},
        {"id": "fib_extension",       "name": "Fibonacci Extension",         "desc": "Target di prezzo post-breakout: 127.2%, 161.8%, 200%, 261.8%"},
        # --- Livelli Psicologici ---
        {"id": "psych_levels",        "name": "Livelli Psicologici",         "desc": "Numeri tondi (es. 3000, 2500) con alta concentrazione di ordini istituzionali"},
        {"id": "psych_levels_fine",   "name": "Livelli Semi-Psicologici",    "desc": "Numeri a semidecina (500, 250) ugualmente seguiti dallo smart money"},
        # --- Supporti e Resistenze Dinamici ---
        {"id": "dynamic_support",     "name": "Supporto Dinamico (Swing)",   "desc": "Linea di supporto tracciata sui minimi di swing significativi"},
        {"id": "dynamic_resistance",  "name": "Resistenza Dinamica (Swing)", "desc": "Linea di resistenza tracciata sui massimi di swing significativi"},
        {"id": "supply_zone",         "name": "Supply Zone (Distribuzione)", "desc": "Area di prezzo dove storicamente i venditori istituzionali sono entrati"},
        {"id": "demand_zone",         "name": "Demand Zone (Accumulazione)", "desc": "Area di prezzo dove storicamente gli acquirenti istituzionali hanno assorbito"},
        # --- Canali di Prezzo ---
        {"id": "linear_regression",   "name": "Canale di Regressione",       "desc": "Canale lineare mediato statisticamente, identifica la tendenza 'matematica'"},
        {"id": "donchian_upper",      "name": "Donchian Channel Superiore",  "desc": "Massimo degli ultimi N periodi, usato nei sistemi Turtle Traders"},
        {"id": "donchian_lower",      "name": "Donchian Channel Inferiore",  "desc": "Minimo degli ultimi N periodi, breakout = segnale di entrata Turtle"},
        {"id": "vwap",                "name": "VWAP (Volume Weighted)",      "desc": "Prezzo medio ponderato sul volume, punto di equilibrio giornaliero istituzionale"},
    ],
    "oscillator": [
        # --- Oscillatori (pannello separato sotto il grafico) ---
        {"id": "rsi",            "name": "RSI 14",                    "desc": "Relative Strength Index: ipercomprato >70, ipervenduto <30. Nison+Murphy"},
        {"id": "macd_line",      "name": "MACD Line (12-26-9)",       "desc": "Differenza EMA12-EMA26, segnali di incrocio con signal line. Murphy"},
        {"id": "macd_signal",    "name": "MACD Signal",               "desc": "EMA 9 della MACD Line, segnale di acquisto/vendita al crossover"},
        {"id": "stochastic_k",   "name": "Stochastic %K (14)",        "desc": "Posizione del close nel range degli ultimi 14 periodi. Nison"},
        {"id": "stochastic_d",   "name": "Stochastic %D (3)",         "desc": "SMA(3) di %K, la linea di segnale dello Stochastic"},
        {"id": "williams_r",     "name": "Williams %R (14)",          "desc": "Indicatore momentum inverso: -100=ipervenduto, 0=ipercomprato. Larry Williams"},
    ]
}

# Colori di default per ogni strumento
DEFAULT_COLORS = {
    # Pattern — Nison candele singole
    "pattern_doji":               "#ffa502",
    "pattern_gravestone_doji":    "#ff4757",
    "pattern_dragonfly_doji":     "#00d4aa",
    "pattern_long_legged_doji":   "#ffd32a",
    "pattern_spinning_top":       "#a29bfe",
    "pattern_hammer":             "#00d4aa",
    "pattern_inverted_hammer":    "#74b9ff",
    "pattern_shooting_star":      "#ff4757",
    "pattern_marubozu":           "#3f8ef5",
    "pattern_belt_hold":          "#fd79a8",
    "pattern_pin_bar":            "#ff9f43",
    # Pattern — Nison candele doppie
    "pattern_engulfing":          "#ff9f43",
    "pattern_harami":             "#ee5a24",
    "pattern_harami_cross":       "#e17055",
    "pattern_tweezer":            "#fd9644",
    "pattern_dark_cloud_cover":   "#ff4757",
    "pattern_piercing_line":      "#00d4aa",
    "pattern_counterattack":      "#a29bfe",
    "pattern_upside_gap_two_crows":"#d63031",
    # Pattern — Nison candele triple
    "pattern_morning_star":       "#00d4aa",
    "pattern_morning_doji_star":  "#55efc4",
    "pattern_evening_doji_star":  "#e84393",
    "pattern_three_candles":      "#3f8ef5",
    "pattern_tasuki_gap":         "#fdcb6e",
    "pattern_rising_three_methods":"#74b9ff",
    "pattern_three_mountain_top": "#ff4757",
    # Pattern — Formazioni chartistiche
    "pattern_inside_bar":         "#fd9644",
    "pattern_powerbar":           "#f53b57",
    "pattern_triangle":           "#ee5a24",
    "pattern_wedge":              "#ff6b81",
    "pattern_flag":               "#fd9644",
    "pattern_double_top":         "#a29bfe",
    "pattern_head_shoulders":     "#e84393",
    # Pattern — Joe Ross
    "pattern_1_2_3_top":          "#ff4757",
    "pattern_1_2_3_bottom":       "#00d4aa",
    "pattern_ledge":              "#ffd32a",
    "pattern_trading_range":      "#74b9ff",
    "pattern_ross_hook":          "#f9ca24",
    "pattern_traders_trick":      "#6c5ce7",
    # Pattern — Larry Williams
    "pattern_oops":               "#00d4aa",
    "pattern_smash_day":          "#ff4757",
    "pattern_outside_day":        "#fd79a8",
    "pattern_volatility_breakout":"#f9ca24",
    "pattern_short_term_pivot":   "#a29bfe",
    # Volume
    "volume_vsa":                 "#3f8ef5",
    # Trend — SMA
    "sma_10":                     "#dfe6e9",
    "sma_20":                     "#dfe6e9",
    "sma_50":                     "#f9ca24",
    "sma_100":                    "#74b9ff",
    "sma_200":                    "#ff9f43",
    # Trend — EMA
    "ema_9":                      "#55efc4",
    "ema_20":                     "#00d4aa",
    "ema_50":                     "#fdcb6e",
    "ema_100":                    "#74b9ff",
    "ema_200":                    "#e17055",
    # Trend — Bande
    "bollinger_upper":            "rgba(116,185,255,0.8)",
    "bollinger_lower":            "rgba(116,185,255,0.8)",
    "bollinger_mid":              "rgba(116,185,255,0.5)",
    "keltner_upper":              "rgba(253,203,110,0.7)",
    "keltner_lower":              "rgba(253,203,110,0.7)",
    # Trend — Indicatori
    "supertrend":                 "#00d4aa",
    "ichimoku_cloud_upper":       "rgba(85,239,196,0.5)",
    "ichimoku_cloud_lower":       "rgba(255,118,117,0.4)",
    "ichimoku_kijun":             "#74b9ff",
    "ichimoku_tenkan":            "#fd79a8",
    "atr_upper":                  "rgba(253,203,110,0.6)",
    "atr_lower":                  "rgba(253,203,110,0.6)",
    # SR
    "pivot_points":               "#dfe6e9",
    "pivot_weekly":               "#b2bec3",
    "fib_retracement":            "#f9ca24",
    "fib_extension":              "#fd9644",
    "psych_levels":               "rgba(255,255,255,0.6)",
    "psych_levels_fine":          "rgba(255,255,255,0.4)",
    "dynamic_support":            "#00d4aa",
    "dynamic_resistance":         "#ff4757",
    "supply_zone":                "rgba(255,71,87,0.25)",
    "demand_zone":                "rgba(0,212,170,0.25)",
    "linear_regression":          "#a29bfe",
    "donchian_upper":             "rgba(116,185,255,0.7)",
    "donchian_lower":             "rgba(116,185,255,0.7)",
    "vwap":                       "#f9ca24",
    # Oscillatori
    "rsi":                        "#74b9ff",
    "macd_line":                  "#00d4aa",
    "macd_signal":                "#ff9f43",
    "stochastic_k":               "#a29bfe",
    "stochastic_d":               "#fd79a8",
    "williams_r":                 "#f9ca24",
}



# ------------------------------------------------------------------
# MAPPATURA LIBRO → DOMINI TECNICI (Deterministico, no LLM)
#
# Indica a quali specialisti (pattern/trend/sr/volume) ogni libro
# contribuisce conoscenza. Usato per costruire la skills_guidance
# in modo deterministico e completo, senza dipendere dall'LLM.
# ------------------------------------------------------------------
BOOK_DOMAIN_MAP = {
    # Candele giapponesi → primario per pattern
    "Steve Nison — Japanese Candlestick Charting":                    ["pattern"],
    # Statistica pattern grafici → pattern e livelli target S/R
    "Thomas Bulkowski — Encyclopedia of Chart Patterns":              ["pattern", "sr"],
    # Day trading operativo → pattern di entrata e livelli operativi
    "Joe Ross — Day Trading":                                         ["pattern", "sr"],
    # Short-term trading → trend di breve e analisi volumetrica
    "Larry Williams — Long-Term Secrets to Short-Term Trading":       ["trend", "volume"],
    # Analisi tecnica classica → trend, S/R, volume
    "John Murphy — Analisi Tecnica dei Mercati Finanziari":           ["trend", "sr", "volume"],
    # Multi-timeframe → trend, allineamento livelli
    "Brian Shannon — Technical Analysis Using Multiple Timeframes":   ["trend", "sr"],
}


# ------------------------------------------------------------------
# MAPPING KEYWORD → OVERLAY ID
#
# Per ogni tecnica estratta dai SKILL.md (heading ##), se contiene
# una delle keyword (lowercase), viene associata all'overlay ID
# corrispondente in computeOverlayData() di chart.js.
# Ordine importante: le keyword più specifiche devono venire prima.
# Tecniche senza match restano come badge informativi (overlay_id=None).
# ------------------------------------------------------------------
TECHNIQUE_OVERLAY_MAP: list[tuple[str, str]] = [
    # ── Doji variants (più specifici prima) ──────────────────────
    ("morning doji star",           "pattern_morning_doji_star"),
    ("evening doji star",           "pattern_evening_doji_star"),
    ("gravestone doji",             "pattern_gravestone_doji"),
    ("dragonfly doji",              "pattern_dragonfly_doji"),
    ("long-legged doji",            "pattern_long_legged_doji"),
    ("long legged doji",            "pattern_long_legged_doji"),
    # ── Stars ──────────────────────────────────────────────────
    ("morning star",                "pattern_morning_star"),
    ("evening star",                "pattern_morning_star"),
    ("star (stelle)",               "pattern_morning_star"),
    # ── Doji generico (dopo le varianti specifiche) ─────────────
    ("doji",                        "pattern_doji"),
    # ── Hammer family ───────────────────────────────────────────
    ("hanging man",                 "pattern_hammer"),
    ("inverted hammer",             "pattern_inverted_hammer"),
    ("shooting star",               "pattern_shooting_star"),
    ("hammer",                      "pattern_hammer"),
    # ── Single candles ──────────────────────────────────────────
    ("spinning top",                "pattern_spinning_top"),
    ("marubozu",                    "pattern_marubozu"),
    ("belt-hold",                   "pattern_belt_hold"),
    ("belt hold",                   "pattern_belt_hold"),
    ("pin bar",                     "pattern_pin_bar"),
    ("power bar",                   "pattern_powerbar"),
    ("power bars",                  "pattern_powerbar"),
    ("inside bar",                  "pattern_inside_bar"),
    # ── Double candles ──────────────────────────────────────────
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
    # ── Triple candles ──────────────────────────────────────────
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
    # ── Chart patterns (Bulkowski / Murphy) ─────────────────────
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
    # ── Ross patterns (TLOC) ─────────────────────────────────────
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
    # ── Williams patterns ────────────────────────────────────────
    ("smash day",                   "pattern_smash_day"),
    ("oops! pattern",               "pattern_oops"),
    ("oops pattern",                "pattern_oops"),
    ("outside day",                 "pattern_outside_day"),
    ("volatility breakout",         "pattern_volatility_breakout"),
    ("swing points as trend change","pattern_short_term_pivot"),
    ("short-term high/low",         "pattern_short_term_pivot"),
    ("short-term pivot",            "pattern_short_term_pivot"),
    # ── SR indicators ────────────────────────────────────────────
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
    # ── Trend indicators ─────────────────────────────────────────
    ("bollinger",                   "bollinger_upper"),
    ("keltner",                     "keltner_upper"),
    ("ichimoku",                    "ichimoku_kijun"),
    ("supertrend",                  "supertrend"),
    ("linear regression",           "linear_regression"),
    ("regressione lineare",         "linear_regression"),
    ("medie mobili",                "sma_20"),
    ("media mobile",                "sma_20"),
    ("moving average",              "sma_20"),
    # ── Volume ───────────────────────────────────────────────────
    ("volume spread analysis",      "volume_vsa"),
    ("vsa",                         "volume_vsa"),
    ("volume analysis",             "volume_vsa"),
    ("volume (volume analysis)",    "volume_vsa"),
]


def _find_overlay_id(technique_name: str) -> str | None:
    """
    Cerca nella TECHNIQUE_OVERLAY_MAP la prima keyword contenuta nel nome
    della tecnica (case-insensitive). Restituisce l'overlay_id corrispondente
    o None se la tecnica non ha rappresentazione visiva sul grafico.
    """
    name_lower = technique_name.lower()
    for keyword, overlay_id in TECHNIQUE_OVERLAY_MAP:
        if keyword in name_lower:
            return overlay_id
    return None


class SkillSelector:
    """
    Seleziona gli strumenti di analisi più adatti al contesto corrente.

    Produce due output distinti:
    - chosen_tools: strumenti grafici per il frontend (pattern/trend/sr overlay)
    - skills_guidance: istruzioni vincolanti con TUTTE le tecniche rilevanti
      per ogni specialista, costruite deterministicamente dal catalogo.
    """

    def __init__(self):
        self.skills_dir = Calibrazione.SKILLS_LIBRARY_DIR
        self._skill_summaries = None   # Cache sommari libri
        self._technique_catalog = None # Cache tecniche estratte dai SKILL.md

    def _load_technique_catalog(self) -> dict:
        """
        Estrae i nomi delle tecniche direttamente dai SKILL.md leggendo i titoli ## .
        Opera solo sui 6 libri tecnici (Calibrazione.TECHNICAL_SKILLS_DIRS).
        Restituisce {label_libro: [lista_nomi_tecniche]}.
        """
        if self._technique_catalog is not None:
            return self._technique_catalog

        # Mappa directory → etichetta leggibile
        BOOK_LABELS = {
            "encyclopedia_of_chart_patterns":        "Thomas Bulkowski — Encyclopedia of Chart Patterns",
            "encyclopedia-of-chart-patterns":         "Thomas Bulkowski — Encyclopedia of Chart Patterns",
            "japanese_candlestick_charting":          "Steve Nison — Japanese Candlestick Charting",
            "japanese-candlestick-charting":          "Steve Nison — Japanese Candlestick Charting",
            "joe_ross_daytrading":                    "Joe Ross — Day Trading",
            "joe-ross-daytrading":                    "Joe Ross — Day Trading",
            "larry_williams_long_term_secrets":       "Larry Williams — Long-Term Secrets to Short-Term Trading",
            "larry-williams-long-term-secrets":       "Larry Williams — Long-Term Secrets to Short-Term Trading",
            "murphy_analisi_tecnica":                 "John Murphy — Analisi Tecnica dei Mercati Finanziari",
            "murphy-analisi-tecnica":                 "John Murphy — Analisi Tecnica dei Mercati Finanziari",
            "technical_analysis_multiple_timeframes": "Brian Shannon — Technical Analysis Using Multiple Timeframes",
            "technical-analysis-multiple-timeframes": "Brian Shannon — Technical Analysis Using Multiple Timeframes",
        }

        catalog = {}
        for skill_dir_path in Calibrazione.TECHNICAL_SKILLS_DIRS:
            skill_file = os.path.join(skill_dir_path, "SKILL.md")
            if not os.path.exists(skill_file):
                logger.warning(f"[SKILL SELECTOR] SKILL.md non trovato: {skill_file}")
                continue

            dir_name = os.path.basename(skill_dir_path)
            label = BOOK_LABELS.get(dir_name, dir_name)
            techniques = []

            try:
                with open(skill_file, "r", encoding="utf-8", errors="ignore") as f:
                    frontmatter_done = False
                    dash_count = 0
                    for line in f:
                        stripped = line.strip()
                        # Salta il frontmatter YAML (tra i due ---)
                        if stripped == "---":
                            dash_count += 1
                            if dash_count == 2:
                                frontmatter_done = True
                            continue
                        if not frontmatter_done:
                            continue
                        # Estrae solo i titoli di secondo livello (## TecnicaNome)
                        # Esclude ### (sottosezioni) e titoli generici come "SKILLS ESTRATTE"
                        if stripped.startswith("## ") and not stripped.startswith("### "):
                            name = stripped[3:].strip()
                            if name and "skill" not in name.lower() and len(name) < 80:
                                techniques.append(name)
                                if len(techniques) >= 30:  # cap per evitare prompt bloat
                                    break
            except Exception as e:
                logger.warning(f"[SKILL SELECTOR] Errore lettura tecniche da {skill_file}: {e}")

            if techniques:
                catalog[label] = techniques
                logger.debug(f"[SKILL SELECTOR] {label}: {len(techniques)} tecniche trovate")

        self._technique_catalog = catalog
        return catalog

    def _load_skill_summaries(self) -> str:
        """
        Legge i file SKILL.md e ne estrae un sommario (max 800 char per libro).
        Usato come contesto aggiuntivo nel prompt del selettore.
        """
        if self._skill_summaries is not None:
            return self._skill_summaries

        summaries = []
        for skill_dir_path in Calibrazione.TECHNICAL_SKILLS_DIRS:
            skill_file = os.path.join(skill_dir_path, "SKILL.md")
            if not os.path.exists(skill_file):
                continue
            try:
                with open(skill_file, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read(800)
                dir_name = os.path.basename(skill_dir_path)
                summaries.append(f"[{dir_name}]:\n{content.strip()}")
            except Exception as e:
                logger.warning(f"[SKILL SELECTOR] Errore lettura {skill_file}: {e}")

        self._skill_summaries = "\n---\n".join(summaries)
        return self._skill_summaries

    def _build_catalog_text(self) -> str:
        """Costruisce la rappresentazione testuale del catalogo strumenti grafici."""
        lines = ["STRUMENTI DISPONIBILI NEL GRAFICO (usa SOLO questi ID):"]
        for group, tools in AVAILABLE_TOOLS.items():
            lines.append(f"\n[{group.upper()}]")
            for t in tools:
                lines.append(f"  - ID: {t['id']} | Nome: {t['name']} | Uso: {t['desc']}")
        return "\n".join(lines)

    def _build_technique_catalog_text(self) -> str:
        """
        Costruisce il testo del catalogo tecniche per il prompt.
        Formato: [Libro]: Tecnica1, Tecnica2, ...
        """
        catalog = self._load_technique_catalog()
        if not catalog:
            return "Nessuna tecnica trovata nelle Skill."

        lines = ["TECNICHE DISPONIBILI DALLE SKILL (seleziona ESCLUSIVAMENTE da questa lista):"]
        for book_label, techniques in catalog.items():
            techs_str = " | ".join(techniques)
            lines.append(f"\n[{book_label}]:\n  {techs_str}")
        return "\n".join(lines)

    def select_tools(self, nome_asset: str, macro_sentiment: str, data_dict: dict) -> dict:
        """
        Analizza il contesto e produce due selezioni complementari:

        1. chosen_tools (pattern/trend/sr): strumenti grafici per il frontend
        2. techniques: tecniche nominate dai libri per vincolare gli agenti specialisti

        Args:
            nome_asset:      Il ticker (es. "GC=F", "AAPL")
            macro_sentiment: Testo del sentiment macro prodotto dall'AgnoMacroExpert
            data_dict:       Dizionario con i dati OHLCV multi-timeframe

        Returns:
            Dict con: pattern · trend · sr · summary · raw_skills_used ·
                      techniques · skills_guidance · success
        """
        logger.info(f"[SKILL SELECTOR] Selezione strumenti e tecniche per {nome_asset}...")

        catalog_text    = self._build_catalog_text()

        try:
            last_1d = data_dict["1d"].tail(5).to_string() if "1d" in data_dict else "N/D"
        except Exception:
            last_1d = "N/D"

        prompt = f"""Sei un Analista Tecnico Senior. Analizza il contesto e produci due selezioni:

ASSET: {nome_asset}

SENTIMENT MACRO:
{macro_sentiment[:1200]}

DATI RECENTI (ultime 5 candele 1D):
{last_1d}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PARTE A — STRUMENTI GRAFICI (per il frontend)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{catalog_text}

Regole per la Parte A:
- Usa SOLO gli ID esatti del catalogo grafico (nessun ID inventato)
- Il campo "reason" deve essere breve: max 10 parole
- Il campo "color" deve essere un colore HEX chiaro e ben visibile: lo sfondo del grafico è SCURO. Non usare MAI nero (#000, #000000, "black") né colori molto scuri. Usa colori come "#f9ca24" (giallo), "#74b9ff" (blu), "#ff9f43" (arancio), "#00d4aa" (verde acqua), "#ff6b81" (rosa), "#a29bfe" (viola).
- Commodity (Oro, Oil): SMA lente + Fibonacci + Zone S/D + Price Action + pattern candlestick Nison + RSI
- Crypto: EMA veloci + SuperTrend + Bollinger + Stochastic + pattern Ross Hook
- Forex: EMA + Ichimoku + Pivot settimanali + MACD
- Sentiment BEARISH: privilegia resistenze, pattern ribassisti (dark_cloud_cover, shooting_star, 1_2_3_top, outside_day, smash_day), Williams %R
- Sentiment BULLISH: privilegia supporti, pattern rialzisti (piercing_line, morning_star, 1_2_3_bottom, oops), RSI, Stochastic
- GRUPPO OSCILLATOR: seleziona TUTTI gli oscillatori rilevanti per il contesto — nessun limite massimo. Includili tutti se utili a confermare i segnali
- PATTERN JOE ROSS: usa pattern_1_2_3_top/bottom, pattern_ross_hook, pattern_ledge per asset con trend chiaro
- PATTERN LARRY WILLIAMS: usa pattern_oops e pattern_volatility_breakout in mercati volatili con gap frequenti

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT — Rispondi SOLO con JSON valido (nessun testo fuori, niente markdown):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{{
  "pattern": [
    {{"id": "pattern_engulfing", "name": "Bullish/Bearish Engulfing", "reason": "...", "color": "#ff9f43"}},
    {{"id": "pattern_morning_star", "name": "Morning Star", "reason": "...", "color": "#00d4aa"}},
    {{"id": "pattern_1_2_3_bottom", "name": "1-2-3 Bottom", "reason": "...", "color": "#00d4aa"}}
  ],
  "trend": [
    {{"id": "sma_200", "name": "SMA 200", "reason": "...", "color": "#f9ca24"}},
    {{"id": "ema_50", "name": "EMA 50", "reason": "...", "color": "#74b9ff"}}
  ],
  "sr": [
    {{"id": "fib_retracement", "name": "Fibonacci Retracement", "reason": "...", "color": "#ffd700"}},
    {{"id": "supply_zone", "name": "Supply Zone", "reason": "...", "color": "#ff6b81"}}
  ],
  "oscillator": [
    {{"id": "rsi",           "name": "RSI 14",             "reason": "...", "color": "#74b9ff"}},
    {{"id": "macd_line",     "name": "MACD Line",          "reason": "...", "color": "#00d4aa"}},
    {{"id": "macd_signal",   "name": "MACD Signal",        "reason": "...", "color": "#ff9f43"}},
    {{"id": "stochastic_k",  "name": "Stochastic %K",      "reason": "...", "color": "#a29bfe"}},
    {{"id": "stochastic_d",  "name": "Stochastic %D",      "reason": "...", "color": "#fd79a8"}},
    {{"id": "williams_r",    "name": "Williams %R",        "reason": "...", "color": "#f9ca24"}}
  ],
  "summary": "Breve frase riassuntiva della scelta strategica per l'asset"
}}"""

        try:
            from agents.model_factory import get_model
            # Usiamo un modello senza thinking mode per output JSON puro.
            # Qwen3 usa troppi token per il blocco <think> e tronca il JSON.
            llm = get_model(Calibrazione.MODEL_SKILL_SELECTOR, temperature=Calibrazione.TEMPERATURE_SKILL_SELECTOR)

            from agno.agent import Agent
            selector_agent = Agent(
                model=llm,
                description="Sei un analista tecnico che seleziona strumenti di analisi in base al contesto.",
                instructions=["Rispondi SOLO con JSON valido, senza markdown extra."],
                markdown=False,
            )

            response = selector_agent.run(prompt)
            raw = response.content if response.content else ""
            raw = raw.strip()

            # Log diagnostico — mostriamo i primi 500 caratteri della risposta
            logger.debug(f"[SKILL SELECTOR] Risposta grezza AI (primi 500 char): {raw[:500]}")

            if not raw:
                logger.error(f"[SKILL SELECTOR] L'AI ha prodotto una risposta VUOTA.")
                return {"success": False, "error": "AI_EMPTY_RESPONSE", "summary": "L'AI non ha prodotto nessuna risposta."}

            # 1. Rimuoviamo i blocchi markdown residui
            raw = re.sub(r'^```(?:json)?\s*', '', raw, flags=re.MULTILINE)
            raw = re.sub(r'\s*```$', '', raw, flags=re.MULTILINE)

            # 2. Rimuoviamo il blocco <think>...</think> se il tag è chiuso
            raw = re.sub(r'<think>.*?</think>', '', raw, flags=re.DOTALL)

            # 3. Se il blocco <think> non è chiuso (risposta troncata nel mezzo del pensiero),
            #    cerchiamo direttamente il primo '{' e prendiamo tutto da lì in poi.
            #    Questo è il fix principale per Qwen3 su Groq che taglia la risposta.
            first_brace = raw.find('{')
            if first_brace == -1:
                logger.error(f"[SKILL SELECTOR] Nessun JSON trovato nella risposta AI.")
                return {"success": False, "error": "AI_NO_JSON", "summary": "Nessun blocco JSON trovato nella risposta."}
            raw = raw[first_brace:]

            # 4. Tentiamo il parsing — se il JSON è troncato, json.loads fallirà
            #    ma almeno avremo tagliato il blocco <think> non chiuso
            
            # 4a. JSON repair: se il JSON è troncato (risposta lunga), lo chiude
            #     automaticamente prima di fare il parsing. Evita crash con output estesi.
            try:
                from json_repair import repair_json
                raw = repair_json(raw)
            except ImportError:
                pass  # json_repair opzionale, si prosegue col parsing normale

            # 4b. Parsing JSON
            chosen = json.loads(raw)

            # Validazione: assicuriamoci che gli ID esistano nel catalogo
            chosen = self._validate_and_fallback(chosen)

            sg = chosen.get('skills_guidance', {})
            logger.success(
                f"[SKILL SELECTOR] Skills guidance deterministica per {nome_asset}: "
                + ", ".join(f"{d}={len(sg.get(d,'').splitlines())} righe" for d in ("pattern","trend","sr","volume"))
            )
            return chosen

        except json.JSONDecodeError as e:
            logger.warning(f"[SKILL SELECTOR] JSON non valido dall'AI ({e}). Raw: '{raw[:300] if 'raw' in dir() else 'N/A'}'. Segnalo fallimento.")
            return {"success": False, "error": "AI_JSON_ERROR", "summary": f"L'AI non ha prodotto un formato JSON valido: {e}"}

        except Exception as e:
            logger.error(f"[SKILL SELECTOR] Errore: {e}. Segnalo fallimento.")
            return {"success": False, "error": "AI_SYSTEM_ERROR", "summary": str(e)}


    def _validate_and_fallback(self, chosen: dict) -> dict:
        """
        Valida il JSON restituito dall'AI:
        - Rimuove ID grafici non presenti nel catalogo (pattern/trend/sr)
        - Valida le tecniche dai libri (techniques): scarta quelle con nome vuoto
        - Costruisce skills_guidance dai techniques validati
        """
        all_valid_ids = {t["id"]: t for group in AVAILABLE_TOOLS.values() for t in group}
        result = {"success": True}

        # Mappa di normalizzazione degli ID generati dall'AI (alias comuni)
        # Questo evita che l'AI scarti pattern validi solo perché ha scelto un nome più specifico.
        ID_ALIASES = {
            "pattern_bullish_engulfing":    "pattern_engulfing",
            "pattern_bearish_engulfing":    "pattern_engulfing",
            "pattern_morning_star_doji":    "pattern_morning_doji_star",
            "pattern_evening_star_doji":    "pattern_evening_doji_star",
            "pattern_hammer_inverted":      "pattern_inverted_hammer",
            "pattern_star_shooting":        "pattern_shooting_star",
            "pattern_bullish_harami":       "pattern_harami",
            "pattern_bearish_harami":       "pattern_harami",
        }

        # ── Parte A: strumenti grafici (frontend) ──────────────────────────────
        for group in ("pattern", "trend", "sr", "oscillator"):
            valid_items = []
            for item in chosen.get(group, []):
                if not isinstance(item, dict):
                    continue
                
                tool_id = item.get("id")

                # 1. Normalizzazione (se l'AI usa un alias comune, lo riportiamo all'ID originale)
                if tool_id in ID_ALIASES:
                    original_id = tool_id
                    tool_id = ID_ALIASES[tool_id]
                    item["id"] = tool_id
                    logger.debug(f"[SKILL SELECTOR] ID normalizzato: {original_id!r} -> {tool_id!r}")

                # 2. Controllo esistenza nel catalogo
                if tool_id not in all_valid_ids:
                    logger.warning(f"[SKILL SELECTOR] ID grafico non valido rimosso: {tool_id!r}")
                    continue

                static_info = all_valid_ids[tool_id]

                # Colore: forza bianco se mancante o nero
                color_val = str(item.get("color", "")).lower().strip()
                is_black = color_val in {"#000", "#000000", "black", "null", "none", "",
                                         "rgb(0,0,0)", "rgba(0,0,0,1)", "rgba(0,0,0,0)"}
                if is_black:
                    logger.debug(f"[SKILL SELECTOR] Colore nero/vuoto scartato per {tool_id}, forzato bianco.")
                item["color"] = "#ffffff" if (is_black or not item.get("color")) else item["color"]
                if not item.get("color"):
                    item["color"] = DEFAULT_COLORS.get(tool_id, "#ffffff")

                item.setdefault("desc", static_info.get("desc", ""))
                item.setdefault("name", static_info.get("name", ""))
                valid_items.append(item)

            result[group] = valid_items

        # ── Parte B: skills_guidance deterministica (indipendente dall'LLM) ────
        # Tutti e 6 i libri sono sempre applicati — nessuna selezione LLM.
        result["techniques"]      = {}   # non più usato (guidance ora deterministica)
        result["summary"]         = chosen.get("summary", "Selezione AI per questo asset.")
        result["raw_skills_used"] = list(BOOK_DOMAIN_MAP.keys())   # sempre tutti i libri
        result["skills_guidance"] = self._build_skills_guidance()

        # ── Parte C: struttura leggibile per il frontend ─────────────────────
        # Espone le tecniche per libro per dominio come JSON strutturato.
        # Ogni tecnica è ora un oggetto {name, overlay_id} dove overlay_id è
        # l'ID computeOverlayData() di chart.js se la tecnica è visualizzabile,
        # oppure null se è una tecnica concettuale senza rendering grafico.
        catalog = self._load_technique_catalog()
        techniques_per_domain = {}
        for domain in ("pattern", "trend", "sr", "volume"):
            books_for_domain = {}
            for book_label, book_techs in catalog.items():
                if domain in BOOK_DOMAIN_MAP.get(book_label, []):
                    books_for_domain[book_label] = [
                        {"name": t, "overlay_id": _find_overlay_id(t)}
                        for t in book_techs
                    ]
            techniques_per_domain[domain] = books_for_domain
        result["techniques_per_domain"] = techniques_per_domain

        return result

    def _build_skills_guidance(self) -> dict:
        """
        Costruisce le istruzioni vincolanti (FOCUS SKILLS) per ogni specialista.

        Approccio DETERMINISTICO: include TUTTE le tecniche del catalogo per ogni
        libro rilevante per quel dominio (via BOOK_DOMAIN_MAP). Non dipende dall'LLM.
        Ogni specialista riceve sempre l'intero corpus di tecniche applicabili.

        Args:
            techniques: ignorato (mantenuto per compatibilità firma). La guidance
                        è ora costruita interamente dal catalogo.
        Returns:
            dict {domain: str} — istruzioni da iniettare nel prompt di ogni specialista
        """
        catalog = self._load_technique_catalog()

        def build_sections_for_domain(domain: str) -> str:
            """Costruisce il testo con tutte le tecniche dei libri rilevanti per il dominio."""
            sections = []
            for book_label, book_techs in catalog.items():
                domains_for_book = BOOK_DOMAIN_MAP.get(book_label, [])
                if domain not in domains_for_book:
                    continue
                numbered = "\n".join(f"  {i+1}. {t}" for i, t in enumerate(book_techs))
                sections.append(f"[{book_label}]:\n{numbered}")
            return "\n\n".join(sections)

        guidance = {}

        # ── Pattern Analyst ────────────────────────────────────────────────────
        sections = build_sections_for_domain("pattern")
        if sections:
            guidance["pattern"] = (
                "FOCUS SKILLS — Tecniche OBBLIGATORIE da tutti i libri rilevanti.\n"
                "Devi analizzare TUTTE le tecniche elencate, anche quelle meno evidenti. "
                "Se una tecnica non è applicabile ai dati attuali, scrivilo esplicitamente.\n\n"
                f"{sections}\n\n"
                "Per ogni tecnica consulta le Skill caricate per le regole di validità esatte "
                "e il calcolo del target con il metodo Bulkowski dove applicabile."
            )
        else:
            guidance["pattern"] = ""

        # ── Trend Analyst ──────────────────────────────────────────────────────
        sections = build_sections_for_domain("trend")
        if sections:
            guidance["trend"] = (
                "FOCUS SKILLS — Tecniche OBBLIGATORIE da tutti i libri rilevanti.\n"
                "Devi analizzare TUTTE le tecniche elencate, anche quelle meno evidenti. "
                "Se una tecnica non è applicabile ai dati attuali, scrivilo esplicitamente.\n\n"
                f"{sections}\n\n"
                "Per ogni tecnica consulta le Skill per le regole operative precise "
                "(criteri di incrocio, analisi top-down, segnali di momentum, allineamento MTF)."
            )
        else:
            guidance["trend"] = ""

        # ── SR Analyst ─────────────────────────────────────────────────────────
        sections = build_sections_for_domain("sr")
        if sections:
            guidance["sr"] = (
                "FOCUS SKILLS — Tecniche OBBLIGATORIE da tutti i libri rilevanti.\n"
                "Devi analizzare TUTTE le tecniche elencate per costruire la mappa completa dei livelli. "
                "Se una tecnica non produce livelli utili, documentalo esplicitamente.\n\n"
                f"{sections}\n\n"
                "Per ogni tecnica consulta le Skill per i criteri di identificazione precisi "
                "e il calcolo del punteggio di confluenza tra livelli diversi."
            )
        else:
            guidance["sr"] = ""

        # ── Volume Analyst ─────────────────────────────────────────────────────
        sections = build_sections_for_domain("volume")
        vol_base = (
            "Il tuo ruolo è VALIDARE i segnali degli altri specialisti con l'analisi volumetrica.\n\n"
            "FOCUS SKILLS — Tecniche OBBLIGATORIE da tutti i libri rilevanti.\n"
            "Devi analizzare TUTTE le tecniche elencate, anche quelle meno evidenti. "
            "Se una tecnica non è applicabile ai dati attuali, scrivilo esplicitamente.\n\n"
        )
        if sections:
            vol_base += f"{sections}\n\n"
        vol_base += (
            "Per ogni tecnica consulta le Skill per i criteri esatti (sforzo vs risultato, "
            "fasi Wyckoff, segnali VSA: No Demand, No Supply, Climax, Spring, Upthrust).\n"
            "REGOLA ASSOLUTA: se i volumi NON confermano i segnali tecnici degli altri specialisti, "
            "devi dichiarare RISCHIO ELEVATO indipendentemente dalla qualità del segnale grafico."
        )
        guidance["volume"] = vol_base

        return guidance
