"""Programmatische, deterministische Qualitätschecks für das Quiz.

Objektive, billige Prüfungen vor dem LLM-Urteil – insbesondere der
Wortzahl-Bias (korrekte Antwort darf nicht systematisch die längste sein).
"""
from typing import List


def structural_checks(questions: List[dict], expected_n: int = 10) -> List[str]:
    issues = []
    if not isinstance(questions, list) or not questions:
        return ["Quiz enthält keine Fragen."]
    if len(questions) != expected_n:
        issues.append(f"Es wurden {len(questions)} statt {expected_n} Fragen erzeugt.")
    for i, q in enumerate(questions, 1):
        opts = q.get("options", [])
        if len(opts) != 4:
            issues.append(f"Frage {i}: {len(opts)} statt 4 Optionen.")
        c = q.get("correct")
        if not isinstance(c, int) or not (0 <= c <= 3):
            issues.append(f"Frage {i}: ungültiger correct-Index ({c}).")
    return issues


def word_balance_check(questions: List[dict], threshold: float = 0.4) -> List[str]:
    longest_is_correct, counted = 0, 0
    for q in questions:
        opts, c = q.get("options", []), q.get("correct")
        if len(opts) != 4 or not isinstance(c, int) or not (0 <= c <= 3):
            continue
        counted += 1
        lengths = [len(str(o).split()) for o in opts]
        if lengths.index(max(lengths)) == c and len(set(lengths)) > 1:
            longest_is_correct += 1
    if counted and longest_is_correct / counted > threshold:
        return [f"Wortzahl-Bias: bei {longest_is_correct}/{counted} Fragen ist die korrekte "
                f"Antwort die längste Option. Optionen angleichen."]
    return []
