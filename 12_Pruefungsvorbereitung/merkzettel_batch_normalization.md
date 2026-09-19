# Merkzettel: Batch Normalization

Kurzreferenz zur Prüfungsvorbereitung

---

## 1. Der Kern in einem Satz

**Batch Normalization normalisiert die Ausgaben einer versteckten Schicht — je Neuron, über alle Samples eines Mini-Batches — und gibt dem Netz anschließend zwei lernbare Parameter, mit denen es diese Normalisierung wieder anpassen kann.**

---

## 2. Das Problem, gegen das es hilft

In einem tiefen Netz ist die Eingabe jeder Schicht die Ausgabe der vorherigen. Beim Training ändern sich alle Gewichte gleichzeitig — also verschiebt sich ständig auch die **Verteilung** der Werte, die weiter hinten ankommen. Schicht 5 muss ihr Ziel treffen, während sich das Ziel bewegt.

Die Folgen sind konkret:

- Aktivierungen laufen in die **Sättigung** (bei Tanh und Sigmoid). Dort ist die Ableitung nahezu null.
- Der Gradient kommt in den vorderen Schichten kaum noch an.
- Man braucht kleine Lernraten und eine sehr sorgfältige Initialisierung.

> **Merksatz:** Je tiefer das Netz, desto größer das Problem. Bei einer einzigen versteckten Schicht bringt Batch Normalization praktisch nichts — dort genügt eine saubere Skalierung der Eingaben.

---

## 3. Die Rechenvorschrift

Vier Schritte, je Neuron, über die *m* Samples des aktuellen Mini-Batches:

```
1. Mittelwert     μ  = (1/m) · Σ zᵢ
2. Varianz        σ² = (1/m) · Σ (zᵢ − μ)²
3. Normalisieren  ẑᵢ = (zᵢ − μ) / √(σ² + ε)
4. Anpassen       yᵢ = γ · ẑᵢ + β
```

- **ε** (epsilon) ist eine winzige Konstante, die Division durch null verhindert. Sie steht **unter** der Wurzel.
- Schritt 1 bis 3 ist die **Z-Transformation** aus der Statistik. Ergebnis: Mittelwert 0, Streuung 1.
- Schritt 4 ist der entscheidende Zusatz (siehe Abschnitt 5).

### Die Richtung ist das Ungewohnte

Normalisiert wird **nicht** innerhalb eines Samples, sondern **entlang der Batch-Dimension**. Stellt man die Ausgaben als Tabelle dar — eine Zeile pro Sample, eine Spalte pro Neuron —, dann rechnet Batch Normalization **spaltenweise**.

| | Neuron 1 | Neuron 2 | Neuron 3 |
|---|---|---|---|
| Sample 1 | 2 | −1 | 5 |
| Sample 2 | 4 | 1 | 3 |
| Sample 3 | 0 | 3 | 7 |
| Sample 4 | 6 | 1 | 5 |
| **μ** | **3** | **1** | **5** |
| **σ²** | **5** | **2** | **2** |

Bei 3 Neuronen entstehen also **3 Mittelwerte und 3 Varianzen** — nicht einer für die ganze Schicht.

---

## 4. Wo die Schicht eingebaut wird

Zwischen der **Summenberechnung** (z = Wx + b) und der **Aktivierungsfunktion**:

```mermaid
flowchart LR
    A[Eingabe x] --> B["Linear<br/>z = Wx + b"]
    B --> C["BatchNorm<br/>normalisieren, dann γ·ẑ + β"]
    C --> D["Aktivierung<br/>ReLU / Tanh"]
    D --> E[nächste Schicht]
```

Zur Illustration derselbe Aufbau in PyTorch-Notation — nur als Beleg für die **Reihenfolge**, nicht als Programmierstoff:

```python
nn.Linear(n_ein, n_aus)      # Summenberechnung
nn.BatchNorm1d(n_aus)        # hier sitzt die Normalisierung
nn.ReLU()                    # Aktivierungsfunktion
```

Zwei Punkte dazu:

- Die **Ausgabeschicht** bekommt kein Batch Normalization. Die Skala der Ausgabewerte soll das Netz frei bestimmen können.
- Die Platzierung *vor* der Aktivierung stammt aus der Originalarbeit. Eine Variante *nach* der Aktivierung existiert; die klassische Antwort ist „davor".

---

## 5. γ und β — die lernbaren Parameter

Reines Normalisieren würde das Netz einschränken: Eine Sigmoid- oder Tanh-Funktion arbeitet um die Null herum nahezu linear. Ein Netz, dessen Werte starr auf Mittelwert 0 und Streuung 1 festgenagelt sind, verliert Ausdrucksstärke.

Deshalb folgen zwei Parameter **je Neuron**:

| Parameter | Wirkung | Startwert |
|---|---|---|
| **γ** (Gamma) | skaliert — macht die Verteilung breiter oder schmaler | 1 |
| **β** (Beta) | verschiebt — hebt die Verteilung nach oben oder unten | 0 |

Beide werden wie ganz normale Gewichte per Gradientenabstieg gelernt. Das Netz kann die Normalisierung damit bei Bedarf teilweise oder vollständig zurücknehmen — aber es **lernt** die passende Skala und Lage, statt sie zufällig zu erben.

Bei *H* Neuronen kommen also **2·H** lernbare Parameter hinzu.

> **Nebenwirkung:** Der Bias *b* der vorangehenden Summenberechnung wird überflüssig — Batch Normalization zieht ihn im nächsten Schritt ohnehin wieder ab. Seine Rolle übernimmt β.

---

## 6. Training und Inferenz sind verschieden

Das ist die häufigste Fehlerquelle in der Praxis.

| | Training | Inferenz (Vorhersage) |
|---|---|---|
| Woher kommen μ und σ²? | aus dem **aktuellen Batch** | aus **gespeicherten** Werten |
| Ändern sie sich? | in jedem Schritt neu | fest |
| γ und β | werden gelernt | bleiben wie gelernt |

Warum die Unterscheidung nötig ist: Ein einzelnes Bild hat keinen Batch. Und die Vorhersage darf nicht davon abhängen, welche anderen Daten zufällig danebenliegen. Deshalb führt die Schicht während des Trainings **gleitende Mittelwerte** mit (*running mean* und *running variance*) und benutzt diese festen Werte bei der Inferenz.

Diese gespeicherten Statistiken sind **keine lernbaren Parameter** — sie werden nicht optimiert, sondern mitgeschrieben. Sie gehören trotzdem zum Modell und müssen mitgespeichert werden.

> In PyTorch schaltet `net.eval()` auf diesen Modus um. Das ist keine Formalie, sondern zwingend.

---

## 7. Die Abhängigkeit von der Batchgröße

Batch Normalization schätzt μ und σ² aus dem Batch. Also gilt:

| Batchgröße | Folge |
|---|---|
| 1 | **Fehler** — aus einem Wert lässt sich keine Varianz berechnen |
| 2 bis 4 | μ und σ² sind schlechte Schätzer, das Training wird verrauscht |
| ab ca. 16 | brauchbar |

Praktische Konsequenz: Bleibt am Ende einer Epoche ein Rest-Batch der Größe 1 übrig, bricht das Training ab. Man verwirft diesen Rest.

**Abgrenzung — Layer Normalization:** Dort wird über die Merkmale *eines* Samples normalisiert, also zeilenweise statt spaltenweise. Die Batchgröße spielt keine Rolle mehr. Deshalb verwenden Transformer Layer Normalization statt Batch Normalization.

---

## 8. Was es bringt — und was nicht

**Vorteile:**

- Höhere Lernraten möglich, dadurch deutlich schnellere Konvergenz
- Robuster gegenüber der Wahl der Initialisierung
- Leichte Regularisierung: μ und σ² schwanken von Batch zu Batch, das wirkt wie schwaches Rauschen

**Grenzen und Missverständnisse:**

- Es ersetzt **nicht** die Skalierung der Eingabedaten. Der Scaler normalisiert die Eingaben einmalig vor dem Training, Batch Normalization die Zwischenergebnisse in jedem Schritt.
- Es ersetzt **keine** Aktivierungsfunktionen und **keine** Schichten.
- In flachen Netzen bringt es meist gar nichts.
- Bei kleinen Batches wird es unzuverlässig.

> **Die richtige Merkregel lautet nicht** „Batch Normalization macht Modelle besser", **sondern:** Batch Normalization macht Tiefe überhaupt erst trainierbar.

---

## 9. Ergänzungen für die Vollständigkeit

**Faltungsnetze:** Dort läuft die Statistik **pro Kanal**, gemittelt über Batch, Höhe und Breite. Begründung: Ein Filter soll dasselbe Merkmal unabhängig vom Ort erkennen — also soll er überall gleich normalisiert werden.

**Der Gradient:** μ und σ² sind für die Rückwärtsrechnung keine Konstanten. Sie hängen von den Eingaben ab, also von den Gewichten, und der Gradient fließt durch sie hindurch. Behandelte man sie als konstant, könnte der Mittelwert unbegrenzt weglaufen.

**Zur Einordnung:** Ioffe und Szegedy begründeten das Verfahren 2015 mit dem *internal covariate shift*. Diese Deutung gilt heute als nicht belegt; Folgearbeiten führen die Wirkung eher darauf zurück, dass die Verlustlandschaft glatter und besser konditioniert wird. Der Nutzen ist unstrittig — die ursprüngliche Begründung nicht.

---

## 10. Die sieben Sätze zum Auswendiglernen

1. Batch Normalization normalisiert **spaltenweise**: je Neuron über alle Samples des Batches.
2. Es sitzt **zwischen Summenberechnung und Aktivierungsfunktion**.
3. Die Formel lautet **ẑ = (z − μ) / √(σ² + ε)**, danach **y = γ·ẑ + β**.
4. **γ skaliert, β verschiebt** — beide werden gelernt, je einer pro Neuron.
5. Beim Training kommen μ und σ² **aus dem Batch**, bei der Inferenz aus **gespeicherten** Werten.
6. Mit **einem einzigen Sample** funktioniert es nicht — es gibt dann keine Varianz.
7. Der Nutzen wächst mit der **Tiefe** des Netzes, nicht mit der Größe der Schicht.

---

## 11. Begriffe kompakt

| Begriff | Bedeutung |
|---|---|
| Mini-Batch | Gruppe von Samples, die gemeinsam durch das Netz laufen |
| μ, σ² | Mittelwert und Varianz, je Neuron über den Batch berechnet |
| ẑ | der normalisierte Wert (Mittelwert 0, Streuung 1) |
| ε | kleine Konstante unter der Wurzel, verhindert Division durch null |
| γ, β | lernbare Skalierung und Verschiebung, je Neuron ein Paar |
| running mean / var | während des Trainings mitgeschriebene Statistik für die Inferenz |
| Sättigung | flacher Bereich einer Aktivierungsfunktion, Ableitung nahe null |
| Layer Normalization | normalisiert je Sample statt je Batch — batchgrößen-unabhängig |
