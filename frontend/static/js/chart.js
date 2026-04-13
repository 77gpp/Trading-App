/**
 * chart.js — Gestione del grafico TradingView Lightweight Charts
 *
 * Questo file gestisce:
 * - Creazione e configurazione del grafico finanziario
 * - Aggiunta delle serie di candele o linee
 * - Overlay degli indicatori tecnici (medie mobili, pivot points, ecc.)
 * - Marcatori delle notizie sul grafico
 * - Linea di proiezione futura (tratteggiata)
 * - Linee di Entry, Stop Loss e Take Profit
 * - Sovrimpressione del grafico reale vs previsione
 */

// -------------------------------------------------------
// PLUGIN: VOLUME PROFILE (Custom Primitive per LWC v4)
// -------------------------------------------------------

class VolumeProfilePrimitive {
    constructor(profiles, color) {
        this._profiles = profiles || []; // Array di { bins, poc, max_volume, startTime? }
        this._color = color;
        this._series = null;
    }
    
    attached(param) {
        this._series = param.series;
        this._chart = param.chart;
        this.requestUpdate = param.requestUpdate;
        if (this.requestUpdate) this.requestUpdate();
    }

    update(profiles) { 
        this._profiles = profiles || []; 
        if (this.requestUpdate) this.requestUpdate();
    }

    updateAllViews() {
        if (this.requestUpdate) this.requestUpdate();
    } // Richiesto nell'API v4 per forzare i ridisegni al movimento del mouse/pan
    
    paneViews() {
        return [this]; // Restituisce l'istanza stessa che implementa renderer() e zOrder()
    }

    renderer() {
        return {
            draw: (target) => {
                target.useBitmapCoordinateSpace((scope) => {
                    const ctx = scope.context;
                    const hRatio = scope.horizontalPixelRatio;
                    const vRatio = scope.verticalPixelRatio;
                    const canvasWidth = scope.mediaSize.width * hRatio;

                    if (!this._profiles.length || !this._series || !this._chart) return;
                    
                    ctx.save();

                    this._profiles.forEach(profile => {
                        if (!profile.bins || profile.bins.length === 0) return;
                        
                        const maxVol = profile.max_volume || 1;
                        const poc = profile.poc;
                        
                        let startX = null;
                        let endX = null;
                        
                        if (profile.startTime) {
                            const xLogical = this._chart.timeScale().timeToCoordinate(profile.startTime);
                            if (xLogical !== null) startX = xLogical * hRatio;
                        }
                        if (profile.endTime) {
                            const xLogical = this._chart.timeScale().timeToCoordinate(profile.endTime);
                            if (xLogical !== null) endX = xLogical * hRatio;
                        }

                        const mode = profile.mode || 'visible';
                        let barMaxWidth;
                        let alignRight = false;
                        
                        if (mode === 'visible') {
                            alignRight = true;
                            barMaxWidth = canvasWidth * 0.25;
                        } else if (mode === 'fixed') {
                            alignRight = false;
                            if (startX !== null && endX !== null) {
                                barMaxWidth = Math.max(10, Math.abs(endX - startX) * 0.3);
                            } else {
                                barMaxWidth = canvasWidth * 0.25;
                            }
                        } else if (mode === 'session') {
                            alignRight = false;
                            if (startX !== null && endX !== null) {
                                // Se startX === endX (es. 1 candela), usiamo una larghezza fissa ragionevole
                                const diff = Math.abs(endX - startX);
                                barMaxWidth = Math.max(60 * hRatio, diff * 0.4);
                            } else if (startX !== null) {
                                barMaxWidth = canvasWidth * 0.15;
                            } else {
                                barMaxWidth = 80 * hRatio;
                            }
                        }

                        // Aggiungo debug point log solo per un giro così lo vediamo
                        if (window._vapDebugCounter === undefined) window._vapDebugCounter = 0;
                        if (window._vapDebugCounter < 5) {
                            console.log(`[VAP Draw Debug] Mode: ${mode}, startX: ${startX}, endX: ${endX}, barMaxWidth: ${barMaxWidth}, binsCount: ${profile.bins.length}`);
                            window._vapDebugCounter++;
                        }

                        const rightOffset = 5 * hRatio;

                        profile.bins.forEach(bin => {
                            const yLogical = this._series.priceToCoordinate(bin.price);
                            if (yLogical === null) return;
                            
                            const yPhys = yLogical * vRatio;
                            const totalWidth = (bin.volume / maxVol) * barMaxWidth;
                            
                            // Calcolo altezza dinamica per far toccare le barre tra loro
                            let height = 4 * vRatio;
                            if (profile.bins.length > 1) {
                                const p1 = this._series.priceToCoordinate(profile.bins[0].price);
                                const p2 = this._series.priceToCoordinate(profile.bins[1].price);
                                height = Math.max(1, Math.abs(p2 - p1) * vRatio);
                            }
                            
                            let isPOC = false;
                            if (profile.bins.length > 1) {
                                isPOC = Math.abs(bin.price - poc) < ( (profile.bins[1].price - profile.bins[0].price) / 2 );
                            } else {
                                isPOC = true;
                            }
                            
                            const xStart = alignRight ? (canvasWidth - totalWidth - rightOffset) : ((startX || 0) + 2);
                            
                            if (isPOC) {
                                ctx.fillStyle = 'rgba(255, 165, 2, 0.85)';
                                ctx.fillRect(xStart, yPhys - (height / 2), totalWidth, height);
                            } else {
                                // Disegno split Buy/Sell
                                const upPart = bin.volume > 0 ? (bin.volUp / bin.volume) : 0;
                                const upWidth = totalWidth * upPart;
                                const downWidth = totalWidth - upWidth;
                                
                                // Colore Buy (Celeste TV)
                                ctx.fillStyle = 'rgba(38, 166, 154, 0.6)';
                                ctx.fillRect(xStart, yPhys - (height / 2), upWidth, height);
                                
                                // Colore Sell (Viola TV)
                                ctx.fillStyle = 'rgba(123, 31, 162, 0.6)';
                                ctx.fillRect(xStart + upWidth, yPhys - (height / 2), downWidth, height);
                            }
                        }); // end bins loop
                        
                        // --- NOVITÀ: Disegno linea POC manuale solo per sessione (per evitare caos di linee globali) ---
                        if (mode === 'session' && poc !== undefined) {
                            const yLogPoc = this._series.priceToCoordinate(poc);
                            if (yLogPoc !== null) {
                                const yPhysPoc = yLogPoc * vRatio;
                                const sX = startX || 0;
                                let eX = endX || sX;
                                
                                // Se la sessione è troppo corta (es. 1 giorno), allunghiamo la linea artificialmente
                                if (Math.abs(eX - sX) < 10) eX = sX + 60 * hRatio;
                                
                                ctx.save();
                                ctx.setLineDash([4 * hRatio, 4 * hRatio]);
                                ctx.strokeStyle = 'rgba(255, 165, 2, 0.95)';
                                ctx.lineWidth = 1.5 * hRatio;
                                ctx.beginPath();
                                ctx.moveTo(sX, yPhysPoc);
                                ctx.lineTo(eX, yPhysPoc);
                                ctx.stroke();
                                ctx.restore();
                            }
                        }

                        // Disegno dello sfondo giallo per simulare l'area del Fixed Range
                        if (mode === 'fixed' && startX !== null && endX !== null && profile.bins.length > 0) {
                            const firstLog = this._series.priceToCoordinate(profile.bins[0].price);
                            const lastLog = this._series.priceToCoordinate(profile.bins[profile.bins.length - 1].price);
                            if (firstLog !== null && lastLog !== null) {
                                const topY = Math.min(firstLog, lastLog) * vRatio;
                                const bottomY = Math.max(firstLog, lastLog) * vRatio;
                                
                                const rTop = topY - (4 * vRatio);
                                const rHeight = (bottomY - topY) + (8 * vRatio);
                                
                                ctx.fillStyle = 'rgba(255, 165, 2, 0.08)'; // Giallo molto leggero
                                ctx.fillRect(startX, rTop, endX - startX, rHeight);
                                
                                // Bordini sottili
                                ctx.fillStyle = 'rgba(255, 165, 2, 0.2)';
                                ctx.fillRect(startX, rTop, endX - startX, 1 * vRatio);
                                ctx.fillRect(startX, rTop + rHeight, endX - startX, 1 * vRatio);
                            }
                        }
                    });
                    
                    ctx.restore();
                });
            }
        };
    }
    zOrder() { return 'top'; }
}

// -------------------------------------------------------
// CONFIGURAZIONE GRAFICO
// -------------------------------------------------------
const CHART_CONFIG = {
  layout: {
    background: { color: '#060b18' },
    textColor: '#9ca3af',
    fontSize: 11,
    fontFamily: "'Inter', sans-serif",
  },
  grid: {
    vertLines: { color: 'rgba(255,255,255,0.03)' },
    horzLines: { color: 'rgba(255,255,255,0.03)' },
  },
  crosshair: {
    mode: 1, // CrosshairMode.Normal
    vertLine: {
      width: 1,
      color: 'rgba(0, 212, 170, 0.4)',
      style: 1,
    },
    horzLine: {
      width: 1,
      color: 'rgba(0, 212, 170, 0.4)',
      style: 1,
    },
  },
  rightPriceScale: {
    borderColor: 'rgba(255,255,255,0.07)',
    textColor: '#9ca3af',
  },
  timeScale: {
    borderColor: 'rgba(255,255,255,0.07)',
    textColor: '#9ca3af',
    timeVisible: true,
    secondsVisible: false,
    rightOffset: 12,
    barSpacing: 10,
    fixLeftEdge: false,
    fixRightEdge: false,
  },
  handleScale: { axisPressedMouseMove: true },
  handleScroll: { mouseWheel: true, pressedMouseMove: true },
};

// -------------------------------------------------------
// COSTANTI COLORI PRINCIPALI
// -------------------------------------------------------
const COLOR_REALE   = '#3fbef5'; // Celeste Professionale (Dati Reali)
const COLOR_AI      = '#BB86FC'; // Viola AI (Proiezione)
const COLOR_SL      = '#CF6666'; // Rosso SL (Stop Loss)
const COLOR_TP      = '#03F5A9'; // Verde TP (Take Profit)
const COLOR_ENTRY   = '#FFFFFF'; // Bianco Entry (Ingresso)

// -------------------------------------------------------
// STATO DEL GRAFICO
// -------------------------------------------------------
let chartState = {
  chart:            null,   // Istanza principale Lightweight Charts
  mainSeries:       null,   // Serie principale (candele o linee)
  volumeSeries:     null,   // Serie volume (istogramma sotto)
  projectionSeries: null,   // Linea tratteggiata proiezione futura
  realAfterSeries:  null,   // Linea del reale storico dopo la data di fine backtest
  entryLine:        null,   // Linea orizzontale Entry
  slLine:           null,   // Linea orizzontale Stop Loss
  tp1Line:          null,   // Linea orizzontale Take Profit 1
  tp2Line:          null,   // Linea orizzontale Take Profit 2
  overlays:         {},     // Dizionario: toolId → {type, series/lines}
  markers:          [],     // Marcatori base (notizie)
  toolMarkers:      {},     // Dizionario: toolId → markers[] per i pattern
  chartType:        'candlestick', 
  currentData:      [],     
  
  // Cache per il rendering unificato delle etichette (Entry | Reale)
  currentSetup:     null,
  realLastPrice:    null,
  unifiedLines:     [],

  vapOptions:       null,   // Opzioni correnti VAP: { mode, fixedStart, fixedEnd }
  vapListener:      null,   // Callback per aggiornamento dinamico
  fixedRangeListener: null, // Listener click per range fisso
};

// -------------------------------------------------------
// INIZIALIZZAZIONE
// -------------------------------------------------------
function initChart(containerId = 'chartContainer') {
  const container = document.getElementById(containerId);
  if (!container) return;

  // Se esiste già un grafico, lo distruggiamo prima
  if (chartState.chart) {
    chartState.chart.remove();
    chartState = { ...chartState, chart: null, mainSeries: null, volumeSeries: null };
  }

  chartState.chart = LightweightCharts.createChart(container, {
    ...CHART_CONFIG,
    width:  container.offsetWidth,
    height: container.offsetHeight,
  });

  // Reattività al resize della finestra
  const ro = new ResizeObserver(entries => {
    for (const entry of entries) {
      chartState.chart.applyOptions({
        width:  entry.contentRect.width,
        height: entry.contentRect.height,
      });
    }
  });
  ro.observe(container);

  // Aggiunta serie volume (in basso, mini istogramma)
  chartState.volumeSeries = chartState.chart.addHistogramSeries({
    color:         'rgba(0, 212, 170, 0.15)',
    priceFormat:   { type: 'volume' },
    priceScaleId:  'volume',
    scaleMargins:  { top: 0.85, bottom: 0 },
    lastValueVisible: false,
  });

  // Serie principale (candele di default)
  _addMainSeries('candlestick');

  // Gestiamo crosshair tooltip
  chartState.chart.subscribeCrosshairMove(handleCrosshairMove);
  
  // Gestiamo il click sulle notizie
  chartState.chart.subscribeClick(handleChartClick);


console.log('[CHART] Grafico inizializzato');
}

// -------------------------------------------------------
// AGGIUNTA SERIE PRINCIPALE
// -------------------------------------------------------
function _addMainSeries(type) {
  // Rimuove la vecchia serie se esiste
  if (chartState.mainSeries) {
    chartState.chart.removeSeries(chartState.mainSeries);
    chartState.mainSeries = null;
  }

  if (type === 'candlestick') {
    chartState.mainSeries = chartState.chart.addCandlestickSeries({
      upColor:          '#00d4aa',
      downColor:        '#ff4757',
      borderUpColor:    '#00d4aa',
      borderDownColor:  '#ff4757',
      wickUpColor:      '#00d4aa',
      wickDownColor:    '#cc3847',
      lastValueVisible: false,
      priceLineVisible: false,
    });
  } else {
    chartState.mainSeries = chartState.chart.addLineSeries({
      color:      COLOR_REALE,
      lineWidth:  2,
      crosshairMarkerVisible: true,
      crosshairMarkerRadius:  5,
      crosshairMarkerBackgroundColor: COLOR_REALE,
      lastValueVisible: false,
      priceLineVisible: false,
    });
  }

  chartState.chartType = type;

  // Se ci sono dati correnti, li riapplica
  if (chartState.currentData.length > 0) {
    _setSeriesData(chartState.currentData, type);
  }
}

function _setSeriesData(data, type) {
  if (!chartState.mainSeries) return;

  if (type === 'candlestick') {
    chartState.mainSeries.setData(data);
  } else {
    // Per le linee usiamo solo close
    const lineData = data.map(d => ({ time: d.time, value: d.close }));
    chartState.mainSeries.setData(lineData);
  }
}

// -------------------------------------------------------
// CARICAMENTO DATI
// -------------------------------------------------------
function loadChartData(candles) {
  if (!chartState.chart || !candles || candles.length === 0) return;

  chartState.currentData = candles;
  _setSeriesData(candles, chartState.chartType);

  // Dati volume
  const volumeData = candles.map(c => ({
    time:  c.time,
    value: c.volume,
    color: c.close >= c.open
      ? 'rgba(0, 212, 170, 0.2)'
      : 'rgba(255, 71, 87, 0.2)',
  }));
  chartState.volumeSeries.setData(volumeData);

  // Zoom sul periodo completo
  chartState.chart.timeScale().fitContent();

  // Aggiorna prezzo corrente in toolbar
  if (candles.length > 0) {
    const last = candles[candles.length - 1];
    const prev = candles.length > 1 ? candles[candles.length - 2] : null;
    updatePriceDisplay(last.close, prev ? last.close - prev.close : 0);
  }

  console.log(`[CHART] ${candles.length} candele caricate`);
}

// -------------------------------------------------------
// SWITCH CANDELE / LINEE
// -------------------------------------------------------
function switchChartType(type) {
  if (type === chartState.chartType) return;
  _addMainSeries(type);

  // Riapplica tutti gli overlay
  reapplyAllOverlays();

  console.log(`[CHART] Tipo grafico: ${type}`);
}

// -------------------------------------------------------
// PROIEZIONE FUTURA
// -------------------------------------------------------
function drawProjection(projectionData) {
  // Rimuove proiezione precedente
  clearProjection();

  if (!projectionData || projectionData.length === 0) return;

  // Linea principale proiezione
  chartState.projectionSeries = chartState.chart.addLineSeries({
    color:        '#BB86FC', // Viola vibrante (Material Design Purple)
    lineWidth:    2,
    lineStyle:    2, // Dashed
    crosshairMarkerVisible: false,
    title: 'Previsione AI',
  });

  const mainLine = projectionData.map(p => ({ time: p.time, value: p.value }));
  chartState.projectionSeries.setData(mainLine);

  // Bande di confidenza coordinate col colore principale
  const upperBand = chartState.chart.addLineSeries({
    color:        'rgba(187, 134, 252, 0.4)', // Più marcato del precedente 0.15
    lineWidth:    1,
    lineStyle:    3, // Dotted
    title:        'Max AI',
    crosshairMarkerVisible: false,
  });
  upperBand.setData(projectionData.map(p => ({ time: p.time, value: p.upper })));

  // Banda inferiore (confidenza)
  const lowerBand = chartState.chart.addLineSeries({
    color:        'rgba(187, 134, 252, 0.4)',
    lineWidth:    1,
    lineStyle:    3,
    title:        'Min AI',
    crosshairMarkerVisible: false,
  });
  lowerBand.setData(projectionData.map(p => ({ time: p.time, value: p.lower })));

  // Salviamo le bande per poterle rimuovere
  chartState._projUpper = upperBand;
  chartState._projLower = lowerBand;

  // Adattiamo la visuale per includere la proiezione
  chartState.chart.timeScale().fitContent();

  console.log(`[CHART] Proiezione disegnata: ${projectionData.length} punti`);
}

function clearProjection() {
  if (chartState.projectionSeries) {
    chartState.chart.removeSeries(chartState.projectionSeries);
    chartState.projectionSeries = null;
  }
  if (chartState._projUpper) {
    chartState.chart.removeSeries(chartState._projUpper);
    chartState._projUpper = null;
  }
  if (chartState._projLower) {
    chartState.chart.removeSeries(chartState._projLower);
    chartState._projLower = null;
  }
}

// -------------------------------------------------------
// GRAFICO REALE DOPO IL BACKTEST
// -------------------------------------------------------
function drawRealAfterProjection(candles) {
  if (chartState.realAfterSeries) {
    chartState.chart.removeSeries(chartState.realAfterSeries);
    chartState.realAfterSeries = null;
  }
  if (!candles || candles.length === 0) return;

  chartState.realAfterSeries = chartState.chart.addLineSeries({
    color:        COLOR_REALE,
    lineWidth:    2,
    lineStyle:    0, // Solid
    title:        'Reale (verifica)',
    lastValueVisible: false, // Gestito manualmente per affiancamento
    crosshairMarkerVisible: true,
  });

  const lastPrice = candles[candles.length - 1].close;
  chartState.realLastPrice = lastPrice;

  const lineData = candles.map(c => ({ time: c.time, value: c.close }));
  chartState.realAfterSeries.setData(lineData);
  
  // Applica le linee unificate
  renderUnifiedPriceLines();

  chartState.chart.timeScale().fitContent();
}

// -------------------------------------------------------
// LINEE DI TRADING (Entry, SL, TP)
// -------------------------------------------------------
function drawTradeLevels(setup) {
  if (!setup || !chartState.mainSeries) return;
  chartState.currentSetup = setup;

  // Applica le linee unificate (che chiamerà internamente clearTradeLevels)
  renderUnifiedPriceLines();
}

/**
 * Logica per unire etichette con lo stesso prezzo (es. "Entry | Reale")
 */
function renderUnifiedPriceLines() {
  clearTradeLevels();
  if (!chartState.mainSeries) return;

  const setup = chartState.currentSetup || {};
  const levels = [];

  // Raccoglie i livelli potenziali
  if (setup.entry)         levels.push({ price: setup.entry, title: 'Entry', color: COLOR_ENTRY, style: 0 });
  if (setup.stop_loss)     levels.push({ price: setup.stop_loss, title: 'SL', color: COLOR_SL, style: 2 });
  if (setup.take_profit_1) levels.push({ price: setup.take_profit_1, title: 'TP1', color: COLOR_TP, style: 2 });
  if (setup.take_profit_2) levels.push({ price: setup.take_profit_2, title: 'TP2', color: '#00E5FF', style: 2 });
  if (chartState.realLastPrice) {
    levels.push({ price: chartState.realLastPrice, title: 'Reale', color: COLOR_REALE, style: 0 });
  }

  if (levels.length === 0) return;

  // Raggruppa per prezzo (con tolleranza minima per float)
  const groups = {};
  levels.forEach(lvl => {
    const key = lvl.price.toFixed(4);
    if (!groups[key]) groups[key] = [];
    groups[key].push(lvl);
  });

  // Crea le linee unificate
  chartState.unifiedLines = [];
  Object.keys(groups).forEach(priceKey => {
    const group = groups[priceKey];
    const price = parseFloat(priceKey);
    
    // Unisce i titoli se necessario
    const mergedTitle = group.map(g => g.title).join(' | ');
    
    // Sceglie il colore: 
    // Se c'è Entry o Reale nel gruppo, usiamo il loro colore. 
    // Altrimenti usiamo il colore del primo elemento.
    let finalColor = group[0].color;
    if (group.some(g => g.title === 'Entry')) finalColor = COLOR_ENTRY;
    else if (group.some(g => g.title === 'Reale')) finalColor = COLOR_REALE;

    const line = chartState.mainSeries.createPriceLine({
      price:     price,
      color:     finalColor,
      lineWidth: group.length > 1 ? 2 : 1,
      lineStyle: group[0].style,
      axisLabelVisible: true,
      title: `${mergedTitle} ${price.toFixed(2)}`,
    });
    
    chartState.unifiedLines.push(line);
  });
}

function clearTradeLevels() {
  if (chartState.unifiedLines && chartState.mainSeries) {
    chartState.unifiedLines.forEach(line => {
      try { chartState.mainSeries.removePriceLine(line); } catch(e){}
    });
    chartState.unifiedLines = [];
  }
}

/**
 * Pulisce completamente l'analisi (proiezioni, setup di trading e dati di verifica)
 * per resettare il grafico prima di un nuovo caricamento.
 */
function clearAnalysis() {
  // Resetta lo stato logico
  chartState.currentSetup = null;
  chartState.realLastPrice = null;

  // Pulisce le serie grafiche
  clearProjection();

  if (chartState.realAfterSeries) {
    try { chartState.chart.removeSeries(chartState.realAfterSeries); } catch(e){}
    chartState.realAfterSeries = null;
  }

  // Pulisce le linee di prezzo (Entry, SL, TP)
  clearTradeLevels();

  console.log('[CHART] Analisi precedente pulita dal grafico');
}

/**
 * Pulisce solo le proiezioni rapide (viola) e i dati di verifica (celeste),
 * mantenendo intatti i livelli di trading (SL, TP) se presenti.
 */
function clearQuickProjections() {
  clearProjection();
  
  if (chartState.realAfterSeries) {
    try { chartState.chart.removeSeries(chartState.realAfterSeries); } catch(e){}
    chartState.realAfterSeries = null;
  }
  
  chartState.realLastPrice = null;
  
  // Aggiorna le etichette per rimuovere "Reale"
  renderUnifiedPriceLines();
  
  console.log('[CHART] Proiezioni rapide rimosse');
}

// -------------------------------------------------------
// MARCATORI NOTIZIE SUL GRAFICO
// -------------------------------------------------------
function drawNewsMarkers(newsItems) {
  if (!newsItems || newsItems.length === 0) {
    chartState.markers = [];
  } else {
    // 0. BLACKLIST RUMORE (Epurazione titoli automatici/ripetitivi)
    const blacklist = ["roundup", "top 12", "top 10", "most-searched", "most searched", "what's going on", "heres why", "market open", "market close"];
    let cleanNews = newsItems.filter(item => {
      const lowerH = item.headline.toLowerCase();
      return !blacklist.some(word => lowerH.includes(word));
    });

    // 1. DEDUPLICAZIONE E CONSOLIDAMENTO DRASTICO (Massimo 1 notizia per giorno)
    const dailyWinners = {};
    cleanNews.forEach(item => {
      const dateStr = new Date(item.time * 1000).toISOString().split('T')[0];
      const currentScore = item.headline.length + (item.summary?.length || 0);
      
      if (!dailyWinners[dateStr] || currentScore > (dailyWinners[dateStr].headline.length + (dailyWinners[dateStr].summary?.length || 0))) {
        dailyWinners[dateStr] = item;
      }
    });

    const consolidatedNews = Object.values(dailyWinners);

    // 2. FILTRO MACRO-IMPATTO (LOOK-AHEAD 10 DAYS CON SOGLIA 7%)
    const threshold = 7.0; // Innalzato al 7% per isolare solo i veri punti di svolta macro
    
    const finalNews = consolidatedNews.filter(item => {
      const isDDG = item.provider === 'duckduckgo';
      if (isDDG) return true; // Le notizie web recenti le mostriamo sempre (allerta immediata)

      const newsDateStr = new Date(item.time * 1000).toISOString().split('T')[0];
      const candleIdx = chartState.currentData.findIndex(c => {
        return new Date(c.time * 1000).toISOString().split('T')[0] === newsDateStr;
      });
      
      if (candleIdx === -1) return false;
      
      const startPrice = chartState.currentData[candleIdx].close;
      
      // Analisi dei 10 giorni lavorativi successivi
      const lookAhead = 10;
      let maxMove = 0;
      
      for (let i = 1; i <= lookAhead; i++) {
        const futureIdx = candleIdx + i;
        if (futureIdx >= chartState.currentData.length) break;
        
        const futureCandle = chartState.currentData[futureIdx];
        const moveHigh = Math.abs((futureCandle.high - startPrice) / startPrice) * 100;
        const moveLow  = Math.abs((futureCandle.low - startPrice) / startPrice) * 100;
        maxMove = Math.max(maxMove, moveHigh, moveLow);
      }
      
      return maxMove >= threshold;
    });

    console.log(`[CHART] Ultra-Filtering Gen 3: ${newsItems.length} news -> ${finalNews.length} macro-impact markers`);

    chartState.markers = finalNews.map((item, index) => {
      const isDDG = item.provider === 'duckduckgo';
      const markerColor = isDDG ? '#3fbef5' : '#ffa502';
      
      let normalizedTime;
      let markerDate = item.date; // Default: data originale della news

      if (isDDG && chartState.currentData && chartState.currentData.length > 0) {
        // Se è DuckDuckGo, pinna all'ultima candela
        const lastCandle = chartState.currentData[chartState.currentData.length - 1];
        normalizedTime = lastCandle.time;
        // Importante: per il tooltip, la data deve coincidere con la candela fisicamente presente
        markerDate = new Date(lastCandle.time * 1000).toISOString().split('T')[0];
      } else {
        const d = new Date(item.time * 1000);
        normalizedTime = Math.floor(new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime() / 1000);
      }

      return {
        time:     normalizedTime,
        originalTime: item.time, // Conserviamo l'orario originale per il tooltip
        position: isDDG ? 'belowBar' : 'aboveBar',
        color:    markerColor,
        shape:    isDDG ? 'arrowUp' : 'circle',
        text:     isDDG ? '🌐' : '📰',
        size:     1,
        id:       `news_${item.time}_${index}`,
        headline: item.headline,
        source:   item.source,
        date:     markerDate,
        url:      item.url,
        provider: item.provider
      };
    });
  }
  _updateAllMarkers();
  console.log(`[CHART] ${chartState.markers.length} marcatori notizie caricati (normalizzati)`);
}

function clearNewsMarkers() {
  chartState.markers = [];
  _updateAllMarkers();
}

/**
 * Unisce tutti i marcatori (notizie + pattern attivi) e li applica alla serie principale.
 */
function _updateAllMarkers() {
  if (!chartState.mainSeries) return;

  let allMarkers = [...chartState.markers];
  
  // Aggiungiamo i marcatori dei vari tool attivi
  Object.values(chartState.toolMarkers).forEach(toolMs => {
    allMarkers = allMarkers.concat(toolMs);
  });

  // Ordiniamo per tempo (importante per Lightweight Charts)
  allMarkers.sort((a, b) => a.time - b.time);
  
  chartState.mainSeries.setMarkers(allMarkers);
}

// -------------------------------------------------------
// OVERLAY INDICATORI TECNICI
// -------------------------------------------------------

// Calcola SMA (Simple Moving Average) da array di close
function calculateSMA(closes, period) {
  const sma = [];
  for (let i = period - 1; i < closes.length; i++) {
    const avg = closes.slice(i - period + 1, i + 1).reduce((a, b) => a + b, 0) / period;
    sma.push(avg);
  }
  return sma;
}

// Calcola EMA (Exponential Moving Average)
function calculateEMA(closes, period) {
  const k = 2 / (period + 1);
  const ema = [closes[0]];
  for (let i = 1; i < closes.length; i++) {
    ema.push(closes[i] * k + ema[i - 1] * (1 - k));
  }
  return ema;
}

// Calcola Fibonacci a partire dagli ultimi N periodi
function calculateFibonacci(data) {
  if (data.length < 2) return [];
  const highs  = data.map(d => d.high);
  const lows   = data.map(d => d.low);
  const maxH   = Math.max(...highs);
  const minL   = Math.min(...lows);
  const diff   = maxH - minL;
  const levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1];
  return levels.map(l => ({
    level: l,
    price: minL + diff * (1 - l),
  }));
}

// Applica un overlay al grafico
function applyOverlay(toolId, toolName, color, data) {
  // Rimuoviamo overlay precedente con lo stesso ID
  removeOverlay(toolId);
  
  if (!chartState.chart || !data || data.length === 0) return;

  let series;

  // Scegliamo il tipo di serie in base allo strumento
  if (toolId.startsWith('sma') || toolId.startsWith('ema') || toolId.startsWith('super') || toolId === 'vwap') {
    series = chartState.chart.addLineSeries({
      color:     color,
      lineWidth: 1,
      title:     toolName,
      crosshairMarkerVisible: false,
    });
    series.setData(data.map(d => ({ time: d.time, value: d.value })));

  } else if (toolId === 'volume_vsa') {
    series = chartState.chart.addHistogramSeries({
      color:        color,
      priceScaleId: 'volume',
      scaleMargins: { top: 0.85, bottom: 0 },
    });
    series.setData(data.map(d => ({ time: d.time, value: d.value, color: d.color || color })));

  } else if (toolId.startsWith('pattern') || toolId.startsWith('power')) {
    // I pattern vengono gestiti come marcatori sulla serie principale
    chartState.toolMarkers[toolId] = data;
    _updateAllMarkers();
    chartState.overlays[toolId] = { type: 'markers' };
    return;

  } else if (toolId === 'volume_profile') {
    // Disegno dei volumi in ORIZZONTALE (Volume Profile Professionale)
    let pocLine = null;
    if (data && typeof data.poc === 'number' && !isNaN(data.poc)) {
      pocLine = chartState.mainSeries.createPriceLine({
        price: data.poc,
        color: '#ffa502',
        lineWidth: 1,
        lineStyle: 2, // Dashed
        axisLabelVisible: true,
        title: 'POC',
      });
    }

    // Creazione del Custom Primitive per le barre orizzontali (v4 API)
    const vpPrimitive = new VolumeProfilePrimitive(data, color);
    chartState.mainSeries.attachPrimitive(vpPrimitive);

    chartState.overlays[toolId] = { 
        type: 'volume_profile', 
        primitive: vpPrimitive, 
        lines: pocLine ? [pocLine] : [] 
    };
    return;

  } else if (toolId.startsWith('pivot') || toolId.startsWith('fib') || toolId.startsWith('livelli')) {
    // Livelli orizzontali multipli 
    if (Array.isArray(data) && data[0] && data[0].levels) {
      const lines = data[0].levels.map((lvl) =>
        chartState.mainSeries.createPriceLine({
          price: lvl.price,
          color: color,
          lineWidth: 1,
          lineStyle: 3,
          axisLabelVisible: true,
          title: `${lvl.level} ${lvl.price.toFixed(2)}`,
        })
      );
      chartState.overlays[toolId] = { type: 'priceLines', lines };
      return;
    }
  } else {
    // Default: linea semplice
    series = chartState.chart.addLineSeries({
      color:     color,
      lineWidth: 1,
      title:     toolName,
    });
    series.setData(data.map(d => ({ time: d.time, value: d.value })));
  }

  if (series) {
    chartState.overlays[toolId] = { type: 'series', series };
  }
}

/**
 * Calcola il Volume Profile (VAP) a partire da un set di candele
 */
function calculateVAP(candles, binsCount = 40) {
    if (!candles || candles.length === 0) return null;

    let minP = Math.min(...candles.map(c => c.low));
    let maxP = Math.max(...candles.map(c => c.high));
    const range = maxP - minP;

    if (range <= 0) return null;

    const binSize = range / binsCount;
    const bins = [];
    for (let i = 0; i < binsCount; i++) {
        bins.push({ 
            price: minP + (i * binSize) + (binSize / 2), 
            volume: 0,
            volUp: 0,
            volDown: 0
        });
    }

    candles.forEach(c => {
        // Calcolo aggregato basato sulla chiusura
        const idx     = Math.floor((c.close - minP) / binSize);
        const safeIdx = Math.max(0, Math.min(binsCount - 1, idx));
        const vol = (c.volume || 0);
        
        bins[safeIdx].volume += vol;
        if (c.close >= c.open) {
            bins[safeIdx].volUp += vol;
        } else {
            bins[safeIdx].volDown += vol;
        }
    });

    const maxBin = bins.reduce((prev, curr) => (prev.volume > curr.volume) ? prev : curr, bins[0]);
    
    return {
        bins: bins,
        poc: maxBin.price,
        max_volume: maxBin.volume
    };
}

/**
 * Gestore principale per l'applicazione del Volume Profile professionale
 */
function applyVolumeProfile(color, options = { mode: 'visible' }) {
    // 1. Rimuoviamo overlay VAP esistente
    removeOverlay('volume_profile');
    
    // Manteniamo le info del range fisso se esistono
    const oldOptions = chartState.vapOptions || {};
    chartState.vapOptions = { ...oldOptions, ...options };

    // 2. Logica di aggiornamento (per modalità 'visible')
    if (options.mode === 'visible') {
        if (!chartState.vapListener) {
            chartState.vapListener = () => {
                const isSelected = document.getElementById('tool-volume_profile')?.checked;
                const currentMode = document.getElementById('vap-mode')?.value;
                if (isSelected && currentMode === 'visible') {
                    _updateVAPDrawing(color);
                }
            };
            chartState.chart.timeScale().subscribeVisibleLogicalRangeChange(chartState.vapListener);
        }
    } else {
        // Se non è visibile, assicuriamoci di pulire il listener concettualmente
        // (lo teniamo sottoscritto ma l'if interno blocca l'esecuzione)
    }

    // 3. Eseguiamo il primo disegno
    _updateVAPDrawing(color);
}

// -------------------------------------------------------
// SELEZIONE RANGE FISSO (VAP)
// -------------------------------------------------------
function startFixedRangeSelection(onFirstClick, onComplete, onError) {
    if (!chartState.chart || !chartState.mainSeries) return;
    
    cancelFixedRangeSelection();
    
    let firstClickTime = null;

    chartState.fixedRangeListener = (param) => {
        if (!param.time) return; // Ignore clicks outside valid chart data

        if (!firstClickTime) {
            firstClickTime = param.time;
            if (onFirstClick) onFirstClick(firstClickTime);
        } else {
            const secondClickTime = param.time;
            chartState.chart.unsubscribeClick(chartState.fixedRangeListener);
            chartState.fixedRangeListener = null;
            
            if (firstClickTime === secondClickTime) {
                if (onError) onError("Devi selezionare due candele differenti.");
                firstClickTime = null;
                if (onFirstClick) onFirstClick(firstClickTime); // reset ui loop
                return;
            }

            if (!chartState.vapOptions) chartState.vapOptions = { mode: 'fixed' };
            
            // Usiamo il ternario invece di Math.min/max così supportiamo anche formati stringa non-numerici o oggetti nel peggiore dei casi (se comparabili)
            const isFirstSmaller = firstClickTime < secondClickTime;
            chartState.vapOptions.fixedStart = isFirstSmaller ? firstClickTime : secondClickTime;
            chartState.vapOptions.fixedEnd = isFirstSmaller ? secondClickTime : firstClickTime;

            if (onComplete) onComplete(chartState.vapOptions.fixedStart, chartState.vapOptions.fixedEnd);
        }
    };
    
    chartState.chart.subscribeClick(chartState.fixedRangeListener);
}

function cancelFixedRangeSelection() {
    if (chartState.fixedRangeListener && chartState.chart) {
        chartState.chart.unsubscribeClick(chartState.fixedRangeListener);
        chartState.fixedRangeListener = null;
    }
}

/**
 * Funzione interna per ricalcolare e disegnare i profili
 */
function _updateVAPDrawing(color) {
    if (!chartState.vapOptions || !chartState.mainSeries) return;
    
    // 0. Pulizia preventiva dell'overlay esistente (fondamentale per rimuovere le vecchie PriceLines)
    // Non usiamo removeOverlay completo qui per non cancellare vapOptions, 
    // ma dobbiamo staccare la primitiva e rimuovere le linee vecchie.
    const oldOverlay = chartState.overlays['volume_profile'];
    if (oldOverlay) {
        if (oldOverlay.primitive) chartState.mainSeries.detachPrimitive(oldOverlay.primitive);
        if (oldOverlay.lines) {
            oldOverlay.lines.forEach(line => {
                try { chartState.mainSeries.removePriceLine(line); } catch(e){}
            });
        }
    }

    const { mode } = chartState.vapOptions;
    const candles = chartState.currentData;
    if (!candles || candles.length === 0) return;

    let profiles = [];

    if (mode === 'visible') {
        const range = chartState.chart.timeScale().getVisibleLogicalRange();
        if (range) {
            const visibleCandles = candles.filter((_, idx) => idx >= range.from && idx <= range.to);
            const vap = calculateVAP(visibleCandles, 100);
            if (vap) {
                vap.mode = 'visible';
                profiles.push(vap);
            }
        }
    } 
    else if (mode === 'fixed') {
        let targetCandles = candles;
        if (chartState.vapOptions.fixedStart !== undefined && chartState.vapOptions.fixedEnd !== undefined) {
             const minT = chartState.vapOptions.fixedStart;
             const maxT = chartState.vapOptions.fixedEnd;
             targetCandles = candles.filter(c => c.time >= minT && c.time <= maxT);
        }
        if (targetCandles.length > 0) {
            const vap = calculateVAP(targetCandles, 100); 
            if (vap) {
                vap.mode = 'fixed';
                vap.startTime = targetCandles[0].time;
                vap.endTime = targetCandles[targetCandles.length - 1].time;
                profiles.push(vap);
            }
        }
    }
    else if (mode === 'session') {
        const sessions = {};
        candles.forEach(c => {
            const day = new Date(c.time * 1000).toISOString().split('T')[0];
            if (!sessions[day]) sessions[day] = [];
            sessions[day].push(c);
        });

        Object.keys(sessions).sort().forEach(day => {
            const sessionCandles = sessions[day];
            const vap = calculateVAP(sessionCandles, 100);
            if (vap) {
                vap.mode = 'session';
                vap.startTime = sessionCandles[0].time;
                vap.endTime = sessionCandles[sessionCandles.length - 1].time;
                profiles.push(vap);
            }
        });
    }

    if (profiles.length === 0) return;

    // 1. Creazione delle linee POC tratteggiate
    const pocLines = [];
    profiles.forEach((profile) => {
        // Solo per visible e fixed creiamo linee globali (PriceLine)
        // Per sessione usiamo il disegno manuale interno alla primitiva
        if (mode !== 'session' && profile.poc !== undefined && !isNaN(profile.poc)) {
            const line = chartState.mainSeries.createPriceLine({
                price: profile.poc,
                color: '#ffa502',
                lineWidth: 1,
                lineStyle: 2, // Dashed
                axisLabelVisible: true,
                title: 'POC',
            });
            pocLines.push(line);
        }
    });

    // 2. Disegno effettivo delle barre
    const vpPrimitive = new VolumeProfilePrimitive(profiles, color);
    chartState.mainSeries.attachPrimitive(vpPrimitive);

    // 3. Salvataggio stato per rimozione futura
    chartState.overlays['volume_profile'] = { 
        type: 'volume_profile', 
        primitive: vpPrimitive,
        lines: pocLines
    };
}

function removeOverlay(toolId) {
  const overlay = chartState.overlays[toolId];
  if (!overlay) return;

  if (overlay.type === 'series') {
    chartState.chart.removeSeries(overlay.series);
  } else if (overlay.type === 'priceLines') {
    overlay.lines.forEach(line => {
      try { chartState.mainSeries.removePriceLine(line); } catch(e){}
    });
  } else if (overlay.type === 'volume_profile') {
    if (overlay.primitive) {
        chartState.mainSeries.detachPrimitive(overlay.primitive);
    }
    overlay.lines.forEach(line => {
      try { chartState.mainSeries.removePriceLine(line); } catch(e){}
    });
  } else if (overlay.type === 'markers') {
    delete chartState.toolMarkers[toolId];
    _updateAllMarkers();
  }

  delete chartState.overlays[toolId];
}

function reapplyAllOverlays() {
  // Chiamata dopo cambio tipo grafico — gli overlay vengono gestiti dall'UI
  // (il mainSeries cambia, quindi le price lines vanno ricreate)
  console.log('[CHART] Reapply overlays dopo cambio tipo grafico');
}

// -------------------------------------------------------
// UTILITY PER VOLUME PROFILE
function _renderImprovedVap(volData) {
  if (!volData || !volData.bins || volData.bins.length === 0) return [];
  if (!chartState.currentData || chartState.currentData.length === 0) return [];

  const lastCandle = chartState.currentData[chartState.currentData.length - 1];
  const lastTime   = lastCandle.time;
  const points     = [];
  const maxVol     = volData.max_volume || 1;
  
  // Ordiniamo i bin per prezzo per una visualizzazione coerente
  const sortedBins = [...volData.bins].sort((a,b) => a.price - b.price);
  
  // Per allineare visivamente le barre a destra nel futuro, usiamo un tempo di partenza
  let currentTime = lastTime + (3600 * 5); 

  sortedBins.forEach((bin) => {
    // Calcoliamo una larghezza proporzionale al volume (max 24 ore di spazio grafico)
    const widthSecs = Math.floor((bin.volume / maxVol) * 3600 * 24);
    
    // Creiamo il "gradino" per ogni bin
    points.push({ time: currentTime, value: bin.price });
    points.push({ time: currentTime + widthSecs, value: bin.price });
    
    // Incrementiamo il tempo per il prossimo bin assicurando la sequenzialità
    currentTime += widthSecs + 1;
  });

  return points;
}


// -------------------------------------------------------
// CALCOLO DATI INDICATORI (Compute Overlay Data)
// -------------------------------------------------------
function computeOverlayData(toolId, candles, volumeProfileData = null) {
  if (!candles || candles.length === 0) return [];

  switch (toolId) {
    case 'volume_profile':
      return volumeProfileData; // Restituiamo direttamente i dati calcolati dal backend
  }

  const times  = candles.map(c => c.time);
  const closes = candles.map(c => c.close);
  const highs  = candles.map(c => c.high);
  const lows   = candles.map(c => c.low);

  switch (toolId) {
    case 'sma_20': {
      const sma = calculateSMA(closes, 20);
      return sma.map((v, i) => ({ time: times[i + 19], value: v }));
    }
    case 'sma_50': {
      const sma = calculateSMA(closes, 50);
      return sma.map((v, i) => ({ time: times[i + 49], value: v }));
    }
    case 'sma_200': {
      const sma = calculateSMA(closes, 200);
      return sma.map((v, i) => ({ time: times[i + 199], value: v }));
    }
    case 'ema_20': {
      const ema = calculateEMA(closes, 20);
      return ema.map((v, i) => ({ time: times[i], value: v }));
    }
    case 'ema_50': {
      const ema = calculateEMA(closes, 50);
      return ema.map((v, i) => ({ time: times[i], value: v }));
    }
    case 'supertrend': {
      // SuperTrend semplificato (ATR-based)
      const period = 14, multiplier = 3;
      const atrArr = [];
      for (let i = 1; i < candles.length; i++) {
        const tr = Math.max(
          highs[i] - lows[i],
          Math.abs(highs[i] - closes[i - 1]),
          Math.abs(lows[i] - closes[i - 1])
        );
        atrArr.push(tr);
      }
      // EMA dell'ATR
      const atrEma = calculateEMA(atrArr, period);
      return atrEma.map((atr, i) => ({
        time:  times[i + 1],
        value: closes[i + 1] > closes[i]
          ? closes[i + 1] - multiplier * atr
          : closes[i + 1] + multiplier * atr,
      }));
    }
    case 'fib_retracement': {
      const maxH = Math.max(...highs);
      const minL = Math.min(...lows);
      const levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1].map(l => ({
        level: l,
        price: minL + (maxH - minL) * (1 - l),
      }));
      return [{ time: times[0], levels }];
    }
    case 'vwap': {
      // VWAP semplificato con protezione divisione per zero e NaN
      let cumVolPrice = 0, cumVol = 0;
      return candles.map((c) => {
        const typicalPrice = (c.high + c.low + c.close) / 3;
        const v = parseFloat(c.volume) || 0;
        cumVolPrice += typicalPrice * v;
        cumVol      += v;
        
        const vwapValue = (cumVol > 0) ? (cumVolPrice / cumVol) : c.close;
        return { time: c.time, value: vwapValue };
      });
    }
    case 'volume_vsa': {
      // VSA: Colora le barre del volume in base alla deviazione dalla media
      const volArr = candles.map(c => c.volume || 0);
      const results = [];
      
      // Calcoliamo una media mobile dei volumi per il confronto (periodo 20)
      const period = 20;
      for (let i = 0; i < candles.length; i++) {
        let avgVol = 0;
        if (i >= period) {
          avgVol = volArr.slice(i - period, i).reduce((a, b) => a + b, 0) / period;
        } else {
          avgVol = volArr.slice(0, i + 1).reduce((a, b) => a + b, 0) / (i + 1);
        }

        const currVol = candles[i].volume || 0;
        let vColor = '#9ca3af'; // Grigio default
        
        if (currVol > avgVol * 2.0) vColor = '#ff4757'; // Volume estremo (Rosso)
        else if (currVol > avgVol * 1.5) vColor = '#ffa502'; // Volume alto (Arancione)
        else if (currVol > avgVol * 1.2) vColor = '#3f8ef5'; // Volume sopra media (Blu)
        
        results.push({
          time:  candles[i].time,
          value: currVol,
          color: vColor
        });
      }
      return results;
    }
    case 'pivot_points': {
      // Pivot Points giornalieri (calcoliamo sull'ultima candela)
      const last = candles[candles.length - 1];
      const P  = (last.high + last.low + last.close) / 3;
      const R1 = 2 * P - last.low;
      const S1 = 2 * P - last.high;
      const R2 = P + (last.high - last.low);
      const S2 = P - (last.high - last.low);
      return [{ time: candles[0].time, levels: [
        { price: R2, level: 'R2' },
        { price: R1, level: 'R1' },
        { price: P,  level: 'PP' },
        { price: S1, level: 'S1' },
        { price: S2, level: 'S2' },
      ]}];
    }
    case 'pattern_engulfing': {
      const markers = [];
      for (let i = 1; i < candles.length; i++) {
        const curr = candles[i];
        const prev = candles[i - 1];
        
        // Bullish Engulfing
        if (prev.close < prev.open && curr.close > curr.open && 
            curr.open <= prev.close && curr.close > prev.open) {
          markers.push({
            time:     curr.time,
            position: 'belowBar',
            color:    '#00d4aa',
            shape:    'arrowUp',
            text:     'Eng. Bull',
            id:       `bull_${curr.time}`
          });
        }
        // Bearish Engulfing
        else if (prev.close > prev.open && curr.close < curr.open && 
                 curr.open >= prev.close && curr.close < prev.open) {
          markers.push({
            time:     curr.time,
            position: 'aboveBar',
            color:    '#ff4757',
            shape:    'arrowDown',
            text:     'Eng. Bear',
            id:       `bear_${curr.time}`
          });
        }
      }
      return markers;
    }
    case 'pattern_powerbar': {
      const markers = [];
      if (candles.length < 15) return [];
      
      const ranges = candles.map(c => c.high - c.low);
      for (let i = 14; i < candles.length; i++) {
        const curr  = candles[i];
        const avgR  = ranges.slice(i-14, i).reduce((a,b)=>a+b, 0) / 14;
        const range = curr.high - curr.low;
        
        // Soglia ridotta da 1.5 a 1.25 per maggior visibilità
        if (range > avgR * 1.25) {
          const bodyRange = Math.abs(curr.close - curr.open);
          if (bodyRange > range * 0.5) { // Chiusura forte (50% range)
            markers.push({
              time:     curr.time,
              position: curr.close > curr.open ? 'belowBar' : 'aboveBar',
              color:    '#3f8ef5',
              shape:    'star',
              text:     'Power',
              id:       `power_${curr.time}`
            });
          }
        }
      }
      return markers;
    }
    case 'pattern_triangle': {
      const markers = [];
      if (candles.length < 20) return [];
      
      for (let i = 15; i < candles.length - 1; i++) {
        const slice = candles.slice(i-15, i); // Finestra più piccola
        const maxs  = slice.map(c => c.high);
        const mins  = slice.map(c => c.low);
        
        // Convergenza in 15 candele
        const maxDown = Math.max(...maxs.slice(0, 5)) > Math.max(...maxs.slice(-5));
        const minUp   = Math.min(...mins.slice(0, 5)) < Math.min(...mins.slice(-5));
        
        if (maxDown && minUp) {
          markers.push({
            time:     candles[i].time,
            position: 'aboveBar',
            color:    '#ffa502',
            shape:    'circle',
            text:     'Conv',
            id:       `conv_${candles[i].time}`
          });
          i += 7;
        }
      }
      return markers;
    }
    case 'pattern_wedge': {
      const markers = [];
      if (candles.length < 40) return [];
      
      for (let i = 30; i < candles.length - 1; i++) {
        const slice = candles.slice(i-20, i);
        const maxs  = slice.map(c => c.high);
        const mins  = slice.map(c => c.low);
        
        // Rising Wedge: massimi salgono, minimi salgono più velocemente
        const highsUp = maxs[maxs.length-1] > maxs[0];
        const lowsUp  = mins[mins.length-1] > mins[0];
        if (highsUp && lowsUp && (mins[mins.length-1]-mins[0]) > (maxs[maxs.length-1]-maxs[0])) {
           markers.push({ time: candles[i].time, position: 'aboveBar', color: '#ff4757', shape: 'circle', text: 'Wedge', id: `wedge_${candles[i].time}` });
           i += 15;
        }
      }
      return markers;
    }
    case 'pattern_flag': {
      const markers = [];
      if (candles.length < 20) return [];
      for (let i = 15; i < candles.length; i++) {
        const prevMove = Math.abs(candles[i-5].close - candles[i-15].close);
        const currCons = Math.max(...highs.slice(i-5, i)) - Math.min(...lows.slice(i-5, i));
        if (currCons < prevMove * 0.3) {
          markers.push({ time: candles[i].time, position: 'belowBar', color: '#ffa502', shape: 'square', text: 'Flag', id: `flag_${candles[i].time}` });
          i += 10;
        }
      }
      return markers;
    }

    // -------------------------------------------------------
    // NUOVI INDICATORI TREND — Medie Mobili Extra
    // -------------------------------------------------------
    case 'sma_10': {
      const sma = calculateSMA(closes, 10);
      return sma.map((v, i) => ({ time: times[i + 9], value: v }));
    }
    case 'sma_100': {
      const sma = calculateSMA(closes, 100);
      return sma.map((v, i) => ({ time: times[i + 99], value: v }));
    }
    case 'ema_9': {
      const ema = calculateEMA(closes, 9);
      return ema.map((v, i) => ({ time: times[i], value: v }));
    }
    case 'ema_100': {
      const ema = calculateEMA(closes, 100);
      return ema.map((v, i) => ({ time: times[i], value: v }));
    }
    case 'ema_200': {
      const ema = calculateEMA(closes, 200);
      return ema.map((v, i) => ({ time: times[i], value: v }));
    }

    // Bollinger Bands (periodo 20, 2 deviazioni standard)
    case 'bollinger_upper':
    case 'bollinger_lower':
    case 'bollinger_mid': {
      if (closes.length < 20) return [];
      const period = 20;
      const result = [];
      for (let i = period - 1; i < closes.length; i++) {
        const slice = closes.slice(i - period + 1, i + 1);
        const mean  = slice.reduce((a, b) => a + b, 0) / period;
        const variance = slice.reduce((a, b) => a + (b - mean) ** 2, 0) / period;
        const std = Math.sqrt(variance);
        const val = toolId === 'bollinger_upper' ? mean + 2 * std
                  : toolId === 'bollinger_lower' ? mean - 2 * std
                  : mean;
        result.push({ time: times[i], value: val });
      }
      return result;
    }

    // Keltner Channel (EMA 20 ± ATR 14 * 1.5)
    case 'keltner_upper':
    case 'keltner_lower': {
      if (candles.length < 20) return [];
      const ema20 = calculateEMA(closes, 20);
      const atrArr = [];
      for (let i = 1; i < candles.length; i++) {
        atrArr.push(Math.max(
          highs[i] - lows[i],
          Math.abs(highs[i] - closes[i-1]),
          Math.abs(lows[i]  - closes[i-1])
        ));
      }
      const atrEma = calculateEMA(atrArr, 14);
      const result = [];
      for (let i = 0; i < atrEma.length; i++) {
        const emaVal = ema20[i + 1] || ema20[ema20.length - 1];
        const val = toolId === 'keltner_upper' ? emaVal + atrEma[i] * 1.5 : emaVal - atrEma[i] * 1.5;
        result.push({ time: times[i + 1], value: val });
      }
      return result;
    }

    // ATR Bands (chiusura ± ATR 14 * 2)
    case 'atr_upper':
    case 'atr_lower': {
      if (candles.length < 15) return [];
      const atrArr = [];
      for (let i = 1; i < candles.length; i++) {
        atrArr.push(Math.max(
          highs[i] - lows[i],
          Math.abs(highs[i] - closes[i-1]),
          Math.abs(lows[i]  - closes[i-1])
        ));
      }
      const atrEma = calculateEMA(atrArr, 14);
      const result = [];
      for (let i = 0; i < atrEma.length; i++) {
        const c = closes[i + 1];
        const val = toolId === 'atr_upper' ? c + atrEma[i] * 2 : c - atrEma[i] * 2;
        result.push({ time: times[i + 1], value: val });
      }
      return result;
    }

    // Ichimoku Kijun Sen (linea di base, media 26 periodi H+L/2)
    case 'ichimoku_kijun': {
      if (candles.length < 26) return [];
      const result = [];
      for (let i = 25; i < candles.length; i++) {
        const slice = candles.slice(i - 25, i + 1);
        const highest = Math.max(...slice.map(c => c.high));
        const lowest  = Math.min(...slice.map(c => c.low));
        result.push({ time: times[i], value: (highest + lowest) / 2 });
      }
      return result;
    }

    // Ichimoku Senkou A (media di Tenkan + Kijun, spostata 26 in avanti)
    case 'ichimoku_cloud_upper': {
      if (candles.length < 52) return [];
      const result = [];
      for (let i = 25; i < candles.length; i++) {
        const t9  = candles.slice(i - 8, i + 1);
        const t26 = candles.slice(i - 25, i + 1);
        const tenkan = (Math.max(...t9.map(c => c.high))  + Math.min(...t9.map(c => c.low)))  / 2;
        const kijun  = (Math.max(...t26.map(c => c.high)) + Math.min(...t26.map(c => c.low))) / 2;
        const futIdx  = i + 26 < candles.length ? i + 26 : candles.length - 1;
        result.push({ time: times[futIdx], value: (tenkan + kijun) / 2 });
      }
      return result;
    }

    // Ichimoku Senkou B (media di 52 periodi, spostata 26 in avanti)
    case 'ichimoku_cloud_lower': {
      if (candles.length < 78) return [];
      const result = [];
      for (let i = 51; i < candles.length; i++) {
        const t52 = candles.slice(i - 51, i + 1);
        const val = (Math.max(...t52.map(c => c.high)) + Math.min(...t52.map(c => c.low))) / 2;
        const futIdx = i + 26 < candles.length ? i + 26 : candles.length - 1;
        result.push({ time: times[futIdx], value: val });
      }
      return result;
    }

    // Donchian Channel
    case 'donchian_upper': {
      const period = 20;
      if (candles.length < period) return [];
      return candles.slice(period - 1).map((_, i) => ({
        time:  times[i + period - 1],
        value: Math.max(...highs.slice(i, i + period))
      }));
    }
    case 'donchian_lower': {
      const period = 20;
      if (candles.length < period) return [];
      return candles.slice(period - 1).map((_, i) => ({
        time:  times[i + period - 1],
        value: Math.min(...lows.slice(i, i + period))
      }));
    }

    // Regressione Lineare (canale)
    case 'linear_regression': {
      if (candles.length < 20) return [];
      const n = closes.length;
      const sumX  = (n * (n - 1)) / 2;
      const sumX2 = (n * (n - 1) * (2 * n - 1)) / 6;
      const sumY  = closes.reduce((a, b) => a + b, 0);
      const sumXY = closes.reduce((acc, v, i) => acc + i * v, 0);
      const m = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
      const b = (sumY - m * sumX) / n;
      return closes.map((_, i) => ({ time: times[i], value: m * i + b }));
    }

    // -------------------------------------------------------
    // NUOVI INDICATORI SR — Livelli aggiuntivi
    // -------------------------------------------------------
    case 'pivot_weekly': {
      // Pivot settimanale basato sull'ultima settimana disponibile
      const weekCandles = candles.slice(-5);
      const wH = Math.max(...weekCandles.map(c => c.high));
      const wL = Math.min(...weekCandles.map(c => c.low));
      const wC = weekCandles[weekCandles.length - 1].close;
      const P  = (wH + wL + wC) / 3;
      const R1 = 2 * P - wL;
      const S1 = 2 * P - wH;
      const R2 = P + (wH - wL);
      const S2 = P - (wH - wL);
      return [{ time: candles[0].time, levels: [
        { price: R2, level: 'WR2' }, { price: R1, level: 'WR1' },
        { price: P,  level: 'WPP' }, { price: S1, level: 'WS1' },
        { price: S2, level: 'WS2' },
      ]}];
    }
    case 'fib_extension': {
      // Fibonacci Extension dal minimo al massimo del periodo
      const maxH = Math.max(...highs);
      const minL = Math.min(...lows);
      const diff = maxH - minL;
      const levels = [1.272, 1.618, 2.0, 2.618].map(l => ({
        level: `Ext ${(l * 100).toFixed(1)}%`,
        price: maxH + diff * (l - 1),
      }));
      return [{ time: times[0], levels }];
    }
    case 'psych_levels': {
      // Livelli psicologici (numeri tondi) nell'intervallo del grafico
      const maxH = Math.max(...highs);
      const minL = Math.min(...lows);
      const step = Math.pow(10, Math.floor(Math.log10(maxH - minL))) / 2;
      const levels = [];
      let lvl = Math.ceil(minL / step) * step;
      while (lvl <= maxH) {
        levels.push({ price: Math.round(lvl * 100) / 100, level: lvl.toFixed(0) });
        lvl += step;
      }
      return levels.length ? [{ time: times[0], levels: levels.slice(0, 10) }] : [];
    }
    case 'psych_levels_fine': {
      // Livelli a semidecina (metà della distanza tra i livelli tondi)
      const maxH = Math.max(...highs);
      const minL = Math.min(...lows);
      const bigStep = Math.pow(10, Math.floor(Math.log10(maxH - minL))) / 2;
      const step = bigStep / 2;
      const levels = [];
      let lvl = Math.ceil(minL / step) * step;
      while (lvl <= maxH) {
        levels.push({ price: Math.round(lvl * 100) / 100, level: lvl.toFixed(0) });
        lvl += step;
      }
      return levels.length ? [{ time: times[0], levels: levels.slice(0, 14) }] : [];
    }
    case 'dynamic_support': {
      // Minimi di swing significativi come livelli orizzontali
      const levels = [];
      const lookback = 5;
      for (let i = lookback; i < candles.length - lookback; i++) {
        const slice = lows.slice(i - lookback, i + lookback + 1);
        const isSwingLow = lows[i] === Math.min(...slice);
        if (isSwingLow) levels.push({ price: lows[i], level: `S ${lows[i].toFixed(0)}` });
      }
      return levels.length ? [{ time: times[0], levels: levels.slice(0, 6) }] : [];
    }
    case 'dynamic_resistance': {
      // Massimi di swing significativi come livelli orizzontali
      const levels = [];
      const lookback = 5;
      for (let i = lookback; i < candles.length - lookback; i++) {
        const slice = highs.slice(i - lookback, i + lookback + 1);
        const isSwingHigh = highs[i] === Math.max(...slice);
        if (isSwingHigh) levels.push({ price: highs[i], level: `R ${highs[i].toFixed(0)}` });
      }
      return levels.length ? [{ time: times[0], levels: levels.slice(0, 6) }] : [];
    }
    case 'supply_zone': {
      // Zone di distribuzione: ultime 3 aree di massimo con inversione
      const levels = [];
      for (let i = 15; i < candles.length - 5; i++) {
        const slH = highs.slice(i - 5, i + 5);
        if (highs[i] === Math.max(...slH) && closes[i + 1] < closes[i] - (highs[i] - lows[i]) * 0.5) {
          const top = highs[i];
          const bot = highs[i] - (highs[i] - lows[i]) * 0.3;
          levels.push({ price: top, level: `S-Zone ${top.toFixed(0)}` });
          levels.push({ price: bot, level: '' });
          i += 10;
        }
      }
      return levels.length ? [{ time: times[0], levels: levels.slice(0, 6) }] : [];
    }
    case 'demand_zone': {
      // Zone di accumulazione: ultime 3 aree di minimo con rimbalzo
      const levels = [];
      for (let i = 15; i < candles.length - 5; i++) {
        const slL = lows.slice(i - 5, i + 5);
        if (lows[i] === Math.min(...slL) && closes[i + 1] > closes[i] + (highs[i] - lows[i]) * 0.5) {
          const bot = lows[i];
          const top = lows[i] + (highs[i] - lows[i]) * 0.3;
          levels.push({ price: bot, level: `D-Zone ${bot.toFixed(0)}` });
          levels.push({ price: top, level: '' });
          i += 10;
        }
      }
      return levels.length ? [{ time: times[0], levels: levels.slice(0, 6) }] : [];
    }

    // -------------------------------------------------------
    // NUOVI PATTERN CANDLESTICK
    // -------------------------------------------------------
    case 'pattern_doji': {
      const markers = [];
      for (let i = 0; i < candles.length; i++) {
        const body  = Math.abs(candles[i].close - candles[i].open);
        const range = candles[i].high - candles[i].low;
        if (range > 0 && body / range < 0.1) {
          markers.push({ time: candles[i].time, position: 'aboveBar', color: '#ffa502', shape: 'circle', text: 'Doji', id: `doji_${candles[i].time}` });
        }
      }
      return markers;
    }
    case 'pattern_hammer': {
      const markers = [];
      for (let i = 1; i < candles.length; i++) {
        const c    = candles[i];
        const body = Math.abs(c.close - c.open);
        const lowerWick = Math.min(c.open, c.close) - c.low;
        const upperWick = c.high - Math.max(c.open, c.close);
        const range = c.high - c.low;
        if (range > 0 && lowerWick >= body * 2 && upperWick < body * 0.5) {
          const isBull = closes[i - 1] > closes[i - 2] ? false : true;
          markers.push({ time: c.time, position: 'belowBar', color: isBull ? '#00d4aa' : '#ff4757', shape: 'arrowUp', text: isBull ? 'Hmr' : 'Hng', id: `hmr_${c.time}` });
        }
      }
      return markers;
    }
    case 'pattern_pin_bar': {
      const markers = [];
      for (let i = 0; i < candles.length; i++) {
        const c    = candles[i];
        const body = Math.abs(c.close - c.open);
        const range = c.high - c.low;
        const lowerWick = Math.min(c.open, c.close) - c.low;
        const upperWick = c.high - Math.max(c.open, c.close);
        if (range > 0 && (lowerWick >= range * 0.6 || upperWick >= range * 0.6) && body <= range * 0.25) {
          const isBullPin = lowerWick > upperWick;
          markers.push({ time: c.time, position: isBullPin ? 'belowBar' : 'aboveBar', color: isBullPin ? '#00d4aa' : '#ff4757', shape: isBullPin ? 'arrowUp' : 'arrowDown', text: 'Pin', id: `pin_${c.time}` });
        }
      }
      return markers;
    }
    case 'pattern_marubozu': {
      const markers = [];
      for (let i = 0; i < candles.length; i++) {
        const c    = candles[i];
        const body = Math.abs(c.close - c.open);
        const range = c.high - c.low;
        if (range > 0 && body / range > 0.9) {
          markers.push({ time: c.time, position: c.close > c.open ? 'belowBar' : 'aboveBar', color: c.close > c.open ? '#00d4aa' : '#ff4757', shape: 'square', text: 'Maru', id: `maru_${c.time}` });
        }
      }
      return markers;
    }
    case 'pattern_harami': {
      const markers = [];
      for (let i = 1; i < candles.length; i++) {
        const prev = candles[i - 1]; const curr = candles[i];
        const prevHigh = Math.max(prev.open, prev.close);
        const prevLow  = Math.min(prev.open, prev.close);
        const currHigh = Math.max(curr.open, curr.close);
        const currLow  = Math.min(curr.open, curr.close);
        if (currHigh < prevHigh && currLow > prevLow) {
          markers.push({ time: curr.time, position: 'aboveBar', color: '#fd9644', shape: 'circle', text: 'Hrm', id: `hrm_${curr.time}` });
        }
      }
      return markers;
    }
    case 'pattern_tweezer': {
      const markers = [];
      for (let i = 1; i < candles.length; i++) {
        const prev = candles[i - 1]; const curr = candles[i];
        const tollerance = (curr.high - curr.low) * 0.02;
        if (Math.abs(curr.high - prev.high) < tollerance && curr.close < prev.close) {
          markers.push({ time: curr.time, position: 'aboveBar', color: '#ff4757', shape: 'arrowDown', text: 'Twz', id: `twzt_${curr.time}` });
        }
        if (Math.abs(curr.low - prev.low) < tollerance && curr.close > prev.close) {
          markers.push({ time: curr.time, position: 'belowBar', color: '#00d4aa', shape: 'arrowUp', text: 'Twz', id: `twzb_${curr.time}` });
        }
      }
      return markers;
    }
    case 'pattern_morning_star': {
      const markers = [];
      for (let i = 2; i < candles.length; i++) {
        const [c1, c2, c3] = [candles[i-2], candles[i-1], candles[i]];
        const body2 = Math.abs(c2.close - c2.open);
        const body1 = Math.abs(c1.close - c1.open);
        // Morning Star: grande ribasso, piccolo corpo, grande rialzo
        if (c1.close < c1.open && body2 < body1 * 0.4 && c3.close > c3.open && c3.close > (c1.open + c1.close) / 2) {
          markers.push({ time: c3.time, position: 'belowBar', color: '#00d4aa', shape: 'arrowUp', text: '★ Morn', id: `mstar_${c3.time}` });
        }
        // Evening Star
        if (c1.close > c1.open && body2 < body1 * 0.4 && c3.close < c3.open && c3.close < (c1.open + c1.close) / 2) {
          markers.push({ time: c3.time, position: 'aboveBar', color: '#ff4757', shape: 'arrowDown', text: '★ Even', id: `estar_${c3.time}` });
        }
      }
      return markers;
    }
    case 'pattern_three_candles': {
      const markers = [];
      for (let i = 2; i < candles.length; i++) {
        const [c1, c2, c3] = [candles[i-2], candles[i-1], candles[i]];
        // Tre soldati bianchi
        if (c1.close > c1.open && c2.close > c2.open && c3.close > c3.open && c2.close > c1.close && c3.close > c2.close) {
          markers.push({ time: c3.time, position: 'belowBar', color: '#00d4aa', shape: 'arrowUp', text: '3Sol', id: `3s_${c3.time}` });
        }
        // Tre corvi neri
        if (c1.close < c1.open && c2.close < c2.open && c3.close < c3.open && c2.close < c1.close && c3.close < c2.close) {
          markers.push({ time: c3.time, position: 'aboveBar', color: '#ff4757', shape: 'arrowDown', text: '3Cor', id: `3c_${c3.time}` });
        }
      }
      return markers;
    }
    case 'pattern_inside_bar': {
      const markers = [];
      for (let i = 1; i < candles.length; i++) {
        const prev = candles[i - 1]; const curr = candles[i];
        if (curr.high < prev.high && curr.low > prev.low) {
          markers.push({ time: curr.time, position: 'aboveBar', color: '#74b9ff', shape: 'circle', text: 'IB', id: `ib_${curr.time}` });
        }
      }
      return markers;
    }
    case 'pattern_double_top': {
      const markers = [];
      if (candles.length < 30) return [];
      for (let i = 15; i < candles.length - 5; i++) {
        const leftH = Math.max(...highs.slice(i - 15, i - 5));
        const currH = highs[i];
        const toLer = leftH * 0.01;
        if (Math.abs(currH - leftH) < toLer && closes[i + 1] < currH * 0.99) {
          markers.push({ time: candles[i].time, position: 'aboveBar', color: '#e84393', shape: 'arrowDown', text: '2Top', id: `dt_${candles[i].time}` });
          i += 10;
        }
      }
      return markers;
    }
    case 'pattern_head_shoulders': {
      const markers = [];
      if (candles.length < 40) return [];
      for (let i = 20; i < candles.length - 10; i++) {
        const leftShoulder  = Math.max(...highs.slice(i - 20, i - 13));
        const head          = Math.max(...highs.slice(i - 13, i - 6));
        const rightShoulder = Math.max(...highs.slice(i - 6,  i));
        if (head > leftShoulder * 1.01 && head > rightShoulder * 1.01 && Math.abs(leftShoulder - rightShoulder) < leftShoulder * 0.03) {
          markers.push({ time: candles[i].time, position: 'aboveBar', color: '#fd79a8', shape: 'arrowDown', text: 'H&S', id: `hs_${candles[i].time}` });
          i += 20;
        }
      }
      return markers;
    }

    // -------------------------------------------------------
    // NUOVI PATTERN CANDLESTICK — Steve Nison (candele singole extra)
    // -------------------------------------------------------
    case 'pattern_shooting_star': {
      const markers = [];
      for (let i = 1; i < candles.length; i++) {
        const c = candles[i];
        const body = Math.abs(c.close - c.open);
        const range = c.high - c.low;
        const upperWick = c.high - Math.max(c.open, c.close);
        const lowerWick = Math.min(c.open, c.close) - c.low;
        if (range > 0 && upperWick >= body * 2 && lowerWick < body * 0.5 &&
            Math.min(c.open, c.close) > candles[i-1].close * 0.995) {
          markers.push({ time: c.time, position: 'aboveBar', color: '#ff4757', shape: 'arrowDown', text: 'ShStar', id: `ss_${c.time}` });
        }
      }
      return markers;
    }
    case 'pattern_inverted_hammer': {
      const markers = [];
      for (let i = 1; i < candles.length; i++) {
        const c = candles[i];
        const body = Math.abs(c.close - c.open);
        const range = c.high - c.low;
        const upperWick = c.high - Math.max(c.open, c.close);
        const lowerWick = Math.min(c.open, c.close) - c.low;
        // Inverted Hammer: ombra superiore lunga, corpo piccolo in basso, dopo downtrend
        if (range > 0 && upperWick >= body * 2 && lowerWick < body * 0.3 &&
            candles[i-1].close < candles[i-1].open) {
          markers.push({ time: c.time, position: 'belowBar', color: '#74b9ff', shape: 'arrowUp', text: 'IHmr', id: `ih_${c.time}` });
        }
      }
      return markers;
    }
    case 'pattern_gravestone_doji': {
      const markers = [];
      for (let i = 0; i < candles.length; i++) {
        const c = candles[i];
        const body = Math.abs(c.close - c.open);
        const range = c.high - c.low;
        const upperWick = c.high - Math.max(c.open, c.close);
        const lowerWick = Math.min(c.open, c.close) - c.low;
        if (range > 0 && body / range < 0.1 && upperWick >= range * 0.6 && lowerWick < range * 0.15) {
          markers.push({ time: c.time, position: 'aboveBar', color: '#ff4757', shape: 'arrowDown', text: 'GrvDoji', id: `gd_${c.time}` });
        }
      }
      return markers;
    }
    case 'pattern_dragonfly_doji': {
      const markers = [];
      for (let i = 0; i < candles.length; i++) {
        const c = candles[i];
        const body = Math.abs(c.close - c.open);
        const range = c.high - c.low;
        const upperWick = c.high - Math.max(c.open, c.close);
        const lowerWick = Math.min(c.open, c.close) - c.low;
        if (range > 0 && body / range < 0.1 && lowerWick >= range * 0.6 && upperWick < range * 0.15) {
          markers.push({ time: c.time, position: 'belowBar', color: '#00d4aa', shape: 'arrowUp', text: 'DrgnDoji', id: `df_${c.time}` });
        }
      }
      return markers;
    }
    case 'pattern_long_legged_doji': {
      const markers = [];
      for (let i = 0; i < candles.length; i++) {
        const c = candles[i];
        const body = Math.abs(c.close - c.open);
        const range = c.high - c.low;
        const upperWick = c.high - Math.max(c.open, c.close);
        const lowerWick = Math.min(c.open, c.close) - c.low;
        if (range > 0 && body / range < 0.1 && upperWick >= range * 0.3 && lowerWick >= range * 0.3) {
          markers.push({ time: c.time, position: 'aboveBar', color: '#ffd32a', shape: 'circle', text: 'LLDoji', id: `lld_${c.time}` });
        }
      }
      return markers;
    }
    case 'pattern_spinning_top': {
      const markers = [];
      for (let i = 0; i < candles.length; i++) {
        const c = candles[i];
        const body = Math.abs(c.close - c.open);
        const range = c.high - c.low;
        const upperWick = c.high - Math.max(c.open, c.close);
        const lowerWick = Math.min(c.open, c.close) - c.low;
        if (range > 0 && body / range < 0.3 && body / range > 0.1 &&
            upperWick > body * 0.5 && lowerWick > body * 0.5) {
          markers.push({ time: c.time, position: 'aboveBar', color: '#a29bfe', shape: 'circle', text: 'Spin', id: `sp_${c.time}` });
        }
      }
      return markers;
    }
    case 'pattern_belt_hold': {
      const markers = [];
      for (let i = 1; i < candles.length; i++) {
        const c = candles[i];
        const body = Math.abs(c.close - c.open);
        const range = c.high - c.low;
        if (range < body * 0.1) continue; // candela troppo piccola
        // Bullish Belt-Hold: open = low (nessuna ombra inferiore), candela rialzista lunga
        if (c.close > c.open && Math.abs(c.open - c.low) < range * 0.05 && body > range * 0.7) {
          markers.push({ time: c.time, position: 'belowBar', color: '#00d4aa', shape: 'arrowUp', text: 'BHBull', id: `bhb_${c.time}` });
        }
        // Bearish Belt-Hold: open = high, candela ribassista lunga
        if (c.close < c.open && Math.abs(c.high - c.open) < range * 0.05 && body > range * 0.7) {
          markers.push({ time: c.time, position: 'aboveBar', color: '#ff4757', shape: 'arrowDown', text: 'BHBear', id: `bhe_${c.time}` });
        }
      }
      return markers;
    }

    // -------------------------------------------------------
    // NUOVI PATTERN CANDLESTICK — Steve Nison (candele doppie extra)
    // -------------------------------------------------------
    case 'pattern_dark_cloud_cover': {
      const markers = [];
      for (let i = 1; i < candles.length; i++) {
        const prev = candles[i-1]; const curr = candles[i];
        const prevMid = (prev.open + prev.close) / 2;
        if (prev.close > prev.open &&           // prima candela rialzista
            curr.close < curr.open &&           // seconda ribassista
            curr.open > prev.close &&           // apre sopra il close di ieri
            curr.close < prevMid &&             // chiude oltre metà del corpo precedente
            curr.close > prev.open) {           // ma non sotto l'open precedente
          markers.push({ time: curr.time, position: 'aboveBar', color: '#d63031', shape: 'arrowDown', text: 'DCC', id: `dcc_${curr.time}` });
        }
      }
      return markers;
    }
    case 'pattern_piercing_line': {
      const markers = [];
      for (let i = 1; i < candles.length; i++) {
        const prev = candles[i-1]; const curr = candles[i];
        const prevMid = (prev.open + prev.close) / 2;
        if (prev.close < prev.open &&           // prima candela ribassista
            curr.close > curr.open &&           // seconda rialzista
            curr.open < prev.close &&           // apre sotto il close di ieri
            curr.close > prevMid &&             // chiude oltre metà del corpo precedente
            curr.close < prev.open) {           // ma non sopra l'open precedente
          markers.push({ time: curr.time, position: 'belowBar', color: '#00d4aa', shape: 'arrowUp', text: 'Pierce', id: `pl_${curr.time}` });
        }
      }
      return markers;
    }
    case 'pattern_harami_cross': {
      const markers = [];
      for (let i = 1; i < candles.length; i++) {
        const prev = candles[i-1]; const curr = candles[i];
        const currBody = Math.abs(curr.close - curr.open);
        const currRange = curr.high - curr.low;
        const prevHigh = Math.max(prev.open, prev.close);
        const prevLow  = Math.min(prev.open, prev.close);
        // Seconda candela è un doji contenuto nel corpo della prima
        if (currBody / (currRange || 1) < 0.1 &&
            Math.max(curr.open, curr.close) < prevHigh &&
            Math.min(curr.open, curr.close) > prevLow) {
          const isBull = prev.close < prev.open; // harami cross rialzista dopo trend ribassista
          markers.push({ time: curr.time, position: isBull ? 'belowBar' : 'aboveBar', color: isBull ? '#00d4aa' : '#ff4757', shape: isBull ? 'arrowUp' : 'arrowDown', text: 'HrmX', id: `hx_${curr.time}` });
        }
      }
      return markers;
    }
    case 'pattern_counterattack': {
      const markers = [];
      for (let i = 1; i < candles.length; i++) {
        const prev = candles[i-1]; const curr = candles[i];
        const tolerance = (curr.high - curr.low) * 0.02;
        if (Math.abs(curr.close - prev.close) < tolerance &&
            ((prev.close > prev.open && curr.close < curr.open) ||
             (prev.close < prev.open && curr.close > curr.open))) {
          const isBull = curr.close > curr.open;
          markers.push({ time: curr.time, position: isBull ? 'belowBar' : 'aboveBar', color: isBull ? '#00d4aa' : '#ff4757', shape: isBull ? 'arrowUp' : 'arrowDown', text: 'CntAtk', id: `ca_${curr.time}` });
        }
      }
      return markers;
    }
    case 'pattern_upside_gap_two_crows': {
      const markers = [];
      if (candles.length < 3) return [];
      for (let i = 2; i < candles.length; i++) {
        const [c1, c2, c3] = [candles[i-2], candles[i-1], candles[i]];
        // c1 rialzista, c2 gap up + ribassista, c3 ribassista che ingloba c2
        if (c1.close > c1.open &&
            c2.open > c1.close && c2.close < c2.open &&
            c3.open >= c2.open && c3.close < c2.close && c3.close < c3.open &&
            c3.close > c1.close) {
          markers.push({ time: c3.time, position: 'aboveBar', color: '#d63031', shape: 'arrowDown', text: 'UG2Cr', id: `ug2c_${c3.time}` });
        }
      }
      return markers;
    }

    // -------------------------------------------------------
    // NUOVI PATTERN CANDLESTICK — Steve Nison (candele triple extra)
    // -------------------------------------------------------
    case 'pattern_morning_doji_star': {
      const markers = [];
      if (candles.length < 3) return [];
      for (let i = 2; i < candles.length; i++) {
        const [c1, c2, c3] = [candles[i-2], candles[i-1], candles[i]];
        const body2 = Math.abs(c2.close - c2.open);
        const range2 = c2.high - c2.low;
        if (c1.close < c1.open &&                          // grande ribasso
            range2 > 0 && body2 / range2 < 0.1 &&         // doji
            c2.high < c1.close &&                          // gap down
            c3.close > c3.open &&                          // rialzo
            c3.close > (c1.open + c1.close) / 2) {        // chiude oltre metà c1
          markers.push({ time: c3.time, position: 'belowBar', color: '#55efc4', shape: 'arrowUp', text: '★MDS', id: `mds_${c3.time}` });
        }
      }
      return markers;
    }
    case 'pattern_evening_doji_star': {
      const markers = [];
      if (candles.length < 3) return [];
      for (let i = 2; i < candles.length; i++) {
        const [c1, c2, c3] = [candles[i-2], candles[i-1], candles[i]];
        const body2 = Math.abs(c2.close - c2.open);
        const range2 = c2.high - c2.low;
        if (c1.close > c1.open &&                          // grande rialzo
            range2 > 0 && body2 / range2 < 0.1 &&         // doji
            c2.low > c1.close &&                           // gap up
            c3.close < c3.open &&                          // ribasso
            c3.close < (c1.open + c1.close) / 2) {        // chiude sotto metà c1
          markers.push({ time: c3.time, position: 'aboveBar', color: '#e84393', shape: 'arrowDown', text: '★EDS', id: `eds_${c3.time}` });
        }
      }
      return markers;
    }
    case 'pattern_tasuki_gap': {
      const markers = [];
      if (candles.length < 3) return [];
      for (let i = 2; i < candles.length; i++) {
        const [c1, c2, c3] = [candles[i-2], candles[i-1], candles[i]];
        // Upward Tasuki Gap: c1 e c2 rialziste con gap, c3 ribassista che riempie parzialmente
        if (c1.close > c1.open && c2.close > c2.open &&
            c2.open > c1.close &&                          // gap up tra c1 e c2
            c3.close < c3.open &&                          // c3 ribassista
            c3.open < c2.close && c3.close > c1.close) {  // riempie parzialmente il gap
          markers.push({ time: c3.time, position: 'belowBar', color: '#fdcb6e', shape: 'arrowUp', text: 'TskU', id: `tsku_${c3.time}` });
        }
        // Downward Tasuki Gap: c1 e c2 ribassiste con gap, c3 rialzista
        if (c1.close < c1.open && c2.close < c2.open &&
            c2.open < c1.close &&                          // gap down
            c3.close > c3.open &&                          // c3 rialzista
            c3.open > c2.close && c3.close < c1.close) {  // riempie parzialmente il gap
          markers.push({ time: c3.time, position: 'aboveBar', color: '#fdcb6e', shape: 'arrowDown', text: 'TskD', id: `tskd_${c3.time}` });
        }
      }
      return markers;
    }
    case 'pattern_rising_three_methods': {
      const markers = [];
      if (candles.length < 5) return [];
      for (let i = 4; i < candles.length; i++) {
        const [c1, c2, c3, c4, c5] = [candles[i-4], candles[i-3], candles[i-2], candles[i-1], candles[i]];
        const body1 = Math.abs(c1.close - c1.open);
        const body5 = Math.abs(c5.close - c5.open);
        // Rising Three Methods: grande rialzo + 3 piccole ribassiste nel range + grande rialzo
        if (c1.close > c1.open && body1 > 0 &&
            c2.high < c1.high && c3.high < c1.high && c4.high < c1.high &&
            c5.close > c5.open && c5.close > c1.close && body5 > body1 * 0.7) {
          markers.push({ time: c5.time, position: 'belowBar', color: '#74b9ff', shape: 'arrowUp', text: 'R3M', id: `r3m_${c5.time}` });
        }
        // Falling Three Methods: grande ribasso + 3 piccole + grande ribasso
        if (c1.close < c1.open && body1 > 0 &&
            c2.low > c1.low && c3.low > c1.low && c4.low > c1.low &&
            c5.close < c5.open && c5.close < c1.close && body5 > body1 * 0.7) {
          markers.push({ time: c5.time, position: 'aboveBar', color: '#74b9ff', shape: 'arrowDown', text: 'F3M', id: `f3m_${c5.time}` });
        }
      }
      return markers;
    }
    case 'pattern_three_mountain_top': {
      const markers = [];
      if (candles.length < 30) return [];
      for (let i = 20; i < candles.length - 5; i++) {
        // Tre picchi approssimativamente allo stesso livello in una finestra
        const window = candles.slice(i - 20, i);
        const windowHighs = window.map(c => c.high);
        const maxH = Math.max(...windowHighs);
        // Conta picchi locali vicini al massimo
        let peaks = 0;
        for (let j = 2; j < window.length - 2; j++) {
          if (windowHighs[j] > windowHighs[j-1] && windowHighs[j] > windowHighs[j+1] &&
              windowHighs[j] > maxH * 0.97) {
            peaks++;
          }
        }
        if (peaks >= 3 && closes[i] < maxH * 0.97) {
          markers.push({ time: candles[i].time, position: 'aboveBar', color: '#ff4757', shape: 'arrowDown', text: '3Mtn', id: `3mt_${candles[i].time}` });
          i += 10;
        }
      }
      return markers;
    }

    // -------------------------------------------------------
    // PATTERN JOE ROSS — TLOC (La Legge dei Grafici)
    // -------------------------------------------------------
    case 'pattern_1_2_3_top': {
      const markers = [];
      if (candles.length < 15) return [];
      for (let i = 8; i < candles.length - 3; i++) {
        // Punto 1: massimo locale significativo
        const lookback = 6;
        const pt1H = Math.max(...highs.slice(i - lookback, i + 1));
        const pt1Idx = highs.lastIndexOf(pt1H, i);
        if (pt1Idx < i - lookback) continue;

        // Punto 2: ritracciamento dal punto 1 (almeno 38% del range)
        const pt2L = Math.min(...lows.slice(pt1Idx, i + 1));
        if (pt2L >= pt1H) continue;
        const retrace = (pt1H - pt2L) / pt1H;
        if (retrace < 0.02) continue; // ritracciamento minimo 2%

        // Punto 3: rimbalzo ma NON supera il punto 1
        const pt3H = Math.max(...highs.slice(pt1Idx, i + 1));
        if (pt3H >= pt1H) continue; // supera pt1 → non è un 1-2-3

        // Conferma: prezzo poi scende sotto punto 2
        if (closes[i] < pt2L) {
          markers.push({ time: candles[i].time, position: 'aboveBar', color: '#ff4757', shape: 'arrowDown', text: '1-2-3T', id: `123t_${candles[i].time}` });
          i += 5;
        }
      }
      return markers;
    }
    case 'pattern_1_2_3_bottom': {
      const markers = [];
      if (candles.length < 15) return [];
      for (let i = 8; i < candles.length - 3; i++) {
        const lookback = 6;
        const pt1L = Math.min(...lows.slice(i - lookback, i + 1));
        const pt1Idx = lows.lastIndexOf(pt1L, i);
        if (pt1Idx < i - lookback) continue;

        const pt2H = Math.max(...highs.slice(pt1Idx, i + 1));
        if (pt2H <= pt1L) continue;

        const pt3L = Math.min(...lows.slice(pt1Idx, i + 1));
        if (pt3L <= pt1L) continue; // scende sotto pt1 → non è un 1-2-3

        if (closes[i] > pt2H) {
          markers.push({ time: candles[i].time, position: 'belowBar', color: '#00d4aa', shape: 'arrowUp', text: '1-2-3B', id: `123b_${candles[i].time}` });
          i += 5;
        }
      }
      return markers;
    }
    case 'pattern_ledge': {
      const markers = [];
      if (candles.length < 8) return [];
      // ATR per soglia di congestione
      let atrSum = 0, atrCnt = 0;
      for (let j = 1; j < Math.min(20, candles.length); j++) {
        atrSum += Math.max(highs[j] - lows[j], Math.abs(highs[j] - closes[j-1]), Math.abs(lows[j] - closes[j-1]));
        atrCnt++;
      }
      const atr = atrCnt > 0 ? atrSum / atrCnt : 1;
      for (let i = 5; i < candles.length - 2; i++) {
        // Finestra di 4+ candele con range compresso < 30% ATR
        const w = candles.slice(i - 4, i + 1);
        const wHigh = Math.max(...w.map(c => c.high));
        const wLow  = Math.min(...w.map(c => c.low));
        if ((wHigh - wLow) < atr * 0.3) {
          // Breakout dalla congestione
          if (candles[i+1] && (candles[i+1].high > wHigh || candles[i+1].low < wLow)) {
            const isBullBreak = candles[i+1].high > wHigh;
            markers.push({ time: candles[i+1].time, position: isBullBreak ? 'belowBar' : 'aboveBar', color: '#ffd32a', shape: isBullBreak ? 'arrowUp' : 'arrowDown', text: 'Ledge', id: `ldg_${candles[i+1].time}` });
            i += 4;
          }
        }
      }
      return markers;
    }
    case 'pattern_trading_range': {
      const markers = [];
      if (candles.length < 15) return [];
      for (let i = 12; i < candles.length - 2; i++) {
        const w = candles.slice(i - 10, i + 1);
        const wHigh = Math.max(...w.map(c => c.high));
        const wLow  = Math.min(...w.map(c => c.low));
        const wRange = wHigh - wLow;
        const wMid = (wHigh + wLow) / 2;
        // Verifica oscillazione attorno alla media (trading range classico)
        let crossings = 0;
        for (let j = 1; j < w.length; j++) {
          if ((w[j-1].close < wMid && w[j].close > wMid) || (w[j-1].close > wMid && w[j].close < wMid)) crossings++;
        }
        if (crossings >= 3 && wRange / closes[i] < 0.06) {
          if (candles[i+1] && (candles[i+1].close > wHigh || candles[i+1].close < wLow)) {
            const isBull = candles[i+1].close > wHigh;
            markers.push({ time: candles[i+1].time, position: isBull ? 'belowBar' : 'aboveBar', color: '#74b9ff', shape: isBull ? 'arrowUp' : 'arrowDown', text: 'TRange', id: `tr_${candles[i+1].time}` });
            i += 8;
          }
        }
      }
      return markers;
    }
    case 'pattern_ross_hook': {
      const markers = [];
      if (candles.length < 10) return [];
      // Ross Hook: dopo un 1-2-3, prima barra che viola il punto 3 (nuovo max/min significativo)
      for (let i = 5; i < candles.length - 1; i++) {
        // Cerchiamo un massimo locale (punto 3 potenziale) nei 5 barre precedenti
        const recentHighs = highs.slice(i - 5, i);
        const recentLows  = lows.slice(i - 5, i);
        const pt3H = Math.max(...recentHighs);
        const pt3L = Math.min(...recentLows);

        // Bullish Ross Hook: candela corrente supera il recente massimo dopo consolidamento
        if (highs[i] > pt3H && closes[i] > pt3H) {
          markers.push({ time: candles[i].time, position: 'belowBar', color: '#f9ca24', shape: 'arrowUp', text: 'RHook↑', id: `rhb_${candles[i].time}` });
          i += 4;
        }
        // Bearish Ross Hook
        else if (lows[i] < pt3L && closes[i] < pt3L) {
          markers.push({ time: candles[i].time, position: 'aboveBar', color: '#f9ca24', shape: 'arrowDown', text: 'RHook↓', id: `rhs_${candles[i].time}` });
          i += 4;
        }
      }
      return markers;
    }
    case 'pattern_traders_trick': {
      const markers = [];
      if (candles.length < 8) return [];
      // TTE: barra che si avvicina al breakout senza ancora violarlo (segnale anticipato)
      for (let i = 4; i < candles.length - 1; i++) {
        const recentHighs = highs.slice(i - 4, i);
        const recentLows  = lows.slice(i - 4, i);
        const pt3H = Math.max(...recentHighs);
        const pt3L = Math.min(...recentLows);
        const tolerance = (pt3H - pt3L) * 0.005; // 0.5% di tolleranza

        // Candela che si avvicina al breakout rialzista
        if (highs[i] >= pt3H - tolerance && highs[i] < pt3H + tolerance && closes[i] > closes[i-1]) {
          markers.push({ time: candles[i].time, position: 'belowBar', color: '#6c5ce7', shape: 'circle', text: 'TTE↑', id: `tteb_${candles[i].time}` });
          i += 3;
        }
        // Candela che si avvicina al breakout ribassista
        else if (lows[i] <= pt3L + tolerance && lows[i] > pt3L - tolerance && closes[i] < closes[i-1]) {
          markers.push({ time: candles[i].time, position: 'aboveBar', color: '#6c5ce7', shape: 'circle', text: 'TTE↓', id: `ttes_${candles[i].time}` });
          i += 3;
        }
      }
      return markers;
    }

    // -------------------------------------------------------
    // PATTERN LARRY WILLIAMS
    // -------------------------------------------------------
    case 'pattern_oops': {
      const markers = [];
      if (candles.length < 2) return [];
      for (let i = 1; i < candles.length; i++) {
        const prev = candles[i-1]; const curr = candles[i];
        // Oops Bullish: open di oggi è SOTTO il minimo di ieri (gap down) → poi chiude nel range di ieri
        if (curr.open < prev.low && curr.close > prev.low) {
          markers.push({ time: curr.time, position: 'belowBar', color: '#00d4aa', shape: 'arrowUp', text: 'Oops↑', id: `oopsb_${curr.time}` });
        }
        // Oops Bearish: open di oggi è SOPRA il massimo di ieri (gap up) → poi chiude nel range di ieri
        if (curr.open > prev.high && curr.close < prev.high) {
          markers.push({ time: curr.time, position: 'aboveBar', color: '#ff4757', shape: 'arrowDown', text: 'Oops↓', id: `oopss_${curr.time}` });
        }
      }
      return markers;
    }
    case 'pattern_smash_day': {
      const markers = [];
      if (candles.length < 5) return [];
      // Smash Day: range eccezionale (>2× media), chiude vicino agli estremi opposti
      let avgRange = 0;
      for (let j = 0; j < 5; j++) avgRange += (highs[j] - lows[j]);
      avgRange /= 5;

      for (let i = 5; i < candles.length; i++) {
        let localAvg = 0;
        for (let j = i-5; j < i; j++) localAvg += (highs[j] - lows[j]);
        localAvg /= 5;

        const range = highs[i] - lows[i];
        const body  = Math.abs(closes[i] - candles[i].open);
        if (range > localAvg * 1.8 && body > range * 0.6) {
          const isBear = closes[i] < candles[i].open;
          markers.push({ time: candles[i].time, position: isBear ? 'aboveBar' : 'belowBar', color: isBear ? '#ff4757' : '#00d4aa', shape: isBear ? 'arrowDown' : 'arrowUp', text: 'SmDay', id: `sd_${candles[i].time}` });
        }
      }
      return markers;
    }
    case 'pattern_outside_day': {
      const markers = [];
      for (let i = 1; i < candles.length; i++) {
        const prev = candles[i-1]; const curr = candles[i];
        if (curr.high > prev.high && curr.low < prev.low) {
          const isBear = curr.close < curr.open;
          markers.push({ time: curr.time, position: isBear ? 'aboveBar' : 'belowBar', color: '#fd79a8', shape: isBear ? 'arrowDown' : 'arrowUp', text: 'OutDay', id: `od_${curr.time}` });
        }
      }
      return markers;
    }
    case 'pattern_volatility_breakout': {
      const markers = [];
      if (candles.length < 15) return [];
      // Volatility Breakout: close > open ± (ATR14 × 0.75)
      for (let i = 14; i < candles.length; i++) {
        let atrSum = 0;
        for (let j = i-13; j <= i; j++) {
          atrSum += Math.max(highs[j] - lows[j], Math.abs(highs[j] - closes[j-1]), Math.abs(lows[j] - closes[j-1]));
        }
        const atr14 = atrSum / 14;
        const openToday = candles[i].open;
        const target    = atr14 * 0.75;
        if (closes[i] > openToday + target) {
          markers.push({ time: candles[i].time, position: 'belowBar', color: '#f9ca24', shape: 'arrowUp', text: 'VBrk↑', id: `vbu_${candles[i].time}` });
        } else if (closes[i] < openToday - target) {
          markers.push({ time: candles[i].time, position: 'aboveBar', color: '#f9ca24', shape: 'arrowDown', text: 'VBrk↓', id: `vbd_${candles[i].time}` });
        }
      }
      return markers;
    }
    case 'pattern_short_term_pivot': {
      const markers = [];
      if (candles.length < 5) return [];
      // Williams Short-Term Pivot: massimo/minimo con 2 barre più basse/alte a destra e sinistra
      for (let i = 2; i < candles.length - 2; i++) {
        const isSwingHigh = highs[i] > highs[i-1] && highs[i] > highs[i-2] &&
                            highs[i] > highs[i+1] && highs[i] > highs[i+2];
        const isSwingLow  = lows[i]  < lows[i-1]  && lows[i]  < lows[i-2] &&
                            lows[i]  < lows[i+1]  && lows[i]  < lows[i+2];
        if (isSwingHigh) {
          markers.push({ time: candles[i].time, position: 'aboveBar', color: '#a29bfe', shape: 'circle', text: 'STP↑', id: `stph_${candles[i].time}` });
        }
        if (isSwingLow) {
          markers.push({ time: candles[i].time, position: 'belowBar', color: '#a29bfe', shape: 'circle', text: 'STP↓', id: `stpl_${candles[i].time}` });
        }
      }
      return markers;
    }

    // -------------------------------------------------------
    // ICHIMOKU TENKAN SEN (linea di conversione, 9 periodi)
    // -------------------------------------------------------
    case 'ichimoku_tenkan': {
      if (candles.length < 9) return [];
      const result = [];
      for (let i = 8; i < candles.length; i++) {
        const slice = candles.slice(i - 8, i + 1);
        const highest = Math.max(...slice.map(c => c.high));
        const lowest  = Math.min(...slice.map(c => c.low));
        result.push({ time: times[i], value: (highest + lowest) / 2 });
      }
      return result;
    }

    default:
      return [];
  }
}


// -------------------------------------------------------
// CROSSHAIR TOOLTIP
// -------------------------------------------------------
function handleCrosshairMove(param) {
  if (!param.point || !param.time || !chartState.mainSeries) return;

  // Normalizzazione del tempo (param.time può essere stringa 'YYYY-MM-DD', oggetto, o numero)
  let pTimeStr = "";
  if (typeof param.time === 'string') {
    pTimeStr = param.time; // '2026-03-17'
  } else if (typeof param.time === 'number') {
    pTimeStr = new Date(param.time * 1000).toISOString().split('T')[0];
  } else if (param.time.year) {
    pTimeStr = `${param.time.year}-${String(param.time.month).padStart(2, '0')}-${String(param.time.day).padStart(2, '0')}`;
  }

  let price;
  const data = param.seriesData.get(chartState.mainSeries);
  if (data) {
    price = (chartState.chartType === 'candlestick') ? data.close : data.value;
  }

  if (price !== undefined) {
    // Risoluzione marker su stesso asse temporale discriminando top/bottom
    const newsForDay = chartState.markers.filter(m => m.date === pTimeStr);

    let newsAtTime = null;
    if (newsForDay.length > 0) {
      if (newsForDay.length === 1) {
        newsAtTime = newsForDay[0];
      } else {
        try {
          const highY = chartState.mainSeries.priceToCoordinate((data.open !== undefined && data.high !== undefined) ? data.high : price);
          const lowY = chartState.mainSeries.priceToCoordinate((data.open !== undefined && data.low !== undefined) ? data.low : price);
          const midY = (highY + lowY) / 2;
          
          if (param.point.y > midY) {
            // Sotto la candela: priorità DuckDuckGo
            newsAtTime = newsForDay.find(m => m.provider === 'duckduckgo' || m.position === 'belowBar') || newsForDay[newsForDay.length-1];
          } else {
            // Sopra la candela: priorità Alpaca
            newsAtTime = newsForDay.find(m => m.provider !== 'duckduckgo' || m.position === 'aboveBar') || newsForDay[0];
          }
        } catch(e) {
          newsAtTime = newsForDay[0];
        }
      }
    }

    if (newsAtTime) {
      showNewsTooltip(newsAtTime, param.point);
    } else {
      hideNewsTooltip();
    }
  } else {
    hideNewsTooltip();
  }
}

// -------------------------------------------------------
// CLICK EVENT (APRI NEWS)
// -------------------------------------------------------
function handleChartClick(param) {
  if (!param.point || !param.time || !chartState.mainSeries) return;

  let pTimeStr = "";
  if (typeof param.time === 'string') {
    pTimeStr = param.time;
  } else if (typeof param.time === 'number') {
    pTimeStr = new Date(param.time * 1000).toISOString().split('T')[0];
  } else if (param.time.year) {
    pTimeStr = `${param.time.year}-${String(param.time.month).padStart(2, '0')}-${String(param.time.day).padStart(2, '0')}`;
  }

  let price;
  const data = param.seriesData.get(chartState.mainSeries);
  if (data) {
    price = (chartState.chartType === 'candlestick') ? data.close : data.value;
  }

  if (price !== undefined) {
    // Risoluzione clic discrimando top/bottom
    const newsForDay = chartState.markers.filter(m => m.date === pTimeStr);

    let newsAtTime = null;
    if (newsForDay.length > 0) {
      if (newsForDay.length === 1) {
        newsAtTime = newsForDay[0];
      } else {
        try {
          const highY = chartState.mainSeries.priceToCoordinate((data.open !== undefined && data.high !== undefined) ? data.high : price);
          const lowY = chartState.mainSeries.priceToCoordinate((data.open !== undefined && data.low !== undefined) ? data.low : price);
          const midY = (highY + lowY) / 2;
          
          if (param.point.y > midY) {
            newsAtTime = newsForDay.find(m => m.provider === 'duckduckgo' || m.position === 'belowBar') || newsForDay[newsForDay.length-1];
          } else {
            newsAtTime = newsForDay.find(m => m.provider !== 'duckduckgo' || m.position === 'aboveBar') || newsForDay[0];
          }
        } catch(e) {
          newsAtTime = newsForDay[0];
        }
      }
    }

    if (newsAtTime && newsAtTime.url) {
      // Apri il link in una nuova finestra
      window.open(newsAtTime.url, '_blank');
    }
  }
}

// -------------------------------------------------------
// TOOLTIP (Gestione visiva)
// -------------------------------------------------------
function showNewsTooltip(news, point) {
  let tooltip = document.getElementById('newsTooltip');
  if (!tooltip) {
    tooltip = document.createElement('div');
    tooltip.id = 'newsTooltip';
    tooltip.style.cssText = `
      position: absolute;
      background: #1a2234;
      border: 1px solid rgba(255,165,2,0.5);
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 12px;
      color: #e8eaed;
      max-width: 280px;
      z-index: 100;
      pointer-events: none;
      box-shadow: 0 4px 20px rgba(0,0,0,0.5);
      line-height: 1.5;
    `;
    document.getElementById('chartContainer').appendChild(tooltip);
  }

  const isDDG = news.provider === 'duckduckgo';
  const icon = isDDG ? '🌐' : '📰';
  const color = isDDG ? '#3fbef5' : '#ffa502'; // Celeste coerente per DDG
  
  tooltip.innerHTML = `
    <div style="color:${color};font-weight:700;margin-bottom:4px">${icon} ${news.date}</div>
    <div style="font-weight:600">${news.headline}</div>
    ${news.source ? `<div style="color:#6b7280;font-size:11px;margin-top:4px">Fonte: ${news.source}</div>` : ''}
    <div style="color:#3fbef5;font-size:10px;margin-top:8px;font-style:italic">🖱 Clicca sulla linea di questa candela per aprire l'articolo</div>
  `;

  const container = document.getElementById('chartContainer');
  const rect = container.getBoundingClientRect();
  let x = point.x + 10;
  let y = point.y + 10;

  if (x + 290 > rect.width) x = point.x - 300;
  if (y + 100 > rect.height) y = point.y - 110;

  tooltip.style.left = x + 'px';
  tooltip.style.top  = y + 'px';
  tooltip.style.display = 'block';
}

function hideNewsTooltip() {
  const tooltip = document.getElementById('newsTooltip');
  if (tooltip) tooltip.style.display = 'none';
}

// -------------------------------------------------------
// AGGIORNAMENTO PREZZO IN TOOLBAR
// -------------------------------------------------------
function updatePriceDisplay(price, change) {
  const priceEl  = document.getElementById('currentPrice');
  const changeEl = document.getElementById('priceChange');

  if (priceEl) priceEl.textContent = price.toLocaleString('it-IT', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 4
  });

  if (changeEl) {
    const pct = change !== 0 ? ((change / (price - change)) * 100).toFixed(2) : '0.00';
    changeEl.textContent = `${change >= 0 ? '+' : ''}${change.toFixed(2)} (${pct}%)`;
    changeEl.className = `price-change ${change >= 0 ? 'positive' : 'negative'}`;
  }
}

// -------------------------------------------------------
// PANNELLO OSCILLATORI
// -------------------------------------------------------

let oscillatorState = {
  chart:      null,          // Istanza LWC del pannello oscillatori
  series:     {},            // toolId → series LWC
  syncUnsub:  null,          // Unsubscribe sincronizzazione timeScale
  activeData: null,          // Ultimi candles caricati (per ricalcolo)
};

/**
 * Inizializza (o re-inizializza) il pannello oscillatori.
 * Viene chiamato la prima volta che un oscillatore viene attivato.
 */
function initOscillatorPanel() {
  const container = document.getElementById('oscillator-chart-container');
  if (!container) return false;

  // Mostra il pannello
  const panel = document.getElementById('oscillator-panel');
  if (panel) panel.style.display = 'flex';

  if (oscillatorState.chart) return true; // già inizializzato

  oscillatorState.chart = LightweightCharts.createChart(container, {
    layout: {
      background: { color: '#060b18' },
      textColor: '#9ca3af',
      fontSize: 10,
      fontFamily: "'Inter', sans-serif",
    },
    grid: {
      vertLines: { color: 'rgba(255,255,255,0.02)' },
      horzLines: { color: 'rgba(255,255,255,0.02)' },
    },
    crosshair: { mode: 1 },
    rightPriceScale: {
      borderColor: 'rgba(255,255,255,0.07)',
      textColor: '#9ca3af',
      scaleMargins: { top: 0.1, bottom: 0.1 },
    },
    timeScale: {
      borderColor: 'rgba(255,255,255,0.07)',
      textColor: '#9ca3af',
      timeVisible: true,
      secondsVisible: false,
    },
    handleScale: { axisPressedMouseMove: true },
    handleScroll: { mouseWheel: true, pressedMouseMove: true },
    width:  container.offsetWidth,
    height: container.offsetHeight,
  });

  // Sincronizzazione bidirezionale con il grafico principale
  if (chartState.chart) {
    const syncToMain = (range) => {
      if (range && chartState.chart) {
        try { chartState.chart.timeScale().setVisibleRange(range); } catch(_) {}
      }
    };
    const syncToOsc = (range) => {
      if (range && oscillatorState.chart) {
        try { oscillatorState.chart.timeScale().setVisibleRange(range); } catch(_) {}
      }
    };
    oscillatorState.chart.timeScale().subscribeVisibleTimeRangeChange(syncToMain);
    chartState.chart.timeScale().subscribeVisibleTimeRangeChange(syncToOsc);

    oscillatorState.syncUnsub = () => {
      try { oscillatorState.chart.timeScale().unsubscribeVisibleTimeRangeChange(syncToMain); } catch(_) {}
      try { chartState.chart.timeScale().unsubscribeVisibleTimeRangeChange(syncToOsc); } catch(_) {}
    };
  }

  // Resize observer
  const ro = new ResizeObserver(() => {
    if (oscillatorState.chart && container.offsetWidth > 0) {
      oscillatorState.chart.applyOptions({ width: container.offsetWidth, height: container.offsetHeight });
    }
  });
  ro.observe(container);

  return true;
}

/**
 * Calcola i dati di un oscillatore a partire dai candles OHLCV.
 * Restituisce array di {time, value}.
 */
function computeOscillatorData(toolId, candles) {
  if (!candles || candles.length === 0) return [];
  const closes = candles.map(c => c.close);
  const highs   = candles.map(c => c.high);
  const lows    = candles.map(c => c.low);
  const times   = candles.map(c => c.time);

  switch (toolId) {
    // ── RSI 14 (smoothing Wilder) ─────────────────────────────
    case 'rsi': {
      const period = 14;
      if (closes.length < period + 1) return [];
      const result = [];
      let avgGain = 0, avgLoss = 0;
      for (let i = 1; i <= period; i++) {
        const diff = closes[i] - closes[i-1];
        if (diff >= 0) avgGain += diff; else avgLoss -= diff;
      }
      avgGain /= period;
      avgLoss /= period;
      const rs0 = avgLoss === 0 ? 100 : avgGain / avgLoss;
      result.push({ time: times[period], value: 100 - (100 / (1 + rs0)) });
      for (let i = period + 1; i < closes.length; i++) {
        const diff = closes[i] - closes[i-1];
        const gain = diff > 0 ? diff : 0;
        const loss = diff < 0 ? -diff : 0;
        avgGain = (avgGain * (period - 1) + gain) / period;
        avgLoss = (avgLoss * (period - 1) + loss) / period;
        const rs = avgLoss === 0 ? 100 : avgGain / avgLoss;
        result.push({ time: times[i], value: Math.round((100 - (100 / (1 + rs))) * 100) / 100 });
      }
      return result;
    }

    // ── MACD Line (EMA12 - EMA26) ─────────────────────────────
    case 'macd_line': {
      if (closes.length < 26) return [];
      const ema12 = calculateEMA(closes, 12);
      const ema26 = calculateEMA(closes, 26);
      const result = [];
      for (let i = 0; i < ema26.length; i++) {
        result.push({ time: times[i], value: Math.round((ema12[i] - ema26[i]) * 10000) / 10000 });
      }
      return result;
    }

    // ── MACD Signal (EMA9 della MACD Line) ────────────────────
    case 'macd_signal': {
      if (closes.length < 35) return [];
      const ema12 = calculateEMA(closes, 12);
      const ema26 = calculateEMA(closes, 26);
      const macdLine = ema26.map((v, i) => ema12[i] - v);
      const signal = calculateEMA(macdLine, 9);
      return signal.map((v, i) => ({ time: times[i], value: Math.round(v * 10000) / 10000 }));
    }

    // ── Stochastic %K (14) ────────────────────────────────────
    case 'stochastic_k': {
      const period = 14;
      if (closes.length < period) return [];
      const result = [];
      for (let i = period - 1; i < closes.length; i++) {
        const sliceH = Math.max(...highs.slice(i - period + 1, i + 1));
        const sliceL = Math.min(...lows.slice(i - period + 1, i + 1));
        const range  = sliceH - sliceL;
        const k = range === 0 ? 50 : ((closes[i] - sliceL) / range) * 100;
        result.push({ time: times[i], value: Math.round(k * 100) / 100 });
      }
      return result;
    }

    // ── Stochastic %D (SMA3 di %K) ───────────────────────────
    case 'stochastic_d': {
      const period = 14;
      if (closes.length < period + 2) return [];
      const kValues = [];
      const kTimes  = [];
      for (let i = period - 1; i < closes.length; i++) {
        const sliceH = Math.max(...highs.slice(i - period + 1, i + 1));
        const sliceL = Math.min(...lows.slice(i - period + 1, i + 1));
        const range  = sliceH - sliceL;
        kValues.push(range === 0 ? 50 : ((closes[i] - sliceL) / range) * 100);
        kTimes.push(times[i]);
      }
      const result = [];
      for (let i = 2; i < kValues.length; i++) {
        const d = (kValues[i-2] + kValues[i-1] + kValues[i]) / 3;
        result.push({ time: kTimes[i], value: Math.round(d * 100) / 100 });
      }
      return result;
    }

    // ── Williams %R (14) ─────────────────────────────────────
    case 'williams_r': {
      const period = 14;
      if (closes.length < period) return [];
      const result = [];
      for (let i = period - 1; i < closes.length; i++) {
        const sliceH = Math.max(...highs.slice(i - period + 1, i + 1));
        const sliceL = Math.min(...lows.slice(i - period + 1, i + 1));
        const range  = sliceH - sliceL;
        const wr = range === 0 ? -50 : -100 * ((sliceH - closes[i]) / range);
        result.push({ time: times[i], value: Math.round(wr * 100) / 100 });
      }
      return result;
    }

    default:
      return [];
  }
}

/** Livelli di riferimento fissi per ogni oscillatore (linee orizzontali) */
const OSCILLATOR_LEVELS = {
  rsi:          [{ value: 70, label: '70', color: 'rgba(255,71,87,0.5)' },
                 { value: 50, label: '50', color: 'rgba(255,255,255,0.15)' },
                 { value: 30, label: '30', color: 'rgba(0,212,170,0.5)' }],
  macd_line:    [{ value: 0, label: '0', color: 'rgba(255,255,255,0.2)' }],
  macd_signal:  [{ value: 0, label: '0', color: 'rgba(255,255,255,0.2)' }],
  stochastic_k: [{ value: 80, label: '80', color: 'rgba(255,71,87,0.5)' },
                 { value: 50, label: '50', color: 'rgba(255,255,255,0.15)' },
                 { value: 20, label: '20', color: 'rgba(0,212,170,0.5)' }],
  stochastic_d: [{ value: 80, label: '80', color: 'rgba(255,71,87,0.5)' },
                 { value: 20, label: '20', color: 'rgba(0,212,170,0.5)' }],
  williams_r:   [{ value: -20,  label: '-20',  color: 'rgba(255,71,87,0.5)' },
                 { value: -50,  label: '-50',  color: 'rgba(255,255,255,0.15)' },
                 { value: -80,  label: '-80',  color: 'rgba(0,212,170,0.5)' }],
};

/**
 * Applica un oscillatore al pannello.
 * @param {string} toolId  - ID strumento (es. 'rsi')
 * @param {Array}  candles - Dati OHLCV
 * @param {string} color   - Colore HEX linea
 */
function applyOscillator(toolId, candles, color = '#74b9ff') {
  if (!initOscillatorPanel()) return;

  // Rimuovi se già presente
  removeOscillator(toolId);

  const data = computeOscillatorData(toolId, candles);
  if (!data || data.length === 0) return;

  const series = oscillatorState.chart.addLineSeries({
    color:          color,
    lineWidth:      1,
    priceLineVisible: false,
    lastValueVisible: true,
    title:          toolId.toUpperCase().replace('_', ' '),
  });
  series.setData(data);

  // Aggiungi livelli di riferimento orizzontali
  const levels = OSCILLATOR_LEVELS[toolId] || [];
  levels.forEach(lvl => {
    series.createPriceLine({
      price:            lvl.value,
      color:            lvl.color,
      lineWidth:        1,
      lineStyle:        2, // Dashed
      axisLabelVisible: true,
      title:            lvl.label,
    });
  });

  oscillatorState.series[toolId] = series;
  oscillatorState.activeData = candles;
}

/**
 * Rimuove un oscillatore dal pannello.
 * Se non ne rimangono altri, nasconde il pannello.
 */
function removeOscillator(toolId) {
  if (!oscillatorState.chart) return;
  const s = oscillatorState.series[toolId];
  if (s) {
    try { oscillatorState.chart.removeSeries(s); } catch(_) {}
    delete oscillatorState.series[toolId];
  }
  // Nascondi pannello se vuoto
  if (Object.keys(oscillatorState.series).length === 0) {
    const panel = document.getElementById('oscillator-panel');
    if (panel) panel.style.display = 'none';
  }
}

// Esportiamo le funzioni globali per l'uso da backtesting.js
window.TradingChart = {
  init:                    initChart,
  loadData:                loadChartData,
  switchType:              switchChartType,
  drawProjection:          drawProjection,
  clearProjection:         clearProjection,
  drawRealAfterProjection: drawRealAfterProjection,
  drawTradeLevels:         drawTradeLevels,
  clearTradeLevels:        clearTradeLevels,
  drawNewsMarkers:         drawNewsMarkers,
  clearNewsMarkers:        clearNewsMarkers,
  applyOverlay:            applyOverlay,
  removeOverlay:           removeOverlay,
  computeOverlayData:      computeOverlayData,
  applyVolumeProfile:      applyVolumeProfile,
  startFixedRangeSelection: startFixedRangeSelection,
  cancelFixedRangeSelection: cancelFixedRangeSelection,
  clearAnalysis:           clearAnalysis,
  clearQuickProjections:   clearQuickProjections,
  // Oscillatori
  applyOscillator:         applyOscillator,
  removeOscillator:        removeOscillator,
  computeOscillatorData:   computeOscillatorData,
};
