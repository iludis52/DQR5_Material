# LangGraph-Agent: Vom Notebook zum validierten Quiz

Dieses Skript erklärt die Architektur eines **LLM-basierten Agenten**, der automatisch Lernmaterial aus Jupyter-Notebooks generiert. Der Kern liegt in der Kombination aus **StateGraph-Orchestrierung**, **programmatischer Qualitätskontrolle** und **kontextbewusster Prompt-Engineering**.

## 1. Architektur: LangGraph und StateGraph

Im Gegensatz zu linearen Pipelines nutzt `langgraph.graph.StateGraph` einen gerichteten Graphen, bei dem Knoten (`nodes`) über Kanten (`edges`) verbunden sind und einen gemeinsamen **State** (Zustand) teilen.

*   **State (`QuizState`):** Ein `TypedDict`, das alle Daten hält (Konfiguration, Notebook-Inhalt, generierte Skripte, Quiz-Fragen, Qualitätsfeedback). Dies ermöglicht es dem Graphen, bei Fehlern zu einem früheren Knoten zurückzukehren (Loop), ohne Daten neu laden zu müssen.
*   **Knoten (`nodes`):** Reine Funktionen, die den State lesen und ein Update-Dictionary zurückgeben. Sie sind zustandslos und damit gut testbar.
*   **Routing:** Die Funktion `route_full` entscheidet basierend auf dem Output des Qualitäts-Knotens (`quality`) und der Iterationszahl, ob der Graph endet (`render`) oder sich selbst korrigiert (`rewrite_script` oder `rewrite_quiz`).

## 2. Der Workflow: Von der Analyse zur Generierung

Der Prozess folgt einer strikten Kette, um die Qualität zu sichern:

1.  **Analyse (`analyze_notebook`):** Das Notebook wird mit `nbformat` gelesen. Code- und Markdown-Zellen werden getrennt extrahiert. Dies bildet die **Faktenbasis (Grounding)**. Nur Informationen aus dieser Basis dürfen im Skript verwendet werden, um Halluzinationen zu vermeiden.
2.  **Skript-Generierung (`node_script`):** Ein LLM erstellt ein Markdown-Skript. Die Temperatur ist niedrig ($0.25$), um faktische Genauigkeit zu gewährleisten.
3.  **Termini-Extraktion (`node_termini`):** Fachbegriffe werden aus dem Skript extrahiert. Diese dienen später als "synthetische Schwerpunkte", um bei der Quiz-Generierung Abwechslung zu erzeugen.
4.  **Quiz-Generierung (`node_quiz`):** Hier wird die **Bloom-Taxonomie** angewendet. Je nach gewählter Schwierigkeitsstufe (1–5) variiert der Prompt die Anforderung (von "Erinnern" bis "Bewerten").
    *   *Wichtig:* Der Prompt erzwingt eine **Wortzahl-Balance** der Antwortoptionen, um das typische LLM-Verhalten zu unterbinden, die korrekte Antwort länger zu formulieren.
5.  **Qualitätsprüfung (`node_quality`):** Dies ist der kritischste Schritt. Er kombiniert zwei Methoden:
    *   **Programmatische Checks:** Prüfen strukturelle Integrität (z.B. genau 4 Optionen, korrekter Index).
    *   **LLM-Bewertung:** Ein separates "Checker-Modell" prüft auf Halluzinationen und fachliche Plausibilität.
6.  **Rendering (`node_render`):** Die validierten Fragen werden in ein HTML-Template injiziert. Die Einbettung als JSON-Variable im `<script>`-Tag ermöglicht das Öffnen der Datei lokal ohne CORS-Probleme.

## 3. Schlüsselkonzepte und Didaktik

### Grounding gegen Halluzinationen
Das System unterscheidet strikt zwischen *generiertem Text* und *faktenbasiertem Text*. Der Prompt enthält explizite Anweisungen ("STRIKTES GROUNDING"), dass nur im Notebook stehende API-Signaturen oder allgemein anerkanntes Wissen verwendet werden dürfen. Der Qualitäts-Knoten bestraft Verstöße explizit.

### Reflexions-Schleife (Self-Correction)
Der Graph ist nicht linear. Wenn `node_quality` Mängel feststellt, wird der State mit Feedback (`script_feedback` oder `quiz_feedback`) angereichert und der Graph zu `script` oder `quiz` zurückgelenkt.
*   **Maximale Iterationen:** Begrenzt auf 3 Durchläufe, um Endlosschleifen zu verhindern.
*   **Anti-Dubletten:** Bei der Generierung *neuer* Quizze (`run_regen`) werden bereits gestellte Fragen in die Ausschlussliste (`avoid_topics`) aufgenommen, um Wiederholungen zu minimieren.

### Kontextuelle Abwechslung
Um bei kleinen lokalen Modellen (z.B. via LM Studio) monotonen Output zu vermeiden, nutzt der Agent die extrahierten **Fachtermini**. Bei jeder neuen Quiz-Generation wird ein zufälliger Subset dieser Begriffe als "Schwerpunkt" in den Prompt injiziert. Dies zwingt das Modell, die gleichen Konzepte aus einer anderen Perspektive zu beleuchten.

## 4. Technische Details

*   **Provider-Agnostizität:** Durch die Nutzung der OpenAI-kompatiblen Schnittstelle (`base_url`) funktioniert der Code mit LM Studio, OpenRouter oder DeepInfra.
*   **Token-Tracking:** Die globale Variable `TOKENS` sammelt Usage-Daten pro LLM-Aufruf. Dies ermöglicht eine grobe Kostenschätzung und Transparenz über den Ressourcenverbrauch.
*   **JSON-Robustheit:** Da LLMs oft unsauberes JSON ausgeben, wird `extract_json` verwendet, das Code-Fences (` ```json `) entfernt und nach gültigen JSON-Strukturen sucht.