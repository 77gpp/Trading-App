---
name: murphy-analisi-tecnica
description: Testo classico di analisi tecnica di John J. Murphy. Copre trend, medie mobili, oscillatori RSI/MACD, pattern grafici, Fibonacci, correlazioni intermarket e la teoria di Dow.
---

# SKILLS ESTRATTE: Murphy - Analisi Tecnica Dei Mercati Finanziari.pdf

## Teoria di Dow (Dow Theory)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 2, Pagina 17-25
**Descrizione:** La teoria di Dow è una delle pietre miliari dell'analisi tecnica. Sostiene che il mercato si muove in tre tipi di trend: primario (long-term, mesi o anni), secondario (intermediate, settimane o mesi), e minore (short-term, ore o giorni). Un principio chiave è che un trend primario non può essere interrotto da un solo movimento secondario o minore. I segnali di un nuovo trend primario devono essere confermati da un indice di trasporto (es. Indice Industriale e Indice Trasporti). L'obiettivo è identificare l'inizio e la fine dei trend primari.
**Logica Tecnica/Pseudocodice:**
1.  **I principi fondamentali:**
    *   Il mercato sconta tutto.
    *   I prezzi si muovono in trend (primari, secondari, minori).
    *   I prezzi devono essere confermati da un indice correlato (es. Indice Industriale e Indice Trasporti negli USA).
    *   La media è composta da tre fasi: accumulazione, partecipazione pubblica, distribuzione.
    *   I volumi devono confermare il trend.
    *   Un trend è in atto fino a che un segnale definitivo di inversione non lo nega.
2.  **Identificazione del trend primario rialzista:**
    *   Successione di massimi e minimi crescenti in entrambe le medie (es. Industriale e Trasporti).
    *   Per la conferma, un nuovo massimo nell'Indice Industriale deve essere seguito da un nuovo massimo nell'Indice Trasporti (e viceversa) che supera i precedenti massimi secondari.
3.  **Identificazione del trend primario ribassista:**
    *   Successione di massimi e minimi decrescenti in entrambe le medie.
    *   Per la conferma, un nuovo minimo nell'Indice Industriale deve essere seguito da un nuovo minimo nell'Indice Trasporti (e viceversa) che infrange i precedenti minimi secondari.
4.  **Conferma tramite Indici Correlati:** Se l'Indice Industriale fa un nuovo massimo superiore al precedente, l'Indice Trasporti deve confermare facendo un nuovo massimo superiore. Senza tale conferma, si ha una *divergenza* che può indicare debolezza del trend primario.
5.  **Volume:** Il volume deve aumentare nella direzione del trend primario (es. aumentare in un uptrend, diminuire in un downtrend). Il volume elevato in un nuovo massimo/minimo conferma il segnale.

---

## Failure Swing (Teoria di Dow)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 2, Pagina 22-23 (Figure 2.3a, 2.3b, 2.4a, 2.4b)
**Descrizione:** Un "failure swing" (fallimento di oscillazione) nella Teoria di Dow è un segnale di inversione del trend primario che si verifica quando il mercato non riesce a confermare un nuovo massimo (o minimo) rispetto al precedente, dopo aver rotto una linea di trend. Questo indica una debolezza nel trend dominante e suggerisce una potenziale inversione.
**Logica Tecnica/Pseudocodice:**
1.  **Failure Swing Top (segnale ribassista):**
    *   Precondizione: Il mercato è in un uptrend.
    *   Passo 1: Il prezzo raggiunge un massimo (Punto A) e poi ritraccia, formando un minimo (Punto B).
    *   Passo 2: Il prezzo sale nuovamente ma non riesce a superare il massimo precedente (Punto A), formando un massimo inferiore (Punto C).
    *   Passo 3: Il prezzo poi scende sotto il minimo precedente (Punto B).
    *   *Segnale:* La rottura al ribasso del Punto B (minimo precedente) dopo un massimo inferiore (Punto C) è un segnale di inversione ribassista ("failure swing top").
2.  **Failure Swing Bottom (segnale rialzista):**
    *   Precondizione: Il mercato è in un downtrend.
    *   Passo 1: Il prezzo raggiunge un minimo (Punto A) e poi ritraccia, formando un massimo (Punto B).
    *   Passo 2: Il prezzo scende nuovamente ma non riesce a superare il minimo precedente (Punto A), formando un minimo superiore (Punto C).
    *   Passo 3: Il prezzo poi sale sopra il massimo precedente (Punto B).
    *   *Segnale:* La rottura al rialzo del Punto B (massimo precedente) dopo un minimo superiore (Punto C) è un segnale di inversione rialzista ("failure swing bottom").

---

## Grafico a Barre (Bar Chart)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 3, Pagina 27-28 (Figura 3.1)
**Descrizione:** Il grafico a barre è una rappresentazione comune dei prezzi in un dato periodo (es. giornaliero, settimanale). Ogni barra verticale rappresenta l'intervallo di prezzo tra il massimo e il minimo della sessione. Un piccolo trattino orizzontale a sinistra indica il prezzo di apertura, mentre un trattino a destra indica il prezzo di chiusura.
**Logica Tecnica/Pseudocodice:**
*   **Input:** Prezzi di apertura (Open), massimo (High), minimo (Low), chiusura (Close) per ogni periodo di tempo.
*   **Visualizzazione:**
    *   Disegna una linea verticale dal prezzo minimo al prezzo massimo del periodo.
    *   Disegna un trattino orizzontale a sinistra della linea verticale al prezzo di apertura.
    *   Disegna un trattino orizzontale a destra della linea verticale al prezzo di chiusura.
*   **Interpretazione:**
    *   L'altezza della barra indica la volatilità del periodo.
    *   La posizione di apertura e chiusura rispetto al range max-min può dare indicazioni sulla forza di acquisto o vendita.

---

## Grafico Lineare (Line Chart)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 3, Pagina 27-28 (Figura 3.2)
**Descrizione:** Il grafico lineare è la forma più semplice di rappresentazione dei prezzi, spesso basato solo sui prezzi di chiusura. Ogni punto sul grafico rappresenta il prezzo di chiusura di un periodo, e questi punti sono collegati da una linea per mostrare il movimento continuo dei prezzi.
**Logica Tecnica/Pseudocodice:**
*   **Input:** Prezzo di chiusura (Close) per ogni periodo di tempo.
*   **Visualizzazione:**
    *   Per ogni periodo, traccia un punto al prezzo di chiusura.
    *   Collega i punti consecutivi con una linea retta.
*   **Interpretazione:**
    *   Fornisce una visione chiara del trend di chiusura senza il "rumore" di apertura, massimo e minimo. Utile per identificare tendenze generali e pattern ampi.

---

## Grafico Point & Figure (Point & Figure Chart)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 3, Pagina 27, 29 (Figura 3.3) e Capitolo 11 (Pagina 201-227)
**Descrizione:** I grafici Point & Figure filtrano i movimenti di prezzo minori per concentrarsi solo sui movimenti significativi. Non includono il tempo (non è sull'asse X) né il volume. I movimenti al rialzo sono rappresentati da colonne di "X" e i movimenti al ribasso da colonne di "O". Una nuova colonna inizia solo quando il prezzo inverte la direzione di un certo importo ("box size") e supera un numero predefinito di box ("reversal amount", tipicamente 3 box).
**Logica Tecnica/Pseudocodice:**
*   **Input:** Prezzi (tipicamente chiusure o massimi/minimi).
*   **Parametri:** `BoxSize` (valore monetario che un movimento di prezzo deve eguagliare o superare per disegnare un nuovo box) e `ReversalAmount` (numero di box necessari per invertire la direzione e iniziare una nuova colonna, tipicamente 3).
*   **Processo:**
    1.  Inizia una colonna con 'X' se il prezzo sale, 'O' se il prezzo scende.
    2.  Se il prezzo si muove al rialzo di almeno `BoxSize`, aggiungi una 'X' alla colonna corrente.
    3.  Se il prezzo si muove al ribasso di almeno `ReversalAmount` volte `BoxSize` dalla cima dell'ultima 'X' (o dalla base dell'ultima 'O' in caso di discesa), inizia una nuova colonna con 'O' alla scatola appropriata.
    4.  Se il prezzo si muove al rialzo di almeno `ReversalAmount` volte `BoxSize` dalla base dell'ultima 'O', inizia una nuova colonna con 'X' alla scatola appropriata.
*   **Scopo:** Eliminare il "rumore" del mercato, evidenziare i trend e i pattern di inversione/continuazione basati sulla forza del movimento di prezzo.

---

## Grafico Candlestick Giapponese (Japanese Candlestick Chart)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 3, Pagina 29-30 (Figura 3.4) e Capitolo 12 (Pagina 229-246)
**Descrizione:** I grafici candlestick forniscono una rappresentazione visiva ricca dei movimenti di prezzo (apertura, massimo, minimo, chiusura) in un dato periodo. Ogni candlestick è composto da un "corpo reale" (la parte spessa) che rappresenta il range tra apertura e chiusura. Le "ombre" o "stoppini" (linee sottili sopra e sotto il corpo) rappresentano i prezzi massimo e minimo raggiunti. Il colore del corpo indica la direzione del movimento: bianco/vuoto se la chiusura è superiore all'apertura (rialzo), nero/pieno se la chiusura è inferiore all'apertura (ribasso).
**Logica Tecnica/Pseudocodice:**
*   **Input:** Prezzi di apertura (Open), massimo (High), minimo (Low), chiusura (Close) per ogni periodo di tempo.
*   **Costruzione:**
    *   **Corpo Reale:** Disegna un rettangolo tra il prezzo di apertura e il prezzo di chiusura.
        *   Se `Close > Open`: Corpo Bianco/Vuoto.
        *   Se `Close < Open`: Corpo Nero/Pieno.
    *   **Ombra Superiore:** Disegna una linea verticale dal prezzo massimo al bordo superiore del corpo reale.
    *   **Ombra Inferiore:** Disegna una linea verticale dal prezzo minimo al bordo inferiore del corpo reale.
*   **Interpretazione:** I pattern formati da uno o più candlestick sono usati per prevedere futuri movimenti di prezzo. Capitolo 12 contiene un elenco esaustivo di formazioni candlestick di inversione e continuazione.

---

## Scala Aritmetica e Logaritmica (Arithmetic and Logarithmic Scale)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 3, Pagina 31 (Figure 3.5, 3.6)
**Descrizione:** I prezzi possono essere rappresentati su scala aritmetica o logaritmica. La scala aritmetica mostra i movimenti di prezzo in punti assoluti (una variazione di 10 punti è la stessa indipendentemente dal livello di prezzo). La scala logaritmica mostra i movimenti di prezzo in termini percentuali (una variazione del 10% è la stessa indipendentemente dal livello di prezzo, quindi la distanza tra 10 e 20 è uguale alla distanza tra 100 e 200).
**Logica Tecnica/Pseudocodice:**
*   **Scala Aritmetica:**
    *   `Prezzo_Grafico = Prezzo_Reale`
    *   Adatta per visualizzare movimenti assoluti di prezzo, specialmente su scale di tempo più brevi o quando le variazioni percentuali sono relativamente piccole.
*   **Scala Logaritmica:**
    *   `Prezzo_Grafico = log(Prezzo_Reale)`
    *   Adatta per visualizzare movimenti percentuali di prezzo, utile per lunghe scale di tempo o quando le variazioni percentuali sono più importanti delle variazioni assolute.
*   **Regola d'uso:** Per grafici a lungo termine o con grandi movimenti di prezzo, è preferibile la scala logaritmica per rappresentare accuratamente la vera entità delle variazioni relative. Per grafici a breve termine o con piccole variazioni assolute, la scala aritmetica è adeguata.

---

## Volume (Volume Analysis)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 3, Pagina 33 (Figura 3.7) e Capitolo 7 (Pagina 123-141)
**Descrizione:** Il volume rappresenta il numero totale di unità scambiate in un dato periodo. È un indicatore secondario ma importante che dovrebbe sempre essere analizzato insieme al movimento dei prezzi per confermare la forza o la debolezza di un trend o di un pattern grafico.
**Logica Tecnica/Pseudocodice:**
*   **Regola Generale:**
    *   **Trend Rialzista (Uptrend):** Il volume dovrebbe aumentare quando i prezzi salgono e diminuire o essere basso durante i ritracciamenti. Un volume elevato in un nuovo massimo conferma il trend.
    *   **Trend Ribassista (Downtrend):** Il volume dovrebbe aumentare quando i prezzi scendono e diminuire o essere basso durante i ritracciamenti rialzisti. Un volume elevato in un nuovo minimo conferma il trend.
    *   **Formazioni di Inversione:** Spesso presentano un picco di volume significativo all'inizio della formazione (es. alla testa in un Head & Shoulders top o al minimo in un V-bottom) e/o un aumento del volume nella rottura della neckline o della linea di trend.
    *   **Formazioni di Continuazione:** Il volume tende a diminuire mentre il pattern si forma e ad aumentare nella direzione del breakout.
*   **Segnali di Divergenza Volume-Prezzo:** Se il prezzo fa un nuovo massimo ma il volume non lo conferma (volume decrescente), può essere un segnale di debolezza del trend e di potenziale inversione.

---

## Open Interest (L'Open Interest dei Futures)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 3, Pagina 33 (Figura 3.8) e Capitolo 7 (Pagina 123-141)
**Descrizione:** L'Open Interest (OI) è il numero totale di contratti futures o opzioni non ancora chiusi alla fine di un giorno di negoziazione. Rappresenta il numero di posizioni aperte sul mercato. È un indicatore particolarmente rilevante nei mercati futures, dove fornisce informazioni sulla forza sottostante di un movimento di prezzo.
**Logica Tecnica/Pseudocodice:**
*   **Input:** Prezzo di chiusura, Open Interest per ogni periodo.
*   **Regola Generale:**
    *   **Prezzi Up, Volume Up, OI Up:** Rialzo forte e sostenibile. Nuovo denaro sta entrando nel mercato. (FORTE RIALZO)
    *   **Prezzi Up, Volume Down, OI Down:** Rialzo debole. Gli acquirenti sono pochi e le posizioni lunghe vengono chiuse. (DEBOLE RIALZO)
    *   **Prezzi Down, Volume Up, OI Up:** Ribasso forte e sostenibile. Nuovo denaro sta entrando nel mercato per posizioni corte. (FORTE RIBASSO)
    *   **Prezzi Down, Volume Down, OI Down:** Ribasso debole. Le posizioni corte vengono chiuse. Potenziale inversione al rialzo. (DEBOLE RIBASSO)
    *   **Prezzi Laterali, Volume Down, OI Down:** Mercato in attesa. I partecipanti si ritirano. Potenziale rottura nella direzione del trend precedente.
*   **Interpretazione aggiuntiva:**
    *   Un aumento dell'Open Interest indica un crescente impegno nel mercato, mentre una diminuzione suggerisce una riduzione dell'interesse.
    *   È cruciale per identificare la fase di un ciclo di mercato (accumulazione, partecipazione, distribuzione).

---

## Grafico Settimanale e Mensile (Weekly and Monthly Charts)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 3, Pagina 35 (Figura 3.9) e Capitolo 8 (Pagina 143-153)
**Descrizione:** Oltre ai grafici giornalieri, è fondamentale analizzare i prezzi su periodi più lunghi, come grafici settimanali e mensili. Questi grafici filtrano il rumore a breve termine e offrono una prospettiva più ampia dei trend dominanti, essenziali per la pianificazione strategica a lungo termine e per identificare i principali livelli di supporto e resistenza.
**Logica Tecnica/Pseudocodice:**
*   **Input:** Dati di prezzo aggregati per settimana o mese.
*   **Costruzione:** Simile ai grafici a barre giornalieri, ma ogni barra (o candlestick) rappresenta l'attività di prezzo di una settimana o un mese.
*   **Scopo:**
    *   Identificazione dei trend primari e secondari.
    *   Individuazione dei principali livelli di supporto e resistenza.
    *   Conferma dei segnali visti sui grafici giornalieri (una divergenza su un grafico giornaliero può essere un segnale meno significativo se non confermata dal grafico settimanale/mensile).
    *   Utilizzato per strategie di investimento a lungo termine.

---

## Trend (Trend Analysis)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 4, Pagina 37-41 (Figura 4.1, 4.2, 4.3, 4.4)
**Descrizione:** Un trend è la direzione generale del mercato. L'analisi del trend è il fondamento dell'analisi tecnica. I prezzi si muovono tipicamente in trend, che possono essere rialzisti (uptrend), ribassisti (downtrend) o laterali (trading range/trendless). L'identificazione della direzione del trend è cruciale per le decisioni di trading.
**Logica Tecnica/Pseudocodice:**
*   **Trend Rialzista (Uptrend):**
    *   Definito da una serie di massimi e minimi crescenti.
    *   `Prezzo_Massimo_N > Prezzo_Massimo_{N-1}`
    *   `Prezzo_Minimo_N > Prezzo_Minimo_{N-1}`
*   **Trend Ribassista (Downtrend):**
    *   Definito da una serie di massimi e minimi decrescenti.
    *   `Prezzo_Massimo_N < Prezzo_Massimo_{N-1}`
    *   `Prezzo_Minimo_N < Prezzo_Minimo_{N-1}`
*   **Trend Laterale/Trading Range (Trendless):**
    *   Definito da massimi e minimi che rimangono entro un intervallo di prezzo relativamente stretto, senza una chiara direzione.
    *   Non c'è una chiara successione di massimi/minimi crescenti o decrescenti.
*   **Classificazione dei Trend:**
    *   **Primario:** Dura da mesi a diversi anni (movimento principale).
    *   **Secondario:** Dura da poche settimane a diversi mesi (correzioni del trend primario).
    *   **Minore:** Dura da pochi giorni a poche settimane (fluttuazioni a breve termine).

---

## Supporto e Resistenza (Support and Resistance)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 4, Pagina 41-48 (Figure 4.5, 4.6, 4.7, 4.8, 4.9, 4.10, 4.11, 4.12, 4.13)
**Descrizione:** Il supporto è un livello di prezzo al di sotto del quale la domanda è sufficientemente forte da arrestare un calo e invertire la direzione dei prezzi. La resistenza è un livello di prezzo al di sopra del quale l'offerta è sufficientemente forte da arrestare un aumento e invertire la direzione dei prezzi. Una volta rotti, i livelli di supporto e resistenza possono scambiarsi di ruolo.
**Logica Tecnica/Pseudocodice:**
*   **Identificazione Supporto:**
    *   Un precedente minimo significativo.
    *   Un livello dove i prezzi hanno toccato o si sono avvicinati più volte prima di invertire al rialzo.
*   **Identificazione Resistenza:**
    *   Un precedente massimo significativo.
    *   Un livello dove i prezzi hanno toccato o si sono avvicinati più volte prima di invertire al ribasso.
*   **Regole di Interscambio di Ruoli:**
    *   Quando un livello di resistenza viene rotto al rialzo, quel livello spesso diventa un nuovo supporto.
    *   Quando un livello di supporto viene rotto al ribasso, quel livello spesso diventa una nuova resistenza.
*   **Forza del Supporto/Resistenza:**
    *   Più volte un livello è stato testato e ha tenuto, più forte è.
    *   Più ampio è il volume associato ai test e ai breakout, più significativo è.
    *   Più recente è il test, più rilevante è il livello.
*   **Livelli di Prezzo Numerici Rotondi (Numeri di Fibonacci, prezzi psicologici):** I numeri interi rotondi (es. 100, 1000) e i livelli di Fibonacci (38.2%, 50%, 61.8%) spesso agiscono come livelli naturali di supporto e resistenza a causa della psicologia di massa.

---

## Linea di Tendenza / Trendline (Trendline)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 4, Pagina 49-57 (Figure 4.15, 4.16, 4.17, 4.18, 4.19, 4.20, 4.21, 4.22, 4.23, 4.24)
**Descrizione:** Una trendline è una linea retta disegnata su un grafico di prezzo per collegare due o più massimi o minimi significativi e mostra la direzione e la pendenza del trend. È uno strumento visivo per definire il trend attuale e identificare potenziali punti di inversione quando viene rotta.
**Logica Tecnica/Pseudocodice:**
*   **Trendline Rialzista (Upward Trendline):**
    *   Collega due o più minimi consecutivi crescenti (il secondo minimo deve essere superiore al primo).
    *   La linea dovrebbe essere disegnata in modo da non incrociare nessun prezzo tra i due punti iniziali.
    *   Estendi la linea nel futuro.
    *   Un trend rialzista è valido finché la trendline non viene rotta al ribasso.
*   **Trendline Ribassista (Downward Trendline):**
    *   Collega due o più massimi consecutivi decrescenti (il secondo massimo deve essere inferiore al primo).
    *   La linea dovrebbe essere disegnata in modo da non incrociare nessun prezzo tra i due punti iniziali.
    *   Estendi la linea nel futuro.
    *   Un trend ribassista è valido finché la trendline non viene rotta al rialzo.
*   **Forza della Trendline:**
    *   Più a lungo la trendline rimane intatta, più significativa è.
    *   Più volte la trendline è toccata (e ha tenuto), più forte è.
    *   Più pronunciata è la pendenza della trendline, più dinamico è il trend.
*   **Rottura della Trendline (Breakout):**
    *   Una rottura valida si verifica quando il prezzo chiude in modo significativo oltre la trendline (es. una chiusura del 3% o per più giorni consecutivi oltre la linea).
    *   Una rottura suggerisce una potenziale inversione o un rallentamento del trend precedente.
*   **Trendline che Inverte il Ruolo:** Dopo una rottura, una trendline precedentemente di supporto può diventare resistenza, e una precedentemente di resistenza può diventare supporto.

---

## Principio del Ventaglio (Fan Principle)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 4, Pagina 58-59 (Figure 4.25, 4.26, 4.27)
**Descrizione:** Il principio del ventaglio si applica quando una trendline viene rotta. Dopo una rottura di una trendline rialzista, i prezzi spesso ritracceranno e testeranno la linea rotta come resistenza. Se questa linea viene nuovamente rotta, si disegna una seconda trendline meno ripida, che se rotta, porta alla terza linea, la cui rottura è considerata un segnale più significativo di inversione del trend. Tre linee di ventaglio sono disegnate dal punto di massima/minima del trend.
**Logica Tecnica/Pseudocodice:**
*   **Rialzista (Bullish Fan):**
    1.  Identifica un uptrend e disegna la prima trendline rialzista (Fan Line 1) collegando due minimi crescenti.
    2.  Quando Fan Line 1 viene rotta al ribasso, disegna una seconda trendline rialzista (Fan Line 2) da un minimo successivo, meno ripida della prima.
    3.  Quando Fan Line 2 viene rotta al ribasso, disegna una terza trendline rialzista (Fan Line 3) ancora meno ripida.
    4.  *Segnale di Inversione:* La rottura al ribasso di Fan Line 3 è un forte segnale di inversione del trend primario al ribasso.
*   **Ribassista (Bearish Fan):**
    1.  Identifica un downtrend e disegna la prima trendline ribassista (Fan Line 1) collegando due massimi decrescenti.
    2.  Quando Fan Line 1 viene rotta al rialzo, disegna una seconda trendline ribassista (Fan Line 2) da un massimo successivo, meno ripida della prima.
    3.  Quando Fan Line 2 viene rotta al rialzo, disegna una terza trendline ribassista (Fan Line 3) ancora meno ripida.
    4.  *Segnale di Inversione:* La rottura al rialzo di Fan Line 3 è un forte segnale di inversione del trend primario al rialzo.
*   **Numero Tre:** Il numero tre ha un ruolo psicologico significativo; la rottura della terza linea di ventaglio è spesso vista come una conferma robusta dell'inversione.

---

## Linea del Canale (Channel Line)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 4, Pagina 62-65 (Figure 4.31, 4.32, 4.33, 4.34, 4.35, 4.36, 4.37)
**Descrizione:** Una linea di canale è una linea parallela a una trendline primaria. In un uptrend, la channel line è disegnata parallelamente alla trendline rialzista, passando sopra i massimi intermedi. In un downtrend, è disegnata parallelamente alla trendline ribassista, passando sotto i minimi intermedi. I canali definiscono un intervallo di prezzo entro cui il trend tende a muoversi.
**Logica Tecnica/Pseudocodice:**
*   **Canale Rialzista (Uptrend Channel):**
    1.  Disegna una trendline rialzista collegando due o più minimi crescenti.
    2.  Traccia una linea parallela (channel line) al primo massimo significativo tra i due minimi usati per la trendline, o il massimo più significativo nel canale.
    3.  *Interpretazione:* I prezzi dovrebbero rimanere all'interno del canale. Un movimento verso la trendline principale suggerisce acquisto, mentre un movimento verso la channel line suggerisce vendita o ritracciamento.
*   **Canale Ribassista (Downtrend Channel):**
    1.  Disegna una trendline ribassista collegando due o più massimi decrescenti.
    2.  Traccia una linea parallela (channel line) al primo minimo significativo tra i due massimi usati per la trendline, o il minimo più significativo nel canale.
    3.  *Interpretazione:* I prezzi dovrebbero rimanere all'interno del canale. Un movimento verso la trendline principale suggerisce vendita, mentre un movimento verso la channel line suggerisce acquisto o ritracciamento.
*   **Rottura del Canale:** Una rottura valida al di fuori del canale può segnalare un'accelerazione del trend o un'imminente inversione.
    *   Una rottura al di sopra della channel line in un uptrend può indicare un'accelerazione.
    *   Una rottura al di sotto della channel line in un downtrend può indicare un'accelerazione.
    *   Una rottura al di sotto della trendline in un uptrend o al di sopra della trendline in un downtrend segnala un'inversione di trend.

---

## Ritracciamento Percentuale (Retracement Percentages)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 4, Pagina 67-69 (Figure 4.39, 4.40)
**Descrizione:** I ritracciamenti percentuali sono movimenti correttivi che si oppongono al trend precedente. Dopo un movimento significativo di prezzo, i ritracciamenti spesso si fermano a percentuali specifiche del movimento originale. I livelli di ritracciamento più comuni sono 33%, 50%, 62% (o 66%), e i ritracciamenti di Fibonacci (38.2%, 50%, 61.8%).
**Logica Tecnica/Pseudocodice:**
*   **Calcolo:**
    1.  Identifica un movimento di prezzo significativo (dall'inizio alla fine del trend).
    2.  Calcola la lunghezza totale di questo movimento (`Max - Min`).
    3.  Moltiplica la lunghezza per le percentuali di ritracciamento:
        *   33% Ritracciamento = `Min + (Lunghezza * 0.33)` in uptrend; `Max - (Lunghezza * 0.33)` in downtrend.
        *   50% Ritracciamento = `Min + (Lunghezza * 0.50)` in uptrend; `Max - (Lunghezza * 0.50)` in downtrend.
        *   62% Ritracciamento = `Min + (Lunghezza * 0.62)` in uptrend; `Max - (Lunghezza * 0.62)` in downtrend.
*   **Scopo:** Questi livelli agiscono spesso come supporto o resistenza e sono usati per identificare potenziali punti di inversione per le correzioni. La rottura di un livello chiave può indicare che il ritracciamento continuerà al livello successivo.

---

## Speed Resistance Lines (Linee di Resistenza di Velocità)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 4, Pagina 69-71 (Figure 4.41, 4.42)
**Descrizione:** Le Speed Resistance Lines sono un metodo per misurare la velocità o la pendenza di un trend. Sono disegnate dividendo l'altezza del movimento di prezzo in terzi. Offrono livelli di supporto/resistenza basati sulla velocità di cambiamento del prezzo.
**Logica Tecnica/Pseudocodice:**
*   **Calcolo per Uptrend:**
    1.  Identifica un punto minimo significativo (Punto 1) e il massimo successivo (Punto 2).
    2.  Calcola la distanza verticale tra Punto 1 e Punto 2.
    3.  Dividi questa distanza in tre parti uguali.
    4.  Disegna tre linee dal Punto 1:
        *   Linea 1/3 Speed: Dal Punto 1, al 1/3 della distanza verticale sotto il Punto 2.
        *   Linea 2/3 Speed: Dal Punto 1, al 2/3 della distanza verticale sotto il Punto 2.
    5.  Estendi le linee nel futuro.
*   **Calcolo per Downtrend:**
    1.  Identifica un punto massimo significativo (Punto 1) e il minimo successivo (Punto 2).
    2.  Calcola la distanza verticale tra Punto 1 e Punto 2.
    3.  Dividi questa distanza in tre parti uguali.
    4.  Disegna tre linee dal Punto 1:
        *   Linea 1/3 Speed: Dal Punto 1, al 1/3 della distanza verticale sopra il Punto 2.
        *   Linea 2/3 Speed: Dal Punto 1, al 2/3 della distanza verticale sopra il Punto 2.
    5.  Estendi le linee nel futuro.
*   **Interpretazione:**
    *   Queste linee agiscono come supporto/resistenza dinamici.
    *   La rottura di una linea di velocità suggerisce un rallentamento o un'accelerazione del trend.
    *   La rottura della linea più ripida (1/3 o 2/3) è un segnale più debole rispetto alla rottura della linea meno ripida. La rottura di tutte le linee di velocità suggerisce un'inversione completa del trend.

---

## Linee a Ventaglio di Gann e Fibonacci (Gann and Fibonacci Fan Lines)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 4, Pagina 71
**Descrizione:** Le linee a ventaglio di Gann e Fibonacci utilizzano angoli specifici e rapporti di ritracciamento per identificare potenziali livelli di supporto e resistenza e la pendenza di un trend. La teoria di Gann si basa su angoli che riflettono il rapporto tra prezzo e tempo, mentre le linee di Fibonacci utilizzano i rapporti aurei.
**Logica Tecnica/Pseudocodice:**
*   **Gann Fan Lines (Linee a Ventaglio di Gann):**
    1.  Identifica un punto estremo (massimo o minimo).
    2.  Disegna linee da questo punto con pendenze specifiche che rappresentano rapporti prezzo/tempo (es. 1x1, 1x2, 2x1, 1x4, 4x1, ecc.). Gli angoli comuni sono 45 gradi (1x1), 26.25 gradi (1x2), 63.75 gradi (2x1), 15 gradi (1x4), 75 gradi (4x1).
    3.  *Interpretazione:* Le linee agiscono come supporto/resistenza. Una rottura al di sotto di una linea di Gann suggerisce che il prezzo si muoverà verso la linea successiva con minore pendenza.
*   **Fibonacci Fan Lines (Linee a Ventaglio di Fibonacci):**
    1.  Identifica un punto estremo (massimo o minimo).
    2.  Identifica un punto di ritracciamento significativo.
    3.  Disegna una linea dal punto estremo al punto di ritracciamento.
    4.  Disegna linee parallele a questa linea attraverso i livelli di ritracciamento di Fibonacci (38.2%, 50%, 61.8%) o altri punti chiave.
    5.  *Interpretazione:* Le linee agiscono come supporto/resistenza dinamici.

---

## Internal Trendlines (Trendlines Interne)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 4, Pagina 72 (Figura 4.44a, 4.44b)
**Descrizione:** Le trendline interne sono simili alle trendline tradizionali ma vengono disegnate con maggiore flessibilità per catturare i movimenti di prezzo più stretti o i veri punti di svolta, anche se questo significa che la linea può attraversare il corpo di alcune barre. Sono particolarmente utili nei mercati meno liquidi o più volatili dove le ombre dei candlestick possono essere lunghe.
**Logica Tecnica/Pseudocodice:**
*   **Differenza da Trendline Standard:** Invece di collegare solo i massimi o i minimi estremi, una trendline interna può passare attraverso il corpo di una o più barre per catturare una linea di trend più accurata che riflette meglio il movimento di prezzo sottostante.
*   **Uso:** Simile alle trendline standard per identificare il trend e i punti di rottura, ma possono essere più sensibili ai cambiamenti di breve termine.

---

## Reversal Day (Giorno di Inversione)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 4, Pagina 72-73 (Figure 4.44a, 4.44b - esempi impliciti)
**Descrizione:** Un "reversal day" (giorno di inversione) è un segnale di inversione del trend a breve termine. In un uptrend, un reversal day si verifica quando il prezzo raggiunge un nuovo massimo, ma poi inverte e chiude significativamente più basso dell'apertura (o della chiusura del giorno precedente). In un downtrend, si verifica quando il prezzo raggiunge un nuovo minimo, ma poi inverte e chiude significativamente più alto dell'apertura (o della chiusura del giorno precedente).
**Logica Tecnica/Pseudocodice:**
*   **Top Reversal Day (segnale ribassista):**
    1.  Precondizione: Il mercato è in un uptrend.
    2.  Condizione 1: Il prezzo raggiunge un nuovo massimo (superiore al massimo del giorno precedente).
    3.  Condizione 2: Il prezzo chiude al di sotto del prezzo di apertura del giorno corrente O al di sotto del prezzo di chiusura del giorno precedente.
    4.  Conferma: Un volume elevato rafforza il segnale.
*   **Bottom Reversal Day (segnale rialzista):**
    1.  Precondizione: Il mercato è in un downtrend.
    2.  Condizione 1: Il prezzo raggiunge un nuovo minimo (inferiore al minimo del giorno precedente).
    3.  Condizione 2: Il prezzo chiude al di sopra del prezzo di apertura del giorno corrente O al di sopra del prezzo di chiusura del giorno precedente.
    4.  Conferma: Un volume elevato rafforza il segnale.

---

## Weekly and Monthly Reversals (Inversioni Settimanali e Mensili)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 4, Pagina 73
**Descrizione:** Concetto simile al Reversal Day, ma applicato a grafici settimanali o mensili. Sono segnali più potenti delle inversioni giornaliere in quanto filtrano il rumore a breve termine e indicano potenziali inversioni di trend a medio o lungo termine.
**Logica Tecnica/Pseudocodice:**
*   **Top Reversal Week/Month:** La settimana/mese raggiunge un nuovo massimo ma chiude al di sotto della chiusura della settimana/mese precedente.
*   **Bottom Reversal Week/Month:** La settimana/mese raggiunge un nuovo minimo ma chiude al di sopra della chiusura della settimana/mese precedente.
*   **Significatività:** Questi segnali sono considerati più affidabili per inversioni di trend di maggior durata.

---

## Price Gaps (Gaps di Prezzo)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 4, Pagina 74-77 (Figure 4.45, 4.46, 4.47, 4.48)
**Descrizione:** Un gap di prezzo si verifica quando il prezzo di apertura di un periodo è significativamente superiore o inferiore al prezzo di chiusura del periodo precedente, senza che vi siano scambi intermedi. I gaps possono segnalare un'accelerazione del trend, la continuazione o l'esaurimento di un movimento, o un'inversione di trend.
**Logica Tecnica/Pseudocodice:**
*   **Breakaway Gap (Gap di Rottura):**
    1.  Si verifica all'inizio di un nuovo trend dopo una formazione di prezzo (es. triangolo, rettangolo).
    2.  Il prezzo salta al di sopra della resistenza (o al di sotto del supporto) con un volume elevato.
    3.  *Interpretazione:* Segnala l'inizio di un movimento di prezzo significativo e un nuovo trend. Raramente vengono colmati.
*   **Runaway Gap / Misuring Gap (Gap di Continuazione / Misurazione):**
    1.  Si verifica nel mezzo di un trend ben stabilito, indicando una continuazione del movimento esistente.
    2.  Spesso accompagnato da un volume elevato.
    3.  *Interpretazione:* Indica la forza del trend e che i prezzi continueranno a muoversi nella stessa direzione. Possono essere usati per stimare l'obiettivo di prezzo proiettando la distanza percorsa prima del gap. Di solito non vengono colmati rapidamente.
*   **Exhaustion Gap (Gap di Esaurimento):**
    1.  Si verifica alla fine di un trend maturo, spesso con un volume elevato insolitamente alto.
    2.  Dopo il gap, il prezzo spesso inverte rapidamente.
    3.  *Interpretazione:* Segnala che il trend sta per finire e un'inversione è imminente. Di solito vengono colmati rapidamente.
*   **Island Reversal (Inversione ad Isola):**
    1.  Un gap di esaurimento seguito da un prezzo laterale (isola) che poi rompe nella direzione opposta con un breakaway gap.
    2.  *Interpretazione:* Un potente segnale di inversione del trend. La zona di prezzo isolata rappresenta un'area di indecisione seguita da un forte consenso in una nuova direzione.
*   **Closing Gaps:** I gaps, soprattutto quelli di esaurimento, tendono ad essere "chiusi" o "colmati" dal prezzo che ritorna al livello del gap. I gaps di rottura e continuazione sono meno propensi a essere colmati.

---

## Formazioni di Inversione (Reversal Patterns)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 5, Pagina 79-100
**Descrizione:** Le formazioni di inversione sono pattern grafici che segnalano un cambiamento nella direzione di un trend di prezzo. Si sviluppano alla fine di un trend esistente e, una volta completate, indicano che il trend precedente è probabile che si inverta. L'analisi del volume è cruciale per la conferma di queste formazioni.
**Logica Tecnica/Pseudocodice:**
*   **Regole Generali:**
    1.  **Trend Preesistente:** Deve esserci un trend precedente da invertire.
    2.  **Segnale Precoce:** I primi segnali di un'inversione appaiono spesso come un rallentamento o una rottura di una trendline minore.
    3.  **Dimensioni:** Più grande e complessa è la formazione, più significativo e duraturo sarà l'inversione di prezzo prevista.
    4.  **Volume:** Il volume è un indicatore cruciale. In genere, il volume tende ad aumentare nella direzione del nuovo trend e a diminuire durante i ritracciamenti all'interno della formazione.
*   **Pattern Specifici:** Testa e Spalle, Tripli Massimi/Minimi, Doppi Massimi/Minimi, V-Formazioni / Spikes, Saucer Tops/Bottoms.

---

## Testa e Spalle (Head & Shoulders Top)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 5, Pagina 82-87 (Figure 5.1, 5.2, 5.3)
**Descrizione:** Il pattern Testa e Spalle è una delle formazioni di inversione più affidabili e comuni, segnalando la fine di un uptrend. È composto da tre massimi: una Spalla Sinistra (SS), una Testa (T) che è il massimo più alto, e una Spalla Destra (SD) che è inferiore alla Testa ma simile alla SS. Una "neckline" (linea del collo) collega i minimi tra la SS e la T, e tra la T e la SD.
**Logica Tecnica/Pseudocodice:**
1.  **Formazione:**
    *   **Trend Preesistente:** Deve esserci un uptrend chiaro.
    *   **Spalla Sinistra (SS):** Un picco con volume elevato, seguito da un ritracciamento su volume più basso.
    *   **Testa (T):** Il prezzo sale oltre il picco della SS, forma un nuovo massimo, spesso con volume inferiore rispetto alla SS, e poi ritraccia di nuovo fino a un livello simile a quello del ritracciamento della SS. Il volume durante il ritracciamento è basso.
    *   **Spalla Destra (SD):** Il prezzo sale di nuovo ma non riesce a raggiungere il livello della Testa, spesso con volume basso o decrescente. Poi ritraccia di nuovo.
    *   **Neckline:** Una linea di trend che collega i minimi tra SS e T, e tra T e SD.
2.  **Segnale di Vendita:**
    *   *Trigger:* La rottura al ribasso della neckline (tipicamente con un gap o volume elevato) è il segnale di vendita.
    *   *Confirmations:* Volume in aumento sulla rottura.
    *   *Pullback:* Spesso, il prezzo può ritornare a testare la neckline rotta da sotto (ora resistenza) prima di continuare a scendere.
3.  **Target di Prezzo:**
    *   Misura la distanza verticale dalla cima della Testa alla neckline.
    *   Proietta questa distanza al ribasso dal punto di rottura della neckline.
    *   `Target = Punto_Rottura_Neckline - (Cima_Testa - Neckline_Altezza)`

---

## Testa e Spalle Rovesciata (Inverse Head & Shoulders Bottom)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 5, Pagina 86-87 (Figura 5.4, 5.5)
**Descrizione:** L'Inverse Head & Shoulders Bottom è il pattern inverso del Testa e Spalle, segnalando la fine di un downtrend e l'inizio di un uptrend. È composto da tre minimi: una Spalla Sinistra (SS) inferiore, una Testa (T) che è il minimo più basso, e una Spalla Destra (SD) inferiore ma più alta della Testa. Una "neckline" collega i massimi tra la SS e la T, e tra la T e la SD.
**Logica Tecnica/Pseudocodice:**
1.  **Formazione:**
    *   **Trend Preesistente:** Deve esserci un downtrend chiaro.
    *   **Spalla Sinistra (SS):** Un minimo con volume elevato, seguito da un ritracciamento su volume più basso.
    *   **Testa (T):** Il prezzo scende oltre il minimo della SS, forma un nuovo minimo (il più basso), spesso con volume inferiore rispetto alla SS, e poi ritraccia di nuovo fino a un livello simile a quello del ritracciamento della SS. Il volume durante il ritracciamento è basso.
    *   **Spalla Destra (SD):** Il prezzo scende di nuovo ma non riesce a raggiungere il livello della Testa, spesso con volume basso o decrescente. Poi ritraccia di nuovo.
    *   **Neckline:** Una linea di trend che collega i massimi tra SS e T, e tra T e SD.
2.  **Segnale di Acquisto:**
    *   *Trigger:* La rottura al rialzo della neckline (tipicamente con un gap o volume elevato) è il segnale di acquisto.
    *   *Confirmations:* Volume in aumento sulla rottura.
    *   *Pullback:* Spesso, il prezzo può ritornare a testare la neckline rotta da sopra (ora supporto) prima di continuare a salire.
3.  **Target di Prezzo:**
    *   Misura la distanza verticale dalla cima della Testa alla neckline.
    *   Proietta questa distanza al rialzo dal punto di rottura della neckline.
    *   `Target = Punto_Rottura_Neckline + (Neckline_Altezza - Minimo_Testa)`

---

## Tripli Massimi e Minimi (Triple Tops and Bottoms)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 5, Pagina 91-92 (Figure 5.6, 5.7)
**Descrizione:** I pattern di Tripli Massimi e Tripli Minimi sono formazioni di inversione meno comuni dei doppi, ma più affidabili. Implicano tre tentativi di rompere un livello di supporto o resistenza che falliscono, seguiti da una rottura decisiva del livello opposto.
**Logica Tecnica/Pseudocodice:**
*   **Triple Top (segnale ribassista):**
    1.  **Trend Preesistente:** Uptrend.
    2.  **Tre Massimi:** Il prezzo raggiunge un picco (M1), ritraccia, risale per raggiungere un secondo picco (M2) a un livello simile al primo, ritraccia, e infine sale per un terzo picco (M3) sempre allo stesso livello (o molto vicino). Il volume tende a diminuire nei successivi picchi.
    3.  **Linee di Supporto:** I minimi tra i picchi formano livelli di supporto.
    4.  **Segnale di Vendita:** La rottura al ribasso del livello di supporto più basso (neckline) formato dai minimi dei ritracciamenti è il segnale di vendita.
    5.  **Target di Prezzo:** Misura la distanza dal picco più alto al livello di supporto. Proietta questa distanza al ribasso dal punto di rottura del supporto.
*   **Triple Bottom (segnale rialzista):**
    1.  **Trend Preesistente:** Downtrend.
    2.  **Tre Minimi:** Il prezzo raggiunge un minimo (m1), ritraccia, scende per raggiungere un secondo minimo (m2) a un livello simile al primo, ritraccia, e infine scende per un terzo minimo (m3) sempre allo stesso livello (o molto vicino). Il volume tende ad aumentare nei successivi minimi, o in corrispondenza del breakout.
    3.  **Linee di Resistenza:** I massimi tra i minimi formano livelli di resistenza.
    4.  **Segnale di Acquisto:** La rottura al rialzo del livello di resistenza più alto (neckline) formato dai massimi dei ritracciamenti è il segnale di acquisto.
    5.  **Target di Prezzo:** Misura la distanza dal minimo più basso al livello di resistenza. Proietta questa distanza al rialzo dal punto di rottura della resistenza.

---

## Doppio Top e Doppio Bottom (Double Tops and Bottoms)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 5, Pagina 93-94 (Figure 5.9, 5.10, 5.11, 5.12, 5.13)
**Descrizione:** I Doppi Massimi e Doppi Minimi sono formazioni di inversione comuni che segnalano un'inversione di trend. Si verificano quando il prezzo tenta di rompere due volte un livello di resistenza o supporto e fallisce, prima di invertire la direzione.
**Logica Tecnica/Pseudocodice:**
*   **Double Top (segnale ribassista):**
    1.  **Trend Preesistente:** Uptrend.
    2.  **Primo Massimo (M1):** Il prezzo raggiunge un picco con volume elevato, poi ritraccia.
    3.  **Secondo Massimo (M2):** Il prezzo risale, spesso con volume inferiore, per raggiungere un secondo picco a un livello simile (entro un piccolo range) a M1. Non deve superare M1 in modo significativo.
    4.  **Linee di Supporto/Neckline:** Il minimo tra M1 e M2 forma un livello di supporto.
    5.  **Segnale di Vendita:** La rottura al ribasso del livello di supporto (neckline) è il segnale di vendita.
    6.  **Target di Prezzo:** Misura la distanza verticale dal massimo più alto al minimo tra i due massimi. Proietta questa distanza al ribasso dal punto di rottura della neckline.
*   **Double Bottom (segnale rialzista):**
    1.  **Trend Preesistente:** Downtrend.
    2.  **Primo Minimo (m1):** Il prezzo raggiunge un minimo con volume elevato, poi ritraccia.
    3.  **Secondo Minimo (m2):** Il prezzo scende di nuovo, spesso con volume inferiore o simile al primo minimo, per raggiungere un secondo minimo a un livello simile (entro un piccolo range) a m1. Non deve scendere significativamente sotto m1.
    4.  **Linee di Resistenza/Neckline:** Il massimo tra m1 e m2 forma un livello di resistenza.
    5.  **Segnale di Acquisto:** La rottura al rialzo del livello di resistenza (neckline) è il segnale di acquisto.
    6.  **Target di Prezzo:** Misura la distanza verticale dal minimo più basso al massimo tra i due minimi. Proietta questa distanza al rialzo dal punto di rottura della neckline.

---

## Falso Breakout (False Breakout)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 5, Pagina 96-97 (Figure 5.14, 5.15, 5.16)
**Descrizione:** Un falso breakout (o "trap") si verifica quando il prezzo sembra rompere un livello chiave di supporto o resistenza o la neckline di un pattern, ma poi inverte rapidamente e si muove nella direzione opposta, intrappolando i trader che hanno agito sul breakout iniziale. I falsi breakout possono essere potenti segnali di inversione.
**Logica Tecnica/Pseudocodice:**
*   **Identificazione:**
    1.  **Breakout Iniziale:** Il prezzo chiude al di sopra di una resistenza (o al di sotto di un supporto) o di una neckline di un pattern di inversione/continuazione.
    2.  **Reversione Rapida:** Entro uno o due periodi successivi, il prezzo inverte e si muove rapidamente nella direzione opposta, spesso chiudendo di nuovo all'interno del pattern o al di sotto/sopra del livello rotto.
    3.  **Volume:** Un volume elevato durante il breakout iniziale e un volume ancora più elevato o significativo durante la reversione possono rafforzare il segnale.
*   **Segnale di Trading:** Un falso breakout è un segnale di trading forte *nella direzione della reversione*. Se un breakout rialzista fallisce, è un segnale ribassista. Se un breakout ribassista fallisce, è un segnale rialzista.
*   **Esempio Double Top con Falso Breakout:** Se il prezzo rompe sopra M2 in un Double Top, ma poi immediatamente inverte e scende sotto M2 o sotto la neckline, è un falso breakout rialzista e un segnale ribassista rinforzato.

---

## Saucers e Spikes (Saucer Tops/Bottoms and Spikes)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 5, Pagina 98-99 (Figure 5.17, 5.18)
**Descrizione:**
*   **Saucer Tops/Bottoms (Formazioni a Piatto):** Sono formazioni di inversione a lungo termine, meno drammatiche, che indicano un cambiamento graduale nel sentiment del mercato. Hanno una forma arrotondata e sono caratterizzate da volumi che si affievoliscono al centro della formazione e aumentano verso i bordi.
*   **Spikes (Formazioni a V o Inversioni a Ago):** Sono formazioni di inversione molto rapide e acute, che indicano un brusco cambiamento nel sentiment del mercato. Sono caratterizzate da un minimo (V-bottom) o massimo (V-top) singolo molto pronunciato, spesso con un volume estremamente elevato.
**Logica Tecnica/Pseudocodice:**
*   **Saucer Bottom (Piatto Rovesciato):**
    1.  **Trend Preesistente:** Downtrend.
    2.  **Formazione:** Il prezzo scende gradualmente, si muove lateralmente per un periodo, e poi sale gradualmente, formando una curva arrotondata.
    3.  **Volume:** Il volume diminuisce gradualmente man mano che il prezzo raggiunge il minimo del piatto, e poi aumenta gradualmente man mano che il prezzo risale.
    4.  **Segnale di Acquisto:** La rottura al rialzo del bordo superiore del piatto (spesso un livello di resistenza orizzontale) con volume elevato.
*   **Saucer Top (Piatto Normale):**
    1.  **Trend Preesistente:** Uptrend.
    2.  **Formazione:** Il prezzo sale gradualmente, si muove lateralmente per un periodo, e poi scende gradualmente.
    3.  **Volume:** Il volume diminuisce gradualmente man mano che il prezzo raggiunge il massimo del piatto, e poi aumenta gradualmente man mano che il prezzo scende.
    4.  **Segnale di Vendita:** La rottura al ribasso del bordo inferiore del piatto (spesso un livello di supporto orizzontale) con volume elevato.
*   **Spike Bottom (Minimo a V):**
    1.  **Trend Preesistente:** Downtrend.
    2.  **Formazione:** Un calo dei prezzi molto rapido e acuto, seguito da un'inversione immediata e un rapido aumento dei prezzi.
    3.  **Volume:** Spesso accompagnato da un volume estremamente elevato al punto di inversione (il minimo della V).
    4.  **Segnale di Acquisto:** La conferma dell'inversione richiede che il prezzo superi una resistenza significativa formata prima o dopo il picco.
*   **Spike Top (Massimo a V):**
    1.  **Trend Preesistente:** Uptrend.
    2.  **Formazione:** Un aumento dei prezzi molto rapido e acuto, seguito da un'inversione immediata e un rapido calo dei prezzi.
    3.  **Volume:** Spesso accompagnato da un volume estremamente elevato al punto di inversione (il massimo della V).
    4.  **Segnale di Vendita:** La conferma dell'inversione richiede che il prezzo scenda sotto un supporto significativo formatosi prima o dopo il picco.

---

## Triangoli (Triangles - General)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 6, Pagina 101-109 (Figure 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9)
**Descrizione:** I triangoli sono formazioni di continuazione che indicano una pausa nel trend precedente, seguita da una ripresa del movimento nella stessa direzione. Sono caratterizzati da linee di trend convergenti che si incontrano a un punto detto apice. Esistono diversi tipi di triangoli. Il volume tende a diminuire man mano che la formazione si sviluppa e ad aumentare al momento del breakout.
**Logica Tecnica/Pseudocodice:**
*   **Regole Generali:**
    1.  **Trend Preesistente:** Necessario un trend precedente.
    2.  **Volume:** Il volume diminuisce durante la formazione e aumenta al breakout.
    3.  **Punti di Contatto:** Richiede almeno due massimi e due minimi per disegnare le linee di trend convergenti.
    4.  **Punto di Rottura:** La rottura dovrebbe avvenire tra 1/2 e 3/4 della lunghezza del triangolo, misurata dalla base all'apice.
    5.  **Target di Prezzo:** Generalmente, la distanza della base del triangolo viene proiettata dal punto di breakout.
*   **Tipi Specifici:**
    *   **Triangolo Simmetrico (Symmetrical Triangle):** Massimi decrescenti e minimi crescenti. Le linee di trend superiore e inferiore convergono quasi simmetricamente. Indica indecisione, il breakout può avvenire in entrambe le direzioni, ma più spesso continua il trend precedente.
    *   **Triangolo Ascendente (Ascending Triangle):** Massimi a un livello orizzontale di resistenza e minimi crescenti. Più spesso si risolve con un breakout rialzista.
    *   **Triangolo Discendente (Descending Triangle):** Minimi a un livello orizzontale di supporto e massimi decrescenti. Più spesso si risolve con un breakout ribassista.
    *   **Triangolo Broadening (Broadening Formation):** Massimi crescenti e minimi decrescenti. Le linee di trend divergono. Indica crescente volatilità e indecisione, spesso si risolve con un'inversione del trend.

---

## Bandiere e Pennant (Flags and Pennants)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 6, Pagina 109-113 (Figure 6.11, 6.12, 6.13, 6.14)
**Descrizione:** Le bandiere e i pennant sono piccole formazioni di continuazione che si verificano dopo un movimento di prezzo brusco e quasi verticale ("asta della bandiera"). Rappresentano brevi pause in un trend forte, seguite da una ripresa del movimento nella stessa direzione. Sono tra le formazioni più affidabili.
**Logica Tecnica/Pseudocodice:**
*   **Formazione:**
    1.  **Asta della Bandiera (Flagpole):** Un movimento di prezzo forte e quasi verticale con volume elevato.
    2.  **Bandiera (Flag):** Un piccolo rettangolo inclinato contro il trend dominante (es. in un uptrend, la bandiera scende leggermente) con volume in calo.
    3.  **Pennant:** Un piccolo triangolo simmetrico, anch'esso inclinato contro il trend o quasi orizzontale, con volume in calo.
*   **Segnale di Trading:**
    *   **Breakout:** La rottura al rialzo (per una bandiera/pennant rialzista) o al ribasso (per una bandiera/pennant ribassista) con un aumento di volume è il segnale.
    *   **Target di Prezzo:** Misura la lunghezza dell'asta della bandiera. Proietta questa distanza dal punto di breakout della bandiera/pennant nella direzione del trend.
    *   `Target = Punto_Breakout + Lunghezza_Asta` (per bandiera/pennant rialzista)
    *   `Target = Punto_Breakout - Lunghezza_Asta` (per bandiera/pennant ribassista)
*   **Durata:** Sono formazioni di breve durata, di solito durano da una a tre settimane.

---

## Formazione Wedge (Wedge Formation)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 6, Pagina 114-115 (Figure 6.15, 6.16, 6.17)
**Descrizione:** Una "wedge" (cuneo) è un pattern di continuazione o inversione caratterizzato da due linee di trend convergenti che sono entrambe inclinate nella stessa direzione (o entrambe verso l'alto o entrambe verso il basso). A differenza dei triangoli, dove le linee di trend convergono, nei cunei le linee sono quasi parallele ma con una leggera inclinazione l'una verso l'altra.
**Logica Tecnica/Pseudocodice:**
*   **Cuneo Rialzista (Rising Wedge):**
    1.  **Formazione:** Entrambe le linee di trend (superiore e inferiore) sono inclinate verso l'alto, ma la linea superiore ha una pendenza leggermente inferiore, o la linea inferiore una pendenza maggiore, portando a una convergenza. I massimi sono crescenti ma con una forza decrescente, e i minimi sono crescenti.
    2.  **Volume:** Generalmente in calo durante la formazione.
    3.  **Segnale:** Spesso si risolve con un breakout ribassista, segnalando una potenziale inversione di downtrend o una continuazione ribassista.
*   **Cuneo Ribassista (Falling Wedge):**
    1.  **Formazione:** Entrambe le linee di trend (superiore e inferiore) sono inclinate verso il basso, ma la linea inferiore ha una pendenza leggermente superiore, o la linea superiore una pendenza minore, portando a una convergenza. I minimi sono decrescenti ma con una forza decrescente, e i massimi sono decrescenti.
    2.  **Volume:** Generalmente in calo durante la formazione.
    3.  **Segnale:** Spesso si risolve con un breakout rialzista, segnalando una potenziale inversione di uptrend o una continuazione rialzista.
*   **Differenza dai Triangoli:** I cunei sono inclinati in una direzione specifica, mentre i triangoli sono orizzontali o simmetrici. I cunei spesso indicano inversioni.
*   **Target di Prezzo:** Misura la base del cuneo (la larghezza massima) e proietta la distanza dal punto di rottura.

---

## Rettangoli (Rectangles)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 6, Pagina 116-117 (Figure 6.18, 6.19, 6.20)
**Descrizione:** Un rettangolo è una formazione di continuazione o inversione in cui il prezzo si muove tra due linee orizzontali parallele di supporto e resistenza. Indica un periodo di consolidamento o indecisione, con la domanda e l'offerta relativamente bilanciate.
**Logica Tecnica/Pseudocodice:**
*   **Formazione:**
    1.  **Trend Preesistente:** Può essere in un uptrend o downtrend.
    2.  **Consolidamento:** Il prezzo si muove orizzontalmente, toccando almeno due volte un livello di resistenza orizzontale e due volte un livello di supporto orizzontale.
    3.  **Volume:** Tende a diminuire durante la formazione del rettangolo e ad aumentare significativamente al momento del breakout.
*   **Segnale di Trading:**
    *   **Breakout:** Una chiusura significativa al di sopra della resistenza (per un breakout rialzista) o al di sotto del supporto (per un breakout ribassista).
    *   **Target di Prezzo:** Misura l'altezza verticale del rettangolo. Proietta questa distanza dal punto di breakout nella direzione del breakout.
    *   `Target = Punto_Breakout + Altezza_Rettangolo` (rialzista)
    *   `Target = Punto_Breakout - Altezza_Rettangolo` (ribassista)
*   **Ruolo:** Principalmente un pattern di continuazione, ma può anche essere un pattern di inversione, specialmente se si verifica dopo un lungo trend o se è di grandi dimensioni.

---

## Measured Move (Misurazione del Movimento)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 6, Pagina 118-119 (Figure 6.21, 6.22)
**Descrizione:** Il "measured move" è un concetto che suggerisce che dopo un movimento di prezzo iniziale (gamba A), seguito da una correzione o consolidamento (gamba B), il movimento successivo (gamba C) sarà di una lunghezza simile alla gamba iniziale (A). È un metodo per prevedere obiettivi di prezzo.
**Logica Tecnica/Pseudocodice:**
*   **Measured Move Up (Rialzista):**
    1.  **Gamba A (Impulso Iniziale):** Identifica un forte movimento al rialzo da un minimo (Punto 1) a un massimo (Punto 2).
    2.  **Gamba B (Correzione):** Segue una correzione o un periodo di consolidamento da Punto 2 a Punto 3.
    3.  **Gamba C (Impulso Successivo):** Il prezzo inizia un nuovo movimento al rialzo da Punto 3.
    4.  **Target di Prezzo:** La lunghezza della gamba C sarà approssimativamente uguale alla lunghezza della gamba A.
    *   `Target = Punto_3 + (Punto_2 - Punto_1)`
*   **Measured Move Down (Ribassista):**
    1.  **Gamba A (Impulso Iniziale):** Identifica un forte movimento al ribasso da un massimo (Punto 1) a un minimo (Punto 2).
    2.  **Gamba B (Correzione):** Segue una correzione o un periodo di consolidamento da Punto 2 a Punto 3.
    3.  **Gamba C (Impulso Successivo):** Il prezzo inizia un nuovo movimento al ribasso da Punto 3.
    4.  **Target di Prezzo:** La lunghezza della gamba C sarà approssimativamente uguale alla lunghezza della gamba A.
    *   `Target = Punto_3 - (Punto_1 - Punto_2)`

---

## Formazione a "Testa e Spalle" di Continuazione (Head & Shoulders Continuation Pattern)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 6, Pagina 120-121 (Figure 6.23, 6.24, 6.25)
**Descrizione:** Sebbene le formazioni Head & Shoulders siano generalmente pattern di inversione, possono occasionalmente apparire come pattern di continuazione, indicando una pausa in un trend forte prima che il movimento riprenda nella stessa direzione.
**Logica Tecnica/Pseudocodice:**
*   **Formazione in Uptrend (Rialzista):**
    1.  **Trend Preesistente:** Uptrend forte.
    2.  **Pattern:** Una formazione che assomiglia a un Testa e Spalle rovesciata (o una forma più complessa di consolidamento) si sviluppa. La "testa" e le "spalle" sono orientate in modo che i minimi siano crescenti.
    3.  **Neckline:** Si forma una neckline inclinata al rialzo.
    4.  **Segnale:** La rottura al rialzo della neckline con volume in aumento conferma la continuazione dell'uptrend.
*   **Formazione in Downtrend (Ribassista):**
    1.  **Trend Preesistente:** Downtrend forte.
    2.  **Pattern:** Una formazione che assomiglia a un Testa e Spalle normale (o una forma più complessa di consolidamento) si sviluppa. La "testa" e le "spalle" sono orientate in modo che i massimi siano decrescenti.
    3.  **Neckline:** Si forma una neckline inclinata al ribasso.
    4.  **Segnale:** La rottura al ribasso della neckline con volume in aumento conferma la continuazione del downtrend.
*   **Differenza dall'Inversione:** La differenza chiave è che queste formazioni si verificano nel mezzo di un trend forte e non al suo culmine, e la rottura conferma la continuazione piuttosto che l'inversione.

---

## Convergenze e Divergenze (Conformity and Divergence)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 6, Pagina 122
**Descrizione:** Le convergenze e divergenze si riferiscono al confronto tra il movimento del prezzo e il movimento di un indicatore tecnico (come volume, open interest o oscillatori).
*   **Convergenza:** Quando prezzo e indicatore si muovono nella stessa direzione, confermando il trend.
*   **Divergenza:** Quando prezzo e indicatore si muovono in direzioni opposte, suggerendo una potenziale debolezza del trend e una possibile inversione.
**Logica Tecnica/Pseudocodice:**
*   **Convergenza Rialzista:**
    *   Prezzo fa minimi crescenti O massimi crescenti E indicatore fa minimi crescenti O massimi crescenti. (Conferma uptrend)
*   **Convergenza Ribassista:**
    *   Prezzo fa massimi decrescenti O minimi decrescenti E indicatore fa massimi decrescenti O minimi decrescenti. (Conferma downtrend)
*   **Divergenza Rialzista (Bullish Divergence):**
    *   Prezzo fa un nuovo minimo inferiore E indicatore (es. RSI, MACD) fa un minimo superiore.
    *   *Interpretazione:* Suggerisce che il momentum di vendita sta diminuendo e che un'inversione al rialzo potrebbe essere imminente.
*   **Divergenza Ribassista (Bearish Divergence):**
    *   Prezzo fa un nuovo massimo superiore E indicatore (es. RSI, MACD) fa un massimo inferiore.
    *   *Interpretazione:* Suggerisce che il momentum di acquisto sta diminuendo e che un'inversione al ribasso potrebbe essere imminente.
*   **Applicazione:** Le divergenze sono considerate segnali di trading più potenti rispetto alle convergenze, indicando spesso una debolezza nel trend attuale.

---

## Interpretazione Volume e Open Interest (Volume & Open Interest Interpretation)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 7, Pagina 123-137
**Descrizione:** L'analisi congiunta di volume e open interest (specialmente nei futures) fornisce indicazioni cruciali sulla forza e sostenibilità di un trend o sulla potenziale inversione. Il volume riflette l'interesse corrente, mentre l'open interest mostra l'impegno di capitale nel mercato.
**Logica Tecnica/Pseudocodice:**
*   **Combinazioni di Prezzo, Volume e Open Interest per i FUTURES:**
    1.  **Prezzo Up, Volume Up, OI Up:** Rialzo forte e sostenibile. Nuovo denaro sta entrando nel mercato. (FORTE RIALZO)
    2.  **Prezzo Up, Volume Down, OI Down:** Rialzo debole. Gli acquirenti sono pochi e le posizioni lunghe vengono chiuse. (DEBOLE RIALZO)
    3.  **Prezzo Down, Volume Up, OI Up:** Ribasso forte e sostenibile. Nuovo denaro sta entrando nel mercato per posizioni corte. (FORTE RIBASSO)
    4.  **Prezzo Down, Volume Down, OI Down:** Ribasso debole. Le posizioni corte vengono chiuse. Potenziale inversione al rialzo. (DEBOLE RIBASSO)
    5.  **Prezzo Laterale, Volume Down, OI Down:** Mercato in attesa. I partecipanti si ritirano. Potenziale rottura nella direzione del trend precedente.
    6.  **Prezzo Laterale, Volume Up, OI Up:** Accumulazione (se il prezzo rompe al rialzo) o distribuzione (se il prezzo rompe al ribasso).
*   **Regole Aggiuntive:**
    *   **Blow-offs (Esplosioni di Volume):** Picchi di volume estremamente elevati in un uptrend o downtrend finale, spesso accompagnati da ampi range di prezzo e successiva inversione rapida. Segnalano esaurimento.
    *   **Selling Climaxes (Climax di Vendita):** Simili ai blow-offs ma con forte pressione di vendita in un downtrend.
    *   **Open Interest nelle Opzioni:** Un alto open interest nelle opzioni CALL (put) può indicare una resistenza (supporto) psicologica. Le posizioni put/call dei trader grandi vs piccoli possono indicare sentiment contrarian.

---

## Analisi Grafici di Lungo Periodo (Long-Term Chart Analysis)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 8, Pagina 143-153
**Descrizione:** L'analisi dei grafici settimanali e mensili è fondamentale per ottenere una prospettiva più ampia del mercato, identificare i trend primari e i principali livelli di supporto e resistenza che non sono visibili sui grafici giornalieri. Aiuta a contestualizzare i movimenti di prezzo a breve termine e a definire strategie di trading/investimento a lungo termine.
**Logica Tecnica/Pseudocodice:**
*   **Input:** Dati di prezzo aggregati su base settimanale e mensile.
*   **Costruzione:** Grafici a barre, lineari o candlestick settimanali/mensili.
*   **Scopo:**
    1.  **Identificazione Trend Primari:** I trend più significativi sono visibili più chiaramente sui grafici a lungo termine.
    2.  **Principali Supporti/Resistenze:** I livelli di supporto e resistenza di lungo periodo sono più robusti e difficili da rompere.
    3.  **Filtraggio del Rumore:** I movimenti di prezzo a breve termine (rumore) sono attenuati, consentendo una visione più chiara dei pattern macro.
    4.  **Conferma dei Segnali:** Un segnale di breakout o inversione su un grafico giornaliero è più affidabile se è confermato o non contraddetto da un grafico di lungo periodo.
    5.  **Inflazione:** Considerare l'impatto dell'inflazione sull'aspetto dei grafici a lungo termine per evitare distorsioni nella percezione dei prezzi reali.
*   **Regola:** Le strategie di trading basate su grafici a lungo termine sono più adatte per gli investitori che non sono attivi nel trading a breve termine.

---

## Media Mobile (Moving Average - General)
**Libro/File Originale:** Analisi Tecnica dei Mercati Finanziari
**Contesto/Pagina:** Capitolo 9, Pagina 155-171
**Descrizione:** Una media mobile è un indicatore tecnico che smussa l'azione dei prezzi filtrando il "rumore" di mercato e aiuta a identificare la direzione del trend. È calcolata come la media dei prezzi in un dato periodo di tempo e aggiornata continuamente. Le medie mobili sono strumenti versatili e possono essere usate per generare segnali di acquisto/vendita.
**Logica Tecnica/Pseudocodice:**
*   **Parametri:** `Periodo` (es. 10, 20, 50, 200 giorni/settimane) e `Tipo` (Semplice, Esponenziale, Ponderata, Adattiva).
*   **Tipi di Media Mobile:**
    *   **Media Mobile Semplice (SMA):** `SMA_N = (Somma_Prezzi_N_Periodi_Precedenti) / N`
    *   **Media Mobile Ponderata Linearmente (LWMA):** Assegna più peso ai prezzi più recenti.
    *