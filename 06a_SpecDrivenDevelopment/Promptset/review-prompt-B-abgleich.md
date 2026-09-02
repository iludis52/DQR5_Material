# Prüf-Prompt B: Abgleich vor der Implementierung

*Einsatz: nachdem `plan.md` und `tasks.md` vorliegen, vor dem ersten Code. In einer frischen Sitzung und mit einem anderen Modell als dem, das Plan oder Tasks geschrieben hat.*
*Mitgeben: `@constitution.md`, `@spec.md`, `@plan.md`, `@tasks.md`.*
*Version 2.0 · Neu: Prüfstand und Prüfmittel (§2, Punkte 5–8), Invariantenabdeckung, erweiterte Abdeckungstabelle.*

---

## 1. Auftrag

Prüfe die vier Dokumente **gegeneinander**. Du änderst nichts. Du bist read-only und lieferst einen Bericht.

Diese Prüfstelle existiert, weil Fehler an den Nahtstellen entstehen: eine Anforderung, die keine Aufgabe hat; eine Aufgabe, die auf keine Anforderung zurückgeht; ein Prüfkriterium, das niemand erfüllen kann; eine technische Annahme, die niemand belegt hat; ein Nachweisverfahren, das eine falsche Umsetzung nicht bemerken würde.

---

## 2. Prüfliste

**Abdeckung**

1. Hat **jedes** Akzeptanzkriterium der `spec.md` mindestens eine Aufgabe in `tasks.md`? Liste die unabgedeckten auf. Prüfe die drei Gruppen getrennt: Verhalten, Invarianten, Zustände. Die Zustandskriterien fallen erfahrungsgemäß zuerst heraus.
2. Verweist **jede** Aufgabe auf das Kriterium, das sie erfüllt? Aufgaben ohne Bezug sind entweder überflüssig oder ein Zeichen für eine fehlende Anforderung — sag, welches von beidem. Ausgenommen ist T0.
3. Hat **jede Invariante** ein Aufgabenpaar, und nennt dessen Fertigkriterium einen **Eingabebereich** samt Toleranz statt einzelner Werte? Eine Invariante, die an handverlesenen Werten geprüft wird, ist ein Beispieltest mit anderem Namen — das ist ein BLOCKIERER, weil genau dieser Fall wie eine Absicherung aussieht und keine ist.

**Prüfbarkeit**

4. Ist jedes Fertigkriterium so formuliert, dass ein **ausführender Agent** es selbst nachweisen kann? Kriterien, die eine menschliche Sichtprüfung verlangen, listest du gesondert auf. Sie sind zulässig, müssen aber als solche gekennzeichnet sein und dürfen später nur GELB erreichen. Ein Kriterium, das Handprüfung verlangt, aber wie ein automatisch prüfbares aussieht, ist ein **BLOCKIERER** — es wird abgehakt werden, ohne erfüllt zu sein.
5. **Existiert T0, und misst der Prüfstand?** Prüfe: Deckt T0 alle in `plan.md` §3.8 festgelegten Prüfmittel ab? Lautet sein Fertigkriterium auf **erwarteten Fehlschlag**? Ein T0, dessen Fertigkriterium „läuft durch" ist, prüft nur sich selbst und ist ein BLOCKIERER. Fehlt T0 ganz, beginnt die Umsetzung ohne Messeinrichtung — ebenfalls BLOCKIERER.
6. **Sind die Prüfmittel aus `plan.md` §3.8 vollständig festgelegt?** Für jedes der drei — Invariantenprüfung, Bedienung der laufenden Anwendung, Belastbarkeit der Tests — muss entweder ein Befehl stehen oder eine ausdrückliche Begründung, warum es entfällt. Schweigen ist ein Befund. Prüfe außerdem, ob die genannten Werkzeuge zum gewählten Stack passen und ob `plan.md` §4 ihre Verfügbarkeit belegt hat.
7. Prüft mindestens ein Prüfschritt das **gebaute, gestartete Artefakt** in der Zielumgebung? Ein grüner Build und grüne Unit-Tests sind kein Nachweis, dass die Anwendung läuft.
8. **Erzeugen die browsergestützten Aufgaben Belege?** Nennt das Fertigkriterium die Artefakte und ihren Ablageort, und hat die Aufgabe ein Feld dafür? Eine browsergestützte Prüfung ohne zurückbleibende Datei ist eine Behauptung.
9. Wie hoch ist der Anteil der Anwendung, der von automatisierten Tests tatsächlich berührt wird? Nenne die Bereiche, die vollständig ungeprüft bleiben. Berührung ist nicht Prüfung: sag zusätzlich, für welche Bereiche eine Verfälschungsprüfung vorgesehen ist und für welche nicht.

**Belege**

10. Enthält `plan.md` Aussagen über das **Verhalten** fremder Bibliotheken? Für jede solche Aussage: Existenz und Signatur einer Funktion sind **kein** Beleg für ihr Verhalten. Verlange ein kurzes Prüfskript gegen die installierte Version und melde ROT, wenn keines vorgesehen ist.
11. Sind alle Abhängigkeiten mit fester Version freigegeben und die Versionsangaben belegt?

**Widerspruch und Erosion**

12. Widersprechen sich die Dokumente? Löse den Widerspruch **nicht** auf — benenne ihn und die betroffenen Stellen.
13. Weicht ein Dokument von der `constitution.md` ab? Zulässig ist nur die ausdrückliche und begründete Abweichung. Stillschweigende Abweichungen meldest du.
14. Ist im Verlauf von Spezifikation zu Plan zu Tasks fachliche Substanz **verlorengegangen**? Vergleiche den Umfang, nicht nur die Formulierungen.
15. **Ist eine Invariante auf dem Weg weich geworden?** Vergleiche den Wortlaut in der Spezifikation mit dem Fertigkriterium in `tasks.md`. Eine Toleranz, die im Plan großzügiger ist als in der Spec, ein Gültigkeitsbereich, der sich verengt hat, eine Relation, die zur Stichprobe geschrumpft ist — das sind stillschweigende Abschwächungen des Maßes und gehören zu den Blockierern.

---

## 3. Form

Bericht in drei Blöcken:

* **BLOCKIERER** — Umsetzung darf nicht beginnen. Je Eintrag: Fundstelle(n), Sachverhalt, was zu tun ist.
* **RISIKEN** — Umsetzung möglich, Nacharbeit wahrscheinlich.
* **ABDECKUNGSTABELLE** — je Akzeptanzkriterium eine Zeile: Gruppe (Verhalten / Invariante / Zustand), abgedeckt durch welche Aufgabe(n), Nachweisart (automatisch / Invariantenprüfung / browsergestützt / Handprüfung / kein Nachweis), Verfälschungsprüfung vorgesehen (ja / nein / entfällt mit Grund).

Schließe mit einer Zeile: **Umsetzung freigegeben** oder **nicht freigegeben** (welcher Blockierer).

Du machst keine Verbesserungsvorschläge zur Technik und schreibst keine Dokumente um. Der Bericht geht an mich.
