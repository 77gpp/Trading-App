import pandas as pd
import yfinance as yf
from loguru import logger

class DataFetcher:
    """
    Recupera dati finanziari reali tramite Yahoo Finance.
    Fornisce dati Multi-Timeframe (1h, 4h, 1d).
    """
    
    @staticmethod
    def get_mtf_data(ticker="GC=F", days=60):
        """
        Scarica dati OHLCV reali per diversi timeframe.
        ticker: Simbolo Yahoo Finance (es. GC=F per Oro, XAUUSD=X per Spot)
        days: Numero di giorni di storico
        """
        logger.info(f"[DATA FETCHER] Download dati reali per {ticker} ({days} giorni)...")
        
        try:
            # 1. Dati Giornalieri (1d)
            df_1d = yf.download(ticker, period=f"{days}d", interval="1d")
            
            # 2. Dati Orari (1h) - Necessari per 1h e per costruire il 4h
            # Nota: yfinance limita lo storico orario a 730 giorni
            df_1h_raw = yf.download(ticker, period="60d", interval="1h")
            
            if df_1d.empty or df_1h_raw.empty:
                raise ValueError(f"Dati non trovati per il ticker {ticker}")

            # pulizia nomi colonne (yfinance a volte ritorna MultiIndex)
            if isinstance(df_1d.columns, pd.MultiIndex):
                df_1d.columns = df_1d.columns.get_level_values(0)
            if isinstance(df_1h_raw.columns, pd.MultiIndex):
                df_1h_raw.columns = df_1h_raw.columns.get_level_values(0)

            # 3. Costruzione Dati 4 Ore (4h) tramite resampling dei dati 1h
            df_4h = df_1h_raw.resample('4h').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }).dropna()

            logger.success(f"[DATA FETCHER] Download completato per {ticker}.")
            
            return {
                "1h": df_1h_raw.tail(100), # Ultime 100 candele per analisi tecnica
                "4h": df_4h.tail(100),
                "1d": df_1d.tail(60)
            }
            
        except Exception as e:
            logger.error(f"Errore durante il download dei dati: {e}")
            raise e

if __name__ == "__main__":
    # Test rapido
    fetcher = DataFetcher()
    try:
        data = fetcher.get_mtf_data("GC=F", days=10)
        print("\n--- TEST DATA FETCHER (ORO) ---")
        print(f"Candele 1d: {len(data['1d'])}")
        print(f"Candele 4h: {len(data['4h'])}")
        print(f"Candele 1h: {len(data['1h'])}")
        print("\nUltimi prezzi 1d:")
        print(data["1d"].tail())
    except Exception as e:
        print(f"Test fallito: {e}")
