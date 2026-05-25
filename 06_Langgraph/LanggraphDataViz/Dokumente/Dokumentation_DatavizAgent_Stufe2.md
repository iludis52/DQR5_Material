# Datenanalyse-Agent mit LangGraph — Stufe 2

## Dokumentation: Architektur & Bedienungsanleitung

---

## Teil A — Architektur des LangGraph-Agenten

### Überblick

Der Datenanalyse-Agent ist als gerichteter Zustandsgraph mit LangGraph implementiert. Er nimmt eine CSV- oder Excel-Datei entgegen, analysiert sie automatisch und liefert Visualisierungen sowie textuelle Erkenntnisse. Das Besondere an Stufe 2 gegenüber einem einfachen LLM-Aufruf: Der Agent wählt seine Analysestrategie dynamisch anhand der Datenstruktur, und ein zweites LLM prüft die Qualität der Ergebnisse — bei Bedarf wird nachgebessert.

### Die fünf Knoten im Graphen

Der Graph besteht aus fünf Knoten, die jeweils eine klar abgegrenzte Aufgabe haben:

**1. Data Profiler** — Der Einstiegspunkt. Dieser Knoten arbeitet rein deterministisch (kein LLM-Aufruf). Er liest die hochgeladene Datei ein, erstellt ein strukturiertes Profil (Spaltentypen, Grundstatistiken, fehlende Werte, Stichprobe) und entscheidet auf Basis einfacher Regeln, welche Analyse-Skills der Analyst erhalten soll. Das Profil und die Liste der aktiven Skills werden im State gespeichert.

**2. Analyst** — Der Hauptakteur. Ein leistungsfähiges LLM (in der DeepInfra-Variante: Qwen3.6-35B, in der LM-Studio-Variante: Nemotron-3-Nano-4B) erhält einen System-Prompt, der zur Laufzeit aus mehreren Skill-Dateien zusammengebaut wird. Der Analyst kann das Tool `execute_python` aufrufen, um Code in einer Sandbox auszuführen. Er arbeitet iterativ: Analyse planen, Code schreiben, Ergebnis lesen, nächsten Schritt planen.

**3. Tools (ToolNode)** — Die Python-Sandbox. Wenn der Analyst einen Tool-Call absetzt, führt dieser Knoten den Python-Code aus und gibt stdout/stderr zurück. Verfügbar sind pandas, matplotlib, seaborn und numpy. Plots werden als PNG-Dateien gespeichert, nicht mit `plt.show()` angezeigt.

**4. Quality Checker** — Das zweite LLM. Ein günstigeres Modell (in der DeepInfra-Variante: Nemotron-3-Nano-Omni-30B, in der LM-Studio-Variante: Qwen3-4B-Instruct) bewertet die bisherige Analyse anhand eines strukturierten Bewertungsschemas. Es kennt die aktiven Skills und prüft gezielt, ob jeder Skill abgearbeitet wurde. Die Ausgabe ist ein JSON-Objekt mit Scores und konkreten Verbesserungsvorschlägen.

**5. Increment Revision** — Ein einfacher Zählerknoten. Er erhöht den `revision_count` im State um 1, bevor der Analyst eine weitere Runde dreht.

### Datenfluss und Routing

Der Graph durchläuft folgende Schritte:

```
START
  │
  ▼
data_profiler ──── Datei einlesen, Profil erstellen, Skills wählen
  │
  ▼
analyst ◄──────── System-Prompt aus Skills zusammenbauen, Analyse starten
  │
  ├─── Tool-Call vorhanden? ──► tools ──► zurück zum analyst
  │
  └─── Kein Tool-Call? ──► quality_checker
                              │
                              ├── Score ≥ Threshold? ──► END
                              │
                              ├── Max. Revisionen erreicht? ──► END
                              │
                              └── Score zu niedrig? ──► increment_revision ──► analyst
```

Zwei bedingte Kanten steuern den Ablauf. Die erste (`should_use_tool`) prüft nach jedem Analyst-Aufruf, ob die letzte Nachricht einen Tool-Call enthält. Falls ja, wird der Code ausgeführt und das Ergebnis an den Analyst zurückgegeben. Falls nein, geht es zum Quality Checker. Die zweite (`should_revise`) entscheidet nach der Qualitätsbewertung: Ist der gewichtete Score mindestens so hoch wie der Threshold (Standard: 70 %), wird die Analyse akzeptiert. Andernfalls wird nachgebessert — maximal dreimal.

### State-Schema

Alle Daten fließen durch ein gemeinsames State-Objekt vom Typ `AnalysisState`. Es enthält den Dateipfad, das Datenprofil, die Liste aktiver Skills, den Nachrichtenverlauf (mit LangGraphs `add_messages`-Reducer), den Qualitäts-Score, das Checker-Feedback und den Revisionszähler. Der Reducer sorgt dafür, dass Nachrichten bei jedem Knotendurchlauf angehängt statt überschrieben werden.

### Zwei-LLM-Strategie

Die Trennung in Analyst und Checker hat didaktische und praktische Gründe. Erstens verhindert sie, dass das Modell seine eigene Arbeit unkritisch bewertet — ein zweites Modell mit separatem Prompt bringt eine unabhängige Perspektive ein. Zweitens spart sie Kosten: Der Checker braucht keine Tool-Calling-Fähigkeit und kein großes Kontextfenster, daher genügt ein kleineres, günstigeres Modell. In der LM-Studio-Variante laufen beide Modelle lokal, was den Ansatz auch ohne API-Kosten nutzbar macht.

### Reflexionsschleife

Die Reflexionsschleife ist das zentrale Qualitätsmerkmal von Stufe 2. Der Checker bewertet entlang zweier Dimensionen: Vollständigkeit (wurden alle Skills abgearbeitet?) und Erkenntnistiefe (sind die Ergebnisse spezifisch und datengestützt?). Der gewichtete Score ergibt sich aus 60 % Vollständigkeit und 40 % Tiefe. Liegt er unter dem Threshold, wird das Checker-Feedback als `HumanMessage` in den Nachrichtenverlauf injiziert — der Analyst sieht konkret, was fehlt, und führt nur die ausstehenden Analysen durch.

### Notebook-Varianten

Es gibt zwei Varianten des Notebooks, die sich ausschließlich im LLM-Backend unterscheiden:

Die **DeepInfra-Variante** (`DatavizAgent_twoLLM_skills.ipynb`) verwendet die DeepInfra-API mit dem OpenAI-kompatiblen Endpunkt. Sie erfordert einen API-Key, der beim Start per `getpass` abgefragt wird. Die Modelle (Qwen3.6-35B als Analyst, Nemotron-3-Nano-Omni-30B als Checker) laufen serverseitig.

Die **LM-Studio-Variante** (`DatavizAgent_twoLLM_skills_lmstudio.ipynb`) spricht stattdessen einen lokalen LM-Studio-Server auf `http://localhost:1234/v1` an. Sie braucht keinen API-Key, setzt aber voraus, dass LM Studio läuft und die Modelle (Nemotron-3-Nano-4B, Qwen3-4B-Instruct) geladen sind. Die `max_tokens` sind hier auf 12.000 erhöht, da lokale Modelle tendenziell mehr Platz brauchen.

Der gesamte übrige Code — Graph-Aufbau, Skills, Tools, Gradio-Interface — ist identisch.

---

## Teil B — Bedienungsanleitung: Das Skill-System

### Was Skills sind

Skills sind Markdown-Dateien (`.md`), die als Prompt-Bausteine dienen. Statt einen monolithischen System-Prompt im Code zu pflegen, lagert das Notebook die Analyseanweisungen in separate Dateien aus. Das hat drei Vorteile: Man kann Skills bearbeiten, ohne Python-Code anzufassen; man kann sie für unterschiedliche Datensätze kombinieren; und man kann neue Skills erstellen, um das System für bestimmte Domänen zu spezialisieren.

### Ordnerstruktur

```
skills/
├── analyst/                   Analyse-Strategien für den Analyst-LLM
│   ├── _basis.md              Wird immer geladen (Grundregeln)
│   ├── numerisch.md           Bei numerischen Spalten
│   ├── kategorisch.md         Bei kategorischen Spalten
│   ├── zeitreihe.md           Bei Datumsspalten
│   └── fehlende_werte.md      Bei fehlenden Werten
└── checker/                   Bewertungskriterien für den Checker-LLM
    └── standard.md            Standard-Bewertungsschema
```

Der `analyst/`-Ordner enthält die Skills, die den System-Prompt des Analysten steuern. Der `checker/`-Ordner enthält das Bewertungsschema, gegen das der Checker prüft.

### Die einzelnen Skills im Detail

**`_basis.md` — Grundregeln (immer aktiv)**

Dieser Skill wird bei jedem Durchlauf geladen, unabhängig vom Datentyp. Er definiert die Rolle des Analysten ("Du bist ein erfahrener Datenanalyst"), enthält das vollständige Datenprofil als JSON-Platzhalter und legt die Code-Konventionen fest: Plots speichern statt anzeigen, `plt.close()` nach jedem Plot, Ergebnisse mit `print()` ausgeben, deutsche Beschriftungen. Der Unterstrich im Dateinamen ist Konvention — er signalisiert, dass die Datei immer geladen wird.

**`numerisch.md` — Numerische Analyse**

Wird aktiviert, sobald der Datensatz mindestens eine numerische Spalte enthält. Fordert den Analysten auf, Verteilungen (Histogramme, Boxplots), Korrelationen (Heatmap), Ausreißer (IQR oder Z-Scores) und deskriptive Statistiken zu untersuchen. Der Qualitätsanspruch verlangt konkrete Zahlen statt vager Aussagen — "Der Median liegt bei X" statt "Die Werte variieren".

**`kategorisch.md` — Kategorische Analyse**

Wird aktiviert bei mindestens einer kategorischen Spalte (Datentyp `object` oder `category`). Fordert Häufigkeitsverteilungen (Balkendiagramme), gruppierte Analysen (numerische Kennzahlen nach Kategorien mit `groupby()`) und Kreuztabellen. Erwartet die Identifikation von Top- und Bottom-Performern mit konkreten Prozentwerten.

**`zeitreihe.md` — Zeitreihenanalyse**

Wird aktiviert, wenn ein Spaltenname ein Datums-Keyword enthält (datum, date, zeit, time, tag, monat, jahr, year, month, day). Fordert die Konvertierung mit `pd.to_datetime()`, Trendanalyse mit Liniendiagrammen und Rolling Averages, saisonale Muster (Aggregation nach Monat/Wochentag/Quartal) und Periodenvergleiche. Erwartet kontextualisierte Aussagen mit konkreten Werten und Prozentwerten.

**`fehlende_werte.md` — Analyse fehlender Werte**

Wird aktiviert, sobald das Datenprofil fehlende Werte enthält. Fordert die Klassifikation des Fehlmusters (MCAR, MAR, MNAR), eine Visualisierung der fehlenden Werte, die Untersuchung von Zusammenhängen (fehlen Werte systematisch in bestimmten Kategorien oder Zeiträumen?) und eine begründete Empfehlung zum Umgang (Löschen, Imputation, Interpolation). Erwartet exakte Anzahlen und Anteile.

**`standard.md` — Bewertungsschema (Checker)**

Dieses Skill steuert nicht den Analysten, sondern den Quality Checker. Es enthält das Datenprofil, die Liste der aktiven Analyst-Skills und zwei Bewertungsdimensionen: Vollständigkeit (0.0–1.0, hat der Analyst jeden geladenen Skill abgearbeitet?) und Erkenntnistiefe (0.0–1.0, sind die Ergebnisse spezifisch und handlungsrelevant?). Der Checker antwortet ausschließlich mit einem JSON-Objekt, das die Scores, fehlende Punkte und Stärken enthält.

### Platzhalter-System

Jeder Skill kann Platzhalter in geschweiften Klammern enthalten, die zur Laufzeit mit echten Werten befüllt werden:

| Platzhalter | Inhalt | Beispiel |
|---|---|---|
| `{file_path}` | Pfad zur Datendatei | `beispiel_verkaufsdaten.csv` |
| `{profile_json}` | Vollständiges Datenprofil als JSON | `{"zeilen": 30, "spalten": 8, ...}` |
| `{spalten}` | Alle Spaltennamen | `datum, produkt, kategorie, region, ...` |
| `{numerische_spalten}` | Nur numerische Spalten | `umsatz, menge, rabatt_prozent, ...` |
| `{kategorische_spalten}` | Nur kategorische Spalten | `produkt, kategorie, region` |
| `{fehlende_werte}` | Dict der fehlenden Werte | `{"umsatz": 2, "kundenzufriedenheit": 1}` |
| `{zeilen}` | Anzahl Zeilen | `30` |
| `{aktive_skills}` | Geladene Skills (nur Checker) | `numerisch.md, kategorisch.md, zeitreihe.md` |

Platzhalter, für die kein Wert vorhanden ist, bleiben im Text stehen — das verhindert Fehler bei unvollständigen Profilen.

### Wie die Skill-Auswahl funktioniert

Die Funktion `select_analyst_skills()` im Notebook trifft die Auswahl deterministisch anhand des Datenprofils. Die Logik ist bewusst einfach gehalten:

1. Hat das Profil nicht-leere `numerische_spalten`? → `numerisch.md` laden.
2. Hat das Profil nicht-leere `kategorische_spalten`? → `kategorisch.md` laden.
3. Enthält ein Spaltenname (case-insensitive) eines der Keywords `datum`, `date`, `zeit`, `time`, `tag`, `monat`, `jahr`, `year`, `month`, `day`? → `zeitreihe.md` laden.
4. Hat das Profil nicht-leere `fehlende_werte`? → `fehlende_werte.md` laden.

Der Basis-Skill `_basis.md` wird immer geladen und ist nicht Teil dieser Auswahl. Die ausgewählten Skills werden mit `---` als Trennzeichen zusammengesetzt und bilden den System-Prompt des Analysten.

### Eigene Skills erstellen

**Schritt 1: Markdown-Datei anlegen.** Eine neue `.md`-Datei im Ordner `skills/analyst/` erstellen. Sie sollte einen Titel, Analyseaufgaben und einen Qualitätsanspruch enthalten — analog zu den bestehenden Skills. Platzhalter können frei verwendet werden.

Beispiel für einen E-Commerce-Skill:

```markdown
# E-Commerce-Analyse

Der Datensatz enthält E-Commerce-Daten mit den Spalten: {spalten}

## Analyseaufgaben

- Durchschnittlicher Warenkorbwert und dessen Entwicklung über die Zeit
- Top/Flop-Produkte nach Umsatz und Menge
- Korrelation zwischen Rabatt und Kundenzufriedenheit

## Qualitätsanspruch

Nenne konkrete Zahlen und vergleiche Gruppen mit Prozentangaben.
```

**Schritt 2: Auswahlfunktion anpassen.** In `select_analyst_skills()` eine neue Bedingung ergänzen, die den Skill bei passenden Datensätzen aktiviert — typischerweise anhand von Spaltennamen:

```python
ecommerce_keywords = {"kunde", "warenkorb", "bestellung", "order", "cart"}
if any(keyword in col for col in all_cols for keyword in ecommerce_keywords):
    skills.append("ecommerce.md")
```

**Schritt 3: Checker erweitern (optional).** Wenn der Quality Checker den neuen Skill bei der Vollständigkeitsbewertung berücksichtigen soll, die Beschreibung in `skills/checker/standard.md` um eine entsprechende Zeile ergänzen, z. B. "E-Commerce-Skill geladen → Wurden Warenkorbwerte und Produktperformance analysiert?"

### Konfigurationsparameter

Die wichtigsten Parameter stehen gesammelt in Abschnitt 2 der Notebooks:

| Parameter | Standard | Bedeutung |
|---|---|---|
| `QUALITY_THRESHOLD` | 0.70 | Mindest-Score für die Akzeptanz der Analyse |
| `MAX_REVISIONS` | 3 | Maximale Nachbesserungsrunden |
| `WEIGHT_COMPLETENESS` | 0.60 | Gewicht der Vollständigkeit im Score |
| `WEIGHT_DEPTH` | 0.40 | Gewicht der Erkenntnistiefe im Score |
| `SKILLS_DIR` | `skills/` | Pfad zum Skills-Ordner (relativ zum Notebook) |

Den Threshold niedriger zu setzen (z. B. 0.50) führt zu schnelleren Durchläufen mit weniger Revisionen, aber potenziell unvollständigen Analysen. Ihn höher zu setzen (z. B. 0.85) erzwingt gründlichere Arbeit, verbraucht aber mehr API-Calls und Zeit.

### Troubleshooting

**Skills werden nicht geladen:** Der Skills-Ordner muss relativ zum Notebook unter `skills/analyst/` bzw. `skills/checker/` liegen. Das Notebook prüft beim Start, ob der Ordner existiert, und gibt eine Warnung aus, falls nicht. Der Agent funktioniert trotzdem — mit Fallback-Prompts, die aber weniger spezifisch sind.

**Checker liefert kein valides JSON:** Das Notebook enthält robustes Regex-basiertes JSON-Parsing, das auch funktioniert, wenn das Modell Markdown-Codeblöcke oder Begleittext mitliefert. Sollte der Parser dennoch scheitern, werden Fallback-Scores von 0.5 gesetzt und "JSON-Parsing fehlgeschlagen" als fehlendes Element gemeldet.

**Reflexionsschleife dreht sich im Kreis:** Wenn der Analyst nach drei Revisionen den Threshold nicht erreicht, wird die Analyse trotzdem akzeptiert und der letzte Score ausgegeben. Das verhindert Endlosschleifen.

**LM Studio antwortet nicht:** In der lokalen Variante muss LM Studio auf Port 1234 laufen und das richtige Modell geladen sein. Die Modellnamen im Notebook müssen exakt mit den in LM Studio geladenen Modellen übereinstimmen.
