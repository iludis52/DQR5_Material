"""
Linkage-Methoden – Diagrammgenerator
=====================================
Erzeugt eine Übersichtsgrafik der fünf gängigen Linkage-Methoden
für hierarchisches Clustering (Single, Complete, Average, Centroid, Ward).

Verwendung:
    python generate_linkage_diagrams.py

Ausgabe:
    linkage_methoden.png  (300 dpi, transparenter Hintergrund optional)

Abhängigkeiten:
    pip install matplotlib numpy
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from itertools import product as cartesian

# ──────────────────────────────────────────────
# Farbpalette (konsistent mit dem Word-Dokument)
# ──────────────────────────────────────────────
C_PRIMARY   = "#1B5E7B"
C_ACCENT    = "#E8882F"
C_BLUE_DOT  = "#1B7EAD"
C_ORANGE_DOT = "#E8882F"
C_LINE      = "#1B7EAD"
C_BG_CARD   = "#F4FAFE"
C_BG_GRID   = "#E8F2F8"
C_BORDER    = "#B8D6E8"
C_TEXT      = "#1A3A4A"
C_FORMULA   = "#555555"
C_WHITE     = "#FFFFFF"

# ──────────────────────────────────────────────
# Cluster-Punkte (fixe Positionen, reproduzierbar)
# ──────────────────────────────────────────────
np.random.seed(42)

# Cluster 1 (links) und Cluster 2 (rechts) – je 4 Punkte
C1 = np.array([[1.0, 2.8], [1.6, 1.8], [0.8, 1.4], [1.8, 2.5]])
C2 = np.array([[3.8, 2.6], [4.4, 1.6], [3.6, 1.2], [4.2, 2.9]])


def draw_cluster_points(ax, c1, c2):
    """Zeichnet die Punkte beider Cluster."""
    ax.scatter(*c1.T, s=70, color=C_ORANGE_DOT, zorder=5, edgecolors="white", linewidths=0.5)
    ax.scatter(*c2.T, s=70, color=C_BLUE_DOT,   zorder=5, edgecolors="white", linewidths=0.5)


def draw_cluster_labels(ax):
    """Beschriftung Cluster 1 / Cluster 2."""
    ax.text(1.3, 3.55, "Cluster 1", ha="center", fontsize=7.5,
            fontweight="bold", color=C_ACCENT)
    ax.text(4.0, 3.55, "Cluster 2", ha="center", fontsize=7.5,
            fontweight="bold", color=C_BLUE_DOT)


def setup_ax(ax):
    """Einheitliche Achsen-Einstellungen."""
    ax.set_xlim(-0.2, 5.4)
    ax.set_ylim(0.3, 3.9)
    ax.set_aspect("equal")
    ax.axis("off")


# ──────────────────────────────────────────────
# 1) Single Linkage
# ──────────────────────────────────────────────
def draw_single(ax):
    # Nächstes Paar finden
    dists = [np.linalg.norm(a - b) for a, b in cartesian(C1, C2)]
    pairs = [(a, b) for a, b in cartesian(C1, C2)]
    i_min = np.argmin(dists)
    a, b = pairs[i_min]

    draw_cluster_points(ax, C1, C2)
    ax.plot([a[0], b[0]], [a[1], b[1]], color=C_LINE, linewidth=2.2,
            linestyle="-", zorder=4, alpha=0.85)
    # Kleine Marker an den Endpunkten
    for p in [a, b]:
        ax.plot(*p, "o", color=C_LINE, markersize=8, zorder=6, alpha=0.3)

    draw_cluster_labels(ax)
    setup_ax(ax)


# ──────────────────────────────────────────────
# 2) Complete Linkage
# ──────────────────────────────────────────────
def draw_complete(ax):
    dists = [np.linalg.norm(a - b) for a, b in cartesian(C1, C2)]
    pairs = [(a, b) for a, b in cartesian(C1, C2)]
    i_max = np.argmax(dists)
    a, b = pairs[i_max]

    draw_cluster_points(ax, C1, C2)
    # Alle Verbindungen blass andeuten
    for p1, p2 in cartesian(C1, C2):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=C_LINE,
                linewidth=0.6, alpha=0.15, zorder=3)
    # Maximale Distanz hervorheben
    ax.plot([a[0], b[0]], [a[1], b[1]], color=C_LINE, linewidth=2.2,
            linestyle="-", zorder=4, alpha=0.85)
    for p in [a, b]:
        ax.plot(*p, "o", color=C_LINE, markersize=8, zorder=6, alpha=0.3)

    draw_cluster_labels(ax)
    setup_ax(ax)


# ──────────────────────────────────────────────
# 3) Average Linkage
# ──────────────────────────────────────────────
def draw_average(ax):
    draw_cluster_points(ax, C1, C2)
    # Alle paarweisen Verbindungen gleich gewichtet
    for p1, p2 in cartesian(C1, C2):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=C_LINE,
                linewidth=1.0, alpha=0.35, zorder=3)

    draw_cluster_labels(ax)
    setup_ax(ax)


# ──────────────────────────────────────────────
# 4) Centroid-Methode
# ──────────────────────────────────────────────
def draw_centroid(ax):
    m1 = C1.mean(axis=0)
    m2 = C2.mean(axis=0)

    draw_cluster_points(ax, C1, C2)
    # Zentroide als größere Rauten
    ax.scatter(*m1, s=120, color=C_ACCENT,  marker="D", zorder=6,
               edgecolors="white", linewidths=1.0)
    ax.scatter(*m2, s=120, color=C_BLUE_DOT, marker="D", zorder=6,
               edgecolors="white", linewidths=1.0)
    # Verbindung der Zentroide
    ax.plot([m1[0], m2[0]], [m1[1], m2[1]], color=C_LINE, linewidth=2.2,
            linestyle="--", zorder=4, alpha=0.85)

    draw_cluster_labels(ax)
    setup_ax(ax)


# ──────────────────────────────────────────────
# 5) Ward's Methode
# ──────────────────────────────────────────────
def draw_ward(ax):
    m1 = C1.mean(axis=0)
    m2 = C2.mean(axis=0)

    draw_cluster_points(ax, C1, C2)

    # Intra-Cluster-Linien (Varianz visualisieren)
    for p in C1:
        ax.plot([p[0], m1[0]], [p[1], m1[1]], color=C_ACCENT,
                linewidth=1.0, alpha=0.45, zorder=3)
    for p in C2:
        ax.plot([p[0], m2[0]], [p[1], m2[1]], color=C_BLUE_DOT,
                linewidth=1.0, alpha=0.45, zorder=3)

    # Zentroide dezent
    ax.scatter(*m1, s=60, color=C_ACCENT,   marker="+", zorder=6, linewidths=2)
    ax.scatter(*m2, s=60, color=C_BLUE_DOT,  marker="+", zorder=6, linewidths=2)

    draw_cluster_labels(ax)
    setup_ax(ax)


# ──────────────────────────────────────────────
# Gesamtgrafik zusammensetzen
# ──────────────────────────────────────────────
methods = [
    {
        "title":   "Single Linkage",
        "subtitle": "Nächster Nachbar",
        "formula": "D(C₁,C₂) = min D(xᵢ, xⱼ)",
        "desc":    "Minimaler Abstand zwischen\nden nächsten Elementen.",
        "draw":    draw_single,
    },
    {
        "title":   "Complete Linkage",
        "subtitle": "Entferntester Nachbar",
        "formula": "D(C₁,C₂) = max D(xᵢ, xⱼ)",
        "desc":    "Maximaler Abstand zwischen\nden entferntesten Elementen.",
        "draw":    draw_complete,
    },
    {
        "title":   "Average Linkage",
        "subtitle": "Mittlerer Abstand",
        "formula": "D(C₁,C₂) = Ø aller D(xᵢ, xⱼ)",
        "desc":    "Durchschnitt aller paarweisen\nAbstände.",
        "draw":    draw_average,
    },
    {
        "title":   "Centroid-Methode",
        "subtitle": "Schwerpunktabstand",
        "formula": "D(C₁,C₂) = ‖m₁ − m₂‖",
        "desc":    "Euklidischer Abstand zwischen\nden Cluster-Schwerpunkten.",
        "draw":    draw_centroid,
    },
    {
        "title":   "Ward's Methode",
        "subtitle": "Minimum-Varianz",
        "formula": "min Δ(Within-Cluster-Varianz)",
        "desc":    "Verschmelzung mit geringstem\nVarianz-Zuwachs.",
        "draw":    draw_ward,
    },
]

fig = plt.figure(figsize=(13, 16), facecolor=C_WHITE)
fig.subplots_adjust(left=0.02, right=0.98, top=0.94, bottom=0.02,
                    hspace=0.55, wspace=0.08)

# Titel
fig.text(0.5, 0.975, "Linkage-Methoden im Überblick",
         ha="center", va="top", fontsize=22, fontweight="bold",
         color=C_PRIMARY, fontfamily="sans-serif")
fig.text(0.5, 0.953, "Abstandsmaße für agglomeratives hierarchisches Clustering",
         ha="center", va="top", fontsize=12, color=C_FORMULA, fontfamily="sans-serif")

TOP_START = 0.77  # lowered from 0.82
ROW_H = 0.18

for idx, m in enumerate(methods):
    row = idx
    # Linke Spalte: Text-Info
    ax_text = fig.add_axes([0.04, TOP_START - row * ROW_H, 0.42, 0.155],
                           facecolor=C_BG_CARD)
    for spine in ax_text.spines.values():
        spine.set_edgecolor(C_BORDER)
        spine.set_linewidth(1.2)
    ax_text.set_xlim(0, 10)
    ax_text.set_ylim(0, 4)
    ax_text.set_xticks([])
    ax_text.set_yticks([])

    # Farbiger Seitenstreifen
    ax_text.add_patch(FancyBboxPatch(
        (0, 0), 0.3, 4, boxstyle="square,pad=0",
        facecolor=C_ACCENT if idx < 3 else C_PRIMARY, edgecolor="none", zorder=2
    ))

    # Nummerierung
    ax_text.text(0.7, 3.3, str(idx + 1), fontsize=18, fontweight="bold",
                 color=C_ACCENT if idx < 3 else C_PRIMARY, va="center", zorder=3)

    # Titel + Subtitle
    ax_text.text(1.5, 3.3, m["title"], fontsize=13, fontweight="bold",
                 color=C_PRIMARY, va="center", fontfamily="sans-serif")
    ax_text.text(1.5, 2.65, m["subtitle"], fontsize=9.5,
                 color=C_ACCENT, va="center", fontstyle="italic",
                 fontfamily="sans-serif")

    # Formel
    ax_text.text(1.5, 1.85, m["formula"], fontsize=10,
                 color=C_TEXT, va="center", fontfamily="monospace",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor=C_BG_GRID,
                           edgecolor=C_BORDER, linewidth=0.8))

    # Beschreibung
    ax_text.text(1.5, 0.75, m["desc"], fontsize=8.5,
                 color=C_FORMULA, va="center", fontfamily="sans-serif",
                 linespacing=1.5)

    # Rechte Spalte: Diagramm
    ax_diagram = fig.add_axes([0.50, TOP_START - row * ROW_H, 0.47, 0.155],
                              facecolor=C_BG_CARD)
    for spine in ax_diagram.spines.values():
        spine.set_edgecolor(C_BORDER)
        spine.set_linewidth(1.2)

    m["draw"](ax_diagram)

# ──────────────────────────────────────────────
# Speichern
# ──────────────────────────────────────────────
OUTPUT = "linkage_methoden.png"
fig.savefig(OUTPUT, dpi=300, bbox_inches="tight", facecolor=C_WHITE)
plt.close(fig)
print(f"Grafik gespeichert: {OUTPUT}")

# Optional: auch als PDF (vektorgrafik)
OUTPUT_PDF = "linkage_methoden.pdf"
fig2 = plt.figure(figsize=(13, 16), facecolor=C_WHITE)
fig2.subplots_adjust(left=0.02, right=0.98, top=0.94, bottom=0.02,
                     hspace=0.55, wspace=0.08)
fig2.text(0.5, 0.975, "Linkage-Methoden im Überblick",
          ha="center", va="top", fontsize=22, fontweight="bold",
          color=C_PRIMARY, fontfamily="sans-serif")
fig2.text(0.5, 0.953, "Abstandsmaße für agglomeratives hierarchisches Clustering",
          ha="center", va="top", fontsize=12, color=C_FORMULA, fontfamily="sans-serif")

for idx, m in enumerate(methods):
    row = idx
    ax_text = fig2.add_axes([0.04, TOP_START - row * ROW_H, 0.42, 0.155],
                            facecolor=C_BG_CARD)
    for spine in ax_text.spines.values():
        spine.set_edgecolor(C_BORDER)
        spine.set_linewidth(1.2)
    ax_text.set_xlim(0, 10)
    ax_text.set_ylim(0, 4)
    ax_text.set_xticks([])
    ax_text.set_yticks([])
    ax_text.add_patch(FancyBboxPatch(
        (0, 0), 0.3, 4, boxstyle="square,pad=0",
        facecolor=C_ACCENT if idx < 3 else C_PRIMARY, edgecolor="none", zorder=2
    ))
    ax_text.text(0.7, 3.3, str(idx + 1), fontsize=18, fontweight="bold",
                 color=C_ACCENT if idx < 3 else C_PRIMARY, va="center", zorder=3)
    ax_text.text(1.5, 3.3, m["title"], fontsize=13, fontweight="bold",
                 color=C_PRIMARY, va="center", fontfamily="sans-serif")
    ax_text.text(1.5, 2.65, m["subtitle"], fontsize=9.5,
                 color=C_ACCENT, va="center", fontstyle="italic",
                 fontfamily="sans-serif")
    ax_text.text(1.5, 1.85, m["formula"], fontsize=10,
                 color=C_TEXT, va="center", fontfamily="monospace",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor=C_BG_GRID,
                           edgecolor=C_BORDER, linewidth=0.8))
    ax_text.text(1.5, 0.75, m["desc"], fontsize=8.5,
                 color=C_FORMULA, va="center", fontfamily="sans-serif",
                 linespacing=1.5)

    ax_diagram = fig2.add_axes([0.50, TOP_START - row * ROW_H, 0.47, 0.155],
                               facecolor=C_BG_CARD)
    for spine in ax_diagram.spines.values():
        spine.set_edgecolor(C_BORDER)
        spine.set_linewidth(1.2)
    m["draw"](ax_diagram)

fig2.savefig(OUTPUT_PDF, bbox_inches="tight", facecolor=C_WHITE)
plt.close(fig2)
print(f"PDF gespeichert:   {OUTPUT_PDF}")
