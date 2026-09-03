# Prompt: Erstellung der tasks.md

*Einsatz: nach Fertigstellung der `plan.md`, vor Prüfstelle B — oder, im Korrekturmodus, nach einer Befundliste aus ⑦.*
*Mitgeben: `@constitution.md`, `@spec.md`, `@plan.md`. Im Korrekturmodus zusätzlich die Befundliste.*
*Version 2.3 · Neu: Etappenfeld (§4), Status und Nachweis wandern ins Laufprotokoll (§4), Erfüllungsnachweis statt Eintrag in plan.md §3.9 (§6), Etappenübersicht und neue Kopfzeile (§7), Korrektur- und Änderungsrunden (§8).*

---

## 1. Auftrag

Zerlege den Umsetzungsplan in einzelne Aufgaben.

Du leitest ausschließlich ab. Neue Anforderungen, neue Kriterien, neue Features entstehen hier nicht. Fällt dir eine Lücke auf, meldest du sie — du füllst sie nicht.

**Zuschnitt:** Jede Aufgabe muss innerhalb **eines** Kontextfensters umsetzbar **und** prüfbar sein. Zu große Aufgaben führen zu Abdriften, zu kleine zu Reibung. Faustregel: eine Aufgabe ist das, was in einem Zug sauber erledigt und abgeschlossen wird.

---

## 2. T0 — der Prüfstand steht zuerst

**Die erste Aufgabe jedes Projekts baut keine Fachlichkeit, sondern die Messeinrichtung.** Sie richtet ein, was §3.8 des Plans festlegt: Umgebung, Prüfbefehle, Bedienwerkzeug für die laufende Anwendung, Verfälschungsbefehl.

```
### T0 — Prüfstand einrichten
Art:             Prüfung
Etappe:          E0 — Prüfstand
Erfüllt:         — (Voraussetzung für alle folgenden Aufgaben)
Hängt ab von:    —
Inhalt:          Prüfmittel aus plan.md §3.8 einrichten und einmal ausführen.
Fertigkriterium: Alle Prüfbefehle laufen und schlagen erwartungsgemäß fehl;
                 das Bedienwerkzeug erzeugt mindestens ein Artefakt an dem in
                 plan.md §3.8 genannten Ablageort.
Nachweisart:     automatisch
Dateien:         <Konfiguration, Skripte>
```

**Das Fertigkriterium ist der Fehlschlag, nicht der Erfolg.** Ein Prüfstand, der auf einem leeren Projekt grün meldet, misst nichts — er prüft nur sich selbst. Das ist dieselbe Logik wie beim Test-Umsetzungs-Paar, eine Ebene höher.

Dies ergänzt das leere Gerüst aus `plan.md` §4: dort wird geprüft, dass etwas **baut und startet**, hier, dass etwas **misst**.

**T0 ist immer eine eigene Etappe** und wird vor allem anderen umgesetzt und gelesen. Ein Lauf, der auf einem ungeprüften Prüfstand aufsetzt, ist wertlos, gleich wie gut er berichtet.

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
Etappe:          <Kennung und Name der Etappe>
Erfüllt:         <IDs der Akzeptanzkriterien aus spec.md>
Hängt ab von:    <Aufgaben-IDs oder —>
Inhalt:          <ein bis drei Sätze>
Fertigkriterium: <konkret und beobachtbar; bei automatischer Prüfung der Befehl>
Nachweisart:     automatisch | browsergestützt | Handprüfung
Dateien:         <Pfade>
```

**Die `tasks.md` ist Maß, nicht Logbuch.** Sie trägt keine Status-, Nachweis- oder Belegfelder. Die umsetzende Instanz schreibt Ampel, wörtliche Prüfausgabe und Artefaktpfade in ihr Laufprotokoll und fasst sie im Etappenbericht zusammen (Umsetzungs-Prompt §6 und §7). Der Grund: eine Datei, die in jedem Lauf von genau der Instanz beschrieben wird, die an ihr gemessen wird, ist kein Maß mehr — und sie nimmt beim häufigen Beschreiben Schaden.

**Das Feld `Etappe` gruppiert die Aufgaben zu Läufen.** Leite die Gruppen aus `Hängt ab von` ab: ein Strang, der nach T0 unabhängig beginnt und später in einen gemeinsamen Block mündet, ist eine Etappe; der gemeinsame Block am Ende ist eine eigene. Erfinde keine Gruppierung nach Thema, wenn die Abhängigkeiten eine andere hergeben — die Abhängigkeit ist das Argument, die Überschrift ist nur der Name.

Eine Aufgabe mit Nachweisart *Handprüfung* kann **nie** GRÜN erreichen, solange kein Mensch geprüft und das Ergebnis im Laufprotokoll eingetragen hat. Schreib das in die Aufgabe hinein.

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

**Der Erfüllungsnachweis entsteht im Laufprotokoll, nicht in `plan.md` §3.9.** §3.9 hält das Nachweis*verfahren* je Kriterium fest und ist für die Umsetzung read-only; eine Aufgabe, die dort Ergebnisse einträgt, verlangt genau das, was der Umsetzungs-Prompt verbietet. Die Abschlussaufgabe erzeugt stattdessen eine Tabelle Kriterium → Aufgabe → Befehl → Artefakt im Laufprotokoll. Das Übertragen in den Anhang der Spezifikation geschieht beim Archivieren nach der Abnahme.

Diese Aufgabe ist zugleich die Grundlage, auf der ⑦ arbeitet. Sie misst — ⑦ prüft, ob die Messung trägt.

---

## 7. Abgabe

Nach der Aufgabenliste lieferst du:

1. **Abdeckungstabelle:** je Akzeptanzkriterium der Spezifikation eine Zeile mit den Aufgaben, die es erfüllen. Unabgedeckte Kriterien führst du gesondert auf — das ist ein Blockierer.
2. **Zählung der Nachweisarten:** wie viele Aufgaben automatisch, browsergestützt, per Handprüfung nachgewiesen werden. Ist der Handprüfungsanteil hoch, sag es deutlich; es bedeutet, dass ein großer Teil des Ergebnisses unbelegt bleiben wird. Weicht die Zählung von der Nachweistabelle des Plans ab, ist das ein Befund, keine Korrektur.
3. **Etappenübersicht:** je Etappe eine Zeile mit den enthaltenen Aufgaben, den eingehenden Abhängigkeiten und der Zahl der Aufgaben. Etappen mit mehr als acht Aufgaben oder mit Abhängigkeiten quer zu anderen Etappen meldest du als Befund — die erste läuft dem Kontext davon, die zweite lässt sich nicht in einem Zug abschließen.
4. **Befunde:** Lücken, Widersprüche, Aufgaben ohne Kriteriumsbezug, Invarianten ohne Aufgabenpaar, interaktive Funktionen ohne Zustandsaufgaben.

Ein Hinweis für die Umsetzung, den du in die Kopfzeile der `tasks.md` schreibst: Aufgaben werden etappenweise bearbeitet, in der Reihenfolge aus `Hängt ab von`, ohne Halt innerhalb der Etappe. T0 ist eine eigene Etappe und kommt vor allem anderen. Status und Nachweis stehen im Laufprotokoll, nicht in dieser Datei. Nach drei erfolglosen Korrekturversuchen an derselben Aufgabe wird abgebrochen und ROT gemeldet.

---

## 8. Korrektur- und Änderungsrunden

Dieser Abschnitt greift nach der Abnahme, wenn Befunde zurückkommen. Welcher Teil gilt, hängt an der Klasse des Befunds.

### 8.1 Korrekturrunde K — Befunde der Klasse 1

Wirst du mit einer **Befundliste** statt mit einem Plan beauftragt, gilt dieser Teil.

**Du nimmst ausschließlich Befunde der Klasse 1 auf** — solche, die ein bestehendes Akzeptanzkriterium verletzen. Befunde der Klasse 2 (Kriteriumslücke) und der Klasse 3 (Änderungswunsch) gehören zurück an ①; du meldest sie und nimmst sie nicht auf. Ist ein Befund nicht eingeordnet oder nennt er kein Kriterium, ist das ein Blockierer, keine Auslegungsfrage. Die Spezifikation wird in diesem Modus nicht angefasst.

**Je Befund ein Paar**, nummeriert `K1`, `K2`, … und zusammengefasst zu einer einzigen Etappe:

```
### K<Nr>a — <Befund>: Reproduktion
Art:             Test
Etappe:          K — Korrekturrunde <Datum>
Erfüllt:         <ID des verletzten Kriteriums>
Fertigkriterium: <Prüfbefehl> schlägt fehl und bildet genau das gemeldete
                 Symptom ab — nicht irgendeinen Fehlschlag.

### K<Nr>b — <Befund>: Behebung
Art:             Umsetzung
Etappe:          K — Korrekturrunde <Datum>
Erfüllt:         <ID des verletzten Kriteriums>
Hängt ab von:    K<Nr>a
Fertigkriterium: <Prüfbefehl> läuft grün; die bestehende Suite bleibt
                 vollständig grün (Bestandsschutz); wo der Plan es vorsieht,
                 meldet <Verfälschungsbefehl> keine überlebende Verfälschung.
```

Die Reihenfolge ist dieselbe wie sonst, aus einem älteren Grund: Verfassung §5 verlangt bei Fehlerbehebung zuerst einen Test, der den Fehler reproduziert. Ein Reproduktionstest, der aus irgendeinem Grund fehlschlägt, ist kein Reproduktionstest — er muss das gemeldete Symptom zeigen, sonst weiß niemand, ob die spätere Behebung dieses Symptom betrifft.

**Der Bestandsschutz ist Pflicht, nicht Kür.** Eine Korrektur, die etwas anderes zerstört, ist keine Korrektur. Nenne im Fertigkriterium die vollständige Suite, nicht nur die Tests des betroffenen Bereichs.

**Die letzte Aufgabe der Runde ist die Gesamtprüfung aus §6**, unverändert.

Liefere zur Runde eine kurze **Zuordnungstabelle**: je Befund die Nummer, das verletzte Kriterium und das Aufgabenpaar. Befunde, die du nicht aufgenommen hast, führst du mit Grund gesondert auf.

### 8.2 Änderungsrunde Ä — nach geänderter Spezifikation

Wirst du mit einer **geänderten `spec.md`** beauftragt und ist der Bestand bereits umgesetzt, gilt dieser Teil. Er greift nach Befunden der Klasse 2 und 3, wenn ① das Kriterium geschärft oder ergänzt und ③ den Plan nachgezogen hat.

**Du erzeugst Aufgaben nur für die geänderten und neuen Kriterien.** Alles Übrige gilt als erfüllt; du leitest dafür keine Aufgaben ab und nummerierst nicht neu. Ist unklar, welche Kriterien geändert wurden, ist das ein Blockierer — frag nach der Liste, rate sie nicht.

Nummerierung `Ä1`, `Ä2`, …, eine Etappe `Ä — Änderungsrunde <Datum>`, im Übrigen das gewohnte Paarmuster aus §3. Zwei Zusätze:

* **Bestandsschutz** gehört in jedes Fertigkriterium der Umsetzungs-Aufgaben, wie in §8.1.
* **Ein geschärftes Kriterium kann bestehendes Verhalten ungültig machen.** Fällt dir beim Ableiten auf, dass eine Änderung einem bereits erfüllten Kriterium widerspricht, ist das ein Befund für ① — du löst den Widerspruch nicht auf.

Die Abgabe entspricht §7, beschränkt auf den geänderten Ausschnitt; die Abdeckungstabelle führt die unveränderten Kriterien mit dem Vermerk „Bestand" auf.
