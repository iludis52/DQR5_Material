# Prompt: Erstellung der plan.md

*Einsatz: nach Freigabe der `spec.md` durch Prüfstelle A, vor der Ableitung der Tasks.*
*Mitgeben: `@constitution.md`, `@spec.md`.*
*Version 2.0 · Neu: Prüfmittel in §3.8, Nachweistabelle als dauerhafter Abschnitt, Prüfstand als erster Arbeitsschritt in §3.10.*

---

## 1. Auftrag

Erstelle aus der freigegebenen `spec.md` einen Umsetzungsplan.

Die Spezifikation sagt **was** und **warum**. Der Plan sagt **wie**. Alles Technische lebt hier: Technologiewahl, Abhängigkeiten, Datenformate, Struktur, Auslieferung, Nachweisverfahren.

Der Plan ist ein flüchtiges Dokument — **mit einer Ausnahme**. Er darf nach abgeschlossener Umsetzung verworfen werden; die Spezifikation bleibt. **§3.8 und §3.9 bleiben ebenfalls**: sie werden beim Verwerfen als Anhang zur `spec.md` gesichert. Sie tragen das Abnahmesignal. Wer sie wegwirft, muss bei der nächsten Änderung neu festlegen, woran ein Kriterium gemessen wird — und das tut dann meist die Instanz, die den Code schreibt.

Schreibe knapp, entscheidungsorientiert, ohne Wiederholung der Spezifikation und **ohne Pseudocode**. Wenn der Plan anfängt, das Programm zu sein, ist er zu detailliert. Der Detailgrad richtet sich nach dem Risiko: geringe Kritikalität, geringer Detailgrad.

Es gilt die `constitution.md`, insbesondere §2 (Annahmen und Rückfragen), §3 (Einfachheit), §6 (keine Erfindungen, Freigabe von Abhängigkeiten) und §7 (Sprache, Daten, Reproduzierbarkeit). Die folgenden Abschnitte wiederholen sie nicht — sie verschärfen sie für diese Phase.

---

## 2. Drei Verschärfungen für diese Phase

**Ungeprüftes wird gekennzeichnet.** Wo du eine Angabe nicht prüfen konntest, schreibe **„ungeprüft"** dazu. Eine plausibel klingende Angabe ohne Prüfung ist schlimmer als eine offen gekennzeichnete Lücke.

**Fachliche Lücken gehen zurück, technische füllst du.** Ist die Spezifikation an einer fachlichen Stelle mehrdeutig, hältst du an und fragst. Technische Lücken zu schließen ist der Zweck dieses Dokuments — dafür fragst du nicht. **Invarianten sind fachlich:** du legst fest, womit sie geprüft werden, nie, ob sie gelten.

**Verhaltensannahmen werden jetzt geprüft, nicht später.** Siehe §3.4.

---

## 3. Inhalt der plan.md

**3.1 Umfang.** Was umgesetzt wird, mit Verweis auf die Spezifikation. Was ausdrücklich nicht.

**3.2 Technologiewahl.** Je Entscheidung eine Zeile Begründung und die verworfene Alternative. Kurz.

**3.3 Freigegebene Abhängigkeiten.** Tabelle: Paket, **feste Version**, Zweck, Beleg. Belegt heißt: gegen die Registry geprüft, nicht erinnert. Prüfe insbesondere, ob ein Paket eigene Typdefinitionen mitbringt oder ein zusätzliches Typpaket braucht.

**3.4 Verhaltensannahmen.** Eigene Tabelle. Jede Aussage darüber, **wie** sich eine fremde Funktion verhält, kommt hierher: Annahme, Prüfszenario, Ergebnis.

Die Prüfung findet **beim Schreiben des Plans** statt, nicht in der Umsetzung. Installiere die festgelegte Version, führe ein kurzes Skript aus, notiere die Ausgabe wörtlich. Kannst du nicht ausführen, markiere die Zeile als **offen** und melde das im Abschlussbericht als Blockierer. Eine unbelegte Verhaltensannahme, auf der die Kernlogik steht, ist der teuerste Fehler in diesem Dokument.

**3.5 Auslieferung.** Zielumgebung, Aufrufpfad, Basispfad-Konfiguration, Umgang mit statischen Dateien und Datendateien. Ein Bauvorgang ohne Fehler ist kein Nachweis, dass das Ergebnis startet — plane einen Schritt, der das ausgelieferte Artefakt tatsächlich aufruft.

**3.6 Datenmodell und Formate.** Schemata, Dateien, Gültigkeitsregeln.

**3.7 Struktur und Benennung.** Verzeichnisse, Module, Sprache der Bezeichner.

**3.8 Prüfbefehle.** *Dieser Abschnitt wird archiviert, nicht verworfen.*

Die Befehle, mit denen das Projekt geprüft wird. Mindestens einer prüft das **gestartete** Produkt, nicht nur den Quellstand. Je Befehl: was er prüft, wo seine Ausgabe landet, was ein Fehlschlag bedeutet.

Zusätzlich legst du fest, sofern das Projekt es braucht:

* **Prüfung der Invarianten.** Womit werden die Relationen aus Teil 3.2 der Spezifikation über einen Eingabebereich geprüft, nicht nur an einzelnen Werten? Nenne das Verfahren, die Zahl der Eingaben und die Toleranz aus der Spezifikation. Eine Invariante, die nur an drei handverlesenen Werten geprüft wird, ist ein Beispieltest mit anderem Namen.
* **Bedienung der laufenden Anwendung.** Hat das Produkt eine Oberfläche, benennst du das Werkzeug, mit dem eine ausführende Instanz sie **selbst bedient**, und die Artefakte, die dabei entstehen: Accessibility-Snapshot, Screenshot, Browserkonsole, Netzwerkmitschnitt, jeweils mit Ablageort. Entscheidend ist nicht das Bedienen, sondern dass prüfbare Dateien zurückbleiben — sie sind unabhängig von dem, was die Instanz über ihren Lauf behauptet. Bevorzuge Werkzeuge, die ihre Ausgabe auf die Festplatte schreiben, statt sie in den Kontext des Modells zu spielen; Kontext ist die knappste Ressource der Umsetzung.
* **Belastbarkeit der Tests.** Ein Befehl, der die Tests gegen absichtlich verfälschten Code laufen lässt. Überlebt eine Verfälschung, ist das eine Testlücke, nicht ein bestandener Lauf. Gibt es für den gewählten Stack kein fertiges Werkzeug, legst du das Verfahren von Hand fest: geänderte Dateien bestimmen, je Kernfunktion eine Verfälschung setzen, Tests laufen lassen, Ergebnis notieren, Verfälschung zurücknehmen. Nenne den Umfang — vollständige Läufe sind teuer, der Kern reicht.

Ist eines dieser Prüfmittel nicht sinnvoll oder nicht verfügbar, schreibst du hin, **warum**, und was stattdessen gilt. Schweigen an dieser Stelle ist ein Befund für Prüfstelle B.

**3.9 Nachweistabelle.** *Dieser Abschnitt wird archiviert, nicht verworfen.*

Eine Zeile je Akzeptanzkriterium der Spezifikation — Verhalten, Invarianten und Zustände gleichermaßen: Kriterium, geplantes Nachweisverfahren (automatisierter Test / Invariantenprüfung / browsergestützte Prüfung / Handprüfung), zuständiger Prüfbefehl.

Kriterien, für die nur Handprüfung bleibt, kennzeichnest du hier. Sie können später nur GELB erreichen — ein Kriterium, das als automatisch prüfbar aussieht, aber Handprüfung braucht, wird abgehakt werden, ohne erfüllt zu sein. Prüfe für jedes solche Kriterium zuerst, ob eine browsergestützte Prüfung möglich wäre. Zustandskriterien sind fast immer browsergestützt prüfbar; ein Fehler- oder Ladezustand lässt sich durch Abfangen und Verzögern der Hintergrundaufrufe herbeiführen, ohne dass ein Mensch zusehen muss.

**3.10 Schnitt in Arbeitsschritte.** Jeder Schritt muss innerhalb **eines** Kontextfensters umsetzbar **und** prüfbar sein. Je Schritt: Inhalt, Prüfkriterium (vor der Umsetzung festgelegt), Nachweisart.

**Der erste Schritt ist immer der Prüfstand**, nicht die erste Fachlichkeit: Umgebung, Prüfbefehle aus §3.8, Bedienwerkzeug, Verfälschungsbefehl. Er ist fertig, wenn der leere Prüfstand läuft und **erwartet fehlschlägt**. Ein Prüfstand, der auf leerem Projekt grün meldet, misst nichts.

**3.11 Risiken und offene Punkte.** Was schiefgehen kann, was ungeprüft blieb, was aus §3.4 offen ist.

---

## 4. Vorarbeit bei neuen Projekten

Handelt es sich um ein neues Projekt, erzeuge **vor** dem Detailplan ein leeres, lauffähiges Projektgerüst im gewählten Stack, mit den festgelegten Abhängigkeiten. Prüfe daran, dass Bauvorgang **und** Aufruf des gebauten Ergebnisses funktionieren. Erst dann planst du weiter. Das kostet zehn Minuten und fängt genau die Fehlerklasse, die sonst erst am Ende auffällt.

Prüfe bei dieser Gelegenheit auch, ob die in §3.8 vorgesehenen Prüfmittel im gewählten Stack überhaupt laufen. Ein Bedienwerkzeug oder eine Verfälschungsprüfung, die erst in der Umsetzung als unverfügbar auffällt, kostet den halben Nutzen des Sets.

---

## 5. Abschlussbericht

* welche Verhaltensannahmen geprüft wurden und mit welchem Ergebnis,
* welche Angaben ungeprüft blieben und warum,
* welche Prüfmittel aus §3.8 festgelegt sind, welche entfallen und mit welcher Begründung,
* je Invariante der Spezifikation: wie sie geprüft wird und über welchen Eingabebereich,
* welche Kriterien nur per Handprüfung nachweisbar sind — mit der Angabe, wie viele davon du durch browsergestützte Prüfung ablösen konntest,
* ob du von der `constitution.md` abgewichen bist und wo,
* ob du auf eine fachliche Lücke gestoßen bist, die zurück in die Spezifikation muss.
