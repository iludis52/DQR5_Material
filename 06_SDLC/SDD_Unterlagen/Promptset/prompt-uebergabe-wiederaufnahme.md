# Prompts: Übergabe und Wiederaufnahme

*Zwei Prompts, die zusammengehören. Der erste wird am Ende einer Sitzung eingesetzt, der zweite zu Beginn der nächsten.*

---

# Teil 1 — Übergabe

*Einsatz: am Ende einer Sitzung, bevor der Kontext knapp wird oder die Arbeit unterbrochen wird. Nicht erst, wenn das Modell anfängt zu schwimmen.*

## Auftrag

Schreibe ein Übergabedokument `uebergabe-<Datum>.md` im Projektordner.

Es beschreibt den **Zustand**, nicht den Gesprächsverlauf. Niemand braucht eine Zusammenfassung dessen, was wir besprochen haben — die nächste Instanz braucht, woran sie anknüpft.

## Vor dem Schreiben: Zustand feststellen

Behaupte nichts über den Projektzustand, ohne nachgesehen zu haben. Führe aus und notiere die Ergebnisse:

* Branch, letzter Commit, nicht eingecheckte Änderungen
* die Prüfbefehle aus `plan.md` — laufen sie? Wörtliche Ausgabe, gekürzt
* Statusfelder in `tasks.md`: was steht dort tatsächlich?

Wo du etwas nicht prüfen konntest, schreibe **„ungeprüft"** dazu.

## Inhalt

```
# Übergabe <Datum, Uhrzeit>

## Ziel
Ein bis zwei Sätze. Wozu das Projekt da ist.

## Bezugsdokumente
constitution.md · spec.md · plan.md · tasks.md — nur nennen, nicht wiedergeben.

## Zustand (geprüft)
Branch, Commit, offene Änderungen, Ergebnis der Prüfbefehle.

## Erledigt
Aufgaben mit Status und Nachweisart. GELB gesondert: was fehlt zum Nachweis.

## Offen
Nächste Aufgabe und die darauf folgenden. Blockierer mit Ursache.

## Entscheidungen dieser Sitzung
Was entschieden wurde und warum — besonders das, was nicht im Plan stand.

## Bewusst nicht getan
Verworfene Wege, mit Grund. Verhindert, dass die nächste Instanz sie erneut geht.

## Offene Fragen an den Menschen
Was ohne Entscheidung nicht weitergeht.

## Nächster Schritt
Ein Satz. Konkret.

## Wiedereinstieg
Die Befehle, mit denen der Arbeitsstand hergestellt wird.
```

Kennzeichne jede Aussage, bei der du dir unsicher bist, als unsicher. Das Dokument gehört mir und ich korrigiere es, bevor ich es weitergebe — dafür muss ich sehen, wo du geraten hast.

Gib am Ende den Wiederaufnahme-Prompt aus Teil 2 in einem Codeblock aus, mit dem Pfad des Übergabedokuments eingesetzt.

---

# Teil 2 — Wiederaufnahme

*Einsatz: erste Nachricht einer neuen Sitzung.*

## Auftrag

Du übernimmst ein laufendes Projekt. Lies in dieser Reihenfolge: das Übergabedokument `<Pfad>`, dann `constitution.md`, `spec.md`, `plan.md`, `tasks.md`.

## Erst prüfen, dann glauben

Das Übergabedokument ist eine **Behauptung** über den Zustand, nicht der Zustand. Es kann veraltet sein, ich kann seither etwas geändert haben, und die vorige Instanz kann sich geirrt haben.

Bevor du irgendetwas tust:

1. Stelle den tatsächlichen Zustand fest — Branch, letzter Commit, offene Änderungen, Prüfbefehle ausführen.
2. Vergleiche mit dem Übergabedokument.
3. **Melde jede Abweichung zuerst.** Wenn das Dokument grüne Tests behauptet und die Tests rot sind, ist das deine erste Aussage, nicht eine Fußnote.
4. Alles, was im Dokument als unsicher markiert ist, prüfst du nach oder kennzeichnest es weiterhin als ungeprüft.
5. Den aktuellen Arbeitsstand leitest du aus den Statusfeldern in `tasks.md` ab, nicht aus der Erzählung des Dokuments.

## Dann melden

Höchstens zehn Zeilen:

* tatsächlicher Zustand
* Abweichungen zum Übergabedokument
* die Aufgabe, die als Nächstes ansteht, mit ihrer Nummer
* offene Fragen, die vor dem Weiterarbeiten zu klären sind

Dann **wartest du**. Du beginnst keine Umsetzung, bevor ich den nächsten Schritt bestätigt habe. Für die Umsetzung selbst gilt anschließend der Umsetzungs-Prompt: eine Aufgabe, ein Bericht.
