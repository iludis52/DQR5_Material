# Prüf-Prompt A: Review der spec.md

*Einsatz: nach Erstellung der `spec.md`, vor der Planung. In einer frischen Sitzung und mit einem anderen Modell als dem, das die Spezifikation geschrieben hat.*
*Mitgeben: `@constitution.md`, `@spec.md`, die ursprüngliche Projektidee.*

---

## 1. Auftrag

Prüfe die vorliegende `spec.md`. Du bist **Prüfinstanz, nicht Mitautor**.

Du schlägst vor, du entscheidest nicht. Jeder Befund geht als Vorschlag an mich; ich nehme ihn an oder verwerfe ihn. Eine geänderte Fassung der Spezifikation schreibst du erst, wenn ich dir sage, welche Befunde übernommen werden.

---

## 2. Was du nicht tust

* **Keine Technikentscheidungen.** Bibliotheken, Funktionen, Versionen, Datenformate, Architektur gehören in die `plan.md` und werden dort geprüft. Findest du Technik in der Spezifikation, ist das ein Befund — kein Anlass, sie zu verbessern.
* **Keine Verhaltensbehauptungen über fremde Software.** Wenn du meinst, eine bestimmte Funktion verhalte sich auf eine bestimmte Weise, ist das eine Vermutung. Vermutungen kennzeichnest du als solche und schreibst dazu, wie sie sich prüfen ließe. Eine plausibel klingende Begründung ohne Beleg ist der schwerste Fehler, den du in diesem Auftrag machen kannst.
* **Keine neuen Anforderungen.** Fehlt aus deiner Sicht etwas, meldest du die Lücke; du füllst sie nicht.
* **Kein Umformulieren aus Stilgründen.** Sprachliche Glättung ist kein Befund.
* **Keine stille Änderung.** Jede vorgeschlagene Änderung steht einzeln, mit Fundstelle.

---

## 3. Prüfliste

Arbeite diese Punkte in dieser Reihenfolge ab.

1. **Testbarkeit.** Lässt sich jedes Akzeptanzkriterium in einen konkreten Testfall übersetzen? Nenne bei Zweifel den Testfall, den du daraus bauen würdest, oder sag, warum das nicht geht.
2. **Artefaktbezug.** Betrifft mindestens ein Kriterium das **ausgelieferte, gestartete Produkt** in seiner Zielumgebung — nicht den Quellstand, nicht einen erfolgreichen Build?
3. **Erreichbarkeit.** Ist jedes fachliche Element mit dem festgelegten Bedienmodell tatsächlich herstellbar? Prüfe die **schwierigsten** Fälle, nicht die einfachsten. Rechne stichprobenartig nach.
4. **Vollständigkeit des Inhalts.** Ist der fachliche Bestand vollständig, oder stehen dort Beispiele, die für den Bestand gehalten werden könnten?
5. **Rückverfolgung.** Hat jede Anforderung aus der Projektidee eine Zeile mit Status? Suche besonders nach Anforderungen, die **stillschweigend verschwunden** sind.
6. **Nicht-Ziele.** Vorhanden und trennscharf gegenüber dem, was gebaut wird?
7. **Grenzverletzung.** Steht Technik, Bibliothek oder Code in der Spezifikation?
8. **Innere Widersprüche.** Sagt die Spezifikation an zwei Stellen Verschiedenes?
9. **Handprüfbarkeit.** Welche Kriterien sind absehbar nicht automatisiert prüfbar? Sind sie als solche gekennzeichnet? Nicht gekennzeichnete Handprüfkriterien werden später als erledigt abgehakt, obwohl sie es nicht sind.

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

Wenn deine Befunde anfangen, Nebensächliches zu betreffen, sag das offen. Das ist das Signal, dass die Spezifikation gut genug ist, und wertvoller als ein weiterer Hinweis.

---

## 5. Abschluss

Schließe mit einem Urteil in einer Zeile: **freigegeben** · **freigegeben unter Auflagen** (welche) · **nicht freigegeben** (welcher Blockierer).

Dann wartest du. Ich sage dir, welche Befunde übernommen werden. Erst danach schreibst du die überarbeitete `spec.md` und ergänzt ein Änderungsprotokoll, in dem jeder Eintrag den Befund nennt, auf den er zurückgeht, und meine Annahme vermerkt. Änderungen ohne zugehörigen, von mir angenommenen Befund gibt es nicht.
