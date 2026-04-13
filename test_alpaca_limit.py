import sys
sys.path.append("/Users/gpp/Programmazione/Trading/In lavorazione/Trading_AI_App v2")
from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import NewsRequest
import Calibrazione

client = NewsClient(
    api_key=Calibrazione.ALPACA_API_KEY, 
    secret_key=Calibrazione.ALPACA_SECRET_KEY
)

req = NewsRequest(
    symbols="AAPL",
    start="2024-01-01T00:00:00Z",
    end="2024-06-01T00:00:00Z",
    limit=5000
)
res = client.get_news(req)
news_list = res.data.get('news', [])
print("With limit=5000, number of news returned in first response:", len(news_list))
if hasattr(res, 'next_page_token') and res.next_page_token:
    print("Has next_page_token:", res.next_page_token)
