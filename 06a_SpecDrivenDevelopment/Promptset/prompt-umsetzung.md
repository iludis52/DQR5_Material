# Prompt: Umsetzung

*Einsatz: je Aufgabe eine Sitzung, nach Freigabe durch Prüfstelle B.*
*Mitgeben: `@constitution.md`, `@spec.md`, `@plan.md`, `@tasks.md` und die Nummer der Aufgabe.*
*Version 2.0 · Neu: fünfte und sechste Verschärfung (§3), Belegzeile im Bericht (§4).*

---

## 1. Auftrag

Setze **genau eine** Aufgabe aus `tasks.md` um: **T\<Nr\>**.

Nicht die folgende, nicht „gleich mit", auch wenn es naheliegt. Eine Aufgabe, ein Bericht, Ende.

Es gilt die `constitution.md`, insbesondere §2 (Annahmen und Rückfragen), §3 (Einfachheit), §4 (chirurgische Änderungen), §5 (Verifikation, Ampel, Abbruch nach drei Versuchen), §6 (keine Erfindungen) und §8 (Grenzen). Lies sie, bevor du beginnst. Die folgenden Abschnitte wiederholen sie nicht — sie verschärfen sie für diese Phase.

---

## 2. Vor Beginn

Sag in einem Satz, was du tun wirst und woran du es messen wirst. Das Kriterium steht in der Aufgabe; du übernimmst es **wörtlich**, du formulierst es nicht neu.

Ist die Aufgabe unklar, widersprüchlich oder ihr Kriterium nicht erfüllbar: halte an und melde ROT. Nicht raten, nicht sinngemäß umsetzen, nicht das Kriterium anpassen.

---

## 3. Sechs Verschärfungen für diese Phase

**Kein Test wird geändert, damit er grün wird.** Schlägt ein Test fehl, ist entweder die Umsetzung falsch oder das Kriterium — beides meldest du, keines behebst du am Test. Ist ein Test grün, der laut Aufgabe fehlschlagen muss, ist das ein Befund und kein Erfolg.

**Kein Kriterium wird umformuliert, abgeschwächt oder für erfüllt erklärt, weil es sich nicht prüfen ließ.** Dafür gibt es GELB.

**Das Maß fasst du nicht an.** `spec.md` und die Abschnitte §3.8 und §3.9 der `plan.md` sind in dieser Sitzung read-only — Akzeptanzkriterien, Invarianten mit ihren Toleranzen und Gültigkeitsbereichen, Prüfbefehle, Nachweistabelle. Auch nicht „nur die Toleranz ein bisschen", auch nicht mit Begründung im Bericht. Hältst du eine Festlegung für falsch, meldest du sie als Befund und arbeitest mit ihr weiter oder meldest ROT. Der Grund ist einfach: Wer das Maß ändern darf, an dem er gemessen wird, wird immer bestehen.

**Aufgaben mit Nachweisart *Handprüfung* enden bei dir immer GELB.** Du kannst nicht von Hand prüfen. Beschreibe stattdessen, was ein Mensch nachsehen muss.

**Kein Ergebnis ohne Ausgabe.** „Tests grün" ist eine Behauptung. Die wörtliche Ausgabe des Prüfbefehls ist ein Nachweis. Behauptungen ohne Ausgabe gelten als nicht nachgewiesen.

**Bei Nachweisart *browsergestützt* endest du an der laufenden Anwendung, nicht am Testbericht.** Starte sie wie in `plan.md` §3.5 vorgesehen, bediene sie mit dem in §3.8 festgelegten Werkzeug entlang des Szenarios der Aufgabe, und lege die Artefakte am dort genannten Ort ab. Der Bericht nennt ihre Pfade und zitiert die Browserkonsole. Eine leere Fehlerkonsole ist Teil des Nachweises; Meldungen, die du für unbedeutend hältst, zitierst du trotzdem und sagst dazu, warum du sie für unbedeutend hältst. Ohne Artefakte gilt die Aufgabe als nicht nachgewiesen — GELB, nicht GRÜN.

---

## 4. Bericht

Am Ende genau dieses Format:

```
T<Nr> — <Titel>
Status:        GRÜN | GELB | ROT
Kriterium:     <wörtlich aus tasks.md>
Prüfschritt:   <ausgeführter Befehl oder Prüfhandlung>
Ergebnis:      <Ausgabe, wörtlich, gern gekürzt>
Belege:        <Pfade der erzeugten Artefakte; Browserkonsole; Ergebnis der
               Verfälschungsprüfung, sofern die Aufgabe eine verlangt — sonst „—">
Dateien:       <geändert / neu>
Bei GELB:      warum nicht nachgewiesen, was ein Mensch prüfen muss
Bei ROT:       der Blockierer, in einem Satz
Abweichungen:  von Plan oder Verfassung — mit Begründung, sonst „—"
Nicht geplant: Entscheidungen, die du treffen musstest, weil der Plan
               schwieg — sonst „—"
Nebenbefunde:  aufgefallen, nicht bearbeitet — sonst „—"
```

Dann trägst du `Status`, `Nachweis` und `Belege` in die Aufgabe in `tasks.md` ein. Das ist die **einzige** Änderung, die du an `tasks.md` vornimmst.

**Überlebt eine Verfälschung, ist die Aufgabe nicht fertig.** Verlangt das Fertigkriterium eine Verfälschungsprüfung und meldet diese eine überlebende Verfälschung, lautet der Status GELB mit dem Vermerk, welche Verfälschung unbemerkt blieb — auch wenn alle Tests grün sind. Nimm die Verfälschung anschließend zurück und weise das nach.

**GELB ist kein Misserfolg.** Es ist die ehrliche Aussage „umgesetzt, aber nicht belegt" und für die nächste Instanz mehr wert als ein GRÜN, das nicht trägt.
