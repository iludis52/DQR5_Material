"""Skill: Prompt für das didaktische Markdown-Lernskript."""
from .common import GROUNDING_RULE


def build_script_prompt(state: dict) -> tuple:
    system = (
        "Du bist eine erfahrene Dozentin für Machine Learning und erstellst knappe, "
        "didaktisch saubere Lern-Skripte auf Deutsch im Markdown-Format. " + GROUNDING_RULE
    )
    user = f"""Analysiere das folgende Jupyter-Notebook (Code und Markdown) und erstelle ein
**knappes** Markdown-Skript, das den nötigen theoretischen Hintergrund zum Verständnis des
Codes vermittelt. Nicht die Länge zählt, sondern didaktische Klarheit.

Beginne mit einer Überschrift der Form `# <kurzer, prägnanter Titel>`.
Erkläre die zentralen Konzepte, Fachbegriffe und das Warum hinter den Code-Schritten.
Gehe besonders auf die folgenden Schwerpunkte des Dozenten ein:
---SCHWERPUNKTE---
{state.get('focus') or '(keine besonderen Schwerpunkte angegeben)'}
---ENDE SCHWERPUNKTE---

NOTEBOOK-CODE:
{state['notebook_code']}

NOTEBOOK-MARKDOWN:
{state['notebook_markdown']}
"""
    if state.get("quality", {}).get("script_feedback"):
        user += f"\n\nUEBERARBEITUNG NÖTIG – berücksichtige diese Kritik:\n{state['quality']['script_feedback']}"
    return system, user
