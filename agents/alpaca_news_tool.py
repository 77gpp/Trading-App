from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import NewsRequest
from datetime import datetime, timedelta
import Calibrazione
from loguru import logger

def get_alpaca_news(symbol: str) -> str:
    """
    Ottiene le ultime 5 notizie finanziarie ufficiali per un determinato simbolo (es. 'AAPL', 'GC=F', 'BTC/USD') da Alpaca Markets News API.
    
    Args:
        symbol (str): Il simbolo dell'asset da cercare.
        
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
        
        # Calcoliamo il periodo di ricerca basandoci sulla calibrazione
        days_back = getattr(Calibrazione, "MACRO_ANALYSIS_DAYS", 10)
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        logger.info(f"[ALPACA TOOL] Ricerca news per {symbol} negli ultimi {days_back} giorni...")
        
        request_params = NewsRequest(
            symbols=symbol,
            start=start_date,
            limit=getattr(Calibrazione, "ALPACA_NEWS_LIMIT", 15)
        )
        
        news_response = client.get_news(request_params)
        
        articles = news_response.data.get('news', [])
        
        if not articles:
            return f"Nessuna notizia ufficiale trovata su Alpaca per {symbol} negli ultimi {days_back} giorni."
        
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
