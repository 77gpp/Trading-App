# BEST PRACTICE: Appunti e Benchmarking per Analisi di Mercato

Questo documento raccoglie le metodologie utilizzate dai trader professionisti e istituzionali. Serve come riferimento (benchmark) per valutare e migliorare le analisi prodotte dal nostro Trading Desk AI.

---

## 🌎 1. Approccio Macro (Dall'alto verso il basso)
I professionisti iniziano sempre dalla "Grande Foto".

*   **Driver primario**: Tassi di interesse e decisioni delle Banche Centrali.
*   **Correlazioni chiave**: Monitorare sempre il **DXY (Dollar Index)**. Se il dollaro è forte, l'oro e le azioni solitamente soffrono.
*   **Sentiment**: Verificare se siamo in una fase di "Risk-On" (ottimismo, si comprano azioni e crypto) o "Risk-Off" (paura, si compra oro e valute rifugio come lo Yen).

## 📊 2. Analisi Tecnica e Volumetrica (Il cuore operativo)
Il prezzo è mosso dai soldi, e i soldi si vedono nei volumi.

*   **Priorità ai Volumi (VSA/Wyckoff)**: Mai fidarsi di una rottura di prezzo se non è accompagnata da un aumento significativo dei volumi. Cercare "Sforzo vs Risultato".
*   **Struttura di Mercato**: Identificare se siamo in un Trend (prezzi che fanno massimi e minimi crescenti) o in un Range.
*   **Pattern Candlestick (Steve Nison)**: Usare le candele (es. Hammer, Engulfing) solo come conferma finale su livelli chiave di supporto o resistenza.

## 🏁 3. Benchmark per Tipologia di Mercato

| Mercato | Focus Primario | Strumento Consigliato |
| :--- | :--- | :--- |
| **Forex** | News Macro e Tassi | `DuckDuckGo` + `Macro Library` |
| **Commodities (Oro)** | Geopolitica e Inflazione | `VSA (Volume Analysis)` |
| **Azioni** | Bilanci e Crescita Settore | `YFinance` (Analyst Recs) |
| **Crypto** | Momentum e On-Chain | `Technical Indicators` |

---

## 🛠️ Come usare questo file
Ogni volta che il **Supervisor** genera un report, confrontalo con questi punti:
1.  L'analisi ha considerato il sentiment macro?
2.  I volumi confermano il movimento dei prezzi?
3.  Il verdetto finale tiene conto del contesto di mercato descritto qui?

---
*Documento creato il 26/03/2026 come parte dell'evoluzione V5.2 del Trading AI Desk.*
