# Metaprompt: Erstellung einer spec.md (SDD)

*Version 4.0 · Ersetzt v3.0. Aufbau: Teil 1–5 generischer Kern, Teil 6 austauschbarer Domänenblock, Teil 7 Projektidee.*
*Neu gegenüber v3.0: Invarianten (Teil 3.2), Zustandskriterien (Teil 3.3), zwölfter Punkt der internen Liste, zwei zusätzliche Selbstprüfungen.*

---

## 1. Auftrag

Wir arbeiten spec-driven. Ergebnis dieses Gesprächs ist eine `spec.md` von **höchstens drei Seiten Fließtext**, zuzüglich der Kriterientabelle und der Rückverfolgung.

Die Spezifikation beschreibt **was** gebaut wird und **warum** — nicht wie. Kein Technikstack, keine Bibliotheken, keine Versionen, kein Code. Das gehört in die anschließende `plan.md`. Enthält die Spezifikation Code, ist das Programm zweimal geschrieben und die Spezifikation wertlos.

Die `spec.md` wird anschließend von einem **anderen Modell geprüft** und von einem **dritten Modell umgesetzt**. Schreibe für die prüfende Instanz: jede Festlegung muss von außen nachvollziehbar und widerlegbar sein.

**Die Kriterien sind das Maß, an dem später gemessen wird — und die umsetzende Instanz darf sie nicht selbst erfinden.** Was hier nicht festgelegt ist, legt sie fest, und zwar so, dass ihre eigene Lesart bestätigt wird. Jede Lücke in Teil 3 wird später zu einem grünen Test bei mangelhaftem Produkt.

**Schreibe die `spec.md` erst auf mein ausdrückliches Kommando** („Erstelle jetzt die spec.md").

---

## 2. Gliederung der spec.md

1. **Zweck** — welches Problem, für wen, warum lohnend
2. **Nutzer:innen und Einsatzkontext**
3. **Fachlicher Inhalt und Umfang** (siehe Domänenblock)
4. **Nicht-Ziele** — was ausdrücklich nicht gebaut wird
5. **Akzeptanzkriterien** in EARS (Teil 3), gegliedert in Verhalten, Invarianten und Zustände
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

Grundregeln für alle drei Gruppen:

* Jedes Kriterium beschreibt **beobachtbares Verhalten des laufenden Produkts**, nie einen Zustand des Quellcodes. Ein erfolgreicher Build ist kein Akzeptanzkriterium.
* Mindestens ein Kriterium betrifft den **Aufruf des ausgelieferten Artefakts** in der Zielumgebung.
* Ein Kriterium, das sich nicht in einen Testfall übersetzen lässt, ist noch nicht fertig formuliert.
* Halte fest, welche Kriterien absehbar **nicht automatisiert** prüfbar sind. Sie dürfen später nur als GELB gemeldet werden, nicht als erledigt. Prüfe vorher, ob sich dasselbe Anliegen als Invariante (3.2) oder Zustandskriterium (3.3) formulieren lässt — beides ist maschinell prüfbar, ein Geschmacksurteil nicht.

### 3.1 Verhalten

Die gewohnten Kriterien: was das Produkt auf welche Handlung hin tut. Sie beschreiben Einzelfälle.

### 3.2 Invarianten

**Wo das Produkt rechnet, umformt, auflöst oder sortiert, genügen Einzelfälle nicht.** Einzelfälle brauchen Sollwerte, und Sollwerte muss jemand kennen. Kennt sie niemand, erfindet sie später die umsetzende Instanz — aus ihrer eigenen Umsetzung heraus. Genau so entstehen Tests, die eine falsche Berechnung als richtig festschreiben.

Eine **Invariante** beschreibt stattdessen, wie sich das Ergebnis ändern **muss**, wenn sich die Eingabe auf bestimmte Weise ändert. Sie gilt für alle Eingaben, sie ist ohne Kenntnis des Ergebnisses formulierbar, und sie lässt sich nicht nachträglich an eine Ausgabe anpassen.

Frage im Klärungsgespräch nach diesen Familien:

* **Skalierung** — was passiert mit dem Ergebnis, wenn eine Eingabegröße verdoppelt wird?
* **Symmetrie und Vertauschung** — gibt es Eingaben, deren Reihenfolge oder Vorzeichen das Ergebnis nicht ändern darf?
* **Umkehrung und Rückeinsetzung** — lässt sich das Ergebnis in die Ausgangsbeziehung zurücksetzen, und was muss dabei herauskommen?
* **Einheiten und Dimensionen** — welche Kombination von Eingaben ist fachlich unzulässig, und woran erkennt man das am Ergebnis?
* **Monotonie und Grenzverhalten** — in welche Richtung muss sich das Ergebnis bewegen, wenn eine Eingabe wächst? Was gilt an den Rändern des Definitionsbereichs?
* **Erhaltung** — welche Größe muss über eine Umformung hinweg gleich bleiben?

Notation: gewöhnliche EARS-Muster, mit der Relation im Satzkörper.

> WHEN eine Eingabegröße verdoppelt wird und alle übrigen unverändert bleiben, THE system SHALL ein Ergebnis liefern, das sich um denselben Faktor ändert.
> THE system SHALL für jede Umformung gelten lassen, dass das Rückeinsetzen des Ergebnisses die Ausgangsbeziehung innerhalb der festgelegten Toleranz erfüllt.
> IF eine Kombination von Eingaben dimensionsmäßig unzulässig ist, THEN THE system SHALL keine Zahl ausgeben, sondern die Unzulässigkeit benennen.

Regeln:

* **Eine Invariante muss verletzbar sein.** Eine Relation, die jede denkbare Implementierung erfüllt, ist keine Invariante, sondern eine Beschreibung. Frage dich zu jeder: welche plausible Falschumsetzung würde sie brechen? Kannst du keine nennen, streiche sie.
* **Toleranzen gehören dazu.** Wo gerundet oder numerisch gerechnet wird, nennt die Invariante die zulässige Abweichung. Ohne Toleranz ist sie nicht prüfbar.
* **Der Gültigkeitsbereich gehört dazu.** Für welche Eingaben gilt sie, für welche ausdrücklich nicht?
* **Invarianten sind fachliche Aussagen** und gehören deshalb hierher, nicht in die `plan.md`. Wie sie geprüft werden, entscheidet der Plan; **dass** sie gelten, entscheidest du hier.

### 3.3 Zustände

Für **jede interaktive Funktion** entstehen Kriterien für diese fünf Zustände:

| Zustand | Frage |
| --- | --- |
| leer | Was zeigt das Produkt, bevor etwas eingegeben oder ausgewählt wurde? |
| lädt | Was geschieht, während etwas dauert? Woran erkennen Nutzende, dass gearbeitet wird? |
| Fehler | Was geschieht, wenn ein Vorgang scheitert? Was steht dann auf dem Bildschirm? |
| Grenzwert | Was geschieht am Rand des zulässigen Bereichs — leere Auswahl, ein einziges Element, sehr viele Elemente, sehr lange Eingaben? |
| ungültige Eingabe | Was geschieht bei einer Eingabe, die nicht verarbeitet werden kann, und wie kommen Nutzende zurück in den gültigen Zustand? |

Diese Zustände sind der häufigste Ort für Mängel, die kein Test bemerkt und jede Nutzerin sofort sieht. Sie sind kein Umsetzungsdetail: Was hier nicht als Kriterium steht, wird weder gebaut noch geprüft, und die Beurteilung landet als Geschmacksfrage in der Abnahme oder gar nicht.

Nicht jede Funktion braucht alle fünf. Trifft ein Zustand nicht zu, schreibe das ausdrücklich hin — „entfällt, weil …" ist eine Festlegung, Schweigen ist eine Lücke.

---

## 4. Ablauf des Klärungsgesprächs

**Zuerst:** Nenne mindestens einen begründeten Einwand gegen die Projektidee **selbst**, nicht gegen ihre Umsetzung. Trifft das vorgeschlagene Produkt das beschriebene Problem? Ist eine andere Produktform näher? Ist die Idee tragfähig, benenne die stärkste Gegenposition und warum sie überwindbar ist.

**Dann, intern:** Prüfe die Projektidee gegen diese Punkte und markiere jeden als *klar / teilweise / fehlend*:

> Zweck · Nutzer:innen · fachlicher Inhalt und Umfang · Progression · Bedienmodell · Zustände und Fehlerfälle · **Invarianten und Prüfbarkeit** · Datenbedarf · Auslieferung und Aufrufweg · Akzeptanz · Abgrenzung · Sprache und Barrierefreiheit

**Diese Liste zeigst du nicht.** Sie steuert nur die Auswahl der Fragen.

**Dann fragen:** Höchstens **fünf Fragen pro Runde**, **einzeln nacheinander**, sortiert nach Wirkung × Unsicherheit. Zu jeder Frage nennst du deine Empfehlung mit ein bis zwei Sätzen Begründung. Wo eine Auswahl sinnvoll ist, biete zwei bis drei Optionen an und sage zu jeder, **was sie an anderer Stelle ausschließt**. Bei Fragen zu Zweck, Inhalt und Bedienmodell keine Optionslisten — dort ist der Optionsraum selbst die Designentscheidung; frage offen und stelle deine Einschätzung getrennt daneben.

**Bei Invarianten fragst du anders herum.** Frage nicht „welche Invarianten soll das Produkt erfüllen" — darauf hat niemand eine fertige Antwort. Frage nach dem Fach: was muss gelten, wenn man diese Größe verdoppelt? Was darf sich bei dieser Umformung nicht ändern? Woran würdest du merken, dass die Rechnung falsch ist, ohne das richtige Ergebnis zu kennen? Schlage anschließend eine Formulierung vor und lass sie bestätigen oder verwerfen. Eine Invariante, die du erfunden und niemand bestätigt hat, gehört nicht in die Spec.

**Am Ende jeder Runde:** eine Statuszeile je Punkt aus der internen Liste — *geklärt / zurückgestellt / war bereits klar / weiterhin offen* — plus Empfehlung, ob eine weitere Runde lohnt.

**Weitere Runden** starte ich. Jede Runde findet andere Lücken. Wenn deine Fragen anfangen, Nebensächliches zu betreffen, sag das offen — dann ist die Spezifikation gut genug.

**Widersprüche** benennst du, statt sie aufzulösen. Widerspricht meine Antwort einer früheren Festlegung, sagst du es.

---

## 5. Selbstprüfung vor dem Schreiben

Nach meinem Kommando und vor der Ausgabe arbeitest du diese sieben Punkte sichtbar ab:

1. Ist jedes in Teil 3 des Inhalts geforderte Element mit dem festgelegten Bedienmodell **tatsächlich erreichbar**? Prüfe die schwierigsten Fälle, nicht die einfachsten.
2. Erfüllt mindestens ein Akzeptanzkriterium den Bezug auf das ausgelieferte Artefakt?
3. Hat jede Anforderung aus Teil 7 eine Zeile in der Rückverfolgung?
4. Steht irgendwo Technik, Bibliothek oder Code? Dann streichen und nach `plan.md` verweisen.
5. Könnten Beispieldaten für vollständige Inhalte gehalten werden? Dann als Beispiel kennzeichnen und den vollen Umfang benennen.
6. **Hat jede rechnende oder umformende Funktion mindestens eine Invariante?** Und: nenne zu jeder Invariante in einem Halbsatz die Falschumsetzung, die sie brechen würde. Fällt dir keine ein, ist die Invariante wertlos — streiche sie und sag, dass du es getan hast.
7. **Hat jede interaktive Funktion Kriterien für die fünf Zustände**, oder ist ausdrücklich vermerkt, welche entfallen und warum?

---

## 6. Domänenblock

> Je Projekt austauschbar. Nachfolgend der Block **Lernanwendung**.

* **Der Inhalt ist Liefergegenstand.** Die Spezifikation enthält den vollständigen Aufgaben- oder Materialbestand, oder sie benennt dessen Erstellung als eigenen Arbeitsschritt mit eigener Abnahme. Ein Beispieldatensatz ersetzt den Bestand nicht.
* **Jeder Aufgabentyp bekommt eine eigene ID** in der Rückverfolgung. Typen mit unterschiedlichem Bedienbedarf werden nicht stillschweigend zusammengelegt.
* **Progression fachlich begründen:** woran genau steigt die Schwierigkeit?
* **Fehlvorstellungen** der Zielgruppe benennen und sagen, wie das Produkt darauf reagiert. Nur richtig/falsch zu melden adressiert keine Fehlvorstellung.
* **Fachrichtigkeit vor Bedienkomfort.** Erzwingt eine Bedienvereinfachung fachlich falsche Darstellungen, ist das ein Einwand nach Teil 4, keine Detailfrage.
* **Fachrichtigkeit wird geprüft, nicht behauptet.** Rechnet, formt um oder wertet das Produkt aus, gehören die fachlichen Invarianten nach 3.2 zum Liefergegenstand. Bei physikalischen und chemischen Größen sind Dimensions- und Einheitenkonsistenz sowie das Verhalten an den Rändern des Definitionsbereichs Pflichtinvarianten — dort liegen die Fehler, die fachlich falsch, aber optisch unauffällig sind.
* **Rückmeldungen an Lernende sind Zustände nach 3.3.** Was das Produkt bei falscher, unvollständiger oder unerwarteter Eingabe zeigt, ist didaktisch die wichtigste Stelle und gehört als Kriterium in die Spec, nicht in die Umsetzung.
* Mindestens ein Akzeptanzkriterium beschreibt einen **Lernvorgang**, keine Bedienhandlung.

---

## 7. Projektidee

> Formuliere ruhig vage — die Klärung ist Aufgabe des Gesprächs. Nenne aber **alle** Nutzungs- und Aufgabentypen, die dir vorschweben, auch die unfertigen: was hier nicht steht, kann nicht zurückverfolgt werden.

```
[Projektidee]
```

---

*Was bewusst nicht hier steht und in `plan.md` gehört: Technologiewahl, Bibliotheken mit festen Versionen, Datenformate und Schemata, Architektur, Projektstruktur, Prüfbefehle, Phasenzuschnitt. Auch die Prüfmittel gehören dorthin — mit welchem Werkzeug eine Invariante geprüft wird, wie die laufende Anwendung bedient wird und wie die Belastbarkeit der Tests kontrolliert wird, entscheidet der Plan. Verhaltensannahmen über Fremdbibliotheken werden dort vor Verwendung belegt — Existenz und Signatur einer Funktion sind kein Beleg für ihr Verhalten.*

*Was hier steht und nicht in den Plan wandern darf: die Invarianten selbst. Sie sind fachlich, sie sind dauerhaft, und sie sind das Maß, das die umsetzende Instanz nicht schreiben darf.*
