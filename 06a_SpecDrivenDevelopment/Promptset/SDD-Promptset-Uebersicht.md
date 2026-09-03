# SDD-Promptset — Übersicht und Kurzanleitung

*Stand 03.09.2026. Acht Prompts, vier Projektdokumente, drei Prüfstellen.*

---

## Die Kette

```
   constitution.md  (dauerhaft, projektübergreifend)
          │
   ①  Metaprompt ─────────────► spec.md        ← dauerhaft, rein fachlich
          │
   ②  Prüfstelle A ────────────► Freigabe der spec.md
          │
   ③  Plan-Prompt ─────────────► plan.md       ← flüchtig bis auf §3.8/§3.9
          │
   ④  Tasks-Prompt ────────────► tasks.md      ← flüchtig, Arbeitsschritte
          │
   ⑤  Prüfstelle B ────────────► Freigabe der Umsetzung
          │
   ⑥  Umsetzungs-Prompt ───────► Code, je Etappe ein Lauf
          │
   ⑦  Prüfstelle C ────────────► Aktenprüfung, Befunde in drei Klassen
          │
   ★  Abnahme durch einen Menschen am laufenden Produkt
          │
          └─► Korrekturrunde (Klasse 1) oder zurück zu ① (Klasse 2 und 3)

   ⑧  Übergabe / Wiederaufnahme  (quer zu allem, bei Unterbrechung)
```

**Zwei Gattungen von Dokumenten, mit einer Ausnahme.** `constitution.md` und `spec.md` sind dauerhaft — sie überleben den Code. `plan.md` und `tasks.md` sind flüchtig. Ausgenommen sind **§3.8 (Prüfbefehle) und §3.9 (Nachweistabelle)** des Plans: sie werden beim Verwerfen als Anhang zur `spec.md` gesichert. Begründung: Diese beiden Abschnitte tragen das Abnahmesignal. Wer sie wegwirft, kann bei der nächsten Änderung nicht mehr feststellen, woran ein Kriterium ursprünglich gemessen wurde, und muss das Orakel neu erfinden — meist von derselben Instanz, die den Code schreibt. Genau das soll das Set verhindern.

**Die Trennlinie zwischen Spec und Plan ist die wichtigste Regel des Sets.** Die Spezifikation sagt was und warum, in Fachsprache, ohne Technologie, ohne Bibliotheken, ohne Code. Der Plan sagt wie. Steht Technik in der Spec, ist das ein Mangel, keine Vorgabe.

**Vorsteuerung und Rückmeldung.** `constitution.md`, `spec.md` und `plan.md` steuern vor: sie erhöhen die Wahrscheinlichkeit, dass etwas Richtiges entsteht. Prüfbefehle, Testläufe und die drei Prüfstellen melden zurück: sie stellen fest, was tatsächlich entstanden ist. Ein Set, das nur vorsteuert, erzeugt gut begründete Fehler. Die Prüfstellen sind Rückmeldung an Etappen- und Sitzungsgrenzen; die Prüfbefehle sind Rückmeldung im Lauf. Beides wird gebraucht.

---

## Die acht Prompts

| # | Datei | Wann | Eingaben | Ergebnis |
| --- | --- | --- | --- | --- |
| ① | `metaprompt-spec-v3.md` | Projektstart | Projektidee | `spec.md` |
| ② | `review-prompt-A-spec.md` | nach ① | constitution, spec, Projektidee | Befundbericht, Urteil |
| ③ | `prompt-plan.md` | nach Freigabe ② | constitution, spec | `plan.md` |
| ④ | `prompt-tasks.md` | nach ③, oder nach einer Befundliste | constitution, spec, plan bzw. Befundliste | `tasks.md` |
| ⑤ | `review-prompt-B-abgleich.md` | nach ④ | alle vier Dokumente | Abdeckungstabelle, Urteil |
| ⑥ | `prompt-umsetzung.md` | je Etappe | alle vier + Etappe | Code, Laufprotokoll, Etappenbericht |
| ⑦ | `review-prompt-C-abnahme.md` | nach der Umsetzung | alle vier, Laufprotokolle, Projekt | Aktenbericht, Befunde 1/2/3 |
| ⑧ | `prompt-uebergabe-wiederaufnahme.md` | bei Unterbrechung | Projektstand | Übergabedokument |

### ① Metaprompt — Spezifikation erarbeiten

Führt ein Klärungsgespräch und schreibt daraus die `spec.md`. Prüft die Projektidee zuerst intern gegen zwölf Punkte, ohne die Liste zu zeigen, und stellt daraus höchstens fünf Fragen pro Runde, einzeln und nach Wirkung sortiert. Akzeptanzkriterien entstehen in EARS-Notation, gegliedert in Verhalten, Invarianten und Zustände.

*Worauf es ankommt:* Vor der ersten Frage steht ein begründeter Einwand gegen die Produktidee selbst. Und: die Spec wird erst auf ausdrückliches Kommando geschrieben.

**Invarianten statt Sollwerten.** Wo das Produkt rechnet, umformt oder auflöst, erhebt das Gespräch **fachliche Invarianten** — Aussagen darüber, wie sich das Ergebnis ändern muss, wenn sich die Eingabe auf bestimmte Weise ändert. Verdopplung, Symmetrie, Einheitenkonsistenz, Rückeinsetzung, Grenzwert- und Randverhalten. Sie werden als EARS-Kriterien aufgeschrieben und sind fachliche Aussagen, kein Technikinhalt; sie gehören deshalb in die Spec und nicht in den Plan.

Der Grund ist der wichtigste Konstruktionsfehler agentischer Umsetzung: Wer Sollwerte nicht vorgibt, überlässt sie der umsetzenden Instanz — und die schreibt Erwartungswerte auf, die ihre eigene Lesart bestätigen. Eine Invariante muss man nicht kennen, um sie zu prüfen. Sie gilt für alle Eingaben und lässt sich nicht nachträglich an ein Ergebnis anpassen.

**Zustände sind Kriterien, keine Bedienungsdetails.** Für jede interaktive Funktion verlangt der Metaprompt EARS-Kriterien für die Zustände *leer*, *lädt*, *Fehler*, *Grenzwert* und *ungültige Eingabe*. Was hier nicht steht, wird nicht gebaut und nicht geprüft — Bedienbarkeit landet sonst zwangsläufig als Geschmacksurteil in der Abnahme oder gar nicht.

### ② Prüfstelle A — Review der Spezifikation

Frische Sitzung, anderes Modell. Prüft Testbarkeit der Kriterien, Erreichbarkeit der Inhalte mit dem festgelegten Bedienmodell, Vollständigkeit der Rückverfolgung.

Zusätzlich prüft A die **Härte der Invarianten**: Ist die Relation notwendig oder nur plausibel? Gilt sie über den ganzen Definitionsbereich? Würde eine falsche Umsetzung sie tatsächlich verletzen? Eine Invariante, die jede Implementierung erfüllt, ist keine.

*Worauf es ankommt:* Die Prüfinstanz **schlägt vor und entscheidet nicht**. Sie korrigiert nichts selbst, und sie stellt keine Behauptungen über das Verhalten fremder Software auf.

### ③ Plan-Prompt — technische Festlegungen

Erzeugt den Umsetzungsplan: Technologiewahl, Abhängigkeiten mit belegten Versionen, Datenformate, Struktur, Auslieferung.

*Worauf es ankommt:* §3.4 — Verhaltensannahmen über Bibliotheken werden **beim Schreiben des Plans ausgeführt**, nicht später geglaubt. §3.9 — jedes Akzeptanzkriterium bekommt hier sein Nachweisverfahren. §4 — bei neuen Projekten zuerst ein leeres Gerüst bauen und aufrufen.

**§3.8 legt zusätzlich zwei Prüfmittel fest**, sofern das Projekt eine Bedienoberfläche oder nennenswerte Rechenlogik hat:

* **Browsersteuerung für Agenten.** Der Plan benennt das Werkzeug, mit dem eine Instanz die *laufende* Anwendung bedient, und wo dessen Artefakte landen — Accessibility-Snapshot, Screenshot, Browserkonsole, Netzwerkmitschnitt. Entscheidend ist nicht das Bedienen, sondern dass dabei prüfbare Dateien entstehen: sie sind unabhängig von dem, was die Instanz über ihren Lauf behauptet.
* **Mutationsprüfung.** Ein Befehl, der die Tests gegen absichtlich verfälschten Code laufen lässt. Überlebt eine Verfälschung, ist das eine Testlücke. Wo kein fertiges Werkzeug passt, genügt das Verfahren von Hand: geänderte Dateien bestimmen, je Kernfunktion eine Verfälschung setzen, Tests laufen lassen, Ergebnis notieren, Verfälschung zurücknehmen.

**§3.9 bleibt erhalten.** Die Nachweistabelle wird beim Verwerfen des Plans zusammen mit §3.8 archiviert. Bei jedem Kriterium, für das nur Handprüfung bliebe, prüft der Plan zuerst, ob die Browsersteuerung es abdeckt. Sie hält das Nachweis*verfahren* fest, nicht das Ergebnis — gefüllt wird sie nicht von der Umsetzung, sondern beim Archivieren nach der Abnahme.

### ④ Tasks-Prompt — Zerlegung

Leitet die Arbeitsschritte ab. Test- und Umsetzungsaufgaben treten paarweise auf: erst die Tests, deren Fertigkriterium ausdrücklich das **Fehlschlagen** ist, dann die Umsetzung, bis sie grün sind.

**T0 ist immer der Prüfstand.** Die erste Aufgabe jedes Projekts baut nicht Fachlichkeit, sondern die Messeinrichtung: Umgebung, Prüfbefehle, Browsersteuerung, Mutationsbefehl. Ihr Fertigkriterium ist ein Lauf des leeren Prüfstands mit **erwartetem Fehlschlag** — rot aus dem richtigen Grund. Das ergänzt das leere Gerüst aus ③ §4 um die Rückmeldeseite: dort wird geprüft, dass etwas *baut und startet*, hier, dass etwas *misst*. T0 ist eine eigene Etappe.

**Testaufgaben tragen die Mutationsprüfung als zweites Fertigkriterium**, wo der Plan sie vorsieht. Ein Test, der eine verfälschte Umsetzung nicht bemerkt, ist noch nicht fertig — auch wenn er fehlschlägt und später grün wird.

**Jede Aufgabe trägt ein Etappenfeld.** Die Gruppierung wird nicht nach Thema erfunden, sondern aus `Hängt ab von` abgeleitet: ein Strang, der nach T0 unabhängig beginnt, ist eine Etappe; der Block, in den alle Stränge münden, ist eine eigene. Die Etappe ist die Einheit, in der ⑥ läuft und in der ein Mensch liest.

**Die `tasks.md` trägt keine Status-, Nachweis- und Belegfelder mehr.** Sie ist Maß, nicht Logbuch; die Umsetzung schreibt in ihr Laufprotokoll.

**§8 sind die Korrektur- und Änderungsrunden.** Mit einer Befundliste statt eines Plans erzeugt ④ eine Korrekturrunde K; mit einer geänderten Spezifikation eine Änderungsrunde Ä, beschränkt auf die geänderten Kriterien. Siehe den Bereich *Nach der Auslieferung* am Ende dieses Dokuments.

*Worauf es ankommt:* Kein Häkchen, sondern eine Ampel — geführt im Laufprotokoll. Jede Aufgabe muss in einem Kontextfenster umsetzbar und prüfbar sein, jede Etappe in einem Lauf abschließbar.

### ⑤ Prüfstelle B — Abgleich vor der Umsetzung

Frische Sitzung, read-only. Prüft die vier Dokumente gegeneinander: Ist jedes Kriterium durch eine Aufgabe abgedeckt? Verweist jede Aufgabe auf ein Kriterium? Sind Handprüfungen als solche gekennzeichnet? Sind Verhaltensannahmen belegt? Existiert T0, und misst der Prüfstand das, was die Nachweistabelle verlangt? Sind die Etappen aus den Abhängigkeiten abgeleitet und in einem Lauf abschließbar?

*Worauf es ankommt:* Ein Kriterium, das automatisch prüfbar aussieht, aber Handprüfung braucht, ist ein Blockierer — es wird sonst abgehakt, ohne erfüllt zu sein.

### ⑥ Umsetzungs-Prompt — eine Etappe

Je Lauf genau eine Etappe, in der Reihenfolge aus `Hängt ab von`, ohne Halt zwischen den Aufgaben. Je Aufgabe ein Protokolleintrag mit Ampel und wörtlicher Befehlsausgabe und ein Kontrollpunkt-Commit; am Ende ein Etappenbericht für den Menschen.

*Worauf es ankommt:* Kein Test wird geändert, damit er grün wird. Kein Kriterium wird abgeschwächt. Das Maß wird nicht angefasst — auch nicht mit einem Statuseintrag. Handprüfungsaufgaben enden immer GELB und halten den Lauf nicht an. Keine Behauptung ohne Ausgabe.

**Was den Lauf beendet, steht abschließend in §5** — ROT, drei erfolglose Versuche, eine überlebende Verfälschung, eine nötige Änderung an Maß oder Test, eine ungeplante Entscheidung mit Wirkung über die Aufgabe hinaus, eine abweichende Prüfsumme, eine fehlende Vorbedingung. Alles andere wird protokolliert und weitergearbeitet. Der Halt liegt an der Etappengrenze, nicht zwischen zwei Aufgaben.

**Kein Ergebnis ohne Ausgabe gilt auch für die Oberfläche.** Bei Aufgaben mit Nachweisart *browsergestützt* endet die Aufgabe nicht am Testbericht, sondern an der laufenden Anwendung. Das Protokoll nennt die erzeugten Artefakte mit Pfad und zitiert die Browserkonsole. „Die Ansicht funktioniert" ist eine Behauptung; ein Snapshot und eine leere Fehlerkonsole sind ein Nachweis.

**Die Absicherungsschicht** trägt, was Prosa über einen langen Lauf nicht mehr allein trägt, und wird einmal je Projekt eingerichtet — nicht in jedem Lauf mitgelesen. Drei Stufen:

* *Stufe 1, immer, portabel:* Prüfsummen über `spec.md` und `plan.md` vor und nach jedem Lauf, beide Werte im Etappenbericht. Das verhindert eine Maßänderung nicht, macht sie aber unverschweigbar. Braucht nur eine Shell; steht als Arbeitsschritt in ⑥ §2.
* *Stufe 2, empfohlen, werkzeugabhängig:* eine Schreibsperre auf die Maßdateien, gesetzt vom Werkzeug statt zugesagt vom Modell. Bietet die Umgebung Modi oder Rollen mit eingeschränkten Schreibrechten, richte einen Umsetzungsmodus ein, der `spec.md`, `plan.md` und `tasks.md` gar nicht erst öffnen kann. Sonst die Dateien für die Dauer des Laufs im Dateisystem schreibschützen.
* *Stufe 3, optional:* eine Prüfung im Lauf, ob während einer Aufgabe der Art *Umsetzung* Dateien im Testverzeichnis verändert wurden. Schlägt sie an, ist das ein Blockierer.

Was das Werkzeug nicht abdeckt, gilt trotzdem — die Verschärfungen in ⑥ §4 stehen unabhängig von Stufe 2 und 3. Umgekehrt ersetzt keine Stufe die Prüfstellen: sie sichern die Regeln, nicht das Ergebnis.

**Warum der Takt fiel.** Die Sitzungsgrenze je Aufgabe war nie eine fachliche Regel, sondern eine Vorsichtsmaßnahme mit drei Funktionen: frischer Kontext, Rücksprungpunkt, Lesepunkt für den Menschen. Der frische Kontext ist Werkzeugsache, der Rücksprungpunkt wurde zum Commit, und nur der Lesepunkt ist qualitätstragend — er liegt jetzt an der Etappengrenze.

**Warum die `tasks.md` read-only wurde.** Eine Datei, die in jedem Lauf von genau der Instanz beschrieben wird, die an ihr gemessen wird, ist kein Maß mehr — und sie nimmt Schaden: im Referenzlauf war eine Aufgabenüberschrift in das Belegfeld der vorigen Aufgabe verschmolzen.

### ⑦ Prüfstelle C — Aktenprüfung

Frische Sitzung, anderes Modell, read-only. C prüft **nicht das Produkt, sondern den Nachweis**: ob die Tests das Kriterium prüfen oder die Umsetzung wiederholen, ob die Invarianten Bereiche prüfen statt fester Werte, ob die behaupteten Belege existieren und zeigen, was sie zeigen sollen, ob irgendwo GRÜN auf einer Handprüfung steht, ob ein Kriterium nur auf einem Nebenpfad erfüllt ist, und ob Umfang und Substanz stimmen.

**C misst nicht ein zweites Mal.** Bauen, Starten, das Durchgehen der Kriterien am laufenden Produkt und die Verfälschungsprüfung hat der Prüfstand geleistet — die Abschlussaufgabe aus ④ §6 und der Mutationsbefehl aus ③ §3.8. Eine Wiederholung derselben Messung unmittelbar danach liefert dasselbe Ergebnis und kostet nur Zeit. Erlaubt bleibt, einen Prüfbefehl erneut laufen zu lassen, wenn eine behauptete Ausgabe fehlt, und die Kernlogik mit eigenen Eingaben anzusprechen.

**C ordnet jeden Befund ein** — eigene wie mitgegebene aus der Nutzung — in Klasse 1, 2 oder 3 (siehe unten). Das ist der Eingang in den Korrekturloop.

*Worauf es ankommt:* Seit die Aufgaben etappenweise laufen, liest niemand mehr jede einzelne Belegbehauptung nach. Genau deshalb ist die Belegprüfung wertvoller geworden, während die Zweitmessung ihren Wert verloren hat.

### ⑧ Übergabe und Wiederaufnahme

Zwei zusammengehörige Prompts für Sitzungsgrenzen. Der erste stellt den Zustand fest (nicht: erinnert ihn) und schreibt ihn auf. Der zweite misst beim Wiedereinstieg nach und meldet Abweichungen zuerst. Bei einem abgebrochenen Etappenlauf sind Laufprotokoll und letzter Kontrollpunkt der Ausgangspunkt, nicht die Erinnerung.

---

## Betriebsregeln

* **Prüfstellen laufen in frischer Sitzung und mit einem anderen Modell** als das prüfende Werk. Ein unbelasteter Kontext findet, was der Autor übersieht.
* **Das Maß schreibt nicht, wer daran gemessen wird.** Akzeptanzkriterien, Invarianten und Nachweistabelle entstehen vor der Umsetzung und außerhalb ihrer Sitzung. Die umsetzende Instanz darf sie lesen, nicht ändern. Ein Änderungswunsch geht über dich zurück an die Stelle, an der das Maß entstanden ist.
* **Das Maß wird auch nicht mit Status beschrieben.** `spec.md`, `plan.md` und `tasks.md` sind während der Umsetzung read-only; Ampeln, Nachweise und Belege stehen im Laufprotokoll.
* **Was nicht gemessen wurde, ist nicht erfüllt.** Ein Prüfmittel, das eine absichtlich verfälschte Umsetzung nicht bemerkt, zählt nicht als Nachweis.
* **Prüfinstanzen ändern nichts.** Sie berichten. Was zurück ins Werk soll, geht über dich.
* **Eine Etappe, ein Lauf, ein Bericht.** Der Halt liegt an der Etappengrenze, nicht zwischen zwei Aufgaben. Was einen Lauf vorzeitig beendet, steht abschließend in ⑥ §5.
* **Ein Kontrollpunkt je Aufgabe.** Ein Commit ersetzt den Rücksprungpunkt, den früher das Sitzungsende lieferte (Verfassung §8).
* **Die Maschine prüft die Akten, der Mensch nimmt das Produkt ab.** Keine Prüfinstanz ersetzt den Blick auf das laufende Ergebnis.
* **Nach drei erfolglosen Versuchen an derselben Aufgabe: Abbruch und ROT.**
* **GELB ist ein zulässiges und ehrliches Ergebnis.** Ein GRÜN, das nicht trägt, ist teurer als ein GELB, das die Lücke benennt.
* **Die Freigabe unterschreibt ein Mensch.** Prüfung durch ein Modell ist Unterstützung, kein Ersatz.

---

## Ein Durchlauf von null

1. `constitution.md` bereitlegen (Version 1.3 oder höher — ab 1.3 sind die Kontrollpunkt-Commits freigegeben).
2. Projektidee in ① einsetzen, Klärungsrunden fahren, Spec schreiben lassen. Auf die Invarianten achten: gibt es zu jeder Rechenfunktion mindestens eine?
3. Spec mit ② prüfen. Befunde annehmen oder verwerfen, überarbeitete Spec anfordern.
4. Mit ③ den Plan erstellen. Abschlussbericht lesen: welche Verhaltensannahmen wurden geprüft, was blieb ungeprüft, welche Prüfmittel sind festgelegt?
5. Mit ④ die Aufgaben ableiten. Auf die Zählung der Nachweisarten achten — ein hoher Handprüfungsanteil ist eine Vorwarnung. Steht T0 an erster Stelle, und trägt die Etappenübersicht Etappen, die in einem Lauf abschließbar sind?
6. Mit ⑤ abgleichen. Blockierer beseitigen, bevor die erste Zeile Code entsteht.
7. **T0 umsetzen und den leeren Prüfstand laufen lassen.** Er muss fehlschlagen. Schlägt er nicht fehl, misst er nichts. Diese eine Etappe wird gelesen, bevor irgendetwas anderes beginnt.
8. Etappen nacheinander mit ⑥ umsetzen. Nach jeder Etappe den Bericht lesen — besonders die Zeilen `Maßprüfung`, `Muster` und `Nicht geplant`. Die Empfehlung am Ende ist ein Vorschlag, keine Freigabe.
9. Mit ⑦ die Akten prüfen lassen.
10. **Selbst abnehmen**, am laufenden Produkt, mit der Liste im Bereich *Nach der Auslieferung*.
11. Befunde einordnen und in eine Korrektur- oder Änderungsrunde geben.
12. Bei Unterbrechung an beliebiger Stelle: ⑧.

---

## Wogegen das Set gebaut ist

Jede Prüfstelle existiert wegen eines konkreten Fehlers, nicht wegen eines Prinzips:

* eine Bibliotheksfunktion, deren Verhalten niemand geprüft hat, im Kern der Anwendung → ③ §3.4, ⑤, Verfassung §6
* eine Anwendung, die gebaut wird, aber im Auslieferungszustand nicht lädt → ③ §3.5 und §4, ④ §6
* grüne Tests bei mangelhafter Anwendung → ④ §2 und §3, ⑥ §4, ⑦ §2
* abgehakte Aufgaben, deren Kriterium niemand geprüft hat → ④ §3, ⑤, ⑥ §4
* eine Anforderung, die zwischen Idee und Spezifikation verschwindet → ① Rückverfolgung, ② §3.5
* ein Review, das Fehler einbaut statt sie zu finden → ② §1 und §2
* **Tests, die aus derselben Lesart stammen wie der Code, den sie prüfen sollen** → ① Invarianten, ② Härteprüfung, Betriebsregel „Das Maß schreibt nicht, wer daran gemessen wird"
* **eine Anwendung, die bis zur Abnahme kein einziges Mal bedient wurde** → ① Zustandskriterien, ③ §3.8, ④ T0, ⑥ Browserartefakte
* **ein Nachweis, der eine kaputte Umsetzung nicht bemerkt** → ③ §3.8, ④ Mutationsprüfung, ⑦ §2
* **eine Maßdatei, die von der gemessenen Instanz beschrieben wird** → ④ §4, ⑥ §3
* **ein Verfahren, das im Alltag nicht durchgehalten wird, weil es nach jedem Schritt einen Handstart verlangt** → ⑥ §1 und §5, ④ Etappenfeld
* **eine Prüfung, die dieselbe Messung wiederholt und deshalb immer besteht** → ⑦ §1
* **ein Nutzerbefund, der als Bugfix behandelt wird, obwohl er eine fehlende Anforderung ist** → ⑦ §3, ④ §8

---

# Nach der Auslieferung

*Dieser Bereich beschreibt, was nach der ersten fertigen Fassung passiert. Er ist bewusst vom Rest getrennt: bis hierher läuft das Set geradeaus, ab hier im Kreis. Wer das Set zum ersten Mal anwendet, kann diesen Teil überspringen, bis das erste Ergebnis vorliegt.*

## Warum es hier anders zugeht

Bis zur Auslieferung ist die Richtung eindeutig: aus der Idee wird eine Spezifikation, daraus ein Plan, daraus Aufgaben, daraus Code. Sobald jemand das Ergebnis benutzt, kommen Befunde zurück — und die haben keine eindeutige Richtung mehr. Ein und derselbe Satz („die Vorschau springt an die falsche Stelle") kann bedeuten, dass der Code falsch ist, dass das Kriterium zu schwach war, oder dass du dir inzwischen etwas anderes wünschst. Diese drei Fälle brauchen drei verschiedene Wege.

Wer sie vermischt, verliert die wichtigste Eigenschaft des Sets: dass das Maß nicht von dem geschrieben wird, der daran gemessen wird. Ein Wunsch, der als Fehlerbehebung durchgeht, landet ohne Spezifikation im Code. Eine Kriteriumslücke, die als Bugfix behandelt wird, führt dazu, dass die Umsetzung sich ihr Kriterium selbst zurechtlegt.

## Wer prüft was

**Die Maschine prüft die Akten.** ⑦ stellt fest, ob der erbrachte Nachweis trägt: existieren die Belege, prüfen die Tests das Kriterium, ist eine Toleranz stillschweigend aufgeweicht worden, hängt eine Erfüllung an einem Nebenpfad. Das ist mechanisch, objektiv und billig — und es ist das Einzige, was eine Instanz leisten kann, die nichts ändern darf und die Messung nicht selbst wiederholen soll.

**Der Mensch nimmt das Produkt ab.** Alles, was Urteil verlangt, bleibt bei dir. Der Grund ist nicht Misstrauen gegen die Technik, sondern eine belegte Schwäche: Modelle bewerten KI-erzeugte Arbeit systematisch zu wohlwollend, erkennen berechtigte Mängel und reden sie sich anschließend klein. Für Fragen wie „ist das bedienbar" gibt es kein grünes Häkchen, das diese Neigung ausgleicht.

### Abnahmeliste für den Menschen

Am gebauten, gestarteten Produkt, im Auslieferungszustand, ohne vorher ins Protokoll zu sehen:

1. **Erster Eindruck ohne Anleitung.** Öffne das Produkt und versuche, die Hauptaufgabe zu erledigen, ohne etwas nachzulesen. Wo du stockst, ist ein Befund — auch wenn alle Tests grün sind.
2. **Die Wege, die niemand aufgeschrieben hat.** Falsche Reihenfolge, Abbruch mittendrin, zweimal dasselbe, Zurück-Taste, Fenster verkleinern.
3. **Die Handprüfungsaufgaben.** Sie stehen im Laufprotokoll auf GELB und warten namentlich auf dich. Jede einzeln durchgehen und das Ergebnis eintragen — vorher ist die Runde nicht fertig.
4. **Die GELB-Anteile aus dem Etappenbericht.** Was hat die Umsetzung nicht belegen können, und stört es dich?
5. **Der Aktenbericht aus ⑦.** Erst jetzt lesen, sonst lenkt er den Blick.
6. **Die Frage, die alles zusammenfasst:** Würdest du dieses Produkt jemandem geben, für den du einstehst? Nur du kannst sie beantworten, und nur deine Antwort zählt als Freigabe.

## Die drei Klassen von Befunden

| Klasse | Was der Fall ist | Wohin |
| --- | --- | --- |
| **1 Mangel** | Ein bestehendes Akzeptanzkriterium ist verletzt. Das Maß war richtig, die Umsetzung nicht. | Korrekturrunde K über ④ §8.1 |
| **2 Kriteriumslücke** | Das Kriterium ist erfüllt, das Ergebnis trotzdem falsch. Das Maß hat nicht gemessen. | zurück zu ①, dann Änderungsrunde Ä |
| **3 Änderungswunsch** | Nichts ist verletzt, es wird etwas anderes gewünscht. | zurück zu ①, dann Änderungsrunde Ä |

**Die Probe ist einfach:** Lässt sich der Befund einem Akzeptanzkriterium zuordnen, das er verletzt? Wenn nein, ist er nicht Klasse 1 — egal wie sehr er sich nach einem Fehler anfühlt. Das ist die häufigste und folgenreichste Fehleinordnung.

**Klasse 2 hat eine Nachpflicht.** Ein Befund, den die Prüfmittel nicht bemerkt haben, hinterlässt nicht nur eine Korrektur, sondern eine Ergänzung am Maß: ein fehlender Zustand, eine fehlende Invariante, eine Verfälschung, die niemand gesetzt hat. Ohne diese Ergänzung wiederholt sich derselbe Fehler in der nächsten Runde, und du hast eine Suite, die Kennzahlen polstert statt zu messen. ⑦ benennt die Lücke, ① formuliert das Kriterium, ② prüft seine Härte.

---

## Was du konkret tust — drei Beispiele

**Vorweg der häufigste Irrtum:** Du änderst die Prompt-Dateien nicht. Sie enthalten die Modi bereits. Was sich unterscheidet, ist allein das, was du beim Aufruf dazuschreibst. Die folgenden drei Blöcke sind vollständige Aufrufe zum Abschreiben und Anpassen.

### Klasse 1 — Korrekturrunde K

*Beispiel: „Beim Speichern einer sehr großen Datei bleibt die Statuszeile leer." ⑦ hat das V10 zugeordnet: das Kriterium verlangt eine Kenntlichmachung während des Sicherns.*

**Schritt 1 — Aufgaben ableiten.** Frische Sitzung mit ④:

```
@constitution.md  @spec.md  @plan.md  @prompt-tasks.md

Korrekturmodus nach §8.1. Die spec.md gilt unverändert; erzeuge nur die
Etappe K aus der folgenden Befundliste.

### B1 — Klasse 1 — verletzt V10
Symptom:       Beim Sichern einer Datei über ca. 1 MB bleibt die Statuszeile
               leer, bis der Vorgang abgeschlossen ist.
Reproduktion:  Ordner öffnen, beispiel-gross.md laden, Speichern auslösen,
               Statuszeile während des Vorgangs beobachten.
Beleg:         test-report/bedienung/bedienung-schritt-6.png
Erwartet laut V10: Kenntlichmachung während des ausstehenden Sicherns.
```

Zurück kommen `K1a` (Reproduktionstest) und `K1b` (Behebung mit Bestandsschutz), dazu die Zuordnungstabelle und die Gesamtprüfung als letzte Aufgabe.

**Schritt 2 — umsetzen.** ⑥ unverändert, mit `Etappe: K`. Ein Lauf, ein Etappenbericht.

**Schritt 3 — prüfen und abnehmen.** ⑦ über die neuen Laufprotokolle, dann deine Abnahmeliste — beschränkt auf den betroffenen Bereich und einen Blick darauf, dass nichts anderes gelitten hat.

**⑤ entfällt in Korrekturrunden.** Prüfstelle B gleicht Spezifikation, Plan und Aufgaben gegeneinander ab; hier hat sich nur die Aufgabenliste geändert, und ihre Abdeckung steht in der Zuordnungstabelle. Bei mehr als etwa fünf Befunden in einer Runde lohnt sie trotzdem.

### Klasse 2 — Kriterium schärfen, dann Änderungsrunde Ä

*Beispiel: „Die Vorschau springt beim Tippen an die falsche Stelle." V11 ist erfüllt — das zugeordnete Element bleibt sichtbar —, aber bei Aufzählungen ist das zugeordnete Element das falsche. Das Kriterium hat den Fall nicht erfasst.*

**Schritt 1 — Kriterium schärfen.** Frische Sitzung mit ①:

```
@constitution.md  @spec.md  @metaprompt-spec-v3.md

Kein neues Projekt: Nachtrag zur bestehenden spec.md.

Klasse-2-Befund aus der Abnahme:
  Betroffenes Kriterium: V11
  Beobachtung:  V11 ist erfüllt — bei Eingabe bleibt das zugeordnete Element
                sichtbar. Innerhalb mehrzeiliger Aufzählungen ist das
                zugeordnete Element jedoch der Listenanfang statt des
                bearbeiteten Punktes.
  Lücke laut ⑦: V11 legt nicht fest, auf welcher Ebene zugeordnet wird.

Auftrag: Führe das Klärungsgespräch nur zu diesem Punkt. Schärfe V11 so,
dass eine falsche Umsetzung es verletzen würde, und prüfe dabei, ob eine
zusätzliche Invariante oder ein zusätzlicher Zustand nötig ist. Schreibe die
betroffenen Abschnitte der spec.md erst auf mein Kommando neu; alle übrigen
Abschnitte bleiben wörtlich unverändert.
```

Dann ② über den geänderten Ausschnitt — die Härteprüfung ist hier der eigentliche Punkt: ein Kriterium, das den Befund nicht gefangen hätte, ist nicht scharf genug.

**Schritt 2 — Prüfstand nachziehen.** ③ mit dem archivierten §3.8/§3.9 und dem Auftrag, für das geschärfte Kriterium Nachweisverfahren und, wo es rechnet, eine Verfälschung zu ergänzen. Das ist die Nachpflicht aus Klasse 2 — ohne sie wiederholt sich der Fall.

**Schritt 3 — Aufgaben, Umsetzung, Prüfung.** ④ im Änderungsmodus:

```
@constitution.md  @spec.md  @plan.md  @prompt-tasks.md

Änderungsmodus nach §8.2. Der Bestand ist umgesetzt und abgenommen.
Geändert wurden: V11 (geschärft), I6 (neu).
Erzeuge nur die Etappe Ä für diese beiden Kriterien; alle übrigen gelten
als erfüllt und stehen unter Bestandsschutz.
```

Danach ⑤ (diesmal ja — das Maß hat sich geändert), ⑥ mit `Etappe: Ä`, ⑦, Abnahme.

### Klasse 3 — neue Anforderung

*Beispiel: „Ich hätte gern eine Suchfunktion über alle Dateien des Ordners."*

Fast derselbe Weg wie Klasse 2 — mit drei Unterschieden, die in der Praxis viel ausmachen:

```
@constitution.md  @spec.md  @metaprompt-spec-v3.md

Kein neues Projekt: Erweiterung der bestehenden spec.md.

Klasse-3-Wunsch: Suche über alle Markdown-Dateien des geöffneten Ordners,
Treffer anspringbar.

Auftrag: Beginne wie vorgesehen mit einem begründeten Einwand gegen diese
Erweiterung — ich will wissen, was sie kostet, bevor ich sie bekomme. Führe
das Klärungsgespräch nur zu diesem Punkt, einschließlich der Zustände leer,
lädt, Fehler, Grenzwert und ungültige Eingabe. Prüfe, ob die Erweiterung
einem bestehenden Kriterium widerspricht, und sag es, statt es aufzulösen.
Schreibe erst auf mein Kommando, und nur die neuen Abschnitte.
```

**Unterschied 1: Der Einwand ist hier ernst gemeint.** Bei Klasse 2 ist der Befund der Beleg — das Kriterium hat nachweislich nicht gemessen, es gibt wenig zu diskutieren. Bei Klasse 3 hast du nur einen Wunsch, und jeder Wunsch vergrößert das Produkt. Das ist der Punkt, an dem aus einem scharfen kleinen Werkzeug ein unübersichtliches großes wird, eine Runde nach der anderen.

**Unterschied 2: Es gibt keine Nachpflicht am Prüfstand.** Bei Klasse 2 *musste* etwas fehlen, sonst wäre der Befund aufgefallen. Bei Klasse 3 hat nichts versagt; der Prüfstand wächst nur, wenn die neue Anforderung Rechenlogik oder Zustände mitbringt.

**Unterschied 3: Das Widerspruchsrisiko liegt anders.** Ein geschärftes Kriterium (Klasse 2) kann bereits abgenommenes Verhalten nachträglich ungültig machen — deshalb steht die Frage danach im Auftrag. Eine neue Anforderung (Klasse 3) kollidiert eher mit einer bestehenden, als dass sie sie aufhebt.

Ab Schritt 2 laufen beide identisch: ② prüft, ③ zieht den Plan nach, ④ erzeugt die Etappe Ä, ⑥ setzt um, ⑦ prüft die Akten, du nimmst ab.

**Und in beiden Fällen gilt:** Klasse-2- und Klasse-3-Befunde nicht in dieselbe Runde mischen. Sonst lässt sich hinterher nicht mehr sagen, ob die Schärfung gewirkt hat oder ob die neue Funktion den alten Fall nur verdeckt.

---

## Der Korrekturloop

```
   Nutzung / Abnahme ──► Befunde
                            │
                            ▼
                    ⑦  Einordnung 1 / 2 / 3
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
     Klasse 1            Klasse 2            Klasse 3
        │                   │                   │
   ④ §8.1               ① Kriterium         ① neue
   Etappe K              schärfen            Anforderung
        │                   │                   │
        │                   └────────┬──────────┘
        │                            ▼
        │                    ② ③ ④ §8.2 ⑤
        │                            │
        ▼                            ▼
   ⑥ Etappe K                  ⑥ Etappe Ä
        │                            │
        └──────────► ⑦ ──► Abnahme ◄─┘
```

Eine **Korrekturrunde** ist keine Sonderform, sondern eine Etappe mit zwei bis acht Aufgaben. ⑥ bleibt unverändert. Je Befund entsteht ein Paar: erst ein Test, der das gemeldete Symptom reproduziert (Verfassung §5), dann die Behebung, deren Fertigkriterium außer dem neuen Test ausdrücklich den **Bestandsschutz** verlangt — die vollständige bestehende Suite bleibt grün. Am Ende steht die Gesamtprüfung aus ④ §6, unverändert.

## Das Persistenzmodell: Living Spec

Für die Frage, wo eine Änderung zuerst landet, gibt es drei gängige Modelle. *Flow-forward* legt für jede Folgeänderung ein neues Spezifikationsverzeichnis an und behält das alte als historischen Beleg. *Living Spec* macht die `spec.md` zum Vertrag; Plan und Aufgaben werden aus ihr neu erzeugt, sobald sich das beabsichtigte Verhalten ändert. *Flow-back* erlaubt die erste Änderung dort, wo die Erkenntnis anfällt, und richtet die übrigen Dokumente danach wieder aus.

**Dieses Set ist ein Living Spec.** Genau deshalb sind `plan.md` und `tasks.md` flüchtig und genau deshalb werden §3.8 und §3.9 archiviert: eine Korrektur- oder Änderungsrunde setzt auf dem archivierten Prüfstand auf und erzeugt Plan und Aufgaben neu.

**Flow-back ist ausgeschlossen.** Es ist das Modell, in dem eine tiefere Änderung im Code oder in den Aufgaben stehenbleibt, während die Spezifikation noch etwas anderes sagt — und damit genau die Betriebsart, die die wichtigste Regel dieses Sets leise aushebelt.
