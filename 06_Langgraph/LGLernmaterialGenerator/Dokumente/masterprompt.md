# Masterprompt – Lernmaterial-Generator (LangGraph-Agent)

**Kontext:** Ich entwickle einen LangGraph-Agenten als Jupyter-Notebook (das Notebook ist selbst Lerngegenstand meiner KI-Vorlesung). Ich lade dir die aktuelle Version `Lernmaterial_Generator_LangGraph.ipynb` hoch. Bitte arbeite an dieser Datei weiter, nicht an einer Neukonstruktion.

**Was der Agent tut:** Aus zwei Eingaben – einem hochgeladenen Jupyter-Notebook (Code + Markdown werden analysiert) und einem Schwerpunkt-Textfeld des Dozenten – erzeugt er drei aufeinander abgestimmte Artefakte: (1) ein knappes, didaktisch sauberes Markdown-Skript mit dem nötigen Theorie-Hintergrund, (2) eine Liste der Fachtermini, (3) eine eigenständige HTML-Quiz-Seite mit 10 Fragen im gewohnten Layout. Alle drei sind herunterladbar. Alles auf Deutsch.

**Architektur:** LangGraph mit den Knoten `script → termini → quiz → quality → render`. Der Quality-Knoten kombiniert programmatische Checks (Struktur, Wortzahl-Balance der Antworten) mit einer LLM-Bewertung (Halluzinationen, Plausibilität) und löst bei Mängeln eine Reflexions-Schleife aus – max. 3 Iterationen. Zweiter, schlanker Graph `quiz → quality → render` für beliebig oft wiederholbare Neu-Quizze.

**Wichtige Designentscheidungen (bitte beibehalten):**

- Modelle provider-agnostisch über OpenAI-kompatible API (LM Studio / DeepInfra / OpenRouter), Felder `base_url`/`api_key`/`model`. Separates, optionales Checker-Modell mit eigenen drei Feldern (leer = Fallback aufs Generator-Modell).
- HTML-Template ist feste Hülle; das LLM liefert nur das `questions`-Array, das inline injiziert wird (kein `fetch`, damit die Datei per `file://` ohne CORS-Probleme öffnet).
- Schwierigkeit 1–5 mit Bloom-Gewichtung; striktes Grounding gegen Halluzinationen (keine erfundenen API-Signaturen/Parameter/Zahlen), domänen-unabhängig (PyTorch, sklearn, pandas, Keras/CNN, ARIMA/Prophet, NLTK …).
- Wortzahl-Balance: korrekte Antwort darf nicht systematisch die längste sein (Prompt-Regel + programmatischer Check).
- Bei „Neues Quiz": rotierender, zufälliger Satz Fachtermini als synthetischer Schwerpunkt + leicht erhöhte Temperatur + Liste bereits gestellter Fragen als Ausschluss (gegen Dubletten bei kleinen Modellen).
- Token-Zähler (summiert `usage`) mit optionaler Kostenschätzung; Fortschrittsanzeige über `graph.stream()` nach jedem Knoten.

**Mein nächstes Ziel:** _[hier eintragen, woran du als Nächstes arbeiten willst]_
