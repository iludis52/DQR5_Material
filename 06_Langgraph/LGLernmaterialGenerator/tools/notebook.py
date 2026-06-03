"""Notebook-Analyse: trennt Code- und Markdown-Inhalte eines .ipynb.

Beides bildet die Faktenbasis (das »Grounding«), auf die sich Skript und Quiz
stützen dürfen.
"""
from typing import Dict

import nbformat


def analyze_notebook(path: str) -> Dict[str, str]:
    """Trennt Code- und Markdown-Inhalte eines .ipynb."""
    nb = nbformat.read(path, as_version=4)
    code_parts, md_parts = [], []
    for cell in nb.cells:
        src = (cell.get("source") or "").strip()
        if not src:
            continue
        if cell.cell_type == "code":
            code_parts.append(src)
        elif cell.cell_type == "markdown":
            md_parts.append(src)
    return {
        "notebook_code": "\n\n# --- nächste Code-Zelle ---\n".join(code_parts),
        "notebook_markdown": "\n\n---\n".join(md_parts) if md_parts else "(keine Markdown-Zellen vorhanden)",
    }
