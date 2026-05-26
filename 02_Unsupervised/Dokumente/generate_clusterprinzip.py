"""
Hierarchisches Clustering – Prinzipdarstellung
================================================
Erzeugt eine Grafik mit zwei Ansichten:
  Links:  Dendrogramm-Baum (Baumstruktur der Verschmelzungsschritte)
  Rechts: Verschachtelte Cluster-Ellipsen (Mengendarstellung)

Verwendung:
    python generate_clusterprinzip.py

Ausgabe:
    clusterprinzip.png  (300 dpi)
    clusterprinzip.pdf  (Vektorgrafik)

Abhängigkeiten:
    pip install matplotlib numpy
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Ellipse

# ──────────────────────────────────────────────
# Farbpalette
# ──────────────────────────────────────────────
C_PRIMARY    = "#1B5E7B"
C_ACCENT     = "#E8882F"
C_NODE_FILL  = "#D5EAF4"
C_NODE_EDGE  = "#1B5E7B"
C_LEAF_FILL  = "#FDE68A"
C_LEAF_EDGE  = "#D4A017"
C_LEAF_TEXT  = "#4A3800"
C_LINE       = "#3A3A3A"
C_ELLIPSE    = "#1B7EAD"
C_ELL_FILL   = "#EAF5FB"
C_BG         = "#FFFFFF"
C_TEXT       = "#1A3A4A"

# ──────────────────────────────────────────────
# Positionen für den Baum (links)
# ──────────────────────────────────────────────
# Innere Knoten (Verschmelzungsschritte)
nodes = {
    4: (5.0, 9.0),
    3: (3.5, 7.0),
    1: (2.0, 5.0),
    2: (5.0, 5.0),
}

# Blätter (Datenpunkte)
leaves = {
    "A": (1.2, 3.0),
    "B": (2.8, 3.0),
    "C": (4.2, 3.0),
    "D": (5.8, 3.0),
    "E": (7.5, 3.0),
}

# Kanten: (Eltern-Knoten, Kind)
edges = [
    (4, 3),
    (4, "E"),
    (3, 1),
    (3, 2),
    (1, "A"),
    (1, "B"),
    (2, "C"),
    (2, "D"),
]


def get_pos(key):
    if isinstance(key, int):
        return nodes[key]
    return leaves[key]


# ──────────────────────────────────────────────
# Zeichenfunktionen
# ──────────────────────────────────────────────
def draw_tree(ax):
    """Zeichnet den Dendrogramm-Baum."""

    # Kanten zeichnen (mit rechtwinkligen Verbindungen)
    for parent, child in edges:
        px, py = get_pos(parent)
        cx, cy = get_pos(child)
        # Vertikale Linie vom Eltern nach unten, dann horizontal zum Kind
        mid_y = py - 0.7
        ax.plot([px, px], [py - 0.45, mid_y], color=C_LINE, linewidth=1.5,
                solid_capstyle="round", zorder=1)
        ax.plot([px, cx], [mid_y, mid_y], color=C_LINE, linewidth=1.5,
                solid_capstyle="round", zorder=1)
        ax.plot([cx, cx], [mid_y, cy + 0.45], color=C_LINE, linewidth=1.5,
                solid_capstyle="round", zorder=1)

    # Innere Knoten (Rechtecke mit abgerundeten Ecken)
    for label, (x, y) in nodes.items():
        box = FancyBboxPatch(
            (x - 0.42, y - 0.40), 0.84, 0.80,
            boxstyle="round,pad=0.08",
            facecolor=C_NODE_FILL, edgecolor=C_NODE_EDGE,
            linewidth=1.8, zorder=3
        )
        ax.add_patch(box)
        ax.text(x, y, str(label), ha="center", va="center",
                fontsize=15, fontweight="bold", color=C_PRIMARY, zorder=4)

    # Blätter (Kreise)
    for label, (x, y) in leaves.items():
        circle = plt.Circle(
            (x, y), 0.42,
            facecolor=C_LEAF_FILL, edgecolor=C_LEAF_EDGE,
            linewidth=1.8, zorder=3
        )
        ax.add_patch(circle)
        ax.text(x, y, label, ha="center", va="center",
                fontsize=14, fontweight="bold", color=C_LEAF_TEXT, zorder=4)

    # Beschriftung
    ax.text(4.3, 10.2, "Dendrogramm (Baumstruktur)",
            ha="center", va="center", fontsize=12, fontweight="bold",
            color=C_PRIMARY, fontfamily="sans-serif")

    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(1.5, 10.8)
    ax.set_aspect("equal")
    ax.axis("off")


def draw_ellipses(ax):
    """Zeichnet die verschachtelten Cluster-Ellipsen."""

    # Ellipsen von außen nach innen (Reihenfolge für korrektes Layering)
    ellipses = [
        {"label": "4", "center": (5.5, 5.0), "w": 10.5, "h": 6.2,
         "color": C_ELLIPSE, "alpha": 0.06, "ls": "-",  "lw": 2.2},
        {"label": "3", "center": (4.3, 5.0), "w": 7.8,  "h": 4.8,
         "color": C_ELLIPSE, "alpha": 0.07, "ls": "--", "lw": 1.6},
        {"label": "1", "center": (2.8, 5.0), "w": 3.4,  "h": 3.0,
         "color": C_ELLIPSE, "alpha": 0.08, "ls": "-.", "lw": 1.4},
        {"label": "2", "center": (5.8, 5.0), "w": 3.4,  "h": 3.0,
         "color": C_ELLIPSE, "alpha": 0.08, "ls": "-.", "lw": 1.4},
    ]

    for e in ellipses:
        ell = Ellipse(
            e["center"], e["w"], e["h"],
            facecolor=(*plt.cm.colors.to_rgb(e["color"]), e["alpha"]),
            edgecolor=e["color"], linewidth=e["lw"],
            linestyle=e["ls"], zorder=2
        )
        ax.add_patch(ell)

        # Label oben rechts an der Ellipse
        cx, cy = e["center"]
        lx = cx + e["w"] * 0.38
        ly = cy + e["h"] * 0.40
        ax.text(lx, ly, e["label"], fontsize=13, fontweight="bold",
                color=C_ELLIPSE, fontstyle="italic", zorder=5,
                fontfamily="sans-serif")

    # Datenpunkte als Kreise
    data_points = {
        "A": (2.0, 5.0),
        "B": (3.6, 5.0),
        "C": (5.0, 5.0),
        "D": (6.6, 5.0),
        "E": (9.2, 5.0),
    }

    for label, (x, y) in data_points.items():
        circle = plt.Circle(
            (x, y), 0.52,
            facecolor=C_LEAF_FILL, edgecolor=C_LEAF_EDGE,
            linewidth=1.8, zorder=6
        )
        ax.add_patch(circle)
        ax.text(x, y, label, ha="center", va="center",
                fontsize=14, fontweight="bold", color=C_LEAF_TEXT, zorder=7)

    # Beschriftung
    ax.text(5.5, 8.8, "Cluster-Verschachtelung (Mengendarstellung)",
            ha="center", va="center", fontsize=12, fontweight="bold",
            color=C_PRIMARY, fontfamily="sans-serif")

    ax.set_xlim(-0.5, 11.5)
    ax.set_ylim(1.5, 9.5)
    ax.set_aspect("equal")
    ax.axis("off")


# ──────────────────────────────────────────────
# Grafik zusammensetzen
# ──────────────────────────────────────────────
fig, (ax_tree, ax_ell) = plt.subplots(1, 2, figsize=(15, 6.5),
                                       facecolor=C_BG,
                                       gridspec_kw={"width_ratios": [1, 1.3]})
fig.subplots_adjust(wspace=0.05, left=0.02, right=0.98, top=0.92, bottom=0.04)

# Haupttitel
fig.text(0.5, 0.97, "Prinzip des hierarchischen Clustering",
         ha="center", va="top", fontsize=18, fontweight="bold",
         color=C_PRIMARY, fontfamily="sans-serif")

draw_tree(ax_tree)
draw_ellipses(ax_ell)

# Verbindungspfeil zwischen beiden Darstellungen
fig.text(0.465, 0.48, "⟷", ha="center", va="center",
         fontsize=28, color=C_ACCENT, fontweight="bold")

# ──────────────────────────────────────────────
# Speichern
# ──────────────────────────────────────────────
OUTPUT_PNG = "clusterprinzip.png"
OUTPUT_PDF = "clusterprinzip.pdf"

fig.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight", facecolor=C_BG)
fig.savefig(OUTPUT_PDF, bbox_inches="tight", facecolor=C_BG)
plt.close(fig)

print(f"PNG gespeichert: {OUTPUT_PNG}")
print(f"PDF gespeichert: {OUTPUT_PDF}")
