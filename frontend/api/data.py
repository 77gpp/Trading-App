"""
api/data.py — Endpoint Flask per il recupero dati finanziari.

Questo modulo espone due API:
1. GET /api/data/chart  — Scarica i dati OHLCV (Open, High, Low, Close, Volume) 
                          da Yahoo Finance per le date selezionate e il timeframe scelto.
2. GET /api/data/news   — Scarica le notizie da Alpaca Markets per il periodo selezionato
                          e le restituisce con data e titolo per visualizzarle sul grafico.
"""

import sys
import os

# Il ROOT del progetto è due livelli sopra (frontend/api → frontend → root)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT_DIR)

from flask import Blueprint, request, jsonify
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from loguru import logger

data_bp = Blueprint("data", __name__)

# ------------------------------------------------------------------
# Lista di simboli comuni con alias (per la ricerca per nome o ISIN)
# ------------------------------------------------------------------
ASSET_ALIASES = {
    # Materie Prime
    "oro": "GC=F", "gold": "GC=F", "xauusd": "GC=F",
    "argento": "SI=F", "silver": "SI=F", "xagusd": "SI=F",
    "petrolio": "CL=F", "oil": "CL=F", "wti": "CL=F",
    "gas naturale": "NG=F", "natural gas": "NG=F",
    # Indici
    "sp500": "^GSPC", "s&p500": "^GSPC", "s&p 500": "^GSPC",
    "nasdaq": "^IXIC", "dow jones": "^DJI", "dj": "^DJI",
    "ftse mib": "FTSEMIB.MI", "dax": "^GDAXI",
    # Forex
    "eurusd": "EURUSD=X", "euro dollaro": "EURUSD=X",
    "gbpusd": "GBPUSD=X", "usdjpy": "USDJPY=X",
    # Crypto
    "bitcoin": "BTC-USD", "btc": "BTC-USD",
    "ethereum": "ETH-USD", "eth": "ETH-USD",
    # Azioni popolari
    "apple": "AAPL", "microsoft": "MSFT", "google": "GOOGL",
    "amazon": "AMZN", "tesla": "TSLA", "nvidia": "NVDA",
    "meta": "META", "netflix": "NFLX",
}

def resolve_ticker(symbol: str) -> str:
    """
    Converte un nome comune o ISIN nel ticker Yahoo Finance corrispondente.
    Se non trovato nella lista, restituisce il simbolo originale (potrebbe 
    già essere un ticker valido come 'GC=F', 'AAPL', ecc.).
    """
    sym_lower = symbol.strip().lower()
    return ASSET_ALIASES.get(sym_lower, symbol.strip().upper())


def calculate_volume_profile(df, bins_count=50):
    """
    Calcola il Volume Profile (Volume by Price) dai dati OHLCV.
    Suddivide il range di prezzo totale in bins_count livelli.
    """
    if df.empty:
        return {"bins": [], "poc": 0}

    low_price  = df["Low"].min()
    high_price = df["High"].max()
    price_range = high_price - low_price

    if price_range <= 0:
        return {"bins": [], "poc": 0}

    bin_size = price_range / bins_count
    
    # Inizializziamo i bin (centro del bin e volume)
    profile = {}
    for i in range(bins_count):
        price_level = low_price + (i * bin_size) + (bin_size / 2)
        profile[i] = {"price": round(price_level, 4), "volume": 0}

    # Distribuiamo il volume di ogni candela sui bin che tocca
    # (Metodo semplificato: assegniamo il volume al bin della chiusura)
    for _, row in df.iterrows():
        price = row["Close"]
        bin_idx = int((price - low_price) / bin_size)
        if bin_idx >= bins_count: bin_idx = bins_count - 1
        if bin_idx < 0: bin_idx = 0
        profile[bin_idx]["volume"] += int(row["Volume"])

    bins_list = list(profile.values())
    
    # Identifichiamo il POC (Point of Control)
    poc_bin = max(bins_list, key=lambda x: x["volume"])
    poc_price = poc_bin["price"]

    return {
        "bins": bins_list,
        "poc": poc_price,
        "max_volume": int(poc_bin["volume"])
    }


# ------------------------------------------------------------------
# ENDPOINT 1: Dati OHLCV per il grafico
# ------------------------------------------------------------------
@data_bp.route("/chart", methods=["GET"])
def get_chart_data():
    """
    Parametri GET:
      - symbol   : ticker o nome asset (es. 'GC=F', 'oro', 'AAPL')
      - start    : data inizio in formato YYYY-MM-DD
      - end      : data fine in formato YYYY-MM-DD
      - interval : timeframe ('1m', '2m', '5m', '15m', '30m', '1h', '4h', '1d', '1wk', '1mo', '3mo') — default '1d'
    
    Restituisce:
      JSON con array di candele: [{time, open, high, low, close, volume}, ...]
    """
    symbol   = request.args.get("symbol", "GC=F")
    start    = request.args.get("start", "")
    end      = request.args.get("end", "")
    interval = request.args.get("interval", "1d")

    ticker = resolve_ticker(symbol)
    logger.info(f"[DATA API] Richiesta dati: {ticker} | {start} → {end} | {interval}")

    if not start or not end:
        return jsonify({"error": "Parametri 'start' e 'end' obbligatori"}), 400

    try:
        # Yahoo Finance non supporta 4h nativo: scarichiamo 1h e poi resampliamo
        yf_interval = "1h" if interval == "4h" else interval

        # yfinance con date esplicite
        df = yf.download(ticker, start=start, end=end, interval=yf_interval, auto_adjust=True)

        if df.empty:
            return jsonify({"error": f"Nessun dato trovato per {ticker} nel periodo {start}→{end}"}), 404

        # Puliamo il MultiIndex se presente (yfinance lo produce a volte)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Resampling 4h se richiesto
        if interval == "4h":
            df = df.resample("4h").agg({
                "Open": "first", "High": "max",
                "Low": "min", "Close": "last", "Volume": "sum"
            }).dropna()

        # Convertiamo in formato JSON per Lightweight Charts
        candles = []
        for ts, row in df.iterrows():
            # Timestamp UNIX in secondi (richiesto da Lightweight Charts)
            time_val = int(ts.timestamp())
            candles.append({
                "time":   time_val,
                "open":   round(float(row["Open"]),  4),
                "high":   round(float(row["High"]),  4),
                "low":    round(float(row["Low"]),   4),
                "close":  round(float(row["Close"]), 4),
                "volume": int(row["Volume"])
            })

        logger.success(f"[DATA API] {len(candles)} candele inviate per {ticker}")
        
        # Calcolo del Volume Profile per l'intero periodo
        vol_profile = calculate_volume_profile(df)

        return jsonify({
            "ticker":   ticker,
            "symbol":   symbol,
            "interval": interval,
            "candles":  candles,
            "volume_profile": vol_profile
        })

    except Exception as e:
        logger.error(f"[DATA API] Errore: {e}")
        return jsonify({"error": str(e)}), 500


# ------------------------------------------------------------------
# ENDPOINT 2: Download notizie da Alpaca per il periodo
# ------------------------------------------------------------------
@data_bp.route("/news", methods=["GET"])
def get_news():
    """
    Parametri GET:
      - symbol : ticker o nome asset (es. 'GC=F', 'AAPL')
      - start  : data inizio formato YYYY-MM-DD
      - end    : data fine formato YYYY-MM-DD
      - limit  : numero massimo di notizie (default 20)
    
    Restituisce:
      JSON con array di notizie: [{date, headline, summary, url, source}, ...]
    """
    symbol = request.args.get("symbol", "GC=F")
    start  = request.args.get("start", "")
    end    = request.args.get("end", "")
    limit  = int(request.args.get("limit", 2000))
    # Forza un check: se il limite è stato cachato o è troppo basso per stock "rumorosi" (es AAPL), alzalo
    if limit < 2000:
        limit = 2000

    ticker = resolve_ticker(symbol)
    symbol_lower = symbol.strip().lower()
    
    # Importiamo la mappa proxy per permettere di reperire notizie per futs/indici
    try:
        from agents.alpaca_news_tool import ALPACA_PROXY_MAP
        if symbol_lower in ALPACA_PROXY_MAP:
            proxy = ALPACA_PROXY_MAP[symbol_lower]
            # La mappa restituisce liste; NewsRequest.symbols vuole stringa CSV
            alpaca_symbol = ",".join(proxy) if isinstance(proxy, list) else proxy
        else:
            alpaca_symbol = ticker.split("=")[0].split("-")[0].replace("^", "").upper()
    except Exception:
        alpaca_symbol = ticker.split("=")[0].split("-")[0].replace("^", "").upper()

    logger.info(f"[NEWS API] Notizie per {alpaca_symbol} ({start} → {end})")

    try:
        import Calibrazione
        from alpaca.data.historical.news import NewsClient
        from alpaca.data.requests import NewsRequest

        if not Calibrazione.ALPACA_API_KEY or not Calibrazione.ALPACA_SECRET_KEY:
            return jsonify({"error": "Chiavi API Alpaca non configurate"}), 503

        client = NewsClient(
            api_key=Calibrazione.ALPACA_API_KEY,
            secret_key=Calibrazione.ALPACA_SECRET_KEY
        )

        # Alpaca richiede formato ISO8601
        start_iso = f"{start}T00:00:00Z" if start else None
        end_iso   = f"{end}T23:59:59Z"   if end   else None

        params = NewsRequest(
            symbols=alpaca_symbol,
            start=start_iso,
            end=end_iso,
            limit=limit
        )
        response = client.get_news(params)
        articles = response.data.get("news", [])

        news_list = []
        for art in articles:
            # Troviamo il timestamp UNIX per posizionare la notizia sul grafico
            dt = art.created_at
            news_list.append({
                "time":     int(dt.timestamp()),
                "date":     dt.strftime("%Y-%m-%d"),
                "headline": art.headline,
                "summary":  getattr(art, "summary", ""),
                "url":      art.url,
                "source":   art.source,
                "symbols":  getattr(art, "symbols", []),
                "provider": "alpaca"
            })

        # --- Integrazione DuckDuckGo ---
        try:
            from ddgs import DDGS
            import dateutil.parser
            
            # Troviamo un nome più "umano" per la ricerca web
            alias_name = symbol
            for k, v in ASSET_ALIASES.items():
                if v == ticker:
                    alias_name = k.capitalize()
                    break

            ddg_limit = getattr(Calibrazione, "DUCKDUCKGO_NEWS_LIMIT", limit)
            search_query = f"{alias_name} finance news"
            ddgs_client = DDGS()
            
            try:
                # Cerchiamo le notizie
                ddgs_news = list(ddgs_client.news(search_query, max_results=ddg_limit))
                if not ddgs_news:
                    raise Exception("0 risultati da DDGS")

                for article in ddgs_news:
                    try:
                        dt = dateutil.parser.parse(article.get('date', ''))
                        news_list.append({
                            "time":     int(dt.timestamp()),
                            "date":     dt.strftime("%Y-%m-%d"),
                            "headline": article.get('title', ''),
                            "summary":  article.get('body', ''),
                            "url":      article.get('url', ''),
                            "source":   article.get('source', 'DuckDuckGo'),
                            "symbols":  [symbol],
                            "provider": "duckduckgo"
                        })
                    except Exception as e_date:
                        logger.debug(f"[NEWS API] Errore parsing data notizie DDG: {e_date}")
            except Exception as search_e:
                logger.debug(f"[NEWS API] DDGS news non disponibile ({type(search_e).__name__}), uso fallback web HTML...")
                # Fallback Scraping su HTML DuckDuckGo
                import requests
                from bs4 import BeautifulSoup
                from datetime import datetime
                
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
                res = requests.get("https://html.duckduckgo.com/html/", params={"q": search_query}, headers=headers, timeout=10)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, 'html.parser')
                    results = soup.find_all('div', class_='result')
                    count = 0
                    for r in results:
                        if count >= ddg_limit: break
                        a_tag = r.find('a', class_='result__url')
                        title_tag = r.find('a', class_='result__snippet') or a_tag
                        snippet_tag = r.find('a', class_='result__snippet')
                        
                        if a_tag and title_tag:
                            href = a_tag.get('href', '')
                            # Pulizia URL: estraiamo l'URL reale dal redirect di DDG (parametro uddg)
                            final_url = href
                            if "uddg=" in href:
                                try:
                                    from urllib.parse import urlparse, parse_qs, unquote
                                    parsed = urlparse(href)
                                    qs = parse_qs(parsed.query)
                                    if 'uddg' in qs:
                                        final_url = unquote(qs['uddg'][0])
                                except:
                                    pass

                            # Mappa la notizia DDG alla data di fine grafico per posizionamento visivo
                            target_dt = datetime.now()
                            if end:
                                try:
                                    target_dt = datetime.strptime(end, "%Y-%m-%d")
                                except:
                                    pass
                            
                            news_list.append({
                                "time": int(target_dt.timestamp()),
                                "date": target_dt.strftime("%Y-%m-%d"),
                                "headline": title_tag.text.strip(),
                                "summary": snippet_tag.text.strip() if snippet_tag else "",
                                "url": final_url,
                                "source": "DuckDuckGo Web",
                                "symbols": [symbol],
                                "provider": "duckduckgo"
                            })
                            count += 1
                else:
                    logger.warning(f"[NEWS API] Fallback DDG HTML ritornato {res.status_code}")
        except Exception as e_ddg_tot:
             logger.warning(f"[NEWS API] Libreria DDG o richieste fallite: {e_ddg_tot}")
        # -------------------------------

        logger.success(f"[NEWS API] {len(news_list)} notizie totali trovate per {alpaca_symbol}")
        return jsonify({
            "symbol":    alpaca_symbol,
            "news":      news_list,
            "total":     len(news_list)
        })

    except Exception as e:
        logger.error(f"[NEWS API] Errore: {e}")
        return jsonify({"news": [], "error": str(e), "total": 0})


# ------------------------------------------------------------------
# ENDPOINT 3: Ricerca simbolo (autocompletamento)
# ------------------------------------------------------------------
@data_bp.route("/search", methods=["GET"])
def search_symbol():
    """
    Parametri GET:
      - q : query di ricerca (es. 'oro', 'apple', 'GC')
    
    Restituisce lista di asset che corrispondono alla query.
    """
    query = request.args.get("q", "").lower()
    results = []
    for alias, ticker in ASSET_ALIASES.items():
        if query in alias or query in ticker.lower():
            results.append({"name": alias.title(), "ticker": ticker})

    # Deduplicazione per ticker
    seen = set()
    unique = []
    for r in results:
        if r["ticker"] not in seen:
            seen.add(r["ticker"])
            unique.append(r)

    return jsonify({"results": unique[:10]})


# ------------------------------------------------------------------
# ENDPOINT 4: Dati Calibrazione correnti
# ------------------------------------------------------------------
@data_bp.route("/calibrazione", methods=["GET"])
def get_calibrazione():
    """
    Restituisce i parametri correnti di Calibrazione.py come JSON.
    Usato dall'interfaccia per pre-popolare i controlli di calibrazione.
    """
    try:
        import Calibrazione
        return jsonify({
            "LLM_PROVIDER":             Calibrazione.LLM_PROVIDER,
            "DEFAULT_PROJECTION_DAYS":  Calibrazione.DEFAULT_PROJECTION_DAYS,
            "ALPACA_NEWS_LIMIT":        Calibrazione.ALPACA_NEWS_LIMIT,
            "DUCKDUCKGO_NEWS_LIMIT":    Calibrazione.DUCKDUCKGO_NEWS_LIMIT,
            "AGENT_MACRO_ENABLED":      Calibrazione.AGENT_MACRO_ENABLED,
            "AGENT_PATTERN_ENABLED":    Calibrazione.AGENT_PATTERN_ENABLED,
            "AGENT_TREND_ENABLED":      Calibrazione.AGENT_TREND_ENABLED,
            "AGENT_SR_ENABLED":         Calibrazione.AGENT_SR_ENABLED,
            "AGENT_VOLUME_ENABLED":     Calibrazione.AGENT_VOLUME_ENABLED,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
