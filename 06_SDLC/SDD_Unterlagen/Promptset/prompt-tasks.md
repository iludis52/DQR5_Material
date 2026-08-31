# Prompt: Erstellung der tasks.md

*Einsatz: nach Fertigstellung der `plan.md`, vor Prüfstelle B.*
*Mitgeben: `@constitution.md`, `@spec.md`, `@plan.md`.*

---

## 1. Auftrag

Zerlege den Umsetzungsplan in einzelne Aufgaben.

Du leitest ausschließlich ab. Neue Anforderungen, neue Kriterien, neue Features entstehen hier nicht. Fällt dir eine Lücke auf, meldest du sie — du füllst sie nicht.

**Zuschnitt:** Jede Aufgabe muss innerhalb **eines** Kontextfensters umsetzbar **und** prüfbar sein. Zu große Aufgaben führen zu Abdriften, zu kleine zu Reibung. Faustregel: eine Aufgabe ist das, was eine Sitzung sauber erledigt und abschließt.

---

## 2. Test und Umsetzung werden gepaart

Aufgaben treten paarweise auf, wo automatisierte Prüfung vorgesehen ist:

* **Test-Aufgabe:** schreibt die Tests für ein Verhalten. Ihr Fertigkriterium lautet ausdrücklich, dass die Tests **kompilieren und fehlschlagen** — es existiert ja noch keine Umsetzung. Ein grüner Test ist hier ein Fehler.
* **Umsetzungs-Aufgabe:** implementiert, bis genau diese Tests grün sind. Ihr Fertigkriterium ist der Testlauf, nicht die eigene Einschätzung.

Damit hat jede Umsetzung ein Tor, das sie nicht selbst definiert hat. Wo der Plan browsergestützte Prüfung vorsieht, gilt dasselbe Muster mit dem Szenario an Stelle des Unit-Tests: erst das Szenario, dann die Umsetzung.

Wo der Plan Handprüfung vorsieht, gibt es kein Paar — dort steht die Aufgabe allein und trägt die Nachweisart **Handprüfung**.

---

## 3. Form einer Aufgabe

Kein Kästchen zum Abhaken. Ein Häkchen kann nur „gemacht" ausdrücken, und „gemacht" ist keine Aussage über Erfüllung.

```
### T<Nr> — <Titel>
Art:             Test | Umsetzung | Prüfung
Erfüllt:         <IDs der Akzeptanzkriterien aus spec.md>
Hängt ab von:    <Aufgaben-IDs oder —>
Inhalt:          <ein bis drei Sätze>
Fertigkriterium: <konkret und beobachtbar; bei automatischer Prüfung der Befehl>
Nachweisart:     automatisch | browsergestützt | Handprüfung
Dateien:         <Pfade>
Status:          offen
Nachweis:        —
```

`Status` füllt die umsetzende Instanz: **GRÜN** (Kriterium erfüllt und nachgewiesen) · **GELB** (umgesetzt, nicht nachgewiesen — Grund im Feld `Nachweis`) · **ROT** (nicht erfüllt oder blockiert). `offen` heißt: noch nicht bearbeitet.

Eine Aufgabe mit Nachweisart *Handprüfung* kann **nie** GRÜN erreichen, solange kein Mensch geprüft und das Ergebnis eingetragen hat. Schreib das in die Aufgabe hinein.

---

## 4. Regeln für die Kriterien

* **Nur was die ausführende Instanz selbst nachweisen kann**, darf als automatisch prüfbar ausgewiesen werden. „Funktioniert", „sieht gut aus", „visuell ausreichend" sind keine Kriterien.
* **Die Nachweisart übernimmst du aus der Nachweistabelle des Plans.** Weicht deine Einschätzung ab, meldest du das, statt sie zu ändern.
* **Jede Aufgabe nennt das Akzeptanzkriterium, das sie erfüllt.** Aufgaben ohne Bezug sind entweder überflüssig oder ein Hinweis auf eine fehlende Anforderung — sag, welches von beidem.
* **Kein Kriterium erfindest du dazu.** Steht in der Spezifikation kein passendes, ist das ein Befund.

---

## 5. Abschließende Aufgabe

Die letzte Aufgabe ist immer eine Gesamtprüfung am **ausgelieferten Artefakt**: bauen, aufrufen, die Akzeptanzkriterien der Spezifikation durchgehen, alle Prüfbefehle des Plans laufen lassen. Sie hat keine eigene Umsetzung und darf keine Fehler „nebenbei" beheben — sie stellt fest.

---

## 6. Abgabe

Nach der Aufgabenliste lieferst du:

1. **Abdeckungstabelle:** je Akzeptanzkriterium der Spezifikation eine Zeile mit den Aufgaben, die es erfüllen. Unabgedeckte Kriterien führst du gesondert auf — das ist ein Blockierer.
2. **Zählung der Nachweisarten:** wie viele Aufgaben automatisch, browsergestützt, per Handprüfung nachgewiesen werden. Ist der Handprüfungsanteil hoch, sag es deutlich; es bedeutet, dass ein großer Teil des Ergebnisses unbelegt bleiben wird.
3. **Befunde:** Lücken, Widersprüche, Aufgaben ohne Kriteriumsbezug.

Ein Hinweis für die Umsetzung, den du in die Kopfzeile der `tasks.md` schreibst: Aufgaben werden einzeln bearbeitet, nicht im Block. Nach drei erfolglosen Korrekturversuchen an derselben Aufgabe wird abgebrochen und ROT gemeldet.
