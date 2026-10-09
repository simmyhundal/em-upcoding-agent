"""Evidence chart: a provider's 99215 share by patient complexity, against all other providers.

One SVG per provider (no plotting dependency). For each complexity level (0, 1, 2, 3, 4, 5+ chronic conditions):
  * a box-and-whisker of the OTHER providers' 99215 shares at that level (a provider has one share per level,
    so the box can only describe peers);
  * the provider under review as a point with a 95% Wilson confidence interval;
  * the number of visits under each level. Levels with too few visits are drawn hollow and marked thin.
Uses only agent-visible files (claims.csv, patients.csv). Never touches ground truth.

Usage:
    python src/evidence_chart.py DATA_DIR FLAGGED_CSV OUT_DIR
"""
import csv
import math
import os
import sys
from collections import defaultdict
from xml.sax.saxutils import escape

import numpy as np

BUCKETS = ["0", "1", "2", "3", "4", "5+"]
MIN_PEER_VISITS = 10     # a peer needs this many visits at a level to contribute a share
MIN_SHOWN_VISITS = 10    # fewer visits than this: the provider's point is drawn hollow ("thin")
Z95 = 1.959964


def bucket(c):
    return "5+" if c >= 5 else str(c)


def wilson(k, n, z=Z95):
    """95% Wilson score interval for k successes in n trials."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def load_counts(data_dir):
    chronic = {}
    with open(os.path.join(data_dir, "patients.csv")) as f:
        for r in csv.DictReader(f):
            chronic[r["patient_id"]] = int(r["chronic_condition_count"])
    counts = defaultdict(lambda: {b: [0, 0] for b in BUCKETS})   # provider -> bucket -> [visits, n_99215]
    with open(os.path.join(data_dir, "claims.csv")) as f:
        for r in csv.DictReader(f):
            c = counts[r["provider_id"]][bucket(chronic[r["patient_id"]])]
            c[0] += 1
            c[1] += r["cpt"] == "99215"
    return counts


def box_stats(values):
    v = np.array(values, dtype=float)
    q1, med, q3 = np.percentile(v, [25, 50, 75])
    iqr = q3 - q1
    lo_fence, hi_fence = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    inside = v[(v >= lo_fence) & (v <= hi_fence)]
    return {"n": int(len(v)), "q1": float(q1), "median": float(med), "q3": float(q3),
            "whisker_lo": float(inside.min()), "whisker_hi": float(inside.max()),
            "outliers": sorted(float(x) for x in v[(v < lo_fence) | (v > hi_fence)])}


def chart_data(counts, pid):
    out = []
    for b in BUCKETS:
        visits, k = counts[pid][b]
        lo, hi = wilson(k, visits)
        peers = [c[b][1] / c[b][0] for p, c in counts.items() if p != pid and c[b][0] >= MIN_PEER_VISITS]
        out.append({"bucket": b, "visits": visits, "n_99215": k,
                    "share": (k / visits) if visits else None, "ci_low": lo, "ci_high": hi,
                    "thin": visits < MIN_SHOWN_VISITS, "peer": box_stats(peers) if peers else None})
    return out


def render_svg(pid, data):
    W, H = 760, 470
    ml, mr, mt, mb = 70, 24, 70, 92
    pw, ph = W - ml - mr, H - mt - mb
    ymax = 0.05
    for d in data:
        ymax = max(ymax, d["ci_high"] if d["visits"] else 0)
        if d["peer"]:
            ymax = max(ymax, d["peer"]["whisker_hi"], *(d["peer"]["outliers"] or [0]))
    ymax = min(1.0, math.ceil((ymax + 0.02) * 20) / 20)

    def y(v):
        return mt + ph * (1 - v / ymax)
    slot = pw / len(data)
    cx = [ml + slot * (i + 0.5) for i in range(len(data))]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Helvetica, Arial, sans-serif" font-size="12">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="{ml}" y="26" font-size="16" font-weight="bold" fill="#111">{escape(pid)}: 99215 share by patient complexity</text>',
         f'<text x="{ml}" y="46" fill="#555">Synthetic data. Boxes: other providers\' shares at each level. '
         f'Point and bar: this provider with 95% confidence interval.</text>']
    for i in range(0, int(round(ymax / 0.05)) + 1):
        v = i * 0.05
        s.append(f'<line x1="{ml}" y1="{y(v):.1f}" x2="{W - mr}" y2="{y(v):.1f}" stroke="#e6e6e6"/>')
        s.append(f'<text x="{ml - 8}" y="{y(v) + 4:.1f}" text-anchor="end" fill="#555">{v:.0%}</text>')
    s.append(f'<text transform="translate(18 {mt + ph / 2}) rotate(-90)" text-anchor="middle" fill="#333">Share of visits billed 99215</text>')
    for x, d in zip(cx, data):
        pr = d["peer"]
        if pr:
            bw = slot * 0.34
            s.append(f'<line x1="{x:.1f}" y1="{y(pr["whisker_lo"]):.1f}" x2="{x:.1f}" y2="{y(pr["whisker_hi"]):.1f}" stroke="#7a7a7a"/>')
            for w in (pr["whisker_lo"], pr["whisker_hi"]):
                s.append(f'<line x1="{x - bw / 3:.1f}" y1="{y(w):.1f}" x2="{x + bw / 3:.1f}" y2="{y(w):.1f}" stroke="#7a7a7a"/>')
            s.append(f'<rect x="{x - bw:.1f}" y="{y(pr["q3"]):.1f}" width="{2 * bw:.1f}" height="{max(1.0, y(pr["q1"]) - y(pr["q3"])):.1f}" '
                     f'fill="#d9dde3" stroke="#7a7a7a"/>')
            s.append(f'<line x1="{x - bw:.1f}" y1="{y(pr["median"]):.1f}" x2="{x + bw:.1f}" y2="{y(pr["median"]):.1f}" stroke="#333" stroke-width="2"/>')
            for o in pr["outliers"]:
                s.append(f'<circle cx="{x:.1f}" cy="{y(o):.1f}" r="2.2" fill="none" stroke="#7a7a7a"/>')
        if d["visits"]:
            px = x + slot * 0.0
            col = "#c2410c"
            s.append(f'<line x1="{px:.1f}" y1="{y(d["ci_low"]):.1f}" x2="{px:.1f}" y2="{y(d["ci_high"]):.1f}" stroke="{col}" stroke-width="2"'
                     + (' stroke-dasharray="3 3"' if d["thin"] else "") + "/>")
            for c in (d["ci_low"], d["ci_high"]):
                s.append(f'<line x1="{px - 6:.1f}" y1="{y(c):.1f}" x2="{px + 6:.1f}" y2="{y(c):.1f}" stroke="{col}" stroke-width="2"/>')
            fill = "#ffffff" if d["thin"] else col
            s.append(f'<circle cx="{px:.1f}" cy="{y(d["share"]):.1f}" r="5" fill="{fill}" stroke="{col}" stroke-width="2"/>')
        s.append(f'<text x="{x:.1f}" y="{mt + ph + 20}" text-anchor="middle" font-weight="bold" fill="#222">{d["bucket"]}</text>')
        s.append(f'<text x="{x:.1f}" y="{mt + ph + 36}" text-anchor="middle" fill="#555">{d["visits"]} visits</text>')
        s.append(f'<text x="{x:.1f}" y="{mt + ph + 50}" text-anchor="middle" fill="#555">{d["n_99215"]} billed 99215</text>')
        if d["thin"]:
            s.append(f'<text x="{x:.1f}" y="{mt + ph + 64}" text-anchor="middle" fill="#a16207">thin (under {MIN_SHOWN_VISITS})</text>')
    s.append(f'<text x="{ml + pw / 2}" y="{H - 12}" text-anchor="middle" fill="#333">Chronic conditions of the patient</text>')
    s.append("</svg>")
    return "\n".join(s)


def make_charts(data_dir, flagged_csv, out_dir):
    counts = load_counts(data_dir)
    with open(flagged_csv) as f:
        ids = [r["provider_id"] for r in csv.DictReader(f) if r["flagged"] == "True"]
    os.makedirs(out_dir, exist_ok=True)
    for pid in ids:
        with open(os.path.join(out_dir, f"{pid}.svg"), "w") as f:
            f.write(render_svg(pid, chart_data(counts, pid)))
    return ids


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    made = make_charts(*sys.argv[1:])
    print(f"{len(made)} charts -> {sys.argv[3]}")
