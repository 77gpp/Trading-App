# SKILLS ESTRATTE: Joe Ross - Daytrading (Merged Clean)



### [PARTE 1: merged_clean_part_01_p1-40.pdf]

## Daytrading (Conceptual)
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 9, "Daytrading e position trading"
**Descrizione:** Daytrading è una modalità di trading che si concentra su operazioni di breve termine, tipicamente aperte e chiuse all'interno della stessa giornata di trading. L'autore sottolinea che, sebbene le dinamiche dei grafici intraday e giornalieri abbiano delle somiglianze, il daytrading richiede decisioni più frequenti e una gestione diversa della volatilità e della dimensione dei movimenti di prezzo. Consente di massimizzare i profitti "lasciando meno denaro sul tavolo" rispetto al position trading giornaliero senza entrate intraday. Richiede grande disciplina per evitare l'eccesso di trading.
**Logica Tecnica/Pseudocodice:** Non applicabile, è una descrizione concettuale della metodologia di trading.

---

## Position Trading Intraday (Conceptual)
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 17, "Dato che il daytrading è così intenso..."
**Descrizione:** Il position trading intraday è una strategia in cui un daytrade di brevissimo termine viene convertito in un trade di maggiore durata, ma comunque chiuso entro la stessa giornata. È considerato più rilassato del daytrading puro, in quanto i trade tendono a "prendersi cura di sé". L'obiettivo è monitorare il trade per spostare uno stop di protezione dei profitti e uscire ai target definiti, cercando di essere "stoppato con un profitto". L'autore ha smesso di cercare i massimi e i minimi del mercato.
**Logica Tecnica/Pseudocodice:**
```
IF (current_trade_is_short_term_daytrade AND potential_for_longer_move) THEN
    convert_to_position_trade_intraday()
    monitor_trade_for_profit_protection()
    move_profit_protection_stop_to_target() // Stop coincides with target, aim for stop-out with profit
    EXIT_TRADE_AT_DEFINED_TARGETS()
END IF
```

---

## La Legge Dei Grafici (The Law Of Charts - TLOC)
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 19, "La Legge dei Grafici"
**Descrizione:** La Legge dei Grafici (TLOC) è un principio che afferma che qualsiasi grafico a barre, mostrando valori massimi e minimi per un dato intervallo temporale, presenterà sempre quattro schemi grafici definiti: Formazioni 1-2-3 (massimo e minimo), Ledge, Trading Range e Ross Hook (Uncino di Ross). Questi schemi sono considerati fondamentali per l'analisi dei movimenti di prezzo.
**Logica Tecnica/Pseudocodice:** Non applicabile, è una legge generale del comportamento dei prezzi.

---

## Formazione 1-2-3 Massimo (1-2-3 Top Formation)
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 20, "Formazioni 1-2-3 massimo e minimo"
**Descrizione:** Una formazione 1-2-3 massimo si sviluppa tipicamente alla fine di un trend al rialzo. I prezzi formano un massimo finale (Punto 1), poi scendono per iniziare una correzione al rialzo fino al Punto 2. Successivamente, i prezzi salgono fino al Punto 3, da cui riprendono un movimento al ribasso, formando il pivot. I punti 2 e 3 possono essere definiti solo dopo una correzione completa.
**Logica Tecnica/Pseudocodice:**
```
// Definizione di un "Massimo 1-2-3"
// Precondizione: Mercato in uptrend
Point_1_is_identified = FALSE
Point_2_is_identified = FALSE
Point_3_is_identified = FALSE

// Punto 1: Ultima barra che forma un nuovo massimo nel movimento al rialzo più recente.
IF (current_bar.High == max_high_in_recent_uptrend) THEN
    Point_1_High = current_bar.High
    Point_1_Index = current_bar.Index
    Point_1_is_identified = TRUE
END IF

// I prezzi scendono dal Punto 1, poi inizia una correzione al rialzo.
// Punto 2: Si verifica una "correzione completa" dal movimento di discesa dal Punto 1.
// Correzione completa per Punto 2 (rispetto al movimento verso l'alto dal potenziale Punto 2):
// UNA singola barra con (High > previous_bar.High AND Low > previous_bar.Low)
// OPPURE una combinazione di MAX 3 barre con (Higher High AND Higher Low) rispetto alla barra precedente.
IF (Point_1_is_identified AND prices_move_down_from_Point_1) THEN
    IF (CompleteCorrectionOccurs(from: potential_Point_2_level, direction: up)) THEN
        Point_2_Low = lowest_low_after_Point_1_before_correction_up
        Point_2_Index = index_of_Point_2_Low
        Point_2_is_identified = TRUE
    END IF
END IF

// I prezzi salgono dal Punto 2, poi riprendono il movimento al ribasso.
// Punto 3: Si verifica una "correzione completa" dal movimento di discesa dal potenziale Punto 3.
// Correzione completa per Punto 3 (rispetto al movimento verso il basso dal potenziale Punto 3):
// UNA singola barra con (Low < previous_bar.Low AND High < previous_bar.High)
// OPPURE una combinazione di MAX 3 barre con (Lower Low AND Lower High) rispetto alla barra precedente.
IF (Point_2_is_identified AND prices_move_up_from_Point_2) THEN
    IF (CompleteCorrectionOccurs(from: potential_Point_3_level, direction: down)) THEN
        Point_3_High = highest_high_after_Point_2_before_correction_down
        Point_3_Index = index_of_Point_3_High
        Point_3_is_identified = TRUE
    END IF
END IF

IF (Point_1_is_identified AND Point_2_is_identified AND Point_3_is_identified) THEN
    // Formazione 1-2-3 Massimo completata
    1_2_3_Top_Formation_Exists = TRUE
END IF

// Congestione
// Dopo 3 barre si considera una congestione (nel contesto della correzione per punto 2)
// (Descrizione più approfondita della congestione verrà fornita in seguito nel corso, Pg 21)

// Possibile che i punti 1 e 2 si verifichino nella stessa barra (Pg 21)
// Possibile che i punti 2 e 3 si verifichino nella stessa barra (Pg 21)
```

---

## Formazione 1-2-3 Minimo (1-2-3 Bottom Formation)
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 22, "Ora esaminiamo un minimo 1-2-3"
**Descrizione:** Una formazione 1-2-3 minimo si sviluppa tipicamente alla fine di un trend al ribasso. I prezzi formano un minimo finale (Punto 1), poi salgono per iniziare una correzione al ribasso fino al Punto 2. Successivamente, i prezzi scendono fino al Punto 3, da cui riprendono un movimento al rialzo, formando il pivot. I punti 2 e 3 possono essere definiti solo dopo una correzione completa.
**Logica Tecnica/Pseudocodice:**
```
// Definizione di un "Minimo 1-2-3"
// Precondizione: Mercato in downtrend
Point_1_is_identified = FALSE
Point_2_is_identified = FALSE
Point_3_is_identified = FALSE

// Punto 1: Ultima barra che forma un nuovo minimo nel movimento al ribasso più recente.
IF (current_bar.Low == min_low_in_recent_downtrend) THEN
    Point_1_Low = current_bar.Low
    Point_1_Index = current_bar.Index
    Point_1_is_identified = TRUE
END IF

// I prezzi salgono dal Punto 1, poi inizia una correzione al ribasso.
// Punto 2: Si verifica una "correzione completa" dal movimento di salita dal Punto 1.
// Correzione completa per Punto 2 (rispetto al movimento verso il basso dal potenziale Punto 2):
// UNA singola barra con (Low < previous_bar.Low AND High < previous_bar.High)
// OPPURE una combinazione di MAX 3 barre con (Lower Low AND Lower High) rispetto alla barra precedente.
IF (Point_1_is_identified AND prices_move_up_from_Point_1) THEN
    IF (CompleteCorrectionOccurs(from: potential_Point_2_level, direction: down)) THEN
        Point_2_High = highest_high_after_Point_1_before_correction_down
        Point_2_Index = index_of_Point_2_High
        Point_2_is_identified = TRUE
    END IF
END IF

// I prezzi scendono dal Punto 2, poi riprendono il movimento al rialzo.
// Punto 3: Si verifica una "correzione completa" dal movimento di salita dal potenziale Punto 3.
// Correzione completa per Punto 3 (rispetto al movimento verso l'alto dal potenziale Punto 3):
// UNA singola barra con (High > previous_bar.High AND Low > previous_bar.Low)
// OPPURE una combinazione di MAX 3 barre con (Higher High AND Higher Low) rispetto alla barra precedente.
IF (Point_2_is_identified AND prices_move_down_from_Point_2) THEN
    IF (CompleteCorrectionOccurs(from: potential_Point_3_level, direction: up)) THEN
        Point_3_Low = lowest_low_after_Point_2_before_correction_up
        Point_3_Index = index_of_Point_3_Low
        Point_3_is_identified = TRUE
    END IF
END IF

IF (Point_1_is_identified AND Point_2_is_identified AND Point_3_is_identified) THEN
    // Formazione 1-2-3 Minimo completata
    1_2_3_Bottom_Formation_Exists = TRUE
END IF

// Congestione
// Dopo 3 barre si considera una congestione (nel contesto della correzione per punto 2)
// (Descrizione più approfondita della congestione verrà fornita in seguito nel corso, Pg 23)

// Possibile che i punti 1 e 2 si verifichino nella stessa barra (Pg 23)
// Possibile che i punti 2 e 3 si verifichino nella stessa barra (Pg 24)
```

---

## Invalidazione Formazione 1-2-3 (1-2-3 Formation Invalidation)
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 24, "L'intero massimo o minimo 1-2-3 è annullato..."
**Descrizione:** Una formazione 1-2-3 (sia massimo che minimo) viene annullata se una barra di prezzo si muove fino a, o oltre, il Punto 1 della formazione.
**Logica Tecnica/Pseudocodice:**
```
// Per 1-2-3 Massimo:
IF (current_bar.High >= Point_1_High) THEN
    1_2_3_Top_Formation_Invalidated = TRUE
END IF

// Per 1-2-3 Minimo:
IF (current_bar.Low <= Point_1_Low) THEN
    1_2_3_Bottom_Formation_Invalidated = TRUE
END IF
```

---

## Ledge Pattern
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 25, "Ledge"
**Descrizione:** Una "Ledge" è un pattern di continuazione che indica una pausa nel trend esistente. Comprende un minimo di 4 barre di prezzo e un massimo di 10 barre. Deve avere almeno due minimi allineati e due massimi allineati. I massimi allineati devono essere separati da almeno una barra di prezzo, così come i minimi allineati. Gli allineamenti non devono essere necessariamente esatti, ma non devono essere distanti più di tre tick. Se ci sono più di due allineamenti, si possono considerare i due più recenti ("a") o quelli estremi ("b"). La Ledge deve verificarsi all'interno di un trend, e si prevede che il trend continui dopo la sua rottura.
**Logica Tecnica/Pseudocodice:**
```
// Definizione di una "Ledge"
// Precondizione: Mercato in un trend esistente

// Parametri:
min_bars = 4
max_bars = 10
max_tick_distance = 3 // Per l'allineamento

// Step 1: Identificare un periodo di prezzo tra min_bars e max_bars
// Step 2: Trovare i massimi e i minimi all'interno di questo periodo.
// Step 3: Verificare i massimi allineati:
// Ci devono essere almeno due massimi (H1, H2) tali che H1_Index < H2_Index.
// H2_Index - H1_Index > 1 (separati da almeno una barra).
// ABS(H1 - H2) <= max_tick_distance.
// (Possibile: più di 2 massimi, considerare "a" i più recenti, "b" gli estremi)

// Step 4: Verificare i minimi allineati:
// Ci devono essere almeno due minimi (L1, L2) tali che L1_Index < L2_Index.
// L2_Index - L1_Index > 1 (separati da almeno una barra).
// ABS(L1 - L2) <= max_tick_distance.
// (Possibile: più di 2 minimi, considerare "a" i più recenti, "b" gli estremi)

IF (Step_1_is_met AND Step_3_is_met AND Step_4_is_met) THEN
    Ledge_Exists = TRUE
    // Si prevede la continuazione del trend dopo la rottura della Ledge
END IF
```

---

## Trading Range Pattern
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 26, "Trading range"
**Descrizione:** Una "Trading Range" è simile a una Ledge, ma deve essere composta da più di dieci barre di prezzo. Le trading range con 10-20 barre sono generalmente di modesta importanza. Tipicamente, tra le barre 20 e 30 (cioè barre 21-29), si verificherà una rottura del massimo o del minimo della trading range, definita dalle barre precedenti alla rottura. Questo pattern implica un consolidamento dei prezzi prima di un'esplosione direzionale.
**Logica Tecnica/Pseudocodice:**
```
// Definizione di una "Trading Range"

// Parametri:
min_bars_for_TR = 11 // "più di dieci barre"

// Step 1: Identificare un periodo di prezzo con più di 10 barre.
// Step 2: Verificare la presenza di massimi e minimi consolidati che definiscono i confini della range.
// (Definizione simile a Ledge, ma con numero di barre maggiore)

IF (num_bars_in_range > 10) THEN
    Trading_Range_Exists = TRUE
END IF

// Aspettativa di breakout:
IF (Trading_Range_Exists AND num_bars_in_range >= 21 AND num_bars_in_range <= 29) THEN
    EXPECT_BREAKOUT_OF_TR_HIGH_OR_LOW = TRUE
END IF
```

---

## Ross Hook (Uncino di Ross)
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 26-27, "Ross Hook: l'Uncino di Ross"
**Descrizione:** Un Ross Hook (RH) si forma come il primo punto in cui i prezzi non riescono a proseguire nella direzione precedente, dopo la rottura di un pattern di consolidamento o inversione. Può formarsi in tre scenari principali:
1. Dopo la rottura di una formazione 1-2-3 (massimo o minimo).
2. Dopo la rottura di una Ledge.
3. Dopo la rottura di una Trading Range.

Esempi specifici:
- **In mercato al rialzo, dopo rottura di un minimo 1-2-3:** Il primo punto in cui una barra di prezzo non riesce a formare un nuovo massimo crea un RH (anche un doppio massimo crea un RH).
- **In mercato al ribasso, dopo rottura di un massimo 1-2-3:** Il primo punto in cui una barra di prezzo non riesce a formare un nuovo minimo crea un RH (anche un doppio minimo crea un RH).
- **Dopo rottura verso l'alto di Ledge o Trading Range:** Il primo punto in cui una barra di prezzo non riesce a formare un nuovo massimo crea un RH.
- **Dopo rottura verso il basso di Ledge o Trading Range:** Il primo punto in cui una barra di prezzo non riesce a formare un nuovo minimo crea un RH (anche un doppio massimo o minimo creano un RH).
**Logica Tecnica/Pseudocodice:**
```
// Definizione di un "Ross Hook" (RH)

// Scenario 1: Dopo la rottura di un 1-2-3 Top/Bottom
IF (1_2_3_Top_Broken_Downwards OR 1_2_3_Bottom_Broken_Upwards) THEN
    IF (Current_Price_Action_Fails_To_Continue_Direction) THEN
        Ross_Hook_Created = TRUE
    END IF
END IF

// Scenario 2: Dopo la rottura di una Ledge
IF (Ledge_Broken_Upwards OR Ledge_Broken_Downwards) THEN
    IF (Current_Price_Action_Fails_To_Continue_Direction) THEN
        Ross_Hook_Created = TRUE
    END IF
END IF

// Scenario 3: Dopo la rottura di una Trading Range
IF (Trading_Range_Broken_Upwards OR Trading_Range_Broken_Downwards) THEN
    IF (Current_Price_Action_Fails_To_Continue_Direction) THEN
        Ross_Hook_Created = TRUE
    END IF
END IF

// Specifiche per l'identificazione del "Fails To Continue Direction":
// Per RH in un Uptrend (dopo rottura di 1-2-3 Minimo o Ledge/TR verso l'alto):
// Condizione: Prezzi salgono, poi una barra non riesce a formare un nuovo massimo.
// O crea un doppio massimo.
IF (current_trend == UP AND current_bar.High <= previous_bar.High AND current_bar.Low < previous_bar.Low) THEN // Simplified for "fails to form new high"
    Ross_Hook_High_Created = TRUE
END IF

// Per RH in un Downtrend (dopo rottura di 1-2-3 Massimo o Ledge/TR verso il basso):
// Condizione: Prezzi scendono, poi una barra non riesce a formare un nuovo minimo.
// O crea un doppio minimo.
IF (current_trend == DOWN AND current_bar.Low >= previous_bar.Low AND current_bar.High > previous_bar.High) THEN // Simplified for "fails to form new low"
    Ross_Hook_Low_Created = TRUE
END IF
```

---

## Calcolo dei Segmenti (Segment Calculation)
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 7, "Un nuovo testo" and Page 31, "calcolo dei segmenti"
**Descrizione:** Un metodo di trading descritto come molto preciso e basato su regole definite e costanti, al punto da poter essere automatizzato con l'intelligenza artificiale. L'autore sottolinea che è stato utilizzato con successo per oltre 126 anni nel position trading e funziona in qualsiasi intervallo temporale, purché sia disponibile un grafico. È una tecnica per operare includendo automaticamente le singole componenti di un mercato, derivando dai concetti sulle congestioni allineate.
**Logica Tecnica/Pseudocodice:** Non specificata nel dettaglio in queste pagine, ma descritta come:
```
// Metodo di trading con regole definite e costanti
FUNCTION CalculateSegments(price_data)
    // Passi dettagliati per il calcolo dei segmenti (non specificati nel testo)
    // Basato sui concetti di "congestioni allineate"
    // Esempio: identifica punti di svolta, livelli di supporto/resistenza, etc.
    RETURN trading_signals
END FUNCTION
```

---

## Regola per la Dimensione dei Contratti (Contract Sizing Rule)
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 7, "Un nuovo testo"
**Descrizione:** Per il numero di contratti, l'autore suggerisce di utilizzare almeno un set di due contratti. Oltre i 5 contratti, raccomanda di utilizzare incrementi di 5 (es. 10, 15, 20, 25). Si preferisce uscire dal mercato con un lotto "non tondo" per minimizzare lo slippage sulla fase di profitto, piuttosto che entrare con un lotto non tondo e subire slippage sul costo iniziale del trade.
**Logica Tecnica/Pseudocodice:**
```
// Regola per la dimensione dei contratti
IF (desired_contracts <= 5) THEN
    contract_size = 2 OR 3 OR 4 OR 5
ELSE IF (desired_contracts > 5) THEN
    contract_size = CEILING(desired_contracts / 5) * 5 // E.g., 6 contracts -> 10, 11 -> 15
END IF

// Gestione dello slippage all'uscita
// Better to incur slippage on profit portion than entry cost
// Avoid "non-round lots" for entry, use for exit
IF (EXIT_TRADE) THEN
    exit_contract_size = non_round_lot // E.g., 9 contracts, liquidate 4 to cover costs, 5 remaining.
                                       // Or 10 contracts, liquidate 4, 6 remaining (non-round).
ELSE IF (ENTER_TRADE) THEN
    enter_contract_size = round_lot // Preferred for entry to minimize slippage on cost
END IF
```

---

## Scelta del Mercato per Daytrading
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 32, "Scegliere un mercato"
**Descrizione:** I mercati ideali per il daytrading intraday devono soddisfare i seguenti criteri:
1.  **Trend su Intervalli Maggiori:** Essere in trend su un intervallo temporale più grande di quello usato per i segnali di entrata.
2.  **Liquidità:** Essere liquidi, con un'azione dei prezzi solida e un buon movimento sul grafico intraday.
3.  **Movimento di Prezzi:** Avere un'ampia movimentazione dei prezzi a causa di eventi attuali, indipendentemente dalla direzione (rialzo o ribasso).
4.  **Potenziale di Profitto:** Avere un movimento di prezzi sufficientemente ampio da consentire un guadagno significativo catturando una parte di tale movimento.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION SelectMarketForDaytrading(market_data, current_timeframe_for_entries)
    // Criterio 1: Trend su intervallo maggiore
    long_term_trend = GetTrend(market_data, current_timeframe_for_entries.magnified_timeframe)
    IF (long_term_trend == NOT_TRENDING) THEN
        RETURN FALSE // Escludi se non è in trend su un timeframe maggiore
    END IF

    // Criterio 2: Liquidità e buona azione dei prezzi intraday
    intraday_liquidity = CheckLiquidity(market_data, current_timeframe_for_entries)
    intraday_price_action_quality = CheckPriceActionQuality(market_data, current_timeframe_for_entries)
    IF (intraday_liquidity < MIN_LIQUIDITY OR intraday_price_action_quality < MIN_PRICE_ACTION_QUALITY) THEN
        RETURN FALSE // Escludi se manca liquidità o qualità dell'azione dei prezzi
    END IF

    // Criterio 3: Movimento di prezzi ampio (volatilità)
    price_movement_magnitude = CalculateAverageDailyRange(market_data) // O basato su eventi attuali
    IF (price_movement_magnitude < MIN_PRICE_MOVEMENT) THEN
        RETURN FALSE // Escludi se il movimento è troppo piccolo
    END IF

    // Criterio 4: Potenziale di profitto sufficiente
    profit_potential = CalculateProfitPotential(price_movement_magnitude, typical_trade_slice)
    IF (profit_potential < MIN_PROFIT_POTENTIAL) THEN
        RETURN FALSE // Escludi se il potenziale di profitto è insufficiente
    END IF

    RETURN TRUE // Il mercato è adatto per il daytrading
END FUNCTION
```

---

## Scelta dell'Intervallo Temporale per Daytrading
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 32, "Scegliere un intervallo temporale"
**Descrizione:** Si sconsiglia di fare trading su grafici con intervalli temporali troppo brevi che non permettono di vedere chiaramente i pattern definiti dalla "Legge dei Grafici". La chiarezza del pattern è più importante della velocità del timeframe.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION SelectTimeframe(available_timeframes)
    FOR EACH timeframe IN available_timeframes
        IF (timeframe.allows_clear_view_of_TLOC_patterns) THEN
            RETURN timeframe // Scegli il primo timeframe che permette chiarezza
        END IF
    END FOR
    RETURN NULL // Nessun timeframe adatto trovato
END FUNCTION
```

---

## Strategia di Entrata basata sulla Spinta (Momentum/Thrust-based Entry Strategy)
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 32, "Scegliere un punto di entrata" and Page 33, "Ciò di cui stiamo parlando è la spinta."
**Descrizione:** Le tecniche di entrata si basano su tre livelli (principali, intermedi, minori) ma hanno in comune la "spinta" (momentum). Si preferisce entrare in trade intraday basati su eventi significativi derivanti dalla spinta e dal momentum di un intervallo temporale maggiore. Un evento significativo è una rottura del massimo o del minimo della barra di prezzo precedente, specialmente se il movimento è sufficientemente grande.
**Logica Tecnica/Pseudocodice:**
```
// Entrata basata sulla spinta/momentum
// Precondizione: Mercato selezionato e timeframe scelti.

FUNCTION GenerateEntrySignal(current_market_data, higher_timeframe_data)
    // Preferenza per eventi significativi da timeframe maggiori
    significant_event_from_higher_timeframe = CheckForSignificantThrustEvent(higher_timeframe_data)

    IF (significant_event_from_higher_timeframe == TRUE) THEN
        // Esempio di evento significativo: rottura di massimo/minimo di barra precedente
        IF (current_bar.High > previous_bar.High_of_higher_timeframe_bar AND movement_magnitude_is_sufficient) THEN
            RETURN BUY_SIGNAL // Entra long sulla rottura del massimo con sufficiente spinta
        END IF
        IF (current_bar.Low < previous_bar.Low_of_higher_timeframe_bar AND movement_magnitude_is_sufficient) THEN
            RETURN SELL_SIGNAL // Entra short sulla rottura del minimo con sufficiente spinta
        END IF
    END IF

    // Le tecniche di entrata includono quelle "principali, intermedie e minori"
    // Tutte queste sono caratterizzate dalla "spinta" (thrust/momentum)
    // Non vengono comprati/venduti i ritracciamenti (correzioni) in corso
    // Non si compra/vende in canali o trading range a meno che il singolo movimento non sia sufficientemente ampio
    RETURN NO_SIGNAL
END FUNCTION
```

---

## Non Trading su Ritracciamenti/Correzioni in Corso
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 32, "Scegliere un punto di entrata"
**Descrizione:** Non si devono comprare o vendere ritracciamenti (correzioni) mentre sono in corso. L'enfasi è sul trading nella direzione della spinta/momentum, non sul contro-trend durante le correzioni.
**Logica Tecnica/Pseudocodice:**
```
IF (current_market_is_retracing_or_correcting_against_main_thrust_direction) THEN
    DO_NOT_ENTER_TRADE = TRUE // Non comprare/vendere ritracciamenti in corso
END IF
```

---

## Trading in Canali o Trading Range (Regola Condizionale)
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 32, "Scegliere un punto di entrata"
**Descrizione:** Non si comprano o vendono asset all'interno di un canale o di una trading range, a meno che un singolo movimento all'interno di tale struttura non abbia un'ampiezza sufficiente a garantire un trade profittevole.
**Logica Tecnica/Pseudocodice:**
```
IF (market_is_in_channel OR market_is_in_trading_range) THEN
    IF (single_movement_amplitude < MIN_AMPLITUDE_FOR_PROFITABLE_TRADE) THEN
        DO_NOT_ENTER_TRADE = TRUE
    ELSE
        // Permetti il trade se il movimento interno è abbastanza ampio
        ALLOW_TRADE_IN_CHANNEL_OR_RANGE = TRUE
    END IF
END IF
```

---

## Utilizzo dei Grafici Multi-Timeframe per Contestualizzazione
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 5, "Filtrare il trade", Page 34, "Non siamo preoccupati di ciò che è accaduto ieri...", Page 36, "Proprio come un trader..."
**Descrizione:** L'autore filtra i daytrade usando grafici su intervalli temporali più lunghi (giornalieri e settimanali). Sebbene l'attenzione del daytrader sia sul presente ("ciò che sta accadendo oggi"), gli eventi passati (anche di giorni precedenti) possono essere collegati all'azione corrente del mercato. L'ampiezza e la "spinta" dei movimenti osservati su timeframe maggiori (es. rottura di un Ross Hook su grafico giornaliero o settimanale) offrono opportunità di guadagno più consistenti rispetto a timeframe minori. Un daytrader non può trascurare le formazioni principali su grafici giornalieri o intraday con intervalli maggiori.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION FilterDaytrade(daytrade_signal, current_bar_data)
    // Filtrare usando timeframe superiori
    daily_chart_trend = GetTrend(daily_data)
    weekly_chart_trend = GetTrend(weekly_data)

    // Considerare il contesto storico per l'azione corrente
    historical_relevance = AnalyzeHistoricalEvents(past_day_data, day_before_past_day_data)

    // Valutare la spinta e l'ampiezza del movimento su timeframe maggiori
    higher_timeframe_thrust = EvaluateThrust(daily_data, weekly_data)

    // Esempio: Entrare in direzione del trend di timeframe superiori
    IF (daytrade_signal.direction == daily_chart_trend.direction AND
        daytrade_signal.direction == weekly_chart_trend.direction AND
        higher_timeframe_thrust > MIN_THRUST) THEN
        RETURN APPROVED_TRADE
    ELSE
        RETURN REJECTED_TRADE
    END IF
END FUNCTION
```

---

## Gestione del Rischio: Stop di Protezione dei Profitti e Obiettivi Definiti
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 17, "Dato che il daytrading è così intenso..."
**Descrizione:** L'autore monitora i trade per spostare uno stop di protezione dei profitti. Tipicamente, questo stop coincide con l'obiettivo di profitto ("Voglio essere stoppato con un profitto"). Questa è una forma di "trade management" piuttosto che di "money management". L'obiettivo non è cercare i massimi o i minimi del mercato, ma assicurarsi un profitto.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION ManageTrade(entry_price, current_price, target_price)
    IF (current_price > entry_price AND current_price >= target_price) THEN
        // Il prezzo ha raggiunto o superato il target
        // Spostare lo stop per garantire un profitto
        profit_protection_stop = target_price
        // L'obiettivo è essere stoppati con un profitto, quindi lo stop diventa il target.
        // Questo implica che una volta raggiunto il target, il trade si chiuderà per profitto o per stop a profitto.
    ELSE IF (current_price > entry_price AND current_price < target_price) THEN
        // Il prezzo è in profitto ma non ha ancora raggiunto il target.
        // Spostare lo stop in un punto che assicuri un profitto minimo (es. break-even o piccolo profitto)
        profit_protection_stop = MAX(entry_price, previous_profit_protection_stop) // Esempio: trailing stop
    END IF
END FUNCTION
```

---

## Segnali di Entrata Principali (Lista)
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 37, "I segnali di entrata principali sono i seguenti:"
**Descrizione:** I segnali di entrata principali hanno la massima priorità e sono tutti derivati dai pattern della "Legge dei Grafici" applicati al grafico a barre giornaliero.
**Logica Tecnica/Pseudocodice:**
```
// Segnali di Entrata Principali
// Precondizione: Analisi su grafico a barre giornaliero.

IF (Breakout_of_1_2_3_Top_Point_2_Occurs) THEN
    Generate_Primary_Entry_Signal("Sell")
END IF

IF (Breakout_of_1_2_3_Bottom_Point_2_Occurs) THEN
    Generate_Primary_Entry_Signal("Buy")
END IF

IF (Breakout_of_Ledge_Occurs) THEN
    Generate_Primary_Entry_Signal(Ledge_Breakout_Direction)
END IF

IF (Breakout_of_Trading_Range_Occurs) THEN
    Generate_Primary_Entry_Signal(Trading_Range_Breakout_Direction)
END IF

IF (Breakout_of_Ross_Hook_Occurs) THEN
    Generate_Primary_Entry_Signal(Ross_Hook_Breakout_Direction)
END IF
```

---

## Regola di Non-Entrata su Gap (No Gap Entries)
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 37, "In tutte queste tecniche basate sul grafico a barre..."
**Descrizione:** Le rotture che si verificano tramite un gap non vengono considerate come segnali di entrata validi. I gap annullano la potenziale entrata nel mercato. L'autore vuole entrare solo in trade in cui il prezzo "passa attraverso" il prezzo di entrata desiderato, indicando un'azione di prezzo continua.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION CheckForGapEntry(entry_price, current_price_action)
    IF (current_price_action_forms_a_gap_over_entry_price) THEN
        RETURN INVALID_ENTRY_SIGNAL // Annulla l'entrata se c'è un gap
    ELSE IF (current_price_action_moves_through_entry_price_without_gap) THEN
        RETURN VALID_ENTRY_SIGNAL // Entra solo se il prezzo passa "attraverso"
    END IF
END FUNCTION
```

---

## Focus sull'Azione dei Prezzi Corrente per Daytrading
**Libro/File Originale:** Daytrading (URI: N/A)
**Contesto/Pagina:** Page 34, "IMPORTANTE - Quando stiamo facendo daytrading..."
**Descrizione:** Quando si fa daytrading su un grafico intraday, l'interesse è esclusivamente su ciò che sta accadendo nel giorno corrente. Non ci si preoccupa della chiusura del mercato (che può essere lontana molte barre) né di ciò che accadrà domani. L'unico riferimento al passato è per capire come gli eventi storici possano essere collegati all'azione odierna, ma il focus primario è il presente.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION AssessDaytradingOpportunity(current_day_price_data)
    // Ignora chiusure future o eventi di domani per le decisioni immediate
    // current_day_price_data è l'input principale.
    // Analizza_solo_oggi(current_day_price_data)

    // Context from past days
    IF (history_data_relevant_to_current_action) THEN
        consider_historical_context()
    END IF

    // Decisione basata principalmente sulla realtà dei prezzi correnti.
    // ... logic for entry/exit ...
END FUNCTION
```

### [PARTE 2: merged_clean_part_02_p41-80.pdf]

## Minimo 1-2-3
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 1 (OCR 52)
**Descrizione:** Un minimo 1-2-3 si forma quando si verifica una correzione completa. Correzione completa significa che, quando i prezzi si muovono verso l'alto dal potenziale punto numero 3, ci deve essere una barra che forma un minimo più alto e un massimo più alto rispetto alla barra precedente, oppure una combinazione di massimo 3 barre che creano sia il minimo più alto, sia il massimo più alto. I punti 2 e 3 possono formarsi sulla stessa barra. Il punto 3 non deve scendere sotto il punto 1 per un trend rialzista. Per individuare un minimo 1-2-3, si cerca quando un mercato sembra formare un minimo, o ha raggiunto un ritracciamento di 1/3 o superiore da un massimo.
**Logica Tecnica/Pseudocodice:**
1.  **Identificazione potenziale 1-2-3:**
    *   `P1_Low = Low_assoluto_recente` (punto più basso)
    *   `P2_High = High_successivo_a_P1` (picco di reazione)
    *   `P3_Low = Low_successivo_a_P2` (minimo di reazione)
2.  **Condizione Minimo 1-2-3:** `P3_Low > P1_Low` (Il punto 3 deve essere un minimo più alto del punto 1).
3.  **Conferma Correzione Completa (dal potenziale P3):**
    *   Dopo il `P3_Low`, osservare le barre successive (movimento al rialzo):
        *   **Opzione 1 (Barra singola):** Trovare una barra `B_conf` tale che `Low(B_conf) > Low(Barra_Precedente_a_B_conf)` E `High(B_conf) > High(Barra_Precedente_a_B_conf)`.
        *   **Opzione 2 (Combinazione 3 barre):** Identificare una sequenza di 3 barre consecutive che, nel loro insieme, formano un minimo più alto e un massimo più alto rispetto alla barra immediatamente precedente a questa sequenza.
4.  **Note:** I punti 2 e 3 possono essere sulla stessa barra (V-shaped reversal).

---

## Massimo 1-2-3
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 1 (OCR 52)
**Descrizione:** Un massimo 1-2-3 si forma quando si verifica una correzione completa, che è l'inverso del Minimo 1-2-3. Per individuare un massimo 1-2-3, si cerca quando un mercato sembra formare un massimo, o ha raggiunto un ritracciamento di 1/3 o superiore da un minimo. Il punto 3 non deve salire sopra il punto 1 per un trend ribassista.
**Logica Tecnica/Pseudocodice:**
1.  **Identificazione potenziale 1-2-3:**
    *   `P1_High = High_assoluto_recente` (punto più alto)
    *   `P2_Low = Low_successivo_a_P1` (minimo di reazione)
    *   `P3_High = High_successivo_a_P2` (massimo di reazione)
2.  **Condizione Massimo 1-2-3:** `P3_High < P1_High` (Il punto 3 deve essere un massimo più basso del punto 1).
3.  **Conferma Correzione Completa (dal potenziale P3):**
    *   Dopo il `P3_High`, osservare le barre successive (movimento al ribasso):
        *   **Opzione 1 (Barra singola):** Trovare una barra `B_conf` tale che `High(B_conf) < High(Barra_Precedente_a_B_conf)` E `Low(B_conf) < Low(Barra_Precedente_a_B_conf)`.
        *   **Opzione 2 (Combinazione 3 barre):** Identificare una sequenza di 3 barre consecutive che, nel loro insieme, formano un massimo più basso e un minimo più basso rispetto alla barra immediatamente precedente a questa sequenza.
4.  **Note:** I punti 2 e 3 possono essere sulla stessa barra (A-shaped reversal).

---

## Annullamento del pattern 1-2-3 (Invalidation of 1-2-3 Pattern)
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 2 (OCR 53)
**Descrizione:** L'intero pattern 1-2-3 (sia massimo che minimo) è annullato se una barra muove i prezzi fino o oltre il livello del punto 1.
**Logica Tecnica/Pseudocodice:**
1.  **Per un Minimo 1-2-3:**
    *   Se `Low(Barra_Corrente) <= P1_Low`, allora `Minimo_123_Invalidato = Vero`.
2.  **Per un Massimo 1-2-3:**
    *   Se `High(Barra_Corrente) >= P1_High`, allora `Massimo_123_Invalidato = Vero`.

---

## Regola del Gap per l'Entrata (No Gap Entry Rule)
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 2 (OCR 53), Pagina 4 (OCR 55), Pagina 6 (OCR 57), Pagina 10 (OCR 61), Pagina 13 (OCR 64), Pagina 15 (OCR 67), Pagina 34 (OCR 88)
**Descrizione:** Non si deve entrare in un trade se i prezzi "saltano in gap" oltre il prezzo di entrata desiderato. L'entrata è valida solo se il mercato "trade attraverso" il prezzo di entrata, ovvero i prezzi passano per il punto di entrata senza un'apertura in gap. Questo evita di essere eseguiti su un gap che potrebbe indicare un esaurimento immediato o una falsa rottura.
**Logica Tecnica/Pseudocodice:**
1.  **Per Entrata Long:**
    *   Sia `Entry_Price_Long` il livello di entrata desiderato.
    *   Condizione di Non-Gap: `Open(Barra_Entrata) <= Entry_Price_Long`.
    *   Condizione di Attraversamento: `Low(Barra_Entrata) <= Entry_Price_Long <= High(Barra_Entrata)` (o, più semplicemente, `Close(Barra_Entrata) > Entry_Price_Long`).
    *   Se `Open(Barra_Entrata) > Entry_Price_Long`, allora `Entrata_Invalidata_per_Gap = Vero`.
2.  **Per Entrata Short:**
    *   Sia `Entry_Price_Short` il livello di entrata desiderato.
    *   Condizione di Non-Gap: `Open(Barra_Entrata) >= Entry_Price_Short`.
    *   Condizione di Attraversamento: `Low(Barra_Entrata) <= Entry_Price_Short <= High(Barra_Entrata)` (o, più semplicemente, `Close(Barra_Entrata) < Entry_Price_Short`).
    *   Se `Open(Barra_Entrata) < Entry_Price_Short`, allora `Entrata_Invalidata_per_Gap = Vero`.

---

## Ledge
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 3 (OCR 54), Pagina 4 (OCR 55)
**Descrizione:** Una "Ledge" è una formazione di prezzo che indica una pausa in un trend, da cui ci si aspetta una continuazione del trend.
**Caratteristiche:**
*   **Durata:** Deve comprendere come minimo 4 barre di prezzo e non più di 10 barre.
*   **Allineamenti:** Deve avere due minimi allineati e due massimi allineati.
    *   I massimi allineati devono essere separati da almeno una barra di prezzo.
    *   I minimi allineati devono essere separati da almeno una barra di prezzo.
    *   Gli allineamenti non devono essere necessariamente esatti, ma non devono distare più di tre tick. Gli allineamenti esatti sono i migliori.
*   **Contesto:** Deve verificarsi in un trend e il mercato deve essere arrivato alla ledge con un trend definito.
*   **Forma:** È caratterizzata da una "quadratura" di massimi e/o minimi il più piatta possibile ("quadrati perfetti" sono i migliori), indicando una congestione stretta.
*   **Scelta dei livelli:** Se ci sono più di due massimi/minimi allineati, si può scegliere tra i due prezzi allineati più recenti ("allineamento a") o i massimi/minimi estremi della serie ("allineamento b") per il segnale di entrata.
**Logica Tecnica/Pseudocodice:**
1.  **Pre-condizione:** Identificare un `Trend_Precedente` (rialzista o ribassista).
2.  **Identificazione Ledge:**
    *   Scansionare un intervallo di barre `N` (tra 4 e 10).
    *   **Trova Massimi Allineati:**
        *   `Lista_Highs = [High(Bar_i) for i in range(Current_Bar - N + 1, Current_Bar + 1)]`
        *   Trova almeno due `Highs[j], Highs[k]` tali che `abs(Highs[j] - Highs[k]) <= 3_ticks` e `abs(j - k) > 1`.
        *   Definire `Livello_Massimi_Allineati = media(Highs[j], Highs[k])` (o max/min degli allineati).
    *   **Trova Minimi Allineati:**
        *   `Lista_Lows = [Low(Bar_i) for i in range(Current_Bar - N + 1, Current_Bar + 1)]`
        *   Trova almeno due `Lows[l], Lows[m]` tali che `abs(Lows[l] - Lows[m]) <= 3_ticks` e `abs(l - m) > 1`.
        *   Definire `Livello_Minimi_Allineati = media(Lows[l], Lows[m])` (o max/min degli allineati).
3.  **Conferma Ledge:** Se entrambe le condizioni di `Massimi_Allineati` e `Minimi_Allineati` sono soddisfatte entro l'intervallo di 4-10 barre.
4.  **Livelli di Breakout (Basato sulla scelta "a" - più recenti o "b" - estremi):**
    *   `Livello_Breakout_Long = Max(Massimi_Allineati) + 1_tick`
    *   `Livello_Breakout_Short = Min(Minimi_Allineati) - 1_tick`
5.  **Entrata:** Entrare sulla rottura di `Livello_Breakout_Long` in un `Trend_Rialzista` o `Livello_Breakout_Short` in un `Trend_Ribassista`, rispettando la `Regola_del_Gap_per_l'Entrata`.
6.  **Invalidazione:** Se la Ledge supera le 10 barre, non considerarla più valida.

---

## Trading Range (TR)
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 7 (OCR 58), Pagina 9 (OCR 60)
**Descrizione:** Una Trading Range è un periodo di consolidamento dei prezzi, generalmente atteso dopo la fine di un trend, una progressione a gradini, o un'esplosione/crollo dei prezzi.
**Caratteristiche:**
*   **Durata:** Deve essere formata da più di dieci barre di prezzo. Le barre tra 10 e 20 sono di modesta importanza. Generalmente, tra 20 e 30 barre (specificamente 21-29) si verifica una rottura del massimo o del minimo della trading range.
*   **Precursore:** Spesso preceduta da un gap o una barra di prezzo con ampia escursione (da massimo a minimo). Può essere anche una combinazione dei due.
*   **Formazione:**
    1.  Movimento (leg) contrario alla spinta del gap o della barra ampia.
    2.  Secondo movimento (leg) nella direzione del gap o della barra ampia (aspetto / o V).
    3.  Disegno di una "envelope" (linea orizzontale sul massimo più alto e sul minimo più basso).
    4.  Terzo movimento (formando /V o V\).
    5.  Quarto movimento (completato tra 21-29 barre, appare come /\/\ o VV).
*   **Definizione del Range:** Il massimo più alto e il minimo più basso tra le barre *prima* della rottura.
*   **Punto di Inizio:** Quando si guarda indietro, scegliere come inizio della trading range la barra che rappresenta il centro verticale di tutto il movimento dei prezzi dall'inizio del consolidamento.
**Logica Tecnica/Pseudocodice:**
1.  **Pre-condizione:** Osservare un `Gap_iniziale` o una `Barra_Ampia` (wide range bar).
2.  **Identificazione dei Movimenti (Legs):**
    *   `Leg1`: Movimento contrario al `Gap_iniziale`/`Barra_Ampia`.
    *   `Leg2`: Movimento nella stessa direzione del `Gap_iniziale`/`Barra_Ampia`.
    *   `Leg3`: Movimento che crea una struttura /V o V\.
    *   `Leg4`: Movimento che completa una struttura /\/\ o VV.
3.  **Definizione dell'Envelope:**
    *   `TR_High = Max(High(Barra_i))` per tutte le barre nell'intervallo `TR`.
    *   `TR_Low = Min(Low(Barra_i))` per tutte le barre nell'intervallo `TR`.
4.  **Criteri Temporali:**
    *   `Num_Barre_TR > 10`.
    *   `Num_Barre_TR` idealmente tra 21 e 29 per la rottura.
5.  **Entrata:** Entrare sulla rottura di `TR_High` (per long) o `TR_Low` (per short) rispettando la `Regola_del_Gap_per_l'Entrata`.
6.  **Allarme:** Impostare allarmi quando il prezzo si avvicina a `TR_High` o `TR_Low`.

---

## Ross Hook (RH) / Uncino di Ross
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 10 (OCR 61), Pagina 11 (OCR 62), Pagina 12 (OCR 63)
**Descrizione:** Un Ross Hook è un punto di correzione che si verifica dopo una rottura di un pattern 1-2-3, una Ledge o una Trading Range.
**Formazione:**
*   È la prima correzione che segue la rottura di un massimo o minimo 1-2-3.
*   È la prima correzione che segue la rottura di una Ledge.
*   È la prima correzione che segue la rottura di una Trading Range.
*   **In Uptrend:** Dopo la rottura di un minimo 1-2-3 (o Ledge/TR verso l'alto), il primo punto in cui una barra di prezzo NON riesce a formare un nuovo massimo crea un Ross Hook (anche un doppio massimo lo crea).
*   **In Downtrend:** Dopo la rottura di un massimo 1-2-3 (o Ledge/TR verso il basso), il primo punto in cui una barra di prezzo NON riesce a formare un nuovo minimo crea un Ross Hook (anche un doppio minimo lo crea).
**Differenze con 1-2-3:**
*   Non richiede un massimo o minimo "importante" e non necessita di una "correzione completa".
*   Può emergere da un'area di congestione (Ledge, TR).
*   Si verifica a qualsiasi livello, a differenza degli 1-2-3 che sono legati a minimi/massimi intermedi o importanti.
**Logica Tecnica/Pseudocodice:**
1.  **Pre-condizione:** Identificare una `Rottura_Valida` (di 1-2-3, Ledge o TR) che indica l'inizio di un nuovo impulso di trend.
2.  **Identificazione RH in Uptrend (dopo rottura long):**
    *   Dopo la `Rottura_Valida`, osservare le barre successive.
    *   Un `RH` è identificato sulla prima barra `Bar_RH` tale che `High(Bar_RH) <= High(Barra_Precedente_a_Bar_RH)`.
    *   `Livello_RH = High(Bar_RH)`.
3.  **Identificazione RH in Downtrend (dopo rottura short):**
    *   Dopo la `Rottura_Valida`, osservare le barre successive.
    *   Un `RH` è identificato sulla prima barra `Bar_RH` tale che `Low(Bar_RH) >= Low(Barra_Precedente_a_Bar_RH)`.
    *   `Livello_RH = Low(Bar_RH)`.
4.  **Entrata:** L'entrata avviene sulla rottura del `Livello_RH` dopo che l'RH è stato formato (vedere `Traders Trick Entry` per entrata anticipata), rispettando la `Regola_del_Gap_per_l'Entrata`.

---

## Trend Consolidato (Consolidated Trend)
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 14 (OCR 65)
**Descrizione:** Un "trend consolidato" si considera stabilito quando si è verificata la rottura di un Ross Hook. Questo implica che il trend ha superato una prima correzione dopo un breakout iniziale, confermando la sua forza.
**Logica Tecnica/Pseudocodice:**
1.  **Condizione:** `Rottura_di_Ross_Hook_Avvenuta = Vero`.
2.  **Stato:** `Stato_del_Mercato = "Trend Consolidato"`.

---

## Segnali di Entrata Intermedi: Rottura Massimo più Elevato delle Ultime Tre Barre
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 15 (OCR 67), Pagina 16 (OCR 68)
**Descrizione:** Entrata long sulla rottura del massimo più elevato tra la barra corrente e le due barre precedenti (un totale di tre barre consecutive). Questo segnale è considerato uno dei più forti tra i segnali intermedi. L'entrata deve avvenire senza gap.
**Logica Tecnica/Pseudocodice:**
1.  `H3_Max = Max(High(Barra_Corrente), High(Barra_Corrente-1), High(Barra_Corrente-2))`.
2.  **Entrata Long:**
    *   Se `Close(Barra_Corrente) > H3_Max`
    *   E `Open(Barra_Corrente) <= H3_Max` (Regola del Non-Gap).
    *   Allora `Entra_Long_a_H3_Max + 1_tick`.

---

## Segnali di Entrata Intermedi: Rottura Minimo più Basso delle Ultime Tre Barre
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 15 (OCR 67), Pagina 17 (OCR 69)
**Descrizione:** Entrata short sulla rottura del minimo più basso tra la barra corrente e le due barre precedenti (un totale di tre barre consecutive). Questo segnale è considerato uno dei più forti tra i segnali intermedi. L'entrata deve avvenire senza gap.
**Logica Tecnica/Pseudocodice:**
1.  `L3_Min = Min(Low(Barra_Corrente), Low(Barra_Corrente-1), Low(Barra_Corrente-2))`.
2.  **Entrata Short:**
    *   Se `Close(Barra_Corrente) < L3_Min`
    *   E `Open(Barra_Corrente) >= L3_Min` (Regola del Non-Gap).
    *   Allora `Entra_Short_a_L3_Min - 1_tick`.

---

## Segnali di Entrata Intermedi: Rottura di un Singolo Minimo delle Ultime Tre Barre (inclusa la barra precedente)
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 15 (OCR 67), Pagina 18 (OCR 70)
**Descrizione:** Entrata short sulla rottura di un singolo minimo significativo tra le ultime tre barre, o specificamente il minimo della barra precedente. Questo è un segnale di continuazione più immediato. L'entrata deve avvenire senza gap.
**Logica Tecnica/Pseudocodice:**
1.  `Livello_Minimo_da_Rompere = Low(Barra_Corrente-1)` (o `Min(Low(Barra_Corrente-1), Low(Barra_Corrente-2), Low(Barra_Corrente-3))`, selezionando un "singolo" minimo rilevante).
2.  **Entrata Short:**
    *   Se `Close(Barra_Corrente) < Livello_Minimo_da_Rompere`
    *   E `Open(Barra_Corrente) >= Livello_Minimo_da_Rompere` (Regola del Non-Gap).
    *   Allora `Entra_Short_a_Livello_Minimo_da_Rompere - 1_tick`.

---

## Segnali di Entrata Intermedi: Rottura di un Singolo Massimo delle Ultime Tre Barre (inclusa la barra precedente)
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 15 (OCR 67), Pagina 19 (OCR 71)
**Descrizione:** Entrata long sulla rottura di un singolo massimo significativo tra le ultime tre barre, o specificamente il massimo della barra precedente. Questo è un segnale di continuazione più immediato. L'entrata deve avvenire senza gap.
**Logica Tecnica/Pseudocodice:**
1.  `Livello_Massimo_da_Rompere = High(Barra_Corrente-1)` (o `Max(High(Barra_Corrente-1), High(Barra_Corrente-2), High(Barra_Corrente-3))`, selezionando un "singolo" massimo rilevante).
2.  **Entrata Long:**
    *   Se `Close(Barra_Corrente) > Livello_Massimo_da_Rompere`
    *   E `Open(Barra_Corrente) <= Livello_Massimo_da_Rompere` (Regola del Non-Gap).
    *   Allora `Entra_Long_a_Livello_Massimo_da_Rompere + 1_tick`.

---

## Segnale di Entrata Minore: Rottura della Prima Congestione Post-Apertura
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 20 (OCR 73), Pagina 21 (OCR 74), Pagina 22 (OCR 75)
**Descrizione:** Si cerca la prima o la seconda rottura della prima congestione che si forma dopo l'apertura del mercato, visibile su un grafico intraday. Questa congestione può anche essere una continuazione dal giorno precedente. L'entrata si ha solo se i prezzi attraversano il punto di rottura; si entra dopo l'apertura per evitare esecuzioni su gap. Il secondo attraversamento della congestione si è spesso rivelato un buon trade.
**Logica Tecnica/Pseudocodice:**
1.  **Identificazione `Prima_Congestione`:**
    *   Subito dopo l'apertura del mercato (o dalla fine del giorno precedente se continua).
    *   Definire una `Congestione` come un periodo di barre (es. 3-5 barre) in cui il prezzo si muove in un range limitato.
    *   `High_Congestione = Max(High(Barre_Congestione))`.
    *   `Low_Congestione = Min(Low(Barre_Congestione))`.
2.  **Contatore di Attraversamenti:** `Count_Attraversamenti = 0`.
3.  **Ciclo per Entrata Long:**
    *   Se `Close(Barra_Corrente) > High_Congestione`
    *   E `Open(Barra_Corrente) <= High_Congestione` (No Gap).
    *   Incrementa `Count_Attraversamenti`.
    *   Se `Count_Attraversamenti == 1` o `Count_Attraversamenti == 2`, allora `Entra_Long_a_High_Congestione + 1_tick`.
4.  **Ciclo per Entrata Short:**
    *   Se `Close(Barra_Corrente) < Low_Congestione`
    *   E `Open(Barra_Corrente) >= Low_Congestione` (No Gap).
    *   Incrementa `Count_Attraversamenti`.
    *   Se `Count_Attraversamenti == 1` o `Count_Attraversamenti == 2`, allora `Entra_Short_a_Low_Congestione - 1_tick`.
5.  **Reimposta:** Se si forma una nuova congestione o il pattern si evolve, reimpostare.

---

## L'Entrata Traders Trick (TTE)
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 23 (OCR 77), Pagina 30 (OCR 84), Pagina 31 (OCR 85), Pagina 32 (OCR 86), Pagina 33 (OCR 87), Pagina 34 (OCR 88)
**Descrizione:** La TTE è una tecnica per entrare in un trade *prima* che si verifichi l'effettiva rottura di un punto chiave (in particolare un Ross Hook o un'area di congestione come doppio/triplo supporto/resistenza). L'obiettivo è anticipare i movimenti del mercato, specialmente quelli potenzialmente "ingegnerizzati" dai grandi operatori ("stop running"). Se la rottura è genuina, si ottiene un profitto significativo; se è una falsa rottura, si coprono almeno i costi e si ottiene un piccolo profitto.
**Regole Generali:**
*   Quando i prezzi si avvicinano al punto di un Ross Hook, comprare (o vendere) la rottura del massimo (o minimo) di una barra di prezzo che fa parte della *correzione* del Ross Hook.
*   Deve esserci spazio sufficiente tra il punto di entrata e il Ross Hook per coprire i costi e realizzare un piccolo profitto.
*   Si considera la prima, la seconda e la terza barra di correzione dopo il Ross Hook. Non si cerca più l'entrata TTE dopo la terza barra di correzione completata.
*   Il mercato deve iniziare a muoversi verso il Ross Hook prima che la quarta barra sia completa.
*   La Regola del Gap per l'Entrata si applica, ma in alcuni contesti (rottura della barra più recente nella correzione) può essere ammesso un piccolo gap interno alle barre di correzione, non oltre il RH.
*   **Eccezione:** Se c'è stata una stretta area di congestione con doppio o triplo supporto/resistenza, è preferibile prendere la rottura di quell'area per la TTE.
**Logica Tecnica/Pseudocodice:**
1.  **Pre-condizione:** Identificare un `Ross_Hook` (RH) o un'area di `Doppio_Triplo_Supporto_Resistenza`.
2.  **Identificazione del `Livello_RH`:**
    *   Per un RH rialzista: `Livello_RH = High(Barra_che_forma_RH)`.
    *   Per un RH ribassista: `Livello_RH = Low(Barra_che_forma_RH)`.
3.  **Identificazione delle Barre di Correzione:**
    *   `Corr_Bar_1`, `Corr_Bar_2`, `Corr_Bar_3` sono le barre successive al `Barra_che_forma_RH` che approfondiscono la correzione.
4.  **Criteri di Entrata Long (TTE su RH rialzista):**
    *   Sia `Entry_Level = High(Corr_Bar_N) + 1_tick` dove `N` è 1, 2 o 3.
    *   Verificare `Spazio_Profitto_Sufficiente`: `(Livello_RH - Entry_Level)` deve coprire costi + piccolo profitto.
    *   Entrare Long se `Close(Barra_Corrente) > Entry_Level` E `Open(Barra_Corrente) <= Entry_Level` (Regola Non-Gap applicata rigorosamente all'Entry_Level).
    *   Se l'entrata sulla `Corr_Bar_1` non viene innescata, provare con `Corr_Bar_2`, poi `Corr_Bar_3`.
    *   **Eccezione TTE su Tripla Resistenza:** `Entry_Level = Max(Tripla_Resistenza_Highs) + 1_tick`.
5.  **Criteri di Entrata Short (TTE su RH ribassista):** (Inverso dei criteri Long)
    *   Sia `Entry_Level = Low(Corr_Bar_N) - 1_tick`.
    *   Verificare `Spazio_Profitto_Sufficiente`: `(Entry_Level - Livello_RH)` deve coprire costi + piccolo profitto.
    *   Entrare Short se `Close(Barra_Corrente) < Entry_Level` E `Open(Barra_Corrente) >= Entry_Level` (Regola Non-Gap applicata rigorosamente all'Entry_Level).
    *   Se l'entrata sulla `Corr_Bar_1` non viene innescata, provare con `Corr_Bar_2`, poi `Corr_Bar_3`.
    *   **Eccezione TTE su Triplo Supporto:** `Entry_Level = Min(Triplo_Supporto_Lows) - 1_tick`.
6.  **Invalidazione:** Se `Count_Correzione_Barre > 3`, annullare l'opportunità TTE.

---

## Buying Climax
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 27 (OCR 81)
**Descrizione:** Un "buying climax" si verifica quando il mercato si avvicina a un massimo, e praticamente tutti vogliono entrare in quel "movimento miracoloso". A meno che non ci siano forti acquisti da parte di operatori esterni per sostenere il prezzo, il mercato crollerà al raggiungimento del massimo o poco dopo. È un fenomeno che spesso precede un'inversione, causato dalla liquidazione di posizioni da parte dei grandi operatori e dai profitti degli "interni".
**Logica Tecnica/Pseudocodice:**
1.  **Identificazione:**
    *   Forte e rapido movimento al rialzo.
    *   Prezzi che si avvicinano a un livello di resistenza chiave (es. `Livello_RH`, `Max_TR`).
    *   Alte probabilità di `Volume_alto` (anche se non esplicitamente menzionato come regola per il climax, è la logica sottostante).
2.  **Implicazione:** Alta probabilità di inversione o almeno una correzione significativa.

---

## Stop Protettivi: Metodo di Violazione - Barre di Inversione
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 36 (OCR 91), Pagina 37 (OCR 92), Pagina 38 (OCR 93), Pagina 40 (OCR 95)
**Descrizione:** Un metodo per piazzare stop mentali basato sulla "violazione" del comportamento atteso del prezzo. Si cerca l'occorrenza di due "barre di inversione" nella direzione del movimento desiderato, ma che indicano una debolezza. Una barra di inversione in un movimento al rialzo è una barra che chiude sotto la sua apertura. In un movimento al ribasso, è una barra che chiude sopra la sua apertura. Le due barre non devono essere consecutive. L'uscita avviene sulla seconda barra di inversione.
**Logica Tecnica/Pseudocodice:**
1.  **In Trade Long (attesa chiusura > apertura):**
    *   `Count_Inversion_Bars = 0`.
    *   Per ogni `Barra_Corrente`:
        *   Se `Close(Barra_Corrente) < Open(Barra_Corrente)`, allora `Count_Inversion_Bars++`.
        *   Se `Count_Inversion_Bars == 2`, allora `Exit_Long_al_mercato` (o a prezzo di chiusura della seconda barra).
2.  **In Trade Short (attesa chiusura < apertura):**
    *   `Count_Inversion_Bars = 0`.
    *   Per ogni `Barra_Corrente`:
        *   Se `Close(Barra_Corrente) > Open(Barra_Corrente)`, allora `Count_Inversion_Bars++`.
        *   Se `Count_Inversion_Bars == 2`, allora `Exit_Short_al_mercato` (o a prezzo di chiusura della seconda barra).

---

## Stop Protettivi: Metodo di Violazione - Violazioni di Massimo e Minimo
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 36 (OCR 91), Pagina 37 (OCR 92), Pagina 38 (OCR 93), Pagina 39 (OCR 94)
**Descrizione:** Un metodo per piazzare stop mentali basato sulla violazione delle aspettative di continuazione del trend.
*   **In un movimento al rialzo (trade long):** Ci si aspetta che i prezzi formino massimi e minimi più alti. Se una barra di prezzo forma un minimo inferiore (violando il minimo della barra precedente), c'è qualcosa che non funziona. Si esce.
*   **In un movimento al ribasso (trade short):** Ci si aspetta che i prezzi formino massimi e minimi più bassi. Se una barra di prezzo forma un massimo superiore (violando il massimo della barra precedente), c'è qualcosa che non funziona. Si esce.
**Logica Tecnica/Pseudocodice:**
1.  **In Trade Long (in uptrend):**
    *   Per ogni `Barra_Corrente`:
        *   Se `Low(Barra_Corrente) < Low(Barra_Precedente)`, allora `Exit_Long_al_mercato`.
2.  **In Trade Short (in downtrend):**
    *   Per ogni `Barra_Corrente`:
        *   Se `High(Barra_Corrente) > High(Barra_Precedente)`, allora `Exit_Short_al_mercato`.

---

## Stop per Obiettivi (Target Stops)
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 36 (OCR 91)
**Descrizione:** Stop basati sul raggiungimento di un obiettivo di profitto prestabilito. Non sono descritti con regole specifiche nel testo, ma menzionati come una delle tre categorie di stop.
**Logica Tecnica/Pseudocodice:**
1.  **Impostazione Obiettivo:**
    *   `Target_Profit_Long = Entry_Price + X_punti_o_percentuale`.
    *   `Target_Profit_Short = Entry_Price - X_punti_o_percentuale`.
2.  **Uscita:**
    *   Se `High(Barra_Corrente) >= Target_Profit_Long` (per long) o `Low(Barra_Corrente) <= Target_Profit_Short` (per short), allora `Exit_Trade_al_Target`.

---

## Stop di Tempo (Time Stops)
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 36 (OCR 91)
**Descrizione:** Stop basati su una durata massima del trade. Non sono descritti con regole specifiche nel testo, ma menzionati come una delle tre categorie di stop.
**Logica Tecnica/Pseudocodice:**
1.  **Impostazione Durata Massima:**
    *   `Max_Bars_in_Trade = N_barre`.
    *   `Max_Time_in_Trade = T_periodo`.
2.  **Uscita:**
    *   Se `Current_Bar_Count - Entry_Bar_Count >= Max_Bars_in_Trade`
    *   O `Current_Time - Entry_Time >= Max_Time_in_Trade`
    *   Allora `Exit_Trade_al_mercato`.

---

## Priorità dei Segnali di Entrata
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 35 (OCR 89)
**Descrizione:** I segnali di entrata sono classificati in tre livelli di priorità: Principali, Intermedi e Minori. Si dovrebbe operare prioritariamente sui segnali Principali e Intermedi rispetto ai Minori. Non c'è una priorità fissa tra Principali e Intermedi, ma la spinta che deriva da un segnale Principale è generalmente maggiore.
**Logica Tecnica/Pseudocodice:**
1.  **Classificazione:**
    *   `Segnali_Principali`: Rottura 1-2-3, Rottura Ledge, Rottura Trading Range, Rottura Ross Hook.
    *   `Segnali_Intermedi`: Rottura massimo/minimo più elevato/basso delle ultime tre barre, Rottura singolo massimo/minimo delle ultime tre barre.
    *   `Segnali_Minori`: Rottura della prima/seconda congestione post-apertura.
2.  **Priorità di Esecuzione:**
    *   `If (Segnale_Principale_Valido)` OR `(Segnale_Intermedio_Valido)`:
        *   `Considera_Trade = Vero`.
    *   `Else If (Segnale_Minore_Valido)`:
        *   `Considera_Trade = Vero`.
    *   `Else`: `Attendi_Segnale`.
3.  **Preferenza:** Se disponibili sia segnali Principali/Intermedi che Minori, preferire i Principali/Intermedi.

---

## Trading su Doppio/Triplo Supporto o Resistenza (per TTE)
**Libro/File Originale:** Documento allegato
**Contesto/Pagina:** Pagina 32 (OCR 86), Pagina 33 (OCR 87)
**Descrizione:** Un'eccezione alla regola generale della TTE sulle barre di correzione è data dalla presenza di una stretta area di congestione con doppio o triplo supporto o resistenza. In questi casi, è preferibile prendere la rottura di tale area per l'entrata Traders Trick.
*   **Doppia Resistenza:** Due massimi a livelli simili.
*   **Tripla Resistenza:** Tre massimi a livelli simili.
*   **Doppio Supporto:** Due minimi a livelli simili.
*   **Triplo Supporto:** Tre minimi a livelli simili.
Si applica la condizione di "spazio sufficiente" per i profitti e la copertura dei costi.
**Logica Tecnica/Pseudocodice:**
1.  **Identificazione Pattern:**
    *   `Doppia_Resistenza_Avvenuta`: Due `High(Barra_i)` e `High(Barra_j)` sono `prossimi` (entro X ticks).
    *   `Tripla_Resistenza_Avvenuta`: Tre `High(Barra_i), High(Barra_j), High(Barra_k)` sono `prossimi`.
    *   `Doppio_Supporto_Avvenuto`: Due `Low(Barra_i)` e `Low(Barra_j)` sono `prossimi`.
    *   `Triplo_Supporto_Avvenuto`: Tre `Low(Barra_i), Low(Barra_j), Low(Barra_k)` sono `prossimi`.
2.  **Definizione Livello di Breakout:**
    *   Per resistenza: `Livello_Breakout_Res = Max(High_allineati) + 1_tick`.
    *   Per supporto: `Livello_Breakout_Sup = Min(Low_allineati) - 1_tick`.
3.  **Entrata TTE (Long su Resistenza):**
    *   Se `Tripla_Resistenza_Avvenuta` e il `Prezzo_Corrente` si avvicina al `Livello_Breakout_Res`.
    *   Verificare `Spazio_Profitto_Sufficiente`.
    *   Entra Long se `Close(Barra_Corrente) > Livello_Breakout_Res` E `Open(Barra_Corrente) <= Livello_Breakout_Res` (Regola Non-Gap).
4.  **Entrata TTE (Short su Supporto):**
    *   Se `Triplo_Supporto_Avvenuto` e il `Prezzo_Corrente` si avvicina al `Livello_Breakout_Sup`.
    *   Verificare `Spazio_Profitto_Sufficiente`.
    *   Entra Short se `Close(Barra_Corrente) < Livello_Breakout_Sup` E `Open(Barra_Corrente) >= Livello_Breakout_Sup` (Regola Non-Gap).

---

### [PARTE 3: merged_clean_part_03_p81-120.pdf]

## Exit on Second Inversion (Implied)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 1, Grafico di trading
**Descrizione:** La prima pagina mostra un grafico di trading con due punti identificati come "Prima inversione" e "Seconda inversione". L'etichetta "X = uscita" è posizionata in corrispondenza della "Seconda inversione", suggerendo una strategia di uscita dal trade. Questo implica che il trader attende due segnali di inversione consecutivi, o un secondo segnale di inversione che conferma il cambiamento di direzione del prezzo, per uscire dalla posizione.
**Logica Tecnica/Pseudocodice:**
```
IF price forms a "Prima inversione" (first significant reversal pattern) THEN
  MONITOR for "Seconda inversione"
END IF

IF price forms a "Seconda inversione" (second significant reversal pattern, confirming a directional change against the trade) THEN
  EXECUTE EXIT ORDER at current market price or at the break of the second inversion's low (for a long trade) / high (for a short trade).
END IF
```

---

## Exit on Higher High in a Downtrend (or Lower Low in an Uptrend)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 2, Grafico di trading e testo descrittivo
**Descrizione:** Questa tecnica di uscita prevede di chiudere una posizione corta in un mercato in ribasso quando il prezzo forma un "massimo superiore" (higher high), indicando un potenziale esaurimento o inversione del trend ribassista. Viceversa, per una posizione lunga in un trend rialzista, l'uscita avverrebbe su un "minimo più basso" (lower low). Il punto "X = uscita" è visualizzato nel grafico in corrispondenza di un massimo superiore in un movimento ribassista.
**Logica Tecnica/Pseudocodice:**
```
// Per una posizione SHORT in un trend ribassista:
IF current_bar.high > previous_bar.high AND market_trend_is_down THEN
  EXECUTE EXIT ORDER at market price.
END IF

// Per una posizione LONG in un trend rialzista (non mostrato ma implicito):
IF current_bar.low < previous_bar.low AND market_trend_is_up THEN
  EXECUTE EXIT ORDER at market price.
END IF
```

---

## Break-Even Stop (for remaining position)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 3, "La gestione degli stop per obiettivi"
**Descrizione:** Dopo aver coperto i costi e/o realizzato un piccolo profitto con una parte della posizione, lo stop-loss per i contratti rimanenti viene spostato al prezzo di ingresso iniziale. Questo garantisce che la parte restante del trade non possa generare una perdita.
**Logica Tecnica/Pseudocodice:**
```
// Assumendo un trade LONG:
IF partial_position_profit_taken_or_costs_covered THEN
  EXECUTE PARTIAL_EXIT_ORDER for 'X' contracts.
  SET STOP_LOSS_ORDER for remaining_contracts TO entry_price.
END IF

// Assumendo un trade SHORT:
IF partial_position_profit_taken_or_costs_covered THEN
  EXECUTE PARTIAL_EXIT_ORDER for 'X' contracts.
  SET STOP_LOSS_ORDER for remaining_contracts TO entry_price.
END IF
```

---

## Trailing Stop (Profit Protection)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 3, "La gestione degli stop per obiettivi"
**Descrizione:** Questo stop viene utilizzato per proteggere i profitti man mano che il trade si muove a favore del trader. Per una posizione lunga, lo stop viene spostato più in alto ogni volta che i prezzi rompono i massimi precedenti. Per una posizione corta, lo stop viene spostato più in basso ogni volta che i prezzi rompono i minimi precedenti. L'obiettivo è proteggere almeno la metà dei profitti "sulla carta". Questo trailing stop sostituisce lo stop di tempo una volta raggiunto il primo obiettivo di profitto.
**Logica Tecnica/Pseudocodice:**
```
// Per un trade LONG:
IF current_price > previous_swing_high THEN
  UPDATE_STOP_LOSS_ORDER to new_higher_level (e.g., protecting at least 50% of unrealized profit).
END IF

// Per un trade SHORT:
IF current_price < previous_swing_low THEN
  UPDATE_STOP_LOSS_ORDER to new_lower_level (e.g., protecting at least 50% of unrealized profit).
END IF
```

---

## Time Stop (Initial Trade Management)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 3, "Stop di tempo"
**Descrizione:** Questo stop è basato sul tempo. Se i prezzi non si muovono nella direzione desiderata entro una quantità di tempo predefinita ("X"), il trader esce dalla posizione, indipendentemente da profitto o perdita. Questo stop è utilizzato principalmente nei minuti iniziali di un trade e viene sostituito da un trailing stop una volta raggiunto il primo obiettivo di profitto.
**Logica Tecnica/Pseudocodice:**
```
// Dopo l'ingresso in un trade:
SET TIMER for DURATION_X.

IF TIMER_EXPIRED AND price_has_NOT_MOVED_IN_DESIRED_DIRECTION THEN
  EXECUTE EXIT_ORDER at market price.
END IF

// Il time stop viene sostituito da un trailing stop una volta raggiunto il primo obiettivo di profitto.
```

---

## Entry Order Preference (Stop Orders)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 4, "Ordini di entrata"
**Descrizione:** La preferenza per l'ingresso in un trade è l'utilizzo di ordini stop (stop di acquisto o stop di vendita) al prezzo di entrata desiderato. Questo significa che l'ordine diventa un ordine a mercato una volta che il prezzo stop specificato viene raggiunto o superato. Se non è possibile utilizzare un ordine stop, si ricorre agli ordini a mercato. Si accetta un leggero scivolamento (slippage) come parte del piano.
**Logica Tecnica/Pseudocodice:**
```
// Per un ingresso LONG:
PLACE BUY STOP ORDER at desired_entry_price.

// Per un ingresso SHORT:
PLACE SELL STOP ORDER at desired_entry_price.

IF STOP_ORDER_NOT_FEASIBLE THEN
  PLACE MARKET ORDER for entry.
END IF

// Accetta uno scivolamento minore come parte del piano.
```

---

## Reactive Intraday Entry
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 4, "Ordini di entrata"
**Descrizione:** I trader non piazzano ordini di entrata prima dell'apertura del mercato. Gli ordini vengono piazzati solo quando si osserva che i prezzi si stanno attivamente avvicinando al punto di entrata desiderato e si muovono nella direzione prevista su un grafico intraday. Questo approccio reattivo assicura che il mercato stia confermando l'intenzione del trader prima di impegnare capitale.
**Logica Tecnica/Pseudocodice:**
```
// Prima di piazzare un ordine:
MONITOR intraday_chart for price_action.

IF price_is_approaching(desired_entry_point) AND price_is_moving_in_desired_direction THEN
  PLACE ENTRY_ORDER (e.g., Stop Order or Market Order as per preference).
END IF
```

---

## Market Order Exit (Final Target)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 5, "Ordini di uscita"
**Descrizione:** Quando l'obiettivo di profitto finale viene raggiunto (o anche leggermente superato), il trader esce dalla posizione utilizzando un ordine a mercato. Questo approccio enfatizza la velocità di uscita e la certezza dell'esecuzione, accettando un potenziale scivolamento (slippage), piuttosto che tentare di ottenere un prezzo migliore con ordini limite che potrebbero portare a mancare l'uscita.
**Logica Tecnica/Pseudocodice:**
```
IF final_profit_target_reached OR current_price_exceeds_target THEN
  EXECUTE EXIT_ALL_CONTRACTS_MARKET_ORDER.
END IF
```

---

## Emergency Exit (Adverse Trade)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 5, "Ordini di uscita"
**Descrizione:** Se un trade va contro il trader, o se c'è incertezza sul fatto che il trade stia procedendo come previsto, il trader deve uscire immediatamente. Questo può significare l'attivazione dello stop di tempo, dello stop protettivo o semplicemente un'uscita a mercato se la situazione è poco chiara o sta peggiorando rapidamente. La filosofia è: "se non va come voglio, esco ora!".
**Logica Tecnica/Pseudocodice:**
```
IF price_moves_significantly_against_trade OR
   (trade_status_uncertain AND price_action_not_confirming_plan) THEN
  EXECUTE IMMEDIATE_MARKET_EXIT_ORDER.
END IF
```

---

## Broker Selection Criteria (Trade Execution Infrastructure)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 11, "Ecco alcune delle cose che cerchiamo in un broker"
**Descrizione:** Questo è un insieme di criteri per la selezione di un broker adatto al daytrading. I requisiti includono: commissioni basse ma non eccessive per il trading elettronico, margini ridotti per il daytrading (non margini pieni), nessuna limitazione sul numero di contratti, compatibilità della piattaforma con diverse tipologie di mercato (elettronici e alle grida), piattaforma di alta qualità per il trading elettronico, accesso diretto ai mercati forex, eccellente servizio clienti con supporto "dal vivo", ampia varietà di tipi di ordini, eseguiti migliori della media grazie all'eccellente liquidità, esecuzioni istantanee, possibilità di "parcheggiare" gli ordini per piazzarli con un solo click e capacità di operare con la propria valuta o gestire il conto nella propria valuta.
**Logica Tecnica/Pseudocodice:**
```
SELECT BROKER WHERE:
  COMMISSION_RATE is low_but_not_excessively_low AND
  MARGIN_REQUIREMENT for daytrading is reduced (half or less, not full) AND
  CONTRACT_LIMITATION is NONE AND
  PLATFORM_COMPATIBILITY includes electronic_and_pit_markets AND
  MARKET_ACCESS includes Futures, Options, Forex (single account if possible) AND
  PLATFORM_QUALITY is high for electronic trading AND
  SERVICE_QUALITY includes live_person_support AND
  ORDER_TYPE_VARIETY is wide (not limited) AND
  EXECUTION_QUALITY is better_than_average (due to direct market access and liquidity) AND
  EXECUTION_SPEED is instant for most cases AND
  ORDER_PARKING_CAPABILITY is TRUE (one-click placement) AND
  CURRENCY_ACCOUNT_MANAGEMENT is available.
```

---

## Daily High/Low Breakout (Momentum Strategy)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 16, "Il piano"
**Descrizione:** Questa strategia si basa sull'idea che la rottura dei massimi o minimi giornalieri precedenti genera solitamente una spinta sufficiente per realizzare un profitto. Più è importante la rottura (ad esempio, la rottura di massimi/minimi di più giorni), maggiori sono le probabilità che la spinta sia sostenuta e porti a un profitto. Si enfatizza l'importanza di utilizzare il grafico giornaliero per ottenere una prospettiva più ampia del mercato.
**Logica Tecnica/Pseudocodice:**
```
IDENTIFY previous_day_high AND previous_day_low.

// Per un trade LONG:
IF current_price > previous_day_high THEN
  INITIATE_LONG_TRADE (on breakout with momentum).
END IF

// Per un trade SHORT:
IF current_price < previous_day_low THEN
  INITIATE_SHORT_TRADE (on breakout with momentum).
```

---

## Quick Initial Profit Taking (Partial Exit)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 17, "Lo voglio a mio modo mio"
**Descrizione:** Una parte fondamentale del piano di trading è uscire con almeno uno, a volte due, contratti non appena si vede un "ragionevole profitto". Questo garantisce che una parte del profitto sia subito bloccata, coprendo i costi e rendendo il trade "gratis" per i contratti rimanenti. Questa azione precoce aiuta anche a rafforzare la fiducia del trader.
**Logica Tecnica/Pseudocodice:**
```
IF unrealized_profit_per_contract >= reasonable_profit_threshold THEN
  EXECUTE PARTIAL_EXIT_ORDER for (1 OR 2) contracts.
  // Questo profitto dovrebbe almeno coprire i costi diretti dell'intera posizione.
END IF
```

---

## Scaled Time Stop (Chart-Dependent)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 17, "Lo voglio a mio modo mio"
**Descrizione:** La durata dello stop di tempo (il periodo entro cui il prezzo deve muoversi nella direzione desiderata) è adattata al timeframe del grafico utilizzato. Ad esempio, su un grafico a 60 minuti, lo stop di tempo è di 30 minuti; su un grafico a 3 minuti, è di 3 minuti. Questo assicura che il limite di tempo sia appropriato per la volatilità e la velocità tipica dell'intervallo del grafico selezionato.
**Logica Tecnica/Pseudocodice:**
```
// Dopo l'ingresso:
IF current_chart_timeframe == 60_minutes THEN
  SET TIME_STOP_DURATION = 30_minutes.
ELSE IF current_chart_timeframe == 3_minutes THEN
  SET TIME_STOP_DURATION = 3_minutes.
// Aggiungere altre condizioni per altri timeframe.
END IF

MONITOR price_movement for TIME_STOP_DURATION.
IF price_has_NOT_MOVED_IN_DESIRED_DIRECTION within TIME_STOP_DURATION THEN
  EXECUTE EXIT_ORDER at market price.
END IF
```

---

## Tiered Profit Taking & Trailing Stop
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 18, "Strategia di gestione della posizione"
**Descrizione:** Questa strategia prevede la realizzazione di profitti in più fasi per una posizione con più contratti (ad esempio, tre set di contratti). I primi due terzi della posizione vengono chiusi a obiettivi di profitto predefiniti. L'ultimo terzo della posizione viene gestito con un trailing stop, permettendogli di "correre" per massimizzare i guadagni da movimenti di mercato più ampi. Questo approccio bilancia la sicurezza dei profitti con la possibilità di catturare trend estesi.
**Logica Tecnica/Pseudocodice:**
```
// Assumendo una posizione di N contratti (N è un multiplo di 3 per questo esempio):
// Dividere la posizione in tre parti: part1 = N/3, part2 = N/3, part3 = N/3.

IF price_reaches_profit_target_1 THEN
  EXECUTE EXIT_ORDER for part1.
END IF

IF price_reaches_profit_target_2 THEN
  EXECUTE EXIT_ORDER for part2.
END IF

// Per il restante part3 (il "runner"):
IMPLEMENT TRAILING_STOP for part3.
// Ad esempio, sposta lo stop sotto il minimo di swing più recente per una posizione lunga,
// o sopra il massimo di swing più recente per una posizione corta, o basato su una media mobile.
```

---

## Layered Entry Signals Approach
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 19, "Lascia che ripeta il piano fino a questo punto"
**Descrizione:** Il piano di trading incorpora segnali di entrata da categorie "principali", "intermedie" e "minori", che vengono prioritizzate e organizzate. Questo implica un approccio gerarchico nell'identificazione e nell'azione sui segnali di trading, probabilmente basato sulla forza o sul timeframe del segnale, garantendo che le opportunità siano valutate in modo strutturato.
**Logica Tecnica/Pseudocodice:**
```
DEFINE main_signals = [lista di segnali forti, su timeframe superiori].
DEFINE intermediate_signals = [lista di segnali di media forza, su timeframe intermedi].
DEFINE minor_signals = [lista di segnali più deboli, su timeframe inferiori].

PRIORITIZE signals based on predefined order (e.g., main > intermediate > minor).

IF main_signal_present THEN
  CONSIDER_ENTRY (massima priorità).
ELSE IF intermediate_signal_present THEN
  CONSIDER_ENTRY.
ELSE IF minor_signal_present THEN
  CONSIDER_ENTRY.
END IF
```

---

## Pre-Trade Order Preparation & Alert System
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 19, "Lascia che ripeta il piano fino a questo punto"
**Descrizione:** Prima di fare trading, tutti i potenziali ordini (di entrata e uscita) vengono meticolosamente scritti esattamente come verrebbero piazzati. Inoltre, viene impostato un sistema di allarmi (visivi e sonori, o monitoraggio manuale) tipicamente da 5 a 10 tick prima del punto di entrata effettivo. Questa preparazione assicura prontezza, riduce gli errori e concede tempo per reagire.
**Logica Tecnica/Pseudocodice:**
```
// Per ogni potenziale trade:
WRITE_DOWN full_order_details (es. BUY/SELL, quantità, prezzo, stop, target).

// Per gli allarmi:
SET VISUAL_ALARM at (entry_price - 5_to_10_ticks_for_long) OR (entry_price + 5_to_10_ticks_for_short).
SET AUDITORY_ALARM at (entry_price - 5_to_10_ticks_for_long) OR (entry_price + 5_to_10_ticks_for_short).

// IF software_does_not_support_alarms THEN
//   MANUALLY_MONITOR price_action_at_alert_levels.
// END IF
```

---

## Sensible Multi-Stage Profit Taking
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 20, "Liquidazione dei contratti"
**Descrizione:** Quando si opera con più contratti (es. 10 contratti), la strategia preferita per la presa di profitto è liquidare la porzione maggiore (es. 6 contratti) al primo obiettivo di profitto. Una porzione minore (es. 3 contratti) viene liquidata al secondo obiettivo. La porzione più piccola rimanente (es. 1 contratto) viene poi gestita con un trailing stop per massimizzare i potenziali guadagni da un movimento esteso. Questo approccio è contrapposto a un metodo "avido" che cerca di tenere una porzione maggiore per un tempo più lungo.
**Logica Tecnica/Pseudocodice:**
```
// Per una posizione di 10 contratti:
SET profit_target_1.
SET profit_target_2.
SET profit_target_3 (implicito per il trailing).

IF price_reaches_profit_target_1 THEN
  EXECUTE EXIT_ORDER for 6 contracts.
END IF

IF price_reaches_profit_target_2 THEN
  EXECUTE EXIT_ORDER for 3 contracts.
END IF

IF price_reaches_profit_target_3 OR price_triggers_trailing_stop THEN
  EXECUTE EXIT_ORDER for 1 contract (il "runner").
  // Assicurarsi che il "runner" non si trasformi in una perdita; il suo stop dovrebbe essere almeno al secondo obiettivo.
END IF
```

---

## Minimum 2-Contract Position Sizing
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 20, "Liquidazione dei contratti"
**Descrizione:** Il trader non opera mai con meno di due contratti. La motivazione è che un trade con un singolo contratto è troppo dipendente da un unico risultato e non consente una gestione efficace del trade (come la presa di profitto parziale o la scalatura). Se non si dispongono di fondi sufficienti per fare trading con almeno due contratti, non si dovrebbe fare trading affatto.
**Logica Tecnica/Pseudocodice:**
```
IF available_funds < margin_required_for_2_contracts THEN
  DO_NOT_TRADE.
ELSE
  INITIATE_TRADE with minimum 2_contracts.
END IF

// Se la dimensione del trade è di 2 contratti:
IF price_reaches_profit_target_2 THEN
  EXECUTE_EXIT_ORDER for both contracts.
END IF
```

---

## Traders Trick (Anticipatory Breakout Filter)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 22, "Filtrare il trade"
**Descrizione:** Il "Traders Trick" è un filtro che si applica quando il mercato si avvicina a un punto di entrata significativo (principale o intermedio). Invece di attendere la violazione del punto di rottura principale (come la rottura di un trading range, un massimo/minimo 1-2-3, una ledge o un Ross Hook), l'entrata avviene sulla rottura di una zona di congestione più piccola che si forma tipicamente *appena prima* del punto di rottura principale. Questo permette di utilizzare uno stop più stretto, aiuta a evitare false rotture e consente di entrare in un trend prima rispetto a una strategia di rottura standard. L'entrata è sempre nella direzione prevista della rottura più ampia.
**Logica Tecnica/Pseudocodice:**
```
IDENTIFY major_breakout_point (es. rottura di range, massimo/minimo 1-2-3, ledge, Ross Hook).

MONITOR price_action as it approaches major_breakout_point.

IF small_congestion_zone forms_just_before major_breakout_point THEN
  // Per un trade LONG:
  IF price_breaks_above_high_of_small_congestion_zone THEN
    EXECUTE LONG_ENTRY_ORDER.
  END IF
  // Per un trade SHORT:
  IF price_breaks_below_low_of_small_congestion_zone THEN
    EXECUTE SHORT_ENTRY_ORDER.
  END IF
END IF
```

---

## 1-2-3 Pattern (High/Low)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 22, "Filtrare il trade", menziona "un 1-2-3 massimo o minimo"
**Descrizione:** Il pattern 1-2-3, spesso associato ai metodi di trading di Joe Ross, identifica un potenziale punto di inversione o continuazione del trend. Un "massimo 1-2-3" comporta un picco (1), un ritracciamento a un minimo superiore (2), seguito da un rally a un nuovo picco, inferiore al primo (3). Un ingresso short viene attivato alla rottura sotto il punto 2. Un "minimo 1-2-3" è l'inverso. Questo pattern è spesso utilizzato come segnale chiave per rotture o cambiamenti di trend.
**Logica Tecnica/Pseudocodice:**
```
// Per un MASSIMO 1-2-3 (inversione ribassista):
1. IDENTIFY price_peak (Punto 1).
2. IDENTIFY subsequent_low (Punto 2).
3. IDENTIFY rally_to_lower_peak (Punto 3).

IF price_breaks_below Punto_2_low THEN
  EXECUTE SHORT_ENTRY_ORDER.
END IF

// Per un MINIMO 1-2-3 (inversione rialzista):
1. IDENTIFY price_trough (Punto 1).
2. IDENTIFY subsequent_high (Punto 2).
3. IDENTIFY decline_to_higher_trough (Punto 3).

IF price_breaks_above Punto_2_high THEN
  EXECUTE LONG_ENTRY_ORDER.
END IF
```

---

## Ledge Pattern
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 22, "Filtrare il trade", menziona "una ledge"
**Descrizione:** Una "ledge" (scaffale/ripiano) nel trading si riferisce a una stretta fascia di consolidamento dei prezzi che si verifica all'interno di un trend o appena prima di una rottura. È un periodo in cui il movimento dei prezzi si blocca temporaneamente, formando una struttura piatta in alto o in basso, prima di riprendere la sua direzione precedente o di rompere in una nuova direzione. Il trading su una ledge spesso comporta l'ingresso quando il prezzo esce da questa stretta zona di consolidamento.
**Logica Tecnica/Pseudocodice:**
```
IDENTIFY period_of_price_consolidation (range ristretto, relativamente piatto).

// Per un trade LONG (rottura rialzista da una ledge):
IF price_breaks_above_resistance_of_ledge THEN
  EXECUTE LONG_ENTRY_ORDER.
END IF

// Per un trade SHORT (rottura ribassista da una ledge):
IF price_breaks_below_support_of_ledge THEN
  EXECUTE SHORT_ENTRY_ORDER.
END IF
```

---

## Ross Hook (RH)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 22, "Filtrare il trade", menziona "un Ross Hook"
**Descrizione:** Un Ross Hook (RH) è un tipo specifico di ritracciamento all'interno di un trend, che segue una rottura. Dopo che il mercato esce da un'area di congestione (ad esempio, una "ledge") e forma un nuovo massimo (o minimo), si verifica un leggero pullback. Questo pullback, o "uncino", è visto come un'opportunità per unirsi al nuovo trend. In un uptrend, dopo un nuovo massimo, il prezzo ritraccia per formare un minimo superiore, e l'ingresso avviene sulla rottura del massimo dell'uncino. In un downtrend, dopo un nuovo minimo, il prezzo ritraccia per formare un massimo inferiore, e l'ingresso avviene sulla rottura del minimo dell'uncino.
**Logica Tecnica/Pseudocodice:**
```
// Per un trade LONG (in un uptrend):
1. IDENTIFY initial_breakout_from_congestion.
2. IDENTIFY new_high (o continuazione del trend).
3. IDENTIFY pullback_forming_higher_low (l'"uncino").

IF price_breaks_above_high_of_the_pullback_bar_or_pattern THEN
  EXECUTE LONG_ENTRY_ORDER.
END IF

// Per un trade SHORT (in un downtrend):
1. IDENTIFY initial_breakout_from_congestion.
2. IDENTIFY new_low (o continuazione del trend).
3. IDENTIFY pullback_forming_lower_high (l'"uncino").

IF price_breaks_below_low_of_the_pullback_bar_or_pattern THEN
  EXECUTE SHORT_ENTRY_ORDER.
END IF
```

---

## Multi-Timeframe Entry Confirmation
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 22, "Filtrare il trade"
**Descrizione:** Il segnale di entrata per un trade dovrebbe essere derivato da un grafico con un timeframe superiore rispetto a quello utilizzato per gestire il trade. Ad esempio, se si opera su un grafico a 60 minuti, il segnale di entrata dovrebbe provenire da un grafico con un timeframe maggiore di 60 minuti. Questo fornisce un contesto più ampio e conferma la validità del segnale, riducendo il "rumore" dal timeframe inferiore.
**Logica Tecnica/Pseudocodice:**
```
LET trade_management_timeframe = Current_Chart_Timeframe.
LET entry_signal_timeframe = Higher_Timeframe (es. Daily, Weekly, o > trade_management_timeframe).

IDENTIFY entry_signal ON entry_signal_timeframe.

IF entry_signal_is_valid ON entry_signal_timeframe THEN
  INITIATE_TRADE_MANAGEMENT ON trade_management_timeframe.
ELSE
  DO_NOT_TRADE.
END IF
```

---

## Gap Trading Restriction (Daily Extremes)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 22, "Filtrare il trade"
**Descrizione:** Come regola generale, tranne in situazioni speciali e avanzate non trattate nel libro, si dovrebbe evitare di fare trading su un'apertura in gap che supera un massimo o un minimo giornaliero precedente. Questo suggerisce cautela intorno a gap significativi che potrebbero essere instabili o portare a un'azione imprevedibile del prezzo.
**Logica Tecnica/Pseudocodice:**
```
IDENTIFY previous_daily_high AND previous_daily_low.
IDENTIFY current_market_open_price.

IF current_market_open_price > previous_daily_high OR current_market_open_price < previous_daily_low THEN
  AVOID_TRADING (a meno che non siano soddisfatte condizioni speciali predefinite).
END IF
```

---

## First Post-Open Congestion Breakout
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 22, "Filtrare il trade"
**Descrizione:** Questa tecnica prevede di fare trading sulla rottura della prima area di congestione che si forma dopo l'apertura del mercato. Questa congestione può essere una nuova formazione o una continuazione della congestione finale del giorno precedente. Una rottura da questa congestione intraday iniziale su un grafico a cinque minuti fornisce un'indicazione di ciò che seguirà nel corso della giornata.
**Logica Tecnica/Pseudocodice:**
```
MONITOR price_action immediately_after_market_open.

IDENTIFY first_congestion_area (zona di consolidamento) formed post-open (può essere una continuazione della congestione finale di ieri).

// Per un trade LONG:
IF price_breaks_above_resistance_of_first_congestion_area THEN
  EXECUTE LONG_ENTRY_ORDER.
END IF

// Per un trade SHORT:
IF price_breaks_below_support_of_first_congestion_area THEN
  EXECUTE SHORT_ENTRY_ORDER.
END IF
```

---

## Exit on Lower Low or Two Bearish Reversal Bars
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 27, "Regola di uscita"
**Descrizione:** Per una posizione lunga, un'uscita dovrebbe essere attivata se una barra forma un minimo inferiore (un nuovo minimo che è al di sotto del minimo della barra precedente). In alternativa, un'uscita è attivata se appaiono due "barre di inversione" consecutive, nello specifico due barre con chiusure inferiori ai loro prezzi di apertura (indicando un sentimento ribassista). Questo segnala un potenziale indebolimento o inversione del movimento al rialzo.
**Logica Tecnica/Pseudocodice:**
```
// Per un trade LONG:
IF current_bar.low < previous_bar.low THEN
  EXECUTE EXIT_ORDER.
END IF

ELSE IF current_bar_is_bearish_reversal_bar AND previous_bar_is_bearish_reversal_bar THEN
  // Una barra di inversione ribassista è quella in cui close < open.
  EXECUTE EXIT_ORDER.
END IF
```

---

## Multiple Breakout Confirmation
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 28, "Descrizione delle entrate"
**Descrizione:** Sebbene la rottura di una semplice area di congestione possa essere un segnale di entrata, la forza e l'affidabilità del segnale sono significativamente aumentate se essa coincide con la rottura di livelli più significativi, come il massimo di tre giorni fa, di due giorni fa o anche solo di un giorno fa. Più livelli storici significativi vengono rotti contemporaneamente, maggiore è la convinzione per il trade.
**Logica Tecnica/Pseudocodice:**
```
IDENTIFY current_congestion_breakout.
IDENTIFY previous_day_high.
IDENTIFY previous_two_day_high.
IDENTIFY previous_three_day_high.

IF current_congestion_breakout is_bullish THEN
  IF price_also_breaks_above previous_day_high OR
     price_also_breaks_above previous_two_day_high OR
     price_also_breaks_above previous_three_day_high THEN
    EXECUTE STRONGER_LONG_ENTRY_ORDER.
  ELSE
    EXECUTE STANDARD_LONG_ENTRY_ORDER.
  END IF
// Logica inversa per le rotture ribassiste.
END IF
```

---

## Three-Bar Failure to Make New High/Low Exit
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 28, "Descrizione delle uscite"
**Descrizione:** In un uptrend, se tre barre consecutive non riescono a formare un nuovo massimo, ciò indica una perdita di slancio al rialzo ed è considerato un segnale di uscita, in particolare per i trader esperti. Al contrario, in un downtrend, tre barre consecutive che non riescono a formare un nuovo minimo segnalerebbero un'uscita. Questa è una regola di uscita basata sullo slancio a breve termine.
**Logica Tecnica/Pseudocodice:**
```
// Per un trade LONG:
IF (current_bar.high <= previous_bar.high) AND
   (previous_bar.high <= bar_before_previous.high) AND
   (bar_before_previous.high <= bar_three_ago.high) THEN
  EXECUTE EXIT_ORDER.
END IF

// Per un trade SHORT:
IF (current_bar.low >= previous_bar.low) AND
   (previous_bar.low >= bar_before_previous.low) AND
   (bar_before_previous.low >= bar_three_ago.low) THEN
  EXECUTE EXIT_ORDER.
END IF
```

---

## Exit on Bearish Reversal Bar after Failed Breakout
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 29, "Analisi del riquadro #2"
**Descrizione:** Dopo un potenziale breakout (ad esempio, nel "riquadro #2"), se la barra di breakout è una "barra di inversione" (cioè chiude significativamente contro la direzione del breakout previsto, implicando un rifiuto del livello), e la barra *successiva* conferma l'inversione, il trade dovrebbe essere chiuso immediatamente, spesso con una perdita. Questa regola è particolarmente enfatizzata se l'entrata non è stata effettuata utilizzando il filtro anticipatorio "Traders Trick".
**Logica Tecnica/Pseudocodice:**
```
// Per uno scenario di entrata LONG:
IF (breakout_bar_is_reversal_bar_against_long_direction AND
    next_bar_confirms_reversal_against_long_direction) THEN
  EXECUTE EXIT_ORDER (probabilmente una perdita).
END IF

// Una barra di inversione in questo contesto potrebbe essere definita come:
// Per un tentativo di breakout rialzista: una barra che ha tentato di rompere al rialzo ma ha chiuso significativamente più in basso (es. più bassa dell'apertura, o vicino al suo minimo).
// Per un tentativo di breakout ribassista: una barra che ha tentato di rompere al ribasso ma ha chiuso significativamente più in alto (es. più alta dell'apertura, o vicino al suo massimo).
```

---

## 1-2-3 Low Breakout Entry (Point 2 Violation)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 30, "Ultimo assalto al massimo"
**Descrizione:** In uno scenario di trend rialzista (o inversione rialzista), dopo che si è formato un pattern "minimo 1-2-3", l'entrata viene attivata dal prezzo che supera di un tick il massimo del "Punto 2" del pattern. Questo indica che il ritracciamento è terminato e lo slancio al rialzo sta riprendendo. L'autore nota che combinare questa entrata con il "Traders Trick" fornisce un segnale di entrata ancora migliore, portando a forti movimenti unidirezionali.
**Logica Tecnica/Pseudocodice:**
```
// Per un pattern MINIMO 1-2-3:
1. IDENTIFY price_trough (Punto 1).
2. IDENTIFY subsequent_high (Punto 2).
3. IDENTIFY decline_to_higher_trough (Punto 3).

IF current_price > (Punto_2_high + 1_tick) THEN
  EXECUTE LONG_ENTRY_ORDER.
END IF

// Per risultati ancora migliori, considerare l'utilizzo del filtro Traders Trick prima di questa entrata.
```

---

## Breakout of Prior Day/Multi-Day High (Example)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 31, "Esempio di trade"
**Descrizione:** Questo è un'applicazione della strategia di breakout del massimo giornaliero. Il grafico illustra entrate attivate dal prezzo che rompe al di sopra del massimo di due giorni fa e poi del massimo di ieri. Queste rotture da precedenti livelli significativi sono considerate forti segnali rialzisti.
**Logica Tecnica/Pseudocodice:**
```
IDENTIFY high_of_yesterday.
IDENTIFY high_of_two_days_ago.

// Per un ingresso LONG:
IF current_price > high_of_two_days_ago THEN
  EXECUTE LONG_ENTRY_ORDER (Acquisto sulla rottura del massimo di due giorni fa).
END IF

IF current_price > high_of_yesterday THEN
  EXECUTE LONG_ENTRY_ORDER (Acquisto sulla rottura del massimo di ieri).
END IF
```

---

## Traders Trick Applied (Pre-Daily Extreme Breakout)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 32, "Spiegazione delle congestioni #1 e #2"
**Descrizione:** Questa regola specifica il nucleo del "Traders Trick": quando si utilizza un segnale di entrata minore, l'entrata viene effettuata sulla rottura di una congestione che *precede* la rottura del massimo o minimo giornaliero (o massimo/minimo di più giorni) che normalmente costituirebbe il segnale di entrata primario. Questo consente un'entrata più precoce, spesso con uno stop più stretto, anticipando il movimento più ampio. Ad esempio, entrando sulla rottura della congestione #1 (che è il massimo del giorno precedente *e* una rottura di congestione) o della congestione #2 (che è una rottura di congestione *appena prima* della rottura del massimo di 2 giorni).
**Logica Tecnica/Pseudocodice:**
```
IDENTIFY primary_daily_extreme_breakout_point (es. previous_day_high, two_day_high).

IDENTIFY pre_breakout_congestion_area (un consolidamento più piccolo che si forma appena prima del primary_daily_extreme_breakout_point).

// Per un trade LONG:
IF price_breaks_above_high_of_pre_breakout_congestion_area THEN
  EXECUTE LONG_ENTRY_ORDER (Questo è l'ingresso "Traders Trick", che anticipa il breakout primario).
END IF

// Per un trade SHORT:
IF price_breaks_below_low_of_pre_breakout_congestion_area THEN
  EXECUTE SHORT_ENTRY_ORDER (Anticipando il breakout primario).
END IF
```

---

## Multiple Re-entries in a Trending Market
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 33, "Strategia di trading illustrata"
**Descrizione:** In un mercato in trend (ad esempio, al rialzo), è possibile effettuare più tentativi di ingresso dopo aver chiuso trade precedenti a causa di ritracciamenti minori o prese di profitto. Questi re-entry sono tipicamente innescati da successive rotture di aree di consolidamento o pattern come i Ross Hook, sempre allineati con il trend generale. L'obiettivo è catturare continuamente profitti dalla direzione prevalente, anche se i singoli trade producono piccoli guadagni o perdite prima di trovare un movimento più forte.
**Logica Tecnica/Pseudocodice:**
```
WHILE market_is_in_uptrend THEN
  // Primo ingresso (es. al #1)
  EXECUTE LONG_ENTRY_ORDER.
  // Se le condizioni di uscita sono soddisfatte (es. minimo inferiore o barra di inversione):
  EXECUTE EXIT_ORDER.

  // Cerca la prossima opportunità di re-entry (es. rottura della congestione #2):
  IF new_bullish_congestion_breakout_signal THEN
    EXECUTE LONG_ENTRY_ORDER.
    // Se le condizioni di uscita sono soddisfatte:
    EXECUTE EXIT_ORDER.
  END IF

  // Cerca un'altra re-entry (es. rottura del Ross Hook #3):
  IF new_bullish_Ross_Hook_signal THEN
    EXECUTE LONG_ENTRY_ORDER.
    // Se le condizioni di uscita sono soddisfatte:
    EXECUTE EXIT_ORDER.
  END IF
END WHILE
```

---

## Average Volatility-Based Stop Loss
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 36, "Money management"
**Descrizione:** Lo stop-loss protettivo iniziale viene posizionato a una distanza dal *prezzo di esecuzione* pari alla volatilità media del mercato, più le commissioni. La volatilità media è calcolata sommando il range (massimo meno minimo) delle ultime 10 barre e dividendo per 10. Questo assicura che lo stop tenga conto del movimento tipico del mercato e dei costi di trading, ed è posizionato in base all'entrata effettiva piuttosto che a un prezzo di entrata teorico.
**Logica Tecnica/Pseudocodice:**
```
CALCULATE average_volatility = SUM(HIGH[i] - LOW[i] for i = 1 to 10) / 10.
LET total_commissions = $10 // Esempio.

// Per un trade LONG:
LET initial_stop_price = executed_entry_price - (average_volatility_in_points + commissions_in_points).
SET STOP_LOSS_ORDER at initial_stop_price.

// Per un trade SHORT:
LET initial_stop_price = executed_entry_price + (average_volatility_in_points + commissions_in_points).
SET STOP_LOSS_ORDER at initial_stop_price.

// Esempio dato: $150 di volatilità, $10 di commissioni -> stop a 11-12 punti ($160-170 totali) dal prezzo di esecuzione.
```

---

## Risk Factor Assessment (Trade Selection)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 37, "Risk management"
**Descrizione:** Prima di entrare in un trade, si valutano varie condizioni di mercato ed esterne per determinarne il rischio intrinseco. Fare trading nelle seguenti condizioni aumenta la probabilità di perdita e quindi il rischio complessivo: mercati veloci, mercati poco liquidi, dimensione di tick anomala, giorni prima di una festività, vicinanza al giorno di First Notice di un future, mercati molto volatili, servizi di brokeraggio scarsi e trading vicino al rilascio di un report. Un trader dovrebbe evitare queste condizioni o adeguare la propria strategia di conseguenza (es. dimensioni della posizione più piccole, stop più stretti).
**Logica Tecnica/Pseudocodice:**
```
// Prima di avviare qualsiasi trade:
CALCULATE trade_risk_score.

IF market_speed == FAST THEN trade_risk_score += HIGH_RISK_FACTOR.
IF market_liquidity == LOW THEN trade_risk_score += HIGH_RISK_FACTOR.
IF tick_size == ANOMALOUS THEN trade_risk_score += HIGH_RISK_FACTOR.
IF days_to_holiday <= THRESHOLD THEN trade_risk_score += MEDIUM_RISK_FACTOR.
IF days_to_first_notice_day_future <= THRESHOLD THEN trade_risk_score += MEDIUM_RISK_FACTOR.
IF market_volatility == HIGH THEN trade_risk_score += MEDIUM_RISK_FACTOR.
IF brokerage_service_quality == POOR THEN trade_risk_score += HIGH_RISK_FACTOR.
IF trading_near_report_release == TRUE THEN trade_risk_score += HIGH_RISK_FACTOR.

IF trade_risk_score > ACCEPTABLE_RISK_THRESHOLD THEN
  AVOID_TRADE OR REDUCE_POSITION_SIZE OR TIGHTEN_STOP.
END IF
```

---

## Cost Coverage First Profit Target (Money Management)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 38, "Money management"
**Descrizione:** L'obiettivo primario della prima fase di presa di profitto è assicurarsi che tutti i costi diretti (commissioni, slippage) per l'intera posizione, inclusi eventuali contratti rimanenti, siano coperti. Una volta osservato un "guadagno sufficiente", una porzione dei contratti viene liquidata specificamente per raggiungere questa copertura dei costi, rendendo il resto del trade "gratis" o a rischio ridotto.
**Logica Tecnica/Pseudocodice:**
```
CALCULATE total_direct_costs = (total_commissions + estimated_slippage_cost).

IF (unrealized_profit_per_contract * initial_number_of_contracts >= total_direct_costs) THEN
  // Calcola il numero di contratti da vendere per coprire i costi (può essere 1 o più).
  EXECUTE PARTIAL_EXIT_ORDER (per coprire total_direct_costs).

  // Dopo aver coperto i costi, aggiusta lo stop per i contratti rimanenti:
  // Opzione 1: Sposta lo stop a pareggio (executed_entry_price).
  // Opzione 2: Sposta lo stop a un punto in cui il rischio per contratto non è superiore al rischio iniziale per contratto.
END IF
```

---

## Dynamic Stop Adjustment (Post-Initial Profit)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 38, "Money management"
**Descrizione:** Dopo aver coperto i costi diretti e realizzato un primo profitto (liquidando una parte dei contratti), lo stop-loss per la posizione *rimanente* viene adeguato. L'aggiustamento dipende dalla velocità del mercato e prevede una delle due opzioni:
1.  **Stop a Pareggio:** Spostare lo stop al prezzo di entrata originale eseguito, garantendo di fatto nessuna perdita sulla parte rimanente.
2.  **Stop a Rischio Ridotto:** Spostare lo stop a un punto in cui il rischio per contratto rimanente non sia più elevato del rischio iniziale assunto per contratto all'inizio del trade.
**Logica Tecnica/Pseudocodice:**
```
// Dopo che PARTIAL_EXIT_ORDER è stato eseguito per coprire i costi e prendere un po' di profitto:

IF market_speed == FAST OR preference_is_break_even THEN
  SET STOP_LOSS_ORDER for remaining_contracts TO executed_entry_price.
END IF

ELSE IF market_speed == NORMAL OR preference_is_reduced_risk THEN
  CALCULATE max_initial_risk_per_contract // (dalla configurazione iniziale).
  DETERMINE new_stop_price_to_match_max_initial_risk_per_contract // (dal prezzo di esecuzione).
  SET STOP_LOSS_ORDER for remaining_contracts TO new_stop_price_to_match_max_initial_risk_per_contract.
END IF
```

---

## Trailing Stop Variants (Runner)
**Libro/File Originale:** [Untitled Document]
**Contesto/Pagina:** Pagina 40, "E se il mio ultimo stop non viene toccato..."
**Descrizione:** Per i contratti finali "runner", dopo che gli obiettivi di profitto iniziali sono stati raggiunti e gli stop sono stati spostati a pareggio o a rischio ridotto, lo stop viene continuamente trascinato. Sono suggeriti diversi metodi:
1.  Mantenere una distanza fissa in dollari (es. $150) dal massimo più recente (per i trade lunghi).
2.  Spostare lo stop di un importo fisso (es. $50) per ogni movimento di prezzo fisso (es. $100) a favore del mercato.
3.  Posizionare lo stop appena sotto il minimo dell'ultimo ritracciamento del mercato prima di un nuovo rally (per i trade lunghi).
4.  Posizionare lo stop uno o due tick sotto una media mobile che segue da vicino il movimento del prezzo.
**Logica Tecnica/Pseudocodice:**
```
// Per i contratti "runner" rimanenti (esempio trade LONG):

// Opzione 1: Distanza fissa in dollari dal massimo recente
SET TRAILING_STOP_PRICE = current_high - fixed_dollar_amount_in_points (es. $150 / valore_tick).

// Opzione 2: Movimento incrementale dello stop
IF price_moves_up_by_X_dollars THEN
  INCREASE TRAILING_STOP_PRICE by Y_dollars_in_points (es. $50 per ogni $100 in aumento).
END IF

// Opzione 3: Sotto il minimo dell'ultimo ritracciamento
IDENTIFY last_retracement_low.
SET TRAILING_STOP_PRICE = last_retracement_low - small_buffer_in_points (es. 1-2 tick).

// Opzione 4: Sotto una media mobile
CALCULATE short_term_moving_average.
SET TRAILING_STOP_PRICE = short_term_moving_average - small_buffer_in_points (es. 1-2 tick).
```

### [PARTE 4: merged_clean_part_04_p121-160.pdf]

## Trade Example (Ribasso - Short)
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 136
**Descrizione:** Questo è un esempio di un trade al ribasso. Il trader entra vendendo a un prezzo specifico, prende profitti in due fasi e gestisce il terzo contratto per lasciarlo correre, aggiustando lo stop per proteggere il profitto.
**Logica Tecnica/Pseudocodice:**
1.  **Apertura:** Prezzi a 1402.5.
2.  **Minimo Giorno 1:** Raggiunto 1399.
3.  **Entrata:** Vendere a 1388.
4.  **Primo Profitto (TP1):** 1377.
5.  **Secondo Profitto (TP2):** 1365.
6.  **Gestione Contratto Rimanente:** Lasciare correre un contratto.
7.  **Aggiustamento Stop:** Quando i prezzi raggiungono 1340 (48 punti di profitto sul contratto rimanente), spostare lo stop a 1364 (proteggendo il 50% del profitto sulla carta).
8.  **Uscita Finale:** Chiusura della posizione a 1364, con un profitto netto di 24 tick sull'ultimo contratto.

---

## Filosofia di Trading: Presa di Profitto Sistematico
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 137, 148, 155
**Descrizione:** La regola fondamentale è prendere i profitti in modo sistematico e secondo un piano prestabilito, senza lasciarsi bloccare dall'avidità. È meglio prendere piccoli profitti costantemente che rischiare di perderli cercando di ottenere il massimo dal mercato.
**Logica Tecnica/Pseudocodice:**
1.  **Identificare Profitti:** Quando i profitti sono disponibili.
2.  **Azione:** Prendere i profitti in modo sistematico.
3.  **Obiettivo:** Coprire i costi e accumulare guadagni.
4.  **Evitare:** Non cercare di ottenere il massimo assoluto o il minimo assoluto del mercato.
5.  **Principio:** "Prendo qualcosa dal tavolo quando ci sono profitti disponibili."

---

## Entrata su Rottura di Congestione (Filtro di Trading)
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 139, 140
**Descrizione:** La tecnica principale di entrata consiste nel fare trading sulla rottura di un'area di congestione che si forma appena prima di un segnale di entrata (principale o intermedio). Questo permette di entrare in anticipo nel trade e di avere un "cuscinetto" di profitto.
**Logica Tecnica/Pseudocodice:**
1.  **Identificare Segnale di Entrata:** Rilevare un segnale di entrata principale o intermedio (es. rottura di un massimo/minimo giornaliero).
2.  **Identificare Congestione Precedente:** Individuare un'area di congestione (consolidamento di prezzi) che si è formata immediatamente prima del punto di rottura del segnale di entrata.
3.  **Entrata:** Entrare nel trade sulla rottura di questa congestione, piuttosto che aspettare la rottura effettiva del massimo o minimo giornaliero.
4.  **Beneficio 1 (Entrata Molto Precoce):** Se la congestione è lontana dal punto di rottura giornaliero, i prezzi quasi certamente testeranno l'area del massimo/minimo. Lo spazio tra la rottura della congestione e il massimo/minimo è l'area di profitto.
5.  **Beneficio 2 (Entrata Non Molto Precoce):** Se la congestione è vicina al punto di rottura giornaliero, i prezzi quasi certamente formeranno un nuovo massimo/minimo. Lo spazio tra la rottura della congestione e il nuovo massimo/minimo è l'area di profitto.

---

## Entrata su Nuovi Estremi Senza Congestione (Non-Gap Breakout)
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 140
**Descrizione:** Se non si riesce a trovare un'area di congestione per un'entrata basata su rottura, ma il mercato sta formando nuovi massimi o minimi rispetto agli ultimi tre giorni o più, è possibile entrare su una rottura *non in gap* del massimo o minimo di ieri.
**Logica Tecnica/Pseudocodice:**
1.  **Condizione 1:** Assenza di un'area di congestione chiara prima del massimo/minimo di ieri.
2.  **Condizione 2:** I prezzi stanno formando nuovi massimi o minimi rispetto agli ultimi tre giorni o più.
3.  **Entrata:** Entrare sulla rottura (non in gap) del massimo o minimo di ieri.

---

## Gestione dell'Entrata in Assenza di Congestione (Apertura Vicino al Massimo)
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 141
**Descrizione:** Quando non ci sono congestioni evidenti prima del massimo, e i prezzi aprono vicino o sotto il massimo di ieri, si possono adottare approcci diversi con vari livelli di rischio.
**Logica Tecnica/Pseudocodice:**
1.  **Scenario:** Prezzi aprono sotto o al livello del massimo di ieri, senza congestione precedente.
2.  **Opzione 1 (Rischiosa):** Prendere una rottura diretta del massimo come entrata.
    *   **Rischio:** Rischio di un movimento breve seguito da un ritracciamento. Richiede di essere pronti a rischiare più del normale.
3.  **Opzione 2 (Prudente - Preferita):** Aspettare e osservare.
    *   **Trigger:** Se i prezzi aprono sotto il massimo e continuano a muoversi per un po' nell'area della chiusura, formando la congestione desiderata.
    *   **Entrata:** Entrare sulla rottura di questa congestione.
    *   **Vantaggio:** Mantiene il rischio entro la volatilità media per contratto.
4.  **Opzione 3 (Rottura Veloce):** Se i prezzi aprono e superano velocemente il massimo.
    *   **Azione:** Aspettare un possibile ritracciamento che testarà il massimo come supporto.
    *   **Entrata:** Entrare dopo il ritracciamento confermato.

---

## Entrata su Seconda Rottura vs. Prima Rottura
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 142
**Descrizione:** Prendere la prima rottura del massimo senza una congestione precedente è considerato più rischioso. È preferibile aspettare la formazione di una congestione per aumentare le probabilità di successo e ridurre il rischio.
**Logica Tecnica/Pseudocodice:**
1.  **Evitare:** Non entrare sulla *prima rottura* di un massimo se non c'è stata una congestione precedente. Questo è un trade più rischioso.
2.  **Attendere:** Aspettare che si formi una congestione.
3.  **Entrata Ottimale:** Entrare sulla rottura di una congestione ben formata (considerata una "seconda rottura" in senso figurato o temporale rispetto al primo tentativo di breakout).
4.  **Beneficio:** Maggiori probabilità di successo e nessun aumento del rischio.

---

## Filosofia di Trading: Pazienza e Coerenza ("A mio modo o non lo voglio")
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 142, 155, 157
**Descrizione:** È fondamentale essere pazienti e aspettare che il mercato offra le condizioni di trading desiderate, anche a costo di perdere un movimento. Il trade deve corrispondere esattamente al proprio piano, altrimenti non si prende.
**Logica Tecnica/Pseudocodice:**
1.  **Definizione del Proprio Modo:** Stabilire chiaramente le condizioni ideali per un trade (es. formazione di congestione in un'area specifica).
2.  **Monitoraggio:** Osservare il mercato per l'emergere di queste condizioni.
3.  **Azione:** Entrare nel trade *solo* se le condizioni corrispondono esattamente al proprio piano.
4.  **Inazione:** Se il mercato si muove senza presentare le condizioni desiderate, "lasciarlo andare" e non entrare.
5.  **Principio:** "Lo voglio a mio modo o non lo voglio affatto." / "Se non accade a mio modo, dimentico quel trade. Il trade deve essere il mio mio trade." / "A mio modo o non lo voglio!"

---

## Rientro/Continuazione del Trade dopo Stop a Pareggio
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 143, 165
**Descrizione:** Se un segnale di rottura si verifica di nuovo dopo essere stati stoppati a pareggio, è accettabile rientrare nel trade per cercare di raggiungere gli obiettivi prefissati, purché il segnale sia ancora valido.
**Logica Tecnica/Pseudocodice:**
1.  **Condizione Precedente:** Essere stati fermati (probabilmente a pareggio o con un piccolo profitto) da un trade precedente.
2.  **Riapparizione Segnale:** Una rottura valida del massimo (o minimo) che era un segnale accettabile in precedenza si presenta di nuovo.
3.  **Azione:** Entrare di nuovo al rialzo (o al ribasso) sulla rottura successiva.
4.  **Obiettivo:** Raggiungere gli obiettivi di profitto stabiliti.

---

## Filosofia di Trading: Semplicità del Movimento dei Prezzi
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 150, 152, 153
**Descrizione:** Il trading efficace si basa sulla comprensione del semplice movimento dei prezzi, non sulla complicazione di indicatori tecnici o formule complesse. La verità del mercato risiede nella sua azione di prezzo diretta.
**Logica Tecnica/Pseudocodice:**
1.  **Focus Primario:** Osservare e interpretare il movimento dei prezzi sul grafico.
2.  **Ignorare Complessità:** Evitare indicatori tecnici complessi, medie mobili multiple, oscillatori, trend line arbitrarie, e teorie predittive (es. Elliott Waves, Gann, Fibonacci) che mascherano i dettagli.
3.  **Identificare Tendenza:** Determinare se il mercato sta salendo, scendendo o muovendosi lateralmente basandosi sull'osservazione visiva.
4.  **Principio:** "Il mio migliore consiglio... è di lavorare per imparare a comprendere il semplice movimento dei prezzi. Imparare a leggerlo e a interpretare ciò che sta dicendo."

---

## Critica all'Overbought/Oversold e agli Indicatori
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 151, 152
**Descrizione:** Il concetto di "ipercomprato" o "ipervenduto" è fallace e gli indicatori tecnici sono in gran parte senza valore. I mercati possono rimanere in stati di "iper" per lunghi periodi e gli indicatori spesso divergono senza prevedere accuratamente le inversioni.
**Logica Tecnica/Pseudocodice:**
1.  **Non fare affidamento su:** Indicatori di ipercomprato/ipervenduto. I mercati possono sfidare queste letture per anni.
2.  **Non fare affidamento su:** Oscillatori derivati da medie mobili (o altri indicatori) che sono correlati e non aggiungono informazioni significative all'azione del prezzo grezza.
3.  **Evitare:** L'uso di impostazioni arbitrarie per gli indicatori ("numeri magici") nella speranza di trovare una "carta vincente".
4.  **Contrario a:** Utilizzare la divergenza dell'oscillatore come un segnale affidabile, poiché i mercati possono continuare a trendare in una direzione mentre l'oscillatore si muove in quella opposta.

---

## Caratteristiche delle Congestioni Preferite
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 161, 167, 168
**Descrizione:** Vengono descritte le caratteristiche delle aree di congestione più favorevoli per il trading, con enfasi sulla loro forma e sulla concentrazione dei prezzi.
**Logica Tecnica/Pseudocodice:**
1.  **Forma Preferita (Priorità 1):** Congestioni "quadrate e piatte".
2.  **Forma Preferita (Priorità 2):** Congestioni che si ripetono allo stesso livello di prezzo.
3.  **Dimensione:** L'area quadrata non deve essere "troppo alta" (massimo-minimo stretto).
4.  **Focalizzazione:** Ignorare i massimi/minimi esterni all'area. Preferire raggruppamenti stretti di aperture, chiusure, massimi e minimi in uno spazio molto ristretto.
5.  **Qualità (per re-entry):** Preferire le congestioni più strette. Questo evita preoccupazioni.

---

## Gestione dei Tre Contratti
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 163
**Descrizione:** Una strategia per gestire un trade con tre contratti, mirata a coprire i costi, prendere profitti intermedi e lasciare correre una parte del trade per catturare grandi movimenti.
**Logica Tecnica/Pseudocodice:**
1.  **Obiettivo:** Essere nel mercato quando "corre" (la maggior parte dei profitti).
2.  **Primo Contratto (Copertura Costi):**
    *   **Azione:** Appena si vede un profitto minimo (es. $100), liquidare il primo insieme di contratti.
    *   **Stop Management:** Spostare lo stop per i restanti contratti (preferibilmente entrambi) a pareggio.
3.  **Secondo Contratto (Profitto Intermedio):**
    *   **Azione:** Se il mercato continua a salire (es. un altro incremento di $100), liquidare il secondo insieme di contratti.
4.  **Terzo Contratto (Lasciare Correre):**
    *   **Azione:** Lasciare correre il terzo contratto. Lo stop è a pareggio.
    *   **Risultato Comune:** Spesso stoppato a pareggio se il mercato non si muove molto.
    *   **Obiettivo Raggiunto:** Se il mercato fa una corsa significativa, il terzo contratto cattura una parte del movimento.
5.  **Non Inseguire:** Se stoppato e il mercato corre dopo, non inseguire il trade.

---

## Re-entry/Continuazione del Trade (I-K)
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 165
**Descrizione:** Questa sezione descrive una potenziale ri-entrata o continuazione del trade (identificata come I-K) dopo un primo set di profitti (A-H). Il trader valuta il rischio aggiuntivo rispetto ai profitti potenziali. Viene menzionata una correlazione vaga con le "onde" (senza riferimento esplicito a Elliott Waves).
**Logica Tecnica/Pseudocodice:**
1.  **Contesto:** Dopo aver completato un ciclo di profitto (A-H) con i contratti iniziali.
2.  **Potenziale Rientro:** Identificazione di una nuova opportunità di entrata (I-K) che ripete la logica della prima.
3.  **Decisione di Rischio:** Considerare che, sebbene ci possano essere buoni profitti, si corrono rischi aggiuntivi rientrando. Il trader non entra sempre in questi set di continuazione.
4.  **Criterio (Vago):** La decisione di rientrare "ha a che fare con le onde" (questo è un elemento più soggettivo e non puramente tecnico, con il disclaimer che se fosse correlato a Elliott Waves, sarebbe una pura coincidenza).

---

## Entrata sulla Rottura della Seconda Congestione (per Continuazione)
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 166, 167
**Descrizione:** Per i trade di continuazione, il trader preferisce entrare sulla rottura di una "seconda congestione" che si forma dopo un primo movimento. Questa tecnica è preferibile se la congestione è piatta e non una "bandiera".
**Logica Tecnica/Pseudocodice:**
1.  **Contesto:** Dopo un movimento iniziale significativo (es. rottura di una prima congestione).
2.  **Identificare:** Una "seconda congestione" (un'area di consolidamento) che si forma dopo il primo movimento.
3.  **Condizione sulla Forma:** Entrare *solo* se la seconda congestione è "relativamente piatta".
4.  **Evitare:** Non entrare se la formazione è una "bandiera" (flag), poiché in questo caso i prezzi tendono a consumare gran parte dello slancio per tornare al punto più alto e non si spingono lontano prima di entrare nuovamente in congestione.
5.  **Timing:** La rottura deve avvenire almeno un'ora prima della chiusura del trading.

---

## Trading di Inversione (Reversal Trading)
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 172
**Descrizione:** Il trading di inversione è appropriato in condizioni di "attività febbrile" del mercato e si basa sull'identificazione di "outside bars" seguite da una rottura di congestione. Le regole di entrata sono simili a quelle dei trade direzionali.
**Logica Tecnica/Pseudocodice:**
1.  **Condizione di Mercato:** Attività febbrile nei mercati.
2.  **Pattern:** Identificare una "barra outside" (prezzo rompe il massimo della barra precedente, inverte e rompe il minimo della barra precedente; può essere molto ampia).
3.  **Regole di Entrata:** Simili al trading direzionale:
    *   Entrare sulla rottura di una congestione *più lunga, più stretta e migliore* che si è verificata *prima dell'estremo* (della outside bar).
4.  **Flessibilità:** È possibile entrare al rialzo, poi al ribasso, anche più volte nella stessa giornata e nella direzione opposta al trade iniziale, senza cambiare la tattica (entry/exit/strategy).

---

## Trading con Gap
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 172, 173
**Descrizione:** Strategia per gestire le aperture in gap, distinguendo tra gap che saltano la congestione di entrata e gap che ritracciano in una congestione precedente.
**Logica Tecnica/Pseudocodice:**
1.  **Scenario 1 (Gap oltre la congestione di entrata):**
    *   **Azione:** Lasciare andare il trade. Non entrare.
2.  **Scenario 2 (Gap nel Ritracciamento):**
    *   **Apertura:** Prezzi aprono in gap.
    *   **Ritracciamento:** I prezzi ritornano nella congestione di ieri (o una congestione precedente fino a tre giorni fa) prima del massimo.
    *   **Formazione:** Segue una nuova congestione oggi.
    *   **Entrata:** Entrare sulla rottura di questa nuova congestione, come originariamente pianificato.
3.  **Scenario 3 (Gap e Rottura in Direzione dell'Apertura):**
    *   **Apertura:** Prezzi aprono in gap.
    *   **Ritracciamento:** I prezzi ritracciano fino a una trading range precedente.
    *   **Rottura:** Poi rompono nella direzione dell'apertura iniziale.
    *   **Entrata:** Entrare sulla rottura di questa congestione.

---

## Prima Rottura vs. Seconda Rottura (Prudenza e Falsi Segnali)
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 174, 175
**Descrizione:** Viene offerta una scelta tra prendere la prima o la seconda rottura di una congestione che precede un segnale di entrata. La seconda rottura è considerata più prudente e aiuta a evitare molti falsi segnali, sebbene possa far perdere alcuni trade "buoni".
**Logica Tecnica/Pseudocodice:**
1.  **Contesto:** Identificare una congestione prima di un segnale di entrata (es. rottura del massimo di una trading range).
2.  **Tecnica Iniziale (Prima Rottura):** Entrare sulla *prima rottura* di questa congestione.
3.  **Tecnica Alternativa (Seconda Rottura - Preferita e più Prudente):** Aspettare una *falsa rottura* o un ritracciamento e poi entrare sulla *successiva rottura* della stessa area di congestione.
    *   **Vantaggio:** Evita molti falsi segnali.
    *   **Svantaggio:** Si perdono alcuni buoni trade in cui il prezzo si muove senza un ritracciamento.
4.  **Condizione della Seconda Rottura:** In un contesto ribassista, il secondo attraversamento deve rompere il minimo del primo attraversamento (o il primo breakout).

---

## Segnale di Entrata Minore
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 177
**Descrizione:** Un segnale di entrata facoltativo basato sulla rottura della prima congestione che si forma dopo l'apertura del mercato, eventualmente proseguendo dal giorno precedente.
**Logica Tecnica/Pseudocodice:**
1.  **Definizione:** La rottura della prima congestione che si forma sul grafico dopo l'apertura. Questo può includere congestione dal giorno precedente.
2.  **Opzionalità:** È un segnale facoltativo; i segnali principali o intermedi sono preferibili.
3.  **Scelta di Rottura:**
    *   **Prima Rottura:** Tende a prenderla se la congestione è molto lunga e sinuosa.
    *   **Seconda Rottura:** Preferita in generale, è più prudente ma spesso non permette l'entrata.
4.  **Spinta:** La prima rottura spesso manca di spinta, a meno che non sia una continuazione dal giorno precedente.
5.  **Priorità:** Se la prima congestione coincide con un segnale più importante, viene trattata come il segnale più importante. Altrimenti, è un segnale a sé stante.

---

## Criteri Aggiuntivi per i Trade di Continuazione
**Libro/File Originale:** Estratti dal libro sul trading
**Contesto/Pagina:** Pagina 171
**Descrizione:** Due regole aggiuntive per decidere quando prendere un trade di continuazione.
**Logica Tecnica/Pseudocodice:**
1.  **Profitto del Terzo Contratto:** Prendere un trade di continuazione solo quando il terzo insieme di contratti (del trade iniziale) è in profitto.
2.  **Retracciamento Limitato:** Il terzo insieme di contratti non deve essere stato chiuso da un ritracciamento del 50%.
3.  **Pattern Specifico:** I migliori trade di continuazione derivano da un "Ross Hook con estremo acuto". Se l'uncino ha un massimo piatto, la continuazione generalmente non andrà lontano.

---

### [PARTE 5: merged_clean_part_05_p161-200.pdf]

## Breakout to the Downside (General Concept)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 181)
**Contesto/Pagina:** Pagina 181
**Descrizione:** Il concetto di una rottura verso il basso, dove i prezzi superano un livello significativo al ribasso. L'autore osserva tali rotture ma è scettico sull'efficacia di "supporti" e "resistenze" tradizionali, ritenendo che i prezzi possano muoversi attraverso questi punti per volontà degli operatori forti senza una logica economica di offerta e domanda.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE un movimento di prezzo che rompe al ribasso un livello precedentemente consolidato o un'area di congestione.
2.  SE la rottura è troppo vicina a un presunto "supporto", la validità del trade può essere compromessa.
3.  EVITARE trade su rotture vicino a supporti se non si tiene conto della manipolazione dei "grandi operatori".

---

## Timeliness of Breakout for Entry
**Libro/File Originale:** Estratti dal libro del corso (Pagina 182)
**Contesto/Pagina:** Pagina 182
**Descrizione:** L'importanza della tempestività dell'entrata su una rottura. Se una rottura si verifica troppo tardi nella giornata, potrebbe non essere utile per un trade profittevole.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE una rottura di prezzo (ad esempio, verso l'alto).
2.  SE la rottura si verifica in un momento avanzato della sessione di trading (troppo tardi), ALLORA non utilizzare l'opportunità per un trade.
3.  IL MOMENTO della rottura è un fattore critico per la decisione di entrata.

---

## Trading su Crollo di Mercato dopo Gap Up (con Problemi Dati)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 183)
**Contesto/Pagina:** Pagina 183
**Descrizione:** Una situazione in cui il mercato apre in gap verso l'alto, ma poi inizia a crollare. L'autore, nonostante problemi di dati in tempo reale, piazza un ordine di vendita in base a dove l'avrebbe piazzato il giorno precedente, sotto un'area chiave.
**Logica Tecnica/Pseudocodice:**
1.  RILEVARE un'apertura di mercato con un gap verso l'alto rispetto alla chiusura precedente.
2.  OSSERVARE l'inizio di un crollo dei prezzi dopo l'apertura in gap.
3.  IDENTIFICARE un punto di vendita predefinito o un'area chiave (ad esempio, appena sotto una piccola area di congestione o un livello predeterminato).
4.  ENTRARE VENDUTO in questo punto, anche se il mercato non ha "corso" molto lontano dopo il crollo iniziale, per realizzare profitti.

---

## Identificazione dei Pivot (Punti di Congestione)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 185)
**Contesto/Pagina:** Pagina 185
**Descrizione:** I "pivot" sono punti naturali di "supporto/resistenza" identificati dall'autore non attraverso teorie tradizionali, ma osservando raggruppamenti di aperture, chiusure, massimi e minimi molto vicini tra loro sul grafico. Questi punti sono dove gli "operatori interni" (insider) accumulano ordini.
**Logica Tecnica/Pseudocodice:**
1.  SCANSIONARE il grafico dei prezzi.
2.  IDENTIFICARE aree in cui le barre consecutive mostrano aperture, chiusure, massimi e minimi raggruppati entro un intervallo di prezzo molto stretto (ad esempio, uno o due tick).
3.  QUELLE aree sono considerate "pivot" e indicano congestione e accumulo di ordini.

---

## Interpretazione dei Movimenti dei Prezzi Vicino ai Segnali di Entrata (Insider vs. Pubblico)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 186)
**Contesto/Pagina:** Pagina 186
**Descrizione:** Quando i prezzi si raggruppano vicino a un segnale di entrata, possono verificarsi due scenari: o gli operatori interni spingono i prezzi fino a un estremo e si fermano (formando un segnale di massimo o minimo), oppure spingono oltre e il pubblico li segue, causando una rottura del segnale di entrata. L'autore si posiziona ai lati di queste congestioni, accettando di perdere i primi tick che gli insider possono catturare, aspettando una chiara conferma del movimento.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE un'area di congestione vicino a un potenziale segnale di entrata.
2.  PREPARARE ordini di entrata su entrambi i lati della congestione.
3.  ATTENDERE un movimento effettivo dei prezzi che rompa la congestione.
4.  ENTRARE nella direzione della rottura, accettando di non catturare i primi movimenti generati dagli "insider".

---

## Gestione del Trade su Rottura di Congestione e all'Estremo
**Libro/File Originale:** Estratti dal libro del corso (Pagina 187)
**Contesto/Pagina:** Pagina 187
**Descrizione:** Strategia di gestione del trade a più livelli. All'inizio, si entra con tre lotti. Si liquida una parte per coprire i costi e ottenere un piccolo profitto. Poi si sposta lo stop a pareggio per il lotto rimanente. Il profitto maggiore si realizza se il pubblico entra nel trade dopo la rottura del punto estremo. L'autore accetta spesso di essere stoppato a pareggio sul lotto finale.
**Logica Tecnica/Pseudocodice:**
1.  ENTRARE con N=3 contratti sulla rottura di una congestione, a condizione che ci sia sufficiente distanza tra la rottura e il punto estremo per coprire i costi e realizzare un profitto minimo.
2.  QUANDO si vede un guadagno accettabile, LIQUIDARE 1 o 2 contratti (N-1 o N-2).
3.  SPOSTARE lo stop loss per i contratti rimanenti (N=1) a pareggio.
4.  SE il punto estremo si rompe e il pubblico entra nel trade, il contratto rimanente (N=1) genererà profitti maggiori.
5.  QUANDO si vede un profitto accettabile sul contratto rimanente, SPOSTARE lo stop loss protettivo per garantire almeno il 50% del profitto realizzato "sulla carta".

---

## Trailing Stop per Grandi Trend e Trading di Continuazione
**Libro/File Originale:** Estratti dal libro del corso (Pagina 188)
**Contesto/Pagina:** Pagina 188
**Descrizione:** Descrive come gestire un trade per catturare grandi profitti in trend sostenuti. Si sposta lo stop loss seguendo una media mobile ritardata o posizionandolo appena fuori dai supporti/resistenze naturali. L'autore valuta anche il trading di continuazione su "Ross Hook" e "Ledge" ben definiti, ma è consapevole dei maggiori rischi associati a questi trade aggiuntivi.
**Logica Tecnica/Pseudocodice:**
1.  SE il mercato entra in un trend sostenuto ("prezzi decollano e non tornano indietro"):
    *   SPOSTARE lo stop loss seguendo una media mobile ritardata.
    *   IN ALTERNATIVA, posizionare lo stop loss appena fuori dai punti di supporto e resistenza naturali.
2.  CONSIDERARE trading di continuazione su formazioni "Ross Hook" e "Ledge" *ben definite*.
3.  ESSERE CONSAPEVOLI che i contratti di continuazione comportano rischi maggiori e possono erodere profitti precedentemente guadagnati.
4.  L'entrata sulla rottura della trading range, *prima* della rottura dell'estremo, offre un vantaggio sui trader giornalieri, permettendo di vendere quando loro comprano e viceversa.
5.  SE l'ingresso dei trader giornalieri e dei daytrader è sufficiente, la terza serie di contratti realizzerà grandi profitti.

---

## Pattern: Apertura in Gap con Pausa/Ritracciamento
**Libro/File Originale:** Estratti dal libro del corso (Pagina 189)
**Contesto/Pagina:** Pagina 189
**Descrizione:** Uno schema di prezzo intraday in cui il mercato apre con un gap, seguito da una fase di pausa o ritracciamento. L'entrata si effettua acquistando (o vendendo) l'estremo della fascia di apertura dopo questa pausa/ritracciamento.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE un'apertura di mercato con un gap (es. gap up).
2.  ATTENDERE che i prezzi formino una pausa (congestione) o un ritracciamento nell'area della congestione, preferibilmente vicino al massimo (o minimo) precedente.
3.  COMPRARE (o VENDERE) la rottura dell'estremo della fascia di apertura (es. il massimo della congestione iniziale) dopo la pausa/ritracciamento.

---

## Pattern: Doppio Attraversamento con Congestione
**Libro/File Originale:** Estratti dal libro del corso (Pagina 190)
**Contesto/Pagina:** Pagina 190
**Descrizione:** Descrive una situazione dove, dopo un'apertura, il prezzo forma una prima congestione ("Primo attraversamento"), poi rompe, e ritraccia per formare una seconda congestione ("Secondo attraversamento"), spesso vicino a un livello chiave come il massimo del giorno precedente. L'entrata avviene sulla rottura della seconda congestione.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE un'apertura (Open).
2.  OSSERVARE la formazione di una "Primo attraversamento" (prima congestione).
3.  OSSERVARE una rottura seguita da un ritracciamento che porta alla formazione di un "Secondo attraversamento" (seconda congestione).
4.  SE la seconda congestione è vicina a un livello di riferimento (es. Massimo di ieri), ALLORA COMPRARE sulla rottura verso l'alto di questa seconda congestione.

---

## Entrata su Rottura del Massimo di Ieri dopo Ritracciamento
**Libro/File Originale:** Estratti dal libro del corso (Pagina 190)
**Contesto/Pagina:** Pagina 190
**Descrizione:** Un'entrata valida per segnali principali o intermedi. Si osserva un ritracciamento verso la congestione del giorno precedente. Se non c'è spazio sufficiente (tick) tra la congestione attuale e il massimo di ieri per un'entrata sicura, si aspetta la rottura del massimo di ieri.
**Logica Tecnica/Pseudocodice:**
1.  OSSERVARE un ritracciamento dei prezzi verso l'area di congestione del giorno precedente.
2.  VALUTARE la distanza in tick tra la fine della congestione attuale e il Massimo di ieri.
3.  SE la distanza è insufficiente per un'entrata profittevole prima della rottura del Massimo di ieri, ALLORA ATTENDERE.
4.  COMPRARE (o VENDERE, se al ribasso) la rottura del Massimo di ieri (o Minimo di ieri).

---

## Pattern: Congestione Larga -> POP -> Congestione Stretta
**Libro/File Originale:** Estratti dal libro del corso (Pagina 191)
**Contesto/Pagina:** Pagina 191
**Descrizione:** Considerato uno dei migliori schemi di trading. Si verifica un'ampia congestione, seguita da una "POP" (piccola esplosione di prezzo in qualsiasi direzione), e poi una congestione più stretta. Questo schema è valido su qualsiasi segnale di entrata principale o intermedio.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE un'area di "Congestione larga".
2.  OSSERVARE un "POP" (piccola esplosione) dei prezzi fuori dalla congestione larga (la direzione del POP non è rilevante per la validità dello schema).
3.  OSSERVARE la formazione di una "Congestione stretta" dopo il POP.
4.  VENDERE (o COMPRARE) la rottura della congestione stretta.
5.  Avere un'altra possibilità di vendita (o acquisto) sulla rottura di un Minimo (o Massimo) di ieri.

---

## Pattern: Gap, Ritracciamento alla Congestione, Nuova Congestione e Rottura
**Libro/File Originale:** Estratti dal libro del corso (Pagina 193)
**Contesto/Pagina:** Pagina 193
**Descrizione:** Dopo un gap, i prezzi ritracciano verso i massimi (o minimi) della congestione più vicina al massimo (o minimo) del giorno precedente. Poi si forma una nuova congestione e la rottura di questa è più vicina al riferimento del giorno precedente. L'entrata dipende dalle dimensioni relative delle due congestioni.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE un'apertura in gap.
2.  OSSERVARE un ritracciamento dei prezzi ai massimi (per gap up) o minimi (per gap down) della congestione più vicina al massimo (o minimo) di ieri.
3.  OSSERVARE la formazione di una nuova congestione ("congestione oggi") e una sua successiva rottura. Questa nuova congestione deve essere più vicina al massimo (o minimo) di ieri rispetto alla congestione precedente.
4.  SE le due congestioni (quella di ieri e quella di oggi) sono di dimensioni simili (da massimo a minimo):
    *   ENTRARE LONG sulla rottura della congestione collocata più in alto.
    *   ENTRARE SHORT sulla rottura della congestione collocata più in basso.
5.  ALTRIMENTI (se le congestioni non sono di dimensioni simili):
    *   ENTRARE sulla rottura della congestione più stretta.

---

## Pattern: Apertura in Gap a Nuovo Massimo (o Minimo) su Tre Giorni
**Libro/File Originale:** Estratti dal libro del corso (Pagina 194)
**Contesto/Pagina:** Pagina 194
**Descrizione:** Regole specifiche per operare su aperture in gap che creano un nuovo massimo (o minimo) degli ultimi tre giorni, considerando la presenza o l'assenza di ritracciamenti e formazioni di congestione.
**Logica Tecnica/Pseudocodice:**
1.  **Scenario: Gap Up a Nuovo Massimo su tre giorni.**
    *   **Senza ritracciamento:**
        *   SE (Apertura in gap a nuovo massimo su tre giorni) E (NON c'è ritracciamento a una congestione degli ultimi tre giorni), ALLORA: NON ENTRARE.
    *   **Con ritracciamento parziale:**
        *   SE (Apertura in gap a nuovo massimo su tre giorni) E (Ritracciamento a metà o al minimo di una congestione degli ultimi tre giorni), ALLORA: ENTRARE NEL TRADE.
    *   **Con ritracciamento e nuova congestione simile:**
        *   SE (Apertura in gap a nuovo massimo su tre giorni) E (Ritracciamento a una congestione degli ultimi tre giorni) E (seguito da un'altra congestione di dimensioni simili), ALLORA: ENTRARE SULLA ROTTURA DELLA CONGESTIONE PIÙ IN ALTO.
2.  **L'opposto vale per l'entrata al ribasso (Gap Down a Nuovo Minimo su tre giorni).**

---

## Regola: Congestione a Massimo/Minimo Precedente con Ritracciamento Obbligatorio
**Libro/File Originale:** Estratti dal libro del corso (Pagina 195)
**Contesto/Pagina:** Pagina 195
**Descrizione:** Se una congestione si forma esattamente a un precedente massimo o minimo, è obbligatorio che ci sia un ritracciamento di almeno metà della congestione prima di poter entrare sulla rottura.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE una congestione che si forma esattamente al livello di un precedente massimo o minimo.
2.  VERIFICARE la presenza di un ritracciamento che penetri almeno a metà della congestione.
3.  SE (ritracciamento presente): CONSIDERARE l'entrata sulla rottura della congestione.
4.  SE (ritracciamento NON presente): NON ENTRARE sulla rottura della congestione.

---

## Trading Attraverso la Congestione
**Libro/File Originale:** Estratti dal libro del corso (Pagina 195)
**Contesto/Pagina:** Pagina 195
**Descrizione:** Un desiderio di fare un trade che attraversi l'area di congestione, indicando un'entrata sulla rottura della congestione stessa, piuttosto che aspettare che i prezzi si allontanino completamente.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE un'area di congestione.
2.  PREPARARE un ordine di acquisto (o vendita) sulla rottura della congestione.
3.  ESGUIRE l'ordine quando il prezzo rompe il limite superiore (per l'acquisto) o inferiore (per la vendita) della congestione.
4.  POTENZIALMENTE, combinare con la rottura di un massimo o minimo più ampio (es. il minimo generale, come nell'esempio di vendita).

---

## Regola: Confronto Dimensionale tra Congestioni (Base su Base)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 195)
**Contesto/Pagina:** Pagina 195
**Descrizione:** Quando si presentano due aree di congestione, la scelta del punto di entrata dipende dalla loro dimensione relativa e dalla distanza.
**Logica Tecnica/Pseudocodice:**
1.  **Scenario: Due congestioni di dimensioni quasi uguali (da massimo a minimo).**
    *   SE (Entrata al rialzo): ENTRARE sulla rottura della congestione collocata *più in alto*.
    *   SE (Entrata al ribasso): ENTRARE sulla rottura della congestione collocata *più in basso*.
    *   **Eccezione:** SE (ci sono sufficienti tick tra le due congestioni): È accettabile entrare sulla prima congestione e uscire quando i prezzi raggiungono la seconda.
2.  **Scenario: Due congestioni di dimensioni non uguali.**
    *   ENTRARE sulla rottura della congestione *più stretta*.

---

## Metodo di Calcolo Semplice per Trovare il Trend (Tre Massimi/Minimi Consecutivi)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 199)
**Contesto/Pagina:** Pagina 199
**Descrizione:** Un metodo prudente per identificare un trend nascente. Per un movimento al rialzo, si cercano tre barre consecutive con massimi più alti, a condizione che il mercato abbia mostrato una correzione formando un minimo inferiore durante la comparsa di questi massimi. Si compra la rottura del terzo massimo. Per movimenti al ribasso, si applicano regole opposte.
**Logica Tecnica/Pseudocodice:**
1.  **Per un movimento al rialzo (BUY):**
    *   IDENTIFICARE tre barre consecutive con massimi sempre più alti (HH1, HH2, HH3).
    *   CONDIZIONE: Il mercato deve aver mostrato una correzione, formando un minimo inferiore, mentre i tre massimi si sono formati.
    *   ENTRARE LONG sulla rottura del terzo massimo (HH3).
    *   USCIRE IMMEDIATAMENTE se i prezzi violano un minimo (formano un minimo inferiore) quando si suppone che si stiano muovendo verso l'alto.
2.  **Per un movimento al ribasso (SELL - regole opposte):**
    *   IDENTIFICARE tre barre consecutive con minimi sempre più bassi (LL1, LL2, LL3).
    *   CONDIZIONE: Il mercato deve aver mostrato una correzione, formando un massimo superiore, mentre i tre minimi si sono formati.
    *   ENTRARE SHORT sulla rottura del terzo minimo (LL3).
    *   USCIRE IMMEDIATAMENTE se i prezzi violano un massimo (formano un massimo superiore) quando si suppone che si stiano muovendo verso il basso.

---

## Entrata Successiva dopo Trade Perdente (Ross Hook)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 200)
**Contesto/Pagina:** Pagina 200
**Descrizione:** In caso di trade perdente dovuto alla formazione di un minimo inferiore dopo un segnale di acquisto, il prossimo tentativo di entrata può essere un tick sopra la barra di acquisto originale, poiché questa è diventata un "Ross Hook".
**Logica Tecnica/Pseudocodice:**
1.  SE un segnale di acquisto iniziale porta a un trade perdente (es. la barra successiva forma un minimo inferiore).
2.  CONSIDERARE la barra di acquisto iniziale come un "Ross Hook".
3.  IL PROSSIMO tentativo di entrata sarà un acquisto (o vendita) un tick sopra (o sotto) il massimo (o minimo) della barra che ha formato il "Ross Hook".

---

## Metodo di Calcolo Semplice - Tre Minimi Inferiori Consecutivi (SELL)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 204)
**Contesto/Pagina:** Pagina 204
**Descrizione:** Un metodo per identificare un'opportunità di vendita. Si attendono tre barre consecutive che formano minimi inferiori. L'entrata short avviene sulla rottura del minimo della terza barra.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE una sequenza di tre barre consecutive che formano minimi inferiori (LL1, LL2, LL3).
2.  SULLA quarta barra, VENDERE la rottura al ribasso del minimo della terza barra (LL3).

---

## Regola: Uscita su Barra Reversal
**Libro/File Originale:** Estratti dal libro del corso (Pagina 205)
**Contesto/Pagina:** Pagina 205
**Descrizione:** Se la barra in cui si è entrati finisce come una barra "reversal" (apertura inferiore alla chiusura in un trade short, o apertura superiore alla chiusura in un trade long), e i prezzi vanno immediatamente contro la posizione chiudendo oltre il massimo/minimo della barra precedente, è necessario uscire dal trade.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE la barra di entrata.
2.  SE la barra di entrata si chiude come una "reversal bar":
    *   IN un trade SHORT: (Open < Close) E (Close > Massimo della barra precedente).
    *   IN un trade LONG: (Open > Close) E (Close < Minimo della barra precedente).
3.  ALLORA USCIRE immediatamente dal trade.

---

## Pattern: Ross Hook (Implicitamente Definito)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 205)
**Contesto/Pagina:** Pagina 205
**Descrizione:** Dopo una barra di inversione (o un primo tentativo di trade fallito), se una barra successiva forma un minimo e un massimo più alti (per un contesto rialzista), questo crea un "Ross Hook". Se i prezzi correggono di nuovo verso il basso, si cerca di entrare al punto dell'uncino o prima che venga raggiunto.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE una barra di prezzo (Barra X).
2.  SE una barra successiva (Barra Y) forma un minimo più alto e un massimo più alto rispetto alla Barra X.
3.  ALLORA si è formato un "Ross Hook" sulla Barra X.
4.  SE i prezzi correggono dopo la Barra Y e ritornano verso il punto del minimo di Barra X (il "punto dell'uncino"), CONSIDERARE l'entrata LONG.
5.  (Opposto per un contesto ribassista: una barra successiva forma un massimo più basso e un minimo più basso, creando un Ross Hook sul massimo precedente).

---

## Trading TLOC: Rottura di Congestione (Ledge) prima di Massimo/Minimo di Ieri
**Libro/File Originale:** Estratti dal libro del corso (Pagina 206)
**Contesto/Pagina:** Pagina 206
**Descrizione:** Una tecnica basata sulla Legge Dei Grafici (TLOC). Si cerca una rottura di una congestione (chiamata "ledge") che si verifica *prima* che i prezzi rompano il massimo o il minimo del giorno precedente.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE una congestione ("ledge") sul grafico.
2.  CONDIZIONE: Questa congestione deve formarsi *prima* che i prezzi rompano il Massimo di ieri (per un long) o il Minimo di ieri (per uno short).
3.  ENTRARE (ad esempio, COMPRARE al punto B) sulla rottura di questa congestione.

---

## Trading Combinato: Calcolo Semplice + Formazione TLOC 1-2-3 (Rottura Massimo)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 206)
**Contesto/Pagina:** Pagina 206
**Descrizione:** Un'opportunità di trading che unisce il "metodo di calcolo semplice" con una formazione "1-2-3" della Legge Dei Grafici (TLOC). Si può entrare al ribasso sulla rottura del punto 2 della formazione 1-2-3, che è contemporaneamente supportata dalla logica del calcolo semplice (es. tre minimi inferiori consecutivi).
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE una formazione "1-2-3 Massimo" (derivante dalla TLOC).
2.  VERIFICARE che questa formazione sia accompagnata da un "calcolo semplice" (es. tre minimi inferiori consecutivi).
3.  ENTRARE SHORT sulla rottura al ribasso del punto 2 della formazione "1-2-3 Massimo".

---

## Calcolo Semplice con Condizione di Correzione per Entrata
**Libro/File Originale:** Estratti dal libro del corso (Pagina 207)
**Contesto/Pagina:** Pagina 207
**Descrizione:** Per utilizzare il "calcolo semplice" come segnale di entrata, è necessaria una correzione precedente. In un contesto ribassista, la correzione è una violazione del massimo della terza barra del calcolo semplice.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE un pattern dal "calcolo semplice" (es. tre minimi inferiori consecutivi che indicano un potenziale ribasso).
2.  ATTENDERE una "correzione" dei prezzi.
3.  IN un contesto ribassista, la correzione è una violazione al rialzo del massimo della barra indicata come "3" nel calcolo semplice (es. la terza barra con minimo inferiore).
4.  DOPO la correzione, SE i prezzi tornano a rompere al ribasso, ALLORA ENTRARE SHORT (es. alla rottura del punto 2 del massimo 1-2-3 combinato).

---

## Pattern: Doji Bar
**Libro/File Originale:** Estratti dal libro del corso (Pagina 208)
**Contesto/Pagina:** Pagina 208
**Descrizione:** Una barra di prezzo significativa dove l'apertura e la chiusura sono uguali o molto vicine. Può verificarsi a qualsiasi livello (massimo, minimo, intermedio). Indica una forte possibilità di cambiamento di direzione, interrompe un trend e mostra esitazione del mercato. È particolarmente rilevante se è anche una barra "interna" (inside bar).
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE una barra di prezzo dove `Abs(Open - Close) <= TickSizeTolerance`.
2.  (Opzionale, ma aumenta la significatività): VERIFICARE se la barra è una "inside bar" (`High <= PreviousHigh` E `Low >= PreviousLow`).
3.  INTERPRETAZIONE: Un segnale di indecisione del mercato, potenziale inversione di trend o interruzione del movimento attuale.

---

## Regola: Doji Bar come Segnale di Uscita/Aggiustamento Stop
**Libro/File Originale:** Estratti dal libro del corso (Pagina 209)
**Contesto/Pagina:** Pagina 209
**Descrizione:** Quando una barra doji si verifica all'interno di un trend in atto, la reazione usuale è di spostare il punto di uscita (stop loss) appena sopra (o sotto) l'estremo della barra doji.
**Logica Tecnica/Pseudocodice:**
1.  SE un trade è aperto in un trend (es. long in uptrend).
2.  E IDENTIFICARE una barra doji durante il trend.
3.  SPOSTARE lo stop loss a un tick sotto il minimo della barra doji.
4.  (Opposto per trade short in downtrend): Spostare lo stop loss a un tick sopra il massimo della barra doji.

---

## Metodo di Riconoscimento di Area di Congestione (Swing Formations)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 212)
**Contesto/Pagina:** Pagina 212
**Descrizione:** Per identificare un'area di congestione, si contano le formazioni "swing" (picchi e valli a forma di /\ o V/). Due swing, composti da quattro movimenti (legs), quasi sempre indicano congestione. Più swing nello stesso intervallo indicano una congestione più consolidata.
**Logica Tecnica/Pseudocodice:**
1.  SCANSIONARE il grafico dei prezzi per identificare formazioni a "swing" (minimi e massimi relativi che formano pattern a V o Λ).
2.  SE si identificano due swing consecutivi (composti da quattro "legs" o movimenti), ALLORA si è in presenza di un'area di congestione.
3.  UNA maggiore quantità di swing (es. tre o più) all'interno di un intervallo di prezzo conferma l'area di congestione.

---

## Metodo di Riconoscimento di Area di Congestione (Reversal Bars / Doji)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 212)
**Contesto/Pagina:** Pagina 212
**Descrizione:** Un'ottima maniera per riconoscere una congestione è osservare una serie di barre di inversione, una serie di doji, o una combinazione di entrambi. Questi pattern indicano indecisione e consolidamento del prezzo.
**Logica Tecnica/Pseudocodice:**
1.  SCANSIONARE il grafico per sequenze di barre.
2.  IDENTIFICARE una "serie di barre reversal" (barre in cui il prezzo si muove in una direzione e poi chiude vicino all'apertura o addirittura in inversione rispetto al movimento principale della barra).
3.  IDENTIFICARE una "serie di doji bars" (barre con apertura e chiusura molto vicine).
4.  SE si verifica una di queste condizioni (o una loro combinazione), ALLORA il mercato è in un'area di congestione.

---

## Metodo di Riconoscimento di Area di Congestione (Alternanza Apertura/Chiusura)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 213)
**Contesto/Pagina:** Pagina 213
**Descrizione:** Durante una fase di congestione, si osserva un'alternanza di barre "apertura alta-chiusura bassa" (corpi rossi/neri) e "apertura bassa-chiusura alta" (corpi verdi/bianchi). Questo comportamento, unito a un intervallo di prezzo ristretto, è un chiaro segno di congestione.
**Logica Tecnica/Pseudocodice:**
1.  OSSERVARE una sequenza di barre.
2.  IDENTIFICARE un'alternanza tra:
    *   Barre dove `Open > Close` (apertura alta - chiusura bassa).
    *   Barre dove `Open < Close` (apertura bassa - chiusura alta).
3.  CONDIZIONE: Questa alternanza deve avvenire all'interno di una "fascia stretta da massimo a minimo".
4.  SE queste condizioni sono soddisfatte, ALLORA l'area è una zona di congestione.

---

## Trading Tecnica: Tre Massimi Decrescenti (TLOC Style per Downtrend)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 216)
**Contesto/Pagina:** Pagina 216
**Descrizione:** Per individuare un potenziale trend al ribasso, si cercano tre massimi decrescenti consecutivi. A differenza del "calcolo semplice", non è necessario che anche i minimi siano decrescenti. Un segnale di entrata short si genera quando viene rotto il minimo della barra che ha formato il terzo massimo inferiore.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE tre barre consecutive che formano "Massimi Decrescenti" (Lower Highs - LH1, LH2, LH3). `LH1 > LH2 > LH3`.
2.  NOTA: I minimi delle barre NON devono essere necessariamente decrescenti.
3.  ENTRARE SHORT quando il prezzo rompe al ribasso il minimo della barra che ha formato il terzo massimo decrescente (LH3).

---

## Trading Tecnica: Tre Minimi Crescenti (TLOC Style per Uptrend)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 216)
**Contesto/Pagina:** Pagina 216
**Descrizione:** La controparte della tecnica dei massimi decrescenti per individuare un potenziale trend al rialzo. Si cercano tre minimi crescenti consecutivi. Un segnale di entrata long si genera quando viene rotto il massimo della barra che ha formato il terzo minimo superiore.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE tre barre consecutive che formano "Minimi Crescenti" (Higher Lows - HL1, HL2, HL3). `HL1 < HL2 < HL3`.
2.  NOTA: I massimi delle barre NON devono essere necessariamente crescenti.
3.  ENTRARE LONG quando il prezzo rompe al rialzo il massimo della barra che ha formato il terzo minimo crescente (HL3).

---

## Pattern: Doppio Minimo come Punto di Entrata per Rottura di Trading Range
**Libro/File Originale:** Estratti dal libro del corso (Pagina 217)
**Contesto/Pagina:** Pagina 217
**Descrizione:** Una formazione di doppio minimo può indicare un potenziale punto di entrata per una rottura al ribasso di una trading range. La presenza del doppio minimo rende evidente la trading range stessa.
**Logica Tecnica/Pseudocodice:**
1.  IDENTIFICARE una "Trading Range" (area di congestione).
2.  ALL'interno o vicino a questa trading range, IDENTIFICARE la formazione di un "Doppio Minimo" (due minimi consecutivi a livelli di prezzo simili).
3.  INTERPRETAZIONE: La formazione del doppio minimo evidenzia la trading range e un possibile punto di rottura.
4.  ENTRARE SHORT sulla rottura al ribasso sotto il livello del doppio minimo e della trading range.

---

## Regola: Rafforzamento del Segnale con Combinazione di Metodi
**Libro/File Originale:** Estratti dal libro del corso (Pagina 219)
**Contesto/Pagina:** Pagina 219
**Descrizione:** Un segnale di trading è significativamente più forte se le condizioni di due metodi diversi (es. calcolo semplice, massimi/minimi decrescenti/crescenti, Legge Dei Grafici - TLOC) si verificano simultaneamente o uno precede l'altro di poco.
**Logica Tecnica/Pseudocodice:**
1.  APPLICARE Metodo A (es. Calcolo Semplice).
2.  APPLICARE Metodo B (es. Massimi Decrescenti).
3.  APPLICARE Metodo C (es. TLOC).
4.  SE (Metodo A è vero) E (Metodo B è vero) simultaneamente, ALLORA la forza del segnale è CONSIDEREVOLMENTE MAGGIORE.
5.  SE (Metodo A è vero) E (Metodo C è vero, o C precede A di poco), ALLORA la forza del segnale è MOLTO FORTE, indicando un movimento significativo.

---

## Trading Tecnica: Calcolo dei Segmenti (per Uptrend)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 219, 222, 223)
**Contesto/Pagina:** Pagine 219, 222, 223
**Descrizione:** Una tecnica avanzata per individuare un movimento nascente. I segmenti sono definiti dagli spazi tra i minimi decrescenti delle barre di prezzo. Si collegano i minimi successivi, e se una barra scende sotto il minimo iniziale, il conteggio nella stessa direzione si interrompe. L'entrata avviene sulla rottura del massimo della barra il cui minimo ha completato il terzo segmento.
**Logica Tecnica/Pseudocodice:**
1.  **Definizione del Segmento:** Un segmento è lo spazio tra due minimi decrescenti consecutivi.
2.  **Conteggio dei Segmenti (per Uptrend):**
    *   IDENTIFICARE un primo minimo (Minimo Base).
    *   IDENTIFICARE un secondo minimo inferiore al Minimo Base (crea Segmento 1).
    *   IDENTIFICARE un terzo minimo inferiore al secondo (crea Segmento 2).
    *   IDENTIFICARE un quarto minimo inferiore al terzo (crea Segmento 3). Il quarto minimo può essere parte di un doppio minimo o un minimo di correzione.
    *   SE una barra successiva scende sotto il Minimo Base, il conteggio dei segmenti in questa direzione si annulla.
3.  **Segnale di Entrata:**
    *   IDENTIFICARE la "barra di acquisto" (la barra il cui minimo ha completato il terzo segmento).
    *   ENTRARE LONG sulla rottura verso l'alto del massimo di questa "barra di acquisto".
4.  **Rafforzamento del Segnale:** Il segnale è più forte se combinato con la rottura di una trading range intraday, la violazione di massimi precedenti, o il superamento di un doppio massimo (potenziale movimento esplosivo).

---

## Regola: Evitare Pattern Grafici Mal Formati
**Libro/File Originale:** Estratti dal libro del corso (Pagina 220)
**Contesto/Pagina:** Pagina 220
**Descrizione:** La tecnica di calcolo dei segmenti (e altre) funziona solo su grafici con schemi "ben formati". Non è possibile fare trading su schemi troppo piatti, troppo squadrati o troppo imprecisi.
**Logica Tecnica/Pseudocodice:**
1.  OSSERVARE la chiarezza e la definizione dei pattern grafici (es. formazioni di swing, congestioni, barre).
2.  SE i pattern sono "troppo piatti", "troppo squadrati" o "troppo imprecisi", ALLORA NON fare trading su quelle formazioni.
3.  RICERCARE pattern con contorni e movimenti di prezzo distinti e chiari.

---

## Scelta dell'Intervallo Temporale (Timeframe)
**Libro/File Originale:** Estratti dal libro del corso (Pagina 221, 222)
**Contesto/Pagina:** Pagine 221, 222
**Descrizione:** La scelta dell'intervallo temporale (es. 5, 30, 60-120 minuti) è cruciale e deve essere basata sulla capacità del grafico di mostrare schemi ben formati. Mercati molto liquidi possono permettere intervalli più brevi (es. 5 minuti), mentre mercati meno liquidi o periodi di trading lento richiedono intervalli più lunghi.
**Logica Tecnica/Pseudocodice:**
1.  VALUTARE il grafico nell'intervallo temporale corrente.
2.  SE il grafico NON mostra schemi ben formati (es. è troppo impreciso, piatto o squadrato), ALLORA:
    *   PASSARE a un intervallo temporale più lungo.
3.  SE il mercato è MOLTO LIQUIDO:
    *   È possibile utilizzare intervalli temporali più brevi (es. 5 minuti), a meno che il trading sia molto lento.
4.  SE il mercato è MENO LIQUIDO (indipendentemente dalla velocità):
    *   È necessario utilizzare intervalli temporali più lunghi (es. 30, 60-120 minuti).

---

## Exit Strategy: Metodo della Continuazione
**Libro/File Originale:** Estratti dal libro del corso (Pagina 224)
**Contesto/Pagina:** Pagina 224
**Descrizione:** Una strategia di uscita a più stadi per massimizzare i profitti nei trend. Inizialmente, si prendono profitti rapidamente per coprire i costi. Poi, si prendono ulteriori profitti quando si forma una seconda barra di inversione. Infine, i contratti rimanenti vengono mantenuti con uno stop a pareggio o in profitto, fino a quando il movimento non sembra terminato, i prezzi vanno contro, o la giornata di trading finisce.
**Logica Tecnica/Pseudocodice:**
1.  **Primo Stadio:** Appena c'è un guadagno accettabile, LIQUIDARE parte della posizione (es. 1 o 2 contratti su 3) per coprire i costi e realizzare un piccolo profitto.
2.  **Secondo Stadio:** QUANDO si forma una "Seconda Inversione" (Seconda Reversal Bar), LIQUIDARE un'altra parte della posizione.
3.  **Terzo Stadio (Continuazione):**
    *   MANTENERE i contratti rimanenti.
    *   SPOSTARE lo stop loss a pareggio o a un livello che garantisca un profitto.
    *   USCIRE COMPLETAMENTE se:
        *   Ci sono motivi per ritenere che il movimento sia finito.
        *   I prezzi si muovono significativamente contro la posizione.
        *   La giornata di trading sta per finire.

---

## Exit Strategy: Metodo della Violazione
**Libro/File Originale:** Estratti dal libro del corso (Pagina 224)
**Contesto/Pagina:** Pagina 224
**Descrizione:** Una strategia di uscita che prevede la chiusura dell'intera posizione al verificarsi di una "violazione". La violazione è definita specificamente come la formazione di due barre di inversione o la formazione di un massimo più alto in un trend al ribasso, o di un minimo più basso in un trend al rialzo.
**Logica Tecnica/Pseudocodice:**
1.  **Definizione di "Violazione":**
    *   **Per un trend al rialzo (LONG):**
        *   FORMAZIONE di due barre di inversione (chiusura inferiore all'apertura).
        *   FORMAZIONE di un minimo più basso.
    *   **Per un trend al ribasso (SHORT):**
        *   FORMAZIONE di due barre di inversione (chiusura superiore all'apertura).
        *   FORMAZIONE di un massimo più alto.
2.  SE si verifica una delle condizioni di "Violazione", ALLORA CHIUDERE l'intera posizione immediatamente.

---

### [PARTE 6: merged_clean_part_06_p201-240.pdf]

## Progressive Exit Strategy
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 1
**Descrizione:** Una strategia per uscire gradualmente da una posizione, chiudendo parte della posizione quando si osservano la prima e la seconda violazione del prezzo, e mantenendo aperta la parte finale fino a un segnale convincente per una chiusura completa. L'approccio per la parte finale è soggettivo.
**Logica Tecnica/Pseudocodice:**
```
IF (first_price_violation_occurs):
    CLOSE_PORTION(position, 1)
IF (second_price_violation_occurs):
    CLOSE_PORTION(position, 2)
WHILE (final_portion_of_position_is_open):
    IF (compelling_exit_reason_arises):
        CLOSE_PORTION(position, FINAL)
        BREAK_LOOP
```

---

## Market Congestion Definition
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 1
**Descrizione:** Una condizione di mercato in cui i prezzi si muovono lateralmente, caratterizzata da barre alternate che formano un doppio minimo in un punto specifico ("a"), seguito da una doji, una barra di inversione e altre due doji. Questa sequenza indica una fase di indecisione prima di un possibile movimento direzionale.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION IsMarketCongestedAtPointA(price_bars):
    IF (bars_are_alternating): // Example: small bodies, overlapping ranges
        IF (forms_double_bottom_pattern_at(price_bars, "point_A")):
            next_bar = GET_NEXT_BAR(price_bars, "point_A")
            IF (next_bar.is_doji):
                next_next_bar = GET_NEXT_BAR(next_bar)
                IF (next_next_bar.is_inversion_bar):
                    next_two_bars = GET_NEXT_TWO_BARS(next_next_bar)
                    IF (next_two_bars.all_are_dojis):
                        RETURN TRUE
    RETURN FALSE
```

---

## Doji Breakout Entry Signal
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 1
**Descrizione:** Un segnale di entrata potenziale che si verifica quando il prezzo rompe il massimo di una barra doji che ha aperto e chiuso al proprio massimo. Questo suggerisce un'immediata spinta rialzista dopo un periodo di equilibrio. Il testo, tuttavia, suggerisce di attendere l'uscita dalla congestione.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION GenerateDojiBreakoutEntrySignal(current_bar, doji_bar):
    IF (doji_bar.open_price == doji_bar.high_price AND doji_bar.close_price == doji_bar.high_price):
        IF (current_bar.high_price > doji_bar.high_price):
            SIGNAL_LONG_ENTRY = TRUE // Potenziale entrata long
    // Nota: Il testo implica che in un contesto di congestione, potrebbe essere preferibile attendere.
```

---

## Segment Tracking for Minima
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 1
**Descrizione:** Un metodo per tracciare il movimento del mercato seguendo i minimi delle barre. Un segmento viene esteso da barra a barra. La sua estremità viene spostata solo quando si forma un nuovo minimo inferiore al precedente.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION TrackSegmentsByMinima(price_bars_data):
    current_segment_lowest_low = price_bars_data[0].low_price
    segment_end_bar_index = 0

    FOR i FROM 1 TO price_bars_data.length - 1:
        IF (price_bars_data[i].low_price < current_segment_lowest_low):
            current_segment_lowest_low = price_bars_data[i].low_price
            segment_end_bar_index = i // Sposta l'estremo del segmento a questa nuova barra con un minimo più basso
        // Altrimenti, il segmento rimane ancorato al minimo precedente e si estende virtualmente orizzontalmente.
    RETURN (current_segment_lowest_low, segment_end_bar_index)
```

---

## Entry Signal (Last Doji Max Breakout)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 1
**Descrizione:** Un segnale di entrata valido per una posizione lunga, attivato dalla rottura al rialzo del massimo della barra doji più recente, specialmente dopo una fase di congestione o un pattern specifico.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION GenerateLastDojiMaxBreakoutEntry(current_price, last_doji_bar):
    last_doji_max_price = last_doji_bar.high_price
    IF (current_price > last_doji_max_price):
        SIGNAL_LONG_ENTRY = TRUE // Segnale di entrata valido per long
```

---

## Segment Trailing Minima Rule
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 2
**Descrizione:** Una regola specifica per il tracciamento dei segmenti sui grafici: un segmento segue i minimi e non viene modificato o spostato finché non si osserva una barra che forma un minimo inferiore rispetto alla barra precedente.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION SegmentFollowsMinima(segment_current_low, segment_anchor_bar, new_bar):
    IF (new_bar.low_price < segment_current_low):
        segment_current_low = new_bar.low_price
        segment_anchor_bar = new_bar // Aggiorna il punto di ancoraggio del segmento
    // Se il nuovo minimo non è inferiore, il segmento "segue" mantenendo il suo punto basso attuale.
```

---

## Entry Signal (Breakout of Last Bar's Maximum or Next Bar's Maximum)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 2
**Descrizione:** Un segnale di entrata valido si genera quando il prezzo supera il massimo della barra più recente o, in alternativa, il massimo della barra immediatamente successiva. Questo indica una potenziale continuazione rialzista.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION GenerateMaxBreakoutEntry(current_price, last_bar, next_bar_if_exists):
    last_bar_max = last_bar.high_price
    IF (current_price > last_bar_max):
        SIGNAL_LONG_ENTRY = TRUE // Rottura del massimo dell'ultima barra
    ELSE IF (next_bar_if_exists IS NOT NULL AND current_price > next_bar_if_exists.high_price):
        SIGNAL_LONG_ENTRY = TRUE // Rottura del massimo della barra successiva
```

---

## Descending Maxima Selling Strategy
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 3
**Descrizione:** Una strategia di vendita attivata quando i prezzi iniziano a scendere dopo che una barra a 30 minuti ha formato il massimo di giornata e ha coinciso con la chiusura del giorno precedente. Implica il conteggio e il collegamento di massimi decrescenti per identificare punti di vendita.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION InitiateDescendingMaximaSell(current_price, bar_30min_high_at_open, prev_day_close):
    IF (current_price < bar_30min_high_at_open.high_price AND current_price < prev_day_close):
        START_TRACKING_DESCENDING_MAXIMA = TRUE
        // Logica per identificare e collegare massimi decrescenti, ad esempio per tracciare una trendline ribassista.
        // Ogni nuovo massimo decrescente può essere un punto per una vendita parziale.
```

---

## Phased Exit Strategy (General)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 3
**Descrizione:** Una strategia di uscita flessibile che prevede la chiusura di una posizione in più fasi (prima, seconda e finale) in base all'andamento del mercato, con l'obiettivo di massimizzare i profitti su diverse parti della posizione.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION ExecutePhasedExit(market_conditions):
    IF (market_conditions.first_exit_trigger_met):
        PERFORM_EXIT("Prima uscita")
    IF (market_conditions.second_exit_trigger_met):
        PERFORM_EXIT("Seconda uscita")
    IF (market_conditions.final_exit_trigger_met):
        PERFORM_EXIT("Uscita finale")
```

---

## Mechanical Trading Entry (Specific High Breakout)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 4
**Descrizione:** Un'entrata in un trade basata esclusivamente sulla rottura di un massimo predefinito, adatta per sistemi di trading puramente meccanici senza l'intervento di decisioni discrezionali.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION MechanicalEntry(current_price, predefined_high_level):
    IF (TRADING_MODE == "MECHANICAL"):
        IF (current_price > predefined_high_level):
            EXECUTE_LONG_ENTRY()
```

---

## Phased Exit Strategy (Minima & Inversion Bars)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 4
**Descrizione:** Una strategia di uscita in tre fasi per una posizione long. La prima parte della posizione viene liquidata quando una barra forma un nuovo minimo inferiore. La seconda parte quando si osservano due barre di inversione. Il resto viene liquidato quando si forma un altro minimo inferiore (basato sul metodo di violazione precedente).
**Logica Tecnica/Pseudocodice:**
```
// Assumendo una posizione long aperta
FUNCTION PhasedExitMinimaInversion(current_bar, previous_bar, inversion_bar_count):
    IF (current_bar.low_price < previous_bar.low_price):
        LIQUIDATE_CONTRACTS(portion_1) // Prima parte su nuovo minimo inferiore

    IF (inversion_bar_count >= 2): // Contatore di barre di inversione
        LIQUIDATE_CONTRACTS(portion_2) // Seconda parte su due barre di inversione

    // Dopo la liquidazione della seconda parte
    IF (current_bar.low_price < previous_bar.low_price AND current_bar_is_after_second_portion_exit):
        LIQUIDATE_CONTRACTS(remaining_portion) // Resto su altro minimo inferiore (metodo violazione)
```

---

## Double High Specific Exit Example
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 4
**Descrizione:** Un esempio specifico di strategia di uscita dopo la formazione di un doppio massimo. Prevede la liquidazione progressiva della posizione in risposta a un nuovo minimo, una seconda barra di inversione e un minimo inferiore con gap.
**Logica Tecnica/Pseudocodice:**
```
// Assumendo che si sia formato un doppio massimo e una posizione long sia aperta
FUNCTION ExitOnDoubleHighPattern(bar_sequence):
    // 1. Prima barra successiva forma un nuovo minimo
    IF (bar_sequence[0].forms_new_minimum):
        LIQUIDATE_CONTRACTS(portion_1)

    // 2. La stessa barra è la seconda barra di inversione
    IF (bar_sequence[0].is_second_inversion_bar):
        EXIT_TRADE(portion_2)

    // 3. Barra successiva forma un minimo inferiore con un gap
    IF (bar_sequence[1].forms_lower_minimum_with_gap):
        EXIT_TRADE(remaining_contracts) // Basato sul metodo di violazione precedente
```

---

## Downward Segment Counting for Long Position Exit
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 5
**Descrizione:** Anche se si è in una posizione rialzista, si inizia a contare i segmenti verso il basso. L'osservazione di 3 segmenti discendenti fornisce un'ulteriore indicazione per chiudere eventuali contratti ancora aperti dalla posizione rialzista precedente.
**Logica Tecnica/Pseudocodice:**
```
// Assumendo una posizione long aperta
FUNCTION CountDownwardSegmentsAndExit(price_action_data):
    current_downward_segments = 0
    // Logic to identify a downward segment (e.g., lower highs and lower lows forming a distinct move down)
    IF (IDENTIFY_DOWNWARD_SEGMENT(price_action_data)):
        current_downward_segments += 1
        IF (current_downward_segments >= 3):
            EXIT_TRADE(all_remaining_long_contracts)
```

---

## Phased Exit with Specific Triggers (Uptrend)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 5
**Descrizione:** Una strategia di uscita scaglionata per un trade long, dove i punti di uscita sono attivati da specifici eventi di prezzo. Include una prima uscita su un nuovo massimo, una vendita generale ("Vendere"), una seconda uscita su una seconda barra di inversione e un'uscita finale negli ultimi 15 minuti del giorno di trading.
**Logica Tecnica/Pseudocodice:**
```
// Assumendo una posizione long aperta
FUNCTION ExecuteSpecificPhasedExit(current_market_data):
    IF (current_market_data.forms_new_higher_high):
        EXIT_TRADE(portion_1, "Prima uscita, massimo più alto")
    IF (current_market_data.meets_general_sell_conditions): // Condizione implicita per "Vendere"
        EXIT_TRADE(some_contracts, "Vendere")
    IF (current_market_data.forms_second_inversion_bar):
        EXIT_TRADE(portion_2, "Seconda uscita, seconda barra di inversione")
    IF (IS_LAST_15_MINUTES_OF_TRADING_DAY):
        EXIT_TRADE(remaining_contracts, "Uscita finale, ultimi 15 minuti")
```

---

## Entry on Third Segment Breakout
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 7
**Descrizione:** Una strategia di entrata rialzista basata sulla rottura del massimo della barra che ha formato il terzo segmento (probabilmente un segmento al rialzo).
**Logica Tecnica/Pseudocodice:**
```
FUNCTION EnterOnThirdSegmentBreakout(current_price, bar_of_third_segment_max):
    IF (current_price > bar_of_third_segment_max):
        EXECUTE_LONG_ENTRY() // "Entrata al rialzo"
```

---

## First Exit on New Minimum
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 7
**Descrizione:** La prima fase di un'uscita da una posizione lunga, attivata quando una barra forma un nuovo minimo, anche se l'uscita è vicina al livello di entrata.
**Logica Tecnica/Pseudocodice:**
```
// Assumendo una posizione long
FUNCTION FirstExitOnNewMinimum(current_bar, previous_bar):
    IF (current_bar.low_price < previous_bar.low_price):
        EXIT_TRADE(portion_1) // "Mia prima uscita è stata circa al livello dell'entrata... per effetto della barra che ha formato un nuovo minimo."
```

---

## Second Exit on Second Inversion Bar
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 7
**Descrizione:** La seconda fase di un'uscita da una posizione lunga, che si verifica all'apertura della seconda barra che segue un massimo relativo, a condizione che sia stata preceduta da una seconda barra di inversione.
**Logica Tecnica/Pseudocodice:**
```
// Assumendo una posizione long
FUNCTION SecondExitOnSecondInversionBar(current_bar, previous_bar, bar_before_previous, relative_high_bar):
    IF (previous_bar.is_second_inversion_bar AND bar_before_previous == relative_high_bar):
        EXIT_TRADE(portion_2, AT_OPEN_OF_CURRENT_BAR) // "Mia seconda uscita è stata all'apertura della seconda barra che ha seguito il massimo relativo, perché è stata preceduta dalla seconda barra di inversione."
```

---

## Final Exit (Doji or Third Inversion Bar)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 7
**Descrizione:** La fase finale di un'uscita da una posizione lunga. Si esce all'apertura di una barra doji, oppure se la barra precedente era una terza barra di inversione. In alternativa, si può uscire se la barra dopo la doji forma un minimo inferiore rispetto alla doji stessa.
**Logica Tecnica/Pseudocodice:**
```
// Assumendo una posizione long
FUNCTION FinalExitDojiThirdInversion(current_bar, previous_bar, bar_after_doji):
    IF (current_bar.is_doji):
        EXIT_TRADE(remaining_contracts, AT_OPEN_OF_CURRENT_BAR) // "Sono uscito all'apertura della barra doji"
    ELSE IF (previous_bar.is_third_inversion_bar):
        EXIT_TRADE(remaining_contracts, AT_OPEN_OF_CURRENT_BAR) // Condizione alternativa
    ELSE IF (current_bar.is_doji AND bar_after_doji.low_price < current_bar.low_price):
        EXIT_TRADE(remaining_contracts, AT_OPEN_OF_BAR_AFTER_DOJI) // "barra dopo la doji... ha formato un minimo inferiore"
```

---

## Daytrade to Position Trade Conversion Conditions
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 9, Capitolo 26
**Descrizione:** Definisce le condizioni sotto le quali un daytrade vincente può essere convertito in un position trade. La posizione deve essere profittevole e l'entrata deve essere avvenuta su un segnale principale o un segnale principale deve verificarsi mentre il daytrade è aperto. Vengono elencati segnali principali e intermedi.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION CheckDaytradeToPositionTradeConversion(trade_data, market_signals):
    IF (trade_data.is_profitable == TRUE):
        principal_signals = ["BREAKOUT_123_HIGH_LOW", "BREAKOUT_LEDGE", "BREAKOUT_TRADING_RANGE", "BREAKOUT_ROSS_HOOK"]
        intermediate_signals = ["BREAKOUT_LAST_3_DAY_LOW", "BREAKOUT_LAST_3_DAY_HIGH"]

        IF (trade_data.entry_signal_type IN principal_signals):
            RETURN TRUE // Entrata originale su segnale principale
        ELSE IF (ANY(signal IN principal_signals FOR signal IN market_signals.occurring_now)):
            RETURN TRUE // Segnale principale si verifica mentre in daytrade
        ELSE IF (ANY(signal IN intermediate_signals FOR signal IN market_signals.occurring_now)):
            RETURN TRUE // Segnale intermedio si verifica mentre in daytrade
    RETURN FALSE
```

---

## Position Trade Management
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 9
**Descrizione:** Linee guida per la gestione di un trade trasformato in position trade. Si mira a mantenere la posizione il più a lungo possibile, monitorando meno frequentemente durante il giorno rispetto a un daytrade. Richiede un posizionamento di stop a protezione dei profitti.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION ManagePositionTrade(trade_id, current_market_data):
    // Minimizzare entrate/uscite frequenti
    SET_MONITORING_FREQUENCY("ReducedIntraday")
    TRY_TO_HOLD_POSITION(trade_id)

    // Gestione overnight
    IF (IS_END_OF_DAY()):
        IF (GET_TRADE_PROFIT(trade_id) > 0):
            PLACE_STOP_LOSS(trade_id, "PROTECT_PROFITS") // Posiziona stop per proteggere i profitti
        ELSE:
            CLOSE_TRADE(trade_id) // Non tenere aperta se non in profitto
```

---

## Consolidated Trend Definition (Position Trade)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 10
**Descrizione:** Un trend viene definito "consolidato" se ha mostrato un movimento direzionale (rialzista o ribassista), seguito da una correzione, e poi ha rotto un Ross Hook. Questa configurazione è considerata robusta per i position trade.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION IsConsolidatedTrend(price_history):
    IF (price_history.shows_initial_directional_movement):
        IF (price_history.shows_a_correction_after_movement):
            IF (price_history.breaks_ross_hook_after_correction):
                RETURN TRUE
    RETURN FALSE
```

---

## Natural Support Point (Stop Placement)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 10
**Descrizione:** Per una posizione rialzista, un punto di supporto naturale è identificato come il punto in cui una correzione smette di muoversi verso il basso e i prezzi riprendono a salire. Questo punto è cruciale per il posizionamento degli stop.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION GetNaturalSupportPoint(price_history, position_direction):
    IF (position_direction == "LONG"):
        // Trova il punto più basso di una fase di correzione seguito da una ripresa al rialzo.
        // E.g., un minimo locale dopo una serie di minimi inferiori, seguito da minimi superiori.
        RETURN (LOWEST_POINT_OF_CORRECTION_BEFORE_UPWARD_REVERSAL)
    // Logica analoga per posizione SHORT, cercando punti di resistenza naturali.
```

---

## Correction Duration Rule
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 11
**Descrizione:** Una regola di gestione del rischio per i position trade: una correzione di prezzo non deve durare più di tre barre. Se la correzione supera le tre barre, la posizione deve essere chiusa.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION MonitorCorrectionDuration(current_position, correction_start_bar):
    MAX_CORRECTION_BARS = 3
    current_bars_in_correction = current_bar_index - correction_start_bar_index + 1

    IF (current_bars_in_correction > MAX_CORRECTION_BARS):
        CLOSE_POSITION(current_position)
        LOG_EVENT("Position closed due to correction exceeding 3 bars.")
```

---

## Traders Trick Entry
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 11
**Descrizione:** Un metodo di entrata per aprire una nuova posizione, che prevede l'acquisto prima della rottura di un Ross Hook, anticipando un movimento rialzista.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION ExecuteTradersTrickEntry(current_market_data):
    IF (ROSS_HOOK_IS_FORMING AND NOT_YET_BROKEN_OUT):
        BUY() // "Comprare qui, prima della rottura del Ross Hook"
```

---

## Position Trade Stop Placement (Natural Support)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 12
**Descrizione:** Una volta che un trade è stato trasformato in position trade, gli stop di protezione devono essere piazzati appena sotto i punti di supporto naturali (per posizioni long) o appena sopra i punti di resistenza naturali (per posizioni short).
**Logica Tecnica/Pseudocodice:**
```
FUNCTION SetPositionTradeStopLoss(trade_id, position_direction, current_market_data):
    IF (position_direction == "LONG"):
        natural_support = GET_NATURAL_SUPPORT_POINT(current_market_data, "LONG")
        PLACE_STOP_LOSS(trade_id, natural_support - SMALL_BUFFER_PIPS) // Appena sotto il supporto
    ELSE IF (position_direction == "SHORT"):
        natural_resistance = GET_NATURAL_RESISTANCE_POINT(current_market_data, "SHORT")
        PLACE_STOP_LOSS(trade_id, natural_resistance + SMALL_BUFFER_PIPS) // Appena sopra la resistenza
```

---

## Position Trade Monitoring Reduction
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 12
**Descrizione:** Se un position trade continua a evolversi favorevolmente oltre la prima correzione significativa sul grafico giornaliero, la necessità di monitoraggio intraday intensivo può essere ridotta.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION ReducePositionTradeMonitoring(trade_id, daily_chart_corrections):
    IF (daily_chart_corrections.count >= 1 AND daily_chart_corrections.first_correction_survived):
        SET_MONITORING_FREQUENCY("ReducedIntraday") // "smettiamo di monitorarlo intraday"
```

---

## Direct Quote Interpretation
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 15
**Descrizione:** Per le coppie di valute a quotazione diretta (es. EURUSD, GBPUSD), un aumento del prezzo sul grafico indica che la valuta base (es. EUR, GBP) sta diventando più costosa rispetto alla valuta quotata (USD). Una diminuzione del prezzo indica che sta diventando meno costosa.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION InterpretDirectQuote(currency_pair, chart_price_movement):
    IF (currency_pair IS_DIRECT_QUOTE): // Es: EURUSD, GBPUSD
        IF (chart_price_movement == "RISING"):
            BASE_CURRENCY_VALUE = "INCREASING"
        ELSE IF (chart_price_movement == "FALLING"):
            BASE_CURRENCY_VALUE = "DECREASING"
```

---

## Reversed Quote Interpretation
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 16
**Descrizione:** Per le coppie di valute a quotazione capovolta (es. USDCHF, USDJPY), un aumento del prezzo sul grafico indica che la valuta quotata (es. CHF, JPY) sta diminuendo di valore rispetto alla valuta base (USD). Una diminuzione del prezzo indica un aumento del suo valore.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION InterpretReversedQuote(currency_pair, chart_price_movement):
    IF (currency_pair IS_REVERSED_QUOTE): // Es: USDCHF, USDJPY
        IF (chart_price_movement == "RISING"):
            QUOTE_CURRENCY_VALUE = "DECREASING"
        ELSE IF (chart_price_movement == "FALLING"):
            QUOTE_CURRENCY_VALUE = "INCREASING"
```

---

## Direct/Reversed Quote Buy/Sell Rules
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 16
**Descrizione:** Le regole per eseguire ordini di acquisto e vendita in base al tipo di quotazione della coppia di valute. Per le quotazioni dirette si compra all'ASK e si vende al BID; per le quotazioni capovolte si compra al BID e si vende all'ASK.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION GetTradingPrices(currency_pair, current_bid, current_ask):
    IF (currency_pair IS_DIRECT_QUOTE):
        BUY_AT = current_ask
        SELL_AT = current_bid
    ELSE IF (currency_pair IS_REVERSED_QUOTE):
        BUY_AT = current_bid
        SELL_AT = current_ask
    RETURN (BUY_AT, SELL_AT)
```

---

## Limit and Stop Orders (General)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 16
**Descrizione:** Descrive l'uso generale degli ordini LIMIT e STOP per la gestione dei trade. SELL LIMIT è piazzato sopra il prezzo corrente per prendere profitto. SELL STOP è piazzato sotto il prezzo corrente per tagliare le perdite.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION PlaceOrder(order_type, price_level, current_price):
    IF (order_type == "SELL_LIMIT"):
        IF (price_level > current_price):
            SUBMIT_SELL_LIMIT_ORDER(price_level) // Ordine per vendere a un prezzo più alto
    ELSE IF (order_type == "SELL_STOP"):
        IF (price_level < current_price):
            SUBMIT_SELL_STOP_ORDER(price_level) // Ordine per vendere a un prezzo più basso (stop loss)
    // Analogamente per BUY_LIMIT (sotto prezzo corrente) e BUY_STOP (sopra prezzo corrente).
```

---

## Broker Selection Criteria (Logical Indicators)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 20
**Descrizione:** Un elenco di criteri fondamentali per la scelta di un broker Forex affidabile, focalizzati sulla qualità dei dati, la trasparenza, i servizi offerti, le performance della piattaforma e la struttura dei costi.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION EvaluateForexBroker(broker_data):
    QUALIFICATION_SCORE = 0
    IF (broker_data.provides_true_interbank_prices AND broker_data.multi_source_data): QUALIFICATION_SCORE += 10
    IF (broker_data.offers_true_bid_ask_spreads AND NOT broker_data.adjusts_prices_on_position_taken): QUALIFICATION_SCORE += 10
    IF (broker_data.adequate_trader_services): QUALIFICATION_SCORE += 5
    IF (NOT broker_data.has_account_fees): QUALIFICATION_SCORE += 5
    IF (NOT broker_data.applies_exchange_taxes): QUALIFICATION_SCORE += 5
    IF (broker_data.provides_info_and_support): QUALIFICATION_SCORE += 5
    IF (broker_data.offers_free_forex_charts): QUALIFICATION_SCORE += 3
    IF (broker_data.offers_free_live_data): QUALIFICATION_SCORE += 3
    IF (broker_data.fast_and_stable_live_quotes): QUALIFICATION_SCORE += 10
    IF (broker_data.fast_trading_platform): QUALIFICATION_SCORE += 10
    IF (broker_data.stable_trading_environment): QUALIFICATION_SCORE += 10
    IF (broker_data.unlimited_trading_capacity): QUALIFICATION_SCORE += 5
    IF (broker_data.high_liquidity): QUALIFICATION_SCORE += 5
    IF (broker_data.allows_seeing_position_value_during_trade): QUALIFICATION_SCORE += 5
    IF (broker_data.leverage >= "10:1_for_qualified_traders"): QUALIFICATION_SCORE += 5
    RETURN QUALIFICATION_SCORE
```

---

## Preferred Forex Trading Market Behaviors
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 22
**Descrizione:** I movimenti di prezzo più favorevoli per il metodo di trading descritto sono i "salti tra cluster" (rotture di cluster) e le "punte esplosive". I trend sono anche operabili ma richiedono stop più ampi. Le fasi di stagnazione sono difficili da gestire e vengono evitate.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION IsPreferredForexMarketBehavior(market_type):
    IF (market_type == "JUMPS_BETWEEN_CLUSTERS" OR market_type == "EXPLOSIVE_SPIKES"):
        RETURN TRUE // Preferito per il metodo
    ELSE IF (market_type == "TRENDS"):
        RETURN TRUE_WITH_CAUTION // Possibile, ma richiede SL più ampi
    ELSE IF (market_type == "STAGNATION"):
        RETURN FALSE // Da evitare
    RETURN FALSE
```

---

## Recommended Liquid Currency Pairs
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 22
**Descrizione:** Le coppie di valute più liquide e consigliate per il trading con questo metodo sono EUR/USD, USD/JPY, USD/CAD e EUR/JPY. EUR/USD è la più trattata e offre buone opportunità.
**Logica Tecnica/Pseudocodice:**
```
RECOMMENDED_FOREX_PAIRS = ["EUR/USD", "USD/JPY", "USD/CAD", "EUR/JPY"]

FUNCTION IsRecommendedForexPair(pair_symbol):
    RETURN pair_symbol IN RECOMMENDED_FOREX_PAIRS
```

---

## Forex Breakout Trading Method (General)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 23
**Descrizione:** Il metodo di trading principale per il Forex si basa sulla capitalizzazione delle "rotture" di "cluster" di prezzo, utilizzando indicatori tecnici semplici. È specificamente progettato per mercati non in trend e richiede una gestione accurata del rischio e dei profitti.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION ExecuteForexBreakoutTradingMethod(current_market_status, current_cluster):
    IF (NOT current_market_status.is_trending):
        IF (current_cluster.is_valid AND current_cluster.has_breakout):
            EXECUTE_TRADE_ACCORDING_TO_RULES()
            MANAGE_RISK_AND_PROFITS_ACCURATELY()
        ELSE:
            WAIT_FOR_CLUSTER_OR_BREAKOUT()
    ELSE:
        AVOID_TRADING_WITH_THIS_METHOD() // Non usare quando il mercato è in trend
```

---

## Rule 1: Determine Chart Price Type (Bid/Ask)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 23 (Regola 1)
**Descrizione:** È essenziale determinare se il software grafico visualizza i prezzi Bid (denaro) o Ask (lettera), poiché tutte le decisioni di trading e i calcoli dipendono da questa impostazione. Il libro usa gli esempi con i prezzi Ask.
**Logica Tecnica/Pseudocodice:**
```
GLOBAL CHART_PRICE_TYPE = "ASK" // Come usato negli esempi del libro

FUNCTION SetChartPriceType(user_input_type):
    IF (user_input_type == "BID" OR user_input_type == "ASK"):
        CHART_PRICE_TYPE = user_input_type
    ELSE:
        ERROR("Invalid chart price type. Must be BID or ASK.")
// Tutte le funzioni di calcolo successive devono fare riferimento a CHART_PRICE_TYPE.
```

---

## Rule 2: 1-Hour Bar and Software Specs
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 23 (Regola 2)
**Descrizione:** Le barre di prezzo utilizzate in questo metodo devono essere a intervalli di 1 ora. Il software grafico deve mostrare il massimo, il minimo e la chiusura di ogni barra e deve essere in grado di calcolare una media mobile semplice a 5 barre.
**Logica Tecnica/Pseudocodice:**
```
REQUIRED_BAR_INTERVAL = "1 HOUR"
REQUIRED_BAR_DATA_FIELDS = ["OPEN", "HIGH", "LOW", "CLOSE"]
REQUIRED_INDICATORS = ["SIMPLE_MOVING_AVERAGE_5_BARS"]

FUNCTION CheckSoftwareRequirements(software_capabilities):
    IF (software_capabilities.bar_interval != REQUIRED_BAR_INTERVAL):
        ERROR("Chart interval must be 1 hour.")
    IF (NOT software_capabilities.provides_ohlc_data):
        ERROR("Chart must show Open, High, Low, Close data.")
    IF (NOT software_capabilities.can_calculate_indicator("SMA", 5)):
        ERROR("Software must calculate 5-bar Simple Moving Average.")
```

---

## Rule 3: Cluster Definition (10+ Bars)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 23 (Regola 3)
**Descrizione:** Un "cluster" è definito come un raggruppamento di 10 o più barre di prezzo a 1 ora. I cluster rappresentano periodi di consolidamento dei prezzi.
**Logica Tecnica/Pseudocodice:**
```
MINIMUM_CLUSTER_BARS = 10 // Numero minimo di barre a 1 ora per definire un cluster

FUNCTION IsACluster(list_of_1hr_bars):
    IF (list_of_1hr_bars.length >= MINIMUM_CLUSTER_BARS):
        // Ulteriori criteri delle regole A-E (Pagina 26) per la validazione del cluster.
        RETURN TRUE
    RETURN FALSE
```

---

## Rule 5: Entry Only on 10+ Bar Cluster Breakout
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 23 (Regola 5)
**Descrizione:** La regola d'oro per l'entrata: si entra in un trade solo sulla rottura di cluster composti da 10 o più barre. Questo evita il trading impulsivo e limita l'esposizione al rischio, concentrandosi solo su rotture significative.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION CanEnterTrade(current_cluster):
    IF (current_cluster.length >= 10):
        IF (current_cluster.has_valid_breakout):
            RETURN TRUE // Entra solo su rottura di cluster di 10 o più barre
    RETURN FALSE // Non entrare, non è per trader compulsivi
```

---

## Rule 6: Buy 5-Pip Breakout of 10+ Bar Cluster
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 24 (Regola 6)
**Descrizione:** Per un'entrata long, si piazza un ordine "Buy Stop" 5 pip sopra il prezzo più alto del cluster, assumendo che il cluster sia composto da 10 o più barre. Questo include un aggiustamento per lo spread Bid/Ask se il grafico mostra prezzi Ask.
**Logica Tecnica/Pseudocodice:**
```
BUY_BREAKOUT_PIPS = 5 // Pips di rottura per il metodo

FUNCTION CalculateBuyEntryPrice(cluster_max_price, chart_price_type, broker_spread_pips):
    // Calcolo basato sull'esempio di Pagina 36:
    // cluster_max_price (assunto come ASK se chart_price_type è ASK) = 1.2412
    // Aggiustamento per software grafico (se chart è ASK e si compra al BID, ma l'esempio lo mette come ADD per comprare al ASK) = +0.0004
    // 5 pips del metodo = +0.0005
    software_graphic_adjustment = 0.0004 // Come da esempio pag 36
    method_pips_value = BUY_BREAKOUT_PIPS / 10000 // Converti pips in valore (per EUR/USD)

    RETURN cluster_max_price + software_graphic_adjustment + method_pips_value
    // Esempio: 1.2412 + 0.0004 + 0.0005 = 1.2421
```

---

## Rule 7: Sell 5-Pip Breakout of 10+ Bar Cluster
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 24 (Regola 7)
**Descrizione:** Per un'entrata short, si piazza un ordine "Sell Stop" 5 pip sotto il prezzo più basso del cluster, assumendo che il cluster sia composto da 10 o più barre. Questo include un aggiustamento per lo spread Bid/Ask se il grafico mostra prezzi Bid.
**Logica Tecnica/Pseudocodice:**
```
SELL_BREAKOUT_PIPS = 5 // Pips di rottura per il metodo

FUNCTION CalculateSellEntryPrice(cluster_min_price, chart_price_type, broker_spread_pips):
    // Calcolo basato sull'esempio di Pagina 38:
    // cluster_min_price (assunto come BID effettivo o già aggiustato) = 1.2394
    // 5 pips del metodo = -0.0005
    method_pips_value = SELL_BREAKOUT_PIPS / 10000 // Converti pips in valore (per EUR/USD)

    // Nota: Il testo a Pagina 37 menziona la sottrazione dello spread per determinare il prezzo di vendita se il grafico è Ask.
    // Tuttavia, l'esempio di Pagina 38 non mostra una sottrazione esplicita dello spread, suggerendo che `cluster_min_price` sia già un prezzo Bid effettivo o che lo spread sia 0.
    RETURN cluster_min_price - method_pips_value
    // Esempio: 1.2394 - 0.0005 = 1.2389
```

---

## Rule 8: Trade with Two or More Contracts
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 24 (Regola 8)
**Descrizione:** Regola di dimensionamento della posizione: operare sempre con due o più contratti. Una linea guida suggerisce 2 contratti per ogni $10.000 nel conto, per facilitare la gestione progressiva del profitto e del rischio.
**Logica Tecnica/Pseudocodice:**
```
MINIMUM_CONTRACTS = 2
ACCOUNT_BALANCE_THRESHOLD = 10000 // USD
CONTRACTS_PER_THRESHOLD = 2

FUNCTION DetermineNumberOfContracts(account_balance):
    recommended_contracts = FLOOR(account_balance / ACCOUNT_BALANCE_THRESHOLD) * CONTRACTS_PER_THRESHOLD
    RETURN MAX(MINIMUM_CONTRACTS, recommended_contracts)
```

---

## Rule 9: Initial Stop Loss Placement
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 24 (Regola 9)
**Descrizione:** Definire lo stop loss iniziale per entrambi i contratti a 1 pip oltre il massimo/minimo della barra a 1 ora precedente, nella direzione opposta al trade.
**Logica Tecnica/Pseudocodice:**
```
SL_PIPS_BEYOND_BAR = 1 // 1 pip oltre la barra precedente
PIP_VALUE = 0.0001 // Per EUR/USD

FUNCTION CalculateInitialStopLoss(trade_direction, previous_1hr_bar_high, previous_1hr_bar_low):
    IF (trade_direction == "LONG"):
        // Uscita è un SELL_STOP (esegue al BID)
        // Esempio Pagina 40: previous_bar_low - 0.0001 = 1.2484 (Sell Stop)
        RETURN previous_1hr_bar_low - PIP_VALUE
    ELSE IF (trade_direction == "SHORT"):
        // Uscita è un BUY_STOP (esegue all'ASK)
        // Esempio Pagina 40: previous_bar_high + 0.0004 (software adj) + 0.0001 (method pip) = 1.2530
        SOFTWARE_ADJUSTMENT = 0.0004 // Come da esempio Pagina 40 per BUY_STOP
        RETURN previous_1hr_bar_high + SOFTWARE_ADJUSTMENT + PIP_VALUE
```

---

## Rule 10: Stop Loss Adjustment (After 1st New Bar)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 24 (Regola 10)
**Descrizione:** Dopo la barra di entrata, all'inizio della prima nuova barra di prezzo, spostare lo stop loss per entrambi i contratti a 1 pip oltre il massimo/minimo della barra precedente (la barra di entrata stessa), nella direzione opposta al trade.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION AdjustStopLossAfterFirstNewBar(trade_direction, entry_bar, new_bar):
    IF (new_bar IS first_bar_after_entry_bar):
        previous_bar_for_sl = entry_bar
        new_sl_price = CalculateInitialStopLoss(trade_direction, previous_bar_for_sl.high_price, previous_bar_for_sl.low_price)
        MOVE_STOP_LOSS(new_sl_price, FOR_BOTH_CONTRACTS)
```

---

## Rule 11: Stop Loss Adjustment (After 2nd New Bar)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 24 (Regola 11)
**Descrizione:** All'inizio della seconda nuova barra di prezzo dopo la barra di entrata, spostare lo stop loss per entrambi i contratti a 1 pip oltre il massimo/minimo della barra precedente (la prima nuova barra), nella direzione opposta al trade.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION AdjustStopLossAfterSecondNewBar(trade_direction, first_new_bar, second_new_bar):
    IF (second_new_bar IS second_bar_after_entry_bar):
        previous_bar_for_sl = first_new_bar
        new_sl_price = CalculateInitialStopLoss(trade_direction, previous_bar_for_sl.high_price, previous_bar_for_sl.low_price)
        MOVE_STOP_LOSS(new_sl_price, FOR_BOTH_CONTRACTS)
```

---

## Rule 12: Exit Condition (No Higher High/Lower Low - If Target Not Reached)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 24 (Regola 12)
**Descrizione:** Se l'obiettivo di profitto iniziale non è stato raggiunto, uscire dal trade con entrambi i contratti alla chiusura della barra (dopo la barra di entrata) che non forma un massimo più alto (per long) o un minimo più basso (per short).
**Logica Tecnica/Pseudocodice:**
```
FUNCTION ExitOnNoProgress(trade_direction, current_bar, previous_bar, initial_target_reached):
    IF (NOT initial_target_reached):
        IF (trade_direction == "LONG"):
            IF (current_bar.high_price <= previous_bar.high_price AND current_bar_is_after_entry_bar):
                EXIT_TRADE(FOR_BOTH_CONTRACTS, AT_CLOSE_OF_CURRENT_BAR)
        ELSE IF (trade_direction == "SHORT"):
            IF (current_bar.low_price >= previous_bar.low_price AND current_bar_is_after_entry_bar):
                EXIT_TRADE(FOR_BOTH_CONTRACTS, AT_CLOSE_OF_CURRENT_BAR)
```

---

## Rule 13: 3-Bar Time Stop (If Target Not Reached)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 24 (Regola 13)
**Descrizione:** Se l'obiettivo di profitto iniziale non è stato raggiunto, utilizzare uno stop di tempo di 3 barre (compresa la barra di entrata). Uscire con entrambi i contratti alla chiusura della terza barra.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION UseThreeBarTimeStop(trade_start_bar_index, current_bar_index, initial_target_reached):
    IF (NOT initial_target_reached):
        IF (current_bar_index - trade_start_bar_index + 1 == 3): // Se la barra corrente è la terza dalla partenza
            EXIT_TRADE(FOR_BOTH_CONTRACTS, AT_CLOSE_OF_CURRENT_BAR)
```

---

## Rule 14: Re-entry After Loss/Trade Cooldown
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 24 (Regola 14)
**Descrizione:** Dopo aver subito una perdita in una direzione, attendere la formazione di 3 barre (compresa la barra di uscita) prima di rientrare nella stessa direzione. Attendere la formazione di 3 barre anche prima di entrare nella direzione opposta, dopo qualsiasi trade.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION IsReEntryAllowed(last_trade_exit_bar_index, current_bar_index, last_trade_direction, desired_entry_direction):
    BARS_SINCE_EXIT = current_bar_index - last_trade_exit_bar_index + 1 // Include barra di uscita

    IF (BARS_SINCE_EXIT < 3):
        RETURN FALSE // Periodo di cooldown attivo

    // Se > 3 barre, re-entrata è permessa
    RETURN TRUE
```

---

## Rule 15: Event-Based Exit (Market Fundamentals)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 24 (Regola 15)
**Descrizione:** Chiudere tutti i trade prima della chiusura del mercato del venerdì (ore 17:00 EST USA / 23:00 Italia) e prima di festività importanti come Natale, per evitare rischi legati a eventi fondamentali.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION CheckEventBasedExit(current_datetime):
    IF (current_datetime.day_of_week == FRIDAY AND current_datetime.time >= "17:00 EST"):
        CLOSE_ALL_TRADES()
    IF (current_datetime.is_pre_major_holiday): // Esempio: Natale
        CLOSE_ALL_TRADES()
```

---

## Rule 16: Initial Profit Target (1st Contract)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 24 (Regola 16)
**Descrizione:** Definire un obiettivo di profitto iniziale di 30 pip per un contratto. Questo serve come primo punto di profitto parziale.
**Logica Tecnica/Pseudocodice:**
```
INITIAL_PROFIT_TARGET_PIPS = 30
PIP_VALUE = 0.0001 // Per EUR/USD

FUNCTION SetInitialProfitTarget(trade_direction, entry_price):
    IF (trade_direction == "LONG"):
        TARGET_PRICE = entry_price + (INITIAL_PROFIT_TARGET_PIPS * PIP_VALUE)
    ELSE IF (trade_direction == "SHORT"):
        TARGET_PRICE = entry_price - (INITIAL_PROFIT_TARGET_PIPS * PIP_VALUE)
    PLACE_LIMIT_ORDER(CONTRACT_1, TARGET_PRICE)
    RETURN TARGET_PRICE
```

---

## Rule 17: Move SL to Breakeven (2nd Contract)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 24 (Regola 17)
**Descrizione:** Quando il primo obiettivo di profitto (per il primo contratto) viene raggiunto, spostare lo stop loss del secondo contratto al prezzo di pareggio (prezzo di entrata).
**Logica Tecnica/Pseudocodice:**
```
FUNCTION MoveSLToBreakeven(contract_1_status, contract_2_sl_order, entry_price):
    IF (contract_1_status.profit_target_reached == TRUE):
        MODIFY_STOP_LOSS(contract_2_sl_order, entry_price) // Sposta SL a pareggio per il 2° contratto
```

---

## Rule 18: Trailing Stop (2nd Contract)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 24 (Regola 18)
**Descrizione:** Per il secondo contratto, ogni volta che si realizzano ulteriori 30 pip di profitto, spostare lo stop loss di 30 pip nella direzione del trade.
**Logica Tecnica/Pseudocodice:**
```
TRAILING_STEP_PIPS = 30
PIP_VALUE = 0.0001

FUNCTION ApplyTrailingStop(contract_2_sl_order, trade_direction, current_profit_pips):
    // Assumendo che il SL sia già a pareggio dopo il 1° target
    last_sl_move_profit_level = GET_LAST_SL_MOVE_PROFIT_LEVEL(contract_2_sl_order)

    IF (current_profit_pips >= last_sl_move_profit_level + TRAILING_STEP_PIPS):
        // Calcola il nuovo livello di profitto per lo spostamento dello SL
        new_sl_move_profit_level = FLOOR(current_profit_pips / TRAILING_STEP_PIPS) * TRAILING_STEP_PIPS

        IF (trade_direction == "LONG"):
            new_sl_price = ENTRY_PRICE + (new_sl_move_profit_level * PIP_VALUE) // Questo potrebbe essere il prezzo di ingresso + profitti acquisiti
        ELSE IF (trade_direction == "SHORT"):
            new_sl_price = ENTRY_PRICE - (new_sl_move_profit_level * PIP_VALUE)

        MODIFY_STOP_LOSS(contract_2_sl_order, new_sl_price)
        SET_LAST_SL_MOVE_PROFIT_LEVEL(contract_2_sl_order, new_sl_move_profit_level)
```

---

## Rule 19: 3-Bar Time Stop (2nd Contract, After Last 30 Pips)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 24 (Regola 19)
**Descrizione:** Se il secondo contratto non genera altri 30 pip di profitto dopo l'ultimo spostamento del trailing stop, chiudere il trade alla chiusura della terza barra (includendo la barra che ha formato gli ultimi 30 pip).
**Logica Tecnica/Pseudocodice:**
```
FUNCTION ApplySecondContractTimeStop(contract_2_status, bar_index_of_last_30_pip_profit, current_bar_index):
    IF (NOT contract_2_status.made_another_30_pips_profit):
        BARS_SINCE_LAST_30_PIP_PROFIT = current_bar_index - bar_index_of_last_30_pip_profit + 1
        IF (BARS_SINCE_LAST_30_PIP_PROFIT == 3):
            EXIT_TRADE(CONTRACT_2, AT_CLOSE_OF_CURRENT_BAR)
```

---

## Cluster Extremes Definition (Detailed)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 26
**Descrizione:** Gli estremi (superiore e inferiore) di un cluster sono definiti dal prezzo massimo della barra più alta e dal prezzo minimo della barra più bassa all'interno del cluster stesso. Questo delimita la fascia di prezzo del consolidamento.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION DefineClusterExtremes(cluster_bars):
    cluster_upper_limit = 0.0
    cluster_lower_limit = Infinity

    FOR each_bar IN cluster_bars:
        cluster_upper_limit = MAX(cluster_upper_limit, each_bar.high_price)
        cluster_lower_limit = MIN(cluster_lower_limit, each_bar.low_price)

    RETURN (cluster_upper_limit, cluster_lower_limit)
```

---

## Cluster Definition Rule A: 5 Days of 1-Hour Bars
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 26 (Regola A)
**Descrizione:** Per una migliore visualizzazione e identificazione dei cluster di prezzo, è consigliabile utilizzare un grafico con almeno 5 giorni di dati a barre di 1 ora. Meno dati potrebbero rendere i cluster meno evidenti.
**Logica Tecnica/Pseudocodice:**
```
MINIMUM_DISPLAY_PERIOD = 5 * 24 // 5 giorni * 24 ore/giorno = 120 barre
FUNCTION IsClusterDataSufficient(chart_data):
    IF (chart_data.number_of_1hr_bars >= MINIMUM_DISPLAY_PERIOD):
        RETURN TRUE
    RETURN FALSE
```

---

## Cluster Definition Rule B: Last Trend Bar as First Cluster Bar
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 26 (Regola B)
**Descrizione:** Quando i prezzi interrompono un trend, l'ultima barra del trend precedente (quella con il massimo più alto in un trend rialzista o il minimo più basso in un trend ribassista) diventa la prima barra del nuovo cluster.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION IdentifyFirstClusterBar(previous_trend_bars):
    IF (previous_trend_bars.was_uptrend):
        RETURN GET_BAR_WITH_HIGHEST_HIGH(previous_trend_bars)
    ELSE IF (previous_trend_bars.was_downtrend):
        RETURN GET_BAR_WITH_LOWEST_LOW(previous_trend_bars)
    RETURN NULL
```

---

## Cluster Definition Rule C: Assume Cluster if Not Trending
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 26 (Regola C)
**Descrizione:** Se il grafico non mostra un chiaro trend (cioè, non forma massimi o minimi consecutivi entro 3 barre), si presume che il mercato sia in un cluster.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION IsPriceTrending(recent_bars):
    // Verifica se ci sono massimi più alti/bassi consecutivi entro 3 barre
    IF (recent_bars.length < 3): RETURN FALSE
    has_higher_highs = TRUE
    has_lower_lows = TRUE
    FOR i FROM 1 TO recent_bars.length - 1:
        IF (recent_bars[i].high_price <= recent_bars[i-1].high_price): has_higher_highs = FALSE
        IF (recent_bars[i].low_price >= recent_bars[i-1].low_price): has_lower_lows = FALSE
    IF (has_higher_highs OR has_lower_lows): RETURN TRUE
    RETURN FALSE

FUNCTION AssumeClusterIfNoTrend(recent_bars):
    IF (NOT IsPriceTrending(recent_bars)):
        RETURN TRUE // Assumi che sia in un cluster
    RETURN FALSE
```

---

## Cluster Definition Rule D: Opposite Trend within Cluster
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 26 (Regola D)
**Descrizione:** Anche se i prezzi smettono di fare un trend in una direzione e iniziano un trend nella direzione opposta, si assume che questa azione stia avvenendo all'interno di un cluster, purché si possa osservare un minimo di 10 barre.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION CheckOppositeTrendInCluster(price_history_segment):
    IF (price_history_segment.shows_trend_reversal_within_segment):
        IF (price_history_segment.length >= 10): // Cluster deve avere almeno 10 barre
            RETURN TRUE // Assumi che sia un cluster
    RETURN FALSE
```

---

## Cluster Definition Rule E: 5-Bar SMA Peak/Extreme
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 26 (Regola E)
**Descrizione:** L'ultimo criterio per identificare un cluster è l'osservazione di un picco o un estremo visibile nella media mobile semplice a 5 barre. Dopo un potenziale cluster rialzista, si aspetta che l'SMA formi un picco e scenda. Dopo un potenziale cluster ribassista, si aspetta che l'SMA formi un estremo (trough) e risalga.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION CheckSMAForCluster(sma5_data, potential_cluster_direction):
    IF (potential_cluster_direction == "AFTER_UPTREND"):
        IF (SMA_HAS_VISIBLE_PEAK(sma5_data) AND SMA_IS_DECREASING(sma5_data)):
            RETURN TRUE // Conferma cluster
    ELSE IF (potential_cluster_direction == "AFTER_DOWNTREND"):
        IF (SMA_HAS_VISIBLE_TROUGH(sma5_data) AND SMA_IS_INCREASING(sma5_data)):
            RETURN TRUE // Conferma cluster
    RETURN FALSE
```

---

## Incomplete Cluster Exclusion
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 29
**Descrizione:** Un raggruppamento di barre non viene qualificato come cluster valido se ha meno di 10 barre prima che si verifichi una rottura. Un cluster deve avere almeno 10 barre per essere considerato completo e valido per il trading.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION IsValidCluster(cluster_bars_list):
    IF (cluster_bars_list.length < 10):
        RETURN FALSE // Cluster incompleto
    // Altre regole di definizione del cluster
    RETURN TRUE
```

---

## Initial Long Bar Handling in Cluster
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 29
**Descrizione:** Quando una barra oraria molto lunga è la prima di un potenziale nuovo cluster, essa viene contata ai fini del numero minimo di 10 barre del cluster, ma i suoi estremi (massimo o minimo) non vengono utilizzati per definire i limiti effettivi (superiore o inferiore) del cluster. Questo per evitare che una singola barra outlier alteri eccessivamente l'ampiezza del cluster.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION AddBarToClusterAndDefineLimits(cluster_bars, new_bar):
    IF (new_bar IS first_bar_of_new_cluster AND new_bar IS_CONSIDERED_A_LONG_BAR_OUTLIER):
        cluster_bars.ADD(new_bar) // Conta la barra
        // Non usare il suo massimo/minimo per definire cluster_upper_limit o cluster_lower_limit.
        // I limiti saranno definiti dalle altre barre.
    ELSE:
        cluster_bars.ADD(new_bar)
        // Usa il suo massimo/minimo per definire cluster_upper_limit o cluster_lower_limit.
```

---

## Long Bar Rule (Uptrend Breakout, Figure 3)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 30 (Figura 3)
**Descrizione:** Se una barra lunga si verifica all'inizio di un cluster dopo una rottura al rialzo, essa viene conteggiata come parte del cluster, ma il suo minimo non deve essere utilizzato per definire l'estremo inferiore del cluster.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION HandleLongBarInUptrendCluster(bar, cluster_definition):
    IF (bar.is_long_bar AND bar.is_first_bar_after_uptrend_breakout_into_cluster):
        ADD_BAR_TO_CLUSTER_COUNT(bar)
        EXCLUDE_BAR_LOW_FROM_CLUSTER_LOWER_LIMIT_CALCULATION(bar)
```

---

## Long Bar Rule (Downtrend Breakout, Figure 4)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 30 (Figura 4)
**Descrizione:** Se una barra lunga apre un nuovo cluster dopo una rottura al ribasso, il suo minimo viene utilizzato per definire l'estremo inferiore del cluster (se è il minimo assoluto), ma il suo massimo non viene utilizzato per definirne l'estremo superiore.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION HandleLongBarInDowntrendCluster(bar, cluster_definition):
    IF (bar.is_long_bar AND bar.is_first_bar_after_downtrend_breakout_into_cluster):
        ADD_BAR_TO_CLUSTER_COUNT(bar)
        INCLUDE_BAR_LOW_FOR_CLUSTER_LOWER_LIMIT_CALCULATION(bar) // Se è il punto più basso
        EXCLUDE_BAR_HIGH_FROM_CLUSTER_UPPER_LIMIT_CALCULATION(bar)
```

---

## False Breakout Cluster Limit Adjustment
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 32
**Descrizione:** Se si verifica una "piccola falsa rottura" (da 1 a 4 pip), dove la barra a 1 ora chiude senza superare tale livello, il limite del cluster viene aggiornato per riflettere questa estensione. I prezzi di entrata/uscita devono essere calcolati in base a questo nuovo limite modificato (5 pip oltre il nuovo limite).
**Logica Tecnica/Pseudocodice:**
```
FALSE_BREAKOUT_MAX_PIPS = 4
ENTRY_PIPS_BEYOND_LIMIT = 5

FUNCTION AdjustClusterLimitsOnFalseBreakout(cluster_limits, breakout_level, breakout_magnitude, bar_close_within_limits):
    IF (breakout_magnitude >= 1_PIP AND breakout_magnitude <= FALSE_BREAKOUT_MAX_PIPS AND bar_close_within_limits):
        new_cluster_limit = breakout_level // Il punto della falsa rottura estende il limite
        // Aggiorna i limiti del cluster
        cluster_limits.upper = MAX(cluster_limits.upper, new_cluster_limit)
        cluster_limits.lower = MIN(cluster_limits.lower, new_cluster_limit)
        // Le future entrate useranno questo nuovo limite: new_cluster_limit +/- ENTRY_PIPS_BEYOND_LIMIT
    RETURN cluster_limits
```

---

## Cluster Modification on Trade Entry
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 32
**Descrizione:** Quando si entra in un trade su una rottura di un cluster (acquisto o vendita), la definizione del cluster viene modificata nella direzione del trade. Tuttavia, nella direzione opposta, il cluster non viene modificato e rimane valido per un potenziale trade futuro fino a quando non se ne forma uno nuovo.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION ModifyClusterOnTradeEntry(cluster_definition, trade_direction, entry_price):
    IF (trade_direction == "LONG"):
        cluster_definition.upper_limit = MAX(cluster_definition.upper_limit, entry_price) // O il massimo del breakout bar
        // cluster_definition.lower_limit rimane invariato per potenziali short
    ELSE IF (trade_direction == "SHORT"):
        cluster_definition.lower_limit = MIN(cluster_definition.lower_limit, entry_price) // O il minimo del breakout bar
        // cluster_definition.upper_limit rimane invariato per potenziali long
```

---

## Significant False Breakout Cluster Expansion
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 33 (Figura 7)
**Descrizione:** Se si verifica una falsa rottura "notevole" (maggiore di 4 pip) dopo la formazione di un cluster, i limiti del cluster devono essere estesi per includere il massimo o il minimo di tale falsa rottura. Si applica la Regola 14 (cooldown per il re-entry).
**Logica Tecnica/Pseudocodice:**
```
FUNCTION ExpandClusterOnSignificantFalseBreakout(cluster_limits, false_breakout_max, false_breakout_min, breakout_direction):
    BREAKOUT_THRESHOLD_PIPS = 4 // Maggiore di 4 pip

    // Identifica se la rottura è stata significativa (es. > 4 pips)
    IF (breakout_direction == "UPWARDS" AND false_breakout_max - cluster_limits.upper > BREAKOUT_THRESHOLD_PIPS):
        cluster_limits.upper = false_breakout_max // Estendi il limite superiore
    ELSE IF (breakout_direction == "DOWNWARDS" AND cluster_limits.lower - false_breakout_min > BREAKOUT_THRESHOLD_PIPS):
        cluster_limits.lower = false_breakout_min // Estendi il limite inferiore

    APPLY_RULE_14_COOLDOWN() // Regola 14: Attendi 3 barre prima di re-entrare
    RETURN cluster_limits
```

---

## Mini Cluster (Cluster Contraction)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 33
**Descrizione:** Un "mini cluster" si forma quando un cluster si restringe o quando un cluster si forma all'interno di un altro. Se si formano 10 barre in questa formazione più stretta, è possibile fare trading su di essa.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION IdentifyAndTradeMiniCluster(current_market_data, parent_cluster_limits):
    // Identifica un periodo di prezzo che si restringe all'interno di un cluster più ampio
    IF (current_market_data.is_narrowing_range_bound AND current_market_data.is_within(parent_cluster_limits)):
        mini_cluster_bars = GET_BARS_IN_NARROWED_RANGE()
        IF (mini_cluster_bars.length >= 10):
            // Considera questo come un mini cluster valido
            TRADE_ON_MINI_CLUSTER_BREAKOUT(mini_cluster_bars) // Utilizza i suoi limiti specifici per le rotture
```

---

## Forex Entry Order Placement Strategy
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 35
**Descrizione:** La strategia per piazzare ordini di entrata nel Forex prevede l'inserimento simultaneo di un ordine Buy Stop e un ordine Sell Stop (per due contratti ciascuno) sulla piattaforma, in attesa della rottura del cluster. Una volta eseguito uno dei due, l'altro ordine deve essere immediatamente cancellato.
**Logica Tecnica/Pseudocodice:**
```
FUNCTION PlaceForexEntryOrders(cluster_data):
    IF (cluster_data.is_valid_10_plus_bar_cluster):
        buy_entry_price = CalculateBuyEntryPrice(cluster_data.max_price, CHART_PRICE_TYPE, BROKER_SPREAD_PIPS)
        sell_entry_price = CalculateSellEntryPrice(cluster_data.min_price, CHART_PRICE_TYPE, BROKER_SPREAD_PIPS)

        buy_order_id = PLACE_BUY_STOP_ORDER(buy_entry_price, NUM_CONTRACTS)
        sell_order_id = PLACE_SELL_STOP_ORDER(sell_entry_price, NUM_CONTRACTS)

        // Monitoraggio per l'esecuzione
        WHEN (ORDER_EXECUTED(buy_order_id)):
            CANCEL_ORDER(sell_order_id)
        WHEN (ORDER_EXECUTED(sell_order_id)):
            CANCEL_ORDER(buy_order_id)
```

---

## Buy Order Calculation Example (Chart Ask, Buy at Ask)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 36 (Figura 9)
**Descrizione:** Un esempio numerico del calcolo del prezzo di un ordine Buy Stop per una rottura. Il calcolo parte dal prezzo massimo del cluster (1.2412), aggiunge un aggiustamento di 0.0004 per il software grafico (presumibilmente per compensare la differenza tra Bid e Ask quando il grafico mostra Ask ma si compra al Bid, anche se il testo lo inserisce come addizione per comprare al Ask) e 0.0005 (5 pip) per il metodo di rottura, risultando in 1.2421.
**Logica Tecnica/Pseudocodice:**
```
// Assumendo CHART_PRICE_TYPE = "ASK" e una coppia EUR/USD
CLUSTER_MAX_PRICE = 1.2412
SOFTWARE_GRAPHIC_ADJUSTMENT = 0.0004 // Come specificato nell'esempio
METHOD_BREAKOUT_PIPS_VALUE = 0.0005 // 5 pips

BUY_STOP_PRICE = CLUSTER_MAX_PRICE + SOFTWARE_GRAPHIC_ADJUSTMENT + METHOD_BREAKOUT_PIPS_VALUE
// BUY_STOP_PRICE = 1.2412 + 0.0004 + 0.0005 = 1.2421
```

---

## 5-Pip Breakout Filter Logic
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 37
**Descrizione:** La logica dietro l'aggiunta di 5 pip al prezzo di rottura è quella di fungere da filtro. Rotture minori (1-3 pip) sono spesso false e non profittevoli. I 5 pip assicurano che si entri solo in rotture significative, indicando che il prezzo è "veramente uscito da un cluster".
**Logica Tecnica/Pseudocodice:**
```
MINIMUM_VALID_BREAKOUT_PIPS = 5

FUNCTION IsBreakoutSignificant(breakout_magnitude_pips):
    IF (breakout_magnitude_pips >= MINIMUM_VALID_BREAKOUT_PIPS):
        RETURN TRUE // Considera una rottura significativa
    RETURN FALSE // Filtra le rotture minori e potenzialmente false
```

---

## Sell Order Calculation Example (Chart Ask, Sell at Bid)
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 38
**Descrizione:** Un esempio numerico del calcolo del prezzo di un ordine Sell Stop per una rottura. Il calcolo parte dal prezzo minimo del cluster (1.2394) e sottrae 0.0005 (5 pip) per il metodo, risultando in 1.2389. Il testo nota che se il grafico traccia Ask e si vende, non sono necessari aggiustamenti per lo spread in questo calcolo specifico (potenzialmente perché 1.2394 è già un prezzo Bid efficace o il contesto implica ciò).
**Logica Tecnica/Pseudocodice:**
```
// Assumendo CHART_PRICE_TYPE = "ASK" e una coppia EUR/USD
CLUSTER_MIN_PRICE = 1.2394
METHOD_BREAKOUT_PIPS_VALUE = 0.0005 // 5 pips

// Nota: il testo afferma che non sono necessari aggiustamenti per gli ordini di vendita se il grafico traccia Ask.
// Quindi, sottraiamo direttamente i 5 pips dal prezzo minimo del cluster.
SELL_STOP_PRICE = CLUSTER_MIN_PRICE - METHOD_BREAKOUT_PIPS_VALUE
// SELL_STOP_PRICE = 1.2394 - 0.0005 = 1.2389
```

---

## Stop Loss for Short Entry Calculation Example
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 39
**Descrizione:** Esempio di calcolo dello stop loss iniziale per un'entrata short. Si parte dal massimo della barra precedente (es. 1.2525), si aggiunge un aggiustamento di 0.0004 per il software grafico (come necessario per un ordine di acquisto che chiude una posizione short, assumendo grafico Ask) e 0.0001 (1 pip) per il metodo, ottenendo 1.2530 come prezzo del Buy Stop.
**Logica Tecnica/Pseudocodice:**
```
// Assumendo CHART_PRICE_TYPE = "ASK" e una coppia EUR/USD
PREVIOUS_BAR_HIGH = 1.2525 // Massimo della barra prima dell'entrata
SOFTWARE_GRAPHIC_ADJUSTMENT = 0.0004 // Aggiustamento per il software grafico (per Buy Stop)
METHOD_SL_PIPS_VALUE = 0.0001 // 1 pip per il metodo

STOP_LOSS_PRICE_SHORT_ENTRY = PREVIOUS_BAR_HIGH + SOFTWARE_GRAPHIC_ADJUSTMENT + METHOD_SL_PIPS_VALUE
// STOP_LOSS_PRICE_SHORT_ENTRY = 1.2525 + 0.0004 + 0.0001 = 1.2530
```

---

## Stop Loss for Long Entry Calculation Example
**Libro/File Originale:** [Allegato PDF]
**Contesto/Pagina:** Pagina 40 (Figura 12)
**Descrizione:** Esempio di calcolo dello stop loss iniziale per un'entrata long. Si parte dal minimo della barra precedente (es. 1.2485) e si sottrae 0.0001 (1 pip) per il metodo, ottenendo 1.2484 come prezzo del Sell Stop. Il testo specifica che, se il software traccia i prezzi Ask e si vende (un Sell Stop), non sono necessari aggiustamenti aggiuntivi per i prezzi.
**Logica Tecnica/Pseudocodice:**
```
// Assumendo CHART_PRICE_TYPE = "ASK" e una coppia EUR/USD
PREVIOUS_BAR_LOW = 1.2485 // Minimo della barra prima dell'entrata
METHOD_SL_PIPS_VALUE = 0.0001 // 1 pip per il metodo

// Nota: il testo afferma che non sono necessari aggiustamenti dei prezzi per gli ordini di vendita (Sell Stop) quando il software traccia Ask.
STOP_LOSS_PRICE_LONG_ENTRY = PREVIOUS_BAR_LOW - METHOD_SL_PIPS_VALUE
// STOP_LOSS_PRICE_LONG_ENTRY = 1.2485 - 0.0001 = 1.2484
```

---

### [PARTE 7: merged_clean_part_07_p241-280.pdf]

## Regola 10. Spostamento dello Stop Loss Iniziale (dopo la prima barra)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 265
**Descrizione:** Gli ordini stop loss non sono statici e vengono spostati ogni ora. Questa regola specifica il primo aggiustamento dello stop loss per entrambi i contratti dopo che la prima barra oraria successiva all'entrata è stata completata. Per un trade al rialzo, lo stop loss viene fissato 1 pip sotto il minimo della barra precedente. Per un trade al ribasso, viene fissato 1 pip sopra il massimo della barra precedente. Questo aggiustamento si verifica una volta completata la prima barra oraria successiva all'entrata.
**Logica Tecnica/Pseudocodice:**
```python
IF direction == "long":
    # stop loss iniziale temporaneo (vedi Regola di stop loss iniziale generale)
    # Dopo che la prima barra oraria (Barra1) si è formata dopo la barra di entrata (Barra0):
    stop_loss_level = Barra0.low - 1_pip 
    # Lo stop loss viene spostato a 1 pip sotto il minimo della barra di entrata per entrambi i contratti
    # Il testo originale della regola indica "la rottura di 1 pip della precedente barra oraria",
    # che dopo la prima barra post-entrata è il minimo della barra di entrata.
    # L'illustrazione in Figura 13 chiarisce che il "Secondo stop loss" (che è il primo spostamento)
    # è sotto il minimo della barra precedente, cioè la barra di entrata (Barra0).
    
IF direction == "short":
    # stop loss iniziale temporaneo (vedi Regola di stop loss iniziale generale)
    # Dopo che la prima barra oraria (Barra1) si è formata dopo la barra di entrata (Barra0):
    stop_loss_level = Barra0.high + 1_pip 
    # Lo stop loss viene spostato a 1 pip sopra il massimo della barra di entrata per entrambi i contratti
```

---

## Regola 11. Spostamento Finale dello Stop Loss (sulla seconda barra)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 266
**Descrizione:** Questo è l'ultimo spostamento dello stop loss se l'obiettivo di profitto iniziale non è stato raggiunto. Quando inizia una seconda barra oraria dopo la barra di entrata, lo stop loss per entrambi i contratti viene spostato alla rottura di 1 pip della precedente barra oraria nella direzione opposta al trade. Per un trade al rialzo, viene spostato 1 pip sotto il minimo della barra dopo quella di entrata (la prima barra completa dopo l'entrata). Per un trade al ribasso, viene spostato 1 pip sopra il massimo della barra dopo quella di entrata.
**Logica Tecnica/Pseudocodice:**
```python
# Sia Barra0 la barra di entrata, Barra1 la prima barra completa dopo Barra0, Barra2 la seconda barra completa dopo Barra0
IF Barra2.started:
    IF direction == "long":
        # Sposta stop loss a 1 pip sotto il minimo della Barra1 (barra formatasi dopo l'entrata)
        stop_loss_level = Barra1.low - 1_pip
    IF direction == "short":
        # Sposta stop loss a 1 pip sopra il massimo della Barra1 (barra formatasi dopo l'entrata)
        stop_loss_level = Barra1.high + 1_pip
```

---

## Regola 12. Uscita alla Chiusura della Barra (Non time-based)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 268
**Descrizione:** Se l'obiettivo di profitto iniziale non è stato raggiunto, si esce dal trade con entrambi i contratti alla chiusura della barra che segue immediatamente la barra di entrata, se questa non forma un massimo più alto (per trade al rialzo) o un minimo più basso (per trade al ribasso). Questa regola serve per uscire da trade che non "decollano" come previsto.
**Logica Tecnica/Pseudocodice:**
```python
# Sia Barra0 la barra di entrata, Barra1 la prima barra completa dopo Barra0
IF initial_profit_target_NOT_reached:
    IF Barra1.completed:
        IF direction == "long" AND Barra1.high <= Barra0.high:
            EXIT_TRADE_AT_Barra1.close_price
        IF direction == "short" AND Barra1.low >= Barra0.low:
            EXIT_TRADE_AT_Barra1.close_price
```

---

## Regola 13. Stop di Tempo di 3 Barre
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 270
**Descrizione:** Se l'obiettivo di profitto iniziale non è stato raggiunto e il trade non è stato stoppato da altre regole di stop loss, si esce con entrambi i contratti alla chiusura della terza barra. Questo conteggio include la barra di entrata come prima barra. L'intervallo di tempo è quindi meno di 3 ore (tra 2 ore e 1 minuto e 2 ore e 59 minuti per barre orarie).
**Logica Tecnica/Pseudocodice:**
```python
# Sia Barra0 la barra di entrata
IF initial_profit_target_NOT_reached AND not_stopped_out_by_price_stop_loss:
    # Dopo che la terza barra (Barra2, contando Barra0 come Barra0) è stata completata
    IF Barra2.completed:
        EXIT_TRADE_AT_Barra2.close_price
```

---

## Regola 14. Regola di Attesa dopo una Perdita
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 272
**Descrizione:** Questa è una regola di gestione del rischio. Se si subisce una perdita in una direzione, bisogna aspettare che si formino 3 barre (incluso la barra di uscita della perdita) prima di entrare di nuovo nella stessa direzione. Inoltre, bisogna aspettare 3 barre (incluso la barra di uscita di qualsiasi trade) prima di entrare nella direzione opposta. L'obiettivo è dare al mercato tempo per recuperare e ai trader tempo per inserire nuovi ordini.
**Logica Tecnica/Pseudocodice:**
```python
# Sia ExitBar la barra in cui il trade precedente è terminato
# cooldown_counter = 0 all'inizio di ExitBar + 1
IF previous_trade_was_loss_in_direction_X:
    FOR current_bar FROM ExitBar.next TO ExitBar.next + 2: # Wait for 3 bars (ExitBar+1, ExitBar+2, ExitBar+3)
        DO_NOT_ENTER_TRADE_IN_DIRECTION_X
    
IF any_previous_trade_just_ended: # If any trade ended (loss or win)
    FOR current_bar FROM ExitBar.next TO ExitBar.next + 2: # Wait for 3 bars
        DO_NOT_ENTER_TRADE_IN_OPPOSITE_DIRECTION_TO_LAST_TRADE
```

---

## Cancellazione Ordini Opposti dopo una Perdita
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 273
**Descrizione:** Se si subisce una perdita in una direzione (es. al rialzo), tutti gli ordini di entrata pendenti nella direzione opposta (es. al ribasso) devono essere cancellati. Viceversa per una perdita al ribasso, gli ordini al rialzo vengono cancellati. Questo previene l'ingresso in trade potenzialmente non profittevoli se le condizioni di mercato non sono favorevoli.
**Logica Tecnica/Pseudocodice:**
```python
IF previous_trade_was_loss_in_direction_X:
    CANCEL_ALL_PENDING_ENTRY_ORDERS_IN_OPPOSITE_DIRECTION_X
```

---

## Regola 15. Chiusura dei Trade Prima della Chiusura del Mercato / Festività
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 273
**Descrizione:** Tutti i trade devono essere chiusi prima della chiusura del mercato del venerdì (ore 17:00 ET USA / 23:00 Italia) e prima di Natale e di altre festività. Questa è una regola di gestione del rischio per evitare l'esposizione a movimenti di prezzo imprevisti (gap) che potrebbero verificarsi durante le ore di chiusura del mercato.
**Logica Tecnica/Pseudocodice:**
```python
IF current_day == FRIDAY AND current_time >= 17:00 ET_USA:
    CLOSE_ALL_OPEN_TRADES
IF current_date IS_BEFORE_MAJOR_HOLIDAY_MARKET_CLOSE:
    CLOSE_ALL_OPEN_TRADES
```

---

## Regola 16. Obiettivo di Profitto Iniziale (per un Contratto)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 274
**Descrizione:** Per uno dei due contratti aperti, viene definito un obiettivo di profitto iniziale fisso a 30 pip. Questo è l'unico ordine limite piazzato sul mercato inizialmente. Il secondo contratto non ha un ordine limite definito e viene gestito con altre regole.
**Logica Tecnica/Pseudocodice:**
```python
IF entering_trade_long:
    SET_LIMIT_ORDER_FOR_CONTRACT_1_AT_PRICE(entry_price + 30_pips)
IF entering_trade_short:
    SET_LIMIT_ORDER_FOR_CONTRACT_1_AT_PRICE(entry_price - 30_pips)
CONTRACT_2_NO_LIMIT_ORDER
```

---

## Stop Loss Iniziale Generale
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 274
**Descrizione:** Quando si piazzano gli ordini, si definisce uno stop loss iniziale di 50 pip. Questo serve come stop di sicurezza generale prima che le regole di stop loss dinamiche (Regole 10 e 11) entrino in gioco.
**Logica Tecnica/Pseudocodice:**
```python
IF placing_entry_orders:
    IF direction == "long":
        SET_INITIAL_STOP_LOSS_FOR_BOTH_CONTRACTS_AT_PRICE(entry_price - 50_pips)
    IF direction == "short":
        SET_INITIAL_STOP_LOSS_FOR_BOTH_CONTRACTS_AT_PRICE(entry_price + 50_pips)
```

---

## Regola 17. Spostamento Stop Loss a Pareggio (per il Secondo Contratto)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 275
**Descrizione:** Una volta che il primo contratto raggiunge il suo obiettivo di profitto di 30 pip, lo stop loss per il secondo contratto (quello rimanente) viene spostato al punto di pareggio (prezzo di entrata). Questo rende il trade sul secondo contratto privo di rischio e permette di farlo correre per profitti maggiori.
**Logica Tecnica/Pseudocodice:**
```python
IF Contract1.limit_order_filled:
    SET_STOP_LOSS_FOR_Contract2_AT_PRICE(entry_price)
```

---

## Regola 18. Spostamento Stop Loss Incrementale (per il Secondo Contratto)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 275
**Descrizione:** Per il secondo contratto, ogni volta che si realizzano altri 30 pip di profitto aggiuntivo (oltre al punto in cui lo stop è stato spostato per l'ultima volta, o dal pareggio se non ci sono stati ulteriori profitti), lo stop loss viene spostato di 30 pip nella direzione del trade. Questo consente di bloccare i profitti man mano che il trade si sviluppa.
**Logica Tecnica/Pseudocodice:**
```python
IF Contract2.open:
    # Esempio per trade long
    # Assumendo che `current_profit_from_entry` sia il profitto corrente in pip dal prezzo di entrata
    # e `last_stop_loss_profit_level` sia il livello di profitto in pip in cui era l'ultimo stop loss
    IF current_profit_from_entry >= (last_stop_loss_profit_level + 30_pips):
        # Sposta lo stop loss al livello del profitto corrente meno 30 pip (per bloccare i profitti)
        # o al livello precedente + 30 pip
        new_stop_loss_profit_level = ((current_profit_from_entry // 30) * 30) - 30 # Esempio: profitto 90 -> stop a 60
        SET_STOP_LOSS_FOR_Contract2_AT_PRICE(entry_price + new_stop_loss_profit_level)
        last_stop_loss_profit_level = new_stop_loss_profit_level # Aggiorna il riferimento
```

---

## Regola 19. Stop di Tempo per il Secondo Contratto (Incrementale)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 276
**Descrizione:** Se il secondo contratto, dopo che il suo stop loss è stato spostato in profitto (tramite Regola 18), non forma ulteriori 30 pip di profitto, si esce dal trade alla chiusura della terza barra. Il conteggio delle barre inizia dalla barra che ha formato gli ultimi 30 pip di profitto incrementale (cioè, la barra che ha attivato l'ultimo spostamento dello stop loss secondo Regola 18).
**Logica Tecnica/Pseudocodice:**
```python
IF Contract2.open AND Contract2.stop_loss_in_profit:
    # Sia Last30PipBar la barra che ha generato gli ultimi 30 pip di profitto aggiuntivo
    # e `new_profit_since_last_30_pip_increment` sia il profitto dal livello di `Last30PipBar`
    IF new_profit_since_last_30_pip_increment < 30_pips:
        # Se 3 barre sono passate da Last30PipBar (Last30PipBar + Barra1 + Barra2)
        IF CurrentBar IS_THIRD_BAR_AFTER_Last30PipBar:
            EXIT_TRADE_FOR_Contract2_AT_CurrentBar.close_price
```

---

## Nota su Tutte le Regole: Flessibilità e Adattamento
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 278
**Descrizione:** Questa è una meta-regola fondamentale. Il trading richiede flessibilità; se una regola non funziona più, deve essere modificata o abbandonata. I mercati cambiano e le strategie devono adattarsi alla realtà del mercato. Mantenere la flessibilità è vitale per il successo a lungo termine.
**Logica Tecnica/Pseudocodice:**
```python
# Non direttamente codificabile come una regola di trading, ma un principio di gestione della strategia.
# Richiede un monitoraggio delle performance delle regole e un processo decisionale umano o AI per l'adattamento.
# IF (performance_di_una_regola_specifica_sotto_soglia):
#     ATTIVA_REVISIONE_MANUALE_O_ADATTAMENTO_ALGORTMICO_DELLA_REGOLA
```

---

## Pazienza: Attesa del Segnale di Entrata (Cluster di 10+ Barre)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 279
**Descrizione:** Un requisito primario è la pazienza nell'attendere il segnale di entrata corretto, che è definito come un cluster di prezzo consolidato di almeno 10 barre. I cluster con meno di 10 barre (es. 8 o 9) non sono considerati validi segnali.
**Logica Tecnica/Pseudocodice:**
```python
IF current_chart_pattern IS_consolidated_price_cluster AND cluster.number_of_bars >= 10:
    SIGNAL_IS_VALID_FOR_ENTRY_EVALUATION
ELSE:
    WAIT_FOR_VALID_CLUSTER
```

---

## Pazienza: Dare Spazio al Trade (Resistere a piccoli drawdown)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 279
**Descrizione:** Dopo aver eseguito un trade, è importante essere pazienti e dare spazio al movimento del prezzo. Non bisogna uscire immediatamente se il prezzo si muove contro di 20 pip. Il metodo prevede che tali piccoli movimenti avversi possano verificarsi.
**Logica Tecnica/Pseudocodice:**
```python
# Assumendo che lo stop loss sia già stato piazzato secondo altre regole
IF current_drawdown_from_entry_price < 20_pips AND not_hit_stop_loss:
    HOLD_TRADE # Non uscire prematuramente
```

---

## Pazienza: Lasciare Correre i Trade Vincenti
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 279
**Descrizione:** La pazienza è necessaria per permettere ai trade vincenti di svilupparsi e raggiungere il loro pieno potenziale. L'uscita prematura da un trade vincente può compromettere significativamente i profitti complessivi e la capacità di recuperare le perdite. Questa è una linea guida per non interferire con le regole di gestione del profitto una volta avviate.
**Logica Tecnica/Pseudocodice:**
```python
IF trade_is_profitable:
    ADHERE_TO_PROFIT_MANAGEMENT_RULES # Non uscire manualmente senza un segnale chiaro dalle regole
```

---

## Requisito di Mercato: Movimento Orizzontale (Congestione)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 280
**Descrizione:** Il metodo di trading descritto nel libro è ottimizzato per coppie di valute che si muovono in modo complessivamente orizzontale, formando consolidamenti (cluster). Se il mercato inizia a formare un trend direzionale forte, il metodo basato sulla rottura di consolidamenti dovrebbe essere interrotto a favore di una strategia di trading sul trend.
**Logica Tecnica/Pseudocodice:**
```python
IF IS_MARKET_IN_STRONG_TREND():
    DO_NOT_APPLY_CONSOLIDATION_BREAKOUT_METHOD
ELSE IF IS_MARKET_IN_HORIZONTAL_CONSOLIDATION():
    APPLY_CONSOLIDATION_BREAKOUT_METHOD
```

---

## Regola sulla Dimensione della Posizione
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 281
**Descrizione:** La regola generale è di operare con 2 contratti per ogni $10.000 disponibili nel conto di trading. Si raccomanda di iniziare con 2 contratti indipendentemente dalla dimensione del conto, e poi scalare la posizione man mano che l'esperienza e il capitale aumentano, sempre tenendo conto del proprio livello di comfort.
**Logica Tecnica/Pseudocodice:**
```python
account_balance = GET_ACCOUNT_BALANCE()
contracts_per_10k = 2
initial_contract_size = 2 # Minimum recommended contracts

IF account_balance < 10000:
    allowed_contracts = initial_contract_size
ELSE:
    allowed_contracts = max(initial_contract_size, (account_balance // 10000) * contracts_per_10k)

# Permette aggiustamenti basati sulla discrezione/comfort del trader
USE_CONTRACTS(min(allowed_contracts, TRADER_COMFORT_LEVEL_CONTRACTS))
```

---

## Identificazione della Reversal Bar (per E-mini S&P)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 284
**Descrizione:** Una "barra di inversione" è un pattern che indica un potenziale cambiamento di direzione a breve termine. In un mercato in discesa, è una barra che chiude più in alto rispetto all'apertura. In un mercato in salita, è una barra che chiude più in basso rispetto all'apertura.
**Logica Tecnica/Pseudocodice:**
```python
IF current_market_direction == "down":
    IF current_bar.close > current_bar.open:
        IS_REVERSAL_BAR = TRUE
    ELSE:
        IS_REVERSAL_BAR = FALSE
IF current_market_direction == "up":
    IF current_bar.close < current_bar.open:
        IS_REVERSAL_BAR = TRUE
    ELSE:
        IS_REVERSAL_BAR = FALSE
```

---

## Strategia di Scalping (su Reversal Bar) per E-mini S&P
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 285
**Descrizione:** Quando si fa trading su una barra di inversione, l'obiettivo è prendere profitti molto rapidamente (scalping). Per l'E-mini S&P, un obiettivo comune è di 1,5 punti per contratto, e l'intera posizione viene chiusa una volta raggiunto questo profitto.
**Logica Tecnica/Pseudocodice:**
```python
IF IS_REVERSAL_BAR_SIGNAL:
    ENTRY_PRICE = GET_ENTRY_PRICE()
    PROFIT_TARGET_POINTS = 1.5
    
    IF direction == "long":
        SET_TAKE_PROFIT_ORDER_FOR_ALL_CONTRACTS(ENTRY_PRICE + PROFIT_TARGET_POINTS)
    IF direction == "short":
        SET_TAKE_PROFIT_ORDER_FOR_ALL_CONTRACTS(ENTRY_PRICE - PROFIT_TARGET_POINTS)
    
    # Implicito: Exit full position when target is hit
```

---

## Stop Loss Protettivo per Scalping (uguale al profitto)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 286
**Descrizione:** Per le operazioni di scalping, lo stop loss protettivo è impostato alla stessa distanza del take profit, creando un rapporto rischio/rendimento 1:1. Ad esempio, se l'obiettivo di profitto è di 1,5 punti, lo stop loss sarà a 1,5 punti. Questo è giustificato dalla ricerca di "trade esplosivi" con forte momentum.
**Logica Tecnica/Pseudocodice:**
```python
IF IS_SCALPING_TRADE:
    PROFIT_TARGET_DISTANCE = GET_PROFIT_TARGET_DISTANCE() # es. 1.5 points
    STOP_LOSS_DISTANCE = PROFIT_TARGET_DISTANCE
    
    IF direction == "long":
        SET_INITIAL_STOP_LOSS_PRICE(ENTRY_PRICE - STOP_LOSS_DISTANCE)
    IF direction == "short":
        SET_INITIAL_STOP_LOSS_PRICE(ENTRY_PRICE + STOP_LOSS_DISTANCE)
```

---

## Spostamento Stop Loss a Pareggio per Scalping (a metà profitto)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 286
**Descrizione:** Nelle operazioni di scalping sull'E-mini S&P, se il prezzo si muove a favore del trade per metà del target di profitto (es. 0.75 punti su un target di 1.5 punti), lo stop loss viene immediatamente spostato al punto di pareggio (prezzo di entrata). Questo protegge il trade da perdite una volta che ha mostrato un iniziale movimento favorevole.
**Logica Tecnica/Pseudocodice:**
```python
IF IS_SCALPING_TRADE:
    PROFIT_TARGET_DISTANCE = GET_PROFIT_TARGET_DISTANCE() # es. 1.5 points
    PROFIT_HALF_WAY_THRESHOLD = PROFIT_TARGET_DISTANCE / 2 # es. 0.75 points

    IF direction == "long" AND current_price >= ENTRY_PRICE + PROFIT_HALF_WAY_THRESHOLD:
        SET_STOP_LOSS_PRICE(ENTRY_PRICE) # Move to breakeven
    IF direction == "short" AND current_price <= ENTRY_PRICE - PROFIT_HALF_WAY_THRESHOLD:
        SET_STOP_LOSS_PRICE(ENTRY_PRICE) # Move to breakeven
```

---

## "Traders Trick™ Entry" (TTE)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 286
**Descrizione:** La "Traders Trick™ Entry" (TTE) è una strategia di entrata che si verifica prima della rottura del "punto 2" in una formazione 1-2-3 high/low. Questo suggerisce un'entrata anticipata basata sull'anticipazione della rottura della formazione 1-2-3.
**Logica Tecnica/Pseudocodice:**
```python
# Assume una funzione per identificare una formazione 1-2-3 (pattern standard di price action)
IF IS_123_FORMATION_DEVELOPING():
    # Identifica le condizioni specifiche per una TTE prima che il punto 2 venga rotto
    IF TTE_CONDITIONS_ARE_MET(point1, point2, point3):
        EXECUTE_ENTRY_BASED_ON_TTE_SIGNAL
```

---

## Ross Hook (Rh)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 288 (e 299 per ulteriore definizione)
**Descrizione:** Un Ross Hook (Rh) è un punto pivot nel grafico che segnala un cambiamento temporaneo nella direzione del mercato, anche per un solo giorno. In un mercato con trend al ribasso, si verifica quando i prezzi non riescono a formare un nuovo minimo (dopo un rally temporaneo, i prezzi scendono ma non rompono il minimo precedente). In un mercato con trend al rialzo, si verifica quando i prezzi non riescono a formare un nuovo massimo. Nel contesto di una formazione 1-2-3, un Rh è il primo punto in cui i prezzi non riescono a estendere il trend dopo la rottura del punto 2.
**Logica Tecnica/Pseudocodice:**
```python
# Context: In a downtrend
IF (last_pivot_low_C AND price_rallies_to_E AND price_then_drops_but_low_F > low_C):
    C_IS_ROSS_HOOK_FOR_DOWNTREND

# General definition:
IF market_is_down_trending:
    IF current_price_fails_to_make_new_low_after_a_rally:
        IDENTIFY_ROSS_HOOK_AT_PIVOT_POINT
IF market_is_up_trending:
    IF current_price_fails_to_make_new_high_after_a_dip:
        IDENTIFY_ROSS_HOOK_AT_PIVOT_POINT
```

---

## Strategia: Trading su Rotture di Congestioni Allineate
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 290
**Descrizione:** Una strategia di trading si concentra su "situazioni esplosive", che includono le rotture di "congestioni allineate". Questo significa cercare più zone di congestione che si allineano, suggerendo un potenziale significativo per una rottura del prezzo.
**Logica Tecnica/Pseudocodice:**
```python
IF IDENTIFY_ALIGNED_CONGESTION_ZONES():
    WAIT_FOR_PRICE_BREAKOUT_OF_ALIGNED_CONGESTION
    EXECUTE_ENTRY_ON_BREAKOUT
```

---

## Strategia: Trading su Barre Reversal dopo Stop Cacciati (Stop Runs)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 290
**Descrizione:** Un'altra "situazione esplosiva" si verifica quando si scambiano barre di inversione che appaiono subito dopo una "caccia agli stop" (stop run), ovvero quando i prezzi si muovono per innescare gli ordini stop-loss e poi si invertono rapidamente. Questo indica false rotture o raccolte di liquidità seguite da un forte cambio di direzione.
**Logica Tecnica/Pseudocodice:**
```python
IF PRICE_HITS_MAJOR_STOP_LOSS_LEVELS AND IMMEDIATELY_FORMS_REVERSAL_BAR():
    EXECUTE_ENTRY_ON_CONFIRMATION_OF_REVERSAL_BAR
```

---

## Principio: Concentrarsi sui Segnali di Entrata Principali
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 290
**Descrizione:** Il trader dovrebbe concentrarsi solo sui "segnali di entrata principali" perché offrono la massima probabilità di successo. Questi segnali non si presentano quotidianamente, ma privilegiare la qualità sulla quantità aiuta a evitare l'overtrading e ad aumentare l'efficacia.
**Logica Tecnica/Pseudocodice:**
```python
IF current_signal IS_MAIN_ENTRY_SIGNAL():
    CONSIDER_TRADE_EXECUTION
ELSE:
    WAIT_FOR_MAIN_ENTRY_SIGNAL # Avoid trading on lesser probability setups
```

---

## Identificazione delle Congestioni (Formazioni /\/\ o \/\/ o serie alternate)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 293
**Descrizione:** Le congestioni sono visibili sul grafico come formazioni del tipo "/\/\ " o "\/\/" (pattern visivi di picchi e valli alternati). La formazione più piccola di tipo "/V\ " o "VV" si ha quando una serie di almeno quattro barre si alternano tra "apertura bassa - chiusura alta" e "apertura alta - chiusura bassa".
**Logica Tecnica/Pseudocodice:**
```python
FUNCTION IS_ALTERNATING_OPEN_CLOSE_BARS(bars_list):
    IF len(bars_list) < 4:
        RETURN FALSE
    
    is_first_bar_up = (bars_list[0].close > bars_list[0].open)
    for i in range(1, len(bars_list)):
        is_current_bar_up = (bars_list[i].close > bars_list[i].open)
        if is_current_bar_up == is_first_bar_up:
            RETURN FALSE # Not alternating
        is_first_bar_up = is_current_bar_up
    RETURN TRUE

# Per i pattern visuali /\/\ o \/\/ serve un'interpretazione algoritmica più complessa dei pivot o degli swing.
# Si considera congestione se:
# 1. Un pattern visivo /\/\ o \/\/ è presente.
# 2. Una serie di almeno 4 barre alternate (open_low_close_high, open_high_close_low) è presente.
```

---

## Identificazione delle Congestioni (con Doji o Chiusure Interne)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 294
**Descrizione:** Un'altra forma di congestione si verifica con una serie di quattro o più barre di prezzo alternate, o che includono candele doji. Inoltre, è considerata congestione se ci sono quattro barre di prezzo consecutive con la chiusura all'interno del range di trading formato dalla barra precedente, anche se i loro massimi o minimi individuali si estendono al di fuori di tale range.
**Logica Tecnica/Pseudocodice:**
```python
FUNCTION CONTAINS_DOJI(bars_list):
    for bar in bars_list:
        IF abs(bar.open - bar.close) < min_doji_body_size: # Placeholder for doji definition
            RETURN TRUE
    RETURN FALSE

FUNCTION IS_CONGESTION_BY_CLOSES_WITHIN_RANGE(current_bars_list, reference_bar):
    IF len(current_bars_list) < 4:
        RETURN FALSE
    
    range_min = min(reference_bar.open, reference_bar.close, reference_bar.low)
    range_max = max(reference_bar.open, reference_bar.close, reference_bar.high)
    
    consecutive_closes_in_range = 0
    for bar in current_bars_list:
        IF bar.close >= range_min AND bar.close <= range_max:
            consecutive_closes_in_range += 1
        ELSE:
            consecutive_closes_in_range = 0
        
        IF consecutive_closes_in_range >= 4:
            RETURN TRUE
    RETURN FALSE

# Una congestione si ha se:
# 1. IS_ALTERNATING_OPEN_CLOSE_BARS(bars_list) OR CONTAINS_DOJI(bars_list) (con almeno 4 barre)
# 2. IS_CONGESTION_BY_CLOSES_WITHIN_RANGE(bars_list, previous_bar)
```

---

## Identificazione del Trend: Nuovi Estremi Successivi (Rialzista)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 294
**Descrizione:** Un modo per identificare un trend rialzista è osservare la rottura del terzo massimo più alto consecutivo in una serie di barre di prezzo. L'azione è di comprare sulla rottura di questo massimo.
**Logica Tecnica/Pseudocodice:**
```python
# Assume una serie di barre N, N-1, N-2, N-3
IF bar_N.high > bar_N-1.high AND bar_N-1.high > bar_N-2.high AND bar_N-2.high > bar_N-3.high:
    # Si sono formati 3 massimi crescenti consecutivi (N-2, N-1, N).
    # L'entrata avviene alla rottura del massimo della barra N.
    IF current_price > bar_N.high:
        ENTRY_LONG_ON_BREAKOUT
```

---

## Identificazione del Trend: Nuovi Estremi Successivi (Ribassista)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 295
**Descrizione:** Per identificare un trend ribassista, si cerca la rottura del terzo minimo più basso consecutivo in una serie di barre di prezzo. L'azione è di vendere sulla rottura di questo minimo.
**Logica Tecnica/Pseudocodice:**
```python
# Assume una serie di barre N, N-1, N-2, N-3
IF bar_N.low < bar_N-1.low AND bar_N-1.low < bar_N-2.low AND bar_N-2.low < bar_N-3.low:
    # Si sono formati 3 minimi decrescenti consecutivi (N-2, N-1, N).
    # L'entrata avviene alla rottura del minimo della barra N.
    IF current_price < bar_N.low:
        ENTRY_SHORT_ON_BREAKOUT
```

---

## Identificazione del Trend: Massimi Decrescenti e Minimi Crescenti (Ribassista)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 295
**Descrizione:** Un trend ribassista può essere identificato da una serie di massimi decrescenti. L'entrata avviene sulla rottura del terzo minimo, anche se non tutte le barre hanno necessariamente minimi più bassi, purché i massimi siano chiaramente decrescenti.
**Logica Tecnica/Pseudocodice:**
```python
IF IS_SERIES_OF_LOWER_HIGHS(lookback_period=X) AND current_price < third_lowest_low_in_pattern:
    ENTRY_SHORT_ON_BREAKOUT
```

---

## Identificazione del Trend: Massimi Decrescenti e Minimi Crescenti (Rialzista)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 295
**Descrizione:** Un trend rialzista può essere identificato da una serie di minimi crescenti. L'entrata avviene sulla rottura del terzo massimo, anche se non tutte le barre hanno necessariamente massimi più alti, purché i minimi siano chiaramente crescenti.
**Logica Tecnica/Pseudocodice:**
```python
IF IS_SERIES_OF_HIGHER_LOWS(lookback_period=X) AND current_price > third_highest_high_in_pattern:
    ENTRY_LONG_ON_BREAKOUT
```

---

## Metodo dei Segmenti (Identificazione del Trend)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 296
**Descrizione:** Questo metodo di identificazione del trend prevede di connettere segmenti di prezzo. Un trend è considerato formato quando tre segmenti consecutivi si muovono nella stessa direzione. Per un trend rialzista, si compra sulla rottura del massimo del terzo segmento. Per un trend ribassista, si vende sulla rottura del minimo del terzo segmento.
**Logica Tecnica/Pseudocodice:**
```python
FUNCTION IDENTIFY_TREND_BY_SEGMENTS(price_data):
    # Identifica i punti pivot (es. swing high/low) per definire i segmenti
    pivots = FIND_PRICE_PIVOTS(price_data)
    
    # Crea segmenti tra i pivot
    segments = CREATE_SEGMENTS_FROM_PIVOTS(pivots)
    
    # Controlla per 3 segmenti consecutivi nella stessa direzione
    IF len(segments) >= 3:
        segment1, segment2, segment3 = segments[-3], segments[-2], segments[-1]
        
        # Trend rialzista: tre segmenti al rialzo consecutivi
        IF segment1.is_up() AND segment2.is_up() AND segment3.is_up():
            IF current_price > segment3.high: # Rottura del massimo del terzo segmento
                RETURN "UPTREND_BUY_SIGNAL"
        
        # Trend ribassista: tre segmenti al ribasso consecutivi
        IF segment1.is_down() AND segment2.is_down() AND segment3.is_down():
            IF current_price < segment3.low: # Rottura del minimo del terzo segmento
                RETURN "DOWNTREND_SELL_SIGNAL"
    RETURN "NO_SIGNAL"
```

---

## Metodo del Vero Trend ("True Trend Method") - Tracciamento Linee di Tendenza (Downtrend)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 298
**Descrizione:** Questo metodo si basa sull'identificazione manuale del trend. In un mercato con trend al ribasso, una linea di tendenza viene tracciata collegando i massimi successivi. Questa linea funge da resistenza dinamica.
**Logica Tecnica/Pseudocodice:**
```python
IF IS_DOWNTRENDING_MARKET_VISUALLY(): # Richiede valutazione visiva/pattern
    # La linea di tendenza è disegnata collegando i massimi (swing highs)
    DRAW_TREND_LINE_CONNECTING_SUCCESSIVE_HIGHS
```

---

## Metodo del Vero Trend ("True Trend Method") - Tracciamento Linee di Tendenza (Uptrend)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 298
**Descrizione:** In un mercato con trend al rialzo, una linea di tendenza viene tracciata collegando i minimi successivi. Questa linea funge da supporto dinamico.
**Logica Tecnica/Pseudocodice:**
```python
IF IS_UPTRENDING_MARKET_VISUALLY(): # Richiede valutazione visiva/pattern
    # La linea di tendenza è disegnata collegando i minimi (swing lows)
    DRAW_TREND_LINE_CONNECTING_SUCCESSIVE_LOWS
```

---

## Metodo del Vero Trend ("True Trend Method") - Aggiornamento Linea di Tendenza (Downtrend)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 299
**Descrizione:** In un downtrend, la trend line viene inizialmente tracciata dal massimo assoluto più alto al massimo della prima correzione significativa. Successivamente, la linea viene aggiornata collegando i massimi di correzione precedenti ai massimi di correzione attuali, ma solo se l'angolo della trend line rimane simile o diventa più ripido, indicando una continuazione o un'accelerazione del momentum.
**Logica Tecnica/Pseudocodice:**
```python
# Inizializzazione
highest_high = GET_ABSOLUTE_HIGHEST_HIGH()
first_correction_high = GET_HIGH_OF_FIRST_SIGNIFICANT_CORRECTION_AFTER_HIGHEST_HIGH()
current_trend_line = CONNECT(highest_high, first_correction_high)

# Aggiornamento
ON_NEW_CORRECTION_HIGH(new_correction_high):
    previous_correction_high = GET_LAST_POINT_OF_CURRENT_TREND_LINE()
    new_segment = CONNECT(previous_correction_high, new_correction_high)
    
    IF GET_ANGLE(new_segment) >= GET_ANGLE(current_trend_line.last_segment): # Include 'similar' as >= roughly
        current_trend_line.ADD_SEGMENT(new_segment)
    ELSE:
        # La linea di tendenza non viene aggiornata se l'angolo si appiattisce troppo
        pass
```

---

## Metodo del Vero Trend ("True Trend Method") - Entrata (Downtrend - Rottura Minimo Giornaliero)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 299
**Descrizione:** In un downtrend, il segnale di entrata per una posizione short è la rottura del minimo del giorno precedente. L'entrata deve avvenire solo se il prezzo *attraversa* il livello di entrata (1 tick sotto il minimo del giorno precedente), non se il prezzo forma un gap al ribasso oltre quel punto. Inizialmente, si entra con un solo contratto.
**Logica Tecnica/Pseudocodice:**
```python
IF IS_DOWNTRENDING_MARKET():
    entry_level = PREVIOUS_DAY_LOW_PRICE - 1_tick
    IF current_price_crosses_below(entry_level) AND NOT_GAPPED_BELOW(entry_level):
        SELL_1_CONTRACT_AT_entry_level
```

---

## Metodo del Vero Trend ("True Trend Method") - Stop Loss Iniziale (10 tick)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 299
**Descrizione:** Lo stop loss iniziale per i trade eseguiti con il "True Trend Method" è fissato a una distanza di 10 tick dal livello di entrata.
**Logica Tecnica/Pseudocodice:**
```python
IF IS_TRUE_TREND_METHOD_TRADE:
    IF direction == "long":
        SET_INITIAL_STOP_LOSS_PRICE(entry_price - 10_ticks)
    IF direction == "short":
        SET_INITIAL_STOP_LOSS_PRICE(entry_price + 10_ticks)
```

---

## Metodo del Vero Trend ("True Trend Method") - Aggiunta di Posizione (Rotture senza gap del minimo precedente)
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 299
**Descrizione:** Nuove posizioni possono essere aggiunte quando i prezzi si allontanano dalla linea di tendenza (indicando un momentum di trend continuo) e rompono il minimo precedente (in un downtrend) senza creare un gap oltre il punto di entrata.
**Logica Tecnica/Pseudocodice:**
```python
IF IS_DOWNTRENDING_MARKET() AND price_is_moving_away_from_trend_line():
    additional_entry_level = PREVIOUS_LOW_PRICE - 1_tick
    IF current_price_crosses_below(additional_entry_level) AND NOT_GAPPED_BELOW(additional_entry_level):
        ADD_CONTRACT_AT_additional_entry_level
```

---

## Metodo del Vero Trend ("True Trend Method") - Regola di Gestione: Limite Correzione Massima
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 299
**Descrizione:** In un downtrend, una correzione non deve andare oltre il massimo del giorno precedente. Se questo accade, è un segnale per rivedere o uscire dal trade. (I criteri sono esattamente opposti per un uptrend).
**Logica Tecnica/Pseudocodice:**
```python
IF IS_DOWNTRENDING_MARKET():
    IF current_correction.high_price > PREVIOUS_DAY_HIGH_PRICE:
        REVIEW_OR_EXIT_TRADE
# Per uptrend, opposto:
IF IS_UPTRENDING_MARKET():
    IF current_correction.low_price < PREVIOUS_DAY_LOW_PRICE:
        REVIEW_OR_EXIT_TRADE
```

---

## Metodo del Vero Trend ("True Trend Method") - Regola di Gestione: Limite Riduzione Profitti
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 299
**Descrizione:** Una correzione non deve ridurre i profitti "sulla carta" di oltre il 50%, una volta che è stato raggiunto un profitto di almeno $100 nel trade. Se i profitti scendono sotto questa soglia, è un segnale per rivedere o uscire.
**Logica Tecnica/Pseudocodice:**
```python
IF paper_profit_current >= 100_dollars:
    IF current_drawdown_from_peak_profit > (peak_paper_profit * 0.5):
        REVIEW_OR_EXIT_TRADE
```

---

## Metodo del Vero Trend ("True Trend Method") - Regola di Gestione: Stop a Pareggio con $50 di Profitto
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 299
**Descrizione:** Quando un trade ha raggiunto $50 di profitto, gli stop loss devono essere spostati al punto di pareggio prima della chiusura del mercato del giorno.
**Logica Tecnica/Pseudocodice:**
```python
IF paper_profit_current >= 50_dollars AND market_is_approaching_daily_close:
    SET_STOP_LOSS_FOR_ALL_CONTRACTS_AT_BREAK_EVEN
```

---

## Metodo del Vero Trend ("True Trend Method") - Regola di Gestione: Stringere Stop su Chiusura Contraria
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 299
**Descrizione:** In un downtrend, il trader deve essere cauto e stringere gli stop loss ogni giorno in cui il mercato chiude sopra l'apertura. Questo indica un potenziale indebolimento del trend ribassista. (I criteri sono esattamente opposti per un uptrend).
**Logica Tecnica/Pseudocodice:**
```python
IF IS_DOWNTRENDING_MARKET():
    IF current_day_close_price > current_day_open_price:
        TIGHTEN_STOP_LOSS_MANUALLY # La logica specifica di "stringere" non è definita
# Per uptrend, opposto:
IF IS_UPTRENDING_MARKET():
    IF current_day_close_price < current_day_open_price:
        TIGHTEN_STOP_LOSS_MANUALLY
```

---

## Metodo del Vero Trend ("True Trend Method") - Breakeven Stop Loss (con piccolo profitto) dopo Entrata
**Libro/File Originale:** Documento PDF allegato
**Contesto/Pagina:** Pagina 301
**Descrizione:** Dopo un'entrata, se si raggiunge un piccolo profitto "sulla carta" (es. 9 tick totali per due contratti, $54) entro la chiusura del mercato, gli stop loss per entrambi i contratti vengono spostati al punto di pareggio. Questo assicura che il trade non possa generare ulteriori perdite.
**Logica Tecnica/Pseudocodice:**
```python
IF total_paper_profit_at_market_close >= 9_ticks_or_54_dollars:
    SET_STOP_LOSS_FOR_ALL_CONTRACTS_AT_BREAK_EVEN
```

---

### [PARTE 8: merged_clean_part_08_p281-316.pdf]

## Ross Hook
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 1, 3, 14, 15, 30
**Descrizione:** Un Ross hook è un pattern che si forma quando un prezzo non crea un nuovo minimo (o massimo, in un trend rialzista) dopo una correzione, segnalando una potenziale continuazione del trend principale. L'autore utilizza i Ross hook come punti di ingresso e come riferimento per posizionare gli stop.
**Logica Tecnica/Pseudocodice:**
1. Identificare un trend (es. al ribasso).
2. Osservare una correzione all'interno di questo trend.
3. Se il prezzo, dopo la correzione, non riesce a formare un nuovo minimo (più basso del minimo precedente significativo) ma forma un minimo più alto di un tick, si è creato un Ross hook.
4. Per un trend al ribasso, un Ross hook viene utilizzato per vendere quando il prezzo rompe il minimo del giorno di formazione del hook o si posiziona uno stop di vendita sotto di esso.
5. Per un trend al rialzo, un Ross hook verrebbe utilizzato per comprare quando il prezzo rompe il massimo del giorno di formazione del hook o si posiziona uno stop di acquisto sopra di esso.

---

## Trend Line
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 1, 3, 5, 6, 8, 9, 15, 30
**Descrizione:** Una trend line è una linea disegnata sul grafico per connettere massimi o minimi successivi, indicando la direzione del trend. L'autore enfatizza il trading in linea con la trend line e la utilizza come riferimento per entrate e uscite.
**Logica Tecnica/Pseudocodice:**
1. Per un trend al ribasso: Disegnare una linea collegando il massimo più alto dell'ultimo movimento al massimo della correzione attuale, e poi i massimi delle correzioni successive.
2. Per un trend al rialzo: Disegnare una linea collegando il minimo più basso dell'ultimo movimento al minimo della correzione attuale, e poi i minimi delle correzioni successive.
3. Posizioni al ribasso sono prese quando i prezzi sono sotto la trend line.
4. Posizioni al rialzo sono prese quando i prezzi sono sopra la trend line.
5. Considerare una rottura della trend line come una continuazione di un nuovo trend appena formato.

---

## Trailing Stop (del 50%)
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 2, 4, 5
**Descrizione:** Un trailing stop mobile che protegge il 50% dei profitti accumulati su un trade. Viene spostato man mano che il profitto aumenta, assicurando che una parte significativa dei guadagni venga mantenuta.
**Logica Tecnica/Pseudocodice:**
1. Aprire una posizione.
2. Quando la posizione mostra un profitto, calcolare il 50% di tale profitto in termini di tick o valore monetario.
3. Spostare lo stop loss a un livello che protegga almeno il 50% del profitto attuale.
4. Aggiornare continuamente il livello dello stop loss man mano che il profitto sul trade aumenta, mantenendo sempre protetto il 50% del profitto massimo raggiunto.
5. Lo stop a pareggio (break-even stop) è una forma iniziale di protezione dove lo stop è posto al prezzo di ingresso.

---

## Stop di Acquisto / Stop di Vendita
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 3, 9
**Descrizione:** Ordini di stop piazzati per limitare le perdite o proteggere i profitti. Un "stop di acquisto" è usato per chiudere una posizione corta, mentre un "stop di vendita" è usato per chiudere una posizione lunga. L'autore sottolinea l'importanza di posizionare correttamente gli stop.
**Logica Tecnica/Pseudocodice:**
1. **Stop di Acquisto (per posizione corta):** Piazzare un ordine di acquisto stop a un livello di prezzo superiore al prezzo di ingresso attuale della posizione corta. L'ordine viene attivato e la posizione chiusa se il prezzo raggiunge o supera il livello dello stop.
2. **Stop di Vendita (per posizione lunga):** Piazzare un ordine di vendita stop a un livello di prezzo inferiore al prezzo di ingresso attuale della posizione lunga. L'ordine viene attivato e la posizione chiusa se il prezzo raggiunge o scende sotto il livello dello stop.
3. Posizionare gli stop sotto ogni Ross hook per le vendite (trend al ribasso) e sopra ogni Ross hook per gli acquisti (trend al rialzo).

---

## Trading con la Rottura del Minimo/Massimo Giornaliero
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 5, 8, 9, 19, 30
**Descrizione:** Tecnica di entrata che sfrutta la rottura del minimo del giorno precedente in un trend al ribasso, o la rottura del massimo del giorno precedente in un trend al rialzo.
**Logica Tecnica/Pseudocodice:**
1. **Per trend al ribasso:** Vendere 1 tick sotto il minimo del giorno precedente (rottura del minimo di ieri).
2. **Per trend al rialzo:** Comprare 1 tick sopra il massimo del giorno precedente (rottura del massimo di ieri).
3. Utilizzare questa logica quando i prezzi si allontanano dalla trend line in corso.

---

## Metodo della Vera Correzione (TCM)
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 7, 8, 11, 12, 13
**Descrizione:** Un metodo per identificare l'inizio di un trend, considerato più prudente del Metodo dei Segmenti. Richiede un calcolo basato su massimi e minimi di barre e un eventuale spostamento del conteggio se le condizioni non sono soddisfatte.
**Logica Tecnica/Pseudocodice:**
**Per trend al ribasso:**
1. **Segmento 1:** Identificare una barra che abbia sia un massimo inferiore sia un minimo inferiore rispetto all'ultimo massimo significativo. Questa barra forma il Segmento 1.
2. **Segmento 2 e 3:** Per i segmenti successivi (2 e 3), cercare solo massimi inferiori.
3. **Validazione:** Se la barra che crea il Segmento 3 non viene rotta dalla barra immediatamente successiva (il suo minimo non viene superato per una vendita), spostare il calcolo verso destra di un segmento e ricominciare a contare dal Segmento 1.
4. **Entrata:** Vendere 1 tick sotto il minimo della barra che ha creato il Segmento 3.

**Per trend al rialzo:**
1. **Segmento 1:** Identificare una barra che abbia sia un minimo superiore sia un massimo superiore rispetto all'ultimo minimo significativo. Questa barra forma il Segmento 1.
2. **Segmento 2 e 3:** Per i segmenti successivi (2 e 3), cercare solo minimi superiori.
3. **Validazione:** Se la barra che crea il Segmento 3 non viene rotta dalla barra immediatamente successiva (il suo massimo non viene superato per un acquisto), spostare il calcolo verso destra di un segmento e ricominciare a contare dal Segmento 1.
4. **Entrata:** Comprare 1 tick sopra il massimo della barra che ha creato il Segmento 3.

---

## Metodo dei Segmenti (SM) / Metodo del Calcolo dei Segmenti (SCM)
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 7, 8, 12, 13
**Descrizione:** Un metodo per identificare l'inizio di un trend, simile al TCM ma meno prudente in quanto il punto di inizio del calcolo è diverso e meno restrittivo. Richiede calcolo e un eventuale spostamento del conteggio. È utile anche per uscire da una congestione.
**Logica Tecnica/Pseudocodice:**
**Per trend al ribasso:**
1. Identificare tre massimi inferiori successivi. Non è necessario che siano consecutivi, ci possono essere barre intermedie.
2. **Validazione:** Richiede 3 segmenti e la rottura da parte della barra immediatamente successiva. Se la barra che crea il Segmento 3 non viene rotta immediatamente dalla barra successiva, spostare il calcolo a destra di un segmento e ricominciare a contare.
3. **Entrata:** Vendere 1 tick sotto il minimo della barra che ha creato il Segmento 3.
4. Questo metodo può essere usato per uscire da una congestione: dopo la rottura, fare trading sul trend e smettere di contare i segmenti.

**Per trend al rialzo:**
1. Identificare tre minimi superiori successivi. Non è necessario che siano consecutivi, ci possono essere barre intermedie.
2. **Validazione:** Richiede 3 segmenti e la rottura da parte della barra immediatamente successiva. Se la barra che crea il Segmento 3 non viene rotta immediatamente dalla barra successiva, spostare il calcolo a destra di un segmento e ricominciare a contare.
3. **Entrata:** Comprare 1 tick sopra il massimo della barra che ha creato il Segmento 3.
4. Questo metodo può essere usato per uscire da una congestione: dopo la rottura, fare trading sul trend e smettere di contare i segmenti.

---

## Metodo del Vero Trend (TTM)
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 8, 9
**Descrizione:** Un metodo di identificazione del trend che si basa esclusivamente sul tracciare una trend line e operare in base ad essa, senza calcoli complessi o spostamenti di conteggi.
**Logica Tecnica/Pseudocodice:**
**Per trend al ribasso:**
1. Disegnare una trend line collegando il massimo più alto dell'ultimo movimento al massimo della correzione attuale, e poi i massimi delle correzioni successive. Si richiede un solo massimo più alto (barra di correzione) per iniziare.
2. **Entrata:** Vendere le rotture del minimo di ogni giorno in cui il mercato si è mosso verso la trend line (1 tick sotto il minimo del giorno precedente).
3. **Gestione del Trade:** Entrare con contratti aggiuntivi quando i prezzi si allontanano dalla trend line, vendendo rotture non in gap del minimo di ogni barra di correzione. Piazzare ordini stop di vendita sotto ogni Ross hook.
4. **Uscita:** Rimanere nel trade fino a quando i prezzi si allontanano dalla trend line formando un massimo inferiore e/o una chiusura più bassa dell'apertura.

**Per trend al rialzo:**
1. Disegnare una trend line collegando il minimo più basso dell'ultimo movimento al minimo della correzione attuale, e poi i minimi delle correzioni successive. Si richiede un solo minimo più basso (barra di correzione) per iniziare.
2. **Entrata:** Comprare le rotture del massimo di ogni giorno in cui il mercato si è mosso verso la trend line (1 tick sopra il massimo del giorno precedente).
3. **Gestione del Trade:** Entrare con contratti aggiuntivi quando i prezzi si allontanano dalla trend line, comprando rotture non in gap del massimo di ogni barra di correzione. Piazzare ordini stop di acquisto sopra ogni Ross hook.
4. **Uscita:** Rimanere nel trade fino a quando i prezzi si allontanano dalla trend line formando un minimo più alto e/o una chiusura più alta dell'apertura.

---

## Metodo dei Nuovi Estremi Successivi (SNEM)
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 9, 10
**Descrizione:** Un metodo di calcolo per identificare l'inizio di un trend basato sulla formazione di tre barre consecutive con minimi o massimi successivi, senza la necessità di aspettare una barra di correzione.
**Logica Tecnica/Pseudocodice:**
**Per trend al ribasso:**
1. Identificare 3 barre consecutive con minimi più bassi (concentrandosi solo sui minimi).
2. **Entrata:** Vendere 1 tick sotto il minimo della barra che forma il terzo minimo più basso.

**Per trend al rialzo:**
1. Identificare 3 barre consecutive con massimi più alti (concentrandosi solo sui massimi).
2. **Entrata:** Comprare 1 tick sopra il massimo della barra che forma il terzo massimo più alto.

---

## Massimi Decrescenti (SHM)
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 10
**Descrizione:** Un metodo di calcolo per identificare un trend al ribasso basato sulla formazione di tre barre consecutive con massimi decrescenti, senza la necessità di nuovi minimi.
**Logica Tecnica/Pseudocodice:**
**Per trend al ribasso:**
1. Identificare tre barre consecutive con massimi più bassi (massimi decrescenti).
2. **Entrata:** Vendere la rottura del minimo della barra che ha formato il terzo massimo inferiore.

---

## Minimi Crescenti (RLM)
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 10, 11
**Descrizione:** Un metodo di calcolo per identificare un trend al rialzo basato sulla formazione di tre barre consecutive con minimi crescenti, senza la necessità di nuovi massimi.
**Logica Tecnica/Pseudocodice:**
**Per trend al rialzo:**
1. Identificare tre barre consecutive con minimi più alti (minimi crescenti).
2. **Entrata:** Comprare la rottura del massimo della barra che ha formato il terzo minimo superiore consecutivo. (Nota: Il testo originale conteneva una potenziale contraddizione suggerendo "Vendi", ma l'interpretazione logica per "minimi crescenti" in un trend al rialzo è l'acquisto.)

---

## Analisi Multi-Timeframe per Ritracciamenti
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 14
**Descrizione:** Tecnica che implica l'osservazione di grafici su diversi intervalli temporali per identificare movimenti contrari al trend su un intervallo più lungo, che potrebbero indicare ritracciamenti e opportunità di ingresso nel trend principale.
**Logica Tecnica/Pseudocodice:**
1. Identificare un trend su un intervallo temporale più lungo (es. 60 minuti).
2. Passare a un intervallo temporale più breve (es. 15 minuti).
3. Cercare movimenti dei prezzi nella direzione opposta al trend del timeframe più lungo (ritracciamenti).
4. Prepararsi a entrare nel mercato quando i prezzi sul timeframe più breve mostrano segni di riprendere il movimento nella direzione del trend principale.

---

## Doji
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 17, 18
**Descrizione:** Un pattern di candele giapponesi in cui il prezzo di apertura e chiusura sono uguali o molto vicini, formando una barra con un corpo molto piccolo. Spesso segnala indecisione nel mercato e può precedere un cambio di direzione.
**Logica Tecnica/Pseudocodice:**
1. Identificare una barra in cui (Close - Open) è molto vicino a zero o uguale a zero.
2. In un trend, una Doji può segnalare che il mercato si sta preparando a muoversi nella direzione opposta nella barra successiva.
3. Se combinata con una barra di inversione, l'indicazione di un cambio di trend imminente è più forte.
4. Le Doji sono meno affidabili nelle aree di congestione, dove sono comuni e indicano consolidamento.
5. Se in un trade, considerare di stringere gli stop in presenza di una Doji in un trend.

---

## Barra di Inversione (Reversal Bar)
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 17, 18
**Descrizione:** Una barra di prezzo che segnala un potenziale cambio di trend. In un mercato che scende, una barra di inversione ha una chiusura più alta dell'apertura. In un mercato che sale, ha una chiusura più bassa dell'apertura.
**Logica Tecnica/Pseudocodice:**
1. **Per inversione al rialzo (in un downtrend):** Una barra con chiusura più alta dell'apertura.
2. **Per inversione al ribasso (in un uptrend):** Una barra con chiusura più bassa dell'apertura.
3. Le barre di inversione possono indicare un cambiamento di trend.
4. Una combinazione di due o tre barre di inversione consecutive, o alternate con barre nella direzione del trend, è un segnale più forte di cambiamento di trend.
5. In presenza di barre di inversione in un trend, considerare di stringere gli stop o prepararsi a uscire.
6. Se non si è entrati, attendere una rottura o l'inizio di un trend.

---

## Traders Trick™ Entry
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 5, 20, 34
**Descrizione:** Una tattica di entrata nel mercato che sfrutta i ritracciamenti verso una trend line. L'entrata avviene quando i prezzi, dopo essersi avvicinati alla trend line, riprendono a muoversi nella direzione del trend principale. Le statistiche mostrano una probabilità di 2 a 1 a favore di un trade nella direzione del trend in queste circostanze.
**Logica Tecnica/Pseudocodice:**
1. Identificare un trend definito e una trend line.
2. Attendere che i prezzi si avvicinino alla trend line a causa di una correzione.
3. Entrare nella direzione del trend principale quando i prezzi riprendono a muoversi in quella direzione dopo il ritracciamento.
4. L'autore menziona anche di entrare su "rotture" in generale come Traders Trick Entry.

---

## Trading sulle Rotture di Consolidamento (Congestione)
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 20, 22, 30, 34
**Descrizione:** Strategia che si concentra sul trading quando i prezzi escono da un'area di consolidamento (congestione), che è un periodo di movimento laterale. L'autore preferisce questa strategia allo scalping all'interno del consolidamento.
**Logica Tecnica/Pseudocodice:**
1. Identificare un'area di consolidamento (movimento laterale dei prezzi).
2. Attendere che i prezzi rompano l'intervallo di questa congestione.
3. Entrare nel trade nella direzione della rottura.
4. Le rotture da "congestioni larghe, seguite da un "pop" o una punta e poi da una congestione più stretta" offrono elevate probabilità di successo.

---

## Trading sull'Inerzia del Mercato dopo Ritracciamenti degli Scalper
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 20
**Descrizione:** Strategia che consiste nell'entrare nel mercato dopo che gli scalper hanno liquidato i loro profitti, causando un piccolo ritracciamento. L'idea è di sfruttare il movimento di continuazione del trend che segue la chiusura delle posizioni degli operatori a breve termine.
**Logica Tecnica/Pseudocodice:**
1. Osservare il mercato per identificare movimenti guidati dagli scalper (che cercano pochi tick).
2. Attendere il piccolo ritracciamento che si verifica quando gli scalper liquidano le loro posizioni.
3. Entrare nel mercato nella direzione del trend principale non appena i prezzi riprendono a muoversi dopo il ritracciamento.

---

## Tazza con Manico (Cup with Handle)
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 21, 22
**Descrizione:** Un pattern grafico che si forma con un calo dei prezzi (la "tazza") seguito da una fase di congestione che inizia a mostrare minimi crescenti verso la fine (il "manico").
**Logica Tecnica/Pseudocodice:**
1. Identificare un calo dei prezzi che forma una forma a "U" o "V" arrotondata (la tazza).
2. Dopo il calo, osservare una fase di congestione laterale (il manico).
3. All'interno del manico, i minimi devono essere crescenti.
4. **Per i futures:** L'aspettativa è una rottura sia al rialzo che al ribasso.
5. **Per il mercato azionario:** L'aspettativa è una rottura al rialzo.
6. Una congestione stretta con minimi crescenti generalmente porta a una rottura e un forte movimento verso l'alto.
7. L'opposto (congestione stretta con massimi decrescenti) di solito porta a un movimento al ribasso.

---

## Aree di Congestione Allineate
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 22
**Descrizione:** Aree di consolidamento orizzontale dei prezzi che possono fungere da eccellenti punti di ingresso. L'orientamento dei minimi (o massimi) all'interno della congestione fornisce indizi sulla direzione più probabile della rottura.
**Logica Tecnica/Pseudocodice:**
1. Identificare un periodo in cui i prezzi si muovono lateralmente, formando un'area di congestione.
2. Osservare l'orientamento dei minimi all'interno della congestione. Se i minimi sono crescenti, suggerisce una rottura al rialzo.
3. Osservare l'orientamento dei massimi all'interno della congestione. Se i massimi sono decrescenti, suggerisce una rottura al ribasso.
4. Utilizzare la rottura da queste aree come punto di ingresso.

---

## Gestione del Rischio: Perdite Piccole e Calcolate
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 6, 24, 26
**Descrizione:** Principio fondamentale per il trading di successo: le perdite devono essere sempre piccole, calcolate e non temute. Questo permette di preservare il capitale e la volontà di continuare a provare.
**Logica Tecnica/Pseudocodice:**
1. Prima di ogni trade, definire un livello massimo di perdita accettabile.
2. Piazzare uno stop loss in modo che la perdita massima rientri nei parametri predefiniti.
3. Non lasciare che le perdite superino il capitale disponibile o il livello di comfort emotivo.
4. Se lo stop non può essere posizionato correttamente (es. troppo lontano), non entrare nel trade.

---

## Non Trading su Fibonacci (Tecnica Rifiutata)
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 25, 26, 27
**Descrizione:** L'autore rifiuta categoricamente l'uso dei numeri di Fibonacci (ritracciamenti 0.382, 0.500, 0.618) come base per decisioni di trading o posizionamento di ordini. Li considera una "magia" o "illusione" che porta i trader a perdere, soprattutto in mercati volatili.
**Logica Tecnica/Pseudocodice:**
1. Non piazzare ordini di entrata basati sui livelli di ritracciamento di Fibonacci (0.382, 0.500, 0.618).
2. Non considerare i ritracciamenti di Fibonacci come supporto o resistenza affidabili per aprire posizioni.
3. Se un trade coincide con un livello di Fibonacci "per puro caso", non è una motivazione valida per l'entrata.

---

## Reiezione del Pattern Testa e Spalle (come strumento predittivo)
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 28, 29
**Descrizione:** Sebbene il pattern "Testa e Spalle" (Head and Shoulders) sia riconosciuto visivamente, l'autore rifiuta la sua comune interpretazione predittiva. Sostiene che le aspettative sulla direzione della rottura sono spesso errate (40-50% delle volte, il prezzo va nella direzione sbagliata).
**Logica Tecnica/Pseudocodice:**
1. Identificare visivamente la formazione "Testa e Spalle" su un grafico.
2. Non assumere che la rottura avverrà nella direzione classicamente prevista (es. al ribasso per una testa e spalle superiore).
3. Non basare decisioni di trading sulla direzione attesa di rottura di questo pattern.

---

## Trading "What I See"
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 29, 30
**Descrizione:** Filosofia di trading fondamentale dell'autore che enfatizza l'azione basata solo su ciò che è oggettivamente visibile sul grafico, piuttosto che su opinioni personali, intuizioni o credenze. È un mantra che guida tutte le decisioni di trading.
**Logica Tecnica/Pseudocodice:**
1. Ignorare pensieri, opinioni o sensazioni personali riguardo alla direzione futura del mercato.
2. Basare tutte le decisioni di acquisto/vendita esclusivamente sull'analisi diretta dei movimenti di prezzo e dei pattern grafici (trend lines, Ross hooks, rotture, ecc.).
3. Se il trend è al rialzo, cercare attivamente opportunità di acquisto (ritracciamenti, rotture di massimi giornalieri, Ross hooks).
4. Se il trend è al ribasso, cercare attivamente opportunità di vendita (correzioni, rotture di minimi giornalieri, Ross hooks).

---

## Selezione dei Migliori Trade e Pazienza
**Libro/File Originale:** Documento Allegato
**Contesto/Pagina:** Pagina 34
**Descrizione:** Un principio di disciplina che suggerisce di non cercare di fare ogni trade possibile, ma di attendere solo i trade con le migliori probabilità di successo. Ciò include aspettare la formazione di congestioni prima delle rotture, preferendo congestioni piccole, strette o lunghe e sottili.
**Logica Tecnica/Pseudocodice:**
1. Evitare il trading eccessivo.
2. Essere selettivi e pazienti, aspettando che il mercato formi configurazioni ad alta probabilità.
3. Concentrarsi su congestioni ben definite, specialmente quelle "larghe, seguite da un 'pop' o una punta e poi da una congestione più stretta".
4. Quando non si fa trading su congestioni, identificare e seguire i trend.

---