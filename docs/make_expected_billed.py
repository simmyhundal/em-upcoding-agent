"""Expected level vs. billed level (99211-99215) for the three provider groups.

Expected level = the level the documentation supports: the higher of the level supported by the documented MDM level and the
level supported by the documented minutes (the real rule is "MDM or time, whichever supports the higher level"). It exists
only for the claims in the records-review sample (about 30%). Billed level comes from claims.csv. Groups come from the
answer key (eval only, gitignored).

Each column is a documented level; the cells show where those visits were billed, so a column adds to 100%. Diagonal = billed
as documented; below it = billed above documented level (upcoded); above it = billed below (downcoded).

In this synthetic data the documented level is generated from the same hidden truth that defines an upcoded visit, with 15%
off-by-one noise, and minutes are drawn from the documented level's band, so time never disagrees with MDM. The grid
illustrates the data model; it does not validate the method.

Usage:
    python docs/make_expected_billed.py [DATA_DIR] [ANSWER_KEY] [OUT_SVG]
"""
import csv
import json
import os
import sys
from collections import defaultdict
from xml.sax.saxutils import escape

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "data", "synthetic")
KEY = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "eval", "answer_key", "ground_truth.json")
OUT = sys.argv[3] if len(sys.argv) > 3 else os.path.join(ROOT, "docs", "images", "expected_billed.svg")
CODES = ["99211", "99212", "99213", "99214", "99215"]
MDM = ["minimal", "straightforward", "low", "moderate", "high"]
MIN_BANDS = [(0, 9), (10, 19), (20, 29), (30, 39), (40, 10 ** 6)]   # minutes supporting each level (illustrative)
GROUPS = [("upcoder", "Upcoders (8)"), ("normal", "Normal doctors (200)"), ("hard_negative", "High-acuity panels (8)")]
FONT = 'font-family="Helvetica, Arial, sans-serif"'


def level_by_minutes(m):
    return max(i for i, (lo, _) in enumerate(MIN_BANDS) if m >= lo)


def grids():
    roles = {p: v["role"] for p, v in json.load(open(KEY))["providers"].items()}
    billed = {}
    prov_of = {}
    for r in csv.DictReader(open(os.path.join(DATA, "claims.csv"))):
        billed[r["claim_id"]] = CODES.index(r["cpt"])
        prov_of[r["claim_id"]] = r["provider_id"]
    g = {k: np.zeros((5, 5)) for k, _ in GROUPS}       # [billed, expected]
    for r in csv.DictReader(open(os.path.join(DATA, "documentation.csv"))):
        exp = max(MDM.index(r["documented_mdm_level"]), level_by_minutes(int(r["documented_minutes"])))
        g[roles[prov_of[r["claim_id"]]]][billed[r["claim_id"]], exp] += 1
    return g


def shade(billed, exp, frac):
    if frac < 0.005:
        return "#ffffff"
    a = 0.12 + 0.88 * min(frac, 1.0)
    base = (21, 128, 61) if billed == exp else ((185, 28, 28) if billed > exp else (37, 99, 235))
    return "#%02x%02x%02x" % tuple(int(255 - (255 - c) * a) for c in base)


def main():
    g = grids()
    W, H = 1000, 460
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<text x="30" y="34" font-size="18" font-weight="bold" fill="#1f2937">Level the records support vs. level billed</text>',
         '<text x="30" y="54" font-size="12" fill="#6b7280">Share of documented visits in each column, by billed level. Records-review sample only '
         '(about 30% of visits). Synthetic data, seed 42.</text>']
    cell, pw = 46, 5 * 46
    for gi, (role, title) in enumerate(GROUPS):
        x0, y0 = 70 + gi * 315, 112
        m = g[role]
        n = int(m.sum())
        s.append(f'<text x="{x0}" y="{y0 - 20}" font-size="14" font-weight="bold" fill="#1f2937">{escape(title)}</text>')
        s.append(f'<text x="{x0}" y="{y0 - 1}" font-size="11" fill="#6b7280">{n:,} documented visits</text>')
        col = m.sum(axis=0)
        for b in range(5):
            yy = y0 + (4 - b) * cell
            s.append(f'<text x="{x0 - 6}" y="{yy + 28}" text-anchor="end" font-size="11" fill="#6b7280">{CODES[b]}</text>')
            for e in range(5):
                frac = m[b, e] / col[e] if col[e] else 0
                xx = x0 + e * cell
                s.append(f'<rect x="{xx}" y="{yy}" width="{cell}" height="{cell}" fill="{shade(b, e, frac)}" stroke="#e5e7eb"/>')
                if frac >= 0.005:
                    t = f"{frac:.0%}" if frac >= 0.01 else "&lt;1%"
                    ink = "#ffffff" if frac >= 0.6 else "#1f2937"
                    s.append(f'<text x="{xx + cell / 2}" y="{yy + 28}" text-anchor="middle" font-size="11.5" fill="{ink}">{t}</text>')
        for e in range(5):
            s.append(f'<text x="{x0 + e * cell + cell / 2}" y="{y0 + 5 * cell + 16}" text-anchor="middle" font-size="11" fill="#6b7280">{CODES[e]}</text>')
        s.append(f'<text x="{x0 + pw / 2}" y="{y0 + 5 * cell + 36}" text-anchor="middle" font-size="12" fill="#1f2937">Level the records support</text>')
        s.append(f'<text x="{x0 - 52}" y="{y0 + pw / 2}" text-anchor="middle" font-size="12" fill="#1f2937" '
                 f'transform="rotate(-90 {x0 - 52} {y0 + pw / 2})">Level billed</text>')
    lx = 70
    for lab, c in (("Billed as documented", "#15803d"), ("Billed above documented level (upcoded)", "#b91c1c"),
                   ("Billed below documented level", "#2563eb")):
        s.append(f'<rect x="{lx}" y="428" width="14" height="14" fill="{c}"/><text x="{lx + 20}" y="440" font-size="12" fill="#1f2937">{lab}</text>')
        lx += 290
    s.append("</svg>")
    open(OUT, "w").write("\n".join(s))
    for role, title in GROUPS:
        m = g[role]
        n = m.sum()
        up = np.tril(m, -1).sum() if False else sum(m[b, e] for b in range(5) for e in range(5) if b > e)
        dn = sum(m[b, e] for b in range(5) for e in range(5) if b < e)
        print(f"{title:26s} n={int(n):6d}  billed above documented {up / n:.1%}  below {dn / n:.1%}  same {1 - (up + dn) / n:.1%}")


if __name__ == "__main__":
    main()
