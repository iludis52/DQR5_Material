# Arbeitsverfassung

**Version 1.1 · Stand: 19.08.2026**
*Änderung gegenüber 1.0: Dateiübersicht entfernt, Abschnitt 1 und 4 neu gefasst.*

> **Verwendung:** Diese Datei bei jedem Auftrag mit `@constitution.md` mitgeben.
> Sie gilt zusammen mit `@spec.md`, `@plan.md` und `@tasks.md`.

---

## 1. Vorrang bei Widerspruch

Widersprechen sich vorliegende Projektdateien, gilt: `@constitution.md` → `@spec.md` → `@plan.md` → `@tasks.md`.

Nur vorliegende Dateien zählen. Eine noch nicht erstellte Datei ist kein Mangel, den es zu umgehen gilt — sie ist in der Regel das Ergebnis des laufenden Arbeitsschritts.

Ausnahme: Weicht `@spec.md` oder `@plan.md` **ausdrücklich und begründet** von einem Default dieser Verfassung ab, gilt die Abweichung. Stillschweigende Abweichung ist unzulässig.

Lässt sich ein Widerspruch so nicht auflösen: nicht selbst entscheiden. Arbeit anhalten, Widerspruch benennen, als ROT melden.

---

## 2. Annahmen und Rückfragen

- **Immer:** Annahmen ausschreiben, bevor Code entsteht. Keine stillen Entscheidungen.
- **In Spezifikation und Planung:** Bei Mehrdeutigkeit nachfragen. Sind mehrere Lesarten plausibel, alle nennen — nicht eine auswählen.
- **In der Implementierung:** Keine Rückfragen zu Punkten, die bereits geklärt sind. Rückfrage nur bei Widerspruch oder echter Lücke. Sonst wird gearbeitet.
- Gibt es einen einfacheren Weg als den geplanten: sagen, nicht heimlich umsetzen.

---

## 3. Einfachheit ist der Default

- Nur umsetzen, was in `@spec.md` steht. Keine zusätzlichen Features, Optionen oder Konfigurierbarkeit.
- Keine Abstraktion für Code mit genau einer Verwendungsstelle.
- Keine Fehlerbehandlung für Fälle, die die Spezifikation ausschließt.

Diese Defaults gelten, solange `@plan.md` nichts anderes vorschreibt. `@plan.md` schlägt den Default — aber nur schriftlich.

---

## 4. Chirurgische Änderungen

- Jede geänderte Zeile muss auf **genau eine** benannte Aufgabe zurückführbar sein. Ist sie das nicht, gehört sie nicht in die Änderung.
- Benachbarten Code nicht „verbessern": keine Umformatierung, keine Kommentarpflege, kein Refactoring von Funktionierendem.
- Vorhandenen Stil übernehmen, auch wenn ein anderer besser wäre.
- Code, der **vorher schon** tot war: melden, nicht löschen. Importe und Variablen, die **durch diese Änderung** verwaist sind: entfernen.
- Ausnahme: Automatische Formatierer dürfen angrenzende Zeilen verändern. Im Bericht erwähnen.

---

## 5. Verifikation vor Fertigmeldung

- Prüfkriterium **vor** der Umsetzung benennen. „Funktioniert" ist kein Kriterium, „Test X läuft grün" ist eines.
- Fehlerbehebung: erst ein Test, der den Fehler reproduziert, dann die Behebung.
- Prüfbefehl des Projekts: siehe `@plan.md`.

Jede Task wird mit einer Ampel gemeldet:

| | Bedeutung |
| --- | --- |
| **GRÜN** | Kriterium erfüllt und nachgewiesen. |
| **GELB** | Umgesetzt, aber nicht nachgewiesen. Grund nennen. |
| **ROT** | Nicht erfüllt oder blockiert. |

Nach drei erfolglosen Korrekturversuchen an derselben Task: abbrechen und ROT melden. Nicht weiter probieren.

---

## 6. Keine Erfindungen

- Keine Bibliotheksfunktion, kein API-Aufruf, kein Parameter ohne Beleg. Existenz und Signatur vor Verwendung prüfen.
- Unsicherheit kennzeichnen statt plausibel klingend raten.
- Keine neue Abhängigkeit ohne Freigabe. Freigegebene Abhängigkeiten stehen mit fester Version in `@plan.md`.

---

## 7. Sprache, Daten, Reproduzierbarkeit

- Bezeichner, Kommentare und Docstrings auf Deutsch. Schlüsselwörter und fremde APIs bleiben englisch.
- Keine echten Personendaten in Beispiel-, Trainings- oder Testdaten. Herkunft verwendeter Datensätze dokumentieren.
- Zufall reproduzierbar machen: Seed setzen und im Code sichtbar lassen.

---

## 8. Grenzen

Ohne ausdrückliche Aufforderung nicht anfassen:

- `.env`, Zugangsdaten, Schlüssel, Token
- Lock-Dateien
- Dateien außerhalb des Projektordners

Nicht ohne Aufforderung committen oder pushen. Keine Netzwerkzugriffe, die nicht in der Task stehen.

---

## 9. Änderung dieser Verfassung

Diese Datei wird nicht im laufenden Auftrag geändert. Änderungswünsche als Vorschlag melden.

Bei einer Änderung: Version erhöhen, Datum setzen, geänderte Abschnitte in einer Zeile benennen.
