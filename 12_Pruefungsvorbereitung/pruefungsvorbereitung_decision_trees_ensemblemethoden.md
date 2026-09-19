# Prüfungsvorbereitung: Decision Trees, Ensemblemethoden, Pruning und Hyperparameter-Tuning

## Ziel dieser Wiederholung

Diese Zusammenfassung vernetzt die wichtigsten Konzepte rund um Decision Trees:

- Wie lernt ein einzelner Decision Tree?
- Was unterscheidet Bagging, Random Forest und Boosting?
- Was bedeuten Feature Subsampling und Pruning?
- Welche Rolle spielen Validierungsdaten und k-fold Cross-Validation?
- Was ist ein Modellparameter, was ein Hyperparameter?
- Was geschieht automatisch beim Training – und was muss ausdrücklich angestoßen werden?

Der zentrale Gedanke lautet: **Bagging, Boosting, Feature Subsampling und Pruning beschreiben, wie ein Modell aufgebaut oder vereinfacht wird. Cross-Validation und Suchverfahren wie Grid Search liegen eine Ebene darüber: Sie bewerten und konfigurieren den gesamten Trainingsprozess.**

---

## 1. Ausgangspunkt: der einzelne Decision Tree

Ein Decision Tree zerlegt den Merkmalsraum schrittweise durch Entscheidungsregeln. Bei jedem inneren Knoten sucht der Trainingsalgorithmus nach einem geeigneten Merkmal und einem geeigneten Schwellenwert.

Beispiel:

> „Teile nach dem Merkmal `Alter` beim Schwellenwert 35.“

Während des Trainings lernt der Baum unter anderem:

- welches Feature an einem Knoten verwendet wird,
- bei welchem Wert gesplittet wird,
- welche weiteren Verzweigungen entstehen,
- welche Vorhersage ein Blatt ausgibt.

Diese gelernten Bestandteile sind **Modellparameter**. Sie werden durch einen normalen Aufruf von `.fit()` automatisch aus den Trainingsdaten bestimmt.

Ein einzelner, tief wachsender Decision Tree ist flexibel, aber oft instabil: Kleine Änderungen in den Trainingsdaten können zu einem deutlich anderen Baum führen. Außerdem kann ein sehr tiefer Baum Besonderheiten oder Rauschen der Trainingsdaten auswendig lernen. Das nennt man **Overfitting**.

Genau an diesen Schwächen setzen Bagging, Boosting und Pruning auf unterschiedliche Weise an.

---

## 2. Bagging: viele unabhängige Bäume zusammenfassen

**Bagging** steht für *Bootstrap Aggregating*. Statt nur einen Baum zu trainieren, werden viele Bäume auf leicht unterschiedlichen Stichproben desselben Trainingsdatensatzes trainiert.

### Ablauf

1. Aus einem Trainingsdatensatz mit \(n\) Beobachtungen wird typischerweise eine neue Stichprobe mit ebenfalls \(n\) Ziehungen erzeugt.
2. Es wird **mit Zurücklegen** gezogen. Eine Beobachtung kann deshalb mehrfach vorkommen, eine andere überhaupt nicht. Das ist eine **Bootstrap-Stichprobe**.
3. Für jede Bootstrap-Stichprobe wird ein eigener Decision Tree trainiert.
4. Die Bäume werden unabhängig voneinander trainiert und ihre Vorhersagen anschließend aggregiert.

Die Aggregation erfolgt typischerweise so:

- **Klassifikation:** Mehrheitsentscheidung
- **Regression:** arithmetischer Mittelwert

### Kurzes Beispiel

Für die Vorhersage, ob ein Kunde ein Produkt kauft, werden 50 Bäume trainiert. Für einen neuen Kunden sagen

- 38 Bäume: „kauft“
- 12 Bäume: „kauft nicht“

Die Mehrheitsentscheidung lautet daher **„kauft“**.

### Warum funktioniert Bagging?

Ein einzelner Decision Tree besitzt häufig eine hohe **Varianz**: Seine Struktur hängt stark von den konkreten Trainingsdaten ab. Die vielen Bäume des Bagging-Verfahrens machen nicht exakt dieselben zufälligen Fehler. Durch Abstimmung oder Mittelung gleichen sich Teile dieser Fehler aus. Das Gesamtsystem wird stabiler und reduziert vor allem die Varianz.

Beim klassischen Bagging gilt:

- Die Zufälligkeit betrifft die **Beobachtungen beziehungsweise Datenzeilen**.
- Jeder Baum darf bei seinen Splits grundsätzlich **alle Features** betrachten.
- Die Bäume werden unabhängig voneinander trainiert; ihr Training kann daher parallelisiert werden.
- Häufig lässt man die einzelnen Bäume relativ tief wachsen. Die Instabilität des Einzelbaums wird durch die Aggregation reduziert.

Merksatz:

> **Bagging = Bootstrap-Stichproben der Daten + unabhängige Modelle + Aggregation ihrer Vorhersagen.**

---

## 3. Feature Subsampling und Random Forest

Das zufällige Reduzieren der betrachteten Features gehört **nicht** zum klassischen Bagging. Es wird meist als **Random Feature Selection** oder **Feature Subsampling** bezeichnet. Verwandt damit ist die **Random Subspace Method**, bei der Modelle auf zufällig ausgewählten Merkmalsräumen trainiert werden. Beim Random Forest wird die Feature-Teilmenge typischerweise an jedem Split neu gezogen.

### Bagging und Random Forest sauber unterscheiden

| Verfahren | Zufällige Beobachtungen | Zufällige Feature-Auswahl | Kombination der Bäume |
|---|---:|---:|---|
| Klassisches Bagging mit Trees | Ja, über Bootstrap-Stichproben | Nein; grundsätzlich stehen alle Features zur Verfügung | Mehrheit beziehungsweise Mittelwert |
| Random Forest | Ja, typischerweise über Bootstrap-Stichproben | Ja, normalerweise bei jedem Split neu | Mehrheit beziehungsweise Mittelwert |

Beim Random Forest wird an einem Knoten nicht unter allen Merkmalen nach dem besten Split gesucht. Stattdessen erhält der Knoten nur eine zufällige Teilmenge der Features als Kandidaten.

Beispiel: Ein Datensatz besitzt 20 Features.

- Beim klassischen Bagging darf jeder Split alle 20 Features prüfen.
- Beim Random Forest darf ein Split vielleicht nur 4 oder 5 zufällig ausgewählte Features prüfen.
- Beim nächsten Split wird normalerweise erneut eine zufällige Feature-Teilmenge gezogen.

Der Zweck besteht darin, die Bäume stärker voneinander zu unterscheiden. Wenn ein sehr dominantes Feature an jedem Knoten zur Verfügung stünde, könnten viele Bäume trotz unterschiedlicher Bootstrap-Stichproben sehr ähnlich werden. Weniger stark korrelierte Bäume liefern bei der Aggregation meist einen größeren Stabilitätsgewinn.

Merksatz:

> **Random Forest = Bagging der Beobachtungen + zufällige Feature-Auswahl bei den Splits.**

---

## 4. Boosting: Bäume lernen nacheinander

Beim **Boosting** werden die Modelle nicht unabhängig, sondern **sequenziell** trainiert. Jeder neue Baum soll Schwächen des bisherigen Ensembles ausgleichen.

Ein anschauliches Bild:

- **Bagging:** Viele unabhängige Experten geben ihre Stimme ab.
- **Boosting:** Ein Experte beginnt; der nächste konzentriert sich auf die bisherigen Fehler; weitere Experten verbessern das Gesamtergebnis schrittweise.

Beim Boosting werden häufig kleine, eher flache Bäume eingesetzt. Die Modelle werden gewichtet oder additiv zu einer Gesamtvorhersage zusammengesetzt. Wie genau ein neuer Baum die bisherigen Fehler berücksichtigt, hängt vom konkreten Boosting-Verfahren ab.

Bekannte Verfahren sind:

- AdaBoost
- Gradient Boosting
- XGBoost
- LightGBM
- CatBoost

### Bagging und Boosting im direkten Vergleich

| Merkmal | Bagging | Boosting |
|---|---|---|
| Abhängigkeit der Bäume | unabhängig | jeder neue Baum baut auf dem bisherigen Ensemble auf |
| Trainingsreihenfolge | parallel möglich | grundsätzlich sequenziell |
| Typische Bäume | häufig große oder tiefe Bäume | häufig kleine oder flache Bäume |
| Kombination | Mehrheit oder Mittelwert | gewichtete beziehungsweise additive Kombination |
| Hauptidee | zufällige Schwankungen einzelner Modelle ausgleichen | verbleibende Fehler schrittweise korrigieren |
| Typischer statistischer Effekt | vor allem Varianzreduktion | häufig Biasreduktion, teilweise auch Varianzreduktion |

Merksatz:

> **Bagging mittelt unabhängige Modelle; Boosting verbessert ein Ensemble schrittweise.**

---

## 5. Pruning: einen Baum vereinfachen

**Pruning** bedeutet, das Wachstum eines Decision Trees zu begrenzen oder nachträglich Teile des Baums zu entfernen. Ziel ist ein einfacherer Baum, der auf unbekannten Daten besser generalisiert.

### Pre-Pruning

Beim **Pre-Pruning** wird der Baum während des Wachstums früh gestoppt. Typische Hyperparameter sind:

- `max_depth`: maximale Tiefe
- `min_samples_split`: Mindestanzahl von Beobachtungen für einen weiteren Split
- `min_samples_leaf`: Mindestanzahl von Beobachtungen in einem Blatt

Streng genommen wird hier nichts nachträglich abgeschnitten; der betreffende Ast entsteht gar nicht erst.

### Post-Pruning

Beim **Post-Pruning** lässt man den Baum zunächst groß oder vollständig wachsen. Anschließend wird geprüft, welche Teilbäume einen sinnvollen zusätzlichen Vorhersagenutzen liefern. Ein wenig hilfreicher Teilbaum wird durch ein einzelnes Blatt ersetzt.

Die allgemeine Regel lautet:

> **Behalte einen Teilbaum nur dann, wenn sein zusätzlicher Vorhersagenutzen seine zusätzliche Komplexität rechtfertigt.**

### Reduced Error Pruning

Beim **Reduced Error Pruning** wird ein Teilbaum probeweise entfernt. Auf einem separaten Validierungsdatensatz wird geprüft, ob sich die Vorhersage verschlechtert. Wird sie nicht schlechter, kann der Teilbaum abgeschnitten werden.

### Cost-Complexity Pruning

Beim für CART typischen **Cost-Complexity Pruning** werden Vorhersagefehler und Baumgröße gemeinsam bewertet. Vereinfacht gilt:

\[
R_\alpha(T) = R(T) + \alpha \cdot |T|
\]

Dabei bezeichnet

- \(R(T)\) den Fehler des Baums,
- \(|T|\) die Anzahl seiner Blätter,
- \(\alpha\) die Stärke der Komplexitätsstrafe.

Die Wirkung von \(\alpha\):

- kleines \(\alpha\): zusätzliche Blätter werden nur schwach bestraft; der Baum bleibt eher groß,
- großes \(\alpha\): zusätzliche Blätter werden stark bestraft; es wird stärker gepruned.

### Kurzes Beispiel

Ein Teilbaum benötigt acht zusätzliche Blätter und verbessert die Genauigkeit nur von 91,0 % auf 91,1 %. Der minimale Gewinn kann die zusätzliche Komplexität möglicherweise nicht rechtfertigen. Der Teilbaum wird dann durch ein Blatt ersetzt.

Wichtig: Auf den Trainingsdaten sieht ein großer Baum fast immer besonders gut aus. Die sinnvolle Pruning-Stärke sollte deshalb nicht allein anhand des Trainingsfehlers gewählt werden, sondern typischerweise über einen Validierungsdatensatz oder Cross-Validation.

---

## 6. Modellparameter und Hyperparameter

Diese Unterscheidung ordnet den gesamten Trainingsprozess.

### Modellparameter

Modellparameter werden während des Trainings automatisch aus den Daten gelernt.

Beispiele beim Decision Tree:

- „Verwende Feature 7 an diesem Knoten.“
- „Setze den Schwellenwert auf 4,3.“
- „Dieses Blatt sagt Klasse A voraus.“

### Hyperparameter

Hyperparameter steuern den Lernalgorithmus und werden nicht wie die Splits durch einen normalen Trainingslauf optimiert.

Beispiele:

- maximale Baumtiefe,
- minimale Blattgröße,
- Pruning-Stärke \(\alpha\),
- Anzahl der Bäume beim Bagging oder Random Forest,
- Anzahl der pro Split geprüften Features,
- Lernrate und Anzahl der Boosting-Schritte.

Ein Hyperparameter kann

1. ausdrücklich vom Programmierer gesetzt werden,
2. als Bibliotheks-Default übernommen werden oder
3. durch eine ausdrücklich eingerichtete Such- und Validierungsprozedur ausgewählt werden.

Ein Defaultwert ist **kein** Ergebnis von Hyperparameter-Tuning. Er ist lediglich eine vorgegebene Einstellung der verwendeten Bibliothek.

---

## 7. Training, Validierung und Test

Die drei Datenrollen beantworten unterschiedliche Fragen:

| Datenbereich | Zweck | Typische Frage |
|---|---|---|
| Training | Modellparameter lernen | Welche Splits und Blattvorhersagen passen zu den Daten? |
| Validierung beziehungsweise Cross-Validation | Konfigurationen bewerten und gegebenenfalls Hyperparameter auswählen | Welche Baumtiefe oder Pruning-Stärke generalisiert voraussichtlich am besten? |
| Test | einmalige, möglichst unverzerrte Schlussbewertung | Wie gut funktioniert der vollständig ausgewählte Prozess auf wirklich unbekannten Daten? |

Sobald Validierungsergebnisse verwendet werden, um Einstellungen auszuwählen, findet Hyperparameter-Tuning statt. Da man sich durch viele Auswahlentscheidungen indirekt an die Validierungsdaten anpassen kann, muss der Testdatensatz bis zum Schluss unangetastet bleiben.

Der typische Ablauf lautet:

1. Trainingsdaten und Testdaten trennen.
2. Nur innerhalb der Trainingsdaten verschiedene Hyperparameter per Cross-Validation vergleichen.
3. Die beste Konfiguration auswählen.
4. Mit dieser Konfiguration ein Modell auf allen verfügbaren Trainingsdaten neu trainieren.
5. Genau dieses finale Modell einmal auf dem unangetasteten Testdatensatz bewerten.

---

## 8. k-fold Cross-Validation: zunächst nur ein Bewertungsverfahren

Bei der **k-fold Cross-Validation** werden die verfügbaren Trainingsdaten in \(k\) Folds aufgeteilt. In jedem Durchlauf dienen \(k-1\) Folds zum Training und der verbleibende Fold zur Validierung. Nach \(k\) Durchläufen war jeder Fold genau einmal Validierungs-Fold. Die Einzelergebnisse werden üblicherweise gemittelt.

Bei 5-fold Cross-Validation entstehen beispielsweise fünf Trainings- und Validierungsdurchläufe.

Wichtig ist die begriffliche Trennung:

- **Cross-Validation mit einer festgelegten Konfiguration** schätzt deren erwartete Generalisierungsleistung.
- **Cross-Validation über mehrere Konfigurationen mit anschließender Auswahl** ist Bestandteil eines Hyperparameter-Tunings.

Wenn ein Modell mit `max_depth=5` in eine Cross-Validation gegeben wird, trainiert die CV mehrere Modelle mit genau `max_depth=5`. Sie beschließt nicht von selbst, zusätzlich die Tiefen 3, 7 oder 12 zu prüfen.

Cross-Validation ist daher zunächst ein **Bewertungsmechanismus**, nicht automatisch ein Suchmechanismus.

Wird dagegen ausdrücklich eine Suche über mehrere Tiefen eingerichtet, könnte eine vereinfachte Ergebnistabelle so aussehen:

| `max_depth` | Mittlere CV-Accuracy |
|---:|---:|
| 3 | 84 % |
| 5 | 88 % |
| 10 | 90 % |
| 20 | 87 % |

Unter diesen geprüften Kandidaten würde die Suche `max_depth=10` auswählen. Das bedeutet nicht, dass 10 universell optimal ist; es ist die beste der getesteten Einstellungen für diese Daten, Folds und Bewertungsmetrik.

---

## 9. Hyperparameter-Tuning: Was läuft automatisch, was muss angestoßen werden?

Ein normaler Aufruf von `.fit()` nimmt die eingestellten Hyperparameter oder deren Defaultwerte und lernt damit die Modellparameter. Das systematische Vergleichen verschiedener Hyperparameterwerte muss in der Regel ausdrücklich eingerichtet werden.

### Gesamtübersicht

| Vorgang | Art der Entscheidung | Automatisch bei einem normalen `.fit()`? | Was muss der Programmierer tun? |
|---|---|---:|---|
| Feature und Schwellenwert eines Tree-Splits bestimmen | Modellparameter lernen | Ja | Passendes Tree-Modell trainieren |
| Blattvorhersagen bestimmen | Modellparameter lernen | Ja | Passendes Tree-Modell trainieren |
| Bootstrap-Stichproben erzeugen | Bestandteil von Bagging | Ja, wenn ein Bagging-Verfahren entsprechend konfiguriert verwendet wird | Bagging-Modell wählen und seine Hyperparameter festlegen |
| Bäume beim Bagging trainieren und aggregieren | Bestandteil von Bagging | Ja | Bagging-Modell aufrufen |
| Zufällige Features pro Split auswählen | Bestandteil des Random Forest | Ja, gemäß dem eingestellten `max_features` | Random Forest verwenden und `max_features` setzen oder Default übernehmen |
| Boosting-Schritte nacheinander durchführen | Bestandteil des Boosting-Algorithmus | Ja | Boosting-Modell wählen und konfigurieren |
| Baum mit einem vorgegebenen \(\alpha\) prunen | Bestandteil des Trainingsalgorithmus | Ja, sofern das Modell diesen Mechanismus unterstützt und \(\alpha\) gesetzt ist | Pruning-Parameter vorgeben |
| Optimale `max_depth` suchen | Hyperparameter-Tuning | Nein | Suchraum und Suchverfahren definieren |
| Optimale `min_samples_leaf` suchen | Hyperparameter-Tuning | Nein | Suchraum und Suchverfahren definieren |
| Optimales `max_features` suchen | Hyperparameter-Tuning | Nein | Suchraum und Suchverfahren definieren |
| Optimale Anzahl der Bäume suchen | Hyperparameter-Tuning | Nein | Kandidaten oder Suchraum festlegen |
| Optimale Learning Rate suchen | Hyperparameter-Tuning | Nein | Suchraum und Suchverfahren definieren |
| Optimale Pruning-Stärke \(\alpha\) suchen | Hyperparameter-Tuning | Normalerweise nein | Kandidaten erzeugen und per Validierung vergleichen |
| Cross-Validation durchführen | Modellbewertung | Nein | CV ausdrücklich aufrufen oder in ein Suchverfahren integrieren |
| Mehrere Hyperparameterkombinationen testen | Hyperparameter-Suche | Nein | etwa Grid Search oder Random Search einrichten |
| Beste getestete Konfiguration auswählen | Teil des Suchverfahrens | Nicht bei normalem `.fit()`; ja innerhalb eines eingerichteten Suchverfahrens | Bewertungsmetrik und Suche konfigurieren |
| Finales Modell mit besten Hyperparametern neu trainieren | Refit | Nicht bei normalem `.fit()`; bei `GridSearchCV` standardmäßig ja | Suchobjekt mit `refit=True` verwenden oder manuell neu trainieren |
| Bibliotheks-Defaults verwenden | Vorgabe, kein Tuning | Ja | nichts; die Defaults werden unverändert übernommen |
| Early Stopping verwenden | datenabhängiges Stoppen innerhalb spezieller Verfahren | Nur wenn ausdrücklich unterstützt und aktiviert | Validierungslogik beziehungsweise Early Stopping konfigurieren |
| Interne CV-Verfahren wie `LassoCV` oder `LogisticRegressionCV` verwenden | im Modell eingebettete Hyperparametersuche | Ja, weil eine spezielle CV-Klasse gewählt wurde | bewusst diese spezielle Modellklasse und ihren Suchraum wählen |

Die wichtigste Regel lautet:

> **Ein normaler `.fit()`-Aufruf lernt Modellparameter. Hyperparameter werden nur dann gesucht, wenn der Programmierer eine zusätzliche Such- und Validierungsebene verwendet oder bewusst ein Verfahren mit eingebauter Suche auswählt.**

---

## 10. Grid Search, Random Search und die Zahl der Trainingsläufe

### Grid Search

Bei einer **Grid Search** werden alle vorgegebenen Kombinationen systematisch geprüft.

Beispiel:

```python
max_depth = [3, 5, 7, 10]
min_samples_leaf = [1, 5, 10]
```

Es entstehen

\[
4 \cdot 3 = 12
\]

Hyperparameterkombinationen. Mit 5-fold Cross-Validation werden daraus

\[
12 \cdot 5 = 60
\]

Trainingsläufe allein für den Vergleich. Wird anschließend mit den besten Hyperparametern auf allen Trainingsdaten neu trainiert, kommt noch ein finaler Refit hinzu.

Ein mögliches scikit-learn-Schema lautet:

```python
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier()

param_grid = {
    "max_depth": [3, 5, 7, 10],
    "min_samples_leaf": [1, 5, 10],
}

search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    cv=5,
)

search.fit(X_train, y_train)
```

Hier hat der Programmierer das Tuning angestoßen, indem er Modell, Suchraum und Zahl der Folds festgelegt hat. `GridSearchCV` übernimmt anschließend die Trainingsläufe, die Berechnung der Validierungswerte, die Auswahl der besten geprüften Kombination und standardmäßig den Refit auf den gesamten übergebenen Trainingsdaten.

### Random Search

Eine **Random Search** prüft nicht jede Kombination eines vollständigen Gitters, sondern zieht zufällige Konfigurationen aus einem vorgegebenen Suchraum. Das ist besonders hilfreich, wenn viele Hyperparameter oder viele mögliche Werte existieren.

Sowohl Grid Search als auch Random Search benötigen eine Bewertungsregel, beispielsweise Accuracy, F1-Score oder einen Regressionsfehler. „Beste Hyperparameter“ bedeutet immer: beste geprüfte Konfiguration **gemäß der gewählten Metrik und Validierungsprozedur**.

---

## 11. Beispiel: Pruning-Stärke mit Cross-Validation auswählen

Angenommen, für Cost-Complexity Pruning sollen vier Kandidaten getestet werden:

\[
\alpha \in \{0,\ 0{,}001,\ 0{,}01,\ 0{,}1\}
\]

Für jedes \(\alpha\) wird eine 5-fold Cross-Validation durchgeführt. Das ergibt

\[
4 \cdot 5 = 20
\]

Trainingsläufe. Für jedes \(\alpha\) entsteht ein mittlerer Validierungswert. Danach wird das bevorzugte \(\alpha\) ausgewählt und ein neuer Tree mit diesem Wert auf allen Trainingsdaten trainiert. Erst anschließend wird das finale Modell einmal am Testdatensatz geprüft.

Dieses Beispiel zeigt zwei Ebenen:

1. **Innerhalb eines Trainingslaufs:** Der Tree wird mit einem fest vorgegebenen \(\alpha\) aufgebaut beziehungsweise gepruned.
2. **Außerhalb der Trainingsläufe:** Cross-Validation und Suche entscheiden, welches \(\alpha\) verwendet werden soll.

---

## 12. Sonderfälle: automatische Entscheidungen innerhalb spezieller Verfahren

Die Regel „`.fit()` tuned keine Hyperparameter“ besitzt bewusst ausgewählte Ausnahmen.

### Early Stopping

Beim Boosting kann eine Validierungsleistung während des Trainings beobachtet werden. Verbessert sie sich über eine festgelegte Zahl von Schritten nicht mehr, wird das Hinzufügen weiterer Bäume gestoppt. Dadurch wird die effektive Anzahl der Boosting-Schritte datenabhängig bestimmt.

Dies geschieht jedoch nur, wenn der konkrete Algorithmus Early Stopping unterstützt und es entsprechend konfiguriert wurde.

### Modellklassen mit eingebauter Cross-Validation

Spezielle Klassen wie `LassoCV` oder `LogisticRegressionCV` führen eine interne Hyperparametersuche durch. Auch hier passiert die Suche nicht deshalb, weil jeder `.fit()`-Aufruf grundsätzlich Hyperparameter optimiert, sondern weil ausdrücklich eine Modellklasse gewählt wurde, deren Trainingsverfahren Cross-Validation enthält.

---

## 13. Die Konzepte als zusammenhängendes System

Die Verfahren lassen sich auf drei Ebenen ordnen:

### Ebene 1: Struktur eines einzelnen Baums

- Der Trainingsalgorithmus lernt Splits, Schwellenwerte und Blätter.
- Pre-Pruning begrenzt das Wachstum.
- Post-Pruning entfernt nachträglich wenig hilfreiche Teilbäume.

### Ebene 2: Kombination mehrerer Bäume

- Bagging trainiert Bäume unabhängig auf Bootstrap-Stichproben.
- Random Forest ergänzt zufällige Feature-Auswahl bei jedem Split.
- Boosting trainiert Bäume sequenziell zur schrittweisen Verbesserung.

### Ebene 3: Auswahl und Bewertung des Trainingsprozesses

- Cross-Validation bewertet eine Konfiguration robuster als eine einzelne Aufteilung.
- Grid Search oder Random Search erzeugt und vergleicht mehrere Konfigurationen.
- Ein Testdatensatz bewertet erst am Ende den vollständig ausgewählten Prozess.

Damit ergibt sich folgende gedankliche Kette:

\[
\text{Hyperparameter und Suchraum}
\rightarrow
\text{Cross-Validation der Trainingsmethode}
\rightarrow
\text{gewählte Konfiguration}
\rightarrow
\text{Refit auf allen Trainingsdaten}
\rightarrow
\text{einmaliger Test}
\]

Cross-Validation ist also kein Bestandteil des Decision Trees selbst. Sie liegt „außen herum“ und kann einen einzelnen Tree, ein Bagging-Verfahren, einen Random Forest oder ein Boosting-Verfahren bewerten und konfigurieren.

---

## 14. Kompakte Prüfungsübersicht

| Begriff | Kerngedanke | Typische Wirkung oder Aufgabe |
|---|---|---|
| Decision Tree | Daten rekursiv durch gelernte Splits aufteilen | flexibles, gut interpretierbares Grundmodell |
| Bagging | Modelle unabhängig auf Bootstrap-Stichproben trainieren und aggregieren | vor allem Varianz und Instabilität reduzieren |
| Feature Subsampling | pro Split nur eine zufällige Feature-Teilmenge betrachten | Bäume voneinander unterscheiden und Korrelation reduzieren |
| Random Forest | Bagging plus zufällige Feature-Auswahl | robustes Tree-Ensemble |
| Boosting | Modelle sequenziell trainieren; neue Modelle verbessern das bisherige Ensemble | häufig Bias reduzieren, teilweise auch Varianz |
| Pre-Pruning | Baumwachstum früh begrenzen | Überanpassung und Komplexität vorbeugen |
| Post-Pruning | bereits gewachsene Teilbäume nachträglich entfernen | Fehler und Komplexität gegeneinander abwägen |
| Cross-Validation | Konfiguration über mehrere Train-/Validierungsaufteilungen bewerten | Generalisierungsleistung schätzen |
| Grid Search | alle vorgegebenen Hyperparameterkombinationen testen | systematisches Hyperparameter-Tuning |
| Random Search | zufällige Konfigurationen aus einem Suchraum testen | effizientere Suche in großen Räumen |
| Refit | Modell mit gewählten Hyperparametern auf allen Trainingsdaten neu trainieren | finale Nutzung aller Trainingsinformationen |
| Testset | vollständig ausgewählten Prozess einmalig bewerten | möglichst unverzerrte Abschlussmessung |

---

## 15. Typische Prüfungsfallen

1. **„Random Forest und Bagging sind dasselbe.“**  
   Nicht ganz. Random Forest baut auf Bagging auf und ergänzt normalerweise zufällige Feature-Auswahl bei jedem Split.

2. **„Feature-Auswahl gehört zum klassischen Bagging.“**  
   Nein. Klassisches Bagging randomisiert die Beobachtungen. Feature Subsampling ist ein zusätzlicher Mechanismus.

3. **„Cross-Validation tuned automatisch Hyperparameter.“**  
   Nein. Mit einer festen Konfiguration bewertet Cross-Validation nur diese Konfiguration. Erst eine äußere Suchschleife mit Auswahl macht daraus Hyperparameter-Tuning.

4. **„Bibliotheks-Defaults sind automatisch optimiert.“**  
   Nein. Ein Default ist eine Vorgabe, kein datenabhängig gefundenes Optimum.

5. **„Ein normaler `.fit()`-Aufruf probiert verschiedene Baumtiefen aus.“**  
   Nein. Er verwendet die gesetzte oder voreingestellte Tiefe und lernt innerhalb dieser Vorgabe die Modellparameter.

6. **„Der Testdatensatz kann zur Auswahl der besten Hyperparameter verwendet werden.“**  
   Dann wäre er kein unabhängiger Testdatensatz mehr. Die Auswahl gehört in die Trainings- und Validierungsphase.

7. **„Post-Pruning sollte anhand des Trainingsfehlers entschieden werden.“**  
   Der Trainingsfehler bevorzugt meist komplexe Bäume. Pruning-Stärken sollten mithilfe separater Validierungsdaten oder Cross-Validation beurteilt werden.

8. **„Boosting-Bäume können wie Bagging-Bäume unabhängig trainiert werden.“**  
   Nein. Beim Boosting hängt jeder neue Schritt vom bisherigen Ensemble ab.

---

## 16. Abschluss-Merksätze

- **Ein Decision Tree lernt Splits und Blattvorhersagen; seine Hyperparameter begrenzen oder steuern diesen Lernprozess.**
- **Bagging randomisiert Datenzeilen und aggregiert unabhängige Modelle.**
- **Random Forest ergänzt beim Bagging die zufällige Auswahl von Features an den Splits.**
- **Boosting baut Modelle nacheinander auf, sodass spätere Modelle die bisherige Vorhersage verbessern.**
- **Pruning vereinfacht einen einzelnen Baum; Post-Pruning entfernt nachträglich wenig nützliche Teilbäume.**
- **Cross-Validation bewertet eine Konfiguration; eine Suchstrategie erzeugt und vergleicht mehrere Konfigurationen.**
- **`.fit()` lernt normalerweise Modellparameter, nicht automatisch die besten Hyperparameter.**
- **Training lernt, Validierung wählt, Testen beurteilt abschließend.**
