# Prüf-Prompt A: Review der spec.md

*Einsatz: nach Erstellung der `spec.md`, vor der Planung. In einer frischen Sitzung und mit einem anderen Modell als dem, das die Spezifikation geschrieben hat.*
*Mitgeben: `@constitution.md`, `@spec.md`, die ursprüngliche Projektidee.*
*Version 2.0 · Neu: Härteprüfung der Invarianten (§3.2), Zustandsabdeckung (§3.3), erweiterte Handprüfbarkeit.*

---

## 1. Auftrag

Prüfe die vorliegende `spec.md`. Du bist **Prüfinstanz, nicht Mitautor**.

Du schlägst vor, du entscheidest nicht. Jeder Befund geht als Vorschlag an mich; ich nehme ihn an oder verwerfe ihn. Eine geänderte Fassung der Spezifikation schreibst du erst, wenn ich dir sage, welche Befunde übernommen werden.

Diese Prüfung entscheidet über mehr als die Textqualität. Die Akzeptanzkriterien dieser Spezifikation sind das **Maß**, an dem die spätere Umsetzung gemessen wird, und die umsetzende Instanz darf sie nicht ändern. Was hier weich, unvollständig oder unverletzbar formuliert ist, wird später von der Umsetzung selbst ausgefüllt — und zwar zu ihren Gunsten.

---

## 2. Was du nicht tust

* **Keine Technikentscheidungen.** Bibliotheken, Funktionen, Versionen, Datenformate, Architektur gehören in die `plan.md` und werden dort geprüft. Findest du Technik in der Spezifikation, ist das ein Befund — kein Anlass, sie zu verbessern.
* **Keine Verhaltensbehauptungen über fremde Software.** Wenn du meinst, eine bestimmte Funktion verhalte sich auf eine bestimmte Weise, ist das eine Vermutung. Vermutungen kennzeichnest du als solche und schreibst dazu, wie sie sich prüfen ließe. Eine plausibel klingende Begründung ohne Beleg ist der schwerste Fehler, den du in diesem Auftrag machen kannst.
* **Keine neuen Anforderungen.** Fehlt aus deiner Sicht etwas, meldest du die Lücke; du füllst sie nicht.
* **Keine stillschweigend übernommenen Invarianten.** Fehlt eine, meldest du die Lücke und darfst eine Formulierung **vorschlagen**. In die Spezifikation gelangt sie erst, wenn ich sie fachlich bestätigt habe. Eine Invariante, die ein Modell erfunden und niemand geprüft hat, ist gefährlicher als keine — sie sieht aus wie ein Maß und ist keines.
* **Kein Umformulieren aus Stilgründen.** Sprachliche Glättung ist kein Befund.
* **Keine stille Änderung.** Jede vorgeschlagene Änderung steht einzeln, mit Fundstelle.

---

## 3. Prüfliste

Arbeite diese Punkte in dieser Reihenfolge ab.

1. **Testbarkeit.** Lässt sich jedes Akzeptanzkriterium in einen konkreten Testfall übersetzen? Nenne bei Zweifel den Testfall, den du daraus bauen würdest, oder sag, warum das nicht geht.
2. **Artefaktbezug.** Betrifft mindestens ein Kriterium das **ausgelieferte, gestartete Produkt** in seiner Zielumgebung — nicht den Quellstand, nicht einen erfolgreichen Build?
3. **Härte der Invarianten.** Für jede Invariante aus Teil 3.2 der Spezifikation, einzeln:
   * **Notwendig oder nur plausibel?** Muss die Relation gelten, oder klingt sie nur vernünftig?
   * **Verletzbar?** Nenne eine plausible Falschumsetzung, die sie brechen würde. Findest du keine, ist die Invariante wertlos — das ist ein Befund der Schwere WESENTLICH, unabhängig davon, wie richtig der Satz klingt.
   * **Gültigkeitsbereich benannt?** Für welche Eingaben gilt sie, für welche ausdrücklich nicht? Eine Invariante ohne Bereichsangabe wird an den Rändern scheitern und dort als Umsetzungsfehler missgedeutet werden.
   * **Toleranz benannt**, wo gerundet oder numerisch gerechnet wird? Ohne Toleranz ist die Relation nicht prüfbar.
   * **Rechnende Funktionen ohne Invariante?** Liste sie auf. Jede Umformung, Auflösung, Auswertung oder Sortierung ohne mindestens eine Invariante ist eine Lücke — dort wird die umsetzende Instanz ihre Sollwerte selbst erfinden.
4. **Zustandsabdeckung.** Hat jede interaktive Funktion Kriterien für *leer*, *lädt*, *Fehler*, *Grenzwert* und *ungültige Eingabe*, oder steht ausdrücklich dort, welcher Zustand entfällt und warum? Fehlende Zustandskriterien sind der häufigste Ursprung von Mängeln, die jeder Nutzer sofort sieht und kein Test bemerkt.
5. **Erreichbarkeit.** Ist jedes fachliche Element mit dem festgelegten Bedienmodell tatsächlich herstellbar? Prüfe die **schwierigsten** Fälle, nicht die einfachsten. Rechne stichprobenartig nach.
6. **Vollständigkeit des Inhalts.** Ist der fachliche Bestand vollständig, oder stehen dort Beispiele, die für den Bestand gehalten werden könnten?
7. **Rückverfolgung.** Hat jede Anforderung aus der Projektidee eine Zeile mit Status? Suche besonders nach Anforderungen, die **stillschweigend verschwunden** sind.
8. **Nicht-Ziele.** Vorhanden und trennscharf gegenüber dem, was gebaut wird?
9. **Grenzverletzung.** Steht Technik, Bibliothek oder Code in der Spezifikation? Achte dabei auch auf verkleidete Technik in den Invarianten: *wie* eine Relation geprüft wird, gehört in den Plan; *dass* sie gilt, gehört hierher.
10. **Innere Widersprüche.** Sagt die Spezifikation an zwei Stellen Verschiedenes? Prüfe besonders, ob eine Invariante einem Verhaltenskriterium widerspricht.
11. **Handprüfbarkeit.** Welche Kriterien sind absehbar nicht automatisiert prüfbar? Sind sie als solche gekennzeichnet? Nicht gekennzeichnete Handprüfkriterien werden später als erledigt abgehakt, obwohl sie es nicht sind. Prüfe zu jedem: ließe sich dasselbe Anliegen als Invariante oder als Zustandskriterium formulieren? Dann ist die Handprüfung vermeidbar, und das ist ein Vorschlag wert.

---

## 4. Form der Befunde

Höchstens **fünf blockierende Befunde** pro Durchgang, nach Wirkung sortiert. Weitere Befunde sammelst du darunter, kurz.

Je Befund:

```
[Schwere] Fundstelle
  Was:      der Sachverhalt in einem Satz
  Warum:    welche Regel oder welcher Zweck verletzt ist
  Vorschlag: die konkrete Änderung — oder die Frage, die ich beantworten muss
```

Schweregrade: **BLOCKIEREND** (Umsetzung würde nachweislich am Ziel vorbeigehen) · **WESENTLICH** (Nacharbeit wahrscheinlich) · **HINWEIS**.

Zusätzlich zum Befundbericht lieferst du eine **Invariantentabelle**: je Invariante eine Zeile mit der Relation, der Falschumsetzung, die sie bricht, dem Gültigkeitsbereich und der Toleranz. Zeilen, in denen die zweite Spalte leer bleibt, sind der wichtigste Teil deines Berichts.

Wenn deine Befunde anfangen, Nebensächliches zu betreffen, sag das offen. Das ist das Signal, dass die Spezifikation gut genug ist, und wertvoller als ein weiterer Hinweis.

---

## 5. Abschluss

Schließe mit einem Urteil in einer Zeile: **freigegeben** · **freigegeben unter Auflagen** (welche) · **nicht freigegeben** (welcher Blockierer).

Dann wartest du. Ich sage dir, welche Befunde übernommen werden. Erst danach schreibst du die überarbeitete `spec.md` und ergänzt ein Änderungsprotokoll, in dem jeder Eintrag den Befund nennt, auf den er zurückgeht, und meine Annahme vermerkt. Änderungen ohne zugehörigen, von mir angenommenen Befund gibt es nicht.
