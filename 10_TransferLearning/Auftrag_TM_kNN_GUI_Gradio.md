# Auftrag: Oberfläche für den Bildklassifikator — Variante A (Gradio)

> **So nutzen Sie dieses Blatt:** Dies ist eine **neue Runde** durch den Software-Lebenszyklus.
> Ihr kNN-Projekt hat Phase 6 (Betrieb & Weiterentwicklung) erreicht — die neue Anforderung
> „bedienbare Oberfläche" stößt einen neuen Durchlauf ab **Phase 1** an. Arbeiten Sie wieder
> nach SDD, diesmal aber die **vollständige** Abfolge inklusive Tests (Schritt 5). Dieses Blatt
> ist Ihre „vage Idee" für den Metaprompt aus Schritt 1.

## Kontext und Motivation

Ihr kNN-Notebook funktioniert — aber es hat keine Oberfläche. Man muss Zellen ausführen und
Code verstehen. Ein echter Klassifikator braucht eine Fläche, auf der jemand ein Bild auswählt
und eine Antwort bekommt, **ohne den Code zu berühren**.

In dieser Runde legen Sie eine grafische Oberfläche mit **Gradio** über Ihre *bestehende*
Klassifikationslogik. Sie bauen nichts am ML-Kern neu — Sie ergänzen ein Feature.

## Ziel

Eine Gradio-Anwendung (lauffähig aus dem bzw. neben dem Notebook), in der eine Person ein Bild
auswählt und Folgendes sieht: die **vorhergesagte Klasse**, die **Konfidenz** und die
**nächsten Nachbarn**, die zu dieser Entscheidung geführt haben.

## Rahmenbedingungen (fest — hier entscheiden Sie nichts)

- **Aufsetzen, nicht neu bauen:** Die Klassifikationslogik stammt aus Ihrem kNN-Notebook und
  bleibt unverändert (MobileNetV2 eingefroren, kNN, bekannter Datenvertrag).
- **Oberfläche mit Gradio** (Python), im oder neben dem Notebook lauffähig.
- **Trennung Logik ↔ Oberfläche (zentral):** Die Klassifikationslogik lebt in einer aufrufbaren
  Funktion — z. B. `klassifiziere(bild) → (klasse, konfidenz, nachbarn)`. Die GUI **ruft diese
  Funktion nur auf** und stellt das Ergebnis dar. Keine ML-Logik im Oberflächen-Code.
- **Sprache:** deutsch, in Oberfläche und Code.

## Gegeben

- Ihr lauffähiges **kNN-Notebook** aus dem ersten Auftrag.
- Die bekannte **Datenstruktur** (`Datasets/Train|Test/<Klasse>`, 224 × 224 RGB).

## Was die fertige Anwendung leisten muss (Verhaltens-Ebene)

Das *Was* — das *Wie* (Layout, Widgets, Aufbau) erarbeiten Sie in Ihrer Spec.

- ein Bild entgegennehmen (Auswahl oder Upload),
- Klasse und Konfidenz anzeigen,
- die nächsten Nachbarn nachvollziehbar zeigen — die kNN-Idee soll auch in der Oberfläche
  **sichtbar** bleiben,
- ungültige oder leere Eingaben verständlich abfangen.

## Qualität & Tests (Phase 4 wird jetzt echt)

Anders als beim Notebook prüfen Sie jetzt **Verhalten**. Das gehört in die Spec und wird getestet.

- In die `spec.md` gehören **Akzeptanzkriterien** („die App muss …") — das ist Ihre Grundlage
  für Phase 4.
- Schreiben Sie **Tests für die Logik-Funktion** (pytest), **nicht** für die Oberfläche.
- **Leitplanken:** Tests prüfen Vertrag und Verhalten — gültiges Klassenlabel, erwartete
  Ausgabeform, stabile Zuordnung eines bekannten Trainingsbildes, sauberes Abfangen leerer
  Eingaben. **Keine** Genauigkeits-Schwellwerte als Test (das ist Modell-Evaluation aus Phase 3,
  nicht Verifikation aus Phase 4).
- **Steigerung:** Tests *zuerst* schreiben (sie schlagen fehl → rot), dann implementieren, bis
  sie grün sind — echtes Test-Driven Development.

## Ausdrücklich nicht Teil dieses Auftrags

- kein Retraining des Netzes, kein Dense-Kopf,
- kein Web-Export, kein Hosting,
- keine Oberflächen-Testframeworks.

## Ihr Vorgehen (SDD, vollständig)

Metaprompt aus Schritt 1 mit diesem Blatt als Idee → `spec.md` **mit Akzeptanzkriterien** →
`plan.md` (Gradio) → `tasks.md` → **Tests** → Implementierung.

**Heben Sie Ihre `spec.md` gut auf — Sie brauchen sie in der nächsten Runde wieder.**

Abgabe: `spec.md`, `plan.md`, `tasks.md`, Tests, lauffähige Gradio-App.
