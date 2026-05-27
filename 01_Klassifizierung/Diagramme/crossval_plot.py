"""
Cross-Validation Diagram (v4)
=============================
5-Fold Cross-Validation mit finalem Training,
separatem Testdatensatz und visueller Trennung
von Daten (Kästen) und Modellen (Ellipsen).

Benötigt: pip install matplotlib
Ausgabe:   crossval_diagram.png (300 dpi)
           crossval_diagram.pdf
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(14, 12.5))
ax.set_xlim(-0.5, 14)
ax.set_ylim(-1.5, 13.5)
ax.axis("off")

# ── Farben ──────────────────────────────────────────
C_TRAIN  = "#7CC47C"
C_VAL    = "#FFD54F"
C_TEST   = "#64B5F6"
C_ALL    = "#E0E0E0"
C_MODEL  = "#CE93D8"
C_FINAL_MODEL = "#AB47BC"
C_BORDER = "#555555"
C_TEXT   = "#333333"
C_LABEL  = "#666666"

# ── Layout ──────────────────────────────────────────
FOLD_X0   = 3.5
TRAIN_W   = 6.0       # Breite des grünen "Training data"-Kastens
FOLD_GAP  = 0.10      # Lücke zwischen Folds
FOLD_W    = (TRAIN_W - 4 * FOLD_GAP) / 5   # = 1.12 → Folds füllen Training-Breite exakt
SPLIT_H   = 0.50
SPLIT_GAP = 0.22
LABEL_X   = 0.1

# Test-data x-Position (für oberen UND unteren Block identisch)
TEST_X    = FOLD_X0 + TRAIN_W + 0.35
TEST_W    = 1.8

folds = ["Fold 1", "Fold 2", "Fold 3", "Fold 4", "Fold 5"]


# ── Hilfsfunktionen ─────────────────────────────────
def data_box(x, y, w, h, color, label="", fontsize=9, bold=False,
             border=C_BORDER, text_color=C_TEXT):
    """Rechteckiger Kasten für DATEN."""
    rect = patches.FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0.02",
        linewidth=1.2, edgecolor=border, facecolor=color)
    ax.add_patch(rect)
    if label:
        ax.text(x + w / 2, y + h / 2, label,
                ha="center", va="center", fontsize=fontsize,
                fontweight="bold" if bold else "normal", color=text_color)


def model_ellipse(cx, cy, w, h, color, label="", fontsize=9,
                  bold=True, border=None, text_color=C_TEXT):
    """Ellipse für MODELLE."""
    ellipse = patches.Ellipse(
        (cx, cy), w, h,
        linewidth=1.5, edgecolor=border or color, facecolor=color,
        alpha=0.92)
    ax.add_patch(ellipse)
    if label:
        ax.text(cx, cy, label,
                ha="center", va="center", fontsize=fontsize,
                fontweight="bold" if bold else "normal", color=text_color)


def process_label(y, line1, line2=None, color=C_LABEL):
    if line2:
        ax.text(LABEL_X, y + 0.15, line1, ha="left", va="center",
                fontsize=8.5, fontweight="bold", color=color)
        ax.text(LABEL_X, y - 0.12, line2, ha="left", va="center",
                fontsize=7.5, color=color)
    else:
        ax.text(LABEL_X, y, line1, ha="left", va="center",
                fontsize=8.5, fontweight="bold", color=color)


def thin_arrow(x1, y1, x2, y2, color=C_TEXT, lw=1.3):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=lw))


def dashed_arrow(x1, y1, x2, y2, color=C_TEXT, lw=1.0):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=lw,
                                linestyle="--", alpha=0.5))


def dashed_line(x1, y1, x2, y2, color=C_TEXT):
    ax.plot([x1, x2], [y1, y2], color=color, lw=1.0,
            linestyle="--", alpha=0.35)


# ══════════════════════════════════════════════════════
#  ZEILE 1: "All Data"
# ══════════════════════════════════════════════════════
row1_y = 12.5
all_w = TRAIN_W + 0.35 + TEST_W
data_box(FOLD_X0, row1_y, all_w, 0.55, C_ALL,
         "All Data", fontsize=12, bold=True)
process_label(row1_y + 0.27, "Gesamtdatensatz")

# ══════════════════════════════════════════════════════
#  ZEILE 2: Train-Test-Split
# ══════════════════════════════════════════════════════
row2_y = 11.45
data_box(FOLD_X0, row2_y, TRAIN_W, 0.55, C_TRAIN,
         "Training data", fontsize=11, bold=True)
data_box(TEST_X, row2_y, TEST_W, 0.55, C_TEST,
         "Test data", fontsize=11, bold=True, text_color="white")
process_label(row2_y + 0.27, "Train-Test-Split")

# Pfeil All Data → Split
dashed_line(FOLD_X0 + all_w / 2, row1_y,
            FOLD_X0 + all_w / 2, row2_y + 0.55)

# ══════════════════════════════════════════════════════
#  ZEILE 3: Train-Val-Split – Fold-Header
# ══════════════════════════════════════════════════════
header_y = 10.35
for i, label in enumerate(folds):
    x = FOLD_X0 + i * (FOLD_W + FOLD_GAP)
    data_box(x, header_y, FOLD_W, 0.42, "#F5F5F5", label,
             fontsize=8, bold=True, border="#AAAAAA")
process_label(header_y + 0.21, "Train-Val-Split",
              "(k = 5 Folds)")

# 5 Pfeile von "Training data" zu den Folds
for i in range(5):
    fold_cx = FOLD_X0 + i * (FOLD_W + FOLD_GAP) + FOLD_W / 2
    thin_arrow(fold_cx, row2_y, fold_cx, header_y + 0.42 + 0.03,
               color="#999999", lw=1.0)

# ══════════════════════════════════════════════════════
#  5 Trainingszyklen
# ══════════════════════════════════════════════════════
cycle_y0 = 9.35

# Label über temporären Modellen
model_cx = FOLD_X0 + TRAIN_W + 1.2
ax.text(model_cx, cycle_y0 + SPLIT_H + 0.35,
        "temporäre Modelle", ha="center", va="center",
        fontsize=8.5, fontweight="bold", color="#7B1FA2",
        linespacing=1.3)

for si in range(5):
    y = cycle_y0 - si * (SPLIT_H + SPLIT_GAP)
    ycenter = y + SPLIT_H / 2

    process_label(ycenter, f"Trainingszyklus {si + 1}")

    for fi in range(5):
        x = FOLD_X0 + fi * (FOLD_W + FOLD_GAP)
        is_val = (fi == si)
        data_box(x, y, FOLD_W, SPLIT_H,
                 C_VAL if is_val else C_TRAIN,
                 folds[fi], fontsize=7, bold=is_val)

    # Pfeil → temporäres Modell (Ellipse)
    last_fold_right = FOLD_X0 + TRAIN_W
    thin_arrow(last_fold_right + 0.05, ycenter,
               model_cx - 0.65, ycenter, lw=1.0)

    model_ellipse(model_cx, ycenter, 1.25, 0.42, C_MODEL,
                  f"Modell {si+1}", fontsize=8.5, bold=False,
                  border="#9C27B0", text_color="#4A148C")

# ══════════════════════════════════════════════════════
#  Klammer rechts: "Parameter-Optimierung"
# ══════════════════════════════════════════════════════
brace_x = model_cx + 0.85
top_y = cycle_y0 + SPLIT_H
bot_y = cycle_y0 - 4 * (SPLIT_H + SPLIT_GAP)
mid_y = (top_y + bot_y) / 2

ax.plot([brace_x, brace_x], [top_y - 0.05, mid_y + 0.12], color=C_TEXT, lw=1.2)
ax.plot([brace_x, brace_x], [mid_y - 0.12, bot_y + 0.05], color=C_TEXT, lw=1.2)
ax.plot([brace_x, brace_x + 0.12], [mid_y + 0.12, mid_y], color=C_TEXT, lw=1.2)
ax.plot([brace_x, brace_x + 0.12], [mid_y - 0.12, mid_y], color=C_TEXT, lw=1.2)
ax.plot([brace_x - 0.08, brace_x], [top_y - 0.05, top_y - 0.05], color=C_TEXT, lw=1.2)
ax.plot([brace_x - 0.08, brace_x], [bot_y + 0.05, bot_y + 0.05], color=C_TEXT, lw=1.2)

ax.text(brace_x + 0.3, mid_y, "Parameter-\nOptimierung",
        ha="left", va="center", fontsize=9.5, fontweight="bold",
        color=C_TEXT, linespacing=1.4)

# ══════════════════════════════════════════════════════
#  FINALES TRAINING
# ══════════════════════════════════════════════════════
final_train_y = bot_y - 1.4

process_label(final_train_y + 0.27, "Finales Training",
              "(alle Trainingsdaten)")

# Gestrichelte Linie "beste Parameter"
dashed_line(FOLD_X0 + TRAIN_W / 2, bot_y,
            FOLD_X0 + TRAIN_W / 2, final_train_y + 0.55)
ax.text(FOLD_X0 + TRAIN_W / 2 + 0.15,
        (bot_y + final_train_y + 0.55) / 2,
        "beste Parameter", ha="left", va="center",
        fontsize=7.5, fontstyle="italic", color=C_LABEL)

# Grüner Kasten: alle Trainingsdaten
data_box(FOLD_X0, final_train_y, TRAIN_W, 0.55, C_TRAIN,
         "Training auf allen 5 Folds (komplette Trainingsdaten)",
         fontsize=9, bold=True)

# Pfeil → Finales Modell (Ellipse)
thin_arrow(FOLD_X0 + TRAIN_W + 0.05, final_train_y + 0.27,
           model_cx - 0.75, final_train_y + 0.27)

model_ellipse(model_cx, final_train_y + 0.27, 1.5, 0.50,
              C_FINAL_MODEL, "Finales\nModell", fontsize=9.5,
              bold=True, border="#6A1B9A", text_color="white")

# ══════════════════════════════════════════════════════
#  FINALE EVALUATION
# ══════════════════════════════════════════════════════
eval_test_y = final_train_y - 1.4
eval_test_x = TEST_X   # x-bündig mit oberem Test-Kasten

process_label(eval_test_y + 0.27, "Finale Evaluation")

# Test-Daten (himmelblau) – direkt unter dem Finalen Modell
data_box(eval_test_x, eval_test_y, TEST_W, 0.55, C_TEST,
         "Test data", fontsize=10, bold=True, text_color="white")

# Pfeil vom Finalen Modell → Test data mit Label "evaluiert auf"
test_box_cx = eval_test_x + TEST_W / 2
thin_arrow(model_cx, final_train_y + 0.27 - 0.27,
           test_box_cx, eval_test_y + 0.55 + 0.03)

# Label "evaluiert auf" neben dem Pfeil
arrow_mid_y = (final_train_y + eval_test_y + 0.55) / 2
ax.text(model_cx + 0.15, arrow_mid_y,
        "evaluiert auf", ha="left", va="center",
        fontsize=8, fontstyle="italic", color=C_LABEL)

# Pfeil nach unten: Deployment
deploy_y = eval_test_y - 0.9
thin_arrow(test_box_cx, eval_test_y,
           test_box_cx, deploy_y + 0.15)
ax.text(test_box_cx, deploy_y,
        "Deployment", ha="center", va="center",
        fontsize=10, fontweight="bold", color=C_TEXT)

# Gestrichelter vertikaler Pfeil: oberer Test-Kasten → unterer Test-Kasten
test_upper_bottom = row2_y
test_lower_top = eval_test_y + 0.55
test_cx = TEST_X + TEST_W / 2
dashed_arrow(test_cx, test_upper_bottom,
             test_cx, test_lower_top + 0.03,
             color=C_TEST, lw=1.2)



# ══════════════════════════════════════════════════════
#  Legende
# ══════════════════════════════════════════════════════
leg_y = deploy_y - 1.0

# Daten-Legende (Kästen)
ax.text(1.0, leg_y + 0.5, "Daten:", fontsize=8, fontweight="bold",
        va="center", color=C_TEXT)
leg_data = [
    (C_TRAIN, "Training"),
    (C_VAL,   "Validation"),
    (C_TEST,  "Test (zurückgehalten)"),
]
cx = 2.0
for color, label in leg_data:
    data_box(cx, leg_y + 0.38, 0.3, 0.22, color, "", border="#999999")
    ax.text(cx + 0.4, leg_y + 0.49, label, fontsize=7.5, va="center", color=C_TEXT)
    cx += len(label) * 0.085 + 0.85

# Modell-Legende (Ellipsen)
ax.text(1.0, leg_y, "Modelle:", fontsize=8, fontweight="bold",
        va="center", color=C_TEXT)
leg_models = [
    (C_MODEL, "Temporäres Modell", "#4A148C"),
    (C_FINAL_MODEL, "Finales Modell", "white"),
]
cx = 2.2
for color, label, tc in leg_models:
    model_ellipse(cx + 0.15, leg_y, 0.35, 0.22, color, "",
                  border="#9C27B0" if color == C_MODEL else "#6A1B9A")
    ax.text(cx + 0.42, leg_y, label, fontsize=7.5, va="center", color=C_TEXT)
    cx += len(label) * 0.085 + 0.85

# ══════════════════════════════════════════════════════
#  Untertitel & Signatur
# ══════════════════════════════════════════════════════
ax.text(7.0, leg_y - 0.7,
        "5-Fold Cross-Validation mit finalem Training und separatem Testdatensatz",
        ha="center", va="center", fontsize=11,
        fontstyle="italic", color="#666666")
ax.text(7.0, leg_y - 1.1,
        "Jörg / Edu4AI – CC BY-SA 4.0",
        ha="center", va="center", fontsize=7, color="#AAAAAA")

# ── Speichern ───────────────────────────────────────
plt.tight_layout()
plt.savefig("crossval_diagram.png", dpi=300, bbox_inches="tight",
            facecolor="white", edgecolor="none")
plt.savefig("crossval_diagram.pdf", bbox_inches="tight",
            facecolor="white", edgecolor="none")
print("✓ crossval_diagram.png (300 dpi)")
print("✓ crossval_diagram.pdf")
plt.show()