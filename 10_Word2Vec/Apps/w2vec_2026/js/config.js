/*
 * ============================================================================
 *  w2vec_2026 — zentrale Konfiguration
 * ----------------------------------------------------------------------------
 *  ALLE veränderbaren Parameter (Limits, Layout, Farben) stehen hier an EINER
 *  Stelle. Wer das Verhalten oder das Aussehen der App anpassen möchte, ändert
 *  ausschließlich diese Datei — der restliche Code liest die Werte dynamisch
 *  aus CONFIG aus. So bleiben spätere didaktische Anpassungen mühelos.
 * ============================================================================
 */
const CONFIG = {

  /* --- Grenzen für den hochgeladenen Beispieltext ------------------------ */
  text: {
    minWords: 10,   // minimale Wortanzahl im Beispieltext
    maxWords: 25,   // maximale Wortanzahl im Beispieltext
  },

  /* --- Fenstergröße (window size) für das Skip-Gram-Verfahren ------------ */
  window: {
    min: 1,         // kleinste erlaubte Fenstergröße
    max: 3,         // größte erlaubte Fenstergröße
    default: 2,     // Voreinstellung
  },

  /* --- Anzahl der Neuronen in der versteckten Schicht -------------------- */
  neurons: {
    min: 3,         // Untergrenze
    max: 10,        // Obergrenze
    default: 5,     // Voreinstellung
  },

  /* --- Trainingsparameter ------------------------------------------------ */
  training: {
    // Lernrate ist über einen Slider einstellbar. Der Bereich ist bewusst auf
    // einen stabilen Korridor begrenzt: zu große Werte (≳ 0.6) lassen den
    // Softmax divergieren (NaN), zu kleine lernen kaum sichtbar.
    learningRate: { min: 0.01, max: 0.5, step: 0.01, default: 0.2 },
    randomSeed: 1,          // Seed für reproduzierbare Initialgewichte
    animationDelayMs: 25,   // Pause zwischen animierten Trainingsschritten
  },

  /* --- Layout & Darstellung --------------------------------------------- */
  layout: {
    decimals: 2,            // Nachkommastellen in der Vektor-Datenbank-Tabelle

    // Datensatz-Tabelle: feste Spaltenbreiten -> daraus wird die maximale
    // Tabellenbreite für maxWords berechnet (siehe app.js / computeOnehotMaxWidth).
    onehot: {
      vocabColPx: 24,       // Breite je Vokabel-Spalte (= CSS .vocab-col)
      wordColPx: 92,        // Breite der Ziel-Wort-Spalte
      paddingPx: 36,        // Rahmen/Polster-Reserve
    },

    // Neuronales Netz (logische SVG-Koordinaten, skaliert responsiv)
    nn: {
      width: 1000,
      baseHeight: 620,      // Mindesthöhe; wächst dynamisch mit der Wortzahl
      rowSpacing: 30,       // logische Höhe pro Ein-/Ausgabe-Neuron
      inputXFrac: 0.16,     // x-Position der Ziel-Wörter (Eingabe), Anteil der Breite
      marginYFrac: 0.10,    // vertikaler Rand
      neuronRadiusFrac: 0.018, // maximaler Neuronen-Radius (Anteil der Breite)
      neuronSpacingFrac: 0.42, // Radius ≤ dieser Anteil des Neuronen-Abstands (kein Überlappen)
      labelFontPx: 20,
      weightFontPx: 15,     // Schriftgröße der Gewichts-Overlays (Hover)
    },

    // PCA-Streudiagramm (deutlich kleiner dargestellt)
    pca: {
      width: 600,
      height: 600,
      pointRadius: 9,
      labelFontPx: 26,
    },

    // Echtzeit-Loss-Kurve
    loss: {
      width: 600,
      height: 300,
    },

    // Farbpalette (an einer Stelle änderbar)
    colors: {
      weightLow:   '#3b6ea5',   // negatives Gewicht / niedrige Aktivierung
      weightMid:   '#f4f4f4',   // neutral
      weightHigh:  '#d6463b',   // positives Gewicht / hohe Aktivierung
      inputWord:   '#1f77b4',   // Ziel-Wörter (Eingabe)
      contextWord: '#ff7f0e',   // Kontext-Wörter (Ausgabe)
      hiddenWord:  '#2ca02c',   // versteckte Neuronen
      highlight:   '#d62728',   // aktive Markierung während eines Schritts
      gridLine:    '#bbbbbb',
      loss:        '#c0392b',   // Linie der Loss-Kurve
      // Diverging-Palette PuOr (ColorBrewer, 7-stufig) für die Barcode-Ansicht
      puOr: ['#b35806', '#f1a340', '#fee0b6', '#f7f7f7', '#d8daeb', '#998ec3', '#542788'],
    },
  },
};

/*
 * Eingebauter Beispieltext im NLTK-Format (Liste von Tokens).
 * Bewusst 25 Wörter (nahe der Obergrenze von 30), damit sich überprüfen lässt,
 * ob das Layout auch bei hoher Auslastung funktioniert. Einige Wörter (z. B.
 * „wolf", „wald") wiederholen sich, damit beim Training erkennbare Strukturen
 * im Vektorraum entstehen.
 * Wird beim Start geladen und steht zugleich als Download bereit
 * (data/sample_text.txt) — so funktioniert die App auch offline (file://).
 */
const SAMPLE_TEXT =
  "['wolf', 'lief', 'durch', 'dunklen', 'wald', 'suchte', 'hungrig', 'kleine', " +
  "'geißlein', 'versteckten', 'angst', 'hinter', 'großen', 'baum', 'mutter', " +
  "'rief', 'laut', 'kinder', 'bleibt', 'still', 'wolf', 'kam', 'näher', 'fand', 'wald']";
