# SKILLS ESTRATTE: Long-Term Secrets to Short-Term Trading 1999.pdf

## Short-Term High/Low (Pivot Points)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 1: Understanding Market Structure (Page 15-17, 21-22)
**Descrizione:** This technique defines short-term market turning points (highs and lows) which are fundamental to understanding market structure. A short-term low occurs when a day's low is bracketed by two consecutive non-inside days with *higher* lows. Conversely, a short-term high occurs when a day's high is bracketed by two consecutive non-inside days with *lower* highs. Inside days (where the entire range is within the previous day's range) are explicitly ignored for identifying these swing points. Outside days (where the range engulfs the previous day's range) may require further intraday analysis. Confirmation of these pivots occurs when price rallies above the high of the low day (for a low) or declines below the low of the high day (for a high).
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data (Open, High, Low, Close)
// Assume 'N' is the total number of days
// An 'inside_day' is defined as: High[i] < High[i-1] AND Low[i] > Low[i-1]

FUNCTION IsInsideDay(Days, i):
    IF i < 1: RETURN FALSE
    RETURN Days[i].High < Days[i-1].High AND Days[i].Low > Days[i-1].Low

// Identify a Short-Term Low at index 'i'
FUNCTION IdentifyShortTermLow(Days, i):
    IF i < 1 OR i >= Days.Length - 1: RETURN FALSE // Needs previous and next day
    IF IsInsideDay(Days, i) OR IsInsideDay(Days, i-1) OR IsInsideDay(Days, i+1): RETURN FALSE
    // Low[i] is a short-term low if it's the lowest, and adjacent lows are higher
    IF Days[i].Low < Days[i-1].Low AND Days[i].Low < Days[i+1].Low AND \
       Days[i-1].Low > Days[i].Low AND Days[i+1].Low > Days[i].Low:
        RETURN TRUE
    RETURN FALSE

// Identify a Short-Term High at index 'i'
FUNCTION IdentifyShortTermHigh(Days, i):
    IF i < 1 OR i >= Days.Length - 1: RETURN FALSE // Needs previous and next day
    IF IsInsideDay(Days, i) OR IsInsideDay(Days, i-1) OR IsInsideDay(Days, i+1): RETURN FALSE
    // High[i] is a short-term high if it's the highest, and adjacent highs are lower
    IF Days[i].High > Days[i-1].High AND Days[i].High > Days[i+1].High AND \
       Days[i-1].High < Days[i].High AND Days[i+1].High < Days[i].High:
        RETURN TRUE
    RETURN FALSE

// Confirm a Short-Term Low identified at index 'pivot_index'
// Confirmation occurs when price rallies above the high of the pivot day
FUNCTION ConfirmShortTermLow(Days, pivot_index, current_index):
    IF IdentifyShortTermLow(Days, pivot_index):
        IF current_index > pivot_index AND Days[current_index].High > Days[pivot_index].High:
            RETURN TRUE
    RETURN FALSE

// Confirm a Short-Term High identified at index 'pivot_index'
// Confirmation occurs when price declines below the low of the pivot day
FUNCTION ConfirmShortTermHigh(Days, pivot_index, current_index):
    IF IdentifyShortTermHigh(Days, pivot_index):
        IF current_index > pivot_index AND Days[current_index].Low < Days[pivot_index].Low:
            RETURN TRUE
    RETURN FALSE
```

---

## Intermediate/Long-Term Highs and Lows (Nested Pivot Points)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 1: Defining Intermediate Highs and Lows (Page 23)
**Descrizione:** This technique extends the concept of short-term highs and lows hierarchically to identify intermediate and long-term turning points. An intermediate-term high is defined as a short-term high that is itself bracketed by two consecutive (non-inside) short-term highs with *lower* values. A long-term high is an intermediate-term high bracketed by two consecutive (non-inside) intermediate-term highs with *lower* values. The same nested logic applies symmetrically for identifying intermediate-term and long-term lows, providing a multi-timeframe perspective on market structure and trend.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'ShortTermHighs' and 'ShortTermLows' are lists of identified Short-Term Pivot Points (index and value).
// Assume similar data structures for IntermediateTermHighs/Lows.

// Identify an Intermediate-Term Low at index 'i' within the ShortTermLows list
FUNCTION IdentifyIntermediateTermLow(ShortTermLows, i):
    IF i < 1 OR i >= ShortTermLows.Length - 1: RETURN FALSE
    // ShortTermLows[i] is an intermediate low if its value is lowest, and adjacent STLs are higher
    IF ShortTermLows[i].Value < ShortTermLows[i-1].Value AND ShortTermLows[i].Value < ShortTermLows[i+1].Value AND \
       ShortTermLows[i-1].Value > ShortTermLows[i].Value AND ShortTermLows[i+1].Value > ShortTermLows[i].Value:
        RETURN TRUE
    RETURN FALSE

// Identify an Intermediate-Term High at index 'i' within the ShortTermHighs list
FUNCTION IdentifyIntermediateTermHigh(ShortTermHighs, i):
    IF i < 1 OR i >= ShortTermHighs.Length - 1: RETURN FALSE
    // ShortTermHighs[i] is an intermediate high if its value is highest, and adjacent STHs are lower
    IF ShortTermHighs[i].Value > ShortTermHighs[i-1].Value AND ShortTermHighs[i].Value > ShortTermHighs[i+1].Value AND \
       ShortTermHighs[i-1].Value < ShortTermHighs[i].Value AND ShortTermHighs[i+1].Value < ShortTermHighs[i].Value:
        RETURN TRUE
    RETURN FALSE

// Identify a Long-Term Low at index 'i' within the IntermediateTermLows list
FUNCTION IdentifyLongTermLow(IntermediateTermLows, i):
    IF i < 1 OR i >= IntermediateTermLows.Length - 1: RETURN FALSE
    // IntermediateTermLows[i] is a long-term low if its value is lowest, and adjacent ITLs are higher
    IF IntermediateTermLows[i].Value < IntermediateTermLows[i-1].Value AND IntermediateTermLows[i].Value < IntermediateTermLows[i+1].Value AND \
       IntermediateTermLows[i-1].Value > IntermediateTermLows[i].Value AND IntermediateTermLows[i+1].Value > IntermediateTermLows[i].Value:
        RETURN TRUE
    RETURN FALSE

// Identify a Long-Term High at index 'i' within the IntermediateTermHighs list
FUNCTION IdentifyLongTermHigh(IntermediateTermHighs, i):
    IF i < 1 OR i >= IntermediateTermHighs.Length - 1: RETURN FALSE
    // IntermediateTermHighs[i] is a long-term high if its value is highest, and adjacent ITHs are lower
    IF IntermediateTermHighs[i].Value > IntermediateTermHighs[i-1].Value AND IntermediateTermHighs[i].Value > IntermediateTermHighs[i+1].Value AND \
       IntermediateTermHighs[i-1].Value < IntermediateTermHighs[i].Value AND IntermediateTermHighs[i+1].Value < IntermediateTermHighs[i].Value:
        RETURN TRUE
    RETURN FALSE
```

---

## Natural Cycle of Range Change (Volatility Cycle)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 2: The Natural Cycle of Range Change (Page 27-29, Figures 2.6-2.13)
**Descrizione:** This fundamental market observation states that price ranges (High minus Low) in any given timeframe and market consistently cycle from small ranges to large ranges, and then back from large ranges to small ranges. Small ranges indicate market contraction and are precursors to explosive price moves (large ranges), which offer the greatest profit potential for short-term traders. Conversely, large ranges often give way to periods of smaller ranges or congestion, signaling reduced profit opportunities. The core idea is to establish trades *in advance* of these large-range days.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data (Open, High, Low, Close)
// Assume 'Range[i]' is Days[i].High - Days[i].Low

// Parameters:
N_AVG_DAYS = 10 // Lookback period for average range
THRESHOLD_FACTOR_SMALL = 0.75 // Current range < 75% of average for small
THRESHOLD_FACTOR_LARGE = 1.25 // Current range > 125% of average for large

// 1. Calculate Average Range
FUNCTION CalculateAverageRange(Days, i, N_days):
    IF i < N_days - 1: RETURN NULL // Not enough data
    sum_ranges = 0
    FOR j FROM i-N_days+1 TO i:
        sum_ranges = sum_ranges + (Days[j].High - Days[j].Low)
    RETURN sum_ranges / N_days

// 2. Identify Small Range Days (Volatility Contraction)
FUNCTION IsSmallRangeDay(Days, i):
    IF i < N_AVG_DAYS: RETURN FALSE
    current_range = Days[i].High - Days[i].Low
    avg_recent_range = CalculateAverageRange(Days, i-1, N_AVG_DAYS) // Use previous days for average
    IF avg_recent_range > 0 AND current_range < avg_recent_range * THRESHOLD_FACTOR_SMALL:
        RETURN TRUE
    RETURN FALSE

// 3. Identify Large Range Days (Volatility Expansion)
FUNCTION IsLargeRangeDay(Days, i):
    IF i < N_AVG_DAYS: RETURN FALSE
    current_range = Days[i].High - Days[i].Low
    avg_recent_range = CalculateAverageRange(Days, i-1, N_AVG_DAYS)
    IF avg_recent_range > 0 AND current_range > avg_recent_range * THRESHOLD_FACTOR_LARGE:
        RETURN TRUE
    RETURN FALSE

// Trading Strategy Implication:
// - Seek entry signals (direction determined by other trend analysis) after a sequence of `IsSmallRangeDay` events, anticipating an imminent large range day.
// - Consider exiting or reducing positions after `IsLargeRangeDay` events, anticipating a return to smaller ranges/congestion.
```

---

## Open-to-Close Relationship on Large-Range Days
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 2: The Importance of the Open to Low or High of the Day (Page 33-36, Figure 2.14, 2.15)
**Descrizione:** This pattern highlights the characteristic behavior of price on days experiencing significant movement (large range days). For large-range *up* days, the market typically opens near its low and closes near its high. Conversely, for large-range *down* days, it generally opens near its high and closes near its low. This implies that if a large-range up day is anticipated, buying opportunities far below the open are statistically less likely to lead to a strong close, and vice-versa for expected large-range down days. The author provides statistical evidence showing that a small dip below the open on an anticipated up day still correlates with a high probability of closing higher.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data (Open, High, Low, Close)
// Assume 'Range[i]' is Days[i].High - Days[i].Low
// Assume 'IsExpectedLargeRangeUpDay(i)' or 'IsExpectedLargeRangeDownDay(i)' are booleans from other predictive models (e.g., Volatility Cycle).

// Parameters for Exit/Avoidance:
DIP_BELOW_OPEN_EXIT_THRESHOLD = 0.70 // If Open-Low is 70% of Range on expected up day, exit long
RALLY_ABOVE_OPEN_EXIT_THRESHOLD = 0.70 // If High-Open is 70% of Range on expected down day, exit short
DIP_BELOW_OPEN_AVOID_BUY_THRESHOLD = 0.20 // If Open-Low > 20% of Range, avoid buying on expected up day

// Rule 1: Don't try to buy big dips below the open on expected up close days.
FUNCTION AvoidBuyingBigDip(Days, i):
    IF IsExpectedLargeRangeUpDay(i):
        dip_from_open_pct = (Days[i].Open - Days[i].Low) / Days[i].Range
        IF dip_from_open_pct > DIP_BELOW_OPEN_AVOID_BUY_THRESHOLD:
            RETURN TRUE // Avoid buying
    RETURN FALSE

// Rule 2: If long and prices fall much below the open on expected big up close days, "get out."
FUNCTION ExitLongOnDeepDip(Days, i, Position_is_Long):
    IF Position_is_Long AND IsExpectedLargeRangeUpDay(i):
        dip_from_open_pct = (Days[i].Open - Days[i].Low) / Days[i].Range
        IF dip_from_open_pct > DIP_BELOW_OPEN_EXIT_THRESHOLD:
            RETURN TRUE // Exit long position
    RETURN FALSE

// Rule 3: Don't try to sell big rallies above the opening on expected large down days.
FUNCTION AvoidSellingBigRally(Days, i):
    IF IsExpectedLargeRangeDownDay(i):
        rally_from_open_pct = (Days[i].High - Days[i].Open) / Days[i].Range
        IF rally_from_open_pct > DIP_BELOW_OPEN_AVOID_BUY_THRESHOLD: // Symmetric logic, using 20% for now
            RETURN TRUE // Avoid selling
    RETURN FALSE

// Rule 4: If short and prices rally much above opening on expected large down days, "get out."
FUNCTION ExitShortOnBigRally(Days, i, Position_is_Short):
    IF Position_is_Short AND IsExpectedLargeRangeDownDay(i):
        rally_from_open_pct = (Days[i].High - Days[i].Open) / Days[i].Range
        IF rally_from_open_pct > RALLY_ABOVE_OPEN_EXIT_THRESHOLD:
            RETURN TRUE // Exit short position
    RETURN FALSE
```

---

## Close Relative to Daily Range Extremes (Trend Indication)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 2: Where the Trend Is with You-The Second Power Play Price Pattern (Page 36-37, 43, Figures 2.16-2.23)
**Descrizione:** This pattern serves as a universal indicator of trend strength across various timeframes. The core principle is that a market that is bottoming or in the early stages of an uptrend will exhibit daily (or bar) closes that are at or very close to the low of the day's range. Conversely, a market that is topping or in the early stages of a downtrend will show closes that are at or very close to the high of the day's range. As a trend matures (upwards), closes will progressively move higher within the daily range, indicating persistent buying pressure. This relationship changes as buying or selling forces dominate.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data (Open, High, Low, Close)
// Assume 'Range[i]' is Days[i].High - Days[i].Low

// Calculate Closing Price Position within Range (0 to 1, where 0 is Low and 1 is High)
FUNCTION ClosingPositionRatio(Days, i):
    IF Days[i].Range == 0: RETURN 0.5 // Handle zero range days (or define appropriately)
    RETURN (Days[i].Close - Days[i].Low) / Days[i].Range

// Interpretation and Trading Rules:
// 1. Market Low / Early Upturn Identification:
//    IF ClosingPositionRatio(Days, i) <= 0.05 (close near low) for a day, and other conditions suggest a reversal up:
//        Anticipate potential market low and a buy signal.
//        (Rule from page 45: "Most all market lows can be found to occur at or shortly after a market closes right on the low of the day.")

// 2. Market High / Early Downturn Identification:
//    IF ClosingPositionRatio(Days, i) >= 0.95 (close near high) for a day, and other conditions suggest a reversal down:
//        Anticipate potential market high and a sell signal.
//        (Rule from page 45: "Most all market highs can be found to occur at or shortly after a market closes right on the high of the day.")

// 3. Trend Strength Indication:
//    - Consistently increasing ClosingPositionRatio (moving towards 1) over several bars indicates a strengthening uptrend.
//    - Consistently decreasing ClosingPositionRatio (moving towards 0) over several bars indicates a strengthening downtrend.
```

---

## Hold to the Close (or Longer)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 3: The Real Secret to Short-Term Trading (Page 45-55, Figures 3.1-3.6, 3.7-3.11)
**Descrizione:** The core principle is that significant profits in short-term trading are achieved not by quick in-and-out trading, but by allowing winning trades enough time to develop and run their course, especially on "large-range days." The author states that "the shorter your time frame of trading the less money you will make." The most profitable strategy for short-term traders is to enter a trade, set a protective stop, and then hold the position until at least the market close, or even longer (2-5 days) to maximize profit potential. This counteracts the common mistake of day traders who limit their profits by exiting too early. This strategy is particularly effective on large-range days, where prices tend to open near one extreme and close near the other, allowing substantial gains to accrue.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Entry_Signal_Occurred' is true based on other trading system rules
// Assume 'Protective_Stop_Price' is set for the trade
// Assume 'CurrentDayIndex' and 'EntryDayIndex' are available

// Entry Logic:
FUNCTION ExecuteEntry(signal_type, entry_price, stop_price):
    // Placeholder for trade execution
    Position = {Type: signal_type, EntryPrice: entry_price, EntryDayIndex: CurrentDayIndex, StopLossPrice: stop_price}
    RETURN Position

// Exit Logic (Primary Strategy):
FUNCTION EvaluateExit(Position, CurrentDayIndex):
    IF Position IS NOT OPEN: RETURN NULL // No active position

    // Apply Protective Stop Loss (first priority)
    IF (Position.Type == BUY AND CurrentDay.Low < Position.StopLossPrice) OR \
       (Position.Type == SELL AND CurrentDay.High > Position.StopLossPrice):
        EXECUTE_EXIT(Position.Type, CurrentMarketPriceAtStopHit)
        RETURN "STOP_LOSS_HIT"

    // Hold to the Close (or longer for multi-day swings)
    // The main point is to avoid premature intraday exits on winning trades.
    // For systems designed for 2-5 day swings, the position should not be closed at end of entry day.

    // Example for multi-day swing exit:
    // If trade is intended for multi-day swing, exit logic needs to be based on further signals
    // or a fixed holding period, not necessarily end-of-day.
    // The "Bailout" exit (first profitable opening) is a more specific rule for such cases (See General Exit Rules).
    
    // For single-day "large-range" trade, exit on close of entry day
    IF IsLargeRangeDay(CurrentDayIndex) AND CurrentDayIndex == Position.EntryDayIndex:
        EXECUTE_EXIT(Position.Type, CurrentDay.Close)
        RETURN "EOD_LARGERANGE_PROFIT_TAKE"

    RETURN NULL // Continue holding
```

---

## Volatility Breakouts (Momentum Breakthrough)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 4: Volatility Breakouts, The Momentum Breakthrough (Page 57-60, Tables 4.1-4.3)
**Descrizione:** This concept posits that market trends are initiated by "explosions of price activity," or significant increases in volatility, which then tend to persist in that direction. The key is to identify when current market volatility (measured by daily range: High-Low) expands significantly relative to recent volatility. A substantial increase in today's range compared to yesterday's range is seen as a strong indicator of a new impetus driving price in a specific direction. The most effective entry method identified is to add a percentage of today's range to tomorrow's open for a buy signal, or subtract it for a sell signal.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data (Open, High, Low, Close)
// Assume 'Range[i]' is Days[i].High - Days[i].Low

// Parameters:
THRESHOLD_FACTOR_BREAKOUT = 1.0 // 100% means today's range must be larger than yesterday's
// Specific Volatility Factors for Buy/Sell (from Table 4.3, e.g., for Cattle: 140% for Buy, for Bonds: 100% for Sell)
// These factors depend on the commodity and direction.

// 1. Identify Volatility Breakout
FUNCTION IsVolatilityBreakout(Days, i):
    IF i < 1: RETURN FALSE // Needs previous day
    IF Days[i-1].Range > 0 AND (Days[i].Range / Days[i-1].Range) > THRESHOLD_FACTOR_BREAKOUT:
        RETURN TRUE
    RETURN FALSE

// 2. Generate Entry Signal based on Breakout
// This function needs market-specific Volatility_Add_Factor and Volatility_Subtract_Factor
FUNCTION GenerateBreakoutEntry(Days, i, Volatility_Add_Factor_Buy, Volatility_Subtract_Factor_Sell):
    IF IsVolatilityBreakout(Days, i-1): // Breakout occurred on previous day (i-1)
        // Buy Signal: Add a percentage of previous day's range to current day's open
        Buy_Entry_Price_Today = Days[i].Open + (Days[i-1].Range * Volatility_Add_Factor_Buy)
        
        // Sell Signal: Subtract a percentage of previous day's range from current day's open
        Sell_Entry_Price_Today = Days[i].Open - (Days[i-1].Range * Volatility_Subtract_Factor_Sell)
        
        RETURN {TYPE_BUY_PRICE: Buy_Entry_Price_Today, TYPE_SELL_PRICE: Sell_Entry_Price_Today}
    RETURN NULL // No breakout signal

// Trading Strategy:
// - Use this as a mechanical entry technique, often combined with other filters (like TDW, TDM).
// - "Best point to add or subtract a volatility expansion value to is tomorrow's open." (Page 60)
//   So, entry is on Open[i] after breakout on Days[i-1].
```

---

## Simple Daily Range Breakouts (with TDW Filter)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 4: Simple Daily Range Breakouts (Page 61-64, Figures 4.1-4.7)
**Descrizione:** This trading model utilizes volatility breakouts as an entry signal, but significantly enhances performance by incorporating a "Trade Day of Week (TDW)" filter. The core entry rule is to buy on the current day's open plus 100% of the previous day's range, or sell on the current day's open minus 100% of the previous day's range. A flat dollar stop ($1,500 for bonds) and a "Bail Out" exit (first profitable opening after entry) are used. The TDW filter restricts trading to specific days of the week that statistically show higher profitability and lower drawdown for a given market, thereby increasing the strategy's accuracy and average profit per trade.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data (Open, High, Low, Close)
// Assume 'Range[i]' is Days[i].High - Days[i].Low
// Assume 'CurrentDayOfWeek' is an enumeration (MONDAY, TUESDAY, ..., FRIDAY)

// Parameters:
BONDS_STOP_LOSS = 1500 // Flat dollar stop for Bonds
BREAKOUT_RANGE_FACTOR = 1.0 // 100% of previous day's range

// TDW Filters for Bonds (derived from Figures 4.2-4.6 and Page 64):
BUY_DAYS_BONDS = {TUESDAY, THURSDAY}
SELL_DAYS_BONDS = {WEDNESDAY, THURSDAY} // Text implies Wednesday & Thursday for sells

// 1. Generate Entry Signal
FUNCTION GenerateSimpleDailyRangeBreakoutEntry(Days, i, CurrentDayOfWeek):
    IF i < 1: RETURN NULL

    // Buy Signal:
    IF CurrentDayOfWeek IN BUY_DAYS_BONDS:
        Buy_Entry_Price = Days[i].Open + (Days[i-1].Range * BREAKOUT_RANGE_FACTOR)
        RETURN {TYPE: BUY, PRICE: Buy_Entry_Price, STOP: BONDS_STOP_LOSS, EntryDayIndex: i}

    // Sell Signal:
    IF CurrentDayOfWeek IN SELL_DAYS_BONDS:
        Sell_Entry_Price = Days[i].Open - (Days[i-1].Range * BREAKOUT_RANGE_FACTOR)
        RETURN {TYPE: SELL, PRICE: Sell_Entry_Price, STOP: BONDS_STOP_LOSS, EntryDayIndex: i}
    
    RETURN NULL // No trade for this day

// 2. Exit Strategy ("Bailout" or Stop Loss)
FUNCTION BailoutExit(Position, Days, i):
    IF Position IS NOT OPEN: RETURN NULL

    // First check for Stop Loss
    IF (Position.Type == BUY AND Days[i].Low < Position.STOP) OR \
       (Position.Type == SELL AND Days[i].High > Position.STOP):
        EXECUTE_EXIT(Position.Type, Position.STOP) // Exit at stop price
        RETURN "STOP_LOSS_HIT"

    // Bailout (first profitable opening after entry)
    IF i > Position.EntryDayIndex: // Only consider after entry day
        IF (Position.Type == BUY AND Days[i].Open > Position.PRICE) OR \
           (Position.Type == SELL AND Days[i].Open < Position.PRICE):
            EXECUTE_EXIT(Position.Type, Days[i].Open)
            RETURN "BAILOUT_EXIT_PROFITABLE"

    RETURN NULL // Continue holding
```

---

## Greatest Swing Value (GSV)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 4: Separating Buyers from Sellers to Find Volatility Using Market Swings (Page 71-72), Chapter 8: Greatest Swing Value (Page 123-128, Figures 8.1-8.4)
**Descrizione:** The Greatest Swing Value (GSV) is a concept for measuring "failure swings" in the market to identify potential volatility expansions and trend reversals, by separating buying and selling pressure.
*   **Average Buy Swing:** Calculated as the average distance from the day's Open to the High, specifically on days that closed *below* the opening, over a lookback period (e.g., 4 days). This represents initial buying pressure that failed to sustain.
*   **Average Sell Swing:** Calculated as the average distance from the day's Open to the Low, specifically on days that closed *above* the opening, over a lookback period (e.g., 4 days). This represents initial selling pressure that failed to sustain.
These average "failure swings" are then multiplied by a factor (e.g., 180%) and used to project entry points from the next day's open, anticipating a volatility expansion in the confirmed direction.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data (Open, High, Low, Close)
// Assume 'Bonds' and 'Gold' are arrays of daily price data for intermarket filters
// Assume 'CurrentDayOfWeek' is an enumeration.

// Parameters:
N_SWING_DAYS_AVG = 4
SWING_FACTOR = 1.80 // 180%
BONDS_STOP_LOSS = 1600
S_P_STOP_LOSS = 2500

// 1. Calculate Average Buy Swing (from Open to High on down-close days)
FUNCTION CalculateAverageBuySwing(Days, i, N_days):
    sum_swings = 0; count = 0
    FOR j FROM i-N_days+1 TO i:
        IF Days[j].Close < Days[j].Open: // Day closed lower than open
            sum_swings += (Days[j].High - Days[j].Open)
            count++
    RETURN IF count > 0 THEN sum_swings / count ELSE 0

// 2. Calculate Average Sell Swing (from Open to Low on up-close days)
FUNCTION CalculateAverageSellSwing(Days, i, N_days):
    sum_swings = 0; count = 0
    FOR j FROM i-N_days+1 TO i:
        IF Days[j].Close > Days[j].Open: // Day closed higher than open
            sum_swings += (Days[j].Open - Days[j].Low)
            count++
    RETURN IF count > 0 THEN sum_swings / count ELSE 0

// Trading System Example (Bonds, Page 126-127):
// Setup Filters:
FUNCTION IsBondsBuySetup(Days, i, CurrentDayOfWeek):
    RETURN Days[i].Close < Days[i-5].Close AND \
           (CurrentDayOfWeek == TUESDAY OR CurrentDayOfWeek == WEDNESDAY OR CurrentDayOfWeek == FRIDAY)

// Buy Entry (Bonds):
IF IsBondsBuySetup(Days, i-1, CurrentDayOfWeek_Yesterday):
    avg_buy_swing = CalculateAverageBuySwing(Days, i-1, N_SWING_DAYS_AVG)
    Buy_Entry_Price = Days[i].Open + (avg_buy_swing * SWING_FACTOR)
    // Place buy order at Buy_Entry_Price
    // Stop Loss: BONDS_STOP_LOSS
    // Exit: First profitable opening after 2 days in trade (similar to bailout)

// Trading System Example (S&P 500, Page 124-125):
// Setup Filters:
FUNCTION IsSPBuySetup(Days, i, CurrentDayOfWeek, Bonds):
    RETURN Bonds[i].Close > Bonds[i-15].Close AND \
           (CurrentDayOfWeek == MONDAY OR CurrentDayOfWeek == TUESDAY OR CurrentDayOfWeek == WEDNESDAY) AND \
           Days[i].Close < Days[i-6].Close // S&P oversold criteria

FUNCTION IsSPSellSetup(Days, i, CurrentDayOfWeek, Bonds):
    RETURN Bonds[i].Close < Bonds[i-15].Close AND \
           (CurrentDayOfWeek != MONDAY) AND \
           Days[i].Close > Days[i-6].Close // S&P overbought criteria

// Buy Entry (S&P 500):
IF IsSPBuySetup(Days, i-1, CurrentDayOfWeek_Yesterday, Bonds):
    avg_buy_swing = CalculateAverageBuySwing(Days, i-1, N_SWING_DAYS_AVG)
    Buy_Entry_Price = Days[i].Open + (avg_buy_swing * SWING_FACTOR)
    // Stop Loss: S_P_STOP_LOSS
    // Exit: Bailout exit

// Sell Entry (S&P 500):
IF IsSPSellSetup(Days, i-1, CurrentDayOfWeek_Yesterday, Bonds):
    avg_sell_swing = CalculateAverageSellSwing(Days, i-1, N_SWING_DAYS_AVG)
    Sell_Entry_Price = Days[i].Open - (avg_sell_swing * SWING_FACTOR)
    // Stop Loss: S_P_STOP_LOSS
    // Exit: Bailout exit
```

---

## Trading Day of Week (TDW) Bias
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 6: The Market Is Not a Coin Flip (Page 82-87, Tables 6.1-6.4)
**Descrizione:** This technique leverages the observed non-randomness of market behavior based on the day of the week. Historical data shows consistent biases in daily trading ranges, open-to-close price changes, and net price changes for specific days. For instance, the S&P 500 often exhibits larger daily ranges on Tuesdays and Fridays and a positive open-to-close on Mondays, while Bonds tend to have large ranges on Thursdays and Fridays. This statistical edge (even if small, like a casino's edge) can be exploited by filtering trading signals from other systems, only taking trades on days that statistically favor the expected direction, thereby improving profitability and reducing drawdown.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data with DayOfWeek property
// Assume 'Signal' is a raw BUY or SELL signal from another trading system.

// 1. Historical Analysis (pre-calculated biases for specific markets):
// Example Biases (from Tables 6.1-6.4, Page 83-87):
// S&P 500:
//    - Mondays: Tendency for positive open-to-close change.
//    - Tuesdays/Fridays: Tendency for larger daily ranges.
// Bonds:
//    - Tuesdays: Largest positive open-to-close change.
//    - Thursdays/Fridays: Largest daily ranges.
// Grains:
//    - Wednesdays: Strong rallying pattern.

// 2. TDW Filter Function
FUNCTION ApplyTDWFilter(Signal, current_day_of_week, market_symbol):
    IF market_symbol == "S&P 500":
        IF Signal.Type == BUY:
            IF current_day_of_week == MONDAY: // Strongest open-to-close
                RETURN TRUE
            // Other days might be considered based on range data or other criteria
        ELSE IF Signal.Type == SELL:
            // S&P 500 Fridays had negative open-to-close value (Table 6.1)
            IF current_day_of_week == FRIDAY:
                RETURN TRUE
    ELSE IF market_symbol == "BONDS":
        IF Signal.Type == BUY:
            IF current_day_of_week == TUESDAY: // Strongest open-to-close
                RETURN TRUE
        ELSE IF Signal.Type == SELL:
            IF current_day_of_week == MONDAY OR current_day_of_week == THURSDAY: // Days with negative open-to-close
                RETURN TRUE
    ELSE IF market_symbol == "GRAINS":
        IF Signal.Type == BUY:
            IF current_day_of_week == WEDNESDAY: // Strong rallying pattern
                RETURN TRUE
    
    RETURN FALSE // Do not take trade if TDW bias is not favorable
```

---

## Trading Day of the Month (TDM) Bias
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 6: Monthly Road Maps (Page 88-92, Tables 6.6-6.7, Figures 6.4-6.6)
**Descrizione:** This technique identifies consistent market biases that occur on specific *trading days* of the month, rather than calendar days, thus accounting for non-trading days. These TDMs act as "setups" or "leading indicators" where the odds of a rally or decline are statistically tipped in the trader's favor. For example, specific TDMs are shown to be highly profitable for S&P 500 and T-Bonds, particularly towards the end and very beginning of the month. The author suggests using TDM biases in conjunction with other filters (like TDW and intermarket correlations) to create "stacked deck trades" with higher probability.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data, where each day has a 'TradingDayOfMonth' property (1 to 22 typically)
// Assume 'Signal' is a raw BUY or SELL signal from another trading system.

// 1. Historical Analysis (pre-calculated biases for specific markets):
// Example Biases (from Tables 6.6-6.7, Page 91):
// S&P 500:
//    - Highly profitable TDMs for BUY: 6, 7, 18, 19, 20, 21, 22.
//    - Poorer performing months to avoid (for month-end rally strategy): January, February, October (from Table 10.1, Page 149).
// Bonds:
//    - Highly profitable TDMs for BUY: 18, 20, 21, 22.
//    - TDM for SELL: 12 (from Figure 10.9, Page 155).
//    - Poorer performing months to avoid: January, February, April, October, (December potentially) (from Table 10.2, Page 150).

// 2. TDM Filter Function
FUNCTION ApplyTDMFilter(Signal, current_trading_day_of_month, current_month, market_symbol):
    IF market_symbol == "S&P 500":
        // Filter out poorer performing months for general month-end strategy
        IF current_month IN {JANUARY, FEBRUARY, OCTOBER}:
            RETURN FALSE // Avoid trading in these months for month-end rally
        
        IF Signal.Type == BUY:
            IF current_trading_day_of_month IN {6, 7, 18, 19, 20, 21, 22}: // Or specific range around month-end/start
                RETURN TRUE
        // Specific SELL TDMs for S&P 500 not explicitly detailed in table 6.6/6.7
    ELSE IF market_symbol == "BONDS":
        IF current_month IN {JANUARY, FEBRUARY, APRIL, OCTOBER}:
            RETURN FALSE // Avoid trading in these months for month-end rally
        
        IF Signal.Type == BUY:
            IF current_trading_day_of_month IN {18, 20, 21, 22}:
                RETURN TRUE
        ELSE IF Signal.Type == SELL:
            IF current_trading_day_of_month == 12:
                RETURN TRUE
    
    RETURN FALSE // Do not take trade if TDM bias is not favorable
```

---

## Pattern: Three Consecutive Down Closes (for Buy)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 7: The Common Element (Page 97)
**Descrizione:** This is a simple yet effective bullish pattern identified in the S&P 500. It suggests that after three consecutive days where the closing price is lower than the previous day's close, there is a statistical tendency for the market to move upwards. This pattern demonstrates that market behavior is not entirely random and can provide a tangible trading advantage, leading to higher accuracy and average profit per trade when buying on the subsequent open.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data (Open, High, Low, Close)

// Parameters:
STOP_LOSS = 3250 // Flat dollar stop for S&P 500

// Buy Setup: Three consecutive down closes
FUNCTION IsThreeConsecutiveDownCloses(Days, i):
    IF i < 3: RETURN FALSE // Need at least 3 previous days
    RETURN Days[i-1].Close < Days[i-2].Close AND \
           Days[i-2].Close < Days[i-3].Close AND \
           Days[i-3].Close < Days[i-4].Close // Using i-1 to i-4 for clarity of "three previous days"

// Trading Logic:
IF IsThreeConsecutiveDownCloses(Days, i-1): // Pattern completed on Day[i-1]
    Entry_Price = Days[i].Open // Buy on today's open (Day[i])
    
    // Place Buy Order at Entry_Price
    // Set Stop Loss: STOP_LOSS below Entry_Price
    
    Exit_Price = Days[i+1].Close // Exit on the next day's close (Day[i+1])
    // Close position at Exit_Price
```

---

## Pattern: Outside Day with Down Close + Lower Open (Bullish Reversal)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 7: The Common Element (Page 98-99, Figures 7.1-7.2)
**Descrizione:** This bullish reversal pattern is considered one of the author's favorites. It starts with an "outside day" (current day's range fully engulfs the previous day's range) that closes significantly lower, specifically below the previous day's low. This price action typically appears very bearish, inducing panic selling from the uninformed public. However, if the following day opens *lower* than the close of this outside down day, it signals an extreme emotional overreaction and sets up a high-probability buying opportunity, as the market is likely to reverse upwards.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data (Open, High, Low, Close)

// Parameters:
STOP_LOSS_SP = 2000 // Example stop loss for S&P 500

// 1. Identify Outside Day (Day X is Days[i-1])
FUNCTION IsOutsideDay(Days, i):
    IF i < 1: RETURN FALSE
    RETURN Days[i].High > Days[i-1].High AND Days[i].Low < Days[i-1].Low

// Buy Setup (for current day 'i', pattern occurred on 'i-1'):
FUNCTION GenerateBullishOutsideDayPattern(Days, i):
    IF i < 2: RETURN NULL // Need at least Day[i-2] and Day[i-1] for comparison

    // Condition 1: Previous day (i-1) was an outside day that closed below Day[i-2]'s low
    IF IsOutsideDay(Days, i-1) AND Days[i-1].Close < Days[i-2].Low:
        // Condition 2: Current day (i) opens lower than the previous day's (i-1) close
        IF Days[i].Open < Days[i-1].Close:
            Entry_Price = Days[i].Open // Buy on the open of Day[i]
            RETURN {TYPE: BUY, PRICE: Entry_Price, STOP: STOP_LOSS_SP, SignalDayHigh: Days[i-1].High, EntryDayIndex: i}
    RETURN NULL

// Exit Strategy (General, as specific exit not detailed for this pattern):
// - Use the set STOP_LOSS_SP.
// - Use Bailout exit (first profitable opening) or Hold to Close/Longer (as per Chapter 3/11).
```

---

## Smash Day Reversals
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 7: My Smash Day Patterns (Page 101-102, Figures 7.7-7.9)
**Descrizione:** Smash Day patterns represent rapid emotional market overreactions that create high-probability reversal trading opportunities.
*   **Smash Day Buy Setup:** Occurs when a day (Day X) closes *lower* than the low of the previous day (Day X-1), often breaking below multiple prior lows (a "naked close" down). This appears to be a strong bearish breakout, attracting public selling. A buy signal is generated if, on the very next day (Day X+1), the price trades *above* the high of Day X. This signifies a failed bearish breakout and an immediate reversal to the upside, trapping late sellers.
*   **Smash Day Sell Setup:** Occurs when a day (Day X) closes *above* the high of the previous day (Day X-1), often breaking above multiple prior highs (a "naked close" up). This appears to be a strong bullish breakout, attracting public buying. A sell signal is generated if, on the very next day (Day X+1), the price trades *below* the low of Day X. This signifies a failed bullish breakout and an immediate reversal to the downside, trapping late buyers.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data (Open, High, Low, Close)
// Assume 'TICKET_SIZE' is a small value to enter slightly above/below trigger.

// Smash Day Buy Setup (Day X is Days[i-1]):
FUNCTION IsSmashDayBuySetup(Days, i):
    IF i < 2: RETURN FALSE
    // Previous day (i-1) closes below the low of the day before (i-2)
    RETURN Days[i-1].Close < Days[i-2].Low

// Smash Day Sell Setup (Day X is Days[i-1]):
FUNCTION IsSmashDaySellSetup(Days, i):
    IF i < 2: RETURN FALSE
    // Previous day (i-1) closes above the high of the day before (i-2)
    RETURN Days[i-1].Close > Days[i-2].High

// Trading Logic:
// For Buy Signal (Reversal after Smash Down Day):
IF IsSmashDayBuySetup(Days, i): // Pattern completed on Days[i-1]
    // Entry when price trades above the high of the Smash Down Day (i-1)
    IF Days[i].High > Days[i-1].High:
        Entry_Price = Days[i-1].High + TICKET_SIZE // Buy slightly above High[i-1]
        RETURN {TYPE: BUY, PRICE: Entry_Price, EntryDayIndex: i}

// For Sell Signal (Reversal after Smash Up Day):
IF IsSmashDaySellSetup(Days, i): // Pattern completed on Days[i-1]
    // Entry when price trades below the low of the Smash Up Day (i-1)
    IF Days[i].Low < Days[i-1].Low:
        Entry_Price = Days[i-1].Low - TICKET_SIZE // Sell short slightly below Low[i-1]
        RETURN {TYPE: SELL, PRICE: Entry_Price, EntryDayIndex: i}

// Stop Loss and Take Profit not explicitly defined here; apply general rules (Chapter 11).
```

---

## Hidden Smash Day Reversals
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 7: My Smash Day Patterns (Page 102-104, Figures 7.10-7.11)
**Descrizione:** Hidden Smash Days are more nuanced reversal patterns than the explicit Smash Days, focusing on intraday closing strength relative to the open and range.
*   **Hidden Smash Day Buy Setup:** Occurs on a day (Day X) that has an *up close* (Close > Open) but the closing price is in the *lower 25%* of the day's total range. This implies that despite an overall gain, buying pressure couldn't sustain the high, potentially trapping buyers who entered late or expected continued strength. A buy signal is triggered if the next day (Day X+1) trades *above* the high of Day X, indicating a failed bearish follow-through and a bullish reversal.
*   **Hidden Smash Day Sell Setup:** Occurs on a day (Day X) that has a *down close* (Close < Open) but the closing price is in the *upper 25%* of the day's total range. This implies that despite an overall loss, selling pressure couldn't maintain the low, potentially trapping sellers. A sell signal is triggered if the next day (Day X+1) trades *below* the low of Day X, indicating a failed bullish follow-through and a bearish reversal.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data (Open, High, Low, Close)
// Assume Range[i] = Days[i].High - Days[i].Low
// Assume 'TICKET_SIZE' is a small value to enter slightly above/below trigger.

// Hidden Smash Day Buy Setup (Day X is Days[i-1]):
FUNCTION IsHiddenSmashDayBuySetup(Days, i):
    IF i < 1: RETURN FALSE
    RETURN Days[i-1].Close > Days[i-1].Open AND \
           (Days[i-1].Close - Days[i-1].Low) / Days[i-1].Range <= 0.25

// Hidden Smash Day Sell Setup (Day X is Days[i-1]):
FUNCTION IsHiddenSmashDaySellSetup(Days, i):
    IF i < 1: RETURN FALSE
    RETURN Days[i-1].Close < Days[i-1].Open AND \
           (Days[i-1].Close - Days[i-1].Low) / Days[i-1].Range >= 0.75

// Trading Logic:
// For Buy Signal (after Hidden Smash Down Day):
IF IsHiddenSmashDayBuySetup(Days, i): // Pattern completed on Days[i-1]
    // Entry when price trades above the high of the Hidden Smash Day (i-1)
    IF Days[i].High > Days[i-1].High:
        Entry_Price = Days[i-1].High + TICKET_SIZE // Buy slightly above Days[i-1].High
        RETURN {TYPE: BUY, PRICE: Entry_Price, EntryDayIndex: i}

// For Sell Signal (after Hidden Smash Up Day):
IF IsHiddenSmashDaySellSetup(Days, i): // Pattern completed on Days[i-1]
    // Entry when price trades below the low of the Hidden Smash Day (i-1)
    IF Days[i].Low < Days[i-1].Low:
        Entry_Price = Days[i-1].Low - TICKET_SIZE // Sell short slightly below Days[i-1].Low
        RETURN {TYPE: SELL, PRICE: Entry_Price, EntryDayIndex: i}

// Stop Loss and Take Profit not explicitly defined here; apply general rules (Chapter 11).
```

---

## Specialists' Trap (False Breakout Reversal)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 7: Specialists' Trap (Page 108-113, Figures 7.18-7.25)
**Descrizione:** The Specialists' Trap identifies false breakouts that lure uninformed traders into taking positions just before a market reversal. These patterns are based on the idea of a "collective consciousness" drawing the public into the game at the wrong times.
*   **Selling Trap (Bearish Reversal / Sell Signal):** Occurs in an uptrending market after 5-10 days of sideways consolidation. A "breakout day" (Day B) sees price close *above* the entire prior 5-10 day trading range (a "naked close" up). The public typically buys this upside breakout. A *sell signal* is generated if, within the next 1-3 days, price then drops *below* the actual low of Day B. This signifies a false breakout, trapping buyers, and indicates an imminent downward reversal.
*   **Buy Trap (Bullish Reversal / Buy Signal):** Occurs in a downtrending market after 5-10 days of sideways consolidation. A "breakout day" (Day B) sees price close *below* the entire prior 5-10 day trading range (a "naked close" down). The public typically sells this downside breakout. A *buy signal* is generated if, within the next 1-3 days, price then rallies *above* the actual high of Day B. This signifies a false breakdown, trapping sellers, and indicates an imminent upward reversal.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data (Open, High, Low, Close)
// Assume 'N_CONSOLIDATION_DAYS' = 5 to 10
// Assume 'N_REVERSAL_DAYS' = 1 to 3
// Assume 'TICKET_SIZE' is a small value to enter slightly above/below trigger.

// 1. Identify Consolidation Range (High/Low of last N_CONSOLIDATION_DAYS)
FUNCTION GetConsolidationRange(Days, current_day_index, N_days):
    IF current_day_index < N_days: RETURN NULL
    max_high = MAX(Days[j].High for j in [current_day_index-N_days to current_day_index-1])
    min_low = MIN(Days[j].Low for j in [current_day_index-N_days to current_day_index-1])
    RETURN {MaxHigh: max_high, MinLow: min_low}

// Selling Trap (Bearish Reversal):
FUNCTION DetectSellingTrap(Days, i): // Signal bar is Days[i]
    IF i < N_CONSOLIDATION_DAYS + N_REVERSAL_DAYS: RETURN NULL

    consolidation = GetConsolidationRange(Days, i, N_CONSOLIDATION_DAYS)
    IF consolidation == NULL: RETURN NULL

    // Condition 1: Breakout Day (Days[i-N_REVERSAL_DAYS-1]) - Close above consolidation range
    // Let's denote the breakout day as 'B' and subsequent days as 'k'.
    breakout_day_index = i - N_REVERSAL_DAYS - 1
    IF breakout_day_index < 0: RETURN NULL

    IF Days[breakout_day_index].Close > consolidation.MaxHigh AND Days[breakout_day_index].Close > Days[breakout_day_index-1].High: // Naked close upside breakout
        // Condition 2: Subsequent day(s) (k) take out the Low of the breakout day
        FOR k FROM breakout_day_index + 1 TO i:
            IF Days[k].Low < Days[breakout_day_index].Low: // Trap is set, breakout failed
                Entry_Price = Days[breakout_day_index].Low - TICKET_SIZE // Sell short slightly below Breakout Day's Low
                RETURN {TYPE: SELL, PRICE: Entry_Price, EntryDayIndex: i}
    RETURN NULL

// Buy Trap (Bullish Reversal):
FUNCTION DetectBuyTrap(Days, i): // Signal bar is Days[i]
    IF i < N_CONSOLIDATION_DAYS + N_REVERSAL_DAYS: RETURN NULL

    consolidation = GetConsolidationRange(Days, i, N_CONSOLIDATION_DAYS)
    IF consolidation == NULL: RETURN NULL

    // Condition 1: Breakout Day (Days[i-N_REVERSAL_DAYS-1]) - Close below consolidation range
    breakout_day_index = i - N_REVERSAL_DAYS - 1
    IF breakout_day_index < 0: RETURN NULL

    IF Days[breakout_day_index].Close < consolidation.MinLow AND Days[breakout_day_index].Close < Days[breakout_day_index-1].Low: // Naked close downside breakdown
        // Condition 2: Subsequent day(s) (k) take out the High of the breakout day
        FOR k FROM breakout_day_index + 1 TO i:
            IF Days[k].High > Days[breakout_day_index].High: // Trap is set, breakdown failed
                Entry_Price = Days[breakout_day_index].High + TICKET_SIZE // Buy slightly above Breakout Day's High
                RETURN {TYPE: BUY, PRICE: Entry_Price, EntryDayIndex: i}
    RETURN NULL

// Stop Loss and Take Profit not explicitly defined here; apply general rules (Chapter 11).
```

---

## Oops! Pattern (Gap Reversal)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 7: Oops! This Is Not a Mistake (Page 113-121, Figures 7.26-7.35)
**Descrizione:** The "Oops!" pattern identifies emotional market overreactions characterized by significant price gaps at the opening, which subsequently reverse. It's named "Oops!" because the public often pitches their positions based on news or charts, only to realize they were wrong as the market reverses.
*   **Oops! Buy Signal:** Occurs when the market opens *below* the previous day's low (`Open[i] < Low[i-1]`). This indicates extreme selling pressure or panic. A buy entry is triggered when the price then rallies back up to the previous day's low (`Low[i-1]`), suggesting the selling pressure has abated and a bullish reversal is underway.
*   **Oops! Sell Signal:** Occurs when the market opens *above* the previous day's high (`Open[i] > High[i-1]`). This indicates extreme buying pressure or euphoria. A sell entry is triggered when the price then falls back down to the previous day's high (`High[i-1]`), suggesting the buying pressure has failed and a bearish reversal is underway.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data (Open, High, Low, Close)
// Assume 'CurrentPrice' is the real-time or bar-by-bar price (for entry trigger)
// Assume 'SMA(data, period)' is a Simple Moving Average function
// Assume 'CurrentDayOfWeek' and 'TradingDayOfMonth' are available.

// Parameters for general Oops! Trading:
S_P_STOP_LOSS = 2000 // For S&P 500
BONDS_STOP_LOSS_BUY = 1800 // For Bonds buy
BONDS_STOP_LOSS_SELL = 1000 // For Bonds sell
N_DAY_SMA = 9 // For 9-day moving average filter

// 1. Detect Oops! Setup
FUNCTION DetectOopsBuySetup(Days, i):
    IF i < 1: RETURN FALSE
    RETURN Days[i].Open < Days[i-1].Low // Current day opens below previous day's low

FUNCTION DetectOopsSellSetup(Days, i):
    IF i < 1: RETURN FALSE
    RETURN Days[i].Open > Days[i-1].High // Current day opens above previous day's high

// 2. Trading Logic for Oops! Buy:
IF DetectOopsBuySetup(Days, i):
    // Entry condition: Price rallies back to previous day's low
    IF CurrentPrice >= Days[i-1].Low:
        Entry_Price = Days[i-1].Low // Buy at or around previous day's low
        
        // Apply Filters (Examples from text):
        // S&P 500: Buy on any day EXCEPT Wednesday or Thursday (Page 117)
        // Bonds: Buy on any day EXCEPT Wednesday (Page 119)
        // S&P 500 (Downtrend/Oversold): Buy on Tuesday, Wednesday, or Friday if SMA(9) is in downtrend (Page 122)
        // Bonds (Oversold): Buy on any day but Thursday if SMA(9) on Friday < SMA(9) on Thursday (Page 121)
        
        // Stop Loss and Exit (Examples from text):
        // S&P 500: $2000 stop, Exit on next day's opening (Page 117)
        // Bonds: $1800 stop, Bailout exit (Page 119)
        // Filtered Bonds: $1400 stop, Exit close on first profitable opening after 3 days (Page 121)
        RETURN {TYPE: BUY, PRICE: Entry_Price, EntryDayIndex: i}

// 3. Trading Logic for Oops! Sell:
IF DetectOopsSellSetup(Days, i):
    // Entry condition: Price falls back to previous day's high
    IF CurrentPrice <= Days[i-1].High:
        Entry_Price = Days[i-1].High // Sell at or around previous day's high
        
        // Apply Filters (Examples from text):
        // Bonds: Sell on Wednesday (Page 119)
        // Filtered Bonds: Sell on Wednesday if SMA(9) on Tuesday > SMA(9) on Monday (overbought Bonds) (Page 121)

        // Stop Loss and Exit (Examples from text):
        // Bonds: $1000 stop, 4-day bailout (Page 119)
        // Filtered Bonds: $1400 stop, Exit close on first profitable opening after 3 days (Page 121)
        RETURN {TYPE: SELL, PRICE: Entry_Price, EntryDayIndex: i}
```

---

## Swing Points as Trend Change Indication
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 9: Swing Points as Trend Change Indication (Page 134-135, Figures 9.2-9.4)
**Descrizione:** This technique uses the identification of short-term pivot highs and lows (as defined in Chapter 1) to signal trend changes. It focuses on the sequential formation of these swing points, aiming to identify shifts in market direction early.
*   **Bullish Trend Change (Buy Signal):** Occurs when the market forms a *higher low* (L2 > L1) and subsequently rallies to break *above* the previous swing high (H1) that occurred between L1 and L2. This pattern is considered a strong indication for a real trend reversal to the upside.
*   **Bearish Trend Change (Sell Signal):** Occurs when the market forms a *lower high* (H2 < H1) and subsequently declines to break *below* the previous swing low (L1) that occurred between H1 and H2.
This method allows traders to align with emerging trends for significant price moves, and can be combined with other filters like TDW and TDM.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'SwingLows' and 'SwingHighs' are lists of identified short-term pivot points (index and value).
// Assume 'Days' is an array of daily price data (Open, High, Low, Close)
// Assume 'TICKET_SIZE' is a small value for entry offset.

// Bullish Trend Change (from Figure 9.2 A):
FUNCTION DetectBullishTrendChange(Days, SwingLows, SwingHighs, current_index):
    IF SwingLows.Length < 2 OR SwingHighs.Length < 1: RETURN NULL // Not enough swing points

    // Get the most recent L1, H1, L2
    L1 = SwingLows[SwingLows.Length-2]
    H1 = SwingHighs[SwingHighs.Length-1] // Most recent high (could be between L1 and L2 or after L2)
    L2 = SwingLows[SwingLows.Length-1]

    // Ensure sequence L1 -> H1 -> L2 where L2 is a higher low
    // This requires H1 to be formed AFTER L1 and BEFORE L2, and L2 is the most recent low
    // Simplified: Look for L1 < L2, and then a break of H1 which is between L1 and L2
    // We need to re-evaluate the actual H1 that corresponds to the L1-L2 pair.
    
    // Find H1 that is between L1 and L2
    found_h1_between = NULL
    FOR k FROM L1.Index + 1 TO L2.Index - 1:
        IF IdentifyShortTermHigh(Days, k): // Assuming IdentifyShortTermHigh returns the pivot point
            IF Days[k].Value > H1.Value: // This should be the highest high between L1 and L2
                found_h1_between = {Index: k, Value: Days[k].Value}
    
    // If no explicit H1 found between L1 and L2, we use the last identified high before L2.
    IF L2.Value > L1.Value: // Condition for Higher Low
        // Check for price breaking above the highest high before L2 (H1)
        IF Days[current_index].High > H1.Value: // current_index is the new bar where breakout occurs
            Entry_Price = H1.Value + TICKET_SIZE // Buy slightly above H1
            RETURN {TYPE: BUY, PRICE: Entry_Price, TriggerHigh: H1.Value, TriggerLow: L1.Value, CurrentLow: L2.Value}
    RETURN NULL

// Bearish Trend Change (Symmetric to Bullish):
FUNCTION DetectBearishTrendChange(Days, SwingLows, SwingHighs, current_index):
    IF SwingHighs.Length < 2 OR SwingLows.Length < 1: RETURN NULL

    H1 = SwingHighs[SwingHighs.Length-2]
    L1 = SwingLows[SwingLows.Length-1]
    H2 = SwingHighs[SwingHighs.Length-1]

    // Find L1 that is between H1 and H2 (not explicitly in diagram B but implied by symmetry)
    // Simplified: Look for H1 > H2, and then a break of L1 which is between H1 and H2
    
    IF H2.Value < H1.Value: // Condition for Lower High
        // Check for price breaking below the lowest low before H2 (L1)
        IF Days[current_index].Low < L1.Value: // current_index is the new bar where breakdown occurs
            Entry_Price = L1.Value - TICKET_SIZE // Sell short slightly below L1
            RETURN {TYPE: SELL, PRICE: Entry_Price, TriggerLow: L1.Value, TriggerHigh: H1.Value, CurrentHigh: H2.Value}
    RETURN NULL

// Filters: Combine with TDW, TDM, secondary data (intermarket correlations).
```

---

## The Three-Bar High/Low System
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 9: The Three-Bar High/Low System (Page 136-138, Figures 9.5-9.6)
**Descrizione:** This short-term trading strategy employs a simple moving average of the highs and a simple moving average of the lows, each calculated over a 3-bar period. It is designed to trade pullbacks within an established trend.
*   **Buy Signal:** When an uptrend is identified (e.g., using the Swing Point Trend Change technique), a buy entry is made at the price of the 3-bar moving average of the lows. This allows buying on dips within the uptrend.
*   **Sell Signal:** When a downtrend is identified, a sell short entry is made at the price of the 3-bar moving average of the highs. This allows selling rallies within the downtrend.
*   **Profit Taking:** Profits are taken when the price reaches the opposite 3-bar moving average (e.g., for a buy, take profit at the 3-bar moving average of the highs). The system works across various intraday timeframes (5-minute to 60-minute bars).
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Bars' is an array of price data (Open, High, Low, Close) for a chosen timeframe (e.g., 15-minute)
// Assume 'IsUptrend(Bars, i)' and 'IsDowntrend(Bars, i)' functions are available from Swing Points Trend Change or other trend identification method.

// 1. Calculate 3-Bar Moving Average of Highs
FUNCTION MA_High_3(Bars, i):
    IF i < 2: RETURN NULL
    RETURN (Bars[i].High + Bars[i-1].High + Bars[i-2].High) / 3

// 2. Calculate 3-Bar Moving Average of Lows
FUNCTION MA_Low_3(Bars, i):
    IF i < 2: RETURN NULL
    RETURN (Bars[i].Low + Bars[i-1].Low + Bars[i-2].Low) / 3

// Trading Logic:
// Buy Entry:
IF IsUptrend(Bars, i):
    Entry_Price = MA_Low_3(Bars, i)
    // Place Buy Limit Order at Entry_Price
    // Stop Loss (e.g., below a recent swing low or fixed dollar stop)
    // Take Profit Target: MA_High_3(Bars, i) (or subsequent MA_High_3 values as trend continues)
    RETURN {TYPE: BUY, Entry: Entry_Price, TakeProfitTarget: MA_High_3(Bars, i)}

// Sell Entry:
IF IsDowntrend(Bars, i):
    Entry_Price = MA_High_3(Bars, i)
    // Place Sell Short Limit Order at Entry_Price
    // Stop Loss (e.g., above a recent swing high or fixed dollar stop)
    // Take Profit Target: MA_Low_3(Bars, i) (or subsequent MA_Low_3 values as trend continues)
    RETURN {TYPE: SELL, Entry: Entry_Price, TakeProfitTarget: MA_Low_3(Bars, i)}
```

---

## Will-Spread Index (Intermarket Momentum)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 9: A New Indicator for Short-Term Traders: Will-Tell (Page 138-143, Figures 9.7-9.10)
**Descrizione:** The Will-Spread Index is a causative indicator designed to measure the relative strength or weakness between a primary market (the one being traded) and a secondary, influencing market (e.g., Bonds for Gold, or T-Bills/Bonds for S&P 500). It helps to understand inner-market influences and identify underlying trends.
**Calculation:**
1.  **Spread:** `Spread[i] = (Primary_Market_Close[i] / Secondary_Market_Close[i]) * 100`
2.  **Will-Spread Indicator:** A MACD-like calculation: `EMA(Spread, Short_Period) - EMA(Spread, Long_Period)`. The author specifies 3-period EMA minus 15-period EMA for 30-minute S&P bars.

**Trading Signals:**
*   **Buy Signal:** When the Will-Spread indicator crosses from negative territory (below 0) to positive territory (above 0).
*   **Confirmation for Buy:** The author prefers to wait for the *next* trading bar (after the cross-up) to rally *above* the high of the bar where the positive crossing occurred.
*   **Sell Signal:** When the Will-Spread indicator crosses from positive territory (above 0) to negative territory (below 0).
*   **Confirmation for Sell:** The author prefers to wait for the *next* trading bar (after the cross-down) to fall *below* the low of the bar where the negative crossing occurred.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'PrimaryMarket' and 'SecondaryMarket' are arrays of price data (e.g., Close)
// Assume 'EMA(data, period)' is a function for Exponential Moving Average

// Parameters:
SHORT_EMA_PERIOD = 3   // For 30-minute S&P bars
LONG_EMA_PERIOD = 15   // For 30-minute S&P bars
TICKET_SIZE = 0.01     // Small offset for entry from confirmation level

// 1. Calculate the Spread
FUNCTION CalculateSpread(PrimaryMarketClose, SecondaryMarketClose):
    IF SecondaryMarketClose == 0: RETURN NULL // Avoid division by zero
    RETURN (PrimaryMarketClose / SecondaryMarketClose) * 100

// 2. Calculate the Will-Spread Indicator series
FUNCTION GetWillSpreadSeries(PrimaryMarket, SecondaryMarket, current_index, short_ema_period, long_ema_period):
    spread_values = []
    FOR j FROM 0 TO current_index:
        spread = CalculateSpread(PrimaryMarket[j].Close, SecondaryMarket[j].Close)
        IF spread != NULL: spread_values.ADD(spread)
    
    IF spread_values.Length < long_ema_period: RETURN NULL
    
    ema_short_series = EMA(spread_values, short_ema_period)
    ema_long_series = EMA(spread_values, long_ema_period)
    
    will_spread_series = []
    FOR k FROM 0 TO ema_short_series.Length - 1:
        will_spread_series.ADD(ema_short_series[k] - ema_long_series[k])
    RETURN will_spread_series

// Trading Logic:
// Assume 'CurrentIndex' is the index of the most recent complete bar.
will_spread_values = GetWillSpreadSeries(PrimaryMarket, SecondaryMarket, CurrentIndex, SHORT_EMA_PERIOD, LONG_EMA_PERIOD)
IF will_spread_values == NULL OR will_spread_values.Length < 2: RETURN NULL

current_will_spread = will_spread_values[will_spread_values.Length-1]
previous_will_spread = will_spread_values[will_spread_values.Length-2]

// Buy Signal:
IF current_will_spread > 0 AND previous_will_spread <= 0: // Cross above zero
    // Confirmation: Next bar rallies above the high of the current bar (CurrentIndex)
    IF PrimaryMarket[CurrentIndex+1].High > PrimaryMarket[CurrentIndex].High: // Check next bar's high
        Entry_Price = PrimaryMarket[CurrentIndex].High + TICKET_SIZE // Buy above the signal bar's high
        RETURN {TYPE: BUY, PRICE: Entry_Price, SignalBarIndex: CurrentIndex}

// Sell Signal:
IF current_will_spread < 0 AND previous_will_spread >= 0: // Cross below zero
    // Confirmation: Next bar falls below the low of the current bar (CurrentIndex)
    IF PrimaryMarket[CurrentIndex+1].Low < PrimaryMarket[CurrentIndex].Low: // Check next bar's low
        Entry_Price = PrimaryMarket[CurrentIndex].Low - TICKET_SIZE // Sell short below the signal bar's low
        RETURN {TYPE: SELL, PRICE: Entry_Price, SignalBarIndex: CurrentIndex}
```

---

## Month-End Trading (Stock Indexes)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 10: Month-End Trading in Stock Indexes (Page 147-149, Figure 10.1, Table 10.1)
**Descrizione:** This strategy exploits a historical bias in stock indexes (like the S&P 500) to rally around the first trading day of each month. The primary rule is to enter a long position on the opening of the first trading day of the month. Performance can be significantly improved by filtering these trades: only take a buy signal if the Bond market shows supportive strength (i.e., Bonds closed higher yesterday than 30 days ago). The author also identifies poorer performing months (January, February, October) which should be avoided or approached with caution.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days' is an array of daily price data for S&P 500 (Open_SP, Close_SP)
// Assume 'Bonds' is an array of daily price data for Bonds (Close_B)
// Assume 'IsFirstTradingDayOfMonth(index)' is a function returning true if Days[index] is the first trading day of its month.
// Assume 'GetMonth(date)' returns the month (1-12).

// Parameters:
S_P_STOP_LOSS = 1500 // Flat dollar stop for S&P 500

// Months to Avoid for this strategy (based on Table 10.1):
AVOID_MONTHS = {1, 2, 10} // January, February, October

// Entry Logic:
FUNCTION GenerateMonthEndStockBuySignal(Days_SP, Bonds, i):
    IF IsFirstTradingDayOfMonth(i):
        current_month = GetMonth(Days_SP[i].Date)
        IF current_month IN AVOID_MONTHS:
            RETURN NULL // Skip trade in poorer performing months

        // Filter: Bonds closed higher yesterday than 30 days ago (supportive Bond market)
        IF i >= 31 AND Bonds[i-1].Close > Bonds[i-31].Close:
            Entry_Price = Days_SP[i].Open // Buy S&P 500 on the open
            RETURN {TYPE: BUY, PRICE: Entry_Price, STOP: S_P_STOP_LOSS, EntryDayIndex: i}
    RETURN NULL

// Exit Logic (from Page 148, similar to "Bailout" rule):
FUNCTION ExitMonthEndStockTrade(Position, Days_SP, i):
    IF Position IS NOT OPEN: RETURN NULL

    // First check for Stop Loss
    IF (Position.Type == BUY AND Days_SP[i].Low < Position.STOP):
        EXECUTE_EXIT(Position.Type, Position.STOP) // Exit at stop price
        RETURN "STOP_LOSS_HIT"

    // Exit on the first profitable opening after entry.
    IF i > Position.EntryDayIndex: // Only consider after entry day
        IF (Position.Type == BUY AND Days_SP[i].Open > Position.PRICE):
            EXECUTE_EXIT(Position.Type, Days_SP[i].Open)
            RETURN "BAILOUT_EXIT_PROFITABLE"

    RETURN NULL // Continue holding
```

---

## Month-End Trading (Bond Market)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 10: Month-End Trading in the Bond Market (Page 149-154, Figure 10.2, Tables 10.2)
**Descrizione:** This strategy capitalizes on the historical tendency for the Bond market to rally around the first trading day of each month.
**Primary Buy Rule:** Buy Bonds on the open of the first trading day of every month.
**Filters and Enhancements:**
1.  **Month Exclusion:** Exclude poorer performing months based on historical data (January, February, April, October, and sometimes December).
2.  **Delayed Entry (TDM 22):** An improved variant suggests delaying entry until the 22nd trading day of the month for even better accuracy and average profit per trade.
3.  **Gold Trend Confirmation:** For TDM 22 buy signals, add a fundamental filter: only take the trade if Gold has closed *lower* than 24 days ago, indicating a downtrend in Gold (which is bullish for Bonds).
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days_B' is an array of daily price data for Bonds (Open_B, Close_B)
// Assume 'Gold' is an array of daily price data for Gold (Close_G)
// Assume 'IsFirstTradingDayOfMonth(index)' and 'GetTradingDayOfMonth(index)' are functions.
// Assume 'GetMonth(date)' returns the month (1-12).

// Parameters:
BONDS_STOP_LOSS_PRIMARY = 1100
BONDS_STOP_LOSS_TDM22_GOLD = 1500 // Note text says $1500 drawdown and improved accuracy, implies same stop as $1100

// Months to Avoid for primary strategy (based on Table 10.2):
AVOID_MONTHS = {1, 2, 4, 10} // January, February, April, October (December is marginal)

// Primary Rule (First Trading Day of Month Buy):
FUNCTION GenerateFirstTDM_BondBuySignal(Days_B, i):
    IF IsFirstTradingDayOfMonth(i):
        current_month = GetMonth(Days_B[i].Date)
        IF current_month IN AVOID_MONTHS:
            RETURN NULL
        
        Entry_Price = Days_B[i].Open // Buy Bonds on the open
        RETURN {TYPE: BUY, PRICE: Entry_Price, STOP: BONDS_STOP_LOSS_PRIMARY, EntryDayIndex: i}
    RETURN NULL

// Enhanced Rule (TDM 22 Buy Signal backed by Gold):
FUNCTION GenerateTDM22_BondBuySignal(Days_B, Gold, i):
    IF GetTradingDayOfMonth(i) == 22:
        // Gold Trend Confirmation: Gold closed lower than 24 days ago (downtrend in Gold)
        IF i >= 25 AND Gold[i-1].Close < Gold[i-25].Close: // Gold[i-25] is 24 days ago
            Entry_Price = Days_B[i].Open // Buy Bonds on the open
            RETURN {TYPE: BUY, PRICE: Entry_Price, STOP: BONDS_STOP_LOSS_TDM22_GOLD, EntryDayIndex: i}
    RETURN NULL

// Exit Logic (from Page 149, similar to "Bailout" rule):
FUNCTION ExitMonthEndBondTrade(Position, Days_B, i):
    IF Position IS NOT OPEN: RETURN NULL

    // First check for Stop Loss
    IF (Position.Type == BUY AND Days_B[i].Low < Position.STOP):
        EXECUTE_EXIT(Position.Type, Position.STOP)
        RETURN "STOP_LOSS_HIT"

    // Exit on the first profitable opening after entry.
    IF i > Position.EntryDayIndex:
        IF (Position.Type == BUY AND Days_B[i].Open > Position.PRICE):
            EXECUTE_EXIT(Position.Type, Days_B[i].Open)
            RETURN "BAILOUT_EXIT_PROFITABLE"
    RETURN NULL
```

---

## Month-Mid Sell (Bond Market)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 10: A Time to Sell as Well (Page 154-156, Figure 10.9, 10.10)
**Descrizione:** This strategy identifies a historical tendency for the Bond market to experience a dip around the 12th trading day of the month (TDM 12), presenting a short-selling opportunity.
**Primary Sell Rule:** Sell Bonds on the open of TDM 12.
**Filters and Enhancements:**
*   **Gold Trend Confirmation:** For TDM 12 sell signals, add a fundamental filter: only take the trade if Gold has closed *greater* than 10 days ago, indicating an uptrend in Gold (which is fundamentally bearish for Bonds). This significantly improves the average profit per trade and reduces drawdown. The trade is typically held for 3 days.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days_B' is an array of daily price data for Bonds (Open_B, Close_B)
// Assume 'Gold' is an array of daily price data for Gold (Close_G)
// Assume 'GetTradingDayOfMonth(index)' is a function.

// Parameters:
BONDS_TDM12_SELL_STOP_LOSS = 1400
HOLDING_PERIOD_DAYS = 3

// Sell Signal:
FUNCTION GenerateTDM12_BondSellSignal(Days_B, Gold, i):
    IF GetTradingDayOfMonth(i) == 12:
        // Gold Trend Confirmation: Gold closed higher than 10 days ago (uptrend in Gold)
        IF i >= 11 AND Gold[i-1].Close > Gold[i-11].Close: // Gold[i-11] is 10 days ago
            Entry_Price = Days_B[i].Open // Sell short Bonds on the open
            RETURN {TYPE: SELL, PRICE: Entry_Price, STOP: BONDS_TDM12_SELL_STOP_LOSS, EntryDayIndex: i}
    RETURN NULL

// Exit Logic:
FUNCTION ExitTDM12_BondSellTrade(Position, Days_B, i):
    IF Position IS NOT OPEN: RETURN NULL

    // First check for Stop Loss
    IF (Position.Type == SELL AND Days_B[i].High > Position.STOP):
        EXECUTE_EXIT(Position.Type, Position.STOP)
        RETURN "STOP_LOSS_HIT"

    // Exit after fixed holding period
    IF (i - Position.EntryDayIndex) >= HOLDING_PERIOD_DAYS:
        EXECUTE_EXIT(Position.Type, Days_B[i].Close) // Exit at close after holding period
        RETURN "FIXED_PERIOD_EXIT"
    
    RETURN NULL // Continue holding
```

---

## General Exit Rules (Stop Loss, Bailout, Reverse)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 11: When to Get Out of Your Trades (Page 157)
**Descrizione:** This section outlines three fundamental rules for managing trade exits, emphasizing capital preservation and responsiveness to market signals over emotional holding or greed.
1.  **Dollar Stop:** Always use a predefined dollar stop loss to protect capital from unexpected market moves.
2.  **"Bailout" Profit-Taking:** A strategy to secure profits by exiting a trade on the *first profitable opening* after entry. For faster markets (like the S&P), even a minimal profit (one tick) is reason to exit. For slower markets, a slight delay (one or two days) may be applied to allow more profit to accrue.
3.  **Exit and Reverse on Opposite Signal:** If a new, clear signal is generated that directly contradicts the current position (e.g., a strong sell signal while holding a long), the existing position should be immediately closed and the new, opposite position taken, overriding any other stop or profit-taking rules.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'CurrentPosition' holds details: {Type: BUY/SELL, EntryPrice, EntryDayIndex, DollarStopAmount}
// Assume 'CurrentMarketPrice' is the real-time or end-of-bar price
// Assume 'CurrentDay.Open' is the opening price of the current day
// Assume 'NewOppositeSignal' is a boolean flag indicating a new, conflicting trade signal.
// Assume 'Entry_Price_for_New_Signal' is the calculated entry price if reversing.

// Rule 1: Always use a dollar stop on all trades
FUNCTION ApplyDollarStop(CurrentPosition, CurrentMarketPrice, CurrentDayLow, CurrentDayHigh):
    IF CurrentPosition IS NOT OPEN: RETURN FALSE

    IF CurrentPosition.Type == BUY:
        // Check if price has touched or gone below the stop level
        IF CurrentDayLow <= CurrentPosition.DollarStopAmount: // Assuming DollarStopAmount is the actual stop price for a long
            EXECUTE_EXIT(CurrentPosition.Type, CurrentPosition.DollarStopAmount) // Exit at stop price
            RETURN TRUE
    ELSE IF CurrentPosition.Type == SELL:
        // Check if price has touched or gone above the stop level
        IF CurrentDayHigh >= CurrentPosition.DollarStopAmount: // Assuming DollarStopAmount is the actual stop price for a short
            EXECUTE_EXIT(CurrentPosition.Type, CurrentPosition.DollarStopAmount) // Exit at stop price
            RETURN TRUE
    RETURN FALSE

// Rule 2: "Bailout" Profit-Taking (for Daily Bars)
FUNCTION ApplyBailoutExit(CurrentPosition, CurrentDayIndex, CurrentDayOpen, MarketType):
    IF CurrentPosition IS NOT OPEN: RETURN FALSE

    IF CurrentDayIndex > CurrentPosition.EntryDayIndex: // Only consider after entry day
        IF CurrentPosition.Type == BUY:
            IF CurrentDayOpen > CurrentPosition.EntryPrice: // Profitable opening
                IF MarketType == "S&P" OR (CurrentDayIndex >= CurrentPosition.EntryDayIndex + 1): // S&P: 1 tick profit, Slower: 1-2 days delay
                    EXECUTE_EXIT(CurrentPosition.Type, CurrentDayOpen)
                    RETURN TRUE
        ELSE IF CurrentPosition.Type == SELL:
            IF CurrentDayOpen < CurrentPosition.EntryPrice: // Profitable opening
                IF MarketType == "S&P" OR (CurrentDayIndex >= CurrentPosition.EntryDayIndex + 1):
                    EXECUTE_EXIT(CurrentPosition.Type, CurrentDayOpen)
                    RETURN TRUE
    RETURN FALSE

// Rule 3: Exit and Reverse if an opposite signal is received
FUNCTION ApplyExitAndReverse(CurrentPosition, NewOppositeSignal, NewSignalType, Entry_Price_for_New_Signal, CurrentMarketPrice):
    IF CurrentPosition IS NOT OPEN: RETURN FALSE
    IF NewOppositeSignal IS TRUE:
        // Close current position immediately
        EXECUTE_EXIT(CurrentPosition.Type, CurrentMarketPrice) // Close at market
        // Enter new opposite position
        EXECUTE_TRADE(NewSignalType, Entry_Price_for_New_Signal)
        RETURN TRUE
    RETURN FALSE
```

---

## The Three Elements of Speculation (Framework)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 12: What Speculation Is All About (Page 160-161)
**Descrizione:** This framework outlines the three essential pillars for successful speculation: Selection, Timing, and Management. Mastery of all three is necessary for consistent profitability and long-term career success in trading.
1.  **Selection:** Involves identifying markets that are "ready to roar" or poised for substantial price changes. This also includes focusing on a limited number of markets to develop deep expertise.
2.  **Timing:** The art of pinpointing the precise moment when a market's explosive move will begin. The advice is to "Buy when the explosion has begun" rather than trying to anticipate absolute tops or bottoms.
3.  **Management:** Encompasses both money management (controlling capital allocation and risk) and trade management (controlling emotions, avoiding overtrading, and adhering to the trading plan). This is presented as the ultimate key to maximizing profits and sustaining a trading career.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// This is a conceptual framework, not a direct trading algorithm. Its implementation relies on
// the integration of specific technical techniques and principles described elsewhere in the book.

// 1. Selection Principles (Market & Asset Choice):
//    - Focus on a few specific markets to become an expert.
//    - Identify optimal periods using:
//        - Trading Day of Month (TDM) biases.
//        - Trading Day of Week (TDW) biases.
//        - Holiday-related biases.
//        - Intermarket correlations (e.g., Bonds-S&P, Gold-Bonds).
//        - Sentiment indicators (e.g., Jake Bernstein, Market Vane) to counter public opinion.
//    - Aim to find "setups" where a market is poised for "explosive" moves.

// 2. Timing Principles (Entry Execution):
//    - Wait for clear confirmation that a move has begun; do not try to "buy cheap" or "sell high" against initial momentum.
//    - Utilize specific entry patterns/indicators:
//        - Volatility Breakouts (e.g., Simple Daily Range Breakouts).
//        - Smash Day Reversals (including Hidden Smash Days).
//        - Oops! Patterns (gap reversals).
//        - Swing Points as Trend Change Indications.

// 3. Management Principles (Risk, Position & Emotion Control):
//    - Implement robust Money Management strategies:
//        - Risk Percentage of Account / Largest Loss formula (Larry Williams' preferred method).
//        - Avoid the pitfalls of the Kelly Formula (due to variable win/loss sizes in trading).
//    - Always use strict Dollar Stops for predefined risk control.
//    - Employ "Bailout" Profit-Taking to secure profits on advantageous openings.
//    - Be prepared to Exit and Reverse positions immediately upon receiving a conflicting signal.
//    - Cultivate patience, avoid overtrading, and do not let greed or fear override a well-tested plan.
//    - "Hold to the Close" (or longer for multi-day swings) for winning trades to allow profits to grow.
```

---

## Money Management: Kelly Formula (Critiqued)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 13: Approaches to Money Management-One Is Right for You (Page 174-177)
**Descrizione:** The Kelly Formula is a mathematical approach to position sizing, aiming to maximize long-term portfolio growth. It calculates the optimal fraction (F) of a bankroll to bet on each trade, based on the system's win rate (P) and the average win/loss ratio (R). The formula is `F = ((R + 1) * P - 1) / R`. While it gained popularity for blackjack, the author criticizes its direct application to commodity and stock trading due to the variable nature of wins and losses (unlike blackjack's fixed payouts), which can lead to excessive leverage and severe equity drawdowns.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Parameters:
SystemWinRate_P // Percentage Accuracy of the System Winning (e.g., 0.65)
AverageWinLossRatio_R // Ratio of Average Winning Trade Size to Average Losing Trade Size (e.g., 1.3)

// Formula Calculation:
FUNCTION CalculateKellyFraction(SystemWinRate_P, AverageWinLossRatio_R):
    IF AverageWinLossRatio_R == 0: RETURN 0 // Avoid division by zero
    
    numerator = ((AverageWinLossRatio_R + 1) * SystemWinRate_P) - 1
    
    IF numerator <= 0:
        RETURN 0 // No edge, or negative edge, so no bet or minimal bet
    
    RETURN numerator / AverageWinLossRatio_R

// Application (and associated criticisms from the author):
// Kelly_Fraction = CalculateKellyFraction(P, R)
// Dollar_Amount_to_Bet = Current_Account_Balance * Kelly_Fraction
// Number_of_Contracts_to_Trade = Dollar_Amount_to_Bet / Margin_Per_Contract

// Author's Critique and Caution:
// - The Kelly Formula assumes fixed win/loss sizes, which is not true in trading.
// - Applying it to trading leads to "wild gyrations" in equity.
// - Can result in excessive leverage and "blowup scenarios" during losing streaks.
// - Author recommends against direct application without significant modification or filtering.
```

---

## Money Management: Ryan Jones' Fixed Ratio Trading
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 13: Ryan Jones and Fixed Ratio Trading (Page 180-181)
**Descrizione:** Ryan Jones' Fixed Ratio Trading is a money management approach designed to control the rate at which trading size (number of contracts) increases with equity growth, aiming for more stable growth than the Kelly Formula. Instead of scaling based on a fixed percentage of the account, it uses a fixed *ratio* between the required profit increase and the current number of contracts to add another unit. This means larger absolute profits are required to increase trading size as the account grows, making the scaling slower and more controlled. The book highlights it can still lead to exponential growth but requires careful parameter selection.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Parameters:
Delta_Factor // A user-defined value, e.g., related to maximum historical drawdown or volatility.
Initial_Account_Balance // Starting capital
Initial_Contracts_Per_Unit // e.g., 1 contract per $10,000 initially.

// Variables:
Current_Account_Equity
Current_Number_of_Contracts // Number of contracts currently active
Equity_Threshold_for_Next_Contract // The equity level needed to add the next contract

// 1. Initialization (at start of trading):
// Current_Number_of_Contracts = FLOOR(Initial_Account_Balance / (Initial_Contracts_Per_Unit * Delta_Factor)) // Example
// Equity_Threshold_for_Next_Contract = Initial_Account_Balance + (Current_Number_of_Contracts * Delta_Factor) // Example

// 2. Dynamic Contract Calculation (based on profit achievement):
FUNCTION UpdateContracts_FixedRatio(Current_Account_Equity, Initial_Account_Balance, Delta_Factor):
    // Common formula for Fixed Ratio:
    // Number of contracts 'n' is found such that Current_Account_Equity - Initial_Account_Balance >= n * (n+1) / 2 * Delta_Factor
    // This can be solved for 'n' using the quadratic formula.
    
    // For simplicity, let's use the explicit example from the text:
    // "if it took $5,000 in profits to jump from one to two contracts, it will take $50,000 in profits on a $100,000 account to go from 10 to 11 units."
    // This implies a dynamic `Profit_Needed_to_Add_Contract` that increases with current `Number_of_Contracts`.

    // Let's implement a simplified step-based model as the exact formula is not given clearly in text.
    // This would require a lookup table for profit thresholds or a defined function that scales the threshold.
    
    // Example (conceptual, requires defining the scaling of thresholds):
    // IF Current_Account_Equity >= Equity_Threshold_for_Next_Contract:
    //    Current_Number_of_Contracts = Current_Number_of_Contracts + 1
    //    Equity_Threshold_for_Next_Contract = Current_Account_Equity + CalculateNextProfitThreshold(Current_Number_of_Contracts, Delta_Factor)
    // ELSE IF Current_Account_Equity < Equity_Threshold_for_Contract_Below_Current: (for scaling down)
    //    Current_Number_of_Contracts = Current_Number_of_Contracts - 1
    //    Update_Equity_Thresholds_for_Scaling_Down()

    // More practically, one common Fixed Ratio interpretation is that each time a contract is added,
    // the amount of equity required to add the *next* contract increases.
    // New_N = FLOOR( (SQRT(1 + 8 * (Current_Account_Equity - Initial_Account_Balance) / Delta_Factor) - 1) / 2 )
    // RETURN New_N
    
    // Given the text's vagueness on the exact formula, the core idea for pseudocode is:
    // Determine the number of contracts `N` such that:
    // `Current_Account_Equity >= Initial_Account_Balance + (N * (N + 1) / 2) * Delta_Factor`
    // And also implement symmetrical logic for scaling down contracts during drawdowns.
    
    // Placeholder using a common Fixed Ratio interpretation
    target_sum_of_natural_numbers = (Current_Account_Equity - Initial_Account_Balance) / Delta_Factor
    N_contracts_candidate = FLOOR( (SQRT(1 + 8 * target_sum_of_natural_numbers) - 1) / 2 )
    
    RETURN MAX(0, N_contracts_candidate)
```

---

## Money Management: Risk Percentage of Account / Largest Loss (Larry Williams' Solution)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 13: And Now My Solution to the Problem (Page 181-184, Figure 13.3, 13.4, 13.5)
**Descrizione:** This is the author's primary money management solution, designed to prevent catastrophic losses from large individual losing trades. It dictates the number of contracts a trader should take by setting a maximum percentage of the *total account balance* to risk on any single trade. This dollar risk amount is then divided by the system's *largest historical loss per contract* (or the maximum loss the trader is willing to take per contract). This approach dynamically adjusts trading size with account equity, ensuring that exposure is always proportional to the account's health and protected against extreme losing events. The author recommends a risk percentage of 10-15%, noting that drawdowns can increase disproportionately above 14-21%.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Parameters:
RISK_PERCENTAGE_OF_ACCOUNT // e.g., 0.10 to 0.15 (10-15%)
LARGEST_LOSS_PER_CONTRACT // The largest historical loss observed for one contract of the system

// Variables:
Current_Account_Balance

// Calculation for Number of Contracts:
FUNCTION CalculateNumberofContracts(Current_Account_Balance, Risk_Percentage_of_Account, Largest_Loss_Per_Contract):
    IF Largest_Loss_Per_Contract <= 0:
        RETURN 0 // Prevent division by zero or invalid loss amount
    
    Dollar_Amount_to_Risk = Current_Account_Balance * Risk_Percentage_of_Account
    Number_of_Contracts = FLOOR(Dollar_Amount_to_Risk / Largest_Loss_Per_Contract)
    
    RETURN MAX(0, Number_of_Contracts) // Ensure contract count is non-negative

// Application:
// At the beginning of each trading day, or after each closed trade:
// 1. Update Current_Account_Balance.
// 2. Calculate New_Number_of_Contracts = CalculateNumberofContracts(Current_Account_Balance, RISK_PERCENTAGE_OF_ACCOUNT, LARGEST_LOSS_PER_CONTRACT).
// 3. Adjust the size of new trades (and potentially existing positions if the system allows dynamic sizing) according to New_Number_of_Contracts.

// Author's Recommendation for Risk_Percentage_of_Account:
// - Tommy Timid: 5%
// - Normal Norma: 10-12%
// - Leveraged Larry: 15-18%
// - Swashbuckling Sam/Dangerous Danielle: >20% (with a warning to "go to church regularly")
// - Optimal range for best profit-to-drawdown ratio is typically 14-21%.
```

---

## S&P 500 Buy Signals based exclusively on Bonds (Intermarket)
**Libro/File Original:** Long-Term Secrets to Short-Term Trading (URI not provided)
**Contesto/Pagina:** Chapter 15: A Look at Data A and Data B (Page 235-237, Figure 15.1, 15.2)
**Descrizione:** This strategy demonstrates the power of intermarket analysis by generating highly profitable S&P 500 buy signals solely based on the price action of the Bond market, without using any S&P 500 price data for the entry signal. The premise is that a bullish breakout in Bonds (indicating falling interest rates) is a strong leading indicator for a rally in the stock market.
**Logica Tecnica/Pseudocodice:**
```pseudocode
// Assume 'Days_SP' is an array of daily price data for S&P 500 (Close_SP)
// Assume 'Bonds' is an array of daily price data for Bonds (High_B, Low_B, Close_B)

// Parameters:
BONDS_BREAKOUT_LOOKBACK = 14 // Days for Bond breakout detection (highest high in last X days)
BONDS_TRAILING_STOP_LOOKBACK = 17 // Days for trailing stop based on Bonds' lowest low
S_P_FLAT_DOLLAR_STOP = 3000 // Alternative flat dollar stop for S&P 500

// 1. Identify Bond Breakout (Bullish)
FUNCTION IsBondBullishBreakout(Bonds, i, lookback_period):
    IF i < lookback_period: RETURN FALSE
    max_high_bonds_past = MAX(Bonds[j].High for j in [i-lookback_period to i-1])
    
    // Bond market closed higher than its highest high of the last 'lookback_period' days
    RETURN Bonds[i].Close > max_high_bonds_past

// 2. S&P 500 Buy Signal (for Day[i]):
IF IsBondBullishBreakout(Bonds, i, BONDS_BREAKOUT_LOOKBACK):
    Entry_Price_SP = Days_SP[i].Close // Buy S&P 500 on the market close
    RETURN {TYPE: BUY, ENTRY_PRICE: Entry_Price_SP, EntryDayIndex: i}

// 3. Exit Strategy for S&P 500 Position (Applies to an open long S&P position):
FUNCTION ExitSPPosition(Position, Days_SP, Bonds, i):
    IF Position IS NOT OPEN: RETURN NULL

    // Option 1: