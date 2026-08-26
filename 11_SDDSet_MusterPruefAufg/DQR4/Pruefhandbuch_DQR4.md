# Prüfhandbuch — DQR4-KI-Prüfungsaufgaben

Verbindliche Grundlage für Erstellung und Prüfung von Aufgaben zur
IHK-Zusatzqualifikation „Künstliche Intelligenz und maschinelles Lernen" für
Auszubildende aller Fachrichtungen. Wird zusammen mit dem Metaprompt in den Chat
gegeben.

**Themengebiete werden über ihren Namen bezeichnet, nie über eine Nummer.** Die
Namen sind identisch mit denen der Stichwortliste; wer dort einen ändert, ändert
ihn auch hier.

**Modulbuchstaben sind mehrdeutig.** Die Prüfung vergibt sie in didaktischer
Reihenfolge, der Rahmenlehrplan in seiner eigenen. Prüfungs-Modul B ist
RLP-Modul C, Prüfungs-Modul C ist RLP-Modul D, Prüfungs-Modul D ist RLP-Modul B.
**In diesem Handbuch und in allen erzeugten Aufgaben gilt ausschließlich die
Prüfungszählung.**

**Pflege:** Der Stolperstein-Katalog (§5) wächst pro Durchgang. Wer einen Fehler
findet, der noch nicht drinsteht, trägt ihn dort als Zeile nach — Thema, was
schiefgeht, was in der Aufgabe stehen muss. Alles andere ändert sich selten.

---

## 1 Rahmen

| Merkmal | Festlegung |
|---|---|
| Niveau | DQR 4, Zusatzqualifikation für Auszubildende aller Fachrichtungen |
| Prüfungsform | schriftlich, auf Papier; nicht programmierbarer, netzunabhängiger Taschenrechner zugelassen |
| Gesamtprüfung | 60 Minuten, 100 Punkte, vier Module |
| Modulkorridore | A Grundbegriffe 18–22 · B Umgang mit Daten 15–20 · C Datenanalyse & ML 45–52 · D Chancen & Ethik 15–18 |
| Teilaufgaben gesamt | 15–19, Regelspanne 3–8 Punkte, höchstens **eine** Aufgabe über 10 |
| Einzelblock | ein Modul, 15–50 Punkte, 3–7 Teilaufgaben |
| Unterrichtskontext | Python ausschließlich mit vorgegebenem Code, Teachable Machine, Tabellenkalkulation — **nichts davon ist Prüfgegenstand** |

**Was aus der Papierprüfung folgt**

1. **Kein Quelltext — weder geschrieben noch gelesen.** In keiner der vier
   Referenzprüfungen kommt Programmcode vor. Das ist keine Auslassung, sondern
   eine Niveauentscheidung: Der Rahmenlehrplan setzt ausdrücklich keine
   Programmierkenntnisse voraus.
2. **Keine Ausführungsumgebung und keine Werkzeugbedienung.** Kein „Was gibt das
   Programm aus", keine Notebook-Schritte, keine Bibliotheksnamen als
   Prüfgegenstand.
3. **Rechnungen in höchstens zwei Minuten.** Der Taschenrechner ist zugelassen,
   glatte Zahlen bleiben trotzdem Soll (S12): Sie machen den Rechenweg prüfbar
   und Folgefehler erkennbar.
4. **Zeichnungen freihändig in unter vier Minuten:** Entscheidungsbaum mit zwei
   bis vier Verzweigungen, Achsenkreuz mit fünf bis zehn Punkten, Säulendiagramm
   mit zwei bis drei Säulen, Regressionsgerade in ein vorhandenes Diagramm.
5. **Rechen- und Ausfülltabellen** höchstens acht Zeilen und fünf Spalten.
6. **Alle benötigten Formeln werden abgedruckt.** Eine Formelsammlung ist nicht
   zugelassen; Accuracy, Precision und Recall stehen neben der Anlage.
7. **Ein Punkt ≈ 36 Sekunden.** 100 Punkte in 60 Minuten. Der DQR-5-Merksatz
   „ein Punkt ≈ eine Minute" gilt hier **nicht** — er würde Aufgaben erzeugen,
   die dreifach zu lang sind.

---

## 2 Scope-Matrix

**Stufen:** **K** kennen und benennen · **V** verstehen, erklären, abgrenzen,
deuten · **A** anwenden, rechnen, modellieren, entscheiden · **—** nicht
prüfungsrelevant. A schließt V und K ein, V schließt K ein. Eine Teilaufgabe darf
die Stufe nicht überschreiten.

**Gewicht** steuert die Häufigkeit im Pool und erscheint nicht in
Prüflingsmaterial. **U** markiert unterdeckte Gebiete — Vorschlagsvorrat für das
Gespräch.

| Themengebiet | Stufe | Gewicht | Ausgeschlossen / Sonderregel |
|---|---|---|---|
| Grundbegriffe des maschinellen Lernens | A | hoch | *ergänzt:* Prozessschritte des maschinellen Lernens als Kette (nur benennen, K) |
| Lernparadigmen | A | sehr hoch | Reinforcement Learning nur K und V: Prinzip beschreiben, Beispiel benennen — keine Rechnung, keine Agentenarchitektur |
| Mathematische Grundlagen | A | mittel **U** | Trägt keine Aufgabe allein — immer mit Regressionsverfahren oder Datenvisualisierung vernetzen |
| Datenrepräsentation & Datenaufbereitung | V, Kennwerte A | mittel **U** | Join-Arten nur V: Inner und Outer unterscheiden, nicht ausführen. Kein SQL |
| Deskriptive Statistik & Datenvisualisierung | A | sehr hoch | Korrelationskoeffizient nur deuten (V), nicht berechnen. Median nur bei ungerader Anzahl der bereinigten Werte |
| Datensicherheit | A | hoch | Phishing ist zulässig und geprüft (anders als auf DQR 5) |
| Datenschutz (DSGVO) | A | hoch | Betroffenenrechte **U**. Pseudonymisierung ≠ Anonymisierung |
| Regressionsverfahren | A | sehr hoch | **Berechnung der Regressionslinie über die Varianz ausgeschlossen.** Determinationskoeffizient nur deuten (V). Steigung wird abgelesen, nicht ausgeglichen |
| Entscheidungs- & Klassifikationsbäume | A | sehr hoch | **Gini-Index — auch nicht als Nebenbemerkung.** Entropie: Basis 2, max. 2 Klassen, Werte so, dass log₂ aufgeht |
| Modellbewertung & Evaluation | A | sehr hoch | *ergänzt:* **MSE nur deuten und interpretieren (V), nie berechnen.** Dasselbe gilt für RMSE. Positive Klasse stets definieren. Trainings- und Testdatenaufteilung **U** |
| Neuronale Netze | V, Schemazuordnung A | hoch **U** | Gewichtematrix und Matrixmultiplikation nur V. **Keine Parameterzahl-Rechnungen, keine Shape-Rechnungen.** Training nur als Ablaufbeschreibung |
| Verantwortungsvolle KI: Bias & Erklärbarkeit | A | hoch **U** | Bias nie rein technisch darstellen |

### Ausschlussliste in Kurzform

**Aus der Stichwortliste gestrichen:** Gini-Index · Berechnung der Regressionslinie
über die Varianz · praktisches Projekt, Teachable Machine und jede
Werkzeugbedienung.

**Zusätzlich ausgeschlossen:** Berechnung von MSE und RMSE (nur deuten) ·
Wahrscheinlichkeitsrechnung aus Häufigkeiten · Programmcode jeder Art ·
Parameterzahl- und Shape-Rechnungen bei neuronalen Netzen · Berechnung des
Korrelationskoeffizienten.

**Gehört zum DQR-5-Bestand und ist hier ausgeschlossen** — diese Zeile ist der
häufigste Fehler beim Generieren, weil das Modell die DQR-5-Themen kennt:
Ensemble-Verfahren, Random Forest, Bagging, Boosting · k-NN und Distanzmaße ·
SVM · kMeans, DBSCAN, Dendrogramme, Silhouettenwerte · PCA, t-SNE,
Feature-Selektion, Regularisierung · CNN, Filterkerne, Pooling, rezeptives Feld ·
Transformer und Attention · Zeitreihenanalyse, SARIMA, Prophet, Windowing ·
Datenbanken, SQL, ERD, Normalformen · Programmiergrundlagen ·
Software-Entwicklung für KI-Systeme, ISO 25010, Architekturdiagramme ·
logistische Regression, p-Wert, Hypothesentest · Data Leakage ·
Bias-Varianz-Trade-off · Early Stopping, Dropout, Batch Normalisierung, Data
Augmentation, Transfer Learning · Optimizer, Lernrate, Batchgröße, Epochen.

Der Test ist mechanisch: **Steht der Begriff in der DQR-4-Stichwortliste? Wenn
nicht, ist er ausgeschlossen** — unabhängig davon, wie naheliegend er fachlich
wirkt.

### Abdeckung des Bestands

Grundlage sind die vier Referenzprüfungen Sommer 2023 bis Sommer 2026.

**Stark abgedeckt, Dublettengefahr:** Entscheidungs- und Klassifikationsbäume
(alle vier Jahrgänge) · Regression aus dem Streudiagramm · Confusion-Matrix und
Metriken · Datensicherheit · deskriptive Kennwerte · Lernparadigmen.

**Unterdeckt, bevorzugt vorschlagen:** mathematische Grundlagen (nie eigenständig
geprüft) · Datenaufbereitung und Join-Arten (nie geprüft) · Trainings- und
Testdatenaufteilung (zuletzt 2023) · Entropie und Informationsgewinn (zuletzt
2023) · neuronale Netze (zwei von vier Jahrgängen) · Erklärbarkeit (zuletzt
2025) · DSGVO-Betroffenenrechte.

**Belegte Szenario-Domänen:** Medizintechnik (2023, 2024), Energieversorgung
(2025), Lebensmittel-Lieferdienst (2026).

**Bekannte Schieflage des Bestands:** Der reproduktive Anteil ist von 23 Punkten
(2024) auf 44–46 Punkte (2025, 2026) gestiegen, und der Jahrgang 2026 enthält
keine einzige Aufgabe der Stufe Bewerten. Beides ist **nicht** fortzuschreiben;
M8 verlangt ausdrücklich je eine Aufgabe der Stufen Bewerten und Gestalten.

---

## 3 Aufgabenschema

### Aufbau

Titel · Szenario · Datenbasis · Teilaufgaben · Anlagen (wenn referenziert) ·
Lösungsskizze · Qualitätsreport. Ausgabe in drei Blöcken: **A** Aufgabe,
**B** Anlagen, **C** Lösungsskizze und Report. A und B sind für sich vollständig
und enthalten keinen Lösungshinweis.

Im Modus „vollständige Prüfung" tritt ein **Deckblatt** hinzu: Prüfungszeit,
Bewertungseinheiten, Bewertungsraster mit den vier Modulen und ihren Punktzahlen,
die Standardhinweise nach M33.

### Szenario

Ein durchgehender Kontext, 3–6 Sätze, fiktives Unternehmen mit sprechendem Namen.
Zu Beginn jedes Moduls wird er um zwei bis drei Sätze fortgeschrieben. Keine
realen Personen oder Unternehmen mit zurechenbaren Aussagen.

**Die Domäne muss kaufmännische und gewerblich-technische Auszubildende
gleichermaßen erreichen.** Kein Vorwissen jenseits des Alltags: Ein Lieferdienst,
ein Energieversorger oder ein Fahrradhersteller funktionieren, eine
Halbleiterfertigung nicht.

### Datenbasis — vollständig heißt

- Jede Spalte mit **Name, Datentyp, Wertebereich oder Kategorienliste**.
- **Die Klassen- oder Zielspalte ist ausdrücklich benannt**, wenn überwacht
  gelernt wird.
  *Schlecht:* „Merkmale Entfernung, Anzahl, Status".
  *Gut:* „drei Spalten: Merkmale Entfernung und Anzahl, Klassenspalte Status mit
  den Werten pünktlich und verspätet".
- Besonderheiten: Anzahl der Datensätze, Klassenverteilung, Anteil fehlender
  Werte, Lage der Ausreißer.
- Alle Verfahrensparameter — siehe Stolperstein-Katalog §5.

### Teilaufgaben

Im Modus „vollständige Prüfung" Aufgaben-IDs im Schema `A1` bis `D3`, je Modul
lückenlos aufsteigend. Im Modus „Einzelblock" `1.1`, `1.2`, … lückenlos,
höchstens eine Ebene tiefer (`1.4.1`). **Nie in Aufzählungspunkte abgleiten,
sobald einmal nummeriert wurde.**

**Progression** — innerhalb jedes Moduls monoton steigend:

| Position | Anforderungsstufe | Operatoren |
|---|---|---|
| erste 1–2 | Reproduzieren | Benennen, Beschreiben, Darstellen, Ordnen |
| Mitte | Analysieren, Anwenden | Analysieren, Interpretieren, Erklären, Erläutern, Bestimmen, Berechnen, Modellieren, Planen |
| letzte 1–2 | Bewerten, Gestalten | Auswerten, Vergleichen, Beurteilen, Entscheiden |

**Verteilung in der vollständigen Prüfung** — Korridore aus der Einzelzuordnung
aller 65 Teilaufgaben der vier Referenzprüfungen:

| Anforderungsstufe | Zielkorridor | Bestand 2023 / 2024 / 2025 / 2026 |
|---|---|---|
| Reproduzieren | 30–40 | 25 / 23 / 46 / 44 |
| Analysieren | 15–25 | 28 / 18 / 19 / 16 |
| Anwenden | 25–35 | 27 / 38 / 18 / 34 |
| Bewerten | 10–15 | 20 / 15 / 12 / **0** |
| Gestalten | 5–10 | 0 / 6 / 5 / 6 |

Im Modus „Einzelblock" gelten die Korridore nicht. Dort genügt: mindestens zwei
Anforderungsstufen, Beginn auf Reproduzieren oder Analysieren, Abschluss auf
einer höheren Stufe.

**Skizzieren ist hier kein reproduktiver Operator.** Für einen aus Daten
konstruierten Entscheidungsbaum lautet der Operator **Modellieren** („gemäß einer
Problemanalyse ein informatisches Modell erstellen"). Wer „Skizzieren" verwendet,
verbucht die anspruchsvollste Aufgabe des Satzes auf der niedrigsten Stufe.

**Vernetzung** — erwünscht, aber im Einzelblock keine Pflicht. In der
vollständigen Prüfung sind mindestens sechs Themengebiete zu berühren. Bewährte
Verkettungen: Datenaufbereitung → Modellwahl · Baum modellieren → neuen Fall
einordnen → Ergebnis bewerten · Streudiagramm deuten → Gerade bestimmen →
Prognose rechnen · Metrik berechnen → fachliche Konsequenz beurteilen.

### Punkteschlüssel

Abgeleitet aus der Punktevergabe der vier Referenzprüfungen.

| Leistung | Punkte |
|---|---|
| Ein Begriff, eine Zahl, eine Zuordnung | 1 |
| Zuordnungstabelle mit fünf Begriffen | 5 |
| Drei Nennungen ohne Begründung | 3 |
| Drei Nennungen mit Szenariobezug oder je einem erläuternden Satz | 6 |
| Sachverhalt beschreiben oder erläutern, 2–4 Sätze | 4–6 |
| Zusammenhang in Fachsprache deuten | 4–5 |
| Einschrittige Rechnung mit Rechenweg (Accuracy, Recall) | 4 |
| Vier bis fünf Kennwerte aus einer Datentabelle | 6–7 |
| Funktionsgleichung aus einem Diagramm bestimmen | 6–7 |
| Diagramm mit Achsenbeschriftung und Titel erstellen | 6 |
| Gerade in ein vorhandenes Diagramm einzeichnen | 3 |
| Ausfüllraster mit vier Leitfragen | 8 |
| Begründete Entscheidung an zwei Situationen | 6 |
| Vergleich über zwei Kriterien mit Begründung | 8 |
| Entscheidungsbaum aus Daten modellieren | 12–15 |
| Einen neuen Fall durch den Baum führen | 5–6 |

**Ein Punkt ≈ 36 Sekunden.** Passt die Summe nicht zur Bearbeitungszeit, sind die
Punkte falsch verteilt — nicht die Zeit. Merksatz: Ein Punkt ist eine Nennung,
keine Minute.

### Materialien

Material heißt hier **Anlage**, fortlaufend nummeriert, abtrennbar und ohne den
Aufgabentext lesbar. **Jede Anlage trägt mindestens zwei Teilaufgaben** — eine
Datentabelle, die nur einmal genutzt wird, ist verschwendete Prüfungszeit.

Bewährte Anlagentypen mit ihren Bauvorgaben stehen im Dokument „Prüfungsgerüst
und Aufgabenmuster", Abschnitt 6. Kurzfassung:

- **Zuordnungstabelle:** links leeres Eintragfeld, rechts fünf Definitionen in je
  einem Satz, Reihenfolge gegenüber der Begriffsliste vertauscht.
- **Rohdatentabelle:** 10–15 ganzzahlige Werte, ein bis zwei klar abgesetzte
  Ausreißer, ungerade Anzahl der bereinigten Werte.
- **Merkmalstabelle mit Klassenspalte:** 6–10 Datensätze, zwei metrische
  Merkmale, zusätzlich als Streudiagramm.
- **Confusion-Matrix:** Vierfeldertafel, glatte Zahlen, Randsumme 100 oder 200,
  Formeln daneben abgedruckt.
- **Schemazeichnung:** nummerierte, gestrichelt umrandete Felder.
- **Ausfüllraster:** vorbereitete Leitfragen mit leeren Antwortfeldern.
- **Leeres Gitternetz:** Zeichenfläche, die Wahl der Skalierung ist Prüfleistung.

**Abbildung nur, wenn sie etwas trägt, das eine Tabelle nicht trägt.** Sinnvoll
bei Streudiagrammen mit Klassenstruktur, Regressionsgeraden, Häufigkeitsvergleich
und Schemazeichnungen. Nicht sinnvoll für fünf Messwerte.

**Ausfülltabellen:** Kopf- und Zeilenbeschriftungen vollständig, Zellen leer,
Spaltenzahl in Kopf und Datenzeilen identisch.

**Keine Quelltextfragmente.** Weder zum Lesen noch zum Lückenfüllen.

### Block C — Lösungsskizze und Qualitätsreport

**Pflicht ist die Lösungsskizze.** Sie ist knapp und besteht je Teilaufgabe aus:

- dem **ausgerechneten Ergebnis** mit allen Zwischenschritten, so wie es von
  Prüflingen erwartet wird — bei Rechenaufgaben also die vollständige Rechnung,
  nicht nur der Endwert;
- den **Teilpunkten**, deren Summe die Punktzahl der Teilaufgabe ergibt.

Sie ist kein Service für die Bewertung, sondern der Nachweis, dass die Aufgabe
lösbar ist. Wer die Lösung nicht ausrechnet, merkt nicht, wenn es keine gibt.
Rundungen werden angegeben.

Bei Zeichenaufgaben tritt an die Stelle der Rechnung die **Beschreibung einer
gültigen Lösung** samt Toleranz: welche Schwellwerte ein Entscheidungsbaum haben
darf, in welchem Bereich Steigung und Achsenabschnitt liegen dürfen.

**Optional, aber empfohlen** — der ausformulierte Erwartungshorizont mit
zulässigen Alternativen, häufigen Fehlern, Folgefehlerregelung und, bei
Entscheidungsaufgaben, dem, was eine Begründung tragfähig macht. Wird er
ausgegeben, gelten dafür die Soll-Punkte S9 und S14.

---

## 4 Prüfliste

**Muss** blockiert die Freigabe — ein einziges Rot verhindert sie, ohne Abwägung.
**Soll** ist ein Hinweis; drei oder mehr zusammen bedeuten „mit Auflagen".

### Muss

| | Prüfpunkt |
|---|---|
| M1 | Punktsumme: vollständige Prüfung **exakt 100**, Einzelblock innerhalb des Modulkorridors. Summe als Zahl protokollieren. |
| M2 | Jede Teilaufgabe trägt genau eine Punktzahl. Keine an Szenario, Überschrift oder Anlage. |
| M3 | Nummerierung lückenlos, aufsteigend, ohne Doppelung, ohne Wechsel auf Aufzählungspunkte. |
| M4 | Vollständige Prüfung 15–19 Teilaufgaben, Einzelblock 3–7. Regelspanne 3–8 Punkte, höchstens eine Aufgabe über 10. |
| M5 | Alle Pflichtbestandteile da; Ausgabe in drei Blöcken; A und B ohne Lösungshinweis. |
| M6 | Genau ein führender Operator je Teilaufgabe, aus der Operatorenliste. |
| M7 | Operator überschreitet die Stufe des Themengebiets nicht. |
| M8 | Vollständige Prüfung: Stufenverteilung in den Korridoren aus §3, **mindestens eine Aufgabe der Stufe Bewerten und eine der Stufe Gestalten.** Verteilung protokollieren. |
| M9 | Anforderungsstufen steigen innerhalb jedes Moduls monoton. |
| M10 | Kein Gegenstand von der Ausschlussliste — auch nicht in Nebensatz, Distraktor oder Block C. Die DQR-5-Liste in §2 wird ausdrücklich mitgeprüft. |
| M11 | Jeder Gegenstand steht in der DQR-4-Stichwortliste. |
| M12 | Ein durchgehendes Szenario trägt alle Teilaufgaben; in der vollständigen Prüfung je Modul um 2–3 Sätze fortgeschrieben. |
| M13 | Keine Dublette zu den vier Referenzprüfungen: Überschneidung in höchstens einem Kernkonzept bei gleichem Aufgabentyp. |
| M14 | Kein Programmcode, keine Werkzeugbedienung, keine Bibliotheksnamen als Prüfgegenstand. |
| M15 | Keine Ausführungsumgebung, kein Netz vorausgesetzt. |
| M16 | Jede Rechnung in ≤ 2 Minuten mit einfachem Taschenrechner lösbar. **Nachrechnen und protokollieren.** |
| M17 | Tabellen ≤ 8 Zeilen, ≤ 5 Spalten. Zeichnungen freihändig ≤ 4 Minuten. |
| M18 | Punktsumme passt zur Zeit: 1 Punkt ≈ 36 Sekunden (±20 %). |
| M19 | Referenzen stimmen **in beide Richtungen**: keine ins Leere, keine verwaisten Anlagenelemente. |
| M20 | Zahlenangaben im Text stimmen mit den Anlagen überein — der Text nennt genau so viele Merkmale, Klassen, Datensätze wie aufgeführt sind. |
| M21 | Jede Teilaufgabe ohne externe Information lösbar; alle Verfahrensparameter da (§5). |
| M22 | Datenbasis nennt je Spalte Typ und Wertebereich; Klassen- oder Zielspalte ausdrücklich benannt. |
| M23 | Ausfülltabellen: Spaltenzahl in Kopf und Datenzeilen identisch. |
| M24 | Anlagen vollständig spezifiziert, alle Felder gefüllt, keine Platzhalter. |
| M25 | Abbildung trägt Information, die eine Tabelle nicht trägt; in Graustufen lesbar; Ablesung eindeutig. |
| M26 | Jede Anlage trägt mindestens zwei Teilaufgaben — oder ihre Einzelnutzung ist in Block C begründet. |
| M27 | Jede in einer Rechenaufgabe benötigte Formel ist im Aufgabensatz abgedruckt. |
| M28 | Block C enthält je Teilaufgabe das ausgerechnete Ergebnis mit Zwischenschritten und die Teilpunkte; bei Zeichenaufgaben die gültige Lösung samt Toleranz. |
| M29 | **Jede Zahl in Block C unabhängig nachgerechnet und protokolliert.** |
| M30 | Teilpunkte summieren sich je Teilaufgabe exakt auf deren Punktzahl. |
| M31 | Erlaubt eine Teilaufgabe mehrere Lösungswege, ist mindestens einer vollständig durchgerechnet. |
| M32 | Keine Verletzung des Stolperstein-Katalogs (§5). |
| M33 | Vollständige Prüfung: Standardhinweise vorhanden — ganze Sätze, Rechenweg angeben, Lösungen auf Beiblätter, abtrennbare Anlagen, zugelassener Taschenrechner. |

### Soll

| | Prüfpunkt |
|---|---|
| S1 | Szenario realistisch, stimmig, ohne Jargon, der nicht Prüfgegenstand ist. |
| S2 | Ein Szenario trägt alle Teilaufgaben. |
| S3 | Aufgaben innerhalb eines Moduls bauen aufeinander auf — das Ergebnis einer Teilaufgabe ist Voraussetzung der nächsten. |
| S4 | Mindestens eine Teilaufgabe verlangt eine echte fachliche Entscheidung mit Abwägung. |
| S5 | Verständnis und Abgrenzungsfähigkeit werden geprüft, nicht Auswendiggelerntes. |
| S6 | Jede Teilaufgabe ist beim ersten Lesen eindeutig. |
| S7 | Lösbar für kaufmännische und gewerblich-technische Auszubildende gleichermaßen, ohne Domänenvorwissen jenseits des Alltags. |
| S8 | Mindestens eine Teilaufgabe ist mit Schlagworten allein nicht zu bestehen. |
| S9 | Zwei Lehrende kämen mit Block C unabhängig zur gleichen Punktzahl. *(nur bei ausformuliertem Erwartungshorizont)* |
| S10 | Niveau steigt gleichmäßig, kein Sprung nach der ersten Teilaufgabe. |
| S11 | Jede Spalte der Datenbasis wird von mindestens einer Teilaufgabe gebraucht — oder ihre Rolle als Ablenkung ist beabsichtigt und in Block C vermerkt. |
| S12 | Glatte Zahlen trotz Taschenrechner: aufgehende Differenzen, Divisoren aus {2, 4, 5, 10, 20, 25, 50, 100}, ablesbare Steigungen als einfache Brüche. |
| S13 | Bei mehrstufigen Rechenaufgaben steht der Folgefehlerhinweis: bei ungelöster Vorstufe darf geschätzt werden. |
| S14 | Ausformulierter Erwartungshorizont vorhanden: zulässige Alternativen, häufige Fehler, Folgefehlerregelung, Begründungsmaßstab bei Entscheidungsaufgaben. |

---

## 5 Stolperstein-Katalog

Nur die Zeilen lesen, die zum Thema der Aufgabe gehören. Ein Verstoß ist ein
**Muss**-Fehler (M32).

### Für alle Themen

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| Die Aufgabe behauptet einen Befund in den Daten und fragt nach seinen Ursachen — „auffällig hohe Schwankung", „starkes Ungleichgewicht", „Ausreißer", „Bias" — aber die Datenbasis trägt ihn nicht | Der Befund muss aus der Datenbasis ableitbar sein: Verteilung, Gruppierung, Anteil der Extremwerte oder Klassenverhältnis benennen. Sonst bleibt den Prüflingen nur Raten |
| Ableseaufgabe an einer Abbildung ohne Grenzangabe | Toleranz oder Bereichsgrenze im Erwartungshorizont festlegen — sonst bewerten zwei Lehrende unterschiedlich |
| Spalten in der Datenbasis, die keine Teilaufgabe braucht | streichen, oder in Block C als beabsichtigte Ablenkung vermerken |
| Ein Gegenstand aus dem DQR-5-Bestand rutscht als Nebenbemerkung hinein — Random Forest, Data Leakage, Dropout, Optimizer, SQL | gegen die Stichwortliste abgleichen, nicht gegen das eigene Fachwissen. Was dort nicht steht, gehört auch nicht in einen Distraktor |
| Ein Operator aus DQR-5-Gewohnheit: „Nennen", „Ermitteln", „Aufstellen", „Notieren", „Zeichnen", „Ableiten" | ausschließlich Operatoren der Operatorenliste. „Nennen" gilt als Synonym zu **Benennen**, alle übrigen werden ersetzt |

### Deskriptive Statistik und Datenvisualisierung

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| Median bei gerader Anzahl der Werte | ungerade Anzahl der zu berücksichtigenden Werte, oder die Mittelung der beiden mittleren Werte ist ausdrücklich Gegenstand |
| „Ausreißer" nicht klar abgesetzt | der Abstand zum nächsten Wert muss ohne Rechnung erkennbar sein; ein Wert, der nur knapp außerhalb liegt, erzeugt Streit |
| Kennwerte „ohne Ausreißer" ohne Angabe, welche das sind | entweder ist das Erkennen der Ausreißer selbst Gegenstand und in Block C festgelegt, oder die zu streichenden Werte stehen im Aufgabentext |
| Korrelationskoeffizient soll berechnet werden | ausgeschlossen. Er wird gedeutet: Richtung, Stärke, Grenzen — und die Berechnungsidee kann erläutert werden |
| Diagramm erstellen ohne passendes Gitternetz | die vorgegebene Zeichenfläche muss die Werte mit einer glatten Skalierung aufnehmen können |

### Regressionsverfahren

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| Steigung nicht ablesbar | zwei Gitterpunkte, durch die die Gerade exakt verläuft; Steigung als einfacher Bruch, y-Achsenabschnitt als glatter Wert |
| Ausgleichsrechnung verlangt | ausgeschlossen. Die Gerade wird nach Augenmaß eingezeichnet, ihre Gleichung abgelesen |
| Abhängige und unabhängige Variable vertauscht | die Wirkrichtung muss aus dem Szenario zwingend folgen; im Zweifel im Aufgabentext benennen |
| Prognose außerhalb des dargestellten Bereichs | der Prognosewert liegt innerhalb der Achsenbereiche, sonst ist Extrapolation zu thematisieren |
| Determinationskoeffizient als „Modellgüte schlechthin" | Anteil erklärter Varianz; nur deuten, nicht berechnen |

### Entscheidungs- und Klassifikationsbäume

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| Gini-Index taucht auf | **ausgeschlossen, auch als Vergleichsgröße** |
| Entropie ohne Basis oder Verteilung | Basis 2, Klassenverteilung, max. 2 Klassen, Werte so, dass log₂ aufgeht |
| Die Klassen sind nicht durch achsenparallele Schnitte trennbar | Daten so wählen, dass ein bis zwei Schwellwerte genügen; **nachprüfen, indem der Baum selbst gezeichnet wird** |
| Der neue Fall liegt auf einer Schwelle | kein Merkmalswert des Anwendungsfalls darf einem Schwellwert entsprechen oder näher als eine Rasterstufe daran liegen |
| Schwellwerte nicht eindeutig | Block C nennt einen Korridor zulässiger Schwellwerte, nicht einen einzelnen Wert |
| Pruning-Parameter ohne Wirkrichtung | kleineres `max_depth`, größeres `min_samples_split` wirken beide gegen Overfitting |

### Metriken und Modellbewertung

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| Precision oder Recall ohne positive Klasse | Definition der positiven Klasse im Aufgabentext |
| Confusion-Matrix mit unbeschrifteten oder vertauschten Achsen | Zeilen „Tatsächlich", Spalten „Vorhergesagt", beide Klassen benannt — die Vertauschung ist der häufigste Fehler und macht Recall unlösbar |
| Accuracy bei Ungleichgewicht ungeprüft | Anteil der Mehrheitsklasse angeben oder ableitbar machen |
| MSE oder RMSE soll berechnet werden | ausgeschlossen. Beide werden gedeutet: was ein niedriger Wert bedeutet, warum quadriert wird, wofür das Maß taugt |
| Validierungs- und Testdaten synonym gebraucht | Validierungsdaten steuern die Modellwahl, Testdaten messen einmalig am Ende |
| Overfitting-Befund ohne Datengrundlage | zwei Kennwerte angeben, aus denen der Unterschied zwischen Trainings- und Testleistung folgt |
| Aufteilungsverhältnis unplausibel als Falle | wenn ein fehlerhaftes Verhältnis beurteilt werden soll, muss es deutlich falsch sein (etwa 20 zu 80 zugunsten des Tests), nicht grenzwertig |

### Neuronale Netze

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| Parameterzahl oder Ausgabegröße soll berechnet werden | ausgeschlossen. Der Aufbau wird beschrieben und zugeordnet, nicht durchgerechnet |
| *Logit* unscharf | Logit = gewichtete Summe vor der Ausgabe-Aktivierung |
| Perzeptron-Schema mehrdeutig nummeriert | jedes nummerierte Feld hat genau eine zutreffende Zuordnung; Gewichte und Eingabewerte dürfen nicht auf dasselbe Feld zeigen |
| Aktivierungsfunktion passt nicht | Sigmoid als typische Aktivierung; weitergehende Funktionen nur benennen |
| Training als Formelapparat | Ablauf in Worten: Verlustfunktion, Gradienten, Anpassung der Gewichte — keine Update-Regeln |

### Umgang mit Daten

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| Join-Art unklar | Inner und Outer benannt oder eindeutig ableitbar; nur unterscheiden, nicht ausführen |
| Fehlende Werte ohne Anzahl | Anzahl oder Anteil der Lücken angeben, sonst ist keine Handlungsempfehlung begründbar |
| Datenqualitätsmängel behauptet, aber nicht sichtbar | die Tabelle muss die Mängel selbst zeigen: leere Zellen, schiefe Klassenverteilung, auffällige Werte |

### Datensicherheit, Datenschutz, Bias und Erklärbarkeit

| Was schiefgeht | Was in der Aufgabe stehen muss |
|---|---|
| Datenschutz und Datensicherheit vermischt | Datensicherheit schützt Daten, Datenschutz schützt Personen; die Frage muss erkennen lassen, welches von beiden gemeint ist |
| Pseudonymisierung = Anonymisierung | pseudonymisierte Daten bleiben personenbezogen |
| TOM undifferenziert | technische und organisatorische Maßnahmen trennen |
| Bias rein technisch dargestellt | Ursachen in Daten, Labels, Zieldefinition und gesellschaftlichem Kontext |
| „Drei Maßnahmen" ohne Bezug zum Szenario | die Maßnahmen müssen an den konkret genannten Daten des Unternehmens ansetzen, sonst ist die Aufgabe reine Reproduktion trotz höherem Operator |
| Erklärbarkeit ohne Vergleichspunkt | mindestens zwei Verfahren nennen, deren Interpretierbarkeit sich unterscheidet |
