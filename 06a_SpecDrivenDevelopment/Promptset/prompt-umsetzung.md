# Prompt: Umsetzung

*Einsatz: je Etappe ein Lauf, nach Freigabe durch Prüfstelle B.*
*Mitgeben: `@constitution.md`, `@spec.md`, `@plan.md`, `@tasks.md` und die Etappe — als Name oder als Aufgabenintervall.*
*Version 3.1 · Etappenlauf statt Einzelaufgabe. Herleitung und Projekteinrichtung stehen in der Übersicht, nicht hier.*

---

## 1. Auftrag

Setze **eine Etappe** aus `tasks.md` um: alle Aufgaben, die zu ihr gehören, in der Reihenfolge aus dem Feld `Hängt ab von`.

Nicht die nächste Etappe, nicht „gleich mit". Innerhalb der Etappe hältst du nicht an. Keine Aufgabe wird übersprungen, mit einer anderen zusammengezogen oder vorgezogen. Was außerhalb der Etappe liegt, fasst du nicht an — auch nicht, wenn dir dort etwas auffällt. Dafür gibt es das Feld `Nebenbefunde`.

Es gilt die `constitution.md`, insbesondere §2 bis §6 und §8. Lies sie, bevor du beginnst. Die folgenden Abschnitte wiederholen sie nicht — sie verschärfen sie für diese Phase.

---

## 2. Vor Beginn

1. **Maß sichern.** Prüfsumme über `spec.md` und über `plan.md` bilden und notieren. Am Ende des Laufs erneut bilden. Weichen sie ab, ist das ein Blockierer.
2. **Etappe auflisten.** Je Aufgabe eine Zeile: Nummer, Titel, Nachweisart, Fertigkriterium **wörtlich**. Du übernimmst das Kriterium, du formulierst es nicht neu.
3. **Laufprotokoll anlegen** — am Ablageort aus `plan.md` §3.8, sonst unter `lauf/`.
4. **Vorbedingungen prüfen.** Zeigt eine Abhängigkeit aus der Etappe heraus auf eine Aufgabe, die nicht abgeschlossen ist, beginnst du nicht.

Ist der Etappenumfang unklar, widersprüchlich oder unvollständig: anhalten und ROT melden, bevor du beginnst. Nicht raten, nicht sinngemäß zuschneiden. Unklarheiten an einer **einzelnen** Aufgabe halten dagegen nicht den ganzen Lauf an — sie folgen §5.

---

## 3. Der Takt je Aufgabe

Für jede Aufgabe, immer in dieser Folge:

1. Fertigkriterium wörtlich ins Laufprotokoll übernehmen.
2. Umsetzen — chirurgisch, nach Verfassung §4.
3. Prüfschritt ausführen: den Befehl aus dem Fertigkriterium, bei Nachweisart *browsergestützt* zusätzlich den Lauf an der laufenden Anwendung nach §4.
4. Die **wörtliche Ausgabe** ins Protokoll schreiben, gern gekürzt, nie zusammengefasst.
5. Ampel setzen, Eintrag nach §6 vervollständigen.
6. Kontrollpunkt setzen: ein Commit je Aufgabe, Botschaft `T<Nr> — <Titel> — <Ampel>`, ausdrücklich erlaubt nach Verfassung §8. Kein Push, keine mehreren Aufgaben in einem Commit.
7. Nächste Aufgabe. Ohne Zwischenbericht, ohne Rückfrage, ohne Zusammenfassung des bisher Erreichten.

**`tasks.md` wird nicht verändert** — weder Status noch Nachweis noch Belege. Sie ist Maß, nicht Logbuch.

---

## 4. Sieben Verschärfungen für diese Phase

**Kein Test wird geändert, damit er grün wird.** Schlägt ein Test fehl, ist entweder die Umsetzung falsch oder das Kriterium — beides meldest du, keines behebst du am Test. Ist ein Test grün, der laut Aufgabe fehlschlagen muss, ist das ein Befund und kein Erfolg.

**Kein Kriterium wird umformuliert, abgeschwächt oder für erfüllt erklärt, weil es sich nicht prüfen ließ.** Dafür gibt es GELB.

**Das Maß fasst du nicht an.** `spec.md` und die Abschnitte §3.8 und §3.9 der `plan.md` sind in diesem Lauf read-only — Akzeptanzkriterien, Invarianten mit Toleranzen und Gültigkeitsbereichen, Prüfbefehle, Nachweistabelle. Auch nicht „nur die Toleranz ein bisschen", auch nicht mit Begründung im Bericht. Hältst du eine Festlegung für falsch, meldest du sie als Befund und arbeitest mit ihr weiter oder meldest ROT. Der Grund: Wer das Maß ändern darf, an dem er gemessen wird, wird immer bestehen.

**Aufgaben mit Nachweisart *Handprüfung* enden bei dir immer GELB.** Du kannst nicht von Hand prüfen. Beschreibe stattdessen, was ein Mensch nachsehen muss. Der Lauf geht danach weiter.

**Kein Ergebnis ohne Ausgabe.** „Tests grün" ist eine Behauptung, die wörtliche Ausgabe des Prüfbefehls ist ein Nachweis. Das gilt für jede Aufgabe der Etappe, nicht nur für die letzte.

**Bei Nachweisart *browsergestützt* endest du an der laufenden Anwendung, nicht am Testbericht.** Starte sie nach `plan.md` §3.5, bediene sie mit dem in §3.8 festgelegten Werkzeug entlang des Szenarios der Aufgabe, lege die Artefakte am dort genannten Ort ab. Das Protokoll nennt ihre Pfade und zitiert die Browserkonsole; eine leere Fehlerkonsole ist Teil des Nachweises. Meldungen, die du für unbedeutend hältst, zitierst du trotzdem und sagst dazu, warum. Ohne Artefakte gilt die Aufgabe als nicht nachgewiesen — GELB, nicht GRÜN.

**Ein Befund hält den Lauf nicht an; ein Blockierer schon.** Ein Befund wird protokolliert, bekommt seine Ampel, die Etappe läuft weiter. Ein Blockierer nach §5 beendet den Lauf sofort. Ein weitergereichter Blockierer verdirbt alles Folgende, ein abgebrochener Befund kostet den halben Nutzen dieser Betriebsart. Wiederholt sich ein Befund, schreibst du beim zweiten Mal „wie T\<Nr\>" und arbeitest weiter — im Etappenbericht steht er einmal, mit allen betroffenen Aufgaben.

---

## 5. Abbruchbedingungen

Der Lauf läuft, bis die Etappe fertig ist — **es sei denn**, eine dieser Bedingungen tritt ein. Die Liste ist abschließend: nichts anderes berechtigt zum Anhalten, alles hier Genannte verpflichtet dazu.

* Eine Aufgabe endet **ROT**.
* Drei erfolglose Korrekturversuche an derselben Aufgabe (Verfassung §5).
* Eine **Verfälschung überlebt**, wo das Fertigkriterium eine Verfälschungsprüfung verlangt. Nimm sie zurück, weise das nach, beende den Lauf.
* Das Kriterium ließe sich nur erfüllen, indem das **Maß geändert** wird.
* Ein bestehender **Test müsste geändert** werden, damit die Aufgabe grün wird.
* Eine **nicht geplante Entscheidung** ist nötig, deren Wirkung über die Aufgabe hinausreicht — Datenformat, Schnittstelle, Abhängigkeit, Struktur. Kleine Entscheidungen im Inneren einer Aufgabe triffst du selbst und notierst sie unter `Nicht geplant`.
* Die **Prüfsummen** aus §2 stimmen nicht mehr.
* Eine **Vorbedingung** aus einer anderen Etappe fehlt.

Ausdrücklich **kein** Grund anzuhalten: eine Handprüfung, ein GELB, ein Nebenbefund, eine Abweichung, die du begründen kannst.

**Bei Abbruch:** Zustand sichern, Kontrollpunkt setzen, Protokoll abschließen, Etappenbericht bis zur Abbruchstelle schreiben. Die restlichen Aufgaben bleiben unbearbeitet — auch die, die du „noch schnell" könntest.

---

## 6. Laufprotokoll

Je Aufgabe genau dieser Eintrag:

```
T<Nr> — <Titel>
Status:        GRÜN | GELB | ROT
Kriterium:     <wörtlich aus tasks.md>
Prüfschritt:   <ausgeführter Befehl oder Prüfhandlung>
Ergebnis:      <Ausgabe, wörtlich, gern gekürzt>
Belege:        <Pfade der erzeugten Artefakte; Browserkonsole; Ergebnis der
               Verfälschungsprüfung, sofern die Aufgabe eine verlangt — sonst „—">
Dateien:       <geändert / neu>
Kontrollpunkt: <Commit>
Bei GELB:      warum nicht nachgewiesen, was ein Mensch prüfen muss
Bei ROT:       der Blockierer, in einem Satz
Abweichungen:  von Plan oder Verfassung — mit Begründung, sonst „—"
Nicht geplant: Entscheidungen, die du treffen musstest, weil der Plan
               schwieg — sonst „—"
Nebenbefunde:  aufgefallen, nicht bearbeitet — sonst „—"
```

**GELB ist kein Misserfolg.** Es ist die ehrliche Aussage „umgesetzt, aber nicht belegt" und für die nächste Instanz mehr wert als ein GRÜN, das nicht trägt.

---

## 7. Etappenbericht

Am Ende des Laufs, genau dieses Format — das Einzige, was ein Mensch zu lesen bekommt:

```
Etappe <Name oder Intervall> — <n> Aufgaben
Lauf:           vollständig | abgebrochen bei T<Nr>
Ampelbilanz:    GRÜN <n> · GELB <n> · ROT <n> · unbearbeitet <n>
Je Aufgabe:     T<Nr> <Ampel> · T<Nr> <Ampel> · …
Maßprüfung:     Prüfsummen spec.md und plan.md vor und nach dem Lauf gleich?
                ja | NEIN — dann welche Datei
Muster:         Befunde, die mehr als einmal auftraten, mit allen betroffenen
                Aufgaben — sonst „—"
Handprüfung:    Aufgaben, die auf einen Menschen warten, je Zeile mit dem, was
                er nachsehen muss — sonst „—"
Blockierer:     Grund des Abbruchs, in einem Satz — sonst „—"
Nicht geplant:  Entscheidungen ohne Deckung im Plan, gesammelt — sonst „—"
Nebenbefunde:   aufgefallen, nicht bearbeitet — sonst „—"
Empfehlung:     weiter mit <Etappe> | Halt — <was ein Mensch entscheiden muss>
Protokoll:      <Pfad>
Kontrollpunkte: <erster Commit> … <letzter Commit>
```

Der Bericht **fasst nicht zusammen, was gut lief**. Er nennt Zahlen, Abweichungen und das, was Aufmerksamkeit braucht. Eine Etappe ohne Auffälligkeiten ist zehn Zeilen lang.
