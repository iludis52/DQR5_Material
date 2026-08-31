# SDD-Promptset — Übersicht und Kurzanleitung

*Stand 31.08.2026. Acht Prompts, vier Projektdokumente, drei Prüfstellen.*

---

## Die Kette

```
   constitution.md  (dauerhaft, projektübergreifend)
          │
   ①  Metaprompt ─────────────► spec.md        ← dauerhaft, rein fachlich
          │
   ②  Prüfstelle A ────────────► Freigabe der spec.md
          │
   ③  Plan-Prompt ─────────────► plan.md       ← flüchtig, alles Technische
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

**Zwei Gattungen von Dokumenten.** `constitution.md` und `spec.md` sind dauerhaft — sie überleben den Code. `plan.md` und `tasks.md` sind flüchtig; nach abgeschlossener Umsetzung dürfen sie verworfen werden.

**Die Trennlinie zwischen Spec und Plan ist die wichtigste Regel des Sets.** Die Spezifikation sagt was und warum, in Fachsprache, ohne Technologie, ohne Bibliotheken, ohne Code. Der Plan sagt wie. Steht Technik in der Spec, ist das ein Mangel, keine Vorgabe.

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

Führt ein Klärungsgespräch und schreibt daraus die `spec.md`. Prüft die Projektidee zuerst intern gegen elf Punkte, ohne die Liste zu zeigen, und stellt daraus höchstens fünf Fragen pro Runde, einzeln und nach Wirkung sortiert. Akzeptanzkriterien entstehen in EARS-Notation.

*Worauf es ankommt:* Vor der ersten Frage steht ein begründeter Einwand gegen die Produktidee selbst. Und: die Spec wird erst auf ausdrückliches Kommando geschrieben.

### ② Prüfstelle A — Review der Spezifikation

Frische Sitzung, anderes Modell. Prüft Testbarkeit der Kriterien, Erreichbarkeit der Inhalte mit dem festgelegten Bedienmodell, Vollständigkeit der Rückverfolgung.

*Worauf es ankommt:* Die Prüfinstanz **schlägt vor und entscheidet nicht**. Sie korrigiert nichts selbst, und sie stellt keine Behauptungen über das Verhalten fremder Software auf.

### ③ Plan-Prompt — technische Festlegungen

Erzeugt den Umsetzungsplan: Technologiewahl, Abhängigkeiten mit belegten Versionen, Datenformate, Struktur, Auslieferung.

*Worauf es ankommt:* §3.4 — Verhaltensannahmen über Bibliotheken werden **beim Schreiben des Plans ausgeführt**, nicht später geglaubt. §3.9 — jedes Akzeptanzkriterium bekommt hier sein Nachweisverfahren. §4 — bei neuen Projekten zuerst ein leeres Gerüst bauen und aufrufen.

### ④ Tasks-Prompt — Zerlegung

Leitet die Arbeitsschritte ab. Test- und Umsetzungsaufgaben treten paarweise auf: erst die Tests, deren Fertigkriterium ausdrücklich das **Fehlschlagen** ist, dann die Umsetzung, bis sie grün sind.

*Worauf es ankommt:* Kein Häkchen, sondern ein Statusfeld mit GRÜN, GELB und ROT. Jede Aufgabe muss in einem Kontextfenster umsetzbar und prüfbar sein.

### ⑤ Prüfstelle B — Abgleich vor der Umsetzung

Frische Sitzung, read-only. Prüft die vier Dokumente gegeneinander: Ist jedes Kriterium durch eine Aufgabe abgedeckt? Verweist jede Aufgabe auf ein Kriterium? Sind Handprüfungen als solche gekennzeichnet? Sind Verhaltensannahmen belegt?

*Worauf es ankommt:* Ein Kriterium, das automatisch prüfbar aussieht, aber Handprüfung braucht, ist ein Blockierer — es wird sonst abgehakt, ohne erfüllt zu sein.

### ⑥ Umsetzungs-Prompt — eine Aufgabe

Je Sitzung genau eine Aufgabe. Bericht mit Ampel und wörtlicher Befehlsausgabe.

*Worauf es ankommt:* Kein Test wird geändert, damit er grün wird. Kein Kriterium wird abgeschwächt. Handprüfungsaufgaben enden immer GELB. Keine Behauptung ohne Ausgabe.

### ⑦ Prüfstelle C — Abnahme

Frische Sitzung, anderes Modell, read-only. Beginnt beim **gebauten, gestarteten Artefakt** und sieht erst danach in den Code. Prüft die Tests darauf, ob sie das Kriterium prüfen oder nur die Umsetzung wiederholen.

*Worauf es ankommt:* Die Statusfelder in `tasks.md` sind Behauptungen. Die Abweichung zwischen Bericht und Wirklichkeit ist der wertvollste Befund.

### ⑧ Übergabe und Wiederaufnahme

Zwei zusammengehörige Prompts für Sitzungsgrenzen. Der erste stellt den Zustand fest (nicht: erinnert ihn) und schreibt ihn auf. Der zweite misst beim Wiedereinstieg nach und meldet Abweichungen zuerst.

---

## Betriebsregeln

* **Prüfstellen laufen in frischer Sitzung und mit einem anderen Modell** als das prüfende Werk. Ein unbelasteter Kontext findet, was der Autor übersieht.
* **Prüfinstanzen ändern nichts.** Sie berichten. Was zurück ins Werk soll, geht über dich.
* **Eine Aufgabe, eine Sitzung, ein Bericht.**
* **Nach drei erfolglosen Versuchen an derselben Aufgabe: Abbruch und ROT.**
* **GELB ist ein zulässiges und ehrliches Ergebnis.** Ein GRÜN, das nicht trägt, ist teurer als ein GELB, das die Lücke benennt.
* **Die Freigabe unterschreibt ein Mensch.** Prüfung durch ein Modell ist Unterstützung, kein Ersatz.

---

## Ein Durchlauf von null

1. `constitution.md` bereitlegen (Version 1.2 oder höher).
2. Projektidee in ① einsetzen, Klärungsrunden fahren, Spec schreiben lassen.
3. Spec mit ② prüfen. Befunde annehmen oder verwerfen, überarbeitete Spec anfordern.
4. Mit ③ den Plan erstellen. Abschlussbericht lesen: welche Verhaltensannahmen wurden geprüft, was blieb ungeprüft?
5. Mit ④ die Aufgaben ableiten. Auf die Zählung der Nachweisarten achten — ein hoher Handprüfungsanteil ist eine Vorwarnung.
6. Mit ⑤ abgleichen. Blockierer beseitigen, bevor die erste Zeile Code entsteht.
7. Aufgaben einzeln mit ⑥ umsetzen. Nach jeder Aufgabe den Bericht lesen, nicht nur den Status.
8. Mit ⑦ abnehmen.
9. Bei Unterbrechung an beliebiger Stelle: ⑧.

---

## Wogegen das Set gebaut ist

Jede Prüfstelle existiert wegen eines konkreten Fehlers, nicht wegen eines Prinzips:

* eine Bibliotheksfunktion, deren Verhalten niemand geprüft hat, im Kern der Anwendung → ③ §3.4, ⑤, Verfassung §6
* eine Anwendung, die gebaut wird, aber im Auslieferungszustand nicht lädt → ③ §3.5 und §4, ⑦ §2
* grüne Tests bei mangelhafter Anwendung → ④ §2, ⑥ §3, ⑦ §3.5
* abgehakte Aufgaben, deren Kriterium niemand geprüft hat → ④ §3, ⑤, ⑥ §3
* eine Anforderung, die zwischen Idee und Spezifikation verschwindet → ① Rückverfolgung, ② §3.5
* ein Review, das Fehler einbaut statt sie zu finden → ② §1 und §2
