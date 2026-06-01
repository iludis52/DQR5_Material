# w2vec_2026 — Word2Vec-Lernhilfe (Skip-Gram)

Eine **bibliotheksfreie** (Vanilla JS, kein jQuery/D3/Bootstrap) didaktische
**Lernhilfe für Studierende**, die den kompletten Skip-Gram-Weg interaktiv
abbildet — von der Textvorverarbeitung bis zur PCA-Projektion der Wortvektoren.

> Bewusst **nur Skip-Gram**. CBOW bleibt einer eigenen, didaktisch
> abgegrenzten App vorbehalten.

## Starten

Keine Installation, kein Server nötig. Einfach `index.html` im Browser öffnen
(funktioniert auch per `file://`, da der Beispieltext eingebettet ist).

## Layout

Die App füllt **exakt das Browserfenster** (16:9) — die beiden Layout-Zeilen
haben eine feste, bildschirmfüllende Höhe; gescrollt wird **nur innerhalb der
einzelnen Tabellen/Boxen**, nie die ganze Seite. Tabellen, neuronales Netz und
Projektion nutzen jeweils die volle verfügbare Höhe ihrer Spalte aus.

- **Kopfzeile:** Titel links, **Text hochladen** und **Beispiel herunterladen**
  (nebeneinander) sowie der Wortzähler rechts.
- **Zeile 1:** Beispieltext (links) · aufbereiteter Datensatz (Mitte, Breite
  **2:1** gegenüber dem Beispieltext) · Steuerung (rechts, **feste Breite**).
- **Zeile 2:** neuronales Netz (groß) · Vektor-Datenbank · Projektion (klein).

## Funktionsumfang

1. **Beispieltext hochladen / herunterladen**
   Erwartet das übliche NLTK-Format einer Token-Liste, z. B.
   `['wolf', 'lief', 'durch', …]`. Zulässige Wortanzahl: **10–25**.
   Der mitgelieferte Beispieltext hat **25 Wörter** (an der Obergrenze, um das
   Layout bei voller Auslastung zu prüfen) und steht als Download bereit
   (`data/sample_text.txt`). Die Datensatz-Tabelle erhält daraus eine fest
   berechnete **Maximalbreite** (maxWords·Spaltenbreite + Wortspalte; Standard
   25·24+92+36 = **728 px**), sodass kein horizontaler Platz verschwendet wird.

2. **Skip-Gram-Datensatz** mit wählbarer **Fenstergröße (1–3)**.
   Bei Fenstergröße > 1 werden die dünn besetzten Kontext-One-Hot-Vektoren
   **aufsummiert** (mehrfach besetzter Kontextvektor).

3. **Layout-Zeile 1 — drei Spalten:** links der **Beispieltext** als
   Token-Liste (**Mouse-over über ein Token** zeigt dessen Sparse-Vektor); in der
   Mitte die scrollbare, nicht veränderbare **Datensatz-Tabelle** (je Zeile ein
   Trainingsbeispiel — Ziel-Wort und sein summierter **Kontext-Vektor als
   Zeilenvektor**; senkrechte, schmale Spaltenköpfe; ausführliche Erklärung als
   **Overlay beim Mouse-over**); rechts die **Steuerung** mit fester Breite
   (Slider untereinander, alle drei Trainings-Buttons in einer Zeile — der
   didaktische Ablauf: Text → Parameter → Training).

4. **Neuronales Netz** (zentrale, größte Einheit) — wählbare
   **Neuronenzahl (3–10)**: links die Ziel-Wörter, in der Mitte die Neuronen,
   rechts die Kontext-Wörter. Die Überschrift nennt die Aktivierungen je Schicht
   (Eingabe: one-hot · versteckt: linear · Ausgabe: Softmax). Der **Neuronen-
   Radius passt sich der Wortzahl an** (verkleinert sich bei 20–25 Wörtern, damit
   nichts überlappt; bleibt bei wenigen Wörtern maximal). Beim Trainingsschritt
   werden die aktuellen Neuronen durch eine **rote Umrandung** markiert (keine
   Pfeile mehr). **Mouse-over über ein Neuron** blendet die Gewichte seiner
   Verbindungen ein (Ein-/Ausgänge).

5. **Vektor-Datenbank** — umschaltbar zwischen **Zahlen-** und
   **Barcode-Darstellung** (Diverging-Palette **PuOr** mit Farblegende). Pro
   Ziel-Wort ein **Zeilenvektor** der Länge = Anzahl Neuronen; aktualisiert
   sich live und ist **so hoch wie das neuronale Netz**.

6. **Projektion** — **entweder** die **PCA-Projektion** **oder** (per Toggle) die
   kleine **Echtzeit-Loss-Kurve** (Verlustfunktion: **Kreuzentropie /
   Cross-Entropy**); nie beide gleichzeitig. Netz, Vektor-Datenbank und
   Projektion liegen in **einer Zeile** nebeneinander.

**Bedienung:** **Lernrate** über einen feinstufigen Slider (Bereich 0.01–0.50,
wirkt sofort). **▶ Training** startet ein fortlaufendes Training, **⏹ Stop** hält
es an, **↺ Reset** initialisiert das Netz neu. Die jeweils sichtbare Projektion
(PCA oder Loss) aktualisiert sich **live nach jeder Epoche**.

## Parameter anpassen

**Alle** veränderbaren Werte (Grenzen, Lernrate, Layout, Farben) stehen zentral
in [`js/config.js`](js/config.js). Wer Limits, Aussehen oder Verhalten ändern
möchte, passt ausschließlich diese Datei an — der übrige Code liest die Werte
dynamisch aus.

| Parameter            | Ort in `config.js`                  | Standard       |
|----------------------|-------------------------------------|----------------|
| Wortanzahl (min/max) | `text.minWords/maxWords`            | 10 / 25        |
| Tabellen-Spaltenbreiten | `layout.onehot.{vocabColPx,wordColPx,paddingPx}` | 24 / 92 / 36 |
| Fenstergröße         | `window.min/max/default`            | 1 / 3 / 2      |
| Neuronen             | `neurons.min/max/default`           | 3 / 10 / 5     |
| Lernrate             | `training.learningRate.{min,max,step,default}` | 0.01 / 0.50 / 0.01 / 0.20 |
| Farben / PuOr        | `layout.colors`                     | —              |

## Aufbau

| Datei              | Inhalt                                                        |
|--------------------|--------------------------------------------------------------|
| `index.html`       | Seitengerüst                                                 |
| `css/style.css`    | Layout (CSS-Grid/Flexbox, zentrale Variablen in `:root`)     |
| `js/config.js`     | **Zentrale Konfiguration** + eingebauter Beispieltext        |
| `js/word2vec.js`   | Parsing, Vokabular, Datensatz, Netz, Vorwärts-/Rückwärtsrechnung |
| `js/pca.js`        | Bibliotheksfreie PCA (Golub-Reinsch-SVD)                     |
| `js/viz.js`        | SVG-/Tabellen-Darstellung                                    |
| `js/app.js`        | Steuerung, dynamische Bedienelemente, Trainingsschleife      |
| `data/sample_text.txt` | Beispieltext zum Download                               |

## Hinweis zum Trainingsverlust

Bei kleinen Texten mit überwiegend eindeutigen Wörtern sinkt der Kreuzentropie-
Verlust zunächst deutlich und erreicht dann ein Plateau nahe der
informationstheoretischen Untergrenze (≈ *k* · ln *k* für *k* Kontextwörter).
Das ist erwartetes Verhalten und didaktisch gut sichtbar.
