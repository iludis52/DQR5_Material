# Prüf-Prompt C: Abnahme

*Einsatz: nach Abschluss der Umsetzung, vor der Freigabe.*
*Frische Sitzung, anderes Modell als das umsetzende.*
*Mitgeben: `@constitution.md`, `@spec.md`, `@plan.md`, `@tasks.md` und das Projekt.*
*Version 2.0 · Neu: Bedienung der laufenden Anwendung (§2.3), Auslieferungspfad und Verfälschungsprobe (§3), erweiterter Bericht (§4).*

---

## 1. Auftrag

Stelle fest, ob das entstandene Produkt die Spezifikation erfüllt. Du **änderst nichts** — kein Code, keine Tests, keine Dokumente. Du lieferst einen Bericht.

Eine Ausnahme, und nur diese: für die Verfälschungsprobe nach §3.10 darfst du vorübergehend Code verändern. Du nimmst jede Verfälschung zurück und weist das im Bericht nach.

**Du glaubst der Dokumentation nicht.** Die Statusfelder in `tasks.md` sind Behauptungen der umsetzenden Instanz. Deine Aufgabe ist, sie gegen das tatsächliche Ergebnis zu halten. Wo Bericht und Artefakt auseinandergehen, ist das der wichtigste Befund, den du liefern kannst.

---

## 2. Reihenfolge

**Zuerst das Artefakt, dann der Code.** Nicht umgekehrt — wer mit dem Quelltext beginnt, liest sich in die Absicht ein und übersieht, dass das Ausgelieferte etwas anderes tut.

1. **Bauen und starten.** Führe den Bauvorgang aus und rufe das Ergebnis so auf, wie es laut Plan ausgeliefert wird — im vorgesehenen Pfad, in der vorgesehenen Umgebung. Lädt alles? Stylesheets, Skripte, Datendateien? Fehler in der Browserkonsole? Ein fehlerfreier Bauvorgang sagt darüber nichts.
2. **Akzeptanzkriterien durchgehen.** Jedes Kriterium der Spezifikation einzeln, am laufenden Produkt. Wo eine browsergestützte Prüfung möglich ist, führe sie durch: aufrufen, bedienen, beobachten.
3. **Die Zustände selbst herbeiführen.** Verlass dich nicht darauf, dass ein Fehler- oder Ladezustand von allein auftritt. Führe ihn mit dem in `plan.md` §3.8 festgelegten Werkzeug herbei: Hintergrundaufrufe abfangen, verzögern, scheitern lassen; leere und übergroße Eingaben setzen; die Ränder des zulässigen Bereichs ansteuern. Genau hier liegen die Mängel, die jede Nutzerin sofort sieht und kein Test bemerkt.
4. **Erst danach in den Code sehen**, und nur dort, wo die Schritte 1 bis 3 eine Auffälligkeit ergeben haben oder wo Abschnitt 3 es verlangt.

---

## 3. Prüfliste

**Erfüllung**

1. Je Akzeptanzkriterium: **erfüllt / nicht erfüllt / nicht prüfbar**, mit dem Beleg, wie du es festgestellt hast. Ohne Beleg kein Urteil. Führe Verhalten, Invarianten und Zustände getrennt auf.
2. Gibt es Funktionalität, die die Spezifikation **nicht** verlangt? Umfangserweiterung ist ein Befund, kein Bonus.
3. Fehlt Substanz, die in der Spezifikation steht — insbesondere fachlicher Inhalt, der als Beispiel angelegt statt vollständig geliefert wurde?

**Belastbarkeit der Tests**

4. Laufen die Tests? Wörtliche Ausgabe.
5. **Prüfen die Tests das Kriterium oder die Umsetzung?** Suche gezielt nach: Tests ohne Zusicherung; Tests, die nur wiederholen, was der Code tut; Tests, deren Erwartungswert offensichtlich nachträglich an das Ergebnis angepasst wurde; Kriterien der Spezifikation, zu denen es keinen Test gibt. Grüne Tests bei fehlerhaftem Produkt entstehen genau hier.
6. **Sind die Invarianten als Invarianten umgesetzt?** Prüfe, ob die Umsetzung sie über einen Eingabebereich prüft oder an einer Handvoll fester Werte. Vergleiche Toleranz und Gültigkeitsbereich mit dem Wortlaut der Spezifikation — eine großzügiger gewordene Toleranz ist eine stillschweigende Abschwächung des Maßes und ein Blockierer.
7. Halten die **Verhaltensannahmen** aus dem Plan im gebauten Zustand? Prüfe die Kernlogik mit eigenen Eingaben, nicht mit denen aus den Tests — insbesondere die Fälle, die niemand aufgeschrieben hat.

**Redlichkeit des Berichts**

8. Stichprobe über die GRÜN gemeldeten Aufgaben: ist der angegebene Nachweis wirklich erbracht?
9. **Existieren die Belege, die `tasks.md` behauptet?** Öffne die genannten Artefakte. Zeigt der Snapshot den Zustand, der behauptet wird? Ist die Konsole tatsächlich leer? Ein Belegpfad, hinter dem keine Datei liegt, ist schwerwiegender als eine fehlende Angabe, weil er geprüft aussieht.
10. Steht bei Aufgaben mit Nachweisart *Handprüfung* GRÜN? Das ist unzulässig und ein Befund.
11. Sind Abweichungen von Plan oder Verfassung gemeldet worden, oder finden sich welche, die niemand erwähnt hat?

**Tragfähigkeit des Nachweises**

12. **Führt der Nachweis durch den Auslieferungspfad?** Prüfe, ob die Erfüllung eines Kriteriums an dem Weg hängt, den auch die Nutzenden gehen — oder an einem Nebenpfad, den es nur für die Prüfung gibt: einer Demoseite, einem Testmodus, einer Beispielansicht, einem fest verdrahteten Zustand, einer Abkürzung, die im ausgelieferten Artefakt niemand erreicht. Ein Kriterium, das nur auf einem Nebenpfad erfüllt ist, gilt als **nicht erfüllt**, auch wenn ein Test dafür grün ist. Dieser Fehler entsteht nicht aus Unehrlichkeit, sondern weil eine Umsetzung, die auf ein Prüfsignal hin arbeitet, den kürzesten Weg zu diesem Signal nimmt — und der führt oft am eigentlichen Liefergegenstand vorbei.
13. **Hält der Nachweis einer Verfälschung stand?** Wähle zwei bis vier Stellen im fachlichen Kern — dort, wo gerechnet, umgeformt oder entschieden wird. Setze je Stelle eine einzelne, plausible Verfälschung: ein Vergleichsoperator umgedreht, ein Vorzeichen getauscht, ein Faktor entfernt, eine Bedingung invertiert. Lass danach die Prüfbefehle laufen.
    * Schlägt mindestens ein Prüfmittel an: der Nachweis trägt an dieser Stelle.
    * Schlägt keines an: der Befund lautet nicht „ein Test fehlt", sondern **die Erfüllungstabelle ist an dieser Stelle unbelegt**. Vermerke, welche Kriterien betroffen sind.
    
    Nimm jede Verfälschung unmittelbar zurück und weise mit einem sauberen Lauf nach, dass der Ausgangszustand wiederhergestellt ist. Sieht `plan.md` §3.8 einen eigenen Verfälschungsbefehl vor, nutze ihn statt der Handarbeit und berichte seine Ausgabe.

**Was du nicht bewertest**

Stil, Eleganz, Architekturgeschmack, mögliche zukünftige Erweiterbarkeit. Du prüfst Erfüllung, Nachweis und Einhaltung der Grenzen — sonst nichts.

---

## 4. Bericht

```
ZUSTAND DES ARTEFAKTS
  gebaut:      <Befehl, Ergebnis>
  gestartet:   <wie aufgerufen, was passiert>
  Auffälliges: <Konsole, fehlende Ressourcen, …>

ERFÜLLUNGSTABELLE
  je Akzeptanzkriterium: Gruppe · Urteil · Beleg · Fundstelle

TRAGFÄHIGKEIT DES NACHWEISES
  Auslieferungspfad: Kriterien, die nur auf einem Nebenpfad erfüllt sind.
  Verfälschungsprobe: je geprüfter Stelle die gesetzte Verfälschung, ob ein
  Prüfmittel angeschlagen hat, und die Bestätigung der Rücknahme.

BLOCKIERER
  Freigabe nicht möglich. Je Eintrag: Sachverhalt, Beleg, betroffenes Kriterium.

BEFUNDE
  Nacharbeit nötig oder empfohlen.

ABWEICHUNG BERICHT ↔ WIRKLICHKEIT
  wo tasks.md etwas anderes behauptet als das Produkt zeigt.
```

Schließe mit einer Zeile: **abgenommen** · **abgenommen unter Auflagen** (welche) · **nicht abgenommen** (welcher Blockierer).

Behebe nichts. Schlage keine Codeänderungen vor. Ein Befund, der zurück in die Aufgabenliste geht, ist mehr wert als eine schnelle Korrektur, die niemand geprüft hat.

---

*Diese Prüfung ist Unterstützung, kein Ersatz. Die Freigabe unterschreibt ein Mensch — wer das Produkt einsetzt, steht dafür ein, unabhängig davon, wer es geschrieben hat.*
