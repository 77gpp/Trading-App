from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import NewsRequest
from datetime import datetime, timedelta
import Calibrazione
from loguru import logger

def get_alpaca_news(symbol: str, start: str = None, end: str = None) -> str:
    """
    Ottiene le notizie finanziarie ufficiali per un determinato simbolo in un periodo specifico.
    
    Args:
        symbol (str): Il simbolo dell'asset da cercare.
        start (str, optional): Data inizio ISO (YYYY-MM-DD). Default: oggi - MACRO_ANALYSIS_DAYS.
        end (str, optional): Data fine ISO (YYYY-MM-DD). Default: oggi.
        
    Returns:
        str: Una stringa formattata con i titoli delle notizie e i link alle fonti.
    """
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
            # Se la stringa è solo data YYYY-MM-DD, aggiungiamo l'ora
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
        
        logger.info(f"[ALPACA TOOL] Ricerca news per {symbol} nel periodo {start_dt_str} -> {end_dt_str}...")
        
        request_params = NewsRequest(
            symbols=symbol,
            start=start_dt_str,
            end=end_dt_str,
            limit=getattr(Calibrazione, "ALPACA_NEWS_LIMIT", 15)
        )
        
        news_response = client.get_news(request_params)
        
        articles = news_response.data.get('news', [])
        
        if not articles:
            return f"Nessuna notizia ufficiale trovata su Alpaca per {symbol} nel periodo indicato ({start_dt_str} -> {end_dt_str})."
        
        formatted_news = [f"### Notizie Alpaca Markets per {symbol}:"]
        for article in articles:
            # Creiamo un formato leggibile per l'agente
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
