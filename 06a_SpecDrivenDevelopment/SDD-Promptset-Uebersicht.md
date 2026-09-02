# SDD-Promptset — Übersicht und Kurzanleitung

*Stand 02.09.2026. Acht Prompts, vier Projektdokumente, drei Prüfstellen.*

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
   ⑥  Umsetzungs-Prompt ───────► Code, je Aufgabe eine Sitzung
          │
   ⑦  Prüfstelle C ────────────► Abnahme am gebauten Artefakt
          │
   ⑧  Übergabe / Wiederaufnahme  (quer zu allem, bei Unterbrechung)
```

**Zwei Gattungen von Dokumenten, mit einer Ausnahme.** `constitution.md` und `spec.md` sind dauerhaft — sie überleben den Code. `plan.md` und `tasks.md` sind flüchtig. Ausgenommen sind **§3.8 (Prüfbefehle) und §3.9 (Nachweistabelle)** des Plans: sie werden beim Verwerfen als Anhang zur `spec.md` gesichert. Begründung: Diese beiden Abschnitte tragen das Abnahmesignal. Wer sie wegwirft, kann bei der nächsten Änderung nicht mehr feststellen, woran ein Kriterium ursprünglich gemessen wurde, und muss das Orakel neu erfinden — meist von derselben Instanz, die den Code schreibt. Genau das soll das Set verhindern.

**Die Trennlinie zwischen Spec und Plan ist die wichtigste Regel des Sets.** Die Spezifikation sagt was und warum, in Fachsprache, ohne Technologie, ohne Bibliotheken, ohne Code. Der Plan sagt wie. Steht Technik in der Spec, ist das ein Mangel, keine Vorgabe.

**Vorsteuerung und Rückmeldung.** `constitution.md`, `spec.md` und `plan.md` steuern vor: sie erhöhen die Wahrscheinlichkeit, dass etwas Richtiges entsteht. Prüfbefehle, Testläufe und die drei Prüfstellen melden zurück: sie stellen fest, was tatsächlich entstanden ist. Ein Set, das nur vorsteuert, erzeugt gut begründete Fehler. Die Prüfstellen sind Rückmeldung an Sitzungsgrenzen; die Prüfbefehle sind Rückmeldung im Lauf. Beides wird gebraucht.

---

## Die acht Prompts

| # | Datei | Wann | Eingaben | Ergebnis |
| --- | --- | --- | --- | --- |
| ① | `metaprompt-spec-v3.md` | Projektstart | Projektidee | `spec.md` |
| ② | `review-prompt-A-spec.md` | nach ① | constitution, spec, Projektidee | Befundbericht, Urteil |
| ③ | `prompt-plan.md` | nach Freigabe ② | constitution, spec | `plan.md` |
| ④ | `prompt-tasks.md` | nach ③ | constitution, spec, plan | `tasks.md` |
| ⑤ | `review-prompt-B-abgleich.md` | nach ④ | alle vier Dokumente | Abdeckungstabelle, Urteil |
| ⑥ | `prompt-umsetzung.md` | je Aufgabe | alle vier + Aufgabennummer | Code + Ampelbericht |
| ⑦ | `review-prompt-C-abnahme.md` | nach der Umsetzung | alle vier + Projekt | Erfüllungstabelle, Urteil |
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

**§3.9 bleibt erhalten.** Die Nachweistabelle wird beim Verwerfen des Plans zusammen mit §3.8 archiviert. Bei jedem Kriterium, für das nur Handprüfung bliebe, prüft der Plan zuerst, ob die Browsersteuerung es abdeckt.

### ④ Tasks-Prompt — Zerlegung

Leitet die Arbeitsschritte ab. Test- und Umsetzungsaufgaben treten paarweise auf: erst die Tests, deren Fertigkriterium ausdrücklich das **Fehlschlagen** ist, dann die Umsetzung, bis sie grün sind.

**T0 ist immer der Prüfstand.** Die erste Aufgabe jedes Projekts baut nicht Fachlichkeit, sondern die Messeinrichtung: Umgebung, Prüfbefehle, Browsersteuerung, Mutationsbefehl. Ihr Fertigkriterium ist ein Lauf des leeren Prüfstands mit **erwartetem Fehlschlag** — rot aus dem richtigen Grund. Das ergänzt das leere Gerüst aus ③ §4 um die Rückmeldeseite: dort wird geprüft, dass etwas *baut und startet*, hier, dass etwas *misst*.

**Testaufgaben tragen die Mutationsprüfung als zweites Fertigkriterium**, wo der Plan sie vorsieht. Ein Test, der eine verfälschte Umsetzung nicht bemerkt, ist noch nicht fertig — auch wenn er fehlschlägt und später grün wird.

*Worauf es ankommt:* Kein Häkchen, sondern ein Statusfeld mit GRÜN, GELB und ROT. Jede Aufgabe muss in einem Kontextfenster umsetzbar und prüfbar sein.

### ⑤ Prüfstelle B — Abgleich vor der Umsetzung

Frische Sitzung, read-only. Prüft die vier Dokumente gegeneinander: Ist jedes Kriterium durch eine Aufgabe abgedeckt? Verweist jede Aufgabe auf ein Kriterium? Sind Handprüfungen als solche gekennzeichnet? Sind Verhaltensannahmen belegt? Existiert T0, und misst der Prüfstand das, was die Nachweistabelle verlangt?

*Worauf es ankommt:* Ein Kriterium, das automatisch prüfbar aussieht, aber Handprüfung braucht, ist ein Blockierer — es wird sonst abgehakt, ohne erfüllt zu sein.

### ⑥ Umsetzungs-Prompt — eine Aufgabe

Je Sitzung genau eine Aufgabe. Bericht mit Ampel und wörtlicher Befehlsausgabe.

*Worauf es ankommt:* Kein Test wird geändert, damit er grün wird. Kein Kriterium wird abgeschwächt. Handprüfungsaufgaben enden immer GELB. Keine Behauptung ohne Ausgabe.

**Kein Ergebnis ohne Ausgabe gilt auch für die Oberfläche.** Bei Aufgaben mit Nachweisart *browsergestützt* endet die Sitzung nicht am Testbericht, sondern an der laufenden Anwendung. Der Bericht nennt die erzeugten Artefakte mit Pfad und zitiert die Browserkonsole. „Die Ansicht funktioniert" ist eine Behauptung; ein Snapshot und eine leere Fehlerkonsole sind ein Nachweis.

### ⑦ Prüfstelle C — Abnahme

Frische Sitzung, anderes Modell, read-only. Beginnt beim **gebauten, gestarteten Artefakt** und sieht erst danach in den Code. Prüft die Tests darauf, ob sie das Kriterium prüfen oder nur die Umsetzung wiederholen.

Zwei zusätzliche Befunde:

* **Führt der Nachweis durch den Auslieferungspfad?** Oder gibt es einen Pfad, den es nur für die Prüfung gibt — eine Demoseite, einen Testmodus, eine Abkürzung, die im ausgelieferten Zustand niemand erreicht? Ein Kriterium, das nur auf einem Nebenpfad erfüllt ist, gilt als nicht erfüllt.
* **Hält der Nachweis einer Verfälschung stand?** C setzt eine gezielte Verfälschung in die Kernlogik und stellt fest, ob die Prüfmittel anschlagen. Tun sie es nicht, ist der Befund nicht „ein Test fehlt", sondern „die Erfüllungstabelle ist unbelegt". Die Verfälschung wird anschließend zurückgenommen und der Vorgang im Bericht dokumentiert.

*Worauf es ankommt:* Die Statusfelder in `tasks.md` sind Behauptungen. Die Abweichung zwischen Bericht und Wirklichkeit ist der wertvollste Befund.

### ⑧ Übergabe und Wiederaufnahme

Zwei zusammengehörige Prompts für Sitzungsgrenzen. Der erste stellt den Zustand fest (nicht: erinnert ihn) und schreibt ihn auf. Der zweite misst beim Wiedereinstieg nach und meldet Abweichungen zuerst.

---

## Betriebsregeln

* **Prüfstellen laufen in frischer Sitzung und mit einem anderen Modell** als das prüfende Werk. Ein unbelasteter Kontext findet, was der Autor übersieht.
* **Das Maß schreibt nicht, wer daran gemessen wird.** Akzeptanzkriterien, Invarianten und Nachweistabelle entstehen vor der Umsetzung und außerhalb ihrer Sitzung. Die umsetzende Instanz darf sie lesen, nicht ändern. Ein Änderungswunsch geht über dich zurück an die Stelle, an der das Maß entstanden ist.
* **Was nicht gemessen wurde, ist nicht erfüllt.** Ein Prüfmittel, das eine absichtlich verfälschte Umsetzung nicht bemerkt, zählt nicht als Nachweis.
* **Prüfinstanzen ändern nichts.** Sie berichten. Was zurück ins Werk soll, geht über dich.
* **Eine Aufgabe, eine Sitzung, ein Bericht.**
* **Nach drei erfolglosen Versuchen an derselben Aufgabe: Abbruch und ROT.**
* **GELB ist ein zulässiges und ehrliches Ergebnis.** Ein GRÜN, das nicht trägt, ist teurer als ein GELB, das die Lücke benennt.
* **Die Freigabe unterschreibt ein Mensch.** Prüfung durch ein Modell ist Unterstützung, kein Ersatz.

---

## Ein Durchlauf von null

1. `constitution.md` bereitlegen (Version 1.2 oder höher).
2. Projektidee in ① einsetzen, Klärungsrunden fahren, Spec schreiben lassen. Auf die Invarianten achten: gibt es zu jeder Rechenfunktion mindestens eine?
3. Spec mit ② prüfen. Befunde annehmen oder verwerfen, überarbeitete Spec anfordern.
4. Mit ③ den Plan erstellen. Abschlussbericht lesen: welche Verhaltensannahmen wurden geprüft, was blieb ungeprüft, welche Prüfmittel sind festgelegt?
5. Mit ④ die Aufgaben ableiten. Auf die Zählung der Nachweisarten achten — ein hoher Handprüfungsanteil ist eine Vorwarnung. Steht T0 an erster Stelle?
6. Mit ⑤ abgleichen. Blockierer beseitigen, bevor die erste Zeile Code entsteht.
7. **T0 umsetzen und den leeren Prüfstand laufen lassen.** Er muss fehlschlagen. Schlägt er nicht fehl, misst er nichts.
8. Aufgaben einzeln mit ⑥ umsetzen. Nach jeder Aufgabe den Bericht lesen, nicht nur den Status.
9. Mit ⑦ abnehmen.
10. Bei Unterbrechung an beliebiger Stelle: ⑧.

---

## Wogegen das Set gebaut ist

Jede Prüfstelle existiert wegen eines konkreten Fehlers, nicht wegen eines Prinzips:

* eine Bibliotheksfunktion, deren Verhalten niemand geprüft hat, im Kern der Anwendung → ③ §3.4, ⑤, Verfassung §6
* eine Anwendung, die gebaut wird, aber im Auslieferungszustand nicht lädt → ③ §3.5 und §4, ⑦ §2
* grüne Tests bei mangelhafter Anwendung → ④ §2, ⑥ §3, ⑦ §3.5
* abgehakte Aufgaben, deren Kriterium niemand geprüft hat → ④ §3, ⑤, ⑥ §3
* eine Anforderung, die zwischen Idee und Spezifikation verschwindet → ① Rückverfolgung, ② §3.5
* ein Review, das Fehler einbaut statt sie zu finden → ② §1 und §2
* **Tests, die aus derselben Lesart stammen wie der Code, den sie prüfen sollen** → ① Invarianten, ② Härteprüfung, Betriebsregel „Das Maß schreibt nicht, wer daran gemessen wird"
* **eine Anwendung, die bis zur Abnahme kein einziges Mal bedient wurde** → ① Zustandskriterien, ③ §3.8, ④ T0, ⑥ Browserartefakte
* **ein Nachweis, der eine kaputte Umsetzung nicht bemerkt** → ③ §3.8, ④ Mutationsprüfung, ⑦ Verfälschungsprobe

---

## Herkunft der Ergänzungen vom 02.09.2026

Die letzten drei Zeilen des vorstehenden Abschnitts stammen aus einem beobachteten Projektverlauf und decken sich mit dem, was seit Anfang 2026 an Praxisberichten dazu vorliegt.

**Beobachtung.** Eine kleine Web-App zur Auflösung physikalischer Formeln, umgesetzt in einer Editor-Umgebung mit getrennten Modellen für Spec/Plan und Tasks/Umsetzung. Die umsetzende Instanz nutzte ein Browser-Testframework und meldete grün; die erste fertige Version enthielt schwere Bedienfehler und benötigte etliche Korrekturrunden für einen MVP-Zustand. Dieselbe Codebasis, an eine Umgebung mit ausführbarem Prüfstand übergeben, förderte die Mängel binnen eines Durchlaufs zutage und erreichte Auslieferungsreife.

**Einordnung.** Die Diagnose ist nicht „das schwächere Modell". In der Praxisliteratur wird der Unterschied dem Harness zugeschrieben — allem an einem Agenten außer dem Modell. Birgitta Böckeler (Thoughtworks) unterteilt dessen Regelungsbereiche in Wartbarkeit, Architekturkonformität und Verhalten und bezeichnet den dritten als den Elefanten im Raum: Verhaltensprüfung stützt sich weitgehend auf agentengenerierte Tests, und ein Agent, der die Anforderung missversteht, erzeugt Tests, die sein Missverständnis bestätigen. Untersuchungen zu LLM-erzeugten Orakeln zeigen dasselbe Muster: die Zusicherungen bilden eher das tatsächliche als das beabsichtigte Verhalten ab, wodurch Fehler als Sollverhalten festgeschrieben werden. Als Gegenmittel gilt ein Abnahmesignal, das die umsetzende Instanz nicht selbst schreiben kann, sowie eine Trennung von umsetzender und prüfender Rolle.

**Warum diese drei Mittel.** Invarianten lösen das Problem, dass niemand alle Sollwerte kennt — sie sind ohne Kenntnis des Ergebnisses formulierbar und nicht nachträglich anpassbar. Die Mutationsprüfung beantwortet die einzige Frage, die Testabdeckung nicht beantwortet: würde diese Suite einen echten Fehler bemerken? Sie wird für agentengeschriebene Tests inzwischen als Gatter empfohlen, weil ein niedriger Wert ein starkes Signal dafür ist, dass eine Suite Kennzahlen polstert. Und die agentengesteuerte Browsersteuerung schließt die Lücke, die deine Nachweisart *browsergestützt* zwar vorsah, aber praktisch nie erreichte: sie erzeugt maschinenlesbare Belege, sodass die umsetzende Instanz nicht mehr nur Erfolg behaupten, sondern ihn belegen muss.

**Was das Set schon vorher richtig hatte** und was durch die Praxisberichte bestätigt wird: getrennte Prüfrollen in frischer Sitzung mit anderem Modell, die Abnahme am gestarteten Artefakt vor dem Blick in den Code, die ausdrückliche Frage, ob ein Test das Kriterium prüft oder die Umsetzung wiederholt, und das Verbot, einen Test anzupassen, damit er grün wird.
