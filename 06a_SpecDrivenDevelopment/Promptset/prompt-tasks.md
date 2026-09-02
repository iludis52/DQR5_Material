# Prompt: Erstellung der tasks.md

*Einsatz: nach Fertigstellung der `plan.md`, vor Prüfstelle B.*
*Mitgeben: `@constitution.md`, `@spec.md`, `@plan.md`.*
*Version 2.0 · Neu: T0 als Prüfstand (§2), Verfälschungskriterium für Testaufgaben (§3), erweiterte Abschlussprüfung (§6).*

---

## 1. Auftrag

Zerlege den Umsetzungsplan in einzelne Aufgaben.

Du leitest ausschließlich ab. Neue Anforderungen, neue Kriterien, neue Features entstehen hier nicht. Fällt dir eine Lücke auf, meldest du sie — du füllst sie nicht.

**Zuschnitt:** Jede Aufgabe muss innerhalb **eines** Kontextfensters umsetzbar **und** prüfbar sein. Zu große Aufgaben führen zu Abdriften, zu kleine zu Reibung. Faustregel: eine Aufgabe ist das, was eine Sitzung sauber erledigt und abschließt.

---

## 2. T0 — der Prüfstand steht zuerst

**Die erste Aufgabe jedes Projekts baut keine Fachlichkeit, sondern die Messeinrichtung.** Sie richtet ein, was §3.8 des Plans festlegt: Umgebung, Prüfbefehle, Bedienwerkzeug für die laufende Anwendung, Verfälschungsbefehl.

```
### T0 — Prüfstand einrichten
Art:             Prüfung
Erfüllt:         — (Voraussetzung für alle folgenden Aufgaben)
Hängt ab von:    —
Inhalt:          Prüfmittel aus plan.md §3.8 einrichten und einmal ausführen.
Fertigkriterium: Alle Prüfbefehle laufen und schlagen erwartungsgemäß fehl;
                 das Bedienwerkzeug erzeugt mindestens ein Artefakt an dem in
                 plan.md §3.8 genannten Ablageort.
Nachweisart:     automatisch
Dateien:         <Konfiguration, Skripte>
Status:          offen
Nachweis:        —
```

**Das Fertigkriterium ist der Fehlschlag, nicht der Erfolg.** Ein Prüfstand, der auf einem leeren Projekt grün meldet, misst nichts — er prüft nur sich selbst. Das ist dieselbe Logik wie beim Test-Umsetzungs-Paar, eine Ebene höher.

Dies ergänzt das leere Gerüst aus `plan.md` §4: dort wird geprüft, dass etwas **baut und startet**, hier, dass etwas **misst**.

---

## 3. Test und Umsetzung werden gepaart

Aufgaben treten paarweise auf, wo automatisierte Prüfung vorgesehen ist:

* **Test-Aufgabe:** schreibt die Tests für ein Verhalten. Ihr Fertigkriterium lautet ausdrücklich, dass die Tests **kompilieren und fehlschlagen** — es existiert ja noch keine Umsetzung. Ein grüner Test ist hier ein Fehler.
* **Umsetzungs-Aufgabe:** implementiert, bis genau diese Tests grün sind. Ihr Fertigkriterium ist der Testlauf, nicht die eigene Einschätzung.

Damit hat jede Umsetzung ein Tor, das sie nicht selbst definiert hat. Wo der Plan browsergestützte Prüfung vorsieht, gilt dasselbe Muster mit dem Szenario an Stelle des Unit-Tests: erst das Szenario, dann die Umsetzung.

Wo der Plan Handprüfung vorsieht, gibt es kein Paar — dort steht die Aufgabe allein und trägt die Nachweisart **Handprüfung**.

**Testaufgaben tragen ein zweites Fertigkriterium**, wo der Plan eine Verfälschungsprüfung vorsieht: Nach dem Grünwerden der zugehörigen Umsetzung muss der Test eine absichtliche Verfälschung der geprüften Funktion bemerken. Formuliere das als eigene Zeile im Fertigkriterium der **Umsetzungs**-Aufgabe, weil es erst dort ausführbar ist:

> Fertigkriterium: `<Prüfbefehl>` läuft grün; anschließend meldet `<Verfälschungsbefehl>` für diese Funktion keine überlebende Verfälschung.

Ein Test, der eine kaputte Umsetzung nicht bemerkt, ist kein Nachweis — auch wenn er zuerst korrekt fehlgeschlagen ist und später korrekt grün wurde. Das ist die einzige Prüfung, die beantwortet, ob die Tests das Kriterium prüfen oder nur die Umsetzung wiederholen.

**Invariantenaufgaben.** Für jede Invariante der Spezifikation entsteht ein Aufgabenpaar wie oben, mit dem in `plan.md` §3.8 festgelegten Eingabebereich und der dort genannten Toleranz im Fertigkriterium. Eine Invariante, die an drei festen Werten geprüft wird, ist als solche nicht umgesetzt — schreib den Bereich hin, nicht die Beispiele.

---

## 4. Form einer Aufgabe

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
Belege:          —
```

`Status` füllt die umsetzende Instanz: **GRÜN** (Kriterium erfüllt und nachgewiesen) · **GELB** (umgesetzt, nicht nachgewiesen — Grund im Feld `Nachweis`) · **ROT** (nicht erfüllt oder blockiert). `offen` heißt: noch nicht bearbeitet.

`Belege` nimmt die Pfade der Artefakte auf, die beim Nachweis entstanden sind — Snapshot, Screenshot, Konsolenmitschnitt, Protokoll der Verfälschungsprüfung. Bei Nachweisart *browsergestützt* ist das Feld Pflicht; ein leeres Feld bedeutet, dass der Nachweis nicht erbracht wurde, unabhängig davon, was im Bericht steht.

Eine Aufgabe mit Nachweisart *Handprüfung* kann **nie** GRÜN erreichen, solange kein Mensch geprüft und das Ergebnis eingetragen hat. Schreib das in die Aufgabe hinein.

---

## 5. Regeln für die Kriterien

* **Nur was die ausführende Instanz selbst nachweisen kann**, darf als automatisch prüfbar ausgewiesen werden. „Funktioniert", „sieht gut aus", „visuell ausreichend" sind keine Kriterien.
* **Die Nachweisart übernimmst du aus der Nachweistabelle des Plans.** Weicht deine Einschätzung ab, meldest du das, statt sie zu ändern.
* **Jede Aufgabe nennt das Akzeptanzkriterium, das sie erfüllt.** Aufgaben ohne Bezug sind entweder überflüssig oder ein Hinweis auf eine fehlende Anforderung — sag, welches von beidem. Ausnahme ist T0, die keine Fachlichkeit erfüllt, sondern die Nachweisbarkeit aller übrigen.
* **Kein Kriterium erfindest du dazu.** Steht in der Spezifikation kein passendes, ist das ein Befund.
* **Zustandskriterien bekommen eigene Aufgaben.** *Leer*, *lädt*, *Fehler*, *Grenzwert* und *ungültige Eingabe* werden nicht als Nebensatz an die Aufgabe für den Normalfall angehängt. Sie sind der Ort, an dem Mängel entstehen, die kein Test bemerkt — sie brauchen ein eigenes Fertigkriterium und einen eigenen Beleg.

---

## 6. Abschließende Aufgabe

Die letzte Aufgabe ist immer eine Gesamtprüfung am **ausgelieferten Artefakt**: bauen, aufrufen, die Akzeptanzkriterien der Spezifikation durchgehen, alle Prüfbefehle des Plans laufen lassen — einschließlich der Invariantenprüfung, eines Durchlaufs mit dem Bedienwerkzeug und der Verfälschungsprüfung über den Kern. Sie hat keine eigene Umsetzung und darf keine Fehler „nebenbei" beheben — sie stellt fest.

---

## 7. Abgabe

Nach der Aufgabenliste lieferst du:

1. **Abdeckungstabelle:** je Akzeptanzkriterium der Spezifikation eine Zeile mit den Aufgaben, die es erfüllen. Unabgedeckte Kriterien führst du gesondert auf — das ist ein Blockierer.
2. **Zählung der Nachweisarten:** wie viele Aufgaben automatisch, browsergestützt, per Handprüfung nachgewiesen werden. Ist der Handprüfungsanteil hoch, sag es deutlich; es bedeutet, dass ein großer Teil des Ergebnisses unbelegt bleiben wird. Weicht die Zählung von der Nachweistabelle des Plans ab, ist das ein Befund, keine Korrektur.
3. **Befunde:** Lücken, Widersprüche, Aufgaben ohne Kriteriumsbezug, Invarianten ohne Aufgabenpaar, interaktive Funktionen ohne Zustandsaufgaben.

Ein Hinweis für die Umsetzung, den du in die Kopfzeile der `tasks.md` schreibst: Aufgaben werden einzeln bearbeitet, nicht im Block. T0 kommt vor allem anderen. Nach drei erfolglosen Korrekturversuchen an derselben Aufgabe wird abgebrochen und ROT gemeldet.
