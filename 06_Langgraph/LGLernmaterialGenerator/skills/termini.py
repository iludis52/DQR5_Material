"""Skill: Prompt zum Extrahieren der Fachtermini (JSON-Array)."""
from .common import GROUNDING_RULE


def build_termini_prompt(state: dict) -> tuple:
    system = ("Du extrahierst Fachtermini aus Lern-Skripten. Antworte AUSSCHLIESSLICH mit "
              "einem JSON-Array von Strings, ohne weiteren Text. " + GROUNDING_RULE)
    user = f"""Lies das folgende Skript und gib die wichtigsten Fachtermini als JSON-Array
von kurzen Strings zurück (je Begriff optional mit knapper Klärung in Klammern).
Nur Begriffe, die im Skript oder Notebook tatsächlich vorkommen.

SKRIPT:
{state.get('script_md','')}
"""
    return system, user
