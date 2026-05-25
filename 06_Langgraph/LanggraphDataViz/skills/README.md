# 📁 Skills-Ordner

Dieses Verzeichnis enthält **austauschbare Prompt-Bausteine** für den 
Datenanalyse-Agenten. Jede `.md`-Datei ist ein Skill, der zur Laufzeit 
geladen und in den System-Prompt eingebaut wird.

## Struktur

```
skills/
├── analyst/                    # Analyse-Strategien
│   ├── _basis.md               # Immer geladen (Grundregeln)
│   ├── numerisch.md            # Bei numerischen Spalten
│   ├── kategorisch.md          # Bei kategorischen Spalten
│   ├── zeitreihe.md            # Bei Datumsspalten
│   └── fehlende_werte.md       # Bei fehlenden Werten
├── checker/                    # Bewertungskriterien
│   └── standard.md             # Standard-Bewertungsschema
└── README.md                   # Diese Datei
```

## Wie Skills funktionieren

1. Der **Data Profiler** analysiert den Datensatz und erkennt, welche 
   Spaltentypen vorhanden sind
2. Basierend darauf werden die passenden Analyst-Skills geladen
3. Der Analyst erhält einen zusammengesetzten Prompt aus `_basis.md` + 
   allen relevanten Spezial-Skills
4. Der Checker lädt sein Bewertungsschema aus `checker/standard.md`

## Eigene Skills erstellen

1. Erstelle eine `.md`-Datei im passenden Unterordner
2. Verwende Platzhalter für dynamische Werte:
   - `{file_path}` — Pfad zur Datendatei
   - `{profile_json}` — Vollständiges Datenprofil als JSON
   - `{spalten}` — Alle Spaltennamen
   - `{numerische_spalten}` — Nur numerische Spalten
   - `{kategorische_spalten}` — Nur kategorische Spalten
   - `{fehlende_werte}` — Dict der fehlenden Werte
   - `{zeilen}` — Anzahl Zeilen
3. Für Analyst-Skills: `_basis.md` beginnt immer mit Unterstrich und wird 
   immer geladen. Weitere Skills werden nach Datenprofil ausgewählt.

## Beispiel: Eigenen Domänen-Skill hinzufügen

```markdown
<!-- skills/analyst/ecommerce.md -->
# E-Commerce-Analyse

Dieser Datensatz enthält E-Commerce-Daten. Zusätzlich zu den 
Standardanalysen solltest du folgende Aspekte untersuchen:

- **Warenkorbanalyse**: Welche Produkte werden zusammen gekauft?
- **Kundenkohorte**: Gibt es Unterschiede zwischen Neukunden und Bestandskunden?
- **Conversion-Funnel**: Wo brechen Kunden ab?
```

Damit dieser Skill geladen wird, muss die Skill-Auswahl im Notebook 
angepasst werden (Funktion `select_analyst_skills`).
