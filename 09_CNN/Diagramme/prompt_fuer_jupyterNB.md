# Aufgabe: Mermaid-Flussdiagramm aus Jupyter-Notebook erstellen

Analysiere das angehängte Jupyter-Notebook und erstelle daraus ein
Mermaid-Flussdiagramm (flowchart TD) als reinen Quelltext, den ich in
VS Code selbst rendern kann.

## Umfang
- Bilde nur den fachlichen Ablauf ab: [HIER ANPASSEN, z. B. "nur die
  Trainings-Zelle" / "das gesamte Notebook" / "nur die Inferenz"]
- Imports, pip-Installs und reine Ausgabe-/Debug-Zeilen weglassen.

## Struktur
1. Jeder fachliche Schritt wird ein eigener Knoten, fortlaufend
   nummeriert (S1, S2, …).
2. Knoten-Label im Format:
   ["<b>N – Kurztitel</b><br/><i>konkrete Funktion / Parameter</i>"]
   Die Kursiv-Zeile nennt die tatsächliche Funktion aus dem Code
   (z. B. train_test_split, random_state=42).
3. Zusammengehörige Schritte in benannte Subgraphs gruppieren
   (typisch: Datenaufbereitung, Modellierung & Training,
   Evaluation & Speichern). Subgraph-Syntax:
   subgraph Name ["Anzeigename"] … end
4. Schleifen und Verzweigungen im Code (z. B. Trainingsschleife über
   Epochen) als Entscheidungsraute {"…?"} mit beschrifteten Kanten
   und Rücksprungpfeil darstellen – nicht als linearen Block.
5. Alle Kantendefinitionen (-->) NACH den Subgraphs gesammelt notieren.

## Farbschema (style-Zeilen pro Knoten am Ende)
- Daten laden / aufbereiten:  fill:#e1f5ee,stroke:#0f6e56,color:#04342c
- Splits / Transformationen:  fill:#eeedfe,stroke:#534ab7,color:#26215c
- Modellierung / Training:    fill:#faece7,stroke:#993c1d,color:#4a1b0c
- Evaluation / Speichern:     fill:#faeeda,stroke:#854f0b,color:#412402

## Syntax-Regeln (wichtig, häufige Fehlerquellen!)
- Ausgabe als reiner Mermaid-Quelltext, ohne umschließende HTML-Tags,
  ohne Kommentare außerhalb der Mermaid-Syntax.
- Alle Labels in doppelte Anführungszeichen setzen.
- Sonderzeichen vermeiden, die Parser stören: % ( ) [ ] { } in Labels
  nur innerhalb von Anführungszeichen; im Zweifel umschreiben
  (z. B. "80/20" statt "80 % / 20 %").
- Nur <b>, <i>, <br/> als HTML in Labels verwenden.
- Vor der Ausgabe gedanklich prüfen: Ist jede subgraph mit end
  geschlossen? Ist jede Knoten-ID eindeutig? Verweist jede Kante auf
  existierende IDs?

## Sprache
Alle Beschriftungen auf Deutsch.