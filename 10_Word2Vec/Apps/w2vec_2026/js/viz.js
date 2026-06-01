/*
 * ============================================================================
 *  w2vec_2026 — Visualisierung (natives SVG + DOM, keine Bibliotheken)
 * ----------------------------------------------------------------------------
 *  Ansichten:
 *    1.  renderOneHotTable() — scrollbare, nicht veränderbare Datensatz-Tabelle
 *    1b. renderText()        — Beispieltext mit Sparse-Vektor-Tooltip je Token
 *    2.  renderNeuralNet()   — Netz; Gewichts-Overlay bei Hover über Neuronen
 *    3.  renderVectorDB()    — Vektor-Datenbank: Zahlen- oder Barcode-Modus (PuOr)
 *    4.  renderPCA()         — 2D-Projektion der Wortvektoren
 *    5.  renderLossChart()   — Echtzeit-Loss-Kurve (Kreuzentropie)
 *
 *  Alle Größen/Farben stammen aus CONFIG.layout.
 * ============================================================================
 */

const SVG_NS = 'http://www.w3.org/2000/svg';

/* Hilfsfunktion: SVG-Element mit Attributen erzeugen. */
function svgEl(name, attrs = {}) {
  const el = document.createElementNS(SVG_NS, name);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  return el;
}

/* Hilfsfunktion: HTML-Element mit Eigenschaften/Kindern erzeugen. */
function htmlEl(name, props = {}, children = []) {
  const el = document.createElement(name);
  for (const [k, v] of Object.entries(props)) {
    if (k === 'class') el.className = v;
    else if (k === 'text') el.textContent = v;
    else if (k === 'html') el.innerHTML = v;
    else el.setAttribute(k, v);
  }
  for (const c of children) el.appendChild(c);
  return el;
}

/* --- Farbabbildung -------------------------------------------------------- */
function _hexToRgb(hex) {
  const n = parseInt(hex.slice(1), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}
function _lerp(a, b, t) {
  const ca = _hexToRgb(a), cb = _hexToRgb(b);
  const r = Math.round(ca[0] + (cb[0] - ca[0]) * t);
  const g = Math.round(ca[1] + (cb[1] - ca[1]) * t);
  const bl = Math.round(ca[2] + (cb[2] - ca[2]) * t);
  return `rgb(${r},${g},${bl})`;
}
/* Sigmoid-basierte Farbe (negativ → blau, neutral → hell, positiv → rot). */
function valueToColor(x) {
  const c = CONFIG.layout.colors;
  const t = 1 / (1 + Math.exp(-5 * x));
  return t < 0.5
    ? _lerp(c.weightLow, c.weightMid, t * 2)
    : _lerp(c.weightMid, c.weightHigh, (t - 0.5) * 2);
}
/* PuOr-Diverging-Palette: t in [0,1] (0 = orange, 0.5 = neutral, 1 = violett). */
function puOrColor(t) {
  const stops = CONFIG.layout.colors.puOr;
  t = Math.max(0, Math.min(1, t));
  const x = t * (stops.length - 1);
  const i = Math.floor(x);
  if (i >= stops.length - 1) return _lerp(stops[stops.length - 1], stops[stops.length - 1], 0);
  return _lerp(stops[i], stops[i + 1], x - i);
}

/* --- Schwebendes Tooltip (für Token-Sparse-Vektoren) --------------------- */
let _tipEl = null;
function _tip() {
  if (!_tipEl) {
    _tipEl = document.createElement('div');
    _tipEl.className = 'float-tip';
    _tipEl.hidden = true;
    document.body.appendChild(_tipEl);
  }
  return _tipEl;
}
function showTip(html, x, y) { const t = _tip(); t.innerHTML = html; t.hidden = false; moveTip(x, y); }
function moveTip(x, y) { const t = _tip(); t.style.left = (x + 14) + 'px'; t.style.top = (y + 14) + 'px'; }
function hideTip() { if (_tipEl) _tipEl.hidden = true; }
function attachTip(el, htmlFn) {
  el.addEventListener('mouseenter', e => showTip(htmlFn(), e.clientX, e.clientY));
  el.addEventListener('mousemove', e => moveTip(e.clientX, e.clientY));
  el.addEventListener('mouseleave', hideTip);
}

/* ===========================================================================
 *  1. Datensatz-Tabelle (scrollbar, schreibgeschützt)
 *     je ZEILE: Ziel-Wort | summierter Kontext-Vektor (Zeilenvektor)
 * ======================================================================== */
function renderOneHotTable(container, vocab, dataset) {
  container.innerHTML = '';
  if (dataset.length === 0) return;

  const table = htmlEl('table', { class: 'onehot-table' });

  const head1 = htmlEl('tr');
  head1.appendChild(htmlEl('th', { class: 'corner', rowspan: '2', text: 'Ziel-Wort' }));
  head1.appendChild(htmlEl('th', { class: 'group group-context', colspan: String(vocab.length), text: 'Kontext-Vektor (summiert)' }));
  table.appendChild(head1);

  const head2 = htmlEl('tr');
  for (const w of vocab) {
    const th = htmlEl('th', { class: 'vocab-col' });
    th.appendChild(htmlEl('span', { class: 'vocab-vertical', text: w }));
    head2.appendChild(th);
  }
  table.appendChild(head2);

  dataset.forEach(row => {
    const tr = htmlEl('tr');
    tr.appendChild(htmlEl('td', { class: 'word', text: row.targetWord }));
    row.contextVec.forEach(v => tr.appendChild(
      htmlEl('td', { class: v ? 'on' : 'off', text: String(v) })));
    table.appendChild(tr);
  });

  container.appendChild(table);
}

/* ===========================================================================
 *  1b. Beispieltext — Tokens mit Position; Hover zeigt den Sparse-Vektor
 * ======================================================================== */
function renderText(container, tokens, vocab) {
  container.innerHTML = '';
  const index = new Map(vocab.map((w, i) => [w, i]));
  const V = vocab.length;

  const list = htmlEl('div', { class: 'token-list' });
  tokens.forEach((tok, i) => {
    const chip = htmlEl('span', { class: 'token-chip' });
    chip.appendChild(htmlEl('span', { class: 'token-pos', text: String(i + 1) }));
    chip.appendChild(htmlEl('span', { class: 'token-word', text: tok }));

    const idx = index.get(tok);
    attachTip(chip, () => {
      const vec = Array.from({ length: V }, (_, k) => (k === idx ? 1 : 0));
      return `<div class="tip-title">„${tok}" — Sparse-Vektor (one-hot)</div>` +
             `<div class="tip-sub">Position ${i + 1} · Vokabel-Index ${idx + 1} von ${V}</div>` +
             `<div class="tip-vec">[${vec.join(', ')}]</div>`;
    });
    list.appendChild(chip);
  });
  container.appendChild(list);
}

/* ===========================================================================
 *  2. Neuronales Netz
 *     links = Ziel-Wörter (Eingabe) · Mitte = Neuronen · rechts = Kontext
 *     Hover über ein Neuron blendet die Gewichte seiner Verbindungen ein.
 * ======================================================================== */
function renderNeuralNet(container, net, activeRow) {
  const cfg = CONFIG.layout.nn;
  const colors = CONFIG.layout.colors;
  const W = cfg.width;
  const V = net.V, hidden = net.H;
  // Höhe wächst mit der Wortzahl, damit die Beschriftungen lesbar bleiben.
  const H = Math.max(cfg.baseHeight, V * cfg.rowSpacing);

  container.innerHTML = '';
  const svg = svgEl('svg', {
    viewBox: `0 0 ${W} ${H}`,
    preserveAspectRatio: 'xMidYMid meet',
    class: 'nn-svg',
  });

  // Geometrie
  const inputX = W * cfg.inputXFrac;
  const outputX = W - inputX;
  const hiddenX = W / 2;
  const marginY = H * cfg.marginYFrac;
  const ioY = i => marginY + (H - 2 * marginY) * (V === 1 ? 0.5 : i / (V - 1));
  const hidY = j => marginY + (H - 2 * marginY) * (hidden === 1 ? 0.5 : j / (hidden - 1));

  // Neuronen-Radius: maximal cfg.neuronRadiusFrac · W, aber so verkleinert, dass
  // sich die Kreise auch bei vielen Wörtern (20–25) nicht überlappen. Bei wenigen
  // Wörtern bleibt der maximale Radius erhalten.
  const ioSpacing = (H - 2 * marginY) / Math.max(1, V - 1);
  const hidSpacing = (H - 2 * marginY) / Math.max(1, hidden - 1);
  const r = Math.min(
    W * cfg.neuronRadiusFrac,
    cfg.neuronSpacingFrac * ioSpacing,
    cfg.neuronSpacingFrac * hidSpacing
  );

  const activeTarget = activeRow ? activeRow.targetIdx : -1;
  const isContext = i => activeRow ? activeRow.contextVec[i] > 0 : false;

  // Kanten W_in (Ziel → versteckt)
  for (let i = 0; i < V; i++) {
    const active = i === activeTarget;
    for (let j = 0; j < hidden; j++) {
      svg.appendChild(svgEl('line', {
        x1: inputX + r, y1: ioY(i), x2: hiddenX - r, y2: hidY(j),
        stroke: active ? valueToColor(net.W_in[i][j]) : '#d7d7d7',
        'stroke-width': active ? 4 : 1, opacity: active ? 1 : 0.45,
      }));
    }
  }
  // Kanten W_out (versteckt → Kontext)
  for (let i = 0; i < V; i++) {
    const active = isContext(i);
    for (let j = 0; j < hidden; j++) {
      svg.appendChild(svgEl('line', {
        x1: hiddenX + r, y1: hidY(j), x2: outputX - r, y2: ioY(i),
        stroke: active ? valueToColor(net.W_out[i][j]) : '#d7d7d7',
        'stroke-width': active ? 4 : 1, opacity: active ? 1 : 0.45,
      }));
    }
  }

  // Hover-Ebene (oben liegend) für die Gewichts-Overlays
  const hoverLayer = svgEl('g', { class: 'hover-layer' });

  // Hilfsfunktion: Neuron als Gruppe (Kreis + optionale Beschriftung).
  // Aktive Neuronen (aktuelles Ziel / aktuelle Kontextwörter) erhalten statt
  // eines Pfeils eine rote Umrandung.
  function neuron(cx, cy, fill, label, anchor, active) {
    const g = svgEl('g', { class: 'neuron' });
    g.appendChild(svgEl('circle', {
      cx, cy, r, fill,
      stroke: active ? colors.highlight : '#666',
      'stroke-width': active ? 4 : 2,
      style: 'cursor:pointer',
    }));
    if (label !== undefined) {
      const dx = anchor === 'end' ? -r * 1.4 : r * 1.4;
      const t = svgEl('text', {
        x: cx + dx, y: cy, 'text-anchor': anchor,
        'dominant-baseline': 'middle', 'font-size': cfg.labelFontPx,
        fill: anchor === 'end' ? colors.inputWord : colors.contextWord,
      });
      t.textContent = label;
      g.appendChild(t);
    }
    svg.appendChild(g);
    return g;
  }

  // Gewichts-Overlay zeichnen
  function clearHover() { while (hoverLayer.firstChild) hoverLayer.removeChild(hoverLayer.firstChild); }
  function olEdge(x1, y1, x2, y2, w) {
    hoverLayer.appendChild(svgEl('line', {
      x1, y1, x2, y2, stroke: valueToColor(w), 'stroke-width': 3, opacity: 0.95,
    }));
  }
  function olLabel(x, y, w, anchor) {
    const t = svgEl('text', {
      x, y, 'text-anchor': anchor || 'middle', 'dominant-baseline': 'middle',
      'font-size': cfg.weightFontPx, fill: '#111',
      'paint-order': 'stroke', stroke: '#fff', 'stroke-width': 3,
    });
    t.textContent = w.toFixed(2);
    hoverLayer.appendChild(t);
  }
  function showWeights(type, idx) {
    clearHover();
    if (type === 'input') {
      for (let j = 0; j < hidden; j++) {
        olEdge(inputX + r, ioY(idx), hiddenX - r, hidY(j), net.W_in[idx][j]);
        olLabel(hiddenX - r * 2.4, hidY(j), net.W_in[idx][j], 'end');
      }
    } else if (type === 'output') {
      for (let j = 0; j < hidden; j++) {
        olEdge(hiddenX + r, hidY(j), outputX - r, ioY(idx), net.W_out[idx][j]);
        olLabel(hiddenX + r * 2.4, hidY(j), net.W_out[idx][j], 'start');
      }
    } else { // hidden: ein- UND ausgehende Gewichte
      for (let i = 0; i < V; i++) {
        olEdge(inputX + r, ioY(i), hiddenX - r, hidY(idx), net.W_in[i][idx]);
        olLabel(inputX + r * 2.4, ioY(i), net.W_in[i][idx], 'start');
        olEdge(hiddenX + r, hidY(idx), outputX - r, ioY(i), net.W_out[i][idx]);
        olLabel(outputX - r * 2.4, ioY(i), net.W_out[i][idx], 'end');
      }
    }
  }
  function bindHover(g, type, idx) {
    g.addEventListener('mouseenter', () => showWeights(type, idx));
    g.addEventListener('mouseleave', clearHover);
  }

  // Eingabe-Neuronen (Ziel-Wörter); aktuelles Ziel: rote Umrandung
  for (let i = 0; i < V; i++) {
    const fill = valueToColor(net.W_in[i].reduce((a, b) => a + b, 0) / net.H);
    bindHover(neuron(inputX, ioY(i), fill, net.vocab[i], 'end', i === activeTarget), 'input', i);
  }
  // versteckte Neuronen
  for (let j = 0; j < hidden; j++) {
    const val = activeRow ? (net.W_in[activeTarget] && net.W_in[activeTarget][j]) : 0;
    bindHover(neuron(hiddenX, hidY(j), valueToColor(val || 0), undefined, null, false), 'hidden', j);
  }
  // Ausgabe-Neuronen (Kontext-Wörter); aktuelle Kontextwörter: rote Umrandung
  for (let i = 0; i < V; i++) {
    const fill = valueToColor(net.W_out[i].reduce((a, b) => a + b, 0) / net.H);
    bindHover(neuron(outputX, ioY(i), fill, net.vocab[i], 'start', isContext(i)), 'output', i);
  }

  // Spaltenüberschriften inkl. Aktivierungsfunktion der Schicht
  const cap = (x, txt, sub, color) => {
    const t = svgEl('text', {
      x, y: marginY * 0.42, 'text-anchor': 'middle',
      'font-size': cfg.labelFontPx * 1.0, fill: color, 'font-weight': 'bold',
    });
    t.textContent = txt;
    svg.appendChild(t);
    const s = svgEl('text', {
      x, y: marginY * 0.72, 'text-anchor': 'middle',
      'font-size': cfg.labelFontPx * 0.8, fill: '#888',
    });
    s.textContent = sub;
    svg.appendChild(s);
  };
  cap(inputX, 'Ziel-Wörter', 'one-hot', colors.inputWord);
  cap(hiddenX, `${hidden} Neuronen`, 'linear', colors.hiddenWord);
  cap(outputX, 'Kontext-Wörter', 'Softmax', colors.contextWord);

  svg.appendChild(hoverLayer);
  container.appendChild(svg);
}

/* ===========================================================================
 *  3. Vektor-Datenbank — zwei Modi
 *     'numbers' : Wort | [Zahlen]
 *     'barcode' : Wort | farbcodierte Zellen (PuOr-Diverging)
 * ======================================================================== */
function renderVectorDB(container, net, mode) {
  container.innerHTML = '';
  mode = mode || 'numbers';
  const dec = CONFIG.layout.decimals;
  const table = htmlEl('table', { class: 'vecdb-table' });

  const head = htmlEl('tr');
  head.appendChild(htmlEl('th', { text: 'Ziel-Wort' }));
  head.appendChild(htmlEl('th', { text: mode === 'barcode' ? 'Wortvektor (Barcode, PuOr)' : 'Wortvektor' }));
  table.appendChild(head);

  if (mode === 'barcode') {
    // gemeinsame Normierung über alle Gewichte für vergleichbare Farben
    let maxAbs = 1e-9;
    net.W_in.forEach(v => v.forEach(x => { maxAbs = Math.max(maxAbs, Math.abs(x)); }));

    net.vocab.forEach((word, i) => {
      const tr = htmlEl('tr');
      tr.appendChild(htmlEl('td', { class: 'word', text: word }));
      const cell = htmlEl('td', { class: 'barcode' });
      const bar = htmlEl('div', { class: 'barcode-row' });
      net.W_in[i].forEach((x, j) => {
        const seg = htmlEl('span', { class: 'barcode-seg' });
        seg.style.background = puOrColor((x / maxAbs + 1) / 2);
        seg.title = `Neuron ${j + 1}: ${x.toFixed(dec)}`;
        bar.appendChild(seg);
      });
      cell.appendChild(bar);
      tr.appendChild(cell);
      table.appendChild(tr);
    });
    container.appendChild(table);

    // kleine Farblegende (−max … 0 … +max)
    const legend = htmlEl('div', { class: 'barcode-legend' });
    const grad = htmlEl('div', { class: 'legend-bar' });
    for (let k = 0; k <= 20; k++) {
      const s = htmlEl('span'); s.style.background = puOrColor(k / 20); grad.appendChild(s);
    }
    legend.appendChild(htmlEl('span', { class: 'legend-end', text: `−${maxAbs.toFixed(dec)}` }));
    legend.appendChild(grad);
    legend.appendChild(htmlEl('span', { class: 'legend-end', text: `+${maxAbs.toFixed(dec)}` }));
    container.appendChild(legend);
  } else {
    net.vocab.forEach((word, i) => {
      const tr = htmlEl('tr');
      tr.appendChild(htmlEl('td', { class: 'word', text: word }));
      const vec = '[' + net.W_in[i].map(v => v.toFixed(dec)).join(', ') + ']';
      tr.appendChild(htmlEl('td', { class: 'vec', text: vec }));
      table.appendChild(tr);
    });
    container.appendChild(table);
  }
}

/* ===========================================================================
 *  4. PCA-Streudiagramm der Wortvektoren
 * ======================================================================== */
function renderPCA(container, net) {
  const cfg = CONFIG.layout.pca;
  const colors = CONFIG.layout.colors;
  const W = cfg.width, H = cfg.height;

  container.innerHTML = '';
  const svg = svgEl('svg', {
    viewBox: `0 0 ${W} ${H}`,
    preserveAspectRatio: 'xMidYMid meet',
    class: 'pca-svg',
  });

  const model = fitPCA(net.W_in);
  const points = net.vocab.map((word, i) => {
    const [px, py] = model.project(net.W_in[i]);
    return { word, px, py };
  });

  const cx = W / 2, cy = H / 2;
  [[0, cy, W, cy], [cx, 0, cx, H]].forEach(([x1, y1, x2, y2]) => {
    svg.appendChild(svgEl('line', {
      x1, y1, x2, y2, stroke: colors.gridLine,
      'stroke-width': 1.5, 'stroke-dasharray': '8,4',
    }));
  });

  let maxAbs = 1e-6;
  points.forEach(p => { maxAbs = Math.max(maxAbs, Math.abs(p.px), Math.abs(p.py)); });
  const scale = (Math.min(W, H) * 0.42) / maxAbs;

  points.forEach(p => {
    const x = cx + p.px * scale;
    const y = cy - p.py * scale;
    svg.appendChild(svgEl('circle', {
      cx: x, cy: y, r: cfg.pointRadius,
      fill: colors.inputWord, stroke: '#fff', 'stroke-width': 1.5,
    }));
    const t = svgEl('text', {
      x: x + cfg.pointRadius + 3, y: y - 3,
      'font-size': cfg.labelFontPx, fill: '#222',
    });
    t.textContent = p.word;
    svg.appendChild(t);
  });

  container.appendChild(svg);
}

/* ===========================================================================
 *  5. Echtzeit-Loss-Kurve (Verlustfunktion: Kreuzentropie / Cross-Entropy)
 *     history: Array mittlerer Verluste je Epoche
 * ======================================================================== */
function renderLossChart(container, history) {
  const cfg = CONFIG.layout.loss;
  const colors = CONFIG.layout.colors;
  const W = cfg.width, H = cfg.height;

  container.innerHTML = '';
  const svg = svgEl('svg', {
    viewBox: `0 0 ${W} ${H}`, preserveAspectRatio: 'xMidYMid meet', class: 'loss-svg',
  });

  const padL = 64, padR = 20, padT = 16, padB = 42;
  const x0 = padL, x1 = W - padR, y0 = H - padB, y1 = padT;

  // Achsen
  svg.appendChild(svgEl('line', { x1: x0, y1: y0, x2: x1, y2: y0, stroke: '#888', 'stroke-width': 2 }));
  svg.appendChild(svgEl('line', { x1: x0, y1: y0, x2: x0, y2: y1, stroke: '#888', 'stroke-width': 2 }));

  const axTxt = (x, y, txt, anchor, size) => {
    const t = svgEl('text', { x, y, 'text-anchor': anchor, 'font-size': size || 22, fill: '#555' });
    t.textContent = txt; svg.appendChild(t);
  };
  axTxt((x0 + x1) / 2, H - 8, 'Epoche', 'middle');
  const yl = svgEl('text', {
    x: 18, y: (y0 + y1) / 2, 'text-anchor': 'middle', 'font-size': 22, fill: '#555',
    transform: `rotate(-90 18 ${(y0 + y1) / 2})`,
  });
  yl.textContent = 'Verlust'; svg.appendChild(yl);

  if (history.length === 0) {
    axTxt((x0 + x1) / 2, (y0 + y1) / 2, 'Noch keine Epoche trainiert', 'middle', 24);
    container.appendChild(svg);
    return;
  }

  const yMax = Math.max(...history, 1e-6);
  const n = history.length;
  const sx = i => (n === 1 ? (x0 + x1) / 2 : x0 + (x1 - x0) * i / (n - 1));
  const sy = v => y0 - (y0 - y1) * (v / yMax);

  // y-Skala (0 und Maximum)
  axTxt(x0 - 8, y0 + 6, '0', 'end', 18);
  axTxt(x0 - 8, y1 + 6, yMax.toFixed(2), 'end', 18);

  // Linie
  const pts = history.map((v, i) => `${sx(i)},${sy(v)}`).join(' ');
  svg.appendChild(svgEl('polyline', {
    points: pts, fill: 'none', stroke: colors.loss, 'stroke-width': 3,
  }));
  // aktueller Wert
  const last = history[n - 1];
  svg.appendChild(svgEl('circle', { cx: sx(n - 1), cy: sy(last), r: 5, fill: colors.loss }));
  axTxt(x1, y1 + 4, `aktuell: ${last.toFixed(3)}`, 'end', 20);

  container.appendChild(svg);
}
