"""
Visualisierungen für das Dokument:
"Zustandsautomaten als Denkwerkzeug für LangGraph-Agenten"

Erzeugt alle Grafik-Platzhalter als PNG-Dateien.
Anpassbar in VS Code — Farben, Positionen, Schriftgrößen.

Abhängigkeiten:
    pip install matplotlib numpy

Benutzung:
    python visualisierungen.py          # Erzeugt alle PNGs
    python visualisierungen.py --show   # Zeigt die Diagramme an statt zu speichern
"""

import matplotlib
matplotlib.use("Agg")  # Für Headless-Umgebungen; entfernen wenn --show genutzt wird
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np
import sys
import os

# ══════════════════════════════════════════════════════════════
# KONFIGURATION — hier anpassen
# ══════════════════════════════════════════════════════════════

SHOW = "--show" in sys.argv
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# House-Stil Farben (passend zum DOCX)
C = {
    "primary":    "#1B4F72",
    "secondary":  "#2E86C1",
    "accent":     "#D4E6F1",
    "light_bg":   "#EBF5FB",
    "dark_text":  "#1C2833",
    "mid_text":   "#566573",
    "node_fill":  "#D4E6F1",
    "node_edge":  "#1B4F72",
    "arrow":      "#2E86C1",
    "cycle_arrow":"#E74C3C",
    "start_fill": "#27AE60",
    "end_fill":   "#1B4F72",
    "mealy_fill": "#FADBD8",
    "mealy_edge": "#C0392B",
    "moore_fill": "#D5F5E3",
    "moore_edge": "#1E8449",
    "bg":         "#FFFFFF",
}

FONT = {"family": "Arial", "size": 11}
plt.rcParams.update({
    "font.family": FONT["family"],
    "font.size": FONT["size"],
    "figure.facecolor": C["bg"],
    "axes.facecolor": C["bg"],
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.3,
})


# ══════════════════════════════════════════════════════════════
# ZEICHENHILFEN
# ══════════════════════════════════════════════════════════════

def draw_state(ax, xy, label, fill=None, edge_color=None, fontsize=11,
               is_end=False, is_start_arrow=False, width=1.6, height=0.7,
               sublabel=None):
    """Zeichnet einen Zustandsknoten (abgerundetes Rechteck)."""
    fill = fill or C["node_fill"]
    edge_color = edge_color or C["node_edge"]
    x, y = xy

    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle=f"round,pad=0.12",
        facecolor=fill, edgecolor=edge_color, linewidth=2,
        zorder=3
    )
    ax.add_patch(box)

    if is_end:
        inner = FancyBboxPatch(
            (x - width/2 + 0.06, y - height/2 + 0.06),
            width - 0.12, height - 0.12,
            boxstyle=f"round,pad=0.08",
            facecolor="none", edgecolor=edge_color, linewidth=1.5,
            zorder=4
        )
        ax.add_patch(inner)

    ax.text(x, y + (0.08 if sublabel else 0), label,
            ha="center", va="center", fontsize=fontsize,
            fontweight="bold", color=C["dark_text"], zorder=5)

    if sublabel:
        ax.text(x, y - 0.18, sublabel,
                ha="center", va="center", fontsize=fontsize - 2,
                color=C["mid_text"], fontstyle="italic", zorder=5)

    if is_start_arrow:
        ax.annotate("", xy=(x - width/2, y), xytext=(x - width/2 - 0.5, y),
                    arrowprops=dict(arrowstyle="-|>", color=C["start_fill"],
                                   lw=2.5, mutation_scale=18), zorder=5)


def draw_dot(ax, xy, label="", color=None, size=0.15):
    """Zeichnet einen Start-/End-Punkt."""
    color = color or C["end_fill"]
    circle = Circle(xy, size, facecolor=color, edgecolor=color, linewidth=2, zorder=3)
    ax.add_patch(circle)
    if label:
        ax.text(xy[0], xy[1] - size - 0.15, label,
                ha="center", va="top", fontsize=9, color=C["mid_text"])


def draw_arrow(ax, start, end, label="", color=None, style="-|>",
               connectionstyle="arc3,rad=0", fontsize=9, lw=2,
               label_offset=(0, 0.15)):
    """Zeichnet einen Übergangspfeil."""
    color = color or C["arrow"]
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle=style, color=color,
                               lw=lw, mutation_scale=16,
                               connectionstyle=connectionstyle),
                zorder=2)
    if label:
        mid_x = (start[0] + end[0]) / 2 + label_offset[0]
        mid_y = (start[1] + end[1]) / 2 + label_offset[1]
        ax.text(mid_x, mid_y, label, ha="center", va="center",
                fontsize=fontsize, color=color, fontstyle="italic",
                bbox=dict(boxstyle="round,pad=0.15", facecolor=C["bg"],
                         edgecolor="none", alpha=0.85),
                zorder=6)


def setup_ax(ax, xlim, ylim):
    """Konfiguriert Achsen."""
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect("equal")
    ax.axis("off")


def save_or_show(fig, filename):
    """Speichert oder zeigt die Grafik."""
    if SHOW:
        plt.show()
    else:
        path = os.path.join(OUTPUT_DIR, filename)
        fig.savefig(path)
        print(f"  ✓ {filename}")
    plt.close(fig)


# ══════════════════════════════════════════════════════════════
# ABB. 1: DREHKREUZ (DEA)
# ══════════════════════════════════════════════════════════════

def fig1_turnstile():
    fig, ax = plt.subplots(figsize=(9, 4))
    setup_ax(ax, (-1.5, 8), (-1.5, 2.5))

    draw_state(ax, (1.5, 0.5), "gesperrt", is_start_arrow=True)
    draw_state(ax, (5.5, 0.5), "entsperrt")

    # Übergänge
    draw_arrow(ax, (2.3, 0.8), (4.65, 0.8), "Münze",
               connectionstyle="arc3,rad=0.3", label_offset=(0, 0.3))
    draw_arrow(ax, (4.7, 0.2), (2.3, 0.2), "Durchgehen",
               connectionstyle="arc3,rad=0.3", label_offset=(0, -0.35))

    # Selbstschleifen
    draw_arrow(ax, (1.2, 1.0), (0.9, 0.85), "Durchgehen",
               connectionstyle="arc3,rad=-2.5", label_offset=(-0.7, 0.7),
               color=C["mid_text"])
    draw_arrow(ax, (5.8, 1.0), (6.1, 0.85), "Münze",
               connectionstyle="arc3,rad=2.5", label_offset=(0.6, 0.7),
               color=C["mid_text"])

    ax.set_title("Abb. 1: Deterministischer endlicher Automat — Drehkreuz",
                fontsize=12, fontweight="bold", color=C["primary"], pad=15)

    # Legende
    ax.text(3.5, -1.1, "Q = {gesperrt, entsperrt}     Σ = {Münze, Durchgehen}     q₀ = gesperrt",
            ha="center", fontsize=9, color=C["mid_text"],
            bbox=dict(boxstyle="round,pad=0.3", facecolor=C["light_bg"],
                     edgecolor=C["secondary"], alpha=0.7))

    save_or_show(fig, "turnstile_dea.png")


# ══════════════════════════════════════════════════════════════
# ABB. 2: MOORE-AUTOMAT (GETRÄNKEAUTOMAT)
# ══════════════════════════════════════════════════════════════

def fig2_moore():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    setup_ax(ax, (-1.5, 10), (-2, 3.5))

    # Zustände mit Ausgabe IM Knoten (Moore!)
    draw_state(ax, (1.5, 1.5), "warten", fill=C["moore_fill"],
               edge_color=C["moore_edge"], is_start_arrow=True,
               sublabel='→ "Bitte 2€"', height=0.9)
    draw_state(ax, (5, 1.5), "hat_1€", fill=C["moore_fill"],
               edge_color=C["moore_edge"],
               sublabel='→ "Noch 1€"', height=0.9)
    draw_state(ax, (8.5, 1.5), "ausgabe", fill=C["moore_fill"],
               edge_color=C["moore_edge"],
               sublabel='→ Getränk', height=0.9)
    draw_state(ax, (5, -0.8), "rückgabe", fill=C["moore_fill"],
               edge_color=C["moore_edge"],
               sublabel='→ 1€ zurück', height=0.9)

    # Kanten
    draw_arrow(ax, (2.35, 1.7), (4.15, 1.7), "Münze",
               color=C["moore_edge"], label_offset=(0, 0.25))
    draw_arrow(ax, (5.85, 1.7), (7.65, 1.7), "Münze",
               color=C["moore_edge"], label_offset=(0, 0.25))
    draw_arrow(ax, (8.5, 1.0), (2.3, 0.2), "auto",
               color=C["mid_text"], connectionstyle="arc3,rad=-0.15",
               label_offset=(0, -0.3))
    draw_arrow(ax, (4.6, 1.05), (4.6, -0.3), "Abbruch",
               color=C["moore_edge"], label_offset=(-0.55, 0))
    draw_arrow(ax, (4.2, -0.65), (2.0, 0.9), "auto",
               color=C["mid_text"], connectionstyle="arc3,rad=0.2",
               label_offset=(-0.6, 0))

    # Selbstschleife: warten + Abbruch
    draw_arrow(ax, (1.2, 2.1), (0.9, 1.95), "Abbruch",
               connectionstyle="arc3,rad=-2.5", label_offset=(-0.7, 0.5),
               color=C["mid_text"])

    ax.set_title("Abb. 2: Moore-Automat — Ausgabe steht IM Knoten",
                fontsize=12, fontweight="bold", color=C["primary"], pad=15)

    ax.text(5, -1.7, "Moore-Eigenschaft: Jeder Zustand hat eine feste Ausgabe, "
            "unabhängig von der Eingabe, die zum Zustand geführt hat.",
            ha="center", fontsize=9, color=C["moore_edge"],
            bbox=dict(boxstyle="round,pad=0.3", facecolor=C["moore_fill"],
                     edgecolor=C["moore_edge"], alpha=0.7))

    save_or_show(fig, "moore_automat.png")


# ══════════════════════════════════════════════════════════════
# ABB. 3: MOORE vs. MEALY VERGLEICH
# ══════════════════════════════════════════════════════════════

def fig3_moore_vs_mealy():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))

    # --- Moore (links) ---
    setup_ax(ax1, (-1, 6.5), (-1, 3))

    ax1.set_title("Moore-Automat\nAusgabe im Knoten", fontsize=11,
                  fontweight="bold", color=C["moore_edge"], pad=10)

    draw_state(ax1, (1.2, 1), "q₀", fill=C["moore_fill"],
               edge_color=C["moore_edge"], is_start_arrow=True,
               sublabel="→ Y₀", height=0.85, width=1.4)
    draw_state(ax1, (4.5, 1), "q₁", fill=C["moore_fill"],
               edge_color=C["moore_edge"],
               sublabel="→ Y₁", height=0.85, width=1.4)

    draw_arrow(ax1, (1.95, 1.25), (3.75, 1.25), "a",
               color=C["moore_edge"], label_offset=(0, 0.25))
    draw_arrow(ax1, (3.75, 0.75), (1.95, 0.75), "b",
               color=C["moore_edge"], label_offset=(0, -0.3),
               connectionstyle="arc3,rad=0.0")

    ax1.text(2.85, -0.5, "λ(q) → Ausgabe\nhängt NUR vom Zustand ab",
             ha="center", fontsize=9, color=C["moore_edge"],
             bbox=dict(boxstyle="round,pad=0.3", facecolor=C["moore_fill"],
                      edgecolor=C["moore_edge"]))

    # --- Mealy (rechts) ---
    setup_ax(ax2, (-1, 6.5), (-1, 3))

    ax2.set_title("Mealy-Automat\nAusgabe an der Kante", fontsize=11,
                  fontweight="bold", color=C["mealy_edge"], pad=10)

    draw_state(ax2, (1.2, 1), "q₀", fill=C["mealy_fill"],
               edge_color=C["mealy_edge"], is_start_arrow=True,
               height=0.7, width=1.4)
    draw_state(ax2, (4.5, 1), "q₁", fill=C["mealy_fill"],
               edge_color=C["mealy_edge"],
               height=0.7, width=1.4)

    draw_arrow(ax2, (1.95, 1.2), (3.75, 1.2), "a / Y₀",
               color=C["mealy_edge"], label_offset=(0, 0.25))
    draw_arrow(ax2, (3.75, 0.8), (1.95, 0.8), "b / Y₁",
               color=C["mealy_edge"], label_offset=(0, -0.3),
               connectionstyle="arc3,rad=0.0")

    ax2.text(2.85, -0.5, "λ(q, a) → Ausgabe\nhängt von Zustand UND Eingabe ab",
             ha="center", fontsize=9, color=C["mealy_edge"],
             bbox=dict(boxstyle="round,pad=0.3", facecolor=C["mealy_fill"],
                      edgecolor=C["mealy_edge"]))

    fig.suptitle("Abb. 3: Vergleich der Notationen — Moore vs. Mealy",
                fontsize=12, fontweight="bold", color=C["primary"], y=1.02)

    plt.tight_layout()
    save_or_show(fig, "moore_vs_mealy.png")


# ══════════════════════════════════════════════════════════════
# ABB. 4: BRÜCKE ZUM ERWEITERTEN AUTOMATEN
# ══════════════════════════════════════════════════════════════

def fig4_efsm_bridge():
    fig, ax = plt.subplots(figsize=(11, 5))
    setup_ax(ax, (-0.5, 11), (-1.5, 4))

    # DEA (links)
    ax.text(2.5, 3.5, "Einfacher DEA", ha="center", fontsize=11,
            fontweight="bold", color=C["mid_text"])
    ax.text(2.5, 3.0, "Zustand = nur Kontrollzustand", ha="center",
            fontsize=9, color=C["mid_text"])

    draw_state(ax, (1.2, 1.5), "q₀", width=1.0, height=0.6, is_start_arrow=True)
    draw_state(ax, (3.8, 1.5), "q₁", width=1.0, height=0.6)
    draw_arrow(ax, (1.75, 1.5), (3.25, 1.5), "a")

    ax.text(2.5, 0.2, "δ(q, a) → q'", ha="center", fontsize=10,
            color=C["primary"], fontstyle="italic")

    # Pfeil in der Mitte
    ax.annotate("", xy=(6.5, 1.5), xytext=(5.3, 1.5),
                arrowprops=dict(arrowstyle="-|>", color=C["start_fill"],
                               lw=3, mutation_scale=22))
    ax.text(5.9, 2.0, "erweitern", ha="center", fontsize=10,
            color=C["start_fill"], fontweight="bold")

    # EFSM (rechts)
    ax.text(8.5, 3.5, "Erweiterter Automat (EFSM)", ha="center", fontsize=11,
            fontweight="bold", color=C["primary"])
    ax.text(8.5, 3.0, "Zustand = Kontrollzustand + Datenzustand", ha="center",
            fontsize=9, color=C["primary"])

    draw_state(ax, (7.2, 1.5), "q₀", width=1.0, height=0.6,
               fill=C["accent"], is_start_arrow=False)
    draw_state(ax, (9.8, 1.5), "q₁", width=1.0, height=0.6,
               fill=C["accent"])
    draw_arrow(ax, (7.75, 1.5), (9.25, 1.5), "δ(q, D)",
               color=C["primary"])

    # Rucksack-Symbol
    rucksack = FancyBboxPatch((7.7, 0.0), 2.0, 0.7,
                              boxstyle="round,pad=0.1",
                              facecolor="#FEF9E7", edgecolor="#F39C12",
                              linewidth=1.5, zorder=3)
    ax.add_patch(rucksack)
    ax.text(8.7, 0.35, "D = {zähler: 2, ...}", ha="center", fontsize=9,
            color="#7D6608", fontweight="bold", zorder=5)
    ax.text(8.7, -0.15, "Datenzustand (Rucksack)", ha="center", fontsize=8,
            color="#B7950B", fontstyle="italic")

    # Verbindungslinie Rucksack → Knoten
    ax.plot([8.7, 8.7], [0.7, 1.15], color="#F39C12", lw=1.5,
            linestyle="--", zorder=1)

    ax.text(8.5, -1.0, "δ(q, D) → (q', D')  —  Nächster Zustand UND Datenupdate",
            ha="center", fontsize=10, color=C["primary"], fontstyle="italic",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=C["light_bg"],
                     edgecolor=C["secondary"]))

    save_or_show(fig, "efsm_bridge.png")


# ══════════════════════════════════════════════════════════════
# ABB. 5: KONZEPT 1 — LINEARER GRAPH
# ══════════════════════════════════════════════════════════════

def fig5_konzept1():
    fig, ax = plt.subplots(figsize=(10, 3))
    setup_ax(ax, (-1.5, 10.5), (-0.5, 2))

    draw_dot(ax, (-0.3, 0.8), "START", color=C["start_fill"])
    draw_state(ax, (2, 0.8), "empfangen", is_start_arrow=False)
    draw_state(ax, (5, 0.8), "verarbeiten")
    draw_state(ax, (8, 0.8), "ausgeben")
    draw_dot(ax, (9.8, 0.8), "END", color=C["end_fill"])

    draw_arrow(ax, (-0.15, 0.8), (1.15, 0.8))
    draw_arrow(ax, (2.85, 0.8), (4.15, 0.8))
    draw_arrow(ax, (5.85, 0.8), (7.15, 0.8))
    draw_arrow(ax, (8.85, 0.8), (9.65, 0.8))

    ax.set_title("Abb. 5: Linearer Graph — Konzept 1: Kontrollfluss",
                fontsize=11, fontweight="bold", color=C["primary"], pad=10)

    save_or_show(fig, "konzept1_linear.png")


# ══════════════════════════════════════════════════════════════
# ABB. 6: KONZEPT 2 — VERZWEIGUNG
# ══════════════════════════════════════════════════════════════

def fig6_konzept2():
    fig, ax = plt.subplots(figsize=(10, 5))
    setup_ax(ax, (-1.5, 10.5), (-1.5, 3.5))

    draw_dot(ax, (-0.3, 1), "START", color=C["start_fill"])
    draw_state(ax, (2, 1), "klassifizieren")
    draw_state(ax, (5.5, 2.5), "recherchieren")
    draw_state(ax, (5.5, -0.5), "antworten")
    draw_state(ax, (8.5, 1), "ausgeben")
    draw_dot(ax, (10, 1), "END", color=C["end_fill"])

    draw_arrow(ax, (-0.15, 1), (1.15, 1))
    draw_arrow(ax, (2.85, 1.2), (4.65, 2.3), '"recherche"',
               label_offset=(-0.2, 0.3))
    draw_arrow(ax, (2.85, 0.8), (4.65, -0.3), '"direkt"',
               label_offset=(-0.2, -0.3))
    draw_arrow(ax, (6.35, 2.3), (7.65, 1.2))
    draw_arrow(ax, (6.35, -0.3), (7.65, 0.8))
    draw_arrow(ax, (9.35, 1), (9.85, 1))

    # Routing-Raute
    diamond = plt.Polygon([(2.8, 1), (3.3, 1.35), (3.8, 1), (3.3, 0.65)],
                          facecolor="#FEF9E7", edgecolor="#F39C12",
                          linewidth=1.5, zorder=4)
    ax.add_patch(diamond)
    ax.text(3.3, 1, "?", ha="center", va="center", fontsize=12,
            fontweight="bold", color="#F39C12", zorder=5)

    ax.set_title("Abb. 6: Bedingter Übergang — Konzept 2: Verzweigung",
                fontsize=11, fontweight="bold", color=C["primary"], pad=10)

    save_or_show(fig, "konzept2_branch.png")


# ══════════════════════════════════════════════════════════════
# ABB. 7: KONZEPT 3 — DATENZUSTAND / RUCKSACK
# ══════════════════════════════════════════════════════════════

def fig7_konzept3():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    setup_ax(ax, (-1, 10.5), (-2.2, 3.5))

    draw_dot(ax, (-0.3, 1.5), "START", color=C["start_fill"])
    draw_state(ax, (2, 1.5), "empfangen")
    draw_state(ax, (5, 1.5), "verarbeiten")
    draw_state(ax, (8, 1.5), "ausgeben")
    draw_dot(ax, (9.8, 1.5), "END", color=C["end_fill"])

    draw_arrow(ax, (-0.15, 1.5), (1.15, 1.5))
    draw_arrow(ax, (2.85, 1.5), (4.15, 1.5))
    draw_arrow(ax, (5.85, 1.5), (7.15, 1.5))
    draw_arrow(ax, (8.85, 1.5), (9.65, 1.5))

    # Rucksack darunter
    rucksack = FancyBboxPatch((1.2, -1.6), 7.5, 1.5,
                              boxstyle="round,pad=0.15",
                              facecolor="#FEF9E7", edgecolor="#F39C12",
                              linewidth=2, zorder=3, linestyle="--")
    ax.add_patch(rucksack)
    ax.text(5, -0.5, "State (Rucksack)", ha="center", fontsize=11,
            fontweight="bold", color="#7D6608", zorder=5)
    ax.text(5, -1.0, 'nachrichten: [...]    route: "..."    ergebnis: "..."    fehler_zähler: 0',
            ha="center", fontsize=9, color="#7D6608", zorder=5,
            fontfamily="monospace")

    # Pfeile: Knoten ↔ Rucksack
    for x in [2, 5, 8]:
        ax.annotate("", xy=(x, -0.25), xytext=(x, 1.1),
                    arrowprops=dict(arrowstyle="<->", color="#F39C12",
                                   lw=1.5, linestyle="--"))

    ax.text(2, 0.4, "liest &\nschreibt", ha="center", fontsize=8,
            color="#B7950B", fontstyle="italic")
    ax.text(5, 0.4, "liest &\nschreibt", ha="center", fontsize=8,
            color="#B7950B", fontstyle="italic")
    ax.text(8, 0.4, "liest &\nschreibt", ha="center", fontsize=8,
            color="#B7950B", fontstyle="italic")

    ax.set_title("Abb. 7: Datenzustand — Konzept 3: Der Rucksack",
                fontsize=11, fontweight="bold", color=C["primary"], pad=10)

    save_or_show(fig, "konzept3_state.png")


# ══════════════════════════════════════════════════════════════
# ABB. 8: KONZEPT 4 — ZYKLUS
# ══════════════════════════════════════════════════════════════

def fig8_konzept4():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    setup_ax(ax, (-1.5, 10.5), (-1.5, 4.5))

    draw_dot(ax, (-0.3, 1.5), "START", color=C["start_fill"])
    draw_state(ax, (2, 1.5), "planen")
    draw_state(ax, (4.8, 1.5), "tool_aufrufen", width=1.9)
    draw_state(ax, (7.6, 1.5), "prüfen")
    draw_state(ax, (7.6, -0.7), "antworten")
    draw_dot(ax, (9.5, -0.7), "END", color=C["end_fill"])

    draw_arrow(ax, (-0.15, 1.5), (1.15, 1.5))
    draw_arrow(ax, (2.85, 1.5), (3.8, 1.5))
    draw_arrow(ax, (5.75, 1.5), (6.75, 1.5))
    draw_arrow(ax, (7.6, 1.1), (7.6, -0.3), '"fertig"',
               label_offset=(0.55, 0))
    draw_arrow(ax, (8.45, -0.7), (9.35, -0.7))

    # Zyklus-Pfeil (rot, prominent)
    draw_arrow(ax, (6.8, 1.85), (2.85, 1.85), '"nochmal"',
               color=C["cycle_arrow"], lw=2.5,
               connectionstyle="arc3,rad=0.35",
               label_offset=(0, 0.7))

    # Zyklus-Markierung
    cycle_box = FancyBboxPatch((1.2, 2.9), 7, 0.7,
                               boxstyle="round,pad=0.1",
                               facecolor="#FADBD8", edgecolor=C["cycle_arrow"],
                               linewidth=1.5, zorder=1, alpha=0.3)
    ax.add_patch(cycle_box)
    ax.text(4.7, 3.25, "◀ Zyklus: planen → tool_aufrufen → prüfen → planen",
            ha="center", fontsize=9, color=C["cycle_arrow"], fontweight="bold")

    # Abbruchbedingung
    ax.text(5, -1.2, "⚠ Abbruchbedingung: fehler_zähler ≥ 3  ODER  ergebnis_ok == True",
            ha="center", fontsize=9, color=C["cycle_arrow"],
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#FADBD8",
                     edgecolor=C["cycle_arrow"], alpha=0.7))

    ax.set_title("Abb. 8: Agent mit Zyklus — Konzept 4: Retry-Muster",
                fontsize=11, fontweight="bold", color=C["primary"], pad=10)

    save_or_show(fig, "konzept4_zyklus.png")


# ══════════════════════════════════════════════════════════════
# ABB. 9: LESEBEISPIEL (QUALITÄTSSCHLEIFE)
# ══════════════════════════════════════════════════════════════

def fig9_lesebeispiel():
    fig, ax = plt.subplots(figsize=(11, 5.5))
    setup_ax(ax, (-1.5, 11.5), (-1.5, 4.5))

    draw_dot(ax, (-0.3, 1.5), "START", color=C["start_fill"])
    draw_state(ax, (2, 1.5), "analysieren")
    draw_state(ax, (4.8, 1.5), "generieren")
    draw_state(ax, (7.5, 1.5), "bewerten")
    draw_state(ax, (7.5, 3.5), "verbessern")
    draw_state(ax, (7.5, -0.7), "ausgeben")
    draw_dot(ax, (9.5, -0.7), "END", color=C["end_fill"])

    draw_arrow(ax, (-0.15, 1.5), (1.15, 1.5))
    draw_arrow(ax, (2.85, 1.5), (3.95, 1.5))
    draw_arrow(ax, (5.65, 1.5), (6.65, 1.5))
    draw_arrow(ax, (7.5, 1.1), (7.5, -0.3), '"ausgeben"',
               label_offset=(0.6, 0))
    draw_arrow(ax, (8.35, -0.7), (9.35, -0.7))

    # Zyklus
    draw_arrow(ax, (7.9, 1.85), (7.9, 3.1), '"verbessern"',
               label_offset=(0.7, 0), color=C["cycle_arrow"])
    draw_arrow(ax, (6.65, 3.5), (5.2, 1.85), "",
               color=C["cycle_arrow"], connectionstyle="arc3,rad=0.15")

    # Zyklus-Label
    ax.text(4.5, 3.7, "Zyklus: generieren → bewerten → verbessern → generieren",
            ha="center", fontsize=9, color=C["cycle_arrow"], fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#FADBD8",
                     edgecolor=C["cycle_arrow"], alpha=0.5))

    # State-Info
    ax.text(5, -1.2, "State: { frage: str, antwort: str, qualitaet: str }",
            ha="center", fontsize=9, color=C["primary"], fontfamily="monospace",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=C["light_bg"],
                     edgecolor=C["secondary"]))

    ax.set_title("Abb. 9: Lesebeispiel — Qualitätsschleife (Kap. 11)",
                fontsize=11, fontweight="bold", color=C["primary"], pad=10)

    save_or_show(fig, "lesebeispiel_loesung.png")


# ══════════════════════════════════════════════════════════════
# ALLE GENERIEREN
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generiere Visualisierungen...")
    fig1_turnstile()
    fig2_moore()
    fig3_moore_vs_mealy()
    fig4_efsm_bridge()
    fig5_konzept1()
    fig6_konzept2()
    fig7_konzept3()
    fig8_konzept4()
    fig9_lesebeispiel()
    print(f"\nFertig! {9} Dateien erzeugt in: {OUTPUT_DIR}")
    print("\nTipp: python visualisierungen.py --show  zum Anzeigen statt Speichern")
