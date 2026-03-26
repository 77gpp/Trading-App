# MASTER FILE: COMPETENZE MACROECONOMICHE GLOBALI (V2)

Questo documento contiene le logiche di analisi per l'Agente Macro dell'IA di Trading. Ogni sezione include la descrizione del fenomeno e la logica tecnica per l'interpretazione.

---

## SEZIONE 1: INDICATORI ECONOMICI E SALUTE DELL'ECONOMIA

### 1.1 Prodotto Interno Lordo (PIL / GDP)
**Descrizione:** Misura la produzione totale di beni e servizi in un paese. È l'indicatore definitivo della crescita economica.
**Logica Tecnica/Pseudocodice:**
- SE GDP_Attuale > GDP_Precedente AND GDP_Attuale > Consensus:
    - Segnale di forza economica (Bullish per Azionario, Bullish per la Valuta del paese).
- SE GDP_Attuale < GDP_Precedente per 2 trimestri consecutivi:
    - Definizione Tecnica di **RECESSIONE**. (Bearish per Azionario, Bearish per la Valuta, Bullish per Gold/Bonds).

### 1.2 Inflazione (CPI / PCE)
**Descrizione:** Misura l'aumento dei prezzi. Le banche centrali (FED, BCE) hanno un obiettivo tipico del 2%.
**Logica Tecnica/Pseudocodice:**
- SE CPI > Consensus AND Trend == Rialzista:
    - Rischio surriscaldamento economia. 
    - ASPETTATIVA: Rialzo dei tassi da parte della Banca Centrale.
    - IMPATTO: Bullish per il Dollaro (DXY), Bearish per l'Oro, Bearish per le Azioni Growth.
- SE CPI < Consensus AND Trend == Ribassista:
    - Rischio deflazione. Segnale di debolezza.

### 1.3 Occupazione (Non-Farm Payrolls - NFP)
**Descrizione:** Numero di posti di lavoro creati negli USA (escluso il settore agricolo).
**Logica Tecnica/Pseudocodice:**
- SE NFP > Consensus AND Tasso_Disoccupazione < 4%:
    - Mercato del lavoro "stretto" (Tight). Bullish per il Dollaro.
    - SE NFP < Consensus: Segnale di possibile raffreddamento economico.

---

## SEZIONE 2: POLITICA MONETARIA E BANCHE CENTRALI

### 2.1 Tassi d'Interesse (Fed Funds Rate)
**Descrizione:** Il costo del denaro stabilito dalla Federal Reserve.
**Logica Tecnica/Pseudocodice:**
- SE Banca_Centrale == "Hawkish" (Aggressiva nel rialzo tassi):
    - DXY (Dollaro) tende a salire. Rendimenti Bond tendono a salire.
- SE Banca_Centrale == "Dovish" (Propensa al taglio tassi):
    - DXY tende a scendere. Azionario (specie Tech) tende a salire.

### 2.2 Dot Plot e Forward Guidance
**Descrizione:** Le proiezioni dei membri della FED sui futuri livelli dei tassi.
**Logica:** Uno spostamento verso l'alto dei "pallini" (dots) nel grafico Dot Plot indica aspettative di tassi più alti per un periodo più lungo.

---

## SEZIONE 3: FORZA DEL DOLLARO (US DOLLAR INDEX - DXY)

### 3.1 Il Dollaro come "Safe Haven" (Bene Rifugio)
**Descrizione:** In periodi di incertezza geopolitica o crolli dell'azionario, gli investitori vendono asset rischiosi e comprano Dollari.
**Logica:**
- SE VIX (Indice della Paura) > 25 AND Azionario < Media 50gg:
    - CORRELAZIONE: DXY Sale (Apprezzamento come rifugio).

### 3.2 Correlazione Inversa con le Commodities (Oil/Gold)
**Descrizione:** Poiché le materie prime sono prezzate in Dollari, un Dollaro forte le rende più care per chi usa altre valute, abbassandone la domanda.
**Logica:**
- SE DXY == Trend_Rialzista_Chiaro:
    - ASPETTATIVA: Petrolio (WTI) e Oro (XAU) tenderanno a trovare resistenza o a scendere.

### 3.3 Differenziale nei Rendimenti (Yield Spreads)
**Descrizione:** Il Dollaro si rafforza se i rendimenti dei titoli di stato USA (Treasury) sono molto più alti di quelli europei (Bund) o giapponesi (JGB).

---

## SEZIONE 4: MERCATI ENERGETICI E GEOPOLITICA

### 4.1 Shock dell'Offerta (Supply Shock)
**Logica:** Tensioni nello stretto di Hormuz o conflitti tra grandi produttori (Medio Oriente, Russia) portano a un aumento repentino del Petrolio. 
**Impatto:** Stagflazione (Alta inflazione + Bassa crescita). Fortemente Bearish per tutti i settori tranne l'Energy.

### 4.2 Cicli Economici dei Paesi Produttori
- Paesi Produttori (CAD, NOK, BRL): Valute forti quando le commodity salgono.
- Paesi Consumatori (EUR, JPY, CNY): Valute deboli quando le commodity salgono.
