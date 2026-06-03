"""Skill: Prompt für die 10 Multiple-Choice-Fragen.

Bloom-Gewichtung nach Schwierigkeit, Wortzahl-Balance und Anti-Dubletten-Logik
sind hier verankert.
"""
from .common import GROUNDING_RULE, bloom_guidance


def build_quiz_prompt(state: dict) -> tuple:
    avoid = state.get("avoid_topics") or []
    avoid_txt = "\n".join(f"- {a}" for a in avoid) if avoid else "(noch keine)"
    spotlight = state.get("quiz_focus_termini") or []
    spotlight_block = ""
    if spotlight:
        spotlight_block = (
            "\n- SCHWERPUNKT DIESES DURCHLAUFS: Baue die Fragen GEZIELT rund um diese "
            "Fachbegriffe auf und beleuchte sie aus einem ANDEREN Blickwinkel als üblich:\n"
            + "\n".join(f"  · {t}" for t in spotlight)
        )
    system = (
        "Du bist Prüfungs-Didaktikerin und erstellst hochwertige Multiple-Choice-Fragen "
        "auf Deutsch. Antworte AUSSCHLIESSLICH mit einem JSON-Array, ohne weiteren Text. "
        + GROUNDING_RULE
    )
    user = f"""Erstelle GENAU 10 Multiple-Choice-Fragen zum folgenden Stoff.

{bloom_guidance(state.get('difficulty', 3))}

FORMAT – ein JSON-Array mit 10 Objekten, jeweils:
{{"text": "Frage?", "options": ["A","B","C","D"], "correct": <Index 0-3>, "explanation": "kurze Begründung"}}

HARTE REGELN:
- Genau 4 Optionen pro Frage, genau eine ist eindeutig korrekt.
- WORTZAHL-BALANCE: Alle vier Optionen müssen ähnlich lang und gleich strukturiert sein.
  Die korrekte Antwort darf NICHT systematisch die längste oder detaillierteste sein.
  Verteile die Position der korrekten Antwort gleichmäßig über die Indizes 0-3.
- Distraktoren müssen fachlich plausibel und verlockend sein, aber eindeutig falsch.
- Decke die Dozenten-Schwerpunkte ab: {state.get('focus') or '(keine)'}{spotlight_block}
- Vermeide thematische Wiederholungen zu bereits gestellten Fragen:
{avoid_txt}

SKRIPT (Grounding):
{state.get('script_md','')}

NOTEBOOK-CODE (Grounding):
{state['notebook_code']}
"""
    if state.get("quality", {}).get("quiz_feedback"):
        user += f"\n\nUEBERARBEITUNG NÖTIG – behebe diese Mängel:\n{state['quality']['quiz_feedback']}"
    return system, user
