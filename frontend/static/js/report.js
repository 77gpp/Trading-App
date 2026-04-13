/**
 * report.js — Rendering del Report AI in HTML
 *
 * Converte il testo Markdown del report generato dagli agenti
 * in HTML formattato e lo inserisce nella sezione report della pagina.
 * Gestisce anche il box riassuntivo con i livelli di trading (Entry, SL, TP).
 */

// -------------------------------------------------------
// RENDER MARKDOWN → HTML (semplificato, senza librerie)
// -------------------------------------------------------
function renderMarkdown(mdText) {
  if (!mdText) return '';

  let html = mdText
    // Escape HTML base
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  // Ripristiniamo i > per i blockquote prima di processare
  html = mdText;

  // H1
  html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
  // H2
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  // H3
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');

  // Bold + Italic
  html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
  // Bold
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  // Italic
  html = html.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, '<em>$1</em>');

  // Code inline
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Blockquote (>[!NOTE], >[!IMPORTANT], >[!WARNING])
  html = html.replace(/^> \[!NOTE\]\s*\n((?:> .+\n?)+)/gm, (m, content) => {
    const text = content.replace(/^> ?/gm, '').trim();
    return `<blockquote class="alert-note">ℹ️ ${text}</blockquote>`;
  });
  html = html.replace(/^> \[!IMPORTANT\]\s*\n((?:> .+\n?)+)/gm, (m, content) => {
    const text = content.replace(/^> ?/gm, '').trim();
    return `<blockquote class="alert-important">⚠️ ${text}</blockquote>`;
  });
  html = html.replace(/^> \[!WARNING\]\s*\n((?:> .+\n?)+)/gm, (m, content) => {
    const text = content.replace(/^> ?/gm, '').trim();
    return `<blockquote class="alert-warning">🚨 ${text}</blockquote>`;
  });
  // Blockquote normale
  html = html.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>');

  // Liste non ordinate
  html = html.replace(/^\- (.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>\n?)+/g, m => `<ul>${m}</ul>`);

  // Liste ordinate
  html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');

  // Link Markdown
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" style="color:#3f8ef5">$1</a>');

  // HR
  html = html.replace(/^---$/gm, '<hr>');

  // Paragrafi (righe non vuote non già in tag)
  html = html.replace(/^([^<\n].+)$/gm, (m) => {
    if (m.trim().startsWith('<')) return m;
    return `<p>${m}</p>`;
  });

  // Puliamo doppie new-line eccessive
  html = html.replace(/\n{3,}/g, '\n\n');

  return html;
}

// -------------------------------------------------------
// RENDER COMPLETO DEL REPORT
// -------------------------------------------------------
function renderReport(reportMarkdown, tradeSetup, config) {
  const container = document.getElementById('reportContent');
  if (!container) return;

  container.innerHTML = '';
  container.classList.add('fade-in');

  // Box metriche Trade Setup
  if (tradeSetup) {
    const setupBox = buildTradeSetupBox(tradeSetup);
    container.appendChild(setupBox);
  }

  // Header del report
  if (config) {
    const headerEl = document.createElement('div');
    headerEl.style.cssText = `
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 0 16px;
      border-bottom: 1px solid rgba(255,255,255,0.07);
      margin-bottom: 16px;
    `;
    headerEl.innerHTML = `
      <div style="background:linear-gradient(135deg,#00d4aa,#3f8ef5);border-radius:8px;padding:8px 12px;font-size:18px;">📊</div>
      <div>
        <div style="font-size:16px;font-weight:800;color:#e8eaed">
          Backtesting: ${config.symbol}
        </div>
        <div style="font-size:12px;color:#6b7280">
          Periodo analisi: ${config.start} → ${config.end} · Generato il ${new Date().toLocaleDateString('it-IT')}
        </div>
      </div>
    `;
    container.appendChild(headerEl);
  }

  // Corpo del report in Markdown
  const bodyEl = document.createElement('div');
  bodyEl.innerHTML = renderMarkdown(reportMarkdown);
  container.appendChild(bodyEl);
}

// -------------------------------------------------------
// BOX TRADE SETUP (Entry, SL, TP, Direzione)
// -------------------------------------------------------
function buildTradeSetupBox(setup) {
  const { entry, stop_loss, take_profit_1, take_profit_2, direction } = setup;
  const isLong = direction === 'bullish';

  const box = document.createElement('div');
  box.className = 'trade-setup-box';
  box.innerHTML = `
    <div class="setup-metric">
      <div class="setup-metric-label">📍 Direzione</div>
      <div class="setup-metric-value ${isLong ? 'bullish' : 'bearish'}">
        ${isLong ? '▲ LONG' : '▼ SHORT'}
      </div>
    </div>
    <div class="setup-metric">
      <div class="setup-metric-label">🎯 Entry</div>
      <div class="setup-metric-value entry">${entry ? entry.toLocaleString('it-IT', {minimumFractionDigits:2,maximumFractionDigits:4}) : '—'}</div>
    </div>
    <div class="setup-metric">
      <div class="setup-metric-label">🛑 Stop Loss</div>
      <div class="setup-metric-value stop">${stop_loss ? stop_loss.toLocaleString('it-IT', {minimumFractionDigits:2,maximumFractionDigits:4}) : '—'}</div>
    </div>
    <div class="setup-metric">
      <div class="setup-metric-label">✅ Take Profit</div>
      <div class="setup-metric-value tp">
        <div>${take_profit_1 ? take_profit_1.toLocaleString('it-IT', {minimumFractionDigits:2,maximumFractionDigits:4}) : '—'}</div>
        ${take_profit_2 ? `<div style="font-size:11px;color:#00a884">${take_profit_2.toLocaleString('it-IT', {minimumFractionDigits:2,maximumFractionDigits:4})}</div>` : ''}
      </div>
    </div>
  `;
  return box;
}

// -------------------------------------------------------
// RENDER PLACEHOLDER (stato iniziale / caricamento)
// -------------------------------------------------------
function renderPlaceholder(message = 'Avvia il backtesting per vedere il report') {
  const container = document.getElementById('reportContent');
  if (!container) return;

  container.innerHTML = `
    <div class="report-placeholder">
      <div class="placeholder-icon">📋</div>
      <div class="placeholder-text">${message}</div>
    </div>
  `;
}

function renderError(message) {
  const container = document.getElementById('reportContent');
  if (!container) return;

  container.innerHTML = `
    <div class="report-placeholder">
      <div class="placeholder-icon">❌</div>
      <div class="placeholder-text" style="color:#ff4757">${message}</div>
    </div>
  `;
}

// -------------------------------------------------------
// EXPORT PER DOWNLOAD
// -------------------------------------------------------
function downloadReport(markdown, symbol) {
  const blob = new Blob([markdown], { type: 'text/markdown' });
  const url  = URL.createObjectURL(blob);
  const a    = document.createElement('a');
  a.href     = url;
  a.download = `BACKTEST_${symbol}_${new Date().toISOString().slice(0,10)}.md`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Esportiamo globalmente
window.TradingReport = {
  render:      renderReport,
  placeholder: renderPlaceholder,
  error:       renderError,
  download:    downloadReport,
};
