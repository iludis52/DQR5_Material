# Metaprompt: Erstellung einer spec.md (SDD)

*Version 3.0 · Ersetzt v2.0. Aufbau: Teil 1–5 generischer Kern, Teil 6 austauschbarer Domänenblock, Teil 7 Projektidee.*

---

## 1. Auftrag

Wir arbeiten spec-driven. Ergebnis dieses Gesprächs ist eine `spec.md` von **höchstens drei Seiten**.

Die Spezifikation beschreibt **was** gebaut wird und **warum** — nicht wie. Kein Technikstack, keine Bibliotheken, keine Versionen, kein Code. Das gehört in die anschließende `plan.md`. Enthält die Spezifikation Code, ist das Programm zweimal geschrieben und die Spezifikation wertlos.

Die `spec.md` wird anschließend von einem **anderen Modell geprüft** und von einem **dritten Modell umgesetzt**. Schreibe für die prüfende Instanz: jede Festlegung muss von außen nachvollziehbar und widerlegbar sein.

**Schreibe die `spec.md` erst auf mein ausdrückliches Kommando** („Erstelle jetzt die spec.md").

---

## 2. Gliederung der spec.md

1. **Zweck** — welches Problem, für wen, warum lohnend
2. **Nutzer:innen und Einsatzkontext**
3. **Fachlicher Inhalt und Umfang** (siehe Domänenblock)
4. **Nicht-Ziele** — was ausdrücklich nicht gebaut wird
5. **Akzeptanzkriterien** in EARS (Teil 3)
6. **Offene Punkte** — bewusst nicht Entschiedenes, je mit Prüfauftrag an das Review
7. **Rückverfolgung** — Tabelle: je Anforderung aus der Projektidee eine Zeile mit ID, Wortlaut, Status (*umgesetzt / verschoben / gestrichen*) und Begründung. Eine Anforderung darf verschwinden, aber nicht unbemerkt.

---

## 3. Akzeptanzkriterien in EARS

Jedes Kriterium folgt einem dieser fünf Muster. Schlüsselwörter englisch, Satzkörper deutsch.

| Muster | Vorlage |
| --- | --- |
| ubiquitär | THE system SHALL … |
| ereignisgetrieben | WHEN … THE system SHALL … |
| zustandsgetrieben | WHILE … THE system SHALL … |
| unerwünschtes Verhalten | IF … THEN … |
| optional | WHERE … THE system SHALL … |

Regeln:

* Jedes Kriterium beschreibt **beobachtbares Verhalten des laufenden Produkts**, nie einen Zustand des Quellcodes. Ein erfolgreicher Build ist kein Akzeptanzkriterium.
* Mindestens ein Kriterium betrifft den **Aufruf des ausgelieferten Artefakts** in der Zielumgebung.
* Ein Kriterium, das sich nicht in einen Testfall übersetzen lässt, ist noch nicht fertig formuliert.
* Halte fest, welche Kriterien absehbar **nicht automatisiert** prüfbar sind. Sie dürfen später nur als GELB gemeldet werden, nicht als erledigt.

---

## 4. Ablauf des Klärungsgesprächs

**Zuerst:** Nenne mindestens einen begründeten Einwand gegen die Projektidee **selbst**, nicht gegen ihre Umsetzung. Trifft das vorgeschlagene Produkt das beschriebene Problem? Ist eine andere Produktform näher? Ist die Idee tragfähig, benenne die stärkste Gegenposition und warum sie überwindbar ist.

**Dann, intern:** Prüfe die Projektidee gegen diese Punkte und markiere jeden als *klar / teilweise / fehlend*:

> Zweck · Nutzer:innen · fachlicher Inhalt und Umfang · Progression · Bedienmodell · Zustände und Fehlerfälle · Datenbedarf · Auslieferung und Aufrufweg · Akzeptanz · Abgrenzung · Sprache und Barrierefreiheit

**Diese Liste zeigst du nicht.** Sie steuert nur die Auswahl der Fragen.

**Dann fragen:** Höchstens **fünf Fragen pro Runde**, **einzeln nacheinander**, sortiert nach Wirkung × Unsicherheit. Zu jeder Frage nennst du deine Empfehlung mit ein bis zwei Sätzen Begründung. Wo eine Auswahl sinnvoll ist, biete zwei bis drei Optionen an und sage zu jeder, **was sie an anderer Stelle ausschließt**. Bei Fragen zu Zweck, Inhalt und Bedienmodell keine Optionslisten — dort ist der Optionsraum selbst die Designentscheidung; frage offen und stelle deine Einschätzung getrennt daneben.

**Am Ende jeder Runde:** eine Statuszeile je Punkt aus der internen Liste — *geklärt / zurückgestellt / war bereits klar / weiterhin offen* — plus Empfehlung, ob eine weitere Runde lohnt.

**Weitere Runden** starte ich. Jede Runde findet andere Lücken. Wenn deine Fragen anfangen, Nebensächliches zu betreffen, sag das offen — dann ist die Spezifikation gut genug.

**Widersprüche** benennst du, statt sie aufzulösen. Widerspricht meine Antwort einer früheren Festlegung, sagst du es.

---

## 5. Selbstprüfung vor dem Schreiben

Nach meinem Kommando und vor der Ausgabe arbeitest du diese fünf Punkte sichtbar ab:

1. Ist jedes in Teil 3 des Inhalts geforderte Element mit dem festgelegten Bedienmodell **tatsächlich erreichbar**? Prüfe die schwierigsten Fälle, nicht die einfachsten.
2. Erfüllt mindestens ein Akzeptanzkriterium den Bezug auf das ausgelieferte Artefakt?
3. Hat jede Anforderung aus Teil 7 eine Zeile in der Rückverfolgung?
4. Steht irgendwo Technik, Bibliothek oder Code? Dann streichen und nach `plan.md` verweisen.
5. Könnten Beispieldaten für vollständige Inhalte gehalten werden? Dann als Beispiel kennzeichnen und den vollen Umfang benennen.

---

## 6. Domänenblock

> Je Projekt austauschbar. Nachfolgend der Block **Lernanwendung**.

* **Der Inhalt ist Liefergegenstand.** Die Spezifikation enthält den vollständigen Aufgaben- oder Materialbestand, oder sie benennt dessen Erstellung als eigenen Arbeitsschritt mit eigener Abnahme. Ein Beispieldatensatz ersetzt den Bestand nicht.
* **Jeder Aufgabentyp bekommt eine eigene ID** in der Rückverfolgung. Typen mit unterschiedlichem Bedienbedarf werden nicht stillschweigend zusammengelegt.
* **Progression fachlich begründen:** woran genau steigt die Schwierigkeit?
* **Fehlvorstellungen** der Zielgruppe benennen und sagen, wie das Produkt darauf reagiert. Nur richtig/falsch zu melden adressiert keine Fehlvorstellung.
* **Fachrichtigkeit vor Bedienkomfort.** Erzwingt eine Bedienvereinfachung fachlich falsche Darstellungen, ist das ein Einwand nach Teil 4, keine Detailfrage.
* Mindestens ein Akzeptanzkriterium beschreibt einen **Lernvorgang**, keine Bedienhandlung.

---

## 7. Projektidee

> Formuliere ruhig vage — die Klärung ist Aufgabe des Gesprächs. Nenne aber **alle** Nutzungs- und Aufgabentypen, die dir vorschweben, auch die unfertigen: was hier nicht steht, kann nicht zurückverfolgt werden.

```
[Projektidee]
```

---

*Was bewusst nicht hier steht und in `plan.md` gehört: Technologiewahl, Bibliotheken mit festen Versionen, Datenformate und Schemata, Architektur, Projektstruktur, Prüfbefehle, Phasenzuschnitt. Verhaltensannahmen über Fremdbibliotheken werden dort vor Verwendung belegt — Existenz und Signatur einer Funktion sind kein Beleg für ihr Verhalten.*
