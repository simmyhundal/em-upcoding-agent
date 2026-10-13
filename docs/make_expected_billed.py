"""Expected level vs. billed level (99211-99215) for four provider groups, on v2 data.

Expected level = what a reviewer would assign from the chart: the level the MDM supports (two of the three elements) or the
level the recorded minutes support, whichever is higher (src/records.py). The grid uses EVERY visit's chart in the records
universe, as if every chart were reviewed; in practice a plan sees only the charts a records request returns. No coder noise is
applied here. Groups come from the answer key (eval only, gitignored): upcoders whose notes tell the truth, upcoders who
clone their notes to match the billed level, normal doctors, and high-acuity panels.

Each column is an expected level; the cells show where those visits were billed, so a column adds to 100%. Diagonal = billed as
documented; below it in the picture = billed above the expected level (upcoded); above it = billed below.

Usage:
    python docs/make_expected_billed.py [V2_DIR] [ANSWER_KEY] [OUT_SVG]
"""
import csv
import json
import os
import sys
from xml.sax.saxutils import escape

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import records  # noqa: E402

DATA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "data", "synthetic_v2_261012_1_code")
KEY = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "eval", "answer_key", "ground_truth_v2_261012_1_code.json")
OUT = sys.argv[3] if len(sys.argv) > 3 else os.path.join(ROOT, "docs", "images", "expected_billed.svg")
CODES = records.CODES
GROUPS = [("upcoder_honest_notes", "Upcoders, honest notes"), ("upcoder_cloned_notes", "Upcoders, cloned notes"),
          ("normal", "Normal doctors"), ("hard_negative", "High-acuity panels")]
FONT = 'font-family="Helvetica, Arial, sans-serif"'


def group_of(v):
    if v["role"] == "upcoder":
        return "upcoder_cloned_notes" if v["clones_notes"] else "upcoder_honest_notes"
    return v["role"]


def grids():
    prov = json.load(open(KEY))["providers"]
    view = os.path.join(DATA, "view")
    claims = {r["claim_id"]: r for r in csv.DictReader(open(os.path.join(view, "claims.csv")))}
    g = {k: np.zeros((5, 5)) for k, _ in GROUPS}       # [billed, expected]
    sizes = {k: set() for k, _ in GROUPS}
    for u in csv.DictReader(open(os.path.join(DATA, "records", "records_universe.csv"))):
        c = claims.get(u["claim_id"])
        if not c:
            continue
        mdm = records.mdm_level(int(u["problems_level"]), int(u["data_level"]), int(u["risk_level"]))
        exp = records.supported_level(mdm, u["documented_minutes"])
        k = group_of(prov[c["provider_id"]])
        g[k][CODES.index(c["cpt"]), exp] += 1
        sizes[k].add(c["provider_id"])
    return g, {k: len(v) for k, v in sizes.items()}


def shade(billed, exp, frac):
    if frac < 0.005:
        return "#ffffff"
    a = 0.12 + 0.88 * min(frac, 1.0)
    base = (21, 128, 61) if billed == exp else ((185, 28, 28) if billed > exp else (37, 99, 235))
    return "#%02x%02x%02x" % tuple(int(255 - (255 - c) * a) for c in base)


def main():
    g, nprov = grids()
    W, H = 1000, 385
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<text x="30" y="34" font-size="18" font-weight="bold" fill="#1f2937">Level the chart supports vs. level billed</text>',
         '<text x="30" y="54" font-size="12" fill="#6b7280">Share of visits in each column, by billed level. Shown as if every chart were reviewed '
         '(a plan sees only what a records request returns). Synthetic v2 data.</text>']
    cell = 36
    pw = 5 * cell
    for gi, (role, title) in enumerate(GROUPS):
        x0, y0 = 62 + gi * 238, 112
        m = g[role]
        col = m.sum(axis=0)
        s.append(f'<text x="{x0}" y="{y0 - 20}" font-size="13" font-weight="bold" fill="#1f2937">{escape(title)}</text>')
        s.append(f'<text x="{x0}" y="{y0 - 5}" font-size="11" fill="#6b7280">{nprov[role]} doctors, {int(m.sum()):,} visits</text>')
        for b in range(5):
            yy = y0 + (4 - b) * cell
            s.append(f'<text x="{x0 - 5}" y="{yy + 22}" text-anchor="end" font-size="10" fill="#6b7280">{CODES[b]}</text>')
            for e in range(5):
                frac = m[b, e] / col[e] if col[e] else 0
                xx = x0 + e * cell
                s.append(f'<rect x="{xx}" y="{yy}" width="{cell}" height="{cell}" fill="{shade(b, e, frac)}" stroke="#e5e7eb"/>')
                if frac >= 0.005:
                    t = f"{frac:.0%}" if frac >= 0.01 else "&lt;1%"
                    ink = "#ffffff" if frac >= 0.6 else "#1f2937"
                    s.append(f'<text x="{xx + cell / 2}" y="{yy + 22}" text-anchor="middle" font-size="10.5" fill="{ink}">{t}</text>')
        for e in range(5):
            s.append(f'<text x="{x0 + e * cell + cell / 2}" y="{y0 + 5 * cell + 14}" text-anchor="middle" font-size="10" fill="#6b7280">{CODES[e]}</text>')
        s.append(f'<text x="{x0 + pw / 2}" y="{y0 + 5 * cell + 32}" text-anchor="middle" font-size="11.5" fill="#1f2937">Level the chart supports</text>')
        if gi == 0:
            s.append(f'<text x="{x0 - 46}" y="{y0 + pw / 2}" text-anchor="middle" font-size="11.5" fill="#1f2937" '
                     f'transform="rotate(-90 {x0 - 46} {y0 + pw / 2})">Level billed</text>')
    lx = 62
    for lab, c in (("Billed as the chart supports", "#15803d"), ("Billed above what the chart supports (upcoded)", "#b91c1c"),
                   ("Billed below what the chart supports", "#2563eb")):
        s.append(f'<rect x="{lx}" y="345" width="14" height="14" fill="{c}"/><text x="{lx + 20}" y="357" font-size="12" fill="#1f2937">{lab}</text>')
        lx += 300
    s.append("</svg>")
    open(OUT, "w").write("\n".join(s))
    for role, title in GROUPS:
        m = g[role]
        n = m.sum()
        up = sum(m[b, e] for b in range(5) for e in range(5) if b > e)
        dn = sum(m[b, e] for b in range(5) for e in range(5) if b < e)
        print(f"{title:26s} doctors={nprov[role]:3d} visits={int(n):6d} above {up / n:.1%} below {dn / n:.1%} same {1 - (up + dn) / n:.1%}")


if __name__ == "__main__":
    main()
