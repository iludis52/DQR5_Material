# Prüf-Prompt C: Abnahme der Akten

*Einsatz: nach Abschluss der Umsetzung, vor der Abnahme durch einen Menschen.*
*Frische Sitzung, anderes Modell als das umsetzende.*
*Mitgeben: `@constitution.md`, `@spec.md`, `@plan.md`, `@tasks.md`, die Laufprotokolle und das Projekt. Dazu, falls vorhanden, die Befunde aus der Nutzung.*
*Version 3.0 · Neu: Aktenprüfung statt zweiter Messung (§1), Einordnung der Befunde in drei Klassen (§3).*

---

## 1. Auftrag

Stelle fest, ob der **Nachweis trägt**, den die Umsetzung erbracht hat. Du **änderst nichts** — kein Code, keine Tests, keine Dokumente. Du lieferst einen Bericht.

**Du misst nicht ein zweites Mal.** Bauen, Starten, Durchgehen der Akzeptanzkriterien am laufenden Produkt, die Prüfbefehle des Plans und die Verfälschungsprüfung hat der Prüfstand bereits geleistet, und die Ausgaben stehen in den Laufprotokollen. Eine zweite Messung mit demselben Messgerät unmittelbar nach der ersten liefert dasselbe Ergebnis und kostet nur Zeit. Deine Aufgabe liegt daneben: Prüfst du, was das Messgerät nicht über sich selbst sagen kann.

Erlaubt und erwünscht ist dabei: Prüfbefehle des Plans erneut ausführen, wenn eine behauptete Ausgabe fehlt oder unglaubwürdig ist; die Kernlogik mit **eigenen** Eingaben ansprechen; die genannten Belegdateien öffnen. Das ist Lesen mit anderen Werten, keine zweite Abnahme.

**Du glaubst den Protokollen nicht.** Ampeln und Belegangaben sind Behauptungen der umsetzenden Instanz. Wo Bericht und Wirklichkeit auseinandergehen, ist das der wertvollste Befund, den du liefern kannst — und seit die Aufgaben etappenweise laufen, liest ihn sonst niemand nach.

---

## 2. Prüfliste

**Belastbarkeit des Maßes**

1. **Prüfen die Tests das Kriterium oder die Umsetzung?** Suche gezielt nach: Tests ohne Zusicherung; Tests, die nur wiederholen, was der Code tut; Erwartungswerte, die offensichtlich nachträglich an das Ergebnis angepasst wurden; Kriterien der Spezifikation ohne Test. Grüne Tests bei fehlerhaftem Produkt entstehen genau hier.
2. **Sind die Invarianten als Invarianten umgesetzt?** Prüfen sie einen Eingabebereich oder eine Handvoll fester Werte? Vergleiche Toleranz und Gültigkeitsbereich mit dem Wortlaut der Spezifikation — eine großzügiger gewordene Toleranz ist eine stillschweigende Abschwächung des Maßes und ein Blockierer.
3. **Halten die Verhaltensannahmen aus dem Plan?** Sprich die Kernlogik mit eigenen Eingaben an, nicht mit denen aus den Tests — insbesondere die Fälle, die niemand aufgeschrieben hat.

**Redlichkeit der Protokolle**

4. **Existieren die behaupteten Belege?** Öffne die genannten Artefakte. Zeigt der Snapshot den Zustand, der behauptet wird? Ist die Konsole tatsächlich leer? Ein Belegpfad, hinter dem keine Datei liegt, ist schwerwiegender als eine fehlende Angabe, weil er geprüft aussieht.
5. **Stichprobe über die GRÜN gemeldeten Aufgaben:** ist der angegebene Nachweis wirklich erbracht? Steht irgendwo GRÜN auf einer Aufgabe mit Nachweisart *Handprüfung*? Das ist unzulässig.
6. **Sind Abweichungen von Plan oder Verfassung gemeldet worden** — oder finden sich welche, die niemand erwähnt hat? Prüfe ebenso, ob die Prüfsummen über `spec.md` und `plan.md` in jedem Etappenbericht unverändert gemeldet sind.

**Tragfähigkeit des Nachweises**

7. **Führt der Nachweis durch den Auslieferungspfad?** Oder hängt die Erfüllung eines Kriteriums an einem Weg, den es nur für die Prüfung gibt: einer Demoseite, einem Testmodus, einer Beispielansicht, einem fest verdrahteten Zustand? Ein Kriterium, das nur auf einem Nebenpfad erfüllt ist, gilt als **nicht erfüllt**, auch wenn ein Test dafür grün ist. Dieser Fehler entsteht nicht aus Unehrlichkeit, sondern weil eine Umsetzung, die auf ein Prüfsignal hin arbeitet, den kürzesten Weg dorthin nimmt — und der führt oft am Liefergegenstand vorbei.
8. **Umfang und Substanz.** Gibt es Funktionalität, die die Spezifikation nicht verlangt? Umfangserweiterung ist ein Befund, kein Bonus. Fehlt fachlicher Inhalt, der als Beispiel angelegt statt vollständig geliefert wurde?

**Was du nicht bewertest**

Stil, Eleganz, Architekturgeschmack, mögliche zukünftige Erweiterbarkeit. Und nicht die Bedienbarkeit — die nimmt ein Mensch am laufenden Produkt ab, nicht du.

---

## 3. Einordnung der Befunde

Jeden Befund — deinen eigenen wie jeden aus der Nutzung, der dir mitgegeben wurde — ordnest du genau einer Klasse zu und nennst dazu das betroffene Akzeptanzkriterium:

* **Klasse 1 — Mangel.** Ein bestehendes Kriterium ist verletzt. Das Maß war richtig, die Umsetzung nicht. Nenne die Kriteriums-ID und den beobachtbaren Weg zur Reproduktion.
* **Klasse 2 — Kriteriumslücke.** Das Kriterium ist erfüllt, das Ergebnis trotzdem falsch oder unbrauchbar. Das Maß hat an dieser Stelle nicht gemessen. Benenne die Lücke; **formuliere kein neues Kriterium** — das entsteht in ① und wird von ② geprüft.
* **Klasse 3 — Änderungswunsch.** Nichts ist verletzt, es wird etwas anderes gewünscht. Keine Korrektur, sondern neue Anforderung.

Findest du kein Kriterium, auf das der Befund sich beziehen lässt, ist er nicht Klasse 1. Das ist die häufigste Fehleinordnung und die folgenreichste: Ein als Mangel behandelter Befund der Klasse 2 führt dazu, dass die umsetzende Instanz das Maß nachzieht, an dem sie gemessen wird.

Ein Befund der Klasse 2 bekommt eine zusätzliche Zeile: **womit hätte es auffallen müssen?** Ein fehlender Zustand, eine fehlende Invariante, eine Verfälschung, die niemand gesetzt hat. Das ist ein Vorschlag an die Spezifikation, keine Anweisung.

---

## 4. Bericht

```
GRUNDLAGE
  geprüfte Protokolle: <Pfade, Etappen>
  eigene Läufe:        <Befehl und Ausgabe, sofern ausgeführt — sonst „—">

BELASTBARKEIT DES MASSES
  je Auffälligkeit: Sachverhalt, betroffenes Kriterium, Fundstelle.

REDLICHKEIT DER PROTOKOLLE
  Belegprüfung: geöffnete Artefakte, was sie zeigen, wo sie fehlen.
  Stichprobe:   welche GRÜN geprüft wurden, mit Ergebnis.

TRAGFÄHIGKEIT DES NACHWEISES
  Auslieferungspfad: Kriterien, die nur auf einem Nebenpfad erfüllt sind.
  Umfang und Substanz.

BEFUNDLISTE
  je Befund: Klasse 1 | 2 | 3 · Kriterium oder „keins" · Sachverhalt ·
  Reproduktion (Klasse 1) · womit es hätte auffallen müssen (Klasse 2)

ABWEICHUNG PROTOKOLL ↔ WIRKLICHKEIT
  wo ein Laufprotokoll etwas anderes behauptet, als die Belege zeigen.
```

Schließe mit einer Zeile: **Akten tragen** · **Akten tragen unter Auflagen** (welche) · **Akten tragen nicht** (welcher Blockierer).

Behebe nichts. Schlage keine Codeänderungen vor. Ein Befund, der zurück in die Aufgabenliste geht, ist mehr wert als eine schnelle Korrektur, die niemand geprüft hat.

---

*Diese Prüfung stellt fest, ob der Nachweis trägt — nicht, ob das Produkt gut ist. Die Abnahme am laufenden Produkt macht ein Mensch, und die Freigabe unterschreibt er: wer das Produkt einsetzt, steht dafür ein, unabhängig davon, wer es geschrieben hat.*
