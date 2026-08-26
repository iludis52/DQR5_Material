# Prüfhandbuch — DQR5-KI-Prüfungsaufgaben

Verbindliche Grundlage für Erstellung und Prüfung. Wird zusammen mit dem
Metaprompt in den Chat gegeben.

**Themengebiete werden über ihren Namen bezeichnet, nie über eine Nummer.** Die
Namen sind identisch mit denen der Stichwortliste; wer dort einen ändert, ändert
ihn auch hier.

**Pflege:** Der Stolperstein-Katalog (§5) wächst pro Durchgang. Wer einen Fehler
findet, der noch nicht drinsteht, trägt ihn dort als Zeile nach — Thema, was
schiefgeht, was in der Aufgabe stehen muss. Alles andere ändert sich selten.

---

## 1 Rahmen

| Merkmal | Festlegung |
|---|---|
| Niveau | DQR 5, IHK „Berufsspezialist" — zwischen Facharbeiter und Bachelor |
| Prüfungsform | schriftlich, auf Papier, ohne Rechner |
| Zeit je Aufgabe | 20–30 Minuten |
| Punkte je Aufgabe | 20–30 |
| Teilaufgaben | 4–8, Niveau steigt monoton |
| Unterrichtskontext | VS Code, Python, scikit-learn, PyTorch, Gradio, SQL |

**Was aus der Papierprüfung folgt**

1. **Kein Code wird geschrieben.** Quelltext wird gelesen, analysiert, korrigiert
   oder lückengefüllt. Eine einzelne SQL-Anweisung zu formulieren ist zulässig.
2. **Keine Ausführungsumgebung.** Kein „Was gibt das Programm aus", keine
   Bibliotheksversionen, keine Laufzeitmessung.
3. **Rechnungen von Hand**, höchstens zwei Minuten. Glatte Differenzen,
   aufgehende Wurzeln, Divisoren aus {2, 4, 5, 10, 20, 25, 50, 100}.
4. **Skizzen freihändig** in unter drei Minuten: Netzskizzen, Komponenten- und
   Aktivitätsdiagramme, Achsenkreuze mit fünf bis acht Punkten.
5. **Rechen-Tabellen** höchstens acht Zeilen und fünf Spalten.

---

## 2 Scope-Matrix

**Stufen:** **K** kennen und benennen · **V** verstehen, erklären, abgrenzen,
deuten · **A** anwenden, rechnen, entwerfen, entscheiden · **—** nicht
prüfungsrelevant. A schließt V und K ein, V schließt K ein. Eine Teilaufgabe darf
die Stufe nicht überschreiten.

**Gewicht** steuert die Häufigkeit im Pool und erscheint nicht in
Prüflingsmaterial. **U** markiert unterdeckte Gebiete — Vorschlagsvorrat für das
Gespräch.

| Themengebiet | Stufe | Gewicht | Ausgeschlossen / Sonderregel |
|---|---|---|---|
| Grundbegriffe des maschinellen Lernens | A | hoch | Annotation von Daten |
| Lernparadigmen | A | hoch | Reinforcement Learning, Agenten |
| Datenrepräsentation & Datenstrukturen | V, Slicing A | mittel | Reshape, Dimensionserweiterung. Slicing max. 4×4 |
| Datenbeschaffung & -aufbereitung | A | hoch | *ergänzt:* Min-Max-Skalierung, One-Hot-Encoding |
| Deskriptive Statistik & Datenvisualisierung | A | mittel **U** | Korrelationskoeffizient nur deuten, nicht berechnen |
| Datensicherheit & Verschlüsselung | A | mittel **U** | Phishing; organisatorische Maßnahmen als eigener Gegenstand |
| Datenschutz (DSGVO) | A | hoch | Betroffenenrechte **U**. Pseudonymisierung ≠ Anonymisierung |
| Regressionsverfahren | A | hoch **U** | R² und p-Wert nur deuten. Interaktionen und höhere Terme nur V |
| Entscheidungs- & Klassifikationsbäume | A | hoch | **Gini-Index — auch nicht als Nebenbemerkung.** Entropie: Basis 2, max. 2 Klassen |
| Ensemble-Verfahren | A | mittel | Bagging↓Varianz, Boosting↓Bias — die Abgrenzung ist der Kern |
| Instanzbasiertes Lernen (k-NN) | A | mittel **U** | Korrelations-Distanz nur K. *ergänzt:* SVM als weiteres distanzbasiertes Verfahren |
| Clustering | A | hoch | Silhouettenplot-Theorie, Rand Index, Purity. Silhouettenwert nur deuten (V). *ergänzt:* DBSCAN |
| Dimensionsreduktion & Feature-Selektion | A | niedrig **U** | PCA-Ladungen nur deuten. Trägt keine Aufgabe allein — immer vernetzen |
| Modellbewertung & Evaluation | A | sehr hoch | *ergänzt:* Data Leakage, Fold-Varianz. Makro/Mikro nur K |
| Neuronale Netze – Grundlagen | A | hoch | *Logit* = gewichtete Summe vor der Ausgabe-Aktivierung |
| Training neuronaler Netze | A | hoch | Optimizer nur V, keine Update-Formeln. *ergänzt:* train/eval, `state_dict` |
| Netzarchitekturen | FNN A, Transformer K | niedrig | Attention, Attention Scores, Encoder-Decoder |
| Convolutional Neural Networks (CNN) | A | hoch | — |
| Overfitting & Robustheit von Modellen | A | hoch | Kovariaten- und Konzeptverschiebung; Adversarial Examples. Transfer Learning und Augmentation nur V **U** |
| Zeitreihenanalyse | A | mittel | Prophet nur Einsatzprofil (V). ACF/PACF nur K |
| Datenbanken & SQL | A | mittel **U** | 3NF max. eine Tabelle mit sechs Spalten |
| Programmiergrundlagen | V, **nur lesend** | niedrig | Zufallszahlen. Kein eigenständiges Aufgabenthema |
| Software-Entwicklung für KI-Systeme | A | hoch | Phasenzahl und -namen müssen vorgegeben werden. *ergänzt:* Aktivitäts- und Komponentendiagramm |
| Verantwortungsvolle KI: Bias & Erklärbarkeit | A | hoch | Bias nie rein technisch darstellen |
| Praktisches Projekt & überfachliche Kompetenzen | — | — | schriftlich nicht erhebbar; in der Stichwortliste als „nicht prüfungsrelevant" gekennzeichnet |

### Ausschlussliste in Kurzform

Reinforcement Learning und Agenten · Annotation von Daten · Phishing ·
organisatorische Datenschutzmaßnahmen als eigener Gegenstand · Gini-Index ·
Projektarbeit · komplexe Tensor-Manipulation · Attention und Encoder-Decoder ·
Kovariaten- und Konzeptverschiebung · Adversarial Examples ·
Silhouettenplot-Theorie, Rand Index, Purity · Zufallszahlen · vollständige
Implementierungen

### Abdeckung des Bestands

**Stark abgedeckt, Dublettengefahr:** Modellbewertung · CNN · Clustering ·
neuronale Netze (Grundlagen und Training) · Overfitting · Software-Entwicklung.

**Unterdeckt, bevorzugt vorschlagen:** deskriptive Statistik · Datensicherheit ·
DSGVO-Betroffenenrechte · Regressionsdiagnostik · k-NN · Dimensionsreduktion ·
Transfer Learning und Data Augmentation · 3NF, ERD und Schlüssel.

**Belegte Szenario-Domänen:** Medizin, Fahrradverleih, Energieversorgung,
Kundenbindung, Maschinenbau, Agrar, Fintech, E-Commerce, Großhandel,
Telekommunikation, Recycling.

---

## 3 Aufgabenschema

### Aufbau

Titel · Szenario · Datenbasis · Teilaufgaben · Anhang (wenn referenziert) ·
Lösungsskizze · Qualitätsreport. Ausgabe in drei Blöcken: **A** Aufgabe,
**B** Anhang, **C** Lösungsskizze und Report. A und B sind für sich
vollständig und enthalten keinen Lösungshinweis.

### Szenario

Ein durchgehender Kontext, 3–6 Sätze, fiktives Unternehmen mit sprechendem Namen.
Bekannte öffentliche Datensätze (Kaggle, UCI) als Datengrundlage sind erwünscht,
das Szenario bleibt erfunden. Keine realen Personen oder Unternehmen mit
zurechenbaren Aussagen.

### Datenbasis — vollständig heißt

- Jede Spalte mit **Name, Datentyp, Wertebereich oder Kategorienliste**.
- **Die Zielvariable ist als Target benannt**, wenn überwacht gelernt wird.
  *Schlecht:* „Features Höhe, Breite, Gewicht".
  *Gut:* „vier Spalten: Features Höhe, Breite, Gewicht und Target Werkstück".
- Besonderheiten: Anteil fehlender Werte, Klassenverteilung, Zeitreihenfrequenz,
  Bildgröße und Kanäle, Anzahl Datensätze.
- Alle Verfahrensparameter — siehe Stolperstein-Katalog §5.

### Teilaufgaben

Nummerierung `1.1`, `1.2`, … lückenlos, höchstens eine Ebene tiefer (`1.4.1`).
**Nie in Aufzählungspunkte abgleiten, sobald einmal nummeriert wurde.**

**Progression** — monoton steigend:

| Position | Anforderungsbereich | Operatoren |
|---|---|---|
| erste 1–2 | I Reproduktion | Benennen/Nennen, Beschreiben, Ordnen |
| Mitte | II Anwendung, Analyse | Berechnen, Bestimmen, Erläutern, Analysieren, Interpretieren, Überführen |
| letzte 1–2 | III Bewertung, Gestaltung | Beurteilen, Bewerten, Entscheiden, Entwerfen, Diskutieren, Vergleichen |

Alle drei Bereiche kommen vor. **III trägt mindestens 25 % der Punkte, I höchstens 25 %.**

**Vernetzung** — mindestens zwei Themengebiete. Bewährt: Datenbeschaffung →
Modellwahl · Metrik → fachliche Konsequenz · Architektur → Anforderungen ·
Vorverarbeitung → Leakage · Clustering → Weiterverwendung der Labels.

### Punkteschlüssel

| Leistung | Punkte |
|---|---|
| Ein Begriff, eine Zahl, eine Zuordnung | 1 |
| Zwei bis drei Nennungen ohne Begründung | 2 |
| Sachverhalt erklärt, 2–4 Sätze | 3 |
| Rechnung mit Rechenweg, ein Schritt | 2–3 |
| Rechnung mit Rechenweg, mehrere Schritte | 4–6 |
| Skizze oder Diagramm mit Beschriftung | 4–6 |
| Tabelle mit n Zellen ausfüllen | ca. n/2, aufgerundet |
| Vergleich über k Kriterien mit Begründung | 2 je Kriterium |
| Begründete Entscheidung mit Abwägung | 4–8 |

**Ein Punkt ≈ eine Minute.** Passt die Summe nicht zur Bearbeitungszeit, sind die
Punkte falsch verteilt — nicht die Zeit.

### Materialien

**Abbildung nur, wenn sie etwas trägt, das eine Tabelle nicht trägt.** Sinnvoll bei
Zeitreihenverlauf, Clusterstruktur, Dendrogramm, Loss-Kurven, Boxplot,
Komponenten- und Aktivitätsdiagrammen. Nicht sinnvoll für fünf Messwerte.
Spezifikationsformat siehe Metaprompt.

**Ausfülltabellen:** Kopf- und Zeilenbeschriftungen vollständig, Zellen leer,
Spaltenzahl in Kopf und Datenzeilen identisch.

**Quelltextfragmente:** so kurz wie möglich, syntaktisch korrekt, alle Namen vor
Gebrauch definiert. Lücken als `____`. Ein **absichtlicher** Fehler erfordert eine
Teilaufgabe, die ausdrücklich zum Suchen auffordert — ein unmarkierter Fehler in
einem als korrekt geltenden Fragment ist ein Blocker.

### Block C — Lösungsskizze und Qualitätsreport

**Pflicht ist die Lösungsskizze.** Sie ist knapp und besteht je Teilaufgabe aus:

- dem **ausgerechneten Ergebnis** mit allen Zwischenschritten, so wie es von
  Prüflingen erwartet wird — bei Rechenaufgaben also die vollständige Rechnung,
  nicht nur der Endwert;
- den **Teilpunkten**, deren Summe die Punktzahl der Teilaufgabe ergibt.

Sie ist kein Service für die Bewertung, sondern der Nachweis, dass die Aufgabe
lösbar ist. Wer die Lösung nicht ausrechnet, merkt nicht, wenn es keine gibt.
Rundungen werden angegeben.

**Optional, aber empfohlen** — der ausformulierte Erwartungshorizont mit
zulässigen Alternativen, häufigen Fehlern, Folgefehlerregelung und, bei
Entscheidungsaufgaben, dem, was eine Begründung tragfähig macht. Wird er
ausgegeben, gelten dafür die Soll-Punkte S9 und S12.

---

## 4 Prüfliste

**Muss** blockiert die Freigabe — ein einziges Rot verhindert sie, ohne Abwägung.
**Soll** ist ein Hinweis; drei oder mehr zusammen bedeuten „mit Auflagen".

### Muss

| | Prüfpunkt |
|---|---|
| M1 | Punktsumme 20–30. Summe als Zahl protokollieren. |
| M2 | Jede Teilaufgabe trägt genau eine Punktzahl. Keine an Szenario, Überschrift oder Anhang. |
| M3 | Nummerierung lückenlos, aufsteigend, ohne Doppelung, ohne Wechsel auf Aufzählungspunkte. |
| M4 | 4–8 Teilaufgaben auf oberster Ebene. |
| M5 | Alle Pflichtbestandteile da; Ausgabe in drei Blöcken; A und B ohne Lösungshinweis. |
| M6 | Genau ein führender Operator je Teilaufgabe, aus der Operatorenliste. |
| M7 | Operator überschreitet die Stufe des Themengebiets nicht. |
| M8 | Alle drei Anforderungsbereiche vorhanden; III ≥ 25 %, I ≤ 25 %. Verteilung protokollieren. |
| M9 | Anforderungsbereiche steigen monoton. |
| M10 | Kein Gegenstand von der Ausschlussliste — auch nicht in Nebensatz, Distraktor oder Block C. |
| M11 | Jeder Gegenstand steht in der Scope-Matrix. |
| M12 | Mindestens zwei Themengebiete verknüpft, beide benennen. |
| M13 | Keine Dublette: Überschneidung in höchstens einem Kernkonzept mit einer Bestandsaufgabe. |
| M14 | Keine Teilaufgabe verlangt eigenen Code. |
| M15 | Keine Ausführungsumgebung, kein Rechner, kein Netz vorausgesetzt. |
| M16 | Jede Rechnung von Hand in ≤ 2 Minuten. **Nachrechnen und protokollieren.** |
| M17 | Rechen-Tabellen ≤ 8 Zeilen, ≤ 5 Spalten. Zeichnungen freihändig ≤ 3 Minuten. |
| M18 | Punktsumme passt zur Zeit (±20 %). |
| M19 | Referenzen stimmen **in beide Richtungen**: keine ins Leere, keine verwaisten Anhangselemente. |
| M20 | Zahlenangaben im Text stimmen mit dem Anhang überein — der Text nennt genau so viele Modelle, Klassen, Optionen wie aufgeführt sind. |
| M21 | Jede Teilaufgabe ohne externe Information lösbar; alle Verfahrensparameter da (§5). |
| M22 | Datenbasis nennt je Spalte Typ und Wertebereich; Target ausdrücklich benannt. |
| M23 | Ausfülltabellen: Spaltenzahl in Kopf und Datenzeilen identisch. |
| M24 | Abbildungen vollständig spezifiziert, alle Felder gefüllt, keine Platzhalter. |
| M25 | Abbildung trägt Information, die eine Tabelle nicht trägt; in Graustufen lesbar; Ablesung eindeutig. |
| M26 | Quelltext syntaktisch korrekt, Namen vor Gebrauch definiert; absichtliche Fehler sind als solche adressiert; Lücken eindeutig lösbar. |
| M27 | Block C enthält je Teilaufgabe das ausgerechnete Ergebnis mit Zwischenschritten und die Teilpunkte. |
| M28 | **Jede Zahl in Block C unabhängig nachgerechnet und protokolliert.** |
| M29 | Teilpunkte summieren sich je Teilaufgabe exakt auf deren Punktzahl. |
| M30 | Erlaubt eine Teilaufgabe mehrere Lösungswege, ist mindestens einer vollständig durchgerechnet. |
| M31 | Keine Verletzung des Stolperstein-Katalogs (§5). |

### Soll

| | Prüfpunkt |
|---|---|
| S1 | Szenario realistisch, stimmig, ohne Jargon, der nicht Prüfgegenstand ist. |
| S2 | Ein Szenario trägt alle Teilaufgaben. |
| S3 | Themengebiete inhaltlich verbunden — das Ergebnis einer Teilaufgabe ist Voraussetzung der nächsten. |
| S4 | Mindestens eine Teilaufgabe verlangt eine echte fachliche Entscheidung mit Abwägung. |
| S5 | Verständnis und Abgrenzungsfähigkeit werden geprüft, nicht Auswendiggelerntes. |
| S6 | Jede Teilaufgabe ist beim ersten Lesen eindeutig. |
| S7 | Lösbar ohne Vorwissen über die Domäne jenseits des Alltags. |
| S8 | Mindestens eine Teilaufgabe ist mit Schlagworten allein nicht zu bestehen. |
| S9 | Zwei Lehrende kämen mit Block C unabhängig zur gleichen Punktzahl. *(nur bei ausformuliertem Erwartungshorizont)* |
| S10 | Niveau steigt gleichmäßig, kein Sprung nach der ersten Teilaufgabe. |
| S11 | Jede Spalte der Datenbasis wird von mindestens einer Teilaufgabe gebraucht — oder ihre Rolle als Ablenkung ist beabsichtigt und in Block C vermerkt. |
| S12 | Ausformulierter Erwartungshorizont vorhanden: zulässige Alternativen, häufige Fehler, Folgefehlerregelung, Begründungsmaßstab bei Entscheidungsaufgaben. |

---

## 5 Stolperstein-Katalog

Nur die Zeilen lesen, die zum Thema der Aufgabe gehören. Ein Verstoß ist ein
**Muss**-Fehler (M31).

### Für alle Themen

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| Die Aufgabe behauptet einen Befund in den Daten und fragt nach seinen Ursachen — „auffällig hohe Schwankung", „starkes Ungleichgewicht", „Ausreißer", „Bias" — aber die Datenbasis trägt ihn nicht | Der Befund muss aus der Datenbasis ableitbar sein: Verteilung, Gruppierung, Zeitbezug, Anteil der Extremwerte oder Klassenverhältnis benennen. Sonst bleibt den Prüflingen nur Raten |
| Ableseaufgabe an einer Abbildung ohne Grenzangabe | Toleranz oder Bereichsgrenze im Erwartungshorizont festlegen — sonst bewerten zwei Lehrende unterschiedlich |
| Spalten in der Datenbasis, die keine Teilaufgabe braucht | streichen, oder in Block C als beabsichtigte Ablenkung vermerken |

### SQL und Datenbanken

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| Join-Art unklar | INNER/LEFT/OUTER benannt oder eindeutig ableitbar |
| „Ein Datensatz je Entität" bei 1:n ohne Regel | Aggregations- oder Auswahlregel. „Alle Informationen beider Tabellen" und „ein Datensatz je Entität" schließen einander aus, sobald nicht aggregierbare Spalten vorliegen |
| NULL und 0 vermischt | `IS NULL`, nie `= NULL`; Unterschied fachlich getrennt |
| GROUP BY mit freien Spalten | nur gruppierte oder aggregierte Spalten in der Auswahl |

### Datenvorverarbeitung und Data Leakage

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| Skalierer vor dem Split gefittet | Reihenfolge: aufteilen → auf Train fitten → beide transformieren |
| Target-Leakage übersehen | zeitlicher Bezug der Merkmale erkennbar (z. B. „Ausgaben **nach** der Kampagne" bei Ziel „Reaktion auf die Kampagne") |
| Zeitliches Leakage | zeitbasierte statt zufälliger Aufteilung, sofern Zeitabhängigkeit besteht |
| Gruppen-Leakage | Duplikate oder wiederholte Entitäten nicht über Splitgrenzen |
| One-Hot mit k Spalten und Achsenabschnitt | k−1 Spalten, oder k ausdrücklich vorgegeben **und** in Block C aufgegriffen (Dummy-Falle) |
| Leakage unabsichtlich im Code | absichtlich → eigene Teilaufgabe; unabsichtlich → Blocker |

### Regression

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| Koeffizient ohne Einheit interpretierbar gemacht | Einheit; bei kategorialen Merkmalen die Referenzkategorie |
| R² als „Modellgüte schlechthin" | Anteil erklärter Varianz; auf Testdaten kann R² negativ werden |
| p-Wert als Wahrscheinlichkeit, dass H₀ stimmt | nur als Distraktor zulässig, nie als erwartete Lösung |
| Logistische Regression: Ausgabe unklar | Wahrscheinlichkeit, Logit oder Klasse festlegen |

### Entscheidungsbäume und Ensembles

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| Entropie ohne Basis oder Verteilung | Basis 2, Klassenverteilung, max. 2 Klassen, Werte so, dass log₂ aufgeht |
| Gini-Index taucht auf | **ausgeschlossen, auch als Vergleichsgröße** |
| Pruning-Parameter ohne Wirkrichtung | kleineres `max_depth`, größeres `min_samples_split` wirken beide gegen Overfitting |
| Bagging und Boosting vermischt | Bagging↓Varianz, Boosting↓Bias — Random Forest = Bagging **plus** Feature-Sampling |

### k-NN und Clustering

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| k fehlt oder Gleichstand unauflösbar | k angegeben; bei zwei Klassen ungerade oder Tie-Break-Regel |
| Distanz ohne Metrik oder Skalierungszustand | Metrik und Skalierungszustand; ganzzahlige Koordinaten |
| DBSCAN unvollständig | `eps`, `min_samples`, Metrik, Skalierung — und die Konvention, dass `min_samples` den Punkt selbst mitzählt |
| Distanz liegt auf der eps-Grenze | **alle paarweisen Distanzen nachrechnen**; keine darf näher als 10 % an eps liegen |
| k-Means ohne k | k angegeben oder seine Bestimmung ist Gegenstand |
| Dendrogramm mehrdeutig | Schnitthöhe eindeutig bestimmbar |
| Rand Index, Purity, Silhouettenplot-Theorie | ausgeschlossen; Silhouettenwert nur deuten |

### Metriken

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| MAE als Betrag der Summe | Summe der Beträge geteilt durch n — auch dann falsch, wenn das Ergebnis zufällig stimmt |
| Precision/Recall ohne positive Klasse | Definition der positiven Klasse |
| Accuracy bei Ungleichgewicht ungeprüft | Anteil der Mehrheitsklasse angeben oder ableitbar machen |
| Mehrklassen ohne Mittelungsart | makro oder mikro benennen |

### Modellbewertung

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| „Lernkurve" für ein Diagramm mit einem Hyperparameter auf der x-Achse | **Lernkurve** = Trainingsmengengröße auf x. **Validierungs- oder Komplexitätskurve** = Hyperparameter auf x (z. B. `max_depth`). Titel, Bildunterschrift und Aufgabentext müssen denselben Begriff verwenden |
| Validierungs- und Testdaten synonym gebraucht | Validierungsdaten steuern die Modellwahl, Testdaten messen einmalig am Ende |
| Fold-Varianz ohne Datengrundlage (siehe „Für alle Themen") | Struktur oder Verteilung angeben, aus der die Schwankung folgen kann |

### Zeitreihen

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| s passt nicht zur Frequenz | täglich mit Wochenzyklus s = 7, stündlich mit Tageszyklus s = 24; **Text und Parameterliste dürfen sich nicht widersprechen** |
| Windowing unklar | Fenstergröße, Horizont, Zielwert; bei n Werten, Fenster w, Horizont 1 → n − w Beispiele |
| Zufälliger Split bei Zeitabhängigkeit | zeitbasierte Aufteilung, sonst ausdrückliche Begründung |

### Neuronale Netze und CNN

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| Shape-Rechnung auf freier Wahl | keine benötigte Größe ist eine Lücke, die die Prüflinge selbst wählen |
| Parameterzahl ohne Bias-Konvention | ausdrücklich sagen, ob Bias mitzählt. Konvolution `k_h·k_w·C_in·C_out (+C_out)`, dichte Schicht `n_in·n_out (+n_out)` |
| Rechnung widerlegt die Pointe | **die Pointe nachrechnen** — sie muss aus den Zahlen folgen |
| Ausgabegröße unbestimmt | `floor((n + 2p − k)/s) + 1`, alle Größen gegeben |
| Aktivierung passt nicht | ReLU in Hidden, Softmax mehrklassig, Sigmoid binär, linear bei Regression |
| Loss passt nicht zur Ausgabe | CrossEntropy klassifizierend (erwartet Logits, keine Softmax-Ausgabe), MSE/L1 regressiv |

### Bias, DSGVO, SDLC

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| Bias rein technisch dargestellt | Ursachen in Daten, Labels, Zieldefinition, Auswahlprozess, gesellschaftlichem Kontext |
| Pseudonymisierung = Anonymisierung | pseudonymisierte Daten bleiben personenbezogen |
| TOM undifferenziert | technische und organisatorische Maßnahmen trennen |
| „Die sechs SDLC-Phasen" ohne Nennung | Anzahl **und** Namen der Phasen vorgeben |
| Komponentendiagramm ohne Kantenbeschriftung | geforderte Komponenten aufzählen, Beschriftung der Verbindungen verlangen |
