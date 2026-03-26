import pandas as pd
import numpy as np

class DataFetcher:
    """
    Simula lo scaricamento di dati finanziari Multi-Timeframe.
    Fornisce dati per 1h, 4h e 1d in modo che siano coerenti tra loro.
    """
    
    @staticmethod
    def get_mtf_data(ticker="AAPL", days=100):
        print(f"[DATA FETCHER] Recupero dati Multi-Timeframe per {ticker}...")
        
        # 1. Dati Giornalieri (1d)
        df_1d = DataFetcher._generate_mock_data(ticker, days, freq='D')
        
        # 2. Dati 4 Ore (4h) - Approssimiamo a 6 candele al giorno (per simulazione)
        df_4h = DataFetcher._generate_mock_data(ticker, days * 6, freq='4h')
        
        # 3. Dati 1 Ora (1h) - 24 candele al giorno
        df_1h = DataFetcher._generate_mock_data(ticker, days * 24, freq='h')
        
        print(f"[DATA FETCHER] Scaricati dati MTF (1h, 4h, 1d) per {ticker}.")
        return {
            "1h": df_1h,
            "4h": df_4h,
            "1d": df_1d
        }

    @staticmethod
    def _generate_mock_data(ticker, count, freq='D'):
        """Generatore interno di dati OHLCV simulati."""
        chiusure = np.random.normal(loc=0, scale=3, size=count).cumsum() + 150
        aperture = chiusure - (np.random.normal(0, 1.5, size=count))
        alti = np.maximum(aperture, chiusure) + np.abs(np.random.normal(0, 2, size=count))
        bassi = np.minimum(aperture, chiusure) - np.abs(np.random.normal(0, 2, size=count))
        volumi = np.random.randint(1000000, 5000000, size=count)
        
        df = pd.DataFrame({
            'Date': pd.date_range(end=pd.Timestamp.today(), periods=count, freq=freq),
            'Open': aperture,
            'High': alti,
            'Low': bassi,
            'Close': chiusure,
            'Volume': volumi
        })
        return df

if __name__ == "__main__":
    fetcher = DataFetcher()
    data = fetcher.get_mtf_data("EUR/USD", days=10)
    print("Ultimi dati 1d:")
    print(data["1d"].tail())
    print("\nUltimi dati 1h:")
    print(data["1h"].tail(24))
