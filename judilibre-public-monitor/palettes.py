# computed from https://github.com/spyrales/gouvdown/blob/master/R/colors.R
from string import ascii_letters


COLOR_LEVELS = {
    "0": [
        "#837C61",
        "#849A5A",
        "#158B57",
        "#405E5A",
        "#0B997D",
        "#55659D",
        "#424669",
        "#D6857B",
        "#B07F73",
        "#DDAE94",
        "#E3CE00",
        "#E2B835",
        "#DD8B4D",
        "#BF8066",
        "#D66C58",
        "#6B4952",
        "#866159",
        "#000000",
    ],
    "1": [
        "#958B62",
        "#91AE4F",
        "#169B62",
        "#466964",
        "#00AC8C",
        "#5770BE",
        "#484D7A",
        "#FF8D7E",
        "#D08A77",
        "#FFC29E",
        "#FFE800",
        "#FDCF41",
        "#FF9940",
        "#E18B63",
        "#FF6F4C",
        "#7D4E5B",
        "#A26859",
        "#000000",
    ],
    "2": [
        "#CEC39C",
        "#BEDB82",
        "#6DD69D",
        "#94B4AF",
        "#65DFBE",
        "#A0B4FF",
        "#9CA0CC",
        "#FFC9C3",
        "#FFBCAC",
        "#FFE1D2",
        "#FFF3B6",
        "#FFE7B7",
        "#FFCDB5",
        "#FFC1AA",
        "#FFBCB3",
        "#CD9DA9",
        "#E7AA9C",
        "#777777",
    ],
    "3": [
        "#ECE1BA",
        "#D4F39A",
        "#8EF5BB",
        "#BCDCD7",
        "#85F9D8",
        "#D1D9FF",
        "#C9CDFA",
        "#FFE4E2",
        "#FFDED8",
        "#FFF0E9",
        "#FFF9DD",
        "#FFF3DD",
        "#FFE6DC",
        "#FFE0D7",
        "#FFDEDA",
        "#F8C7D3",
        "#FFD1C7",
        "#B9B9B9",
    ],
    "4": [
        "#FEF3CC",
        "#E5FFB4",
        "#C8FFDE",
        "#D5F5F0",
        "#CCFFEE",
        "#EDF0FF",
        "#E9EBFF",
        "#FEF4F4",
        "#FFF2F0",
        "#FEF9F7",
        "#FFFDF2",
        "#FFFAF2",
        "#FFF5F1",
        "#FFF3F0",
        "#FFF2F1",
        "#FFE8ED",
        "#FFEDE9",
        "#E2E2E2",
    ],
}

COLORS = {}

for level in COLOR_LEVELS:
    for letter, c in zip(ascii_letters, COLOR_LEVELS[level]):
        COLORS[f"{letter}{level}"] = c


COLORS["bleu_france"] = "#000091"
COLORS["blanc"] = "#FFFFFF"
COLORS["rouge_marianne"] = "#E1000F"

COLORS["cc"] = "#FF8D7E"
COLORS["ca"] = "#484D7A"
COLORS["tj"] = "#FFE800"

PALETTES = {
    "pal_gouv_fr": [COLORS[i] for i in ("bleu_france", "blanc", "rouge_marianne")],
    "pal_gouv_a": [COLORS[i] for i in ("a0", "a1", "a2", "a3", "a4")],
    "pal_gouv_b": [COLORS[i] for i in ("b0", "b1", "b2", "b3", "b4")],
    "pal_gouv_c": [COLORS[i] for i in ("c0", "c1", "c2", "c3", "c4")],
    "pal_gouv_d": [COLORS[i] for i in ("d0", "d1", "d2", "d3", "d4")],
    "pal_gouv_e": [COLORS[i] for i in ("e0", "e1", "e2", "e3", "e4")],
    "pal_gouv_f": [COLORS[i] for i in ("f0", "f1", "f2", "f3", "f4")],
    "pal_gouv_g": [COLORS[i] for i in ("g0", "g1", "g2", "g3", "g4")],
    "pal_gouv_h": [COLORS[i] for i in ("h0", "h1", "h2", "h3", "h4")],
    "pal_gouv_i": [COLORS[i] for i in ("i0", "i1", "i2", "i3", "a4")],
    "pal_gouv_j": [COLORS[i] for i in ("j0", "j1", "j2", "j3", "j4")],
    "pal_gouv_k": [COLORS[i] for i in ("k0", "k1", "k2", "k3", "k4")],
    "pal_gouv_l": [COLORS[i] for i in ("l0", "l1", "l2", "l3", "l4")],
    "pal_gouv_m": [COLORS[i] for i in ("m0", "m1", "m2", "m3", "m4")],
    "pal_gouv_n": [COLORS[i] for i in ("n0", "n1", "n2", "n3", "n4")],
    "pal_gouv_o": [COLORS[i] for i in ("o0", "o1", "o2", "o3", "o4")],
    "pal_gouv_p": [COLORS[i] for i in ("p0", "p1", "p2", "p3", "p4")],
    "pal_gouv_q": [COLORS[i] for i in ("q0", "q1", "q2", "q3", "a4")],
    "pal_gouv_r": [COLORS[i] for i in ("r1", "r2", "r3", "r4")],
    "pal_gouv_qual1": [
        COLORS[i] for i in (f"{letter}1" for letter in ascii_letters[1:18])
    ],
    "pal_gouv_qual2": [COLORS[i] for i in ("c1", "f1", "h1", "k1", "p1")],
    "pal_gouv_div1": [
        COLORS[i] for i in ("f0", "f1", "f2", "f3", "f4", "h4", "h3", "h2", "h1", "h0")
    ],
    "pal_gouv_div2": [
        COLORS[i] for i in ("p0", "p1", "p2", "p3", "p4", "c4", "c3", "c2", "c1", "c0")
    ],
}
