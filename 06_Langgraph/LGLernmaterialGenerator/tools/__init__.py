"""Deterministische Werkzeuge des Lernmaterial-Generators.

Kein LLM-»Urteil«, sondern reproduzierbare Bausteine: LLM-Client samt
Token-Zähler, Notebook-Parser, HTML-Render und programmatische Checks.
"""
from .llm import TOKENS, reset_tokens, call_llm, extract_json
from .notebook import analyze_notebook
from .quiz_html import QUIZ_TEMPLATE, build_quiz_html
from .checks import structural_checks, word_balance_check

__all__ = [
    "TOKENS",
    "reset_tokens",
    "call_llm",
    "extract_json",
    "analyze_notebook",
    "QUIZ_TEMPLATE",
    "build_quiz_html",
    "structural_checks",
    "word_balance_check",
]
