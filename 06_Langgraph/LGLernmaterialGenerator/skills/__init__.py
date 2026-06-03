"""Skills – die fachliche Prompt-Schicht (»der eigentliche Skill«).

Domänen-unabhängige Prompts mit striktem Grounding gegen Halluzinationen und
Bloom-Gewichtung nach Schwierigkeitsstufe. Jeder Graph-Knoten bezieht hier
seinen System- und User-Prompt.
"""
from .common import GROUNDING_RULE, bloom_guidance
from .script import build_script_prompt
from .termini import build_termini_prompt
from .quiz import build_quiz_prompt
from .checker import build_checker_prompt

__all__ = [
    "GROUNDING_RULE",
    "bloom_guidance",
    "build_script_prompt",
    "build_termini_prompt",
    "build_quiz_prompt",
    "build_checker_prompt",
]
