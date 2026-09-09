# Datenaufteilung und Modellbewertung

**Kurzreferenz zur Prüfungsvorbereitung — KI und Maschinelles Lernen (DQR 5)**

---

## Was steht wo

| | Thema | Stichworte aus der Prüfungsliste |
|---|---|---|
| 1 | Die drei Datenmengen | Aufteilung, Repräsentativität, typische Verhältnisse |
| 2 | Validierungsdaten vs. Testdaten | Validierungsdaten vs. Testdaten |
| 3 | n-fache Cross-Validierung | n-fache Cross-Validierung, Schwankung zwischen den Folds |
| 4 | Aufteilung bei neuronalen Netzen | Trainingsschleife, Verlust- und Accuracy-Kurven |
| 5 | Bewertungsmaße | Konfusionsmatrix, Accuracy, Precision, Recall, F-Score, RMSE, MAE, R² |
| 6 | Overfitting erkennen | Overfitting erkennen, Vergleich Trainings-/Testdaten |
| 7 | Bias, Varianz, irreduzibler Fehler | Bias-Varianz-Trade-off, irreduzibler Fehler |
| 8 | Data Augmentation | Data Augmentation |
| 9 | Data Leakage | Skalierung vor dem Split, Target-Leakage, zeitliches Leakage, Duplikate |
| 10 | Zeitreihen | Zeitbasierte vs. zufällige Aufteilung, Windowing |
| 11 | Zusammenfassung | — |
| 12 | Ausblick (nicht prüfungsrelevant) | — |

---

## 1 · Die drei Datenmengen

**Definition**

Vor dem Training wird der Datensatz in getrennte Teilmengen zerlegt:

**Trainingsdaten**
: Die Daten, aus denen das Modell seine **Parameter** bestimmt. Bei der linearen
  Regression sind das die Koeffizienten, beim neuronalen Netz die Gewichte und
  Bias-Werte. Nur diese Menge fließt in die Optimierung ein.

**Validierungsdaten**
: Die Daten, an denen **Hyperparameter** eingestellt werden: `max_depth` beim Baum,
  `k` bei kNN, Lernrate und Epochenzahl beim Netz. Das Modell lernt hieraus nicht,
  wird aber daran ausgerichtet.

**Testdaten**
: Die Daten für die **einmalige Schlussbewertung** des fertigen Modells.

### Typische Verhältnisse

| Aufteilung | Wann |
|---|---|
| 80 / 20 (Train / Test) | wenn keine Hyperparameter eingestellt werden |
| 70 / 15 / 15 | Standardfall |
| 60 / 20 / 20 | wenn viel eingestellt wird und Daten reichlich sind |

*Beispiel:* 1000 Datensätze bei 70/15/15 ergeben 700 / 150 / 150.

Die Zahlen sind Konventionen, keine Gesetze. Entscheidend ist, ob jede Menge genug
Fälle enthält, damit die daraus berechnete Kennzahl belastbar ist.

### Repräsentativität

**Definition:** Eine Teilmenge ist repräsentativ, wenn ihre Zusammensetzung der
Zusammensetzung des Gesamtdatensatzes entspricht.

- **Mischen vor dem Split** ist bei ungeordneten Daten Pflicht. Ist ein Datensatz nach
  der Zielvariablen sortiert, enthielte die Testmenge sonst womöglich nur eine Klasse.
- **Stratifizierung** hält die Klassenverhältnisse in allen Mengen gleich. Bei
  unausgewogenen Daten notwendig.
- **Ausnahme Zeitreihen:** Dort wird nicht gemischt (siehe Abschnitt 10).

> **Merksatz**
> Erst trennen, dann alles andere. Jede Aufbereitung kommt nach dem Split.

**Das sollten Sie erklären können**

- Wofür jede der drei Mengen zuständig ist
- Warum vor dem Split gemischt wird und wann nicht
- Was Stratifizierung bewirkt

---

## 2 · Validierungsdaten vs. Testdaten

Diese Unterscheidung wird am häufigsten verwechselt. Der Unterschied liegt **nicht** in
der Art der Daten. Beide Mengen sind ungesehene Daten aus derselben Quelle. Der
Unterschied liegt darin, **wie oft** sie benutzt werden und **was der Zugriff bewirkt**.

| | Validierungsdaten | Testdaten |
|---|---|---|
| **Zweck** | Entscheidungen treffen | Ergebnis berichten |
| **Zugriffe** | viele | genau einer |
| **Wirkung** | verändert das Modell | verändert nichts |
| **Fehlerschätzung** | etwas zu optimistisch | unverzerrt |
| **Analogie** | Übungsklausur mit Korrektur | Prüfung |

### Warum eine dritte Menge nötig ist

Wer zehn Varianten eines Modells ausprobiert und die beste auswählt, wählt teilweise
diejenige aus, die zufällig zu genau dieser Bewertungsmenge passt. Das Ergebnis dieser
Menge ist danach geschönt. Deshalb braucht es eine weitere Menge, die an keiner
Entscheidung beteiligt war.

> **Merksatz**
> Die Testmenge wird in dem Moment zur Validierungsmenge, in dem jemand ihr Ergebnis
> ansieht und daraufhin etwas am Modell ändert. Dieser Wechsel ist nicht umkehrbar.

**Wann genügen zwei Mengen?** Wenn keine einzige Entscheidung anhand von Ergebnissen
getroffen wird: feste Hyperparameter, ein Durchlauf, fertig.

**Das sollten Sie erklären können**

- Den Unterschied zwischen Validierungs- und Testdaten in einem Satz
- Warum die Validierungsschätzung optimistisch ist
- Wann zwei Mengen ausreichen

---

## 3 · n-fache Cross-Validierung

**Definition**

Bei der n-fachen Cross-Validierung (Kreuzvalidierung) wird die Datenmenge in $n$ gleich
große, nicht überlappende Teile zerlegt, die **Folds**. Es folgen $n$ Durchläufe: In
jedem Durchlauf dient ein anderer Fold als Bewertungsmenge, die übrigen $n-1$ Folds
dienen als Trainingsmenge. Die $n$ Ergebnisse werden gemittelt.

*Hinweis:* In der Literatur und in scikit-learn heißt der Parameter **k** (*k-fold*).
„n-fach" und „k-fach" meinen dasselbe.

### Ablauf bei n = 5

```
Durchlauf 1:   [B] [T] [T] [T] [T]
Durchlauf 2:   [T] [B] [T] [T] [T]
Durchlauf 3:   [T] [T] [B] [T] [T]
Durchlauf 4:   [T] [T] [T] [B] [T]
Durchlauf 5:   [T] [T] [T] [T] [B]

[T] = Training     [B] = Bewertung
```

Bei 1000 Datensätzen und $n = 5$ enthält jeder Fold 200 Datensätze. Jeder Datensatz
wird genau einmal bewertet und viermal zum Training benutzt.

### Wozu Cross-Validierung?

Ein einzelner Split hat einen Nachteil: Das Ergebnis hängt davon ab, welche Fälle
zufällig in der Bewertungsmenge gelandet sind. Die Cross-Validierung mittelt über
mehrere Aufteilungen und nutzt außerdem jeden Datenpunkt sowohl zum Trainieren als auch
zum Bewerten. Das ist besonders bei **kleinen Datensätzen** wertvoll.

### Schwankung zwischen den Folds

Neben dem Mittelwert wird die **Streuung** der Einzelergebnisse ausgewertet.

*Beispiel:* Fünf Folds liefern die Accuracy-Werte 0,82 · 0,85 · 0,71 · 0,88 · 0,84.

- Mittelwert: $4{,}10 / 5 = 0{,}82$
- Spannweite: 0,71 bis 0,88, also 17 Prozentpunkte

| Beobachtung | Deutung |
|---|---|
| Geringe Streuung | Das Ergebnis hängt kaum von der Aufteilung ab. Stabile Schätzung. |
| Hohe Streuung | Das Ergebnis hängt stark davon ab, welche Fälle im Bewertungsfold liegen. Ursachen: zu wenige Daten, heterogene Daten, seltene Klassen ungleich verteilt. |

> **Merksatz**
> Ein Mittelwert allein sagt zu wenig. Erst Mittelwert **und** Streuung ergeben ein
> Bild. Hohe Streuung ist ein Warnsignal.

### Was genau wird validiert?

Der zurückgehaltene Fold ist eine **Validierungsmenge**, kein Testset. Wird die
Cross-Validierung benutzt, um zwischen Modellen zu entscheiden, gilt Abschnitt 2: Das
Ergebnis ist eine Entscheidungsgrundlage und damit etwas zu optimistisch. Sauber ist:

```
Gesamtdaten
   |
   +-- Testmenge          <- zuerst abtrennen, dann nicht mehr anfassen
   |
   +-- Entwicklungsmenge  <- hierauf läuft die Cross-Validierung
```

Ein zweiter Punkt: Bei der Cross-Validierung entstehen $n$ Modelle, von denen keines das
Endprodukt ist. Das endgültige Modell wird anschließend auf allen Entwicklungsdaten neu
trainiert. Die Cross-Validierung bewertet also ein **Verfahren**, nicht ein einzelnes
Modell.

### Gegenüberstellung: einfacher Split oder Cross-Validierung?

| | Einfacher Split | n-fache Cross-Validierung |
|---|---|---|
| Trainingsläufe | 1 | $n$ |
| Rechenaufwand | gering | $n$-fach |
| Datenausnutzung | ein Teil wird nie trainiert | jeder Punkt dient beidem |
| Stabilität | von der einen Aufteilung abhängig | gemittelt, stabiler |
| Zusatzinformation | keine | Streuung über die Folds |
| Geeignet bei | großen Datenmengen | kleinen bis mittleren Datenmengen |
| Bei Zeitreihen | zeitlich, ja | in der Standardform nein |

Übliche Werte sind $n = 5$ oder $n = 10$.

**Das sollten Sie erklären können**

- Den Ablauf der n-fachen Cross-Validierung beschreiben
- Aus gegebenen Fold-Ergebnissen Mittelwert und Streuung bestimmen und deuten
- Begründen, wann sich der Mehraufwand lohnt und wann nicht

---

## 4 · Aufteilung bei neuronalen Netzen

Beim neuronalen Netz wird üblicherweise in **drei feste Mengen** geteilt und **nicht**
kreuzvalidiert. Vier Gründe, nach Gewicht:

**1. Rechenaufwand.** $n$ Folds bedeuten $n$ vollständige Trainingsläufe. Bei einem
Netz, das Stunden trainiert, entscheidet dieser Punkt allein.

**2. Datenmenge.** Cross-Validierung nützt vor allem bei knappen Daten. Bei 60 000
Bildern enthält eine 10-Prozent-Validierungsmenge bereits 6000 Fälle. Die Schätzung ist
auch ohne Mittelung stabil.

**3. Die Validierungsmenge hat hier eine andere Aufgabe.** Sie wird nicht am Ende
einmal abgefragt, sondern **in jeder Epoche**. Sie steuert Entscheidungen mitten im
Training:

| Wozu | Was passiert |
|---|---|
| Early Stopping | Training abbrechen, wenn der Validierungsverlust nicht mehr sinkt |
| Modellauswahl | die Gewichte der besten Epoche behalten |
| Lernrate anpassen | Lernrate senken, wenn die Kurve stagniert |

Damit ist die Validierungsmenge Teil der Trainingsschleife. Ein Trainingslauf lässt sich
nicht sinnvoll „in Folds aufteilen".

**4. Andere Streuungsquellen.** Bei neuronalen Netzen streut das Ergebnis ohnehin über
die zufällige Initialisierung der Gewichte. Wiederholungen mit verschiedenen Startwerten
sind hier oft aussagekräftiger als Wiederholungen über Folds.

> **Merksatz**
> Weil die Validierungsmenge beim Netz in jeder Epoche abgefragt wird, ist ihr Ergebnis
> am Ende geschönt. Genau deshalb braucht das Netz zusätzlich eine Testmenge.

**Wann Cross-Validierung auch bei Netzen vorkommt:** bei sehr kleinen Datensätzen, etwa
in medizinischen Anwendungen.

**Das sollten Sie erklären können**

- Warum bei neuronalen Netzen meist nicht kreuzvalidiert wird
- Welche drei Entscheidungen die Validierungsmenge während des Trainings steuert
- Warum trotz Validierungsmenge zusätzlich eine Testmenge nötig ist

---

## 5 · Bewertungsmaße

### Klassifikation

Die **Konfusionsmatrix** stellt Vorhersage und Wahrheit gegenüber. Die positive Klasse
muss vorher festgelegt werden.

| | Vorhersage positiv | Vorhersage negativ |
|---|---|---|
| **tatsächlich positiv** | TP (richtig positiv) | FN (falsch negativ) |
| **tatsächlich negativ** | FP (falsch positiv) | TN (richtig negativ) |

$$\text{Accuracy} = \frac{TP+TN}{TP+TN+FP+FN} \qquad
\text{Precision} = \frac{TP}{TP+FP} \qquad
\text{Recall} = \frac{TP}{TP+FN}$$

$$\text{F1} = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision}+\text{Recall}}$$

*Rechenbeispiel:* TP = 40, FN = 10, FP = 20, TN = 430 (500 Fälle)

- Accuracy $= 470/500 = 0{,}94$
- Precision $= 40/60 = 0{,}67$
- Recall $= 40/50 = 0{,}80$
- $\text{F1} = 2 \cdot (0{,}67 \cdot 0{,}80) / (0{,}67 + 0{,}80) = 0{,}73$

**In Worten:** Precision beantwortet „Wie viele der als positiv gemeldeten Fälle waren
es wirklich?" Recall beantwortet „Wie viele der tatsächlich positiven Fälle wurden
gefunden?"

> **Merksatz zur Metrikwahl**
> Bei unausgewogenen Klassen täuscht die Accuracy. Im Beispiel oben erreicht ein
> Modell, das immer „negativ" sagt, eine Accuracy von $450/500 = 0{,}90$ bei einem
> Recall von 0. Es findet keinen einzigen positiven Fall.

### Regression

$$\text{MAE} = \frac{1}{m} \cdot \sum \lvert y - \hat{y} \rvert$$

$$\text{RMSE} = \sqrt{\frac{1}{m} \cdot \sum (y - \hat{y})^2}$$

Dabei ist $m$ die Anzahl der Datenpunkte, $y$ der wahre Wert und $\hat{y}$ die
Vorhersage. Summiert wird über alle $m$ Datenpunkte.

$R^2$ gibt den Anteil der erklärten Varianz an.

| Maß | Eigenschaft |
|---|---|
| MAE | in der Einheit der Zielgröße direkt lesbar, behandelt alle Fehler gleich |
| RMSE | bestraft große Einzelfehler stärker, weil quadriert wird |
| $R^2$ | einheitenlos, über Datensätze hinweg vergleichbar |

**Das sollten Sie erklären können**

- Aus einer gegebenen Konfusionsmatrix alle vier Maße berechnen
- Begründen, wann Accuracy irreführend ist
- Den Unterschied zwischen MAE und RMSE benennen

---

## 6 · Overfitting erkennen

**Definition**

**Overfitting (Überanpassung)** liegt vor, wenn ein Modell Eigenheiten der
Trainingsdaten abbildet, die in neuen Daten nicht wiederkehren. Es lernt Rauschen statt
Struktur.

**Underfitting (Unteranpassung)** liegt vor, wenn ein Modell zu wenig Kapazität hat, um
die vorhandene Struktur überhaupt abzubilden.

### Die Diagnose: zwei Werte vergleichen

Overfitting sieht man **nie an einem einzelnen Wert**, sondern immer am Vergleich:

| Trainingsfehler | Testfehler | Diagnose |
|---|---|---|
| hoch | hoch | **Underfitting** — Modell zu einfach oder Merkmale untauglich |
| niedrig | niedrig | passend |
| niedrig | hoch | **Overfitting** |
| hoch | niedrig | Aufbaufehler — nachrechnen |

*Beispiel:* Ein Entscheidungsbaum ohne Tiefenbegrenzung erreicht 100 % Accuracy auf den
Trainingsdaten und 68 % auf den Testdaten. Klassisches Overfitting.

### Beim neuronalen Netz: die Kurven lesen

Trägt man Trainings- und Validierungsverlust über die Epochen auf, zeigt sich derselbe
Sachverhalt als Kurvenverlauf:

```
Verlust
   |
   |\
   | \.                    ___ Validierung steigt wieder
   |  \  `-.        ___.--'
   |   \     `-.--''
   |    `--.._______________ Training sinkt weiter
   |
   +-------------------------------> Epoche
              ^
              hier trennen sich die Kurven
```

Der Trainingsverlust sinkt weiter, der Validierungsverlust steigt ab einem Punkt wieder.
Dieser Punkt ist der richtige Abbruchzeitpunkt für **Early Stopping**.

### Gegenmaßnahmen und wo sie ansetzen

| Maßnahme | Setzt an bei | Themengebiet |
|---|---|---|
| Tree Pruning (`max_depth`, `min_samples_leaf`) | Modellkapazität | Entscheidungsbäume |
| L1-/L2-Regularisierung | Modellkapazität | Regression, neuronale Netze |
| Dropout | Modellkapazität | neuronale Netze |
| Early Stopping | Trainingsdauer | Training neuronaler Netze |
| Batch Normalisierung | Stabilität der Optimierung | neuronale Netze |
| Data Augmentation | Datenmenge und -vielfalt | Robustheit |
| Bagging / Random Forest | Varianz durch Mittelung | Ensemble-Verfahren |
| Mehr Trainingsdaten | Datenmenge | grundsätzlich |

**Das sollten Sie erklären können**

- Overfitting anhand zweier Fehlerwerte erkennen und von Underfitting unterscheiden
- Eine Verlustkurve deuten und den Early-Stopping-Punkt benennen
- Zu jeder Gegenmaßnahme sagen, woran sie ansetzt

---

## 7 · Bias, Varianz und irreduzibler Fehler

**Definition**

Der erwartete Fehler eines Modells zerfällt in drei Anteile:

$$\text{Fehler} = \text{Bias}^2 + \text{Varianz} + \text{irreduzibler Fehler}$$

**Bias (Verzerrung)**
: Fehler durch zu starke Vereinfachung. Ein Modell mit hohem Bias verfehlt die Struktur
  systematisch, unabhängig davon, wie viele Daten es bekommt.
  *Beispiel:* eine Gerade für einen erkennbar gekrümmten Zusammenhang.

**Varianz**
: Fehler durch zu starke Abhängigkeit von den konkreten Trainingsdaten. Ein Modell mit
  hoher Varianz sieht bei einem anderen Trainingssplit deutlich anders aus.
  *Beispiel:* ein ungestutzter Entscheidungsbaum.

**Irreduzibler Fehler (Bayes-Fehler)**
: Der Anteil, den auch ein perfektes Modell nicht beseitigen kann, weil die Zielgröße
  aus den verfügbaren Merkmalen nicht vollständig bestimmt ist. Er ist die
  **Untergrenze** des erreichbaren Fehlers.

### Der Zusammenhang

| | Bias | Varianz | zeigt sich als |
|---|---|---|---|
| Modell zu einfach | hoch | niedrig | Underfitting |
| Modell zu komplex | niedrig | hoch | Overfitting |
| passend | mittel | mittel | gute Generalisierung |

Erhöht man die Modellkomplexität, sinkt der Bias und steigt die Varianz. Dazwischen
liegt ein Optimum.

**Querbezug:** Bagging (Random Forest) reduziert die **Varianz** durch Mittelung über
viele Bäume. Boosting reduziert den **Bias**, indem schwache Modelle nacheinander die
Fehler ihrer Vorgänger korrigieren.

> **Merksatz**
> Der irreduzible Fehler ist die Untergrenze. Wer sie scheinbar unterbietet, hat einen
> Fehler im Aufbau, meistens Data Leakage.

**Das sollten Sie erklären können**

- Bias und Varianz jeweils an einem Beispiel erläutern
- Den Trade-off in eigenen Worten beschreiben
- Sagen, was der irreduzible Fehler ist und warum er nicht unterschritten werden kann

---

## 8 · Data Augmentation

**Definition**

Unter **Data Augmentation** versteht man das künstliche Vergrößern der **Trainingsmenge**
durch Transformationen, die das Label unverändert lassen. Bei Bildern zum Beispiel:

| Art | Beispiele |
|---|---|
| geometrisch | Spiegeln, Verschieben, Drehen, Ausschnitt, Skalieren |
| photometrisch | Helligkeit, Kontrast, Farbverschiebung |
| Störung | Rauschen hinzufügen, Bildteile verdecken |

### Wozu?

Die Transformationen bringen dem Netz bei, was **egal** sein soll: Eine gespiegelte Katze
ist eine Katze. Damit ist Augmentierung zugleich eine Maßnahme gegen Overfitting und
eingebrachtes Fachwissen. Sie hilft besonders bei kleinen Datensätzen und lässt sich
gezielt auf unterrepräsentierte Klassen anwenden.

### Drei Grenzen

**1. Nur auf den Trainingsdaten.** Validierungs- und Testdaten werden nie augmentiert.
Wer **vor** dem Split augmentiert, verteilt Varianten desselben Ausgangsbildes auf beide
Seiten. Das ist Duplikat-Leakage (Abschnitt 9).

**2. Label-Erhaltung ist eine fachliche Entscheidung.** Horizontales Spiegeln ist bei
Katzenbildern richtig und bei handschriftlichen Ziffern falsch, weil eine gespiegelte 2
keine 2 mehr ist und 6 und 9 verwechselbar werden. Es gibt keine allgemeingültige
Augmentierungsliste.

**3. Es entsteht keine neue Information.** Augmentierung behebt keine falschen Labels,
keine verzerrte Stichprobe und keine im Datensatz fehlende Klasse.

> **Merksatz**
> Augmentierung ist eine Behauptung über die Domäne: „Diese Veränderung ändert das
> Label nicht." Wer die Behauptung nicht prüft, erzeugt falsch gelabelte Trainingsdaten.

**Das sollten Sie erklären können**

- Was Augmentierung bewirkt und warum sie gegen Overfitting hilft
- Warum sie nur auf Trainingsdaten angewandt wird
- Ein Beispiel nennen, bei dem eine Transformation das Label zerstört

---

## 9 · Data Leakage

**Definition**

**Data Leakage (Informationsabfluss)** ist das Einfließen von Information in den
Modellbildungsprozess, die zum Zeitpunkt der Vorhersage in der realen Anwendung nicht
zur Verfügung stünde.

> **Merksatz zur Wirkungsrichtung**
> Leakage macht das gemeldete Ergebnis **zu gut**. Das Modell versagt anschließend im
> Einsatz. Leakage schönt, es verschlechtert nicht.

### Form 1 · Skalierung vor dem Split

**Was passiert:** Eine Vorverarbeitung, die Kennwerte **aus den Daten lernt**, wird auf
den ganzen Datensatz angewandt, bevor getrennt wird. Die gelernten Kennwerte enthalten
dann Information aus den Testdaten.

| Verfahren | Was es aus den Daten lernt |
|---|---|
| `StandardScaler` (z-Scores) | Mittelwert und Standardabweichung |
| `MinMaxScaler` | Minimum und Maximum |
| Imputation fehlender Werte | Mittelwert bzw. Median der Spalte |
| PCA | die Hauptkomponenten |
| Feature-Selektion | welche Merkmale nützlich sind |

**Nicht betroffen** sind Umrechnungen mit festen, vorab bekannten Konstanten, etwa das
Teilen von Graustufenwerten durch 255.

**Die Regel:**

```
fit / fit_transform  ->  NUR auf den Trainingsdaten
transform            ->  auf allen Mengen, mit den aus dem Training gelernten Werten
```

### Form 2 · Target-Leakage

**Was passiert:** Ein Merkmal verrät die Zielvariable, weil es zum Vorhersagezeitpunkt
noch gar nicht vorläge.

*Beispiele:*

- Bluthochdruck vorhersagen und dabei die Einnahme blutdrucksenkender Medikamente als
  Merkmal verwenden
- Maschinenausfall vorhersagen und dabei das Feld „Reparaturdatum" mitführen
- Kaufabschluss vorhersagen und dabei die Rechnungsnummer mitführen

**Die Prüffrage:** Läge dieser Wert zum Vorhersagezeitpunkt tatsächlich vor? Das ist ein
fachliches Urteil, kein technisches.

### Form 3 · Zeitliches Leakage

**Was passiert:** Das Modell wird mit Daten trainiert, die zeitlich **nach** den
Bewertungsdaten liegen. Es lernt aus der Zukunft, um die Vergangenheit vorherzusagen.

Häufigster Auslöser: zufälliges Mischen oder Standard-Cross-Validierung bei Zeitreihen.
Ausführlich in Abschnitt 10.

### Form 4 · Duplikate über Splitgrenzen

**Was passiert:** Derselbe oder ein fast identischer Fall liegt in Trainings- **und**
Testmenge. Das Modell erkennt in der Bewertung etwas wieder.

*Typische Auslöser:*

- echte Duplikate im Rohdatensatz, vor dem Split nicht entfernt
- mehrere Aufnahmen desselben Objekts, etwa fünf Fotos desselben Werkstücks
- Augmentierung vor dem Split

**Die Regel:** Duplikate **vor** dem Split entfernen.

### Prüfschema

Bei jeder Fallanalyse in dieser Reihenfolge durchgehen:

1. Wurde **zuerst** getrennt und **danach** aufbereitet?
2. Wurde jede gelernte Transformation nur auf den Trainingsdaten gefittet?
3. Läge jedes Merkmal zum Vorhersagezeitpunkt vor?
4. Ist bei zeitlichen Daten der Split chronologisch?
5. Gibt es Duplikate über die Grenze hinweg?
6. Ist das Ergebnis plausibel oder zu gut für diese Aufgabe?

**Das sollten Sie erklären können**

- Alle vier Formen benennen und je ein Beispiel geben
- Die Wirkungsrichtung begründen
- In einem vorgelegten Vorgehen die fehlerhafte Stelle finden und benennen

---

## 10 · Zeitreihen

### Warum die Standardregeln hier nicht gelten

Bei Zeitreihen sind zwei Voraussetzungen verletzt, die sonst gelten:

- **Unabhängigkeit:** Benachbarte Werte hängen voneinander ab (Autokorrelation).
- **Beliebige Reihenfolge:** Die Reihenfolge trägt Information (Trend, Saisonalität).

### Zeitbasierte vs. zufällige Aufteilung

| | Zufällige Aufteilung | Zeitbasierte Aufteilung |
|---|---|---|
| Vorgehen | mischen, dann trennen | chronologisch trennen, nicht mischen |
| Zulässig bei | unabhängigen Fällen (Bilder, Kundendatensätze) | Zeitreihen |
| Bei Zeitreihen | zeitliches Leakage | korrekt |
| Simuliert | nichts Reales | die tatsächliche Einsatzsituation |

**Warum zufälliges Mischen hier so stark schönt:** Bei einer glatten Reihe liegen die
unmittelbaren zeitlichen Nachbarn eines Bewertungspunktes im Training. Das Modell muss
keine Struktur lernen, es genügt, zwischen den bekannten Nachbarwerten zu interpolieren.
Das Ergebnis sieht ausgezeichnet aus und sagt über die Prognosefähigkeit nichts.

Dieselbe Überlegung gilt für die Standard-Cross-Validierung: Sie zerlegt die Reihe ohne
Rücksicht auf die Zeitachse und ist bei Zeitreihen daher in ihrer Standardform nicht
anwendbar.

### Windowing

**Definition:** Beim **Windowing** wird eine Zeitreihe in überlappende Abschnitte
zerlegt, um sie als überwachtes Lernproblem zu formulieren.

**Fenstergröße $w$**
: Anzahl der zurückliegenden Zeitschritte, die als Eingabe dienen.

**Horizont $h$**
: Anzahl der Zeitschritte, um die die Vorhersage in der Zukunft liegt. Bei $h = 1$ wird
  der unmittelbar folgende Wert vorhergesagt.

**Anzahl erzeugbarer Trainingsbeispiele:**

$$\text{Anzahl Fenster} = n - w - h + 1$$

*Beispiel AirPassengers:* $n = 144$ Monate, $w = 12$, $h = 1$
$\rightarrow 144 - 12 - 1 + 1 = 132$ Fenster.
Bei $h = 3$ wären es $144 - 12 - 3 + 1 = 130$.

```
Reihe:      o o o o o o o o o o o o o o o o o
Fenster 1:  [----- w = 12 -----] -> Ziel
Fenster 2:    [----- w = 12 -----] -> Ziel
Fenster 3:      [----- w = 12 -----] -> Ziel
```

Die Fenster **überlappen** einander. Zwei aufeinanderfolgende Fenster teilen sich $w-1$
Zeitschritte. Innerhalb der Trainingsmenge ist das unschädlich.

### Die Splitgrenze

**Die Regel:** Kein Trainingsbeispiel darf einen Zeitpunkt berühren, der zu einem
Bewertungsziel gehört oder danach liegt.

Praktisch: Den höchsten vom Training berührten Zeitindex bestimmen und mit dem Index des
ersten Bewertungsziels vergleichen. Der zweite muss größer sein.

Bei $h = 1$ ergibt sich der nötige Abstand von einem Zeitschritt von selbst. Bei $h > 1$
nicht: Dann reicht das Ziel eines Fensters $h$ Schritte über dessen Fensterende hinaus,
und zwischen Trainings- und Testblock muss eine Lücke von mindestens $h$ Zeitschritten
bleiben.

### Naive Vergleichsmaßstäbe

Ein Zeitreihenmodell ist erst dann etwas wert, wenn es ein triviales Verfahren schlägt:

**Persistenz (naive Prognose)**
: $\hat{y}[t] = y[t-1]$, also „morgen wie heute"

**Seasonal Naive**
: $\hat{y}[t] = y[t-s]$ mit der Saisonperiode $s$, also „gleicher Monat wie im Vorjahr"

Bei einer Reihe mit klarer Jahressaison und Monatsdaten ist $s = 12$, und Seasonal Naive
ist der **faire** Maßstab. Ein Modell, das nur die Persistenz schlägt, hat womöglich
lediglich den Trend gelernt.

**Querbezug:** Dasselbe $s$ tritt bei SARIMA im saisonalen Teil $(P,D,Q,s)$ auf und muss
zur Datenfrequenz passen.

**Das sollten Sie erklären können**

- Warum bei Zeitreihen nicht gemischt wird
- Aus $n$, $w$ und $h$ die Anzahl der Fenster berechnen
- Prüfen, ob eine gegebene Splitgrenze korrekt liegt
- Beide naiven Vergleichsmaßstäbe angeben und begründen, welcher passt

---

## 11 · Zusammenfassung

### Neun Merksätze

> **1** Erst trennen, dann aufbereiten. Immer in dieser Reihenfolge.
>
> **2** `fit` nur auf Trainingsdaten, `transform` auf alle.
>
> **3** Die Validierungsmenge dient Entscheidungen, die Testmenge dem Bericht.
>
> **4** Die Testmenge wird genau einmal benutzt.
>
> **5** Bei Cross-Validierung immer Mittelwert **und** Streuung angeben.
>
> **6** Overfitting erkennt man nur im Vergleich zweier Fehlerwerte, nie an einem.
>
> **7** Bei Zeitreihen ist die Zeit die Trennlinie. Nicht mischen.
>
> **8** Augmentierung nur auf den Trainingsdaten und nur label-erhaltend.
>
> **9** Ein auffällig gutes Ergebnis ist zuerst ein Leakage-Verdacht.

### Was allen Regeln gemeinsam ist

Wenn Sie die neun Merksätze verdichten, bleiben drei Fragen übrig. Das ist **kein
zusätzlicher Lernstoff**, sondern eine Rückfallebene für den Fall, dass Ihnen in einer
Aufgabe die passende Einzelregel nicht einfällt:

1. **Was ist eine unabhängige Einheit?** Zeile, Bild, Werkstück, Zeitfenster? Zwei
   voneinander abhängige Fälle dürfen nicht auf verschiedene Seiten der Trennlinie
   geraten. → Merksätze 1, 7, 8
2. **Was weiß ich zum Vorhersagezeitpunkt?** Alles andere darf das Modell nicht sehen.
   → Merksätze 2, 7
3. **Wie oft habe ich diese Datenmenge schon benutzt?** Jeder Zugriff, der zu einer
   Änderung führt, verbraucht ein Stück ihrer Aussagekraft. → Merksätze 3, 4, 5

---

## 12 · Ausblick — **nicht prüfungsrelevant**

> Außerhalb unserer Prüfungsgrenzen sind weitere Prinzipien wichtig, die Ihnen bei
> späterer Arbeit begegnen werden:
>
> **verschachtelte Kreuzvalidierung** · **Purging und Embargo bei Zeitreihen** ·
> **Aufteilen nach Gruppen statt nach Zeilen (GroupKFold)** · **Sampling-Bias und
> Verteilungsverschiebung** · **Mixup und CutMix** · **Test-Time-Augmentation** ·
> **Permutationstest zur Leakage-Erkennung** · **Modell-Infoblätter zur Dokumentation**
>
> Diese Themen werden **explizit nicht abgefragt**. Sie sind hier nur genannt, damit
> erkennbar ist, dass sie bewusst ausgenommen wurden.

---

## 13 · Literatur

**Data Leakage**

- Kaufman, S., Rosset, S., Perlich, C., Stitelman, O. (2012). *Leakage in Data Mining:
  Formulation, Detection, and Avoidance.* ACM Transactions on Knowledge Discovery from
  Data 6(4), Artikel 15. DOI: 10.1145/2382577.2382579
- Kapoor, S., Narayanan, A. (2023). *Leakage and the reproducibility crisis in
  machine-learning-based science.* Patterns 4(9), 100804.
  DOI: 10.1016/j.patter.2023.100804

**Cross-Validierung und Modellauswahl**

- Kohavi, R. (1995). *A Study of Cross-Validation and Bootstrap for Accuracy Estimation
  and Model Selection.* Proceedings IJCAI 1995.
- Cawley, G. C., Talbot, N. L. C. (2010). *On Over-fitting in Model Selection and
  Subsequent Selection Bias in Performance Evaluation.* Journal of Machine Learning
  Research 11, 2079–2107.
- Dwork, C., Feldman, V., Hardt, M., Pitassi, T., Reingold, O., Roth, A. (2015).
  *Generalization in Adaptive Data Analysis and Holdout Reuse.* NeurIPS 2015.

**Zeitreihen**

- Roberts, D. R. et al. (2017). *Cross-validation strategies for data with temporal,
  spatial, hierarchical, or phylogenetic structure.* Ecography 40, 913–929.
- Box, G. E. P., Jenkins, G. M. (1976). *Time Series Analysis: Forecasting and Control.*
  Holden-Day. Quelle des AirPassengers-Datensatzes.

**Data Augmentation**

- LeCun, Y., Bottou, L., Bengio, Y., Haffner, P. (1998). *Gradient-Based Learning
  Applied to Document Recognition.* Proceedings of the IEEE 86(11), 2278–2324.
- Krizhevsky, A., Sutskever, I., Hinton, G. E. (2012). *ImageNet Classification with
  Deep Convolutional Neural Networks.* NeurIPS 2012.
- Shorten, C., Khoshgoftaar, T. M. (2019). *A survey on Image Data Augmentation for
  Deep Learning.* Journal of Big Data 6, 60.

**Praxis**

- scikit-learn: *Common pitfalls and recommended practices.*
  https://scikit-learn.org/stable/common_pitfalls.html
- scikit-learn: *Cross-validation: evaluating estimator performance.*
  https://scikit-learn.org/stable/modules/cross_validation.html

---

*iludis.de — Kurzreferenz zur Prüfungsvorbereitung KI und Maschinelles Lernen (DQR 5)*
