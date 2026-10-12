"""Billing level vs. patient complexity for the three provider groups, with 95% confidence intervals.

Complexity score = the patient's chronic-condition count (0 to 6 or more), the same number the risk-adjusted screen uses.
Groups come from the answer key (eval only, gitignored): upcoders, the 200 normal doctors, and the high-acuity panels
(honest doctors with sicker patients). For each group and complexity level we take every provider's share of visits billed
at the level, then average across providers and build a t-interval over providers. Providers, not visits, are the unit,
because visits from one doctor are not independent; intervals from 8 providers are wide on purpose.

Usage:
    python docs/make_complexity_chart.py [DATA_DIR] [ANSWER_KEY] [OUT_SVG]
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
OUT = sys.argv[3] if len(sys.argv) > 3 else os.path.join(ROOT, "docs", "images", "complexity.svg")
MAX_C = 6          # complexity 6 or more share one bucket
MIN_VISITS = 10    # a provider needs this many visits at a complexity level to count there
MIN_PROVIDERS = 4  # a group needs this many providers at a level to be plotted (fewer gives meaningless intervals)
GROUPS = [("normal", "Normal doctors (200)", "#6b7280"), ("hard_negative", "High-acuity panels (honest, 8)", "#2563eb"),
          ("upcoder", "Upcoders (8)", "#b91c1c")]
T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
        11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131, 20: 2.086, 30: 2.042}
FONT = 'font-family="Helvetica, Arial, sans-serif"'


def tcrit(df):
    if df >= 60:
        return 1.96
    keys = [k for k in sorted(T975) if k <= df]
    return T975[keys[-1]] if df < 30 else 2.0


def load():
    roles = {p: v["role"] for p, v in json.load(open(KEY))["providers"].items()}
    chronic = {r["patient_id"]: min(int(r["chronic_condition_count"]), MAX_C)
               for r in csv.DictReader(open(os.path.join(DATA, "patients.csv")))}
    cnt = defaultdict(lambda: np.zeros(3))      # (provider, complexity) -> visits, n99215, n99214or15
    for r in csv.DictReader(open(os.path.join(DATA, "claims.csv"))):
        a = cnt[(r["provider_id"], chronic[r["patient_id"]])]
        a += (1, r["cpt"] == "99215", r["cpt"] in ("99214", "99215"))
    return roles, cnt


def intervals(roles, cnt, col):
    out = {}
    for role, _, _ in GROUPS:
        for c in range(MAX_C + 1):
            sh = [cnt[(p, c)][col] / cnt[(p, c)][0] for p, r in roles.items()
                  if r == role and (p, c) in cnt and cnt[(p, c)][0] >= MIN_VISITS]
            if len(sh) < MIN_PROVIDERS:
                continue
            m, se = np.mean(sh), np.std(sh, ddof=1) / np.sqrt(len(sh))
            h = tcrit(len(sh) - 1) * se
            out[(role, c)] = (m, max(0.0, m - h), min(1.0, m + h), len(sh))
    return out


def panel(s, x0, y0, w, h, title, res, ymax):
    s.append(f'<text x="{x0}" y="{y0 - 14}" font-size="14" font-weight="bold" fill="#1f2937">{escape(title)}</text>')
    px = lambda c, off: x0 + 40 + (c + 0.5) * (w - 50) / (MAX_C + 1) + off
    py = lambda v: y0 + h - v / ymax * h
    for k in range(5):
        v = ymax * k / 4
        s.append(f'<line x1="{x0 + 40}" x2="{x0 + w}" y1="{py(v):.1f}" y2="{py(v):.1f}" stroke="#e5e7eb"/>')
        s.append(f'<text x="{x0 + 34}" y="{py(v) + 4:.1f}" text-anchor="end" font-size="11" fill="#6b7280">{v:.0%}</text>')
    for c in range(MAX_C + 1):
        lab = f"{c}+" if c == MAX_C else str(c)
        s.append(f'<text x="{px(c, 0):.1f}" y="{y0 + h + 18}" text-anchor="middle" font-size="11" fill="#6b7280">{lab}</text>')
    s.append(f'<text x="{x0 + 40 + (w - 50) / 2}" y="{y0 + h + 38}" text-anchor="middle" font-size="12" fill="#1f2937">'
             f'Patient complexity (chronic conditions)</text>')
    for gi, (role, _, col) in enumerate(GROUPS):
        off = (gi - 1) * 9
        pts = [(c, res[(role, c)]) for c in range(MAX_C + 1) if (role, c) in res]
        s.append(f'<polyline fill="none" stroke="{col}" stroke-width="1.5" points="'
                 + " ".join(f"{px(c, off):.1f},{py(v[0]):.1f}" for c, v in pts) + '"/>')
        for c, (m, lo, hi, n) in pts:
            s.append(f'<line x1="{px(c, off):.1f}" x2="{px(c, off):.1f}" y1="{py(lo):.1f}" y2="{py(hi):.1f}" stroke="{col}" stroke-width="2"/>')
            s.append(f'<circle cx="{px(c, off):.1f}" cy="{py(m):.1f}" r="3.5" fill="{col}"/>')


def main():
    roles, cnt = load()
    r15, r1415 = intervals(roles, cnt, 1), intervals(roles, cnt, 2)
    W, H = 1000, 470
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         '<text x="30" y="34" font-size="18" font-weight="bold" fill="#1f2937">How often each group bills the top codes, by how sick the patient is</text>',
         '<text x="30" y="54" font-size="12" fill="#6b7280">Mean across doctors with a 95% confidence interval over doctors. '
         'Synthetic data (seed 42). Groups come from the answer key.</text>']
    panel(s, 30, 100, 450, 280, "Share of visits billed 99215", r15, max(v[2] for v in r15.values()) * 1.05)
    panel(s, 520, 100, 450, 280, "Share of visits billed 99214 or 99215", r1415, 1.0)
    lx = 30
    for _, lab, col in GROUPS:
        s.append(f'<circle cx="{lx + 6}" cy="438" r="5" fill="{col}"/><text x="{lx + 18}" y="442" font-size="12" fill="#1f2937">{escape(lab)}</text>')
        lx += 250
    s.append("</svg>")
    open(OUT, "w").write("\n".join(s))
    for name, res in (("99215", r15), ("99214+99215", r1415)):
        print(name)
        for role, lab, _ in GROUPS:
            print(f"  {lab:34s}", " ".join(f"{res[(role, c)][0]:.2f}[{res[(role, c)][1]:.2f},{res[(role, c)][2]:.2f}]n{res[(role, c)][3]}"
                                           if (role, c) in res else "   -   " for c in range(MAX_C + 1)))


if __name__ == "__main__":
    main()
