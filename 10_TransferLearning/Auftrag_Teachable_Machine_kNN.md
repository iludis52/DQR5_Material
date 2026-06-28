# Auftrag: Teachable Machine (kNN-Variante) als Jupyter-Notebook

> **So nutzen Sie dieses Blatt:** Diese Beschreibung ist Ihre „noch vage Idee" für
> **Schritt 1** des Spec-Driven Development. Setzen Sie sie in den grünen Bereich des
> Metaprompts ein, beantworten Sie die Rückfragen des Modells und leiten Sie daraus
> erst `spec.md`, dann `plan.md` und `tasks.md` ab. Diese Seite ist der **Ausgangspunkt,
> nicht die Spec** — die Spec schreiben Sie.

## Kontext und Motivation

Google Teachable Machine lässt Menschen ohne Programmierkenntnisse einen Bild­klassifikator
„trainieren". Im Kern steckt dahinter eine erstaunlich schlichte Idee: Ein großes, bereits
vortrainiertes neuronales Netz verwandelt jedes Bild in eine Liste von Zahlen, und ein
einfacher Klassifikator entscheidet allein anhand dieser Zahlen. Die **erste** Version von
Teachable Machine (2017) benutzte dafür **k-Nearest-Neighbors (kNN)** — kein eigenes Training,
nur Vergleichen: „Welchen bekannten Bildern ähnelt das neue Bild am meisten?"

In diesem Auftrag bauen Sie genau diese kNN-Variante nach — ohne grafische Oberfläche, als
nachvollziehbares Jupyter-Notebook. Ziel ist **kein** perfektes Produkt, sondern ein Notebook,
an dem man *versteht*, was Teachable Machine im Kern tut.
**Didaktische Klarheit geht vor technischer Vollkommenheit.**

## Ziel

Ein einzelnes Jupyter-Notebook, das Bilder mehrerer Klassen einliest, sie mit einem
vortrainierten **MobileNetV2** in Merkmale übersetzt und mit einem **kNN-Klassifikator** neue
Bilder einordnet — und dabei jeden Schritt verständlich erklärt.

## Rahmenbedingungen (fest — hier entscheiden Sie nichts)

- **Form:** ein einziges Jupyter-Notebook. Keine GUI, keine Web-App.
- **Sprache:** durchgehend Deutsch, auch in Erklärtexten und Code-Kommentaren.
- **Merkmals-Extraktor:** MobileNetV2, vortrainiert auf ImageNet, **eingefroren** — es wird
  *nicht* trainiert. Der originale Klassifikationskopf wird entfernt, sodass pro Bild die
  Merkmalszahlen herauskommen.
- **Klassifikator:** k-Nearest-Neighbors. *(Die trainierte Dense-Variante ist ein späterer,
  eigener Auftrag und hier ausdrücklich __nicht__ Teil der Aufgabe.)*
- **Modellgewichte:** die heruntergeladene Modelldatei wird lokal im Unterordner `Models/`
  abgelegt und bei weiteren Läufen von dort gelesen (kein erneuter Download).
- **Zielgruppe:** Einsteiger ohne Vorwissen zu neuronalen Netzen. Fachbegriffe sind erlaubt,
  müssen aber an Ort und Stelle in einem Satz erklärt werden.

## Gegeben: die Datenstruktur (Vertrag, nicht ändern)

Die Bilder liegen bereits als **224 × 224 Pixel, RGB** vor. Ein separates Skript erzeugt sie —
das ist **nicht** Teil dieses Auftrags. Verlassen Sie sich auf genau diese Ordnerstruktur:

```
Datasets/Train/KlasseA
Datasets/Train/KlasseB
Datasets/Test/KlasseA
Datasets/Test/KlasseB
```

Jeder Unterordner ist eine Klasse. Ihre Lösung soll mit **beliebigen Klassennamen** und
**beliebig vielen Klassen** funktionieren — nicht fest auf „KlasseA/KlasseB" verdrahtet sein.

## Was das fertige Notebook leisten muss (Ergebnis-Ebene)

Dies ist die *Was*-Ebene. Das *Wie* — Aufbau, Reihenfolge, konkrete Umsetzung — erarbeiten Sie
in Ihrer Spec.

- die Bilder gemäß Ordnerstruktur einlesen und die Klassen automatisch erkennen,
- jedes Trainings- und Testbild mit MobileNetV2 in seine Merkmale übersetzen,
- neue (Test-)Bilder per kNN einer Klasse zuordnen,
- die **Funktionsweise von kNN nachvollziehbar** machen: Jemand soll am Notebook *sehen*
  können, **warum** eine Entscheidung so fällt und nicht anders,
- die **Güte** des Ergebnisses auf den Testdaten belegen.

## Ausdrücklich nicht Teil dieses Auftrags

- kein eigenes Training des neuronalen Netzes,
- kein Dense-/MLP-Klassifikator (das ist der Folgeauftrag),
- keine grafische Oberfläche, kein Export, kein Deployment.

## Ihr Vorgehen (SDD)

Erarbeiten Sie die Lösung **vollständig nach Spec-Driven Development**. Starten Sie mit dem
Metaprompt aus Schritt 1 und nehmen Sie diese Auftragsbeschreibung als Ihre „vage Idee".
Beachten Sie: Für ein Notebook lesen sich zwei der fünf Frage-Kategorien etwas anders —
„User-Interface-Elemente und Layout" wird hier zu **Notebook-Aufbau und Visualisierungen**,
„Datenspeicherung" zu **Daten- und Merkmals-Repräsentation**.

Abgabe: `spec.md`, `plan.md`, `tasks.md` sowie das lauffähige Notebook.
