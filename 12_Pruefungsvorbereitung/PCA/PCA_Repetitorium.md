# PCA – Hauptkomponentenanalyse: kompaktes Repetitorium

## 1. Idee und theoretischer Hintergrund

**Principal Component Analysis (PCA)** ist ein unüberwachtes, lineares Verfahren zur Dimensionsreduktion. Es bildet aus mehreren numerischen Ausgangsmerkmalen neue Merkmale, die **Hauptkomponenten**. Dazu sucht PCA Richtungen, entlang derer die Eingabedaten möglichst stark streuen. Die Zielvariable eines späteren Vorhersagemodells geht in diese Suche nicht ein.

**Das Bild für zwei Merkmale:** Zeichnet man alle Beobachtungen als Punkte, entsteht häufig eine längliche Punktwolke. Die erste Hauptkomponente (HK1) verläuft entlang ihrer längsten Richtung – anschaulich entlang der langen Achse einer gedachten Ellipse durch die Punktwolke. Die zweite Komponente (HK2) steht senkrecht darauf und erfasst die verbleibende Streuung in dieser Richtung. Bei drei oder mehr Merkmalen gilt dieselbe Idee in einem höherdimensionalen Merkmalsraum; die Richtungen lassen sich dann nur schwerer zeichnen. Bei einer ungefähr kreisförmigen Punktwolke gibt es keine eindeutig ausgezeichnete „lange Achse“.

PCA betrachtet die Daten **um ihren Mittelpunkt**: Die Merkmale werden vor der Bestimmung der Richtungen zentriert. Jede Hauptkomponente ist eine *gewichtete Linearkombination* dieser zentrierten Merkmale. Ihre Gewichte beschreiben die Richtung im ursprünglichen Merkmalsraum; ein Datenpunkt erhält seine neue Koordinate durch Projektion auf diese Richtung. Bei standardisierten Eingaben kann man sich HK1 schematisch als `0,7 · z₁ + 0,7 · z₂` vorstellen: Sie verbindet zwei Merkmale, statt eines von ihnen auszuwählen. Die tatsächlichen Gewichte lernt PCA aus den Trainingsdaten.

Die Richtungen der Hauptkomponenten stehen **paarweise senkrecht (orthogonal)** aufeinander. Die daraus berechneten Komponentenwerte sind für die Daten, an denen PCA angepasst wurde, **unkorreliert**. HK1 erklärt die größtmögliche Varianz einer Richtung, HK2 die größtmögliche *zusätzliche* Varianz unter der Bedingung, senkrecht auf HK1 zu stehen; entsprechend folgen die weiteren Komponenten. Die maximale Anzahl unterscheidbarer Komponenten ist durch die Zahl der Merkmale und der Trainingsbeobachtungen begrenzt. PCA findet lineare Richtungen, keine beliebigen gekrümmten Strukturen.

## 2. Erklärte Varianz und Wahl der Komponentenzahl

Die **erklärte Varianz** einer Komponente bezeichnet ihren Anteil an der gesamten Varianz der für die PCA verwendeten Eingabedaten. Die Anteile der einzelnen Komponenten sind nach Größe absteigend geordnet. Ihre Summe bis einschließlich HK *k* ist die **kumulierte erklärte Varianz**. Beispiel: Erklären HK1, HK2 und HK3 jeweils 50 %, 30 % und 12 %, erklären die ersten zwei zusammen 80 % und die ersten drei zusammen 92 %. Die Prozente beziehen sich auf die Streuung der Eingabedaten **nach der gewählten Vorverarbeitung**, nicht auf die Güte eines Vorhersagemodells.

Ein **Scree-Plot** trägt typischerweise die erklärte Varianz *je Komponente* gegen die Komponentennummer auf. Man sucht etwa einen Knick, nach dem weitere Komponenten nur noch wenig zusätzliche Varianz beitragen. Ergänzend zeigt eine **kumulative Varianzkurve**, ab welcher Komponentenzahl ein gewünschter Anteil erreicht wird. Ein Schwellenwert wie 90 % ist eine mögliche Entscheidungshilfe, aber keine allgemeingültige Qualitätsgarantie.

**Entscheidend:** PCA maximiert die Varianz der Eingaben und kennt die Zielvariable nicht. Eine Richtung mit geringer Varianz kann für eine Klassifikation oder Regression sehr wichtig sein. Daher gilt **hohe erklärte Varianz ≠ hohe Vorhersagegüte**. Für Vorhersageaufgaben beurteilt man die Komponentenzahl zusätzlich anhand einer geeigneten Modellmetrik auf bisher ungesehenen Daten, beispielsweise per Kreuzvalidierung. Die passende Metrik hängt von der Aufgabe ab; Accuracy allein ist insbesondere bei ungleichen Klassenhäufigkeiten oft wenig aussagekräftig.

Die Reduktion auf weniger Komponenten verwirft Information. Je kleiner die gewählte Zahl, desto größer kann dieser **Informationsverlust** sein. Beibehaltung aller Komponenten ist im Wesentlichen ein Wechsel der Koordinaten; erst das Weglassen von Komponenten reduziert die Dimension.

## 3. Wann PCA sinnvoll ist – und welche Grenzen sie hat

**Typische Anwendungen:**

- **Verdichten vieler numerischer Merkmale**, besonders wenn sie stark zusammenhängen und sich ähnliche Information in mehreren Spalten wiederholt.
- **Vorbereitung eines nachgelagerten Modells**, wenn eine kompaktere Darstellung die Rechenarbeit oder das Verhalten des Modells im konkreten Fall verbessert. Ob das gelingt, muss man prüfen; PCA ist kein automatisch vorteilhafter Standardschritt.
- **Visualisierung** in zwei oder drei Komponenten, um eine erste Ansicht höherdimensionaler Daten zu gewinnen. Die Grafik zeigt nur den erhaltenen Ausschnitt der Streuung; scheinbare Trennung oder Überlappung ist vorsichtig zu interpretieren.

**Grenzen und Abwägungen:**

- **Interpretierbarkeit:** Einzelne Komponenten mischen häufig viele Ausgangsmerkmale. Ihre Gewichte lassen sich ansehen, aber die Bedeutung der neuen Achsen ist meist weniger unmittelbar als die der ursprünglichen Merkmale. Insbesondere fachlich zu erklärende Einzelvorhersagen werden schwieriger nachzuvollziehen.
- **Zielbezug:** Hohe Eingabevarianz kann für die Vorhersage irrelevant sein; PCA ersetzt weder die Modellbewertung noch eine fachlich begründete Merkmalswahl.
- **Ausreißer und Struktur:** Einzelne extreme Beobachtungen können die Hauptachsen stark beeinflussen. PCA bildet lineare Zusammenhänge ab und erhält bei Reduktion nicht zwangsläufig alle Abstände, Gruppen oder seltenen Muster.
- **Verfahren danach:** Eine geringe Zahl von Komponenten kann ausreichen, muss aber nicht. Modelle mit und ohne PCA unter denselben fairen Bewertungsbedingungen vergleichen.

## 4. Praktische Umsetzung: Vorverarbeitung und Training

1. **Geeignete Eingaben festlegen.** PCA setzt numerische Merkmale voraus. Fehlende Werte müssen geeignet behandelt, kategoriale Merkmale gegebenenfalls passend kodiert werden. Die Zielvariable gehört nicht zu den PCA-Eingaben.
2. **Daten für die Bewertung trennen.** Eine unabhängige Testmenge, sofern vorgesehen, vor dem Lernen der Vorverarbeitung zurücklegen. Auch innerhalb einer Kreuzvalidierung muss der jeweilige Validierungsfold unbekannt bleiben, solange die Verarbeitung angepasst wird.
3. **Merkmale skalieren.** PCA reagiert auf unterschiedliche Größenordnungen, weil sie Richtungen mit großer Varianz bevorzugt. `StandardScaler` ist häufig eine gute Wahl: Er zieht je Merkmal den Trainingsmittelwert ab und teilt durch die Trainingsstandardabweichung. Dadurch wird jedes Merkmal auf vergleichbare Streuung gebracht. Das ist **keine zwingende mathematische Voraussetzung**: Liegen Merkmale bereits auf sinnvoll vergleichbaren Skalen, kann eine andere Entscheidung fachlich gerechtfertigt sein. Standardisierung ist zudem empfindlich gegenüber Ausreißern.
4. **PCA am Training anpassen und transformieren.** PCA ermittelt Mittelwerte, Richtungen und Varianzanteile ausschließlich aus den Trainingsdaten. Das Ergebnis sind neue Koordinaten der Trainingsbeobachtungen auf den Komponenten. Validierungs-, Test- und spätere neue Daten erhalten **dieselbe gelernte Skalierung und dieselbe gelernte Projektion**; auf ihnen wird PCA nicht erneut angepasst.
5. **Komponentenzahl festlegen und Ergebnis prüfen.** Scree-Plot und kumulierte Varianz beschreiben den Informationsanteil. Bei einer Vorhersageaufgabe bestimmt zusätzlich die Leistung des *gesamten* Ablaufs, ob die Reduktion sinnvoll ist. Wird die Komponentenzahl anhand von Validierungsergebnissen gewählt, ist sie eine Modellentscheidung, die innerhalb des dafür vorgesehenen Trainings- und Auswahlverfahrens getroffen werden muss.

**Wichtig bei k-facher Kreuzvalidierung:** In *jedem* Durchgang werden Skalierer, PCA und nachgelagertes Modell **neu und nur auf dem jeweiligen Trainingsfold angepasst**. Der zugehörige Validierungsfold wird lediglich mit den dort gelernten Schritten transformiert und anschließend bewertet. Wer Skalierer oder PCA vor der Aufteilung auf den gesamten Datensatz anpasst, lässt Information aus den Validierungsfolds in das Training einfließen (**Data Leakage**) und erhält möglicherweise zu optimistische Ergebnisse. Eine Pipeline hält die Reihenfolge und die Datengrenzen konsistent.

Schematisch: `StandardScaler → PCA → Modell` – diese *gesamte Pipeline* wird kreuzvalidiert. Nach Auswahl und Bewertung kann die fertige Pipeline für den späteren Einsatz auf den dafür vorgesehenen Trainingsdaten erneut angepasst werden; eine zurückgelegte Testmenge dient der abschließenden, unabhängigen Prüfung.

## 5. Begriffe, die man sicher unterscheiden sollte

| Begriff | Präzise Bedeutung |
| --- | --- |
| Ausgangsmerkmal | Ursprünglich erhobene Eingabevariable; PCA wählt nicht einfach einzelne davon aus. |
| Hauptkomponente | Neue Achse beziehungsweise die Koordinate eines Datenpunkts auf dieser Achse; im jeweiligen Zusammenhang „Richtung“ und „Komponentenwert“ auseinanderhalten. |
| Komponenten-Gewichte | Zahlen, die festlegen, wie die ursprünglichen Merkmale zur Richtung einer Komponente beitragen. |
| Erklärte Varianz | Anteil der Eingabevarianz, den eine einzelne Komponente erfasst. |
| Kumulierte erklärte Varianz | Summe der erklärten Anteile der ersten *k* Komponenten. |
| Modellgüte | Anhand geeigneter Daten gemessene Leistung für die eigentliche Aufgabe; folgt nicht unmittelbar aus der erklärten Varianz. |

**Merksatz:** PCA sucht in den Eingabedaten neue, zueinander senkrechte Achsen mit möglichst viel Streuung. Wie viele Achsen man behält und ob sie einem Vorhersagemodell helfen, entscheidet man anhand des Anwendungsziels und einer sauberen Bewertung ohne Data Leakage.
