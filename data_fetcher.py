import pandas as pd
import numpy as np

class DataFetcher:
    """
    Simula lo scaricamento di dati finanziari (es. da Yahoo Finance).
    Nella versione di produzione finale, questo componente userà 'yfinance' o 'ccxt'.
    Per la fase di sviluppo architetturale, genera candele coerenti.
    """
    
    @staticmethod
    def get_historical_data(ticker="AAPL", period_days=250):
        print(f"[DATA FETCHER] Collegamento all'Exchange simulato per {ticker}...")
        
        # Generazione Random Walk (Passeggiata Aleatoria) realistica
        chiusure = np.random.normal(loc=0, scale=3, size=period_days).cumsum() + 150
        aperture = chiusure - (np.random.normal(0, 1.5, size=period_days))
        alti = np.maximum(aperture, chiusure) + np.abs(np.random.normal(0, 2, size=period_days))
        bassi = np.minimum(aperture, chiusure) - np.abs(np.random.normal(0, 2, size=period_days))
        volumi = np.random.randint(1000000, 5000000, size=period_days)
        
        df = pd.DataFrame({
            'Date': pd.date_range(end=pd.Timestamp.today(), periods=period_days),
            'Open': aperture,
            'High': alti,
            'Low': bassi,
            'Close': chiusure,
            'Volume': volumi
        })
        
        print(f"[DATA FETCHER] Scaricati {period_days} giorni di dati per {ticker}.")
        return df

if __name__ == "__main__":
    df = DataFetcher.get_historical_data("EUR/USD")
    print(df.tail())
