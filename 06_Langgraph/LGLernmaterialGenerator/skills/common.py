"""Gemeinsame Prompt-Bausteine: Grounding-Regel und Bloom-Gewichtung.

Diese beiden Bausteine werden von mehreren Skill-Prompts geteilt.
"""

def bloom_guidance(difficulty: int) -> str:
    """Verteilung der Bloom-Stufen je nach Schwierigkeit 1-5."""
    table = {
        1: "Schwerpunkt ERINNERN & VERSTEHEN (~70 %), wenig ANWENDEN (~30 %). Klare, einfache Distraktoren.",
        2: "VERSTEHEN überwiegt (~50 %), ANWENDEN (~35 %), erste ANALYSE-Fragen (~15 %).",
        3: "Ausgewogen: VERSTEHEN/ANWENDEN/ANALYSIEREN zu etwa gleichen Teilen. Distraktoren plausibel.",
        4: "Schwerpunkt ANWENDEN & ANALYSIEREN (~60 %), BEWERTEN (~25 %), wenig reines Erinnern. Feine Distraktoren.",
        5: "Hochwertige Stufen: ANALYSIEREN/BEWERTEN/ERSCHAFFEN (~75 %), Mehrschritt-Reasoning, sehr plausible, nah beieinanderliegende Distraktoren.",
    }
    d = max(1, min(5, int(difficulty)))
    return f"Schwierigkeitsstufe {d}/5 – {table[d]}"


GROUNDING_RULE = (
    "STRIKTES GROUNDING: Stütze dich ausschließlich auf (a) den bereitgestellten "
    "Notebook-Code samt Kommentaren und Markdown sowie (b) allgemein anerkanntes, "
    "gesichertes Fachwissen der dort verwendeten Bibliotheken. Erfinde NIEMALS "
    "API-Signaturen, Parameternamen, Default-Werte, Kennzahlen oder Funktionsverhalten. "
    "Wenn du dir nicht sicher bist, formuliere allgemeiner statt zu spekulieren."
)
