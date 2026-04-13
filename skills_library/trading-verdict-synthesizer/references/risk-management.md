# Risk Management — Regole Professionali

## Indice
1. [Principi Fondamentali](#1-principi-fondamentali)
2. [Position Sizing](#2-position-sizing)
3. [Stop Loss Methodology](#3-stop-loss-methodology)
4. [Take Profit e Gestione della Posizione](#4-take-profit-e-gestione-della-posizione)
5. [Risk:Reward — Calcolo e Soglie Minime](#5-riskreward--calcolo-e-soglie-minime)
6. [Drawdown Limits](#6-drawdown-limits)

---

## 1. Principi Fondamentali

**La preservazione del capitale è priorità assoluta sul profitto.**

Un trader professionista sopravvive perdendo bene, non vincendo spesso. La asimmetria è il vantaggio: rischi 1 per guadagnare 2-3. Nel tempo, anche con un win rate del 40%, questa asimmetria genera rendimenti consistenti.

**Regole cardinali**:
- Non rischiare mai più dell'1-2% del capitale totale su un singolo trade
- Non aprire mai una posizione senza avere già definito entry, stop e target
- Lo stop loss non si sposta MAI nella direzione sfavorevole (trailing stop solo in favore)
- Un trade senza stop è speculazione, non trading professionale

---

## 2. Position Sizing

### Formula Base
```
Size = (Capitale × Rischio%) / (Entry - Stop Loss)
```

**Esempio pratico (Gold GC=F)**:
- Capitale: $100.000
- Rischio per trade: 1% → $1.000
- Entry: $3.250
- Stop Loss: $3.210 (distanza: $40)
- Size = $1.000 / $40 = 25 contratti (o unità)

### Scala di Rischio per Qualità del Setup

| Score Confluenza | Rischio max per trade |
|------------------|----------------------|
| 8-10 (eccellente) | 2% del capitale |
| 5-7 (buono) | 1% del capitale |
| 3-4 (marginale) | 0.5% del capitale |
| < 3 | NO TRADE |

### Fattori che Riducono la Size
- Correlazione tra posizioni aperte: riduci del 50% se hai già un trade nella stessa direzione
- Volatilità elevata (ATR > 2× media storica): riduci del 30-50%
- News macro imminenti (Fed, CPI, NFP): riduci del 50% o chiudi prima
- Post-drawdown (hai perso > 5% nella settimana): riduci del 50% fino al recupero

---

## 3. Stop Loss Methodology

### Gerarchia dei Metodi (priorità decrescente)

**1. Stop Strutturale** (metodo preferito dai professionisti)
Posizionato oltre il livello che, se violato, invalida completamente la tesi del trade.
- Long: sotto il minimo dello swing HL che ha confermato l'uptrend, o sotto la demand zone
- Short: sopra il massimo dello swing LH che ha confermato il downtrend, o sopra la supply zone
- Vantaggio: logico, difendibile, basato sulla struttura reale del mercato

**2. Stop da Order Block (ICT)**
- Long: appena sotto il bullish order block di entry (ultima candela bearish prima dell'impulso rialzista)
- Short: appena sopra il bearish order block di entry
- Razionale: se il prezzo ritorna nell'order block e lo chiude, l'istituzione ha abbandonato quella zona

**3. Stop ATR-Based** (complementare, non sostitutivo)
- Stop = Entry ± (1.5 × ATR_14)
- Usato quando lo stop strutturale è troppo vicino (< 0.5 ATR) e rischia whipsaw
- Usato per commodity con alta volatilità giornaliera

**4. Stop da Wyckoff**
- Long dopo Spring: stop sotto il minimo dello Spring
- Short dopo Upthrust: stop sopra il massimo dell'Upthrust
- Razionale: se quei livelli vengono violati, la narrativa Wyckoff è invalidata

### Regola del Buffer
Aggiungi sempre un buffer al di là dello stop strutturale per evitare di essere stoppato da spike di liquidità:
- Forex/Futures: 5-10 pips / tick oltre il livello
- Commodity (Gold): $3-8 oltre il livello strutturale
- Non troppo ampio: se il buffer porta il R:R sotto 1:2, ricerca un entry migliore

---

## 4. Take Profit e Gestione della Posizione

### Strategia di Uscita a Livelli Multipli

**A Target 1 (TP1)**:
- Chiudi il 50-60% della posizione
- Sposta lo stop al breakeven (entry price + piccolo buffer per le commissioni)
- Motivo: blocchi il profitto, elimini il rischio sul trade, lasci correre parte del trade

**A Target 2 (TP2)**:
- Chiudi un altro 30% della posizione
- Sposta lo stop a TP1 (trailing)
- Motivo: cattura il move ampio mantenendo protezione

**Posizione residua (10-20%)**:
- Trailing stop basato su struttura (ogni nuovo HL in uptrend = sposta stop sotto il nuovo HL)
- Chiudi se il prezzo non fa nuovi massimi/minimi in 3-5 sessioni
- Motivo: lascia correre i winner eccezionali senza sacrificare il profitto già acquisito

### Uscita Anticipata (Exit Management)
Considera di uscire prima dello stop o del target se:
- Volume dramatically decreasing approaching target (mancanza di momentum)
- Pattern di inversione forte sul timeframe 4H contro il trade aperto
- Macro news inaspettato che cambia il bias fondamentale
- Prezzo raggiunge zona di fortissima resistenza/supporto istituzionale non identificata in precedenza

---

## 5. Risk:Reward — Calcolo e Soglie Minime

### Formula
```
R:R = (TP1 - Entry) / (Entry - Stop Loss)    [per long]
R:R = (Entry - TP1) / (Stop Loss - Entry)    [per short]
```

### Soglie Minime per Apertura del Trade

| Tipo di Trade | R:R Minimo | Note |
|--------------|------------|------|
| Trade standard | 1:2 | Soglia professionale universale |
| Setup ad alta confluenza (score 8+) | 1:1.5 | Solo se rischio molto definito e strutturale |
| Counter-trend | 1:3 | Richiede confluenza eccezionale |
| Scalp/Day trade | 1:1.5 | Solo se win rate atteso > 60% |
| NO TRADE | < 1:1.5 | Indipendentemente dalla qualità del setup |

### Perché 1:2 è il Minimo
Con un R:R di 1:2 puoi perdere il 60% dei trade e restare in pareggio.
Con un win rate realistico del 45-55% per setup di qualità media, un R:R di 1:2 produce rendimenti positivi nel lungo periodo.

**La matematica non mente**: un sistema con win rate 40% e R:R 1:2.5 rende il +20% netto. Un sistema con win rate 60% e R:R 1:1 rende il +20% netto. Ma il secondo richiede uno sforzo molto maggiore per mantenere quel win rate.

---

## 6. Drawdown Limits

### Regole di Protezione del Capitale

**Daily Loss Limit**: se perdi il 3% del capitale in un giorno, STOP. Non aprire altri trade fino al giorno successivo. La mente in perdita prende decisioni sub-ottimali.

**Weekly Loss Limit**: se perdi il 5% nella settimana, riduci la size al 50% per la settimana successiva.

**Monthly Loss Limit**: se perdi il 10% nel mese, fermati per una settimana. Rivedi la strategia. Non è un mercato favorevole o stai facendo qualcosa di sbagliato.

**Maximum Drawdown**: oltre il 20% dal peak, stop totale alle attività e revisione completa del sistema.

### Correlazione tra Trade
Non aprire mai 3+ trade nella stessa direzione in asset correlati (es. Gold long + Silver long + DXY short = stesso trade, triplicato il rischio reale).

Calcola sempre il rischio aggregato del portafoglio, non solo il rischio del singolo trade.
