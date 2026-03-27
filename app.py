import sys
import os

from loguru import logger
from data_fetcher import DataFetcher
from agents.supervisor_agent import SupervisorAgent

def main():
    print("="*60)
    print(" 🚀 AVVIO TRADING AI APP - CONFIGURABLE AGNO DESK (V5) 🚀")
    print("="*60)
    
    # 1. Acquisizione Dati Multi-Timeframe (1h, 4h, 1d)
    ticker = "GC=F"
    try:
        data_mtf = DataFetcher.get_mtf_data(ticker, days=100)
    except Exception as e:
        logger.error(f"Errore nello scaricamento dei dati MTF: {e}")
        sys.exit(1)
        
    # 2. Inizializzazione del Cervello (Orchestratore Dinamico V5)
    supervisore = SupervisorAgent()
    
    # 3. L'Orchestratore esegue l'analisi (Macro + Technical Team)
    report_definitivo = supervisore.analizza_asset(data_mtf, ticker)
    
    # 4. Output del Report Professionale
    print(report_definitivo)
    
    print("\n[APP] Analisi Agno V5 (Configurabile) completata con successo.")

if __name__ == "__main__":
    main()
