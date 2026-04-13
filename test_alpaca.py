import sys
import os

# Add project root to path
project_root = "/Users/gpp/Programmazione/Trading/In lavorazione/Trading_AI_App v2"
sys.path.append(project_root)

# Setup virtual environment path
venv_python = os.path.join(project_root, ".venv/bin/python")

from agents.alpaca_news_tool import get_alpaca_news
from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import NewsRequest
import Calibrazione

try:
    client = NewsClient(
        api_key=Calibrazione.ALPACA_API_KEY, 
        secret_key=Calibrazione.ALPACA_SECRET_KEY
    )

    req = NewsRequest(
        symbols="AAPL",
        start="2024-01-01T00:00:00Z",
        end="2024-06-01T00:00:00Z",
        limit=50
    )
    res = client.get_news(req)
    print("--- RAW API RESPONSE ATTRIBUTES ---")
    print(dir(res))
    
    print("\n--- Testing Data Structure ---")
    if hasattr(res, 'news'):
        print(f"res.news exists: list of {len(res.news)} elements")
    if hasattr(res, 'data'):
        print(f"res.data exists, keys: {res.data.keys() if isinstance(res.data, dict) else 'not a dict'}")
        if isinstance(res.data, dict) and 'news' in res.data:
            print(f"res.data['news'] has {len(res.data['news'])} elements")
            
    print("\n--- Testing wrapper function ---")
    output = get_alpaca_news("AAPL", start="2024-01-01", end="2024-06-01")
    lines = output.splitlines()
    print(f"Wrapper output lines: {len(lines)}")
    if lines and len(lines) > 0:
        print("First 3 lines of output:")
        for line in lines[:3]:
            print(f"> {line}")
            
except Exception as e:
    print(f"Error occurred: {e}")
