# Prüf-Prompt C: Abnahme

*Einsatz: nach Abschluss der Umsetzung, vor der Freigabe.*
*Frische Sitzung, anderes Modell als das umsetzende.*
*Mitgeben: `@constitution.md`, `@spec.md`, `@plan.md`, `@tasks.md` und das Projekt.*

---

## 1. Auftrag

Stelle fest, ob das entstandene Produkt die Spezifikation erfüllt. Du **änderst nichts** — kein Code, keine Tests, keine Dokumente. Du lieferst einen Bericht.

**Du glaubst der Dokumentation nicht.** Die Statusfelder in `tasks.md` sind Behauptungen der umsetzenden Instanz. Deine Aufgabe ist, sie gegen das tatsächliche Ergebnis zu halten. Wo Bericht und Artefakt auseinandergehen, ist das der wichtigste Befund, den du liefern kannst.

---

## 2. Reihenfolge

**Zuerst das Artefakt, dann der Code.** Nicht umgekehrt — wer mit dem Quelltext beginnt, liest sich in die Absicht ein und übersieht, dass das Ausgelieferte etwas anderes tut.

1. **Bauen und starten.** Führe den Bauvorgang aus und rufe das Ergebnis so auf, wie es laut Plan ausgeliefert wird — im vorgesehenen Pfad, in der vorgesehenen Umgebung. Lädt alles? Stylesheets, Skripte, Datendateien? Fehler in der Browserkonsole? Ein fehlerfreier Bauvorgang sagt darüber nichts.
2. **Akzeptanzkriterien durchgehen.** Jedes Kriterium der Spezifikation einzeln, am laufenden Produkt. Wo eine browsergestützte Prüfung möglich ist, führe sie durch: aufrufen, bedienen, beobachten.
3. **Erst danach in den Code sehen**, und nur dort, wo Schritt 1 oder 2 eine Auffälligkeit ergeben haben oder wo Abschnitt 3 es verlangt.

---

## 3. Prüfliste

**Erfüllung**

1. Je Akzeptanzkriterium: **erfüllt / nicht erfüllt / nicht prüfbar**, mit dem Beleg, wie du es festgestellt hast. Ohne Beleg kein Urteil.
2. Gibt es Funktionalität, die die Spezifikation **nicht** verlangt? Umfangserweiterung ist ein Befund, kein Bonus.
3. Fehlt Substanz, die in der Spezifikation steht — insbesondere fachlicher Inhalt, der als Beispiel angelegt statt vollständig geliefert wurde?

**Belastbarkeit der Tests**

4. Laufen die Tests? Wörtliche Ausgabe.
5. **Prüfen die Tests das Kriterium oder die Umsetzung?** Suche gezielt nach: Tests ohne Zusicherung; Tests, die nur wiederholen, was der Code tut; Tests, deren Erwartungswert offensichtlich nachträglich an das Ergebnis angepasst wurde; Kriterien der Spezifikation, zu denen es keinen Test gibt. Grüne Tests bei fehlerhaftem Produkt entstehen genau hier.
6. Halten die **Verhaltensannahmen** aus dem Plan im gebauten Zustand? Prüfe die Kernlogik mit eigenen Eingaben, nicht mit denen aus den Tests — insbesondere die Fälle, die niemand aufgeschrieben hat.

**Redlichkeit des Berichts**

7. Stichprobe über die GRÜN gemeldeten Aufgaben: ist der angegebene Nachweis wirklich erbracht?
8. Steht bei Aufgaben mit Nachweisart *Handprüfung* GRÜN? Das ist unzulässig und ein Befund.
9. Sind Abweichungen von Plan oder Verfassung gemeldet worden, oder finden sich welche, die niemand erwähnt hat?

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
  je Akzeptanzkriterium: Urteil · Beleg · Fundstelle

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
