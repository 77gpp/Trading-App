import sys
import os

from loguru import logger
from data_fetcher import DataFetcher
from agents.supervisor_agent import SupervisorAgent

def main():
    print("="*60)
    print(" 🚀 AVVIO TRADING AI APP - SISTEMA AGENTIC (Skills + Gemini File API) 🚀")
    print("="*60)
    
    # 1. Acquisizione Dati (Mock o Futuro API Reale come YFinance)
    ticker = "APPLE (AAPL)"
    try:
        df_mercato = DataFetcher.get_historical_data(ticker, period_days=300)
    except Exception as e:
        logger.error(f"Errore nello scaricamento dei dati: {e}")
        sys.exit(1)
        
    # 2. Inizializzazione del Cervello (L'Agente Orchestratore)
    supervisore = SupervisorAgent()
    
    # 3. L'Orchestratore esegue l'analisi
    # In futuro utilizzerà le nuove Skill estratte via Agentic File Search
    report_definitivo = supervisore.analizza_asset(df_mercato, ticker, autore="joe_ross")
    
    # 4. Output a schermo (Futuro: output sulla Web App React/HTML)
    print(report_definitivo)
    
    print("\n[APP] Analisi completata con successo. Attesa nuovo input...")

if __name__ == "__main__":
    main()
