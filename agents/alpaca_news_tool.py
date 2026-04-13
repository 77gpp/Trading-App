from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import NewsRequest
from datetime import datetime, timedelta
import Calibrazione
from loguru import logger

# Dizionario per mappare asset non azionari (future, indici, materie prime, forex)
# nei loro equivalenti ETF/simboli Alpaca. I valori sono liste di simboli per
# massimizzare la copertura delle notizie: Alpaca cercherà news associate a
# qualsiasi dei simboli elencati.
ALPACA_PROXY_MAP = {
    # ── Oro / Gold ────────────────────────────────────────────────────────────
    "oro": ["GLD", "IAU", "GDX", "GOLD"],
    "gold": ["GLD", "IAU", "GDX", "GOLD"],
    "gc=f": ["GLD", "IAU"], "xauusd": ["GLD", "IAU"], "gc": ["GLD", "IAU"],

    # ── Argento / Silver ──────────────────────────────────────────────────────
    "argento": ["SLV", "PSLV", "PAAS"],
    "silver": ["SLV", "PSLV"], "si=f": ["SLV"], "xagusd": ["SLV"], "si": ["SLV"],

    # ── Petrolio / Crude Oil ──────────────────────────────────────────────────
    "petrolio": ["USO", "XLE", "OXY"],
    "oil": ["USO", "XLE"], "crude oil": ["USO", "XLE"],
    "wti": ["USO"], "brent": ["BNO", "USO"],
    "cl=f": ["USO"], "cl": ["USO"],

    # ── Gas Naturale ──────────────────────────────────────────────────────────
    "gas naturale": ["UNG", "BOIL"],
    "natural gas": ["UNG", "BOIL"], "ng=f": ["UNG"], "ng": ["UNG"],

    # ── S&P 500 ───────────────────────────────────────────────────────────────
    "sp500": ["SPY", "IVV", "VOO"],
    "s&p 500": ["SPY", "IVV"], "s&p500": ["SPY", "IVV"],
    "^gspc": ["SPY"], "es=f": ["SPY"],

    # ── Nasdaq ────────────────────────────────────────────────────────────────
    "nasdaq": ["QQQ", "TQQQ"], "^ixic": ["QQQ"], "nq=f": ["QQQ"],

    # ── Dow Jones ─────────────────────────────────────────────────────────────
    "dow jones": ["DIA"], "dj": ["DIA"], "^dji": ["DIA"], "ym=f": ["DIA"],

    # ── Russell 2000 ──────────────────────────────────────────────────────────
    "russell 2000": ["IWM"], "rut": ["IWM"], "^rut": ["IWM"],

    # ── Crypto ────────────────────────────────────────────────────────────────
    "bitcoin": ["BTCUSD", "IBIT", "FBTC"],
    "btc": ["BTCUSD", "IBIT"], "btc-usd": ["BTCUSD"], "btcusd": ["BTCUSD"],
    "ethereum": ["ETHUSD", "ETHA"],
    "eth": ["ETHUSD"], "eth-usd": ["ETHUSD"], "ethusd": ["ETHUSD"],

    # ── Forex ─────────────────────────────────────────────────────────────────
    "eurusd": ["EURUSD", "FXE"], "eurusd=x": ["EURUSD", "FXE"], "euro": ["FXE", "EURUSD"],
    "dollaro": ["UUP"], "dollar": ["UUP"], "usd": ["UUP"],
    "dxy": ["UUP"], "dx-y.nyb": ["UUP"],
    "gbpusd": ["GBPUSD", "FXB"], "gbp": ["FXB"],
    "usdjpy": ["USDJPY", "FXY"], "jpy": ["FXY"], "yen": ["FXY"],
    "usdchf": ["USDCHF"], "chf": ["USDCHF"],

    # ── Bond / Tassi ──────────────────────────────────────────────────────────
    "treasury": ["TLT", "IEF", "SHY"],
    "bond": ["TLT", "IEF"], "bonds": ["TLT", "IEF"],
    "10y treasury": ["TLT", "IEF"], "tnote": ["IEF", "TLT"],
    "^tnx": ["TLT", "IEF"], "zn=f": ["IEF"],

    # ── Materie prime / Commodities ───────────────────────────────────────────
    "rame": ["CPER", "FCX", "COPX"],
    "copper": ["CPER", "FCX"], "hg=f": ["CPER", "FCX"],
    "frumento": ["WEAT"], "wheat": ["WEAT"],
    "mais": ["CORN"], "corn": ["CORN"],
    "soia": ["SOYB"], "soybean": ["SOYB"],
    "materie prime": ["DJP", "PDBC"], "commodities": ["DJP", "PDBC"],

    # ── Volatilità ────────────────────────────────────────────────────────────
    "vix": ["VXX", "UVXY"], "^vix": ["VXX"],

    # ── Mercati emergenti ──────────────────────────────────────────────────────
    "emerging markets": ["EEM", "VWO"], "em": ["EEM", "VWO"],

    # ── High Yield / Credit ───────────────────────────────────────────────────
    "high yield": ["HYG", "JNK"], "hy": ["HYG", "JNK"],

    # ── Settori ───────────────────────────────────────────────────────────────
    "energia": ["XLE", "VDE"], "energy": ["XLE", "VDE"],
    "tecnologia": ["XLK", "VGT"], "tech": ["XLK", "QQQ"],
    "finanza": ["XLF", "VFH"], "financials": ["XLF"],
    "difesa": ["ITA", "XAR"], "defense": ["ITA", "XAR"],
}

def get_alpaca_news(symbol: str, start: str = None, end: str = None) -> str:
    """
    Ottiene le notizie finanziarie ufficiali per un determinato asset in un periodo specifico.

    IMPORTANTE: Passa il nome comune dell'asset in italiano o inglese (es. 'gold', 'oro',
    'oil', 'petrolio', 'bitcoin', 'sp500', 'eurusd', 'nasdaq') invece di ticker con caratteri
    speciali (es. 'GC=F', 'CL=F', '^GSPC'). Il tool converte automaticamente il nome nel
    simbolo ETF/proxy corretto per Alpaca e cerca news su più simboli correlati.

    Args:
        symbol (str): Nome comune o simbolo dell'asset.
                      Esempi corretti: 'gold', 'oil', 'bitcoin', 'sp500', 'eurusd', 'AAPL'.
                      Da evitare: 'GC=F', 'CL=F', '^GSPC' (ticker con caratteri speciali).
        start (str, optional): Data inizio ISO (YYYY-MM-DD). Obbligatoria.
        end (str, optional): Data fine ISO (YYYY-MM-DD). Default: oggi.

    Returns:
        str: Una stringa formattata con i titoli delle notizie e i link alle fonti.
    """
    # Mappatura Proxy per superare il limite di Alpaca sui futures/indici
    original_symbol = symbol
    symbol_lower = symbol.strip().lower()

    # Se il nome è nella mappa, usiamo la lista di simboli proxy (copertura massima)
    if symbol_lower in ALPACA_PROXY_MAP:
        proxy = ALPACA_PROXY_MAP[symbol_lower]
        alpaca_symbols = proxy if isinstance(proxy, list) else [proxy]
        logger.info(f"[ALPACA TOOL] Mapping '{original_symbol}' -> proxy: {alpaca_symbols}")
    else:
        # Fallback: puliamo il ticker dallo stile Yahoo Finance -> Alpaca
        cleaned = symbol.split("=")[0].split("-")[0].replace("^", "").upper()
        alpaca_symbols = [cleaned]

    if not Calibrazione.ALPACA_API_KEY or not Calibrazione.ALPACA_SECRET_KEY:
        logger.warning("[ALPACA TOOL] Chiavi API non trovate.")
        return "Errore: Chiavi API Alpaca non configurate. Verificare il file .env"

    try:
        client = NewsClient(
            api_key=Calibrazione.ALPACA_API_KEY,
            secret_key=Calibrazione.ALPACA_SECRET_KEY
        )

        # Calcoliamo il periodo di ricerca basandoci sui parametri obbligatori
        if start:
            if len(start) == 10: start += "T00:00:00Z"
            start_dt_str = start
        else:
            logger.error("[ALPACA TOOL] Data di inizio mancante. Impossibile procedere senza periodo definito.")
            return "ERRORE: Periodo di analisi non fornito. L'analisi richiede date di inizio e fine obbligatorie."

        if end:
            if len(end) == 10: end += "T23:59:59Z"
            end_dt_str = end
        else:
            end_dt_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

        symbols_label = ", ".join(alpaca_symbols)
        # NewsRequest.symbols vuole una stringa CSV, non una lista
        symbols_csv = ",".join(alpaca_symbols)
        logger.info(f"[ALPACA TOOL] Ricerca news per [{symbols_label}] nel periodo {start_dt_str} -> {end_dt_str}...")

        request_params = NewsRequest(
            symbols=symbols_csv,
            start=start_dt_str,
            end=end_dt_str,
            limit=getattr(Calibrazione, "ALPACA_NEWS_LIMIT", 15)
        )

        news_response = client.get_news(request_params)

        articles = news_response.data.get('news', [])

        if not articles:
            return f"Nessuna notizia ufficiale trovata su Alpaca per [{symbols_label}] nel periodo indicato ({start_dt_str} -> {end_dt_str})."

        formatted_news = [f"### Notizie Alpaca Markets per {original_symbol} [{symbols_label}]:"]
        for article in articles:
            headline = article.headline
            url = article.url
            source = article.source
            date = article.created_at.strftime('%Y-%m-%d')
            formatted_news.append(f"- **{headline}** ({date}) - [Leggi Fonte]({url}) [Fonte: {source}]")

        return "\n".join(formatted_news)
        
    except Exception as e:
        logger.error(f"[ALPACA TOOL] Errore: {e}")
        return f"Errore tecnico nel recupero news Alpaca: {str(e)}"

if __name__ == "__main__":
    # Test rapido se lanciato direttamente
    print(get_alpaca_news("AAPL"))
