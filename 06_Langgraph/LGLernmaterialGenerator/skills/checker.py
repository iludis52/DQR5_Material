"""Skill: Prompt für die LLM-Qualitätsprüfung (Halluzinationen, Plausibilität)."""
import json


def build_checker_prompt(state: dict) -> tuple:
    system = (
        "Du bist ein strenger Qualitätsprüfer für Lernmaterial. Du prüfst faktische "
        "Korrektheit gegen die gegebene Faktenbasis und meldest jede nicht belegte Aussage. "
        "Antworte AUSSCHLIESSLICH mit einem JSON-Objekt."
    )
    user = f"""Prüfe Skript und Quiz gegen die Faktenbasis (Notebook + gesichertes Fachwissen).

Gib ein JSON-Objekt zurück:
{{"script_ok": bool, "quiz_ok": bool,
  "script_feedback": "konkrete Mängel oder ''",
  "quiz_feedback": "konkrete Mängel oder ''"}}

Prüfkriterien:
1. HALLUZINATIONEN: Werden API-Funktionen, Parameter, Default-Werte oder Zahlen behauptet,
   die weder im Notebook stehen noch gesichertes Allgemeinwissen sind? -> nicht ok.
2. Hat jede Quizfrage genau eine eindeutig korrekte Antwort?
3. Sind die Distraktoren fachlich plausibel (keine offensichtlich absurden Optionen)?
4. Werden die Dozenten-Schwerpunkte abgedeckt: {state.get('focus') or '(keine)'} ?
5. Passt das Anspruchsniveau zur Stufe {state.get('difficulty', 3)}/5?

NOTEBOOK-CODE:
{state['notebook_code']}

SKRIPT:
{state.get('script_md','')}

QUIZ (JSON):
{json.dumps(state.get('quiz_questions', []), ensure_ascii=False)}
"""
    return system, user
