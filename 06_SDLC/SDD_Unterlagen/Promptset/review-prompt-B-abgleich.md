# Prüf-Prompt B: Abgleich vor der Implementierung

*Einsatz: nachdem `plan.md` und `tasks.md` vorliegen, vor dem ersten Code. In einer frischen Sitzung und mit einem anderen Modell als dem, das Plan oder Tasks geschrieben hat.*
*Mitgeben: `@constitution.md`, `@spec.md`, `@plan.md`, `@tasks.md`.*

---

## 1. Auftrag

Prüfe die vier Dokumente **gegeneinander**. Du änderst nichts. Du bist read-only und lieferst einen Bericht.

Diese Prüfstelle existiert, weil Fehler an den Nahtstellen entstehen: eine Anforderung, die keine Aufgabe hat; eine Aufgabe, die auf keine Anforderung zurückgeht; ein Prüfkriterium, das niemand erfüllen kann; eine technische Annahme, die niemand belegt hat.

---

## 2. Prüfliste

**Abdeckung**

1. Hat **jedes** Akzeptanzkriterium der `spec.md` mindestens eine Aufgabe in `tasks.md`? Liste die unabgedeckten auf.
2. Verweist **jede** Aufgabe auf das Kriterium, das sie erfüllt? Aufgaben ohne Bezug sind entweder überflüssig oder ein Zeichen für eine fehlende Anforderung — sag, welches von beidem.

**Prüfbarkeit**

3. Ist jedes Fertigkriterium so formuliert, dass ein **ausführender Agent** es selbst nachweisen kann? Kriterien, die eine menschliche Sichtprüfung verlangen, listest du gesondert auf. Sie sind zulässig, müssen aber als solche gekennzeichnet sein und dürfen später nur GELB erreichen. Ein Kriterium, das Handprüfung verlangt, aber wie ein automatisch prüfbares aussieht, ist ein **BLOCKIERER** — es wird abgehakt werden, ohne erfüllt zu sein.
4. Prüft mindestens ein Prüfschritt das **gebaute, gestartete Artefakt** in der Zielumgebung? Ein grüner Build und grüne Unit-Tests sind kein Nachweis, dass die Anwendung läuft.
5. Wie hoch ist der Anteil der Anwendung, der von automatisierten Tests tatsächlich berührt wird? Nenne die Bereiche, die vollständig ungeprüft bleiben.

**Belege**

6. Enthält `plan.md` Aussagen über das **Verhalten** fremder Bibliotheken? Für jede solche Aussage: Existenz und Signatur einer Funktion sind **kein** Beleg für ihr Verhalten. Verlange ein kurzes Prüfskript gegen die installierte Version und melde ROT, wenn keines vorgesehen ist.
7. Sind alle Abhängigkeiten mit fester Version freigegeben und die Versionsangaben belegt?

**Widerspruch und Erosion**

8. Widersprechen sich die Dokumente? Löse den Widerspruch **nicht** auf — benenne ihn und die betroffenen Stellen.
9. Weicht ein Dokument von der `constitution.md` ab? Zulässig ist nur die ausdrückliche und begründete Abweichung. Stillschweigende Abweichungen meldest du.
10. Ist im Verlauf von Spezifikation zu Plan zu Tasks fachliche Substanz **verlorengegangen**? Vergleiche den Umfang, nicht nur die Formulierungen.

---

## 3. Form

Bericht in drei Blöcken:

* **BLOCKIERER** — Umsetzung darf nicht beginnen. Je Eintrag: Fundstelle(n), Sachverhalt, was zu tun ist.
* **RISIKEN** — Umsetzung möglich, Nacharbeit wahrscheinlich.
* **ABDECKUNGSTABELLE** — je Akzeptanzkriterium eine Zeile: abgedeckt durch welche Aufgabe(n), Nachweisart (automatisch / Handprüfung / kein Nachweis).

Schließe mit einer Zeile: **Umsetzung freigegeben** oder **nicht freigegeben** (welcher Blockierer).

Du machst keine Verbesserungsvorschläge zur Technik und schreibst keine Dokumente um. Der Bericht geht an mich.
