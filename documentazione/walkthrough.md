# WALKTHROUGH: Trading AI Desk V5 (Agno - Configurable)

Congratulazioni! Il tuo sistema di trading IA è stato elevato a un'architettura **multi-agente professionale** basata sul framework **Agno v2.x**.

## 🚀 Novità Principali della V5

### 1. Cuore Agno (Ex Phidata)
Abbiamo abbandonato gli script asincroni manuali per adottare le classi `Agent` e `Team` di Agno. Questo garantisce:
*   **Ragionamento Coordinato**: Gli specialisti (Pattern, Trend, S/R, Volumi) lavorano ora in un vero **Trading Desk** sotto un capo-team.
*   **Memoria Nativa**: Ogni analisi viene ricordata grazie alla persistenza SQLite.

### 2. Configurazione "Settings-First"
Tutto il sistema si controlla ora dal file **[settings.py](file:///Users/gpp/Programmazione/Trading/In%20Lavorazione/Trading_AI_App%20v2/settings.py)**:
*   **Modelli Dinamici**: Puoi cambiare al volo tra `gemini-2.0-flash` (veloce/economico) e `gemini-1.5-pro` (profondo) senza toccare il codice degli agenti.
*   **Percorsi Locali**: I tuoi libri (`data/books`) e le skill sono centralizzati e facilmente accessibili.

### 3. Diagnostica e Stabilità
È stato risolto ogni problema tecnico legato agli aggiornamenti delle librerie:
*   **Google GenAI**: Integrato il nuovo SDK ufficiale di Google.
*   **Memory SQLite**: Configurato `SqliteDb` per salvare le sessioni sul tuo Mac in `storage/memory/`.

---

## 🛠️ Come Utilizzare il Sistema

1.  **Avvio Analisi**: Usa il comando `python3 app.py`.
2.  **Scelta Asset**: Cambia il `ticker` in `app.py` (es. "XAU/USD" per l'oro).
3.  **Monitoraggio**: Controlla i log colorati (Loguru) per vedere gli agenti che dialogano in tempo reale.

> [!TIP]
> **Errore Quota (429)**: Se ricevi un errore di quota, significa che hai raggiunto il limite giornaliero gratuito di Google. Google resetta questi limiti ogni giorno (o dopo pochi minuti per le sessioni brevi).

---

## ✅ Verifiche Effettuate
*   **Mappatura Modelli**: Identificato l'ID corretto `gemini-2.0-flash` tramite lo script di diagnostica dedicato.
*   **Inizializzazione**: Verificato il caricamento dei database e dei percorsi libreria.
*   **Integrazione**: Il `SupervisorAgent` orchestra ora correttamente il nuovo `AgnoMacroExpert` e il `AgnoTechnicalTeam`.

---
Il tuo Trading Desk è ora pronto per sfidare i mercati con l'intelligenza di Agno!
