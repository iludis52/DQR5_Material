/*
 * ============================================================================
 *  w2vec_2026 — Kern-Logik (Skip-Gram)
 * ----------------------------------------------------------------------------
 *  Reines, bibliotheksfreies JavaScript:
 *   - Einlesen des NLTK-artigen Token-Listen-Formats
 *   - Aufbau des Vokabulars
 *   - Erzeugung des Skip-Gram-Datensatzes (one-hot Ziel, summierter Kontext)
 *   - Initialisierung des neuronalen Netzes
 *   - Vorwärts- und Rückwärtsrechnung (Softmax + Kreuzentropie)
 *
 *  Bewusst NUR Skip-Gram. CBOW bleibt einer eigenen, didaktisch
 *  abgegrenzten App vorbehalten.
 * ============================================================================
 */

/*
 * Wandelt eine Zeichenkette im NLTK-Format
 *   ['wort1', 'wort2', ...]
 * in ein Array von Tokens um. Tolerant gegenüber doppelten/einfachen
 * Anführungszeichen und überflüssigen Leerzeichen.
 */
function parseTokenList(raw) {
  const inner = String(raw).trim()
    .replace(/^\[/, '')
    .replace(/\]$/, '');
  return inner
    .split(',')
    .map(s => s.trim())
    .map(s => s.replace(/^['"]/, '').replace(/['"]$/, ''))
    .filter(s => s.length > 0);
}

/*
 * Prüft die Token-Anzahl gegen die in CONFIG.text definierten Grenzen.
 * Liefert { ok, message }.
 */
function validateTokenCount(tokens) {
  const { minWords, maxWords } = CONFIG.text;
  if (tokens.length < minWords) {
    return { ok: false, message:
      `Zu wenige Wörter: ${tokens.length} (Minimum ${minWords}).` };
  }
  if (tokens.length > maxWords) {
    return { ok: false, message:
      `Zu viele Wörter: ${tokens.length} (Maximum ${maxWords}).` };
  }
  return { ok: true, message: '' };
}

/* Eindeutiges, alphabetisch sortiertes Vokabular. */
function buildVocab(tokens) {
  return Array.from(new Set(tokens)).sort((a, b) => a.localeCompare(b, 'de'));
}

/* Erzeugt einen one-hot-Vektor der Länge size mit einer 1 an Position idx. */
function oneHot(idx, size) {
  const v = new Array(size).fill(0);
  v[idx] = 1;
  return v;
}

/*
 * Erzeugt den Skip-Gram-Datensatz.
 *
 * Für jede Position im Text bildet das zentrale Wort das ZIEL (Eingabe,
 * one-hot). Der KONTEXT (Ausgabe) ergibt sich aus allen Wörtern innerhalb
 * der Fenstergröße. Ist windowSize > 1, werden die einzelnen, dünn besetzten
 * Kontext-one-hot-Vektoren AUFADDIERT (mehrfach besetzter Zielvektor).
 *
 * Rückgabe: Array von Zeilen
 *   { pos, targetWord, targetIdx, targetVec, contextWords, contextVec }
 */
function buildSkipgramDataset(tokens, vocab, windowSize) {
  const index = new Map(vocab.map((w, i) => [w, i]));
  const V = vocab.length;
  const rows = [];

  for (let i = 0; i < tokens.length; i++) {
    const targetIdx = index.get(tokens[i]);
    const contextVec = new Array(V).fill(0);
    const contextWords = [];

    const lo = Math.max(0, i - windowSize);
    const hi = Math.min(tokens.length - 1, i + windowSize);
    for (let j = lo; j <= hi; j++) {
      if (j === i) continue;
      contextVec[index.get(tokens[j])] += 1;  // aufsummieren (multi-hot)
      contextWords.push(tokens[j]);
    }

    rows.push({
      pos: i,
      targetWord: tokens[i],
      targetIdx,
      targetVec: oneHot(targetIdx, V),
      contextWords,
      contextVec,
    });
  }
  return rows;
}

/* ---------------------------------------------------------------------------
 *  Neuronales Netz
 * ------------------------------------------------------------------------ */

/*
 * Deterministischer Pseudozufallsgenerator (wie in der Original-App),
 * damit Initialgewichte bei gleichem Seed reproduzierbar sind.
 */
function makeRandom(seed) {
  let s = seed >>> 0;
  return function () {
    s = (s * 25214903917 + 11) & 0xffff;
    return s / 65536;  // in [0, 1)
  };
}

/*
 * Initialisiert das Netz mit zwei Gewichtsmatrizen:
 *   W_in  (V × H): Ziel-/Wort-Einbettungen   (links → Mitte)
 *   W_out (V × H): Kontext-Einbettungen       (Mitte → rechts)
 */
function createNetwork(vocab, hiddenSize, seed) {
  const V = vocab.length;
  const rand = makeRandom(seed);
  const W_in = [];
  const W_out = [];
  for (let i = 0; i < V; i++) {
    const inRow = [];
    const outRow = [];
    for (let j = 0; j < hiddenSize; j++) {
      inRow.push((rand() - 0.5) / hiddenSize);
      outRow.push((rand() - 0.5) / hiddenSize);
    }
    W_in.push(inRow);
    W_out.push(outRow);
  }
  return { vocab, V, H: hiddenSize, W_in, W_out };
}

/*
 * Vorwärtsrechnung für ein Ziel-Wort (Skip-Gram: genau ein Eingabeneuron
 * ist aktiv). Versteckte Schicht = Eingabevektor des Ziels. Ausgabe = Softmax.
 * Rückgabe: { h (versteckt), u (Netto-Eingaben), y (Softmax-Wahrscheinlichkeiten) }
 */
function feedforward(net, targetIdx) {
  const h = net.W_in[targetIdx].slice();
  const u = new Array(net.V);
  let maxU = -Infinity;
  for (let i = 0; i < net.V; i++) {
    let s = 0;
    for (let j = 0; j < net.H; j++) s += net.W_out[i][j] * h[j];
    u[i] = s;
    if (s > maxU) maxU = s;
  }
  // numerisch stabiler Softmax
  let sum = 0;
  const y = new Array(net.V);
  for (let i = 0; i < net.V; i++) {
    const e = Math.exp(u[i] - maxU);
    y[i] = e;
    sum += e;
  }
  for (let i = 0; i < net.V; i++) y[i] /= sum;
  return { h, u, y };
}

/*
 * Ein Trainingsschritt für eine Datensatzzeile.
 * Zielverteilung t = aufsummierter Kontextvektor (kann Werte > 1 enthalten).
 * Gradient des Softmax mit Kreuzentropie:  EI_i = y_i * (Σ t) − t_i
 * Aktualisiert W_out (alle Zeilen) und die eine aktive W_in-Zeile.
 * Rückgabe: { y, loss } für optionale Anzeige.
 */
function trainStep(net, row, learningRate) {
  const { h, y } = feedforward(net, row.targetIdx);
  const t = row.contextVec;
  const T = t.reduce((a, b) => a + b, 0);  // Anzahl Kontextwörter

  // Fehler an der Ausgabeschicht
  const EI = new Array(net.V);
  for (let i = 0; i < net.V; i++) EI[i] = y[i] * T - t[i];

  // Fehler an der versteckten Schicht (vor dem Update von W_out berechnen)
  const EH = new Array(net.H).fill(0);
  for (let i = 0; i < net.V; i++) {
    for (let j = 0; j < net.H; j++) EH[j] += EI[i] * net.W_out[i][j];
  }

  // W_out aktualisieren
  for (let i = 0; i < net.V; i++) {
    for (let j = 0; j < net.H; j++) net.W_out[i][j] -= learningRate * EI[i] * h[j];
  }
  // aktive W_in-Zeile aktualisieren
  for (let j = 0; j < net.H; j++) net.W_in[row.targetIdx][j] -= learningRate * EH[j];

  // Kreuzentropie-Verlust (nur zur Anzeige)
  let loss = 0;
  for (let i = 0; i < net.V; i++) if (t[i] > 0) loss -= t[i] * Math.log(y[i] + 1e-12);

  return { y, loss };
}
