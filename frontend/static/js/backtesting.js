/**
 * backtesting.js — Logica principale della pagina Backtesting
 *
 * Gestisce:
 * - Form di configurazione (simbolo, date, timeframe, agenti)
 * - Chiamate API al backend Flask
 * - Polling del job di analisi AI
 * - Coordinamento con chart.js e report.js
 * - Parametri di calibrazione
 * - Overlay indicatori tecnici
 * - Toast notifications
 */

// -------------------------------------------------------
// STATO APPLICAZIONE
// -------------------------------------------------------
const App = {
  currentJob: null,    // ID del job di analisi in corso
  pollingInterval: null,    // Intervallo di polling
  currentData: [],      // Dati OHLCV caricati
  currentNews: [],      // Notizie caricate
  currentSymbol: 'GC=F',  // Ticker corrente
  showNews: false,   // Se mostrare notizie sul grafico
  calibrazione: {},      // Parametri calibrazione correnti
  volumeProfileData: null,  // Dati del Volume Profile calcolati dal backend
};

// -------------------------------------------------------
// DEFINIZIONE AGENTI E STRUMENTI
// -------------------------------------------------------
const AGENTS = {
  pattern: {
    name: 'Pattern Analyst',
    icon: '🔍',
    color: '#ff9f43',
    tools: [
      { id: 'pattern_engulfing', name: 'Bullish/Bearish Engulfing', defaultColor: '#ff9f43' },
      { id: 'pattern_triangle', name: 'Triangoli (Asc/Desc)', defaultColor: '#ee5a24' },
      { id: 'pattern_powerbar', name: 'Power Bars (Joe Ross)', defaultColor: '#f53b57' },
      { id: 'pattern_wedge', name: 'Wedge Rising/Falling', defaultColor: '#ff6b81' },
      { id: 'pattern_flag', name: 'Flag / Pennant', defaultColor: '#fd9644' },
    ]
  },
  trend: {
    name: 'Trend Analyst',
    icon: '📈',
    color: '#ffffff',
    tools: [
      { id: 'sma_20', name: 'SMA 20', defaultColor: '#ffffff' },
      { id: 'sma_50', name: 'SMA 50', defaultColor: '#ffffff' },
      { id: 'sma_200', name: 'SMA 200', defaultColor: '#ffffff' },
      { id: 'ema_20', name: 'EMA 20', defaultColor: '#ffffff' },
      { id: 'ema_50', name: 'EMA 50', defaultColor: '#ffffff' },
      { id: 'supertrend', name: 'SuperTrend', defaultColor: '#ffffff' },
    ]
  },
  sr: {
    name: 'SR Analyst',
    icon: '🎯',
    color: '#ffffff',
    tools: [
      { id: 'pivot_points', name: 'Pivot Points', defaultColor: '#ffffff' },
      { id: 'fib_retracement', name: 'Fibonacci Retracement', defaultColor: '#ffffff' },
      { id: 'psych_levels', name: 'Livelli Psicologici', defaultColor: '#ffffff' },
    ]
  },
  volume: {
    name: 'Volume Analyst',
    icon: '🌊',
    color: '#fd79a8',
    tools: [
      { id: 'volume_vsa', name: 'VSA Volume Bars', defaultColor: '#fd79a8' },
      { id: 'volume_profile', name: 'Volume Profile (VAP)', defaultColor: '#ff7f50' },
      { id: 'vwap', name: 'VWAP', defaultColor: '#e84393' },
    ]
  },
};

// -------------------------------------------------------
// INIZIALIZZAZIONE PAGINA
// -------------------------------------------------------
document.addEventListener('DOMContentLoaded', async () => {
  // 1. Inizializzazione grafico
  TradingChart.init('chartContainer');
  TradingReport.placeholder();

  // 2. Costruzione accordion agenti
  buildAgentAccordions();

  // 3. Carica parametri calibrazione dal backend
  await loadCalibrazioneFromBackend();

  // 4. Setup event listeners
  setupEventListeners();

  // 5. Imposta data default (ultimi 6 mesi)
  setDefaultDates();

  showToast('Sistema pronto. Seleziona uno strumento e avvia il backtesting.', 'info');
});

// -------------------------------------------------------
// DATE DEFAULT
// -------------------------------------------------------
function setDefaultDates() {
  const end = new Date();
  const start = new Date();
  start.setMonth(start.getMonth() - 6);

  document.getElementById('startDate').value = start.toISOString().slice(0, 10);
  document.getElementById('endDate').value = end.toISOString().slice(0, 10);
}

// -------------------------------------------------------
// COSTRUZIONE ACCORDION AGENTI
// -------------------------------------------------------

/**
 * Costruisce TUTTI gli accordion al caricamento pagina.
 * - Il Volume Analyst è SEMPRE staticamente presente.
 * - Gli altri 3 (Pattern, Trend, SR) partono con un placeholder
 *   e vengono ricostruiti dinamicamente dopo l'analisi AI.
 */
function buildAgentAccordions() {
  const container = document.getElementById('agentsContainer');
  if (!container) return;

  // 1. Costruiamo i 4 accordion dinamici con il placeholder
  const dynamicGroups = ['pattern', 'trend', 'sr', 'oscillator'];
  const dynamicMeta = {
    pattern: { name: 'Pattern Analyst', icon: '🔍', color: '#ff9f43' },
    trend: { name: 'Trend Analyst', icon: '📈', color: '#00d4aa' },
    sr: { name: 'SR Analyst', icon: '🎯', color: '#a29bfe' },
    oscillator: { name: 'Oscillatori', icon: '〰️', color: '#74b9ff' },
  };

  dynamicGroups.forEach(key => {
    const meta = dynamicMeta[key];
    const accordion = document.createElement('div');
    accordion.className = 'accordion';
    accordion.id = `accordion-${key}`;
    accordion.innerHTML = `
      <div class="accordion-header" onclick="toggleAccordion('${key}')">
        <div class="accordion-title">
          <span class="accordion-icon">${meta.icon}</span>
          <span>${meta.name}</span>
          <span id="badge-${key}" style="font-size:10px;background:rgba(59,130,246,0.18);padding:1px 6px;border-radius:4px;color:#60a5fa;margin-left:5px;display:none">AI ✦</span>
        </div>
        <div class="accordion-actions">
          <button class="btn-clear-agent" title="Deseleziona tutto" onclick="clearAgentTools(event, '${key}')">
            ✕
          </button>
          <span class="accordion-arrow">▼</span>
        </div>
      </div>
      <div class="accordion-body" id="body-${key}">
        <div style="text-align:center;color:#64748b;font-size:11px;font-style:italic;padding:14px 0;">
          Avvia il Backtesting AI per vedere gli strumenti scelti.
        </div>
      </div>
    `;
    container.appendChild(accordion);
  });

  // 2. Costruiamo il Volume Analyst STATICO (invariato)
  const volumeAgent = AGENTS.volume;
  const volAccordion = document.createElement('div');
  volAccordion.className = 'accordion';
  volAccordion.id = 'accordion-volume';
  volAccordion.innerHTML = `
    <div class="accordion-header" onclick="toggleAccordion('volume')">
      <div class="accordion-title">
        <span class="accordion-icon">${volumeAgent.icon}</span>
        <span>${volumeAgent.name}</span>
      </div>
      <div class="accordion-actions">
        <button class="btn-clear-agent" title="Deseleziona tutto" onclick="clearAgentTools(event, 'volume')">
          ✕
        </button>
        <span class="accordion-arrow">▼</span>
      </div>
    </div>
    <div class="accordion-body">
      ${volumeAgent.tools.map(tool => `
        <div class="tool-item-container" id="container-${tool.id}">
          <div class="tool-item">
            <label class="tool-checkbox-wrap">
              <input type="checkbox" class="tool-checkbox"
                     id="tool-${tool.id}"
                     data-tool-id="${tool.id}"
                     data-tool-name="${tool.name}"
                     data-agent="volume"
                     onchange="onToolToggle(this)">
              <span class="tool-name">${tool.name}</span>
            </label>
            <input type="color"
                   class="color-picker"
                   id="color-${tool.id}"
                   value="${tool.defaultColor}"
                   title="Colore indicatore"
                   onchange="onColorChange('${tool.id}')">
          </div>
          ${tool.id === 'volume_profile' ? `
            <div id="vap-extra-controls" class="tool-extra-panel" style="display:none;">
              <div class="form-group" style="margin-bottom: 0;">
                <label class="form-label" style="font-size: 10px; color: var(--text-muted);">MODALITÀ VAP</label>
                <select id="vap-mode" class="form-control" style="font-size: 11px; height: 26px; padding: 2px 5px;" onchange="refreshVap()">
                  <option value="visible">Range Visibile (Dinamico)</option>
                  <option value="fixed">Range Fisso (Avanzato)</option>
                  <option value="session">Sessione (Tutti i Giorni)</option>
                </select>
              </div>
              <div id="vap-fixed-range-controls" style="display:none; margin-top: 5px;">
                <button id="vap-select-range-btn" class="btn btn-sm btn-outline" style="width: 100%; font-size: 10px; padding: 2px;" onclick="enableFixedRangeSelection()">🎯 Seleziona Area su Grafico</button>
                <div id="vap-fixed-range-status" style="font-size: 10px; color: #ff9f43; text-align: center; margin-top: 3px; display: none;">Clicca candela INIZIO...</div>
              </div>
            </div>
          ` : ''}
        </div>
      `).join('')}
    </div>
  `;
  container.appendChild(volAccordion);
}

/**
 * Ricostruisce i 3 accordion dinamici (Pattern / Trend / SR)
 * con gli strumenti scelti dall'AI e li applica automaticamente al grafico.
 * @param {object} chosenTools - { pattern: [...], trend: [...], sr: [...] }
 */
function buildDynamicAccordions(chosenTools) {
  if (!chosenTools) return;

  // Rimuoviamo tutti i checkbox/overlay esistenti dei 4 gruppi dinamici
  ['pattern', 'trend', 'sr', 'oscillator'].forEach(key => {
    const oldBody = document.getElementById(`body-${key}`);
    if (oldBody) {
      oldBody.querySelectorAll('.tool-checkbox').forEach(cb => {
        if (cb.checked) {
          cb.checked = false;
          onToolToggle(cb, { silent: true });
        }
      });
    }
  });

  // Se l'AI ha fallito esplicitamente, mostriamo un avviso rosso in tutti gli accordion coinvolti
  if (chosenTools.success === false) {
    ['pattern', 'trend', 'sr', 'oscillator'].forEach(key => {
      const body = document.getElementById(`body-${key}`);
      const badge = document.getElementById(`badge-${key}`);
      if (body) {
        body.innerHTML = `
          <div style="text-align:center;color:#f87171;font-size:11px;padding:12px 8px;background:rgba(248,113,113,0.05);border-radius:6px;border:1px dashed rgba(248,113,113,0.3);margin:5px;line-height:1.4;">
             <div style="font-weight:bold;margin-bottom:4px;">❌ Analisi AI Fallita</div>
             <div style="font-size:10px;opacity:0.8;">${chosenTools.summary || "L'intelligenza artificiale non è riuscita a completare l'analisi tecnica."}</div>
             <div style="font-size:9px;margin-top:6px;color:#94a3b8;">Nessun indicatore suggerito (evitato fallback silenzioso).</div>
          </div>
        `;
      }
      if (badge) badge.style.display = 'none';
    });
    return;
  }

  // ── Pattern / Trend / SR: box con strumenti USATI NELL'ANALISI ──────────────
  ['pattern', 'trend', 'sr'].forEach(key => {
    const body = document.getElementById(`body-${key}`);
    const badge = document.getElementById(`badge-${key}`);
    if (!body) return;

    const appliedTechs = ((chosenTools.applied_techniques_per_domain || {})[key]) || [];
    body.innerHTML = buildAnalysisSection(key, appliedTechs, App.currentData, App.volumeProfileData);
    if (badge) badge.style.display = appliedTechs.length ? 'inline' : 'none';
  });

  // ── Oscillator: suggeriti dal SkillSelector per visualizzazione ──────────────
  {
    const body = document.getElementById('body-oscillator');
    const badge = document.getElementById('badge-oscillator');
    if (body) {
      const oscTools = (chosenTools['oscillator'] || []).filter(tool => {
        const d = TradingChart.computeOscillatorData(tool.id, App.currentData);
        return d && d.length > 0;
      });
      if (badge) badge.style.display = oscTools.length ? 'inline' : 'none';
      if (oscTools.length === 0) {
        body.innerHTML = `<div style="text-align:center;color:#64748b;font-size:11px;padding:10px 0;">Nessun oscillatore con segnale nel periodo.</div>`;
      } else {
        body.innerHTML = oscTools.map(tool => {
          const c = (tool.color || '').toLowerCase().trim();
          const col = (!c || c === '#000000' || c === '#000' || c === 'black') ? '#ffffff' : tool.color;
          return `
            <div class="tool-item-container" id="container-${tool.id}">
              <div class="tool-item">
                <label class="tool-checkbox-wrap">
                  <input type="checkbox" class="tool-checkbox"
                         id="tool-${tool.id}"
                         data-tool-id="${tool.id}"
                         data-tool-name="${tool.name}"
                         data-agent="oscillator"
                         onchange="onToolToggle(this)">
                  <span class="tool-name">${tool.name}</span>
                </label>
                <input type="color" class="color-picker"
                       id="color-${tool.id}"
                       value="${col}"
                       title="Colore indicatore"
                       onchange="onColorChange('${tool.id}')">
              </div>
              ${tool.reason ? `<div style="font-size:10px;color:#94a3b8;padding:2px 8px 6px 8px;line-height:1.35;border-left:2px solid rgba(148,163,184,0.2);margin-left:6px;"><span style="color:var(--primary);opacity:0.7">💡</span> ${tool.reason}</div>` : ''}
            </div>`;
        }).join('');
      }
    }
  }

  // ── Volume: box statico — appende la sezione "usati nell'analisi" ────────────
  {
    const volBody = document.getElementById('body-volume');
    if (volBody) {
      const prev = volBody.querySelector('.analysis-section');
      if (prev) prev.remove();
      const volApplied = ((chosenTools.applied_techniques_per_domain || {})['volume']) || [];
      if (volApplied.length > 0) {
        const html = buildAnalysisSection('volume', volApplied, App.currentData, App.volumeProfileData);
        if (html) {
          const wrapper = document.createElement('div');
          wrapper.className = 'analysis-section';
          wrapper.innerHTML = html;
          volBody.appendChild(wrapper);
        }
      }
    }
  }

  // ── Toast riepilogativo ──────────────────────────────────────────────────────
  const totalApplied = ['pattern', 'trend', 'sr', 'volume'].reduce((acc, d) => {
    return acc + ((chosenTools.applied_techniques_per_domain || {})[d] || []).length;
  }, 0);
  showToast(`📊 ${totalApplied} tecniche usate nell'analisi — attiva quelle grafiche per visualizzarle`, 'info', 6000);

  console.log('[APP] Accordion ricostruiti con tecniche effettivamente usate:', chosenTools);
}


/**
 * Costruisce la sezione HTML "📚 Tecniche dai Libri" per un box agente.
 * Mostra per ogni libro il nome breve, il numero di tecniche e un'anteprima.
 *
 * @param {string} domain - 'pattern' | 'trend' | 'sr' | 'volume'
 * @param {object} techPerDomain - chosenTools.techniques_per_domain dal backend
 * @returns {string} HTML della sezione, stringa vuota se non ci sono dati
 */
/**
 * Costruisce la sezione "📚 Tecniche dai Libri" per un box agente.
 *
 * Le tecniche con overlay_id vengono rese come checkbox togolabili sul grafico.
 * Le tecniche senza overlay_id (concettuali) vengono rese come badge informativi.
 * Le tecniche il cui overlay_id è già presente in shownOverlayIds (sezione grafica
 * principale) vengono saltate per evitare duplicati.
 *
 * @param {string}  domain          - 'pattern' | 'trend' | 'sr' | 'volume'
 * @param {object}  techPerDomain   - chosenTools.techniques_per_domain dal backend
 * @param {Set}     shownOverlayIds - overlay IDs già mostrati nella sezione grafica
 * @returns {string} HTML della sezione, '' se vuota
 */
/**
 * buildAnalysisSection — costruisce le sezioni di un accordion agente
 * mostrando ESCLUSIVAMENTE gli strumenti usati durante l'analisi AI.
 *
 * Sezione 1 — 📊 Strumenti grafici: tecniche con overlay_id e dati computabili
 *             → checkbox + color picker → attivabili sul grafico
 * Sezione 2 — 📚 Tecniche teoriche: tecniche senza overlay grafico o senza dati
 *             → badge informativi (non attivabili)
 *
 * @param {string} domain          - 'pattern'|'trend'|'sr'|'volume'
 * @param {Array}  appliedTechs    - [{name, overlay_id}] da applied_techniques_per_domain
 * @param {Array}  currentData     - candele correnti (per computeOverlayData)
 * @param {object} volumeProfileData
 */
function buildAnalysisSection(domain, appliedTechs, currentData, volumeProfileData) {
  if (!appliedTechs || appliedTechs.length === 0) {
    return `<div style="text-align:center;color:#64748b;font-size:11px;font-style:italic;padding:14px 0;">
              Avvia il Backtesting AI per vedere gli strumenti utilizzati nell'analisi.
            </div>`;
  }

  const visual = [];   // {name, overlayId} — rappresentabili sul grafico
  const conceptual = [];   // {name}            — puramente teorici
  const seenIds = new Set();

  for (const tech of appliedTechs) {
    const overlayId = tech.overlay_id || null;

    if (!overlayId) {
      conceptual.push({ name: tech.name });
      continue;
    }
    if (seenIds.has(overlayId)) continue;   // deduplication

    // Oscillatori: usa computeOscillatorData; overlay chart: usa computeOverlayData
    let hasData = false;
    if (OSCILLATOR_IDS.has(overlayId)) {
      const d = TradingChart.computeOscillatorData(overlayId, currentData);
      hasData = d && d.length > 0;
    } else {
      const d = TradingChart.computeOverlayData(overlayId, currentData, volumeProfileData);
      hasData = d && (Array.isArray(d) ? d.length > 0 : Object.keys(d).length > 0);
    }

    if (hasData) {
      seenIds.add(overlayId);
      visual.push({ name: tech.name, overlayId });
    } else {
      // overlay_id presente ma dati insufficienti nel periodo → badge teorico
      conceptual.push({ name: tech.name });
    }
  }

  // ── Sezione 1: Strumenti grafici ──────────────────────────────────────────
  let visualHtml = '';
  if (visual.length > 0) {
    const rows = visual.map(({ name, overlayId }) => `
      <div class="tool-item-container" id="container-${overlayId}">
        <div class="tool-item">
          <label class="tool-checkbox-wrap">
            <input type="checkbox" class="tool-checkbox"
                   id="tool-${overlayId}"
                   data-tool-id="${overlayId}"
                   data-tool-name="${name}"
                   data-agent="${domain}"
                   onchange="onToolToggle(this)">
            <span class="tool-name">${name}</span>
          </label>
          <input type="color" class="color-picker"
                 id="color-${overlayId}"
                 value="#ffffff"
                 title="Colore indicatore"
                 onchange="onColorChange('${overlayId}')">
        </div>
      </div>`).join('');

    visualHtml = `
      <div style="padding:4px 0 2px 0;">
        <div style="font-size:9px;color:#64748b;padding:3px 8px 5px 8px;
                    letter-spacing:0.05em;text-transform:uppercase;">
          📊 Strumenti grafici (${visual.length})
        </div>
        ${rows}
      </div>`;
  }

  // ── Sezione 2: Tecniche teoriche ──────────────────────────────────────────
  let conceptualHtml = '';
  if (conceptual.length > 0) {
    const badges = conceptual.map(({ name }) =>
      `<span style="display:inline-block;background:rgba(116,185,255,0.08);
               border:1px solid rgba(116,185,255,0.18);border-radius:3px;
               padding:1px 6px;margin:2px 2px;font-size:9px;color:#74b9ff;
               line-height:1.5;">${name}</span>`
    ).join('');

    conceptualHtml = `
      <div style="border-top:1px solid rgba(100,116,139,0.12);
                  margin-top:${visual.length ? '4px' : '0'};padding:6px 8px;">
        <div style="font-size:9px;color:#64748b;margin-bottom:4px;
                    letter-spacing:0.05em;text-transform:uppercase;">
          📚 Tecniche teoriche (${conceptual.length})
        </div>
        <div style="line-height:1.8;">${badges}</div>
      </div>`;
  }

  return visualHtml + conceptualHtml;
}


function toggleAccordion(agentKey) {
  const el = document.getElementById(`accordion-${agentKey}`);
  const isCurrentlyOpen = el.classList.contains('open');

  // Se stiamo per chiudere l'accordion (isCurrentlyOpen è true), resettiamo tutte le sottosezioni "Libri"
  if (isCurrentlyOpen) {
    const body = document.getElementById(`body-${agentKey}`);
    if (body) {
      const booksSection = body.querySelector('.books-section');
      if (booksSection) {
        // Seleziona tutti i div dentro .books-section
        const allDivs = booksSection.querySelectorAll('div');
        if (allDivs.length >= 2) {
          // Il secondo div (index 1) è il contenuto che vogliamo chiudere
          const booksContent = allDivs[1];
          booksContent.style.display = 'none';

          // Resetta il chevron a ▶ (chiuso)
          const chevron = booksSection.querySelector('.books-chevron');
          if (chevron) {
            chevron.textContent = '▶';
          }
        }
      }
    }
  }

  el.classList.toggle('open');
}

// -------------------------------------------------------
// TOGGLE OVERLAY INDICATORE
// -------------------------------------------------------
// Set degli ID appartenenti al gruppo oscillator (sincronizzato con AVAILABLE_TOOLS)
const OSCILLATOR_IDS = new Set(['rsi', 'macd_line', 'macd_signal', 'stochastic_k', 'stochastic_d', 'williams_r', 'mao']);

function onToolToggle(checkbox, options = {}) {
  const toolId = checkbox.dataset.toolId;
  const toolName = checkbox.dataset.toolName;
  const color = document.getElementById(`color-${toolId}`)?.value || '#ffffff';
  const isSilent = options.silent === true;

  // Gestione visibilità pannello extra VAP
  if (toolId === 'volume_profile') {
    const extraPanel = document.getElementById('vap-extra-controls');
    if (extraPanel) extraPanel.style.display = checkbox.checked ? 'block' : 'none';
  }

  if (checkbox.checked) {
    if (!App.currentData || App.currentData.length === 0) {
      if (!isSilent) showToast(`Carica prima i dati del grafico per applicare ${toolName}.`, 'warning');
      checkbox.checked = false;
      return;
    }

    if (toolId === 'volume_profile') {
      refreshVap();
    } else if (OSCILLATOR_IDS.has(toolId)) {
      // ── Oscillatore → pannello separato sotto il grafico ──
      TradingChart.applyOscillator(toolId, App.currentData, color);
      // Aggiorna label attivi nel pannello
      _updateOscillatorLabels();
      if (!isSilent) showToast(`${toolName} applicato`, 'success', 2000);
    } else {
      const data = TradingChart.computeOverlayData(toolId, App.currentData, App.volumeProfileData);
      const hasData = data && (Array.isArray(data) ? data.length > 0 : Object.keys(data).length > 0);

      if (hasData) {
        TradingChart.applyOverlay(toolId, toolName, color, data);
        if (!isSilent) showToast(`${toolName} applicato`, 'success', 2000);
      } else {
        if (!isSilent) showToast(`${toolName} consultato (nessun segnale nel periodo)`, 'info');
      }
    }
  } else {
    if (OSCILLATOR_IDS.has(toolId)) {
      TradingChart.removeOscillator(toolId);
      _updateOscillatorLabels();
    } else {
      TradingChart.removeOverlay(toolId);
    }
  }
}

/** Aggiorna le label degli oscillatori attivi nel header del pannello */
function _updateOscillatorLabels() {
  const container = document.getElementById('oscillator-active-labels');
  if (!container) return;
  const active = [...document.querySelectorAll('[data-tool-id]')]
    .filter(cb => OSCILLATOR_IDS.has(cb.dataset.toolId) && cb.checked)
    .map(cb => `<span style="padding:1px 6px;border-radius:3px;background:rgba(255,255,255,0.08);">${cb.dataset.toolName}</span>`);
  container.innerHTML = active.join('');
}

/**
 * Ricarica il Volume Profile in base alla modalità selezionata
 */
function refreshVap() {
  const checkbox = document.getElementById('tool-volume_profile');
  if (!checkbox || !checkbox.checked) return;

  const mode = document.getElementById('vap-mode').value;
  const color = document.getElementById('color-volume_profile').value;

  const fixedRangeCtrls = document.getElementById('vap-fixed-range-controls');
  if (fixedRangeCtrls) {
    if (mode === 'fixed') {
      fixedRangeCtrls.style.display = 'block';
    } else {
      fixedRangeCtrls.style.display = 'none';
      if (window.TradingChart && typeof TradingChart.cancelFixedRangeSelection === 'function') {
        TradingChart.cancelFixedRangeSelection();
      }
      const statusEl = document.getElementById('vap-fixed-range-status');
      if (statusEl) statusEl.style.display = 'none';
    }
  }

  // Chiamiamo il metodo del grafico passando le opzioni
  TradingChart.applyVolumeProfile(color, { mode });
}

function clearAgentTools(event, agentKey) {
  if (event) event.stopPropagation(); // Evita di chiudere/aprire l'accordion

  // Supporto per gruppi dinamici (pattern/trend/sr) e statici (volume)
  const body = document.getElementById(`body-${agentKey}`) ||
    (document.getElementById(`accordion-${agentKey}`)?.querySelector('.accordion-body'));

  if (body) {
    body.querySelectorAll('.tool-checkbox').forEach(cb => {
      if (cb.checked) {
        cb.checked = false;
        onToolToggle(cb, { silent: true });
      }
    });
    const groupNames = { pattern: 'Pattern Analyst', trend: 'Trend Analyst', sr: 'SR Analyst', volume: 'Volume Analyst' };
    showToast(`Tutti gli indicatori di ${groupNames[agentKey] || agentKey} rimossi`, 'info', 2000);
  }
}

function enableFixedRangeSelection() {
  const statusEl = document.getElementById('vap-fixed-range-status');
  const mode = document.getElementById('vap-mode').value;
  if (mode !== 'fixed') return;

  if (statusEl) {
    statusEl.style.display = 'block';
    statusEl.textContent = 'Clicca candela INIZIO...';
  }

  if (window.TradingChart && typeof TradingChart.startFixedRangeSelection === 'function') {
    TradingChart.startFixedRangeSelection((startInfo) => {
      // onFirstClick
      if (statusEl) statusEl.textContent = 'Clicca candela FINE...';
    }, (start, end) => {
      // onComplete
      if (statusEl) {
        statusEl.style.display = 'none';
      }
      refreshVap(); // Disegna il nuovo intervallo
    }, (msg) => {
      // onError
      if (statusEl) statusEl.textContent = msg;
    });
  }
}

function onColorChange(toolId) {
  const checkbox = document.getElementById(`tool-${toolId}`);
  if (checkbox?.checked) {
    // Riapplica con il nuovo colore
    onToolToggle(checkbox);
  }
}

// -------------------------------------------------------
// AUTOCOMPLETE SIMBOLO
// -------------------------------------------------------
function setupSymbolAutocomplete() {
  const input = document.getElementById('symbolInput');
  const list = document.getElementById('autocompleteList');
  if (!input || !list) return;

  let debounceTimer;

  input.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    const q = input.value.trim();

    if (q.length < 2) {
      list.style.display = 'none';
      return;
    }

    debounceTimer = setTimeout(async () => {
      try {
        const res = await fetch(`/api/data/search?q=${encodeURIComponent(q)}`);
        const data = await res.json();

        if (data.results && data.results.length > 0) {
          list.innerHTML = data.results.map(r => `
            <div class="autocomplete-item" onclick="selectSymbol('${r.ticker}', '${r.name}')">
              <span>${r.name}</span>
              <span class="autocomplete-ticker">${r.ticker}</span>
            </div>
          `).join('');
          list.style.display = 'block';
        } else {
          list.style.display = 'none';
        }
      } catch (e) {
        list.style.display = 'none';
      }
    }, 300);
  });

  // Chiudi autocomplete al click fuori
  document.addEventListener('click', e => {
    if (!input.contains(e.target) && !list.contains(e.target)) {
      list.style.display = 'none';
    }
  });
}

function selectSymbol(ticker, name) {
  const input = document.getElementById('symbolInput');
  const list = document.getElementById('autocompleteList');
  if (input) input.value = ticker;
  if (list) list.style.display = 'none';
  App.currentSymbol = ticker;
  updateTickerBadge(ticker);
}

function updateTickerBadge(ticker) {
  const badge = document.getElementById('tickerBadge');
  if (badge) badge.textContent = ticker;
}

// -------------------------------------------------------
// CARICAMENTO CALIBRAZIONE DAL BACKEND
// -------------------------------------------------------
async function loadCalibrazioneFromBackend() {
  try {
    const res = await fetch('/api/data/calibrazione');
    const data = await res.json();
    App.calibrazione = data;

    // Popoliamo i campi UI
    Object.entries(data).forEach(([key, val]) => {
      const el = document.getElementById(`calib-${key}`);
      if (!el) return;

      if (el.type === 'checkbox') {
        el.checked = val;
      } else if (el.tagName === 'SELECT') {
        el.value = val;
      } else {
        el.value = val;
      }
    });
  } catch (e) {
    console.warn('[APP] Impossibile caricare calibrazione:', e);
  }
}

function getCalibrazione() {
  const calib = {};
  const keys = [
    'LLM_PROVIDER', 'QWEN_THINKING_ENABLED',
    'DEFAULT_PROJECTION_DAYS',
    'ALPACA_NEWS_LIMIT', 'DUCKDUCKGO_NEWS_LIMIT', 'AGENT_MACRO_ENABLED',
    'AGENT_PATTERN_ENABLED', 'AGENT_TREND_ENABLED', 'AGENT_SR_ENABLED',
    'AGENT_VOLUME_ENABLED', 'TEMPERATURE_KNOWLEDGE_SEARCH',
    'TEMPERATURE_MACRO_EXPERT', 'TEMPERATURE_TECH_ORCHESTRATOR',
    'TEMPERATURE_TECH_SPECIALISTS', 'TEMPERATURE_SKILL_SELECTOR'
  ];

  keys.forEach(key => {
    const el = document.getElementById(`calib-${key}`);
    if (!el) return;
    if (el.type === 'checkbox') {
      calib[key] = el.checked;
    } else if (el.type === 'number') {
      // Usiamo parseFloat per le temperature (decimali) e parseInt per gli altri
      calib[key] = key.startsWith('TEMPERATURE') ? parseFloat(el.value) : parseInt(el.value);
      if (isNaN(calib[key])) calib[key] = 0;
    } else {
      calib[key] = el.value;
    }
  });

  return calib;
}

// -------------------------------------------------------
// EVENT LISTENERS
// -------------------------------------------------------
function setupEventListeners() {
  // Autocomplete simbolo
  setupSymbolAutocomplete();

  // Slider proiezione
  const projSlider = document.getElementById('projectionDays');
  const projValue = document.getElementById('projectionValue');
  if (projSlider && projValue) {
    projSlider.addEventListener('input', () => {
      projValue.textContent = projSlider.value + ' giorni';
    });
  }

  // Toggle tipo grafico
  document.querySelectorAll('[data-chart-type]').forEach(btn => {
    btn.addEventListener('click', () => {
      const type = btn.dataset.chartType;
      document.querySelectorAll('[data-chart-type]').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      TradingChart.switchType(type);
    });
  });

  // Toggle timeframe (Custom Dropdown)
  const tfDropdown = document.getElementById('timeframeDropdown');
  const tfTrigger = document.getElementById('timeframeTrigger');
  const tfMenu = document.getElementById('timeframeMenu');

  if (tfTrigger && tfMenu) {
    tfTrigger.addEventListener('click', (e) => {
      e.stopPropagation();
      tfDropdown.classList.toggle('open');
    });

    document.querySelectorAll('#timeframeMenu .dropdown-item').forEach(item => {
      item.addEventListener('click', () => {
        const value = item.dataset.value;
        const label = item.dataset.label;
        const code = item.querySelector('.item-code').textContent;

        // Aggiorna UI attiva
        document.querySelectorAll('#timeframeMenu .dropdown-item').forEach(i => i.classList.remove('active'));
        item.classList.add('active');

        // Aggiorna Trigger
        document.getElementById('currentTimeframeLabel').textContent = label;
        document.getElementById('currentTimeframeCode').textContent = code;

        // Chiudi menu
        tfDropdown.classList.remove('open');

        // Ricarica dati
        loadChartPreview();
      });
    });

    // Chiudi al click fuori
    document.addEventListener('click', () => {
      tfDropdown.classList.remove('open');
    });
  }

  // Toggle notizie
  const newsToggle = document.getElementById('showNewsToggle');
  if (newsToggle) {
    newsToggle.addEventListener('change', () => {
      App.showNews = newsToggle.checked;
      if (App.showNews && App.currentNews.length > 0) {
        TradingChart.drawNewsMarkers(App.currentNews);
      } else {
        TradingChart.clearNewsMarkers();
      }
    });
  }

  // Filtri Notizie Sidebar
  const newsSearchInput = document.getElementById('newsFilterSource');
  const newsDateInput = document.getElementById('newsFilterDate');

  if (newsSearchInput) {
    newsSearchInput.addEventListener('input', () => renderNewsSidebar());
  }
  if (newsDateInput) {
    newsDateInput.addEventListener('change', () => renderNewsSidebar());
  }




  // Toggle proiezioni rapide
  const quickProjToggle = document.getElementById('showQuickProjections');
  if (quickProjToggle) {
    quickProjToggle.addEventListener('change', async () => {
      if (quickProjToggle.checked) {
        if (App.currentData && App.currentData.length > 0) {
          const symbol = App.currentSymbol;
          const end = document.getElementById('endDate').value;
          const days = parseInt(document.getElementById('projectionDays')?.value || 30);

          await loadProjection(symbol, end, days);
          await loadRealAfterData(symbol, end);
        }
      } else {
        if (window.TradingChart && typeof TradingChart.clearQuickProjections === 'function') {
          TradingChart.clearQuickProjections();
        }
      }
    });
  }

  // Toggle calibrazione panel
  const calibBtn = document.getElementById('toggleCalibBtn');
  const calibPanel = document.getElementById('calibrationPanel');
  if (calibBtn && calibPanel) {
    calibBtn.addEventListener('click', () => {
      calibPanel.classList.toggle('open');
      calibBtn.querySelector('.calib-arrow').textContent =
        calibPanel.classList.contains('open') ? '▲' : '▼';
    });
  }

  // Pulsante AVVIA
  const runBtn = document.getElementById('runBacktestBtn');
  if (runBtn) runBtn.addEventListener('click', runBacktest);

  // Pulsante STOP
  const stopBtn = document.getElementById('stopBacktestBtn');
  if (stopBtn) stopBtn.addEventListener('click', stopBacktest);

  // Pulsante Solo Grafico (anteprima veloce senza AI)
  const previewBtn = document.getElementById('previewChartBtn');
  if (previewBtn) previewBtn.addEventListener('click', loadChartPreview);

  // Toggle Sidebar (Collapse/Expand)
  const appLayout = document.getElementById('appLayout');
  const collapseBtn = document.getElementById('sidebarCollapseBtn');
  const expandBtn = document.getElementById('sidebarExpandBtn');

  if (appLayout && collapseBtn && expandBtn) {
    const toggleSidebar = () => {
      appLayout.classList.toggle('sidebar-collapsed');

      // Piccolo trick: forziamo il resize del grafico dopo la transizione CSS
      // per assicurarci che Lightweight Charts si adatti al nuovo spazio.
      setTimeout(() => {
        window.dispatchEvent(new Event('resize'));
      }, 310); // leggermente più del tempo della transizione CSS (0.3s)
    };

    collapseBtn.addEventListener('click', toggleSidebar);
    expandBtn.addEventListener('click', toggleSidebar);
  }

  // Toggle Report Area (Minimizza/Fullscreen)
  const reportArea = document.getElementById('reportArea');
  const minBtn = document.getElementById('minimizeReportBtn');
  const fullBtn = document.getElementById('fullscreenReportBtn');

  if (reportArea && minBtn && fullBtn) {
    const triggerResize = () => {
      setTimeout(() => { window.dispatchEvent(new Event('resize')); }, 310);
    };

    minBtn.addEventListener('click', () => {
      reportArea.classList.remove('fullscreen');
      reportArea.classList.toggle('collapsed');
      triggerResize();
    });

    fullBtn.addEventListener('click', () => {
      reportArea.classList.remove('collapsed');
      reportArea.classList.toggle('fullscreen');
      triggerResize();
    });
  }

  // Pulsante Download Report
  const dlBtn = document.getElementById('downloadReportBtn');
  if (dlBtn) {
    dlBtn.addEventListener('click', () => {
      if (App.lastReport) {
        TradingReport.download(App.lastReport, App.currentSymbol);
      }
    });
  }

  // Input simbolo → aggiorna ticker badge
  const symbolInput = document.getElementById('symbolInput');
  if (symbolInput) {
    symbolInput.addEventListener('change', () => {
      App.currentSymbol = symbolInput.value.trim() || 'GC=F';
      updateTickerBadge(App.currentSymbol);
    });
  }
}

/**
 * Renderizza la lista delle notizie nella sidebar applicando i filtri.
 */
function renderNewsSidebar() {
  const container = document.getElementById('newsSidebarContainer');
  const countEl = document.getElementById('newsListCount');
  if (!container) return;

  const searchText = document.getElementById('newsFilterSource')?.value.toLowerCase() || "";
  const filterDate = document.getElementById('newsFilterDate')?.value || "";

  // Filtriamo l'array globale delle notizie
  const filtered = App.currentNews.filter(n => {
    const matchText = n.headline.toLowerCase().includes(searchText) ||
      (n.source && n.source.toLowerCase().includes(searchText));
    const matchDate = filterDate ? n.date === filterDate : true;
    return matchText && matchDate;
  });

  if (countEl) countEl.innerText = filtered.length;

  if (filtered.length === 0) {
    container.innerHTML = `<div style="text-align: center; color: #64748b; font-size: 12px; font-style: italic; padding: 20px 0;">Nessuna notizia trovata.</div>`;
    return;
  }

  container.innerHTML = filtered.map(n => {
    const isDDG = n.provider === 'duckduckgo';
    const accentColor = isDDG ? '#3fbef5' : '#ffa502';
    const icon = isDDG ? '🌐' : '📰';

    return `
      <div class="news-card" onclick="window.open('${n.url}', '_blank')" style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255,255,255,0.05); border-left: 3px solid ${accentColor}; border-radius: 6px; padding: 8px; cursor: pointer; transition: all 0.2s ease; position: relative; margin-bottom: 8px;">
        <div style="font-size: 10px; color: ${accentColor}; font-weight: bold; margin-bottom: 2px; display: flex; justify-content: space-between;">
           <span>${icon} ${n.date}</span>
           <span style="opacity: 0.7;">${n.source || 'News'}</span>
        </div>
        <div style="font-size: 11.5px; color: #e2e8f0; line-height: 1.3; font-weight: 500;">${n.headline}</div>
        <style>
          .news-card:hover { background: rgba(51, 65, 85, 0.8) !important; transform: translateX(2px); border-color: rgba(255,255,255,0.15) !important; }
        </style>
      </div>
    `;
  }).join('');
}

// -------------------------------------------------------
// ANTEPRIMA GRAFICO (senza analisi AI)
// -------------------------------------------------------
async function loadChartPreview() {
  const symbol = document.getElementById('symbolInput').value.trim() || 'GC=F';
  const start = document.getElementById('startDate').value;
  const end = document.getElementById('endDate').value;
  const interval = document.querySelector('#timeframeMenu .dropdown-item.active')?.dataset.value || '1d';

  if (!start || !end) {
    showToast('Seleziona le date di inizio e fine', 'warning');
    return;
  }

  App.currentSymbol = symbol;
  updateTickerBadge(symbol);

  // Pulizia analisi precedente (Stop Loss, Take Profit, vecchie proiezioni)
  if (window.TradingChart && typeof TradingChart.clearAnalysis === 'function') {
    TradingChart.clearAnalysis();
  }

  showChartLoader('Caricamento dati da Yahoo Finance...');

  try {
    // 1. Dati OHLCV
    const res = await fetch(
      `/api/data/chart?symbol=${encodeURIComponent(symbol)}&start=${start}&end=${end}&interval=${interval}`
    );
    const data = await res.json();

    if (data.error) {
      hideChartLoader();
      showToast(`Errore dati: ${data.error}`, 'error');
      return;
    }

    App.currentData = data.candles;
    App.volumeProfileData = data.volume_profile; // Salviamo il profilo calcolato dal server
    TradingChart.loadData(data.candles);

    // 2. Notizie Alpaca (background)
    loadNewsForChart(symbol, start, end);

    // 3. Proiezioni Veloci (Facoltative)
    const quickProjEnabled = document.getElementById('showQuickProjections')?.checked;

    if (quickProjEnabled) {
      // 3a. Proiezione statistica (solo se toggle attivo)
      await loadProjection(symbol, end, parseInt(document.getElementById('projectionDays')?.value || 30));
    }

    // 3b. Dati reali dopo la data di fine — SEMPRE se endDate < oggi
    const _endCheck = new Date(end);
    const _today = new Date();
    _today.setHours(0, 0, 0, 0);
    if (_endCheck < _today) {
      await loadRealAfterData(symbol, end);
    }

    hideChartLoader();
    showToast(`${data.candles.length} candele caricate per ${data.ticker}`, 'success');

  } catch (e) {
    hideChartLoader();
    showToast(`Errore di connessione: ${e.message}`, 'error');
  }
}

// -------------------------------------------------------
// CARICAMENTO NOTIZIE
// -------------------------------------------------------
async function loadNewsForChart(symbol, start, end) {
  try {
    const limit = document.getElementById('calib-ALPACA_NEWS_LIMIT')?.value || 300;
    const res = await fetch(
      `/api/data/news?symbol=${encodeURIComponent(symbol)}&start=${start}&end=${end}&limit=${limit}`
    );
    const data = await res.json();

    App.currentNews = data.news || [];

    // Renderizziamo subito la sidebar
    renderNewsSidebar();

    const isNewsEnabled = document.getElementById('showNewsToggle')?.checked || false;
    App.showNews = isNewsEnabled;

    if (App.showNews && App.currentNews.length > 0) {
      TradingChart.drawNewsMarkers(App.currentNews);
      showToast(`${App.currentNews.length} notizie caricate`, 'info', 3000);
    }
  } catch (e) {
    console.warn('[APP] Notizie non disponibili:', e);
  }
}

// -------------------------------------------------------
// PROIEZIONE FUTURA
// -------------------------------------------------------
async function loadProjection(symbol, endDate, days) {
  try {
    const res = await fetch('/api/backtest/projection', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ symbol, end: endDate, days })
    });
    const data = await res.json();

    if (data.projection && data.projection.length > 0) {
      TradingChart.drawProjection(data.projection);

      // Aggiorna leggenda
      updateLegend();
    }
  } catch (e) {
    console.warn('[APP] Proiezione non disponibile:', e);
  }
}

// -------------------------------------------------------
// DATI REALI DOPO LA DATA DI FINE (Verifica Proiezione)
// -------------------------------------------------------
async function loadRealAfterData(symbol, endDate) {
  try {
    // Scarichiamo i 60 giorni successivi alla data di fine per confronto
    const endDateObj = new Date(endDate);
    const realStart = new Date(endDate);
    realStart.setDate(realStart.getDate() + 1);
    let realEnd = new Date(endDateObj);
    realEnd.setDate(realEnd.getDate() + 90);

    if (realEnd > new Date()) {
      realEnd = new Date(); // clampa all'oggi completo (giorno + mese + anno)
    }

    if (realStart >= realEnd) return; // Non ci sono dati futuri disponibili

    const res = await fetch(
      `/api/data/chart?symbol=${encodeURIComponent(symbol)}&start=${realStart.toISOString().slice(0, 10)}&end=${realEnd.toISOString().slice(0, 10)}&interval=1d`
    );
    const data = await res.json();

    if (data.candles && data.candles.length > 0) {
      // Candela ponte: aggancia la linea blu all'ultima candela dell'analisi storica
      const lastCandle = App.currentData[App.currentData.length - 1];
      const bridgeCandle = { time: lastCandle.time, close: lastCandle.close };
      TradingChart.drawRealAfterProjection([bridgeCandle, ...data.candles]);
    }
  } catch (e) {
    console.warn('[APP] Dati reali post-backtest non disponibili:', e);
  }
}

// -------------------------------------------------------
// AVVIO ANALISI AI (BACKTESTING COMPLETO)
// -------------------------------------------------------
async function runBacktest() {
  const symbol = document.getElementById('symbolInput').value.trim() || 'GC=F';
  const start = document.getElementById('startDate').value;
  const end = document.getElementById('endDate').value;
  const projectionDays = parseInt(document.getElementById('projectionDays')?.value || 30);
  const interval = document.querySelector('#timeframeMenu .dropdown-item.active')?.dataset.value || '1d';

  if (!start || !end) {
    showToast('Seleziona le date di inizio e fine', 'warning');
    return;
  }

  if (new Date(start) >= new Date(end)) {
    showToast('La data di inizio deve essere precedente alla data di fine', 'warning');
    return;
  }

  // Prima carichiamo il grafico
  await loadChartPreview();

  // Poi avviamo l'analisi AI
  App.currentSymbol = symbol;

  const runBtn = document.getElementById('runBacktestBtn');
  const stopBtn = document.getElementById('stopBacktestBtn');

  if (runBtn) {
    runBtn.disabled = true;
    runBtn.innerHTML = '<span class="btn-spinner" style="width:16px;height:16px;border:2px solid #000;border-top-color:transparent;border-radius:50%;animation:spin .6s linear infinite;display:inline-block"></span> Analisi...';
  }

  if (stopBtn) {
    stopBtn.disabled = false;
  }

  TradingReport.placeholder('⏳ Analisi AI in corso... potrebbe richiedere 3-5 minuti.');

  try {
    const res = await fetch('/api/backtest/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        symbol,
        start,
        end,
        projection_days: projectionDays,
        interval,
        calibrazione: getCalibrazione()
      })
    });

    const data = await res.json();

    if (data.error) {
      showToast(`Errore: ${data.error}`, 'error');
      resetRunBtn();
      return;
    }

    App.currentJob = data.job_id;
    showToast(`Analisi avviata! Job ID: ${data.job_id.slice(0, 8)}...`, 'info');

    // Iniziamo il polling ogni 5 secondi
    startPolling(data.job_id, { symbol, start, end });

  } catch (e) {
    showToast(`Errore di connessione: ${e.message}`, 'error');
    resetRunButtons();
  }
}

/**
 * Ferma l'analisi AI corrente
 */
async function stopBacktest() {
  if (!App.currentJob) return;

  const jobId = App.currentJob;
  const stopBtn = document.getElementById('stopBacktestBtn');

  if (stopBtn) {
    stopBtn.disabled = true;
    stopBtn.innerHTML = '<span class="btn-spinner" style="width:16px;height:16px;border:2px solid #fff;border-top-color:transparent;border-radius:50%;animation:spin .6s linear infinite;display:inline-block"></span> Interruzione...';
  }

  try {
    const res = await fetch(`/api/backtest/cancel/${jobId}`, { method: 'POST' });
    const data = await res.json();

    if (data.status === 'cancelled') {
      clearInterval(App.pollingInterval);
      App.currentJob = null;

      TradingReport.placeholder('🛑 Analisi interrotta dall\'utente.');
      showToast('Analisi interrotta con successo', 'info');
      resetRunButtons();
    }
  } catch (e) {
    console.error('[APP] Stop Error:', e);
    showToast('Impossibile fermare l\'analisi lato server, interruzione locale...', 'warning');
    clearInterval(App.pollingInterval);
    resetRunButtons();
  }
}

// -------------------------------------------------------
// POLLING STATO JOB
// -------------------------------------------------------
function startPolling(jobId, config) {
  if (App.pollingInterval) clearInterval(App.pollingInterval);

  let elapsed = 0;
  const loader = document.getElementById('reportContent');

  App.pollingInterval = setInterval(async () => {
    elapsed += 5;
    if (loader) {
      loader.querySelector('.placeholder-text') &&
        (loader.querySelector('.placeholder-text').textContent =
          `⏳ Analisi AI in corso... (${elapsed}s) - potrebbe richiedere 3-5 minuti.`);
    }

    try {
      const res = await fetch(`/api/backtest/status/${jobId}`);
      const data = await res.json();

      if (data.status === 'done') {
        clearInterval(App.pollingInterval);

        // Salviamo il report
        App.lastReport = data.report;

        // Rendiamo il report
        TradingReport.render(data.report, data.trade_setup, config);

        // Disegnamo i livelli di trading sul grafico
        if (data.trade_setup) {
          TradingChart.drawTradeLevels(data.trade_setup);
        }

        // Aggiorniamo la proiezione
        if (data.projection && data.projection.candles) {
          TradingChart.drawProjection(data.projection.candles);
        }

        // *** NUOVO: Ricostruiamo gli accordion con gli strumenti scelti dall'AI ***
        if (data.chosen_tools && Object.keys(data.chosen_tools).length > 0) {
          buildDynamicAccordions(data.chosen_tools);
        }

        resetRunButtons();
        showToast('✅ Analisi completata! Report generato.', 'success', 5000);
        updateLegend();

      } else if (data.status === 'cancelled') {
        clearInterval(App.pollingInterval);
        TradingReport.placeholder('🛑 Analisi annullata.');
        resetRunButtons();
        showToast('L\'analisi è stata annullata.', 'info');

      } else if (data.status === 'error') {
        clearInterval(App.pollingInterval);
        TradingReport.error(`Errore durante l'analisi: ${data.error}`);
        resetRunButtons();
        showToast(`Errore analisi: ${data.error}`, 'error');
      }

    } catch (e) {
      console.error('[APP] Polling error:', e);
    }
  }, 5000);
}

function resetRunButtons() {
  const runBtn = document.getElementById('runBacktestBtn');
  const stopBtn = document.getElementById('stopBacktestBtn');

  if (runBtn) {
    runBtn.disabled = false;
    runBtn.innerHTML = '🚀 Start Analisi AI';
  }

  if (stopBtn) {
    stopBtn.disabled = true;
    stopBtn.innerHTML = '🛑 Stop Analisi AI';
  }
}

// -------------------------------------------------------
// CHART LOADER
// -------------------------------------------------------
function showChartLoader(message = 'Caricamento...') {
  const loader = document.getElementById('chartLoader');
  if (loader) {
    loader.classList.remove('hidden');
    const txt = loader.querySelector('.loader-text');
    if (txt) txt.textContent = message;
  }
}

function hideChartLoader() {
  const loader = document.getElementById('chartLoader');
  if (loader) loader.classList.add('hidden');
}

// -------------------------------------------------------
// LEGGENDA GRAFICO
// -------------------------------------------------------
function updateLegend() {
  const legend = document.getElementById('chartLegend');
  if (!legend) return;

  const items = [
    { color: '#3fbef5', label: 'Prezzo Storico', icon: '' },
    { color: '#BB86FC', label: 'Proiezione AI', icon: '', opacity: 0.8 },
    { color: '#3fbef5', label: 'Reale (verifica)', icon: '' },
    { color: '#FFFFFF', label: 'Entry', icon: '' },
    { color: '#CF6679', label: 'Stop Loss', icon: '' },
    { color: '#03F5A9', label: 'Take Profit', icon: '' },
    { color: '#ffa502', label: 'Notizia', icon: '📰 ' },
  ];

  legend.innerHTML = items.map(item => `
    <div class="legend-item">
      <div class="legend-color" 
           style="background:${item.color}; opacity:${item.opacity || 1};"></div>
      <span>${item.icon}${item.label}</span>
    </div>
  `).join('');
}

// -------------------------------------------------------
// TOAST NOTIFICATIONS
// -------------------------------------------------------
function showToast(message, type = 'info', duration = 4000) {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;

  const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
  toast.innerHTML = `<span>${icons[type] || 'ℹ️'}</span><span>${message}</span>`;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'slide-in-toast 0.3s ease reverse forwards';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}
