/*
 * ============================================================================
 *  w2vec_2026 — Anwendungssteuerung
 * ----------------------------------------------------------------------------
 *  Verbindet Bedienelemente, Kern-Logik (word2vec.js) und Darstellung (viz.js).
 *  Steuerelemente werden DYNAMISCH aus CONFIG aufgebaut, damit Layout- und
 *  Parameteränderungen ohne Eingriff in den HTML-Code möglich sind.
 * ============================================================================
 */

const state = {
  tokens: [],
  vocab: [],
  dataset: [],
  net: null,
  windowSize: CONFIG.window.default,
  neurons: CONFIG.neurons.default,
  learningRate: CONFIG.training.learningRate.default,
  cursor: 0,           // nächster zu trainierender Datensatz-Index
  steps: 0,            // Anzahl absolvierter Trainingsschritte
  epoch: 0,            // Anzahl abgeschlossener Epochen
  running: false,      // läuft das fortlaufende Training gerade?
  timer: null,         // Handle des Trainings-Timers
  vecdbMode: 'numbers',// Vektor-Datenbank: 'numbers' | 'barcode'
  showLoss: false,     // Loss-Kurve eingeblendet?
  lossHistory: [],     // mittlerer Verlust je Epoche
  epochLossSum: 0,     // Akkumulator für die laufende Epoche
};

/* DOM-Verknüpfungen */
const dom = {};

document.addEventListener('DOMContentLoaded', () => {
  cacheDom();
  buildHeaderActions();
  buildControls();
  loadTokens(parseTokenList(SAMPLE_TEXT), 'Eingebauter Beispieltext geladen.');
});

function cacheDom() {
  // nur die statischen Container; dynamische Elemente werden in
  // buildHeaderActions()/buildControls() erzeugt und dort referenziert.
  ['controls', 'header-actions', 'status', 'onehot', 'text', 'nn', 'vecdb', 'pca',
   'loss', 'loss-chart', 'toggle-loss', 'toggle-vecdb']
    .forEach(id => { dom[id] = document.getElementById(id); });

  // Umschalter für Vektor-Datenbank (Zahlen/Barcode)
  dom['toggle-vecdb'].addEventListener('click', () => {
    state.vecdbMode = state.vecdbMode === 'numbers' ? 'barcode' : 'numbers';
    dom['toggle-vecdb'].textContent =
      state.vecdbMode === 'numbers' ? '▦ Barcode' : '½ Zahlen';
    if (state.net) renderVectorDB(dom['vecdb'], state.net, state.vecdbMode);
  });
  // Umschalter PCA <-> Loss-Kurve (entweder/oder, nie beide gleichzeitig)
  dom['toggle-loss'].addEventListener('click', () => {
    state.showLoss = !state.showLoss;
    updateRightView();
  });

  // berechnete Maximalbreite der Datensatz-Tabelle fest hinterlegen
  document.documentElement.style.setProperty('--onehot-max-width', computeOnehotMaxWidth() + 'px');
}

/*
 * Berechnet die maximale Breite der Datensatz-Tabelle aus den festen
 * Spaltenbreiten und der maximalen Wortzahl:
 *   maxWords · vocabColPx + wordColPx + paddingPx
 * Beispiel (Standard): 25 · 24 + 92 + 36 = 728 px.
 */
function computeOnehotMaxWidth() {
  const o = CONFIG.layout.onehot;
  return CONFIG.text.maxWords * o.vocabColPx + o.wordColPx + o.paddingPx;
}

/* Zeigt entweder die PCA-Projektion ODER die Loss-Kurve (entweder/oder). */
function updateRightView() {
  dom['pca'].hidden = state.showLoss;
  dom['loss'].hidden = !state.showLoss;
  dom['toggle-loss'].textContent = state.showLoss ? '→ PCA-Projektion' : '→ Loss-Kurve';
  if (!state.net) return;
  if (state.showLoss) renderLossChart(dom['loss-chart'], state.lossHistory);
  else renderPCA(dom['pca'], state.net);
}

/* ---------------------------------------------------------------------------
 *  Kopfzeilen-Aktionen: Text-Upload + Download (rechts oben, nebeneinander)
 * ------------------------------------------------------------------------ */
function buildHeaderActions() {
  const h = dom['header-actions'];
  h.innerHTML = '';

  // Wortzähler (kompakt, links neben den Buttons)
  dom['word-count'] = htmlEl('span', { id: 'word-count', class: 'word-count' });
  h.appendChild(dom['word-count']);

  const uploadBtn = htmlEl('button', { class: 'btn', text: '⬆ Text hochladen' });
  const fileInput = htmlEl('input', { type: 'file', accept: '.txt', style: 'display:none' });
  fileInput.addEventListener('change', onFileChosen);
  uploadBtn.addEventListener('click', () => fileInput.click());
  h.appendChild(uploadBtn);
  h.appendChild(fileInput);

  h.appendChild(htmlEl('a', {
    class: 'btn btn-link', href: 'data/sample_text.txt', download: 'sample_text.txt',
    text: '⬇ Beispiel herunterladen',
  }));
}

/* ---------------------------------------------------------------------------
 *  Aufbau der Steuerelemente (dynamisch aus CONFIG)
 * ------------------------------------------------------------------------ */
function buildControls() {
  const c = dom['controls'];
  c.innerHTML = '';
  c.appendChild(htmlEl('h3', { text: 'Steuerung' }));

  // --- Fenstergröße (window size) ---
  c.appendChild(buildSlider(
    'Window', CONFIG.window.min, CONFIG.window.max, state.windowSize,
    val => { state.windowSize = val; rebuildDataset(); }));

  // --- Anzahl Neuronen ---
  c.appendChild(buildSlider(
    'Neurons', CONFIG.neurons.min, CONFIG.neurons.max, state.neurons,
    val => { state.neurons = val; rebuildNetwork(); }));

  // --- Lernrate (Slider, feinstufig) ---
  const lr = CONFIG.training.learningRate;
  c.appendChild(buildSlider(
    'Lernrate', lr.min, lr.max, state.learningRate,
    val => { state.learningRate = val; },   // wirkt sofort beim nächsten Schritt
    { step: lr.step, decimals: 2 }));

  // --- Aktionen: alle drei Trainings-Buttons nebeneinander in EINER Zeile ---
  c.appendChild(htmlEl('label', { class: 'ctrl-label', text: 'Training:' }));
  const actions = htmlEl('div', { class: 'ctrl-actions' });

  const resetBtn = htmlEl('button', { class: 'btn btn-warn', text: '↺ Reset' });
  resetBtn.addEventListener('click', rebuildNetwork);
  actions.appendChild(resetBtn);

  dom['btn-train'] = htmlEl('button', { class: 'btn btn-train', text: '▶ Training' });
  dom['btn-train'].addEventListener('click', startTraining);
  actions.appendChild(dom['btn-train']);

  dom['btn-stop'] = htmlEl('button', { class: 'btn btn-warn', text: '⏹ Stop' });
  dom['btn-stop'].disabled = true;
  dom['btn-stop'].addEventListener('click', stopTraining);
  actions.appendChild(dom['btn-stop']);

  c.appendChild(actions);
}

/*
 * Baut einen beschrifteten Schieberegler (mit Min/Max aus CONFIG) und
 * einer Live-Wertanzeige.
 */
function buildSlider(label, min, max, value, onChange, opts = {}) {
  const step = opts.step || 1;
  const decimals = opts.decimals || 0;
  const fmt = v => Number(v).toFixed(decimals);

  const group = htmlEl('div', { class: 'ctrl-group' });
  group.appendChild(htmlEl('label', { text: `${label}:` }));

  const slider = htmlEl('input', {
    type: 'range', min: String(min), max: String(max),
    value: String(value), step: String(step),
  });
  const out = htmlEl('span', { class: 'slider-value', text: fmt(value) });

  slider.addEventListener('input', () => {
    const v = decimals > 0 ? parseFloat(slider.value) : parseInt(slider.value, 10);
    out.textContent = fmt(v);
    onChange(v);
  });

  group.appendChild(slider);
  group.appendChild(out);
  group.appendChild(htmlEl('span', { class: 'slider-range', text: `(${fmt(min)}–${fmt(max)})` }));
  return group;
}

/* ---------------------------------------------------------------------------
 *  Datei-Upload
 * ------------------------------------------------------------------------ */
function onFileChosen(evt) {
  const file = evt.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    const tokens = parseTokenList(e.target.result);
    const check = validateTokenCount(tokens);
    if (!check.ok) {
      setStatus(check.message, true);
      return;
    }
    loadTokens(tokens, `Datei „${file.name}“ geladen.`);
  };
  reader.readAsText(file);
  evt.target.value = '';  // erlaubt erneutes Hochladen derselben Datei
}

/* ---------------------------------------------------------------------------
 *  Lade- und Aufbau-Logik
 * ------------------------------------------------------------------------ */
function loadTokens(tokens, msg) {
  const check = validateTokenCount(tokens);
  if (!check.ok) { setStatus(check.message, true); return; }

  state.tokens = tokens;
  state.vocab = buildVocab(tokens);
  dom['word-count'].textContent =
    `${tokens.length} Wörter · ${state.vocab.length} eindeutige`;
  renderText(dom['text'], tokens, state.vocab);
  rebuildDataset();
  setStatus(msg, false);
}

/* Datensatz neu erzeugen und Netz neu initialisieren. */
function rebuildDataset() {
  if (state.tokens.length === 0) return;
  stopTraining();
  state.dataset = buildSkipgramDataset(state.tokens, state.vocab, state.windowSize);
  renderOneHotTable(dom['onehot'], state.vocab, state.dataset);
  rebuildNetwork();
}

/* Netz neu initialisieren und alle Ansichten zurücksetzen. */
function rebuildNetwork() {
  if (state.vocab.length === 0) return;
  stopTraining();
  state.net = createNetwork(state.vocab, state.neurons, CONFIG.training.randomSeed);
  state.cursor = 0;
  state.steps = 0;
  state.epoch = 0;
  state.lossHistory = [];
  state.epochLossSum = 0;
  renderNeuralNet(dom['nn'], state.net, null);
  renderVectorDB(dom['vecdb'], state.net, state.vecdbMode);
  updateRightView();
  setStatus(`Netz initialisiert: ${state.vocab.length} Wörter · ${state.neurons} Neuronen · ` +
            `Fenstergröße ${state.windowSize} · Lernrate ${state.learningRate.toFixed(2)}.`, false);
}

/* ---------------------------------------------------------------------------
 *  Fortlaufendes Training
 *  Läuft Schritt für Schritt (animiert) weiter, bis "Stop" gedrückt wird.
 *  Nach jeder abgeschlossenen Epoche wird die PCA in Echtzeit aktualisiert.
 * ------------------------------------------------------------------------ */
function startTraining() {
  if (state.running || !state.net || state.dataset.length === 0) return;
  state.running = true;
  dom['btn-train'].disabled = true;
  dom['btn-stop'].disabled = false;
  trainStepLoop();
}

function stopTraining() {
  state.running = false;
  if (state.timer) { clearTimeout(state.timer); state.timer = null; }
  if (dom['btn-train']) dom['btn-train'].disabled = false;
  if (dom['btn-stop']) dom['btn-stop'].disabled = true;
  // neutrale Netzdarstellung nach dem Anhalten
  if (state.net) renderNeuralNet(dom['nn'], state.net, null);
}

function trainStepLoop() {
  if (!state.running) return;
  const row = state.dataset[state.cursor];

  // aktiven Schritt im Netz hervorheben
  renderNeuralNet(dom['nn'], state.net, row);

  // Gewichte aktualisieren (Lernrate live aus dem Slider)
  const { loss } = trainStep(state.net, row, state.learningRate);
  state.steps++;
  state.epochLossSum += loss;
  state.cursor = (state.cursor + 1) % state.dataset.length;

  // Vektor-Datenbank fortlaufend aktualisieren
  renderVectorDB(dom['vecdb'], state.net, state.vecdbMode);

  // Epochengrenze erreicht? -> sichtbare Projektion (PCA ODER Loss) live aktualisieren
  if (state.cursor === 0) {
    state.epoch++;
    state.lossHistory.push(state.epochLossSum / state.dataset.length);
    state.epochLossSum = 0;
    updateRightView();
  }

  setStatus(`Epoche ${state.epoch} · Schritt ${state.steps} · ` +
            `Ziel „${row.targetWord}“ · Verlust ${loss.toFixed(3)}`, false);

  state.timer = setTimeout(trainStepLoop, CONFIG.training.animationDelayMs);
}

/* ---------------------------------------------------------------------------
 *  Statusanzeige
 * ------------------------------------------------------------------------ */
function setStatus(msg, isError) {
  dom['status'].textContent = msg;
  dom['status'].className = isError ? 'status error' : 'status';
}
