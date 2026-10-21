"""Draw the README figures (dependency-free SVG).

  docs/images/pipeline.svg   the pipeline in plain English
  docs/images/results.svg    honest providers still accused after review, from the checked summaries and the answer key
  docs/images/case_card.svg  one real case summary with its evidence chart
  docs/images/funnel.svg     the filtering steps with the live run's counts

The results figure needs the answer key (eval/answer_key/ground_truth.json), which is gitignored; regenerate it with
src/generate_synthetic.py first. Numbers come from the same functions the eval report uses.

Usage:
    python docs/make_figures.py
"""
import json
import os
import re
import sys
import textwrap
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "eval"))
sys.path.insert(0, os.path.join(ROOT, "src"))
import run_eval  # noqa: E402

FONT = 'font-family="Helvetica, Arial, sans-serif"'
INK, MUTED, LINE = "#1f2937", "#6b7280", "#d1d5db"
BLUE, ORANGE, GREEN, RED = "#2563eb", "#c2410c", "#15803d", "#b91c1c"


def write(name, svg):
    with open(os.path.join(ROOT, "docs", "images", name), "w") as f:
        f.write(svg)


PEOPLE = "#7c3aed"
LATEST = "v3.0"
VERSIONS = {
    "v1.0": ("Statistics screens upcoders then AI suggests and explains. Humans review generated cases.", [
        ("Billing data", "Claims data. Here: synthetic claims shaped like public Medicare numbers.", GREEN),
        ("Statistical screen", "Flags doctors who bill the top visit code unusually often for their patients. The most unusual go on.", BLUE),
        ("AI review", "Reads each flagged doctor's evidence and writes a short explanation citing the exact visits.", ORANGE),
        ("AI filter", "In the same call, suggests: looks like upcoding, sicker patients, or unclear. Only 'upcoding' moves on.", ORANGE),
        ("Citation check", "Code rejects any summary that cites a visit that does not exist or belongs to someone else.", GREEN),
        ("Case pages", "One page per flagged doctor: the summary, its cited visits and a chart against peers.", GREEN),
        ("Recovery packets", "For suspected upcoders only: records to request, a sample plan, an overpayment estimate.", GREEN),
        ("People review", "SIU reviewers read the cases. Payment integrity requests records and decides what happens next.", PEOPLE)]),
    "v2.0": ("Statistics screen, code asks for charts and settles the clear cases, AI handles the rest. Humans review.", [
        ("Claims data", "Plan-shaped synthetic data: members, claim lines, denials. Conditions are derived from the claims.", GREEN),
        ("Statistical screen", "Flags doctors who bill the top code more than their patients explain: suspicion 5 or higher.", BLUE),
        ("Records request", "Asks each flagged doctor's office for charts. Some come late, incomplete or not at all.", GREEN),
        ("Chart rules", "Code checks whether the charts support the level billed and decides the clear-cut cases.", GREEN),
        ("AI interpretation", "Where the rules are silent, a model reads a compact evidence card and gives an advisory leaning.", ORANGE),
        ("Checks", "A citation check and a number check reject anything unsupported by the evidence.", GREEN),
        ("Case pages and packets", "Draft case pages and recovery packets for the doctors called upcoding.", GREEN),
        ("People review", "SIU reviewers read the drafts and decide. Nothing is sent automatically.", PEOPLE)]),
    "v3.0": ("An agent chooses the next step. Code limits and checks it. Humans review the findings.", [
        ("Claims data", "Plan-shaped synthetic data: members, claim lines, denials. Conditions are derived from the claims.", GREEN),
        ("Screen tool", "A statistical screen the agent can run with any cutoff, as often as it likes.", BLUE),
        ("Agent decides", "A model picks the next step within caps: look closer, compare peers, ask for charts, follow up, stop.", ORANGE),
        ("Provider office", "Simulated practices answer: complete, partial, late, unusable or not at all.", GREEN),
        ("Evidence checks", "Chart rule, claim facts and summary rules, available to the agent as tools.", GREEN),
        ("AI findings", "The agent submits a leaning for each doctor it examined, with a short interpretation.", ORANGE),
        ("Checks", "A citation check and a number check run on the findings; every tool call is logged.", GREEN),
        ("People review", "Findings are drafts. People decide; nothing is sent automatically.", PEOPLE)]),
}


def how_it_works(version):
    """Eight steps, colored by who does the work: statistics, AI, plain code and checks, people. One figure per version."""
    title, raw = VERSIONS[version]
    steps = [(str(i + 1), t, body, col) for i, (t, body, col) in enumerate(raw)]
    W, H = 1000, 470
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="30" y="40" font-size="19" font-weight="bold" fill="{INK}">{escape(title)}</text>',
         f'<text x="{W - 30}" y="{H - 18}" text-anchor="end" font-size="12.5" fill="{MUTED}">{version}</text>']
    bw, bh, gap, x0 = 225, 150, 20, 30
    rows_y = (74, 268)
    pos = [(x0 + (i % 4) * (bw + gap), rows_y[i // 4]) for i in range(8)]
    s.append(f'<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
             f'<path d="M0 0 L10 5 L0 10 z" fill="{MUTED}"/></marker></defs>')
    for (n, t, body, col), (x, y) in zip(steps, pos):
        s.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="10" fill="#f9fafb" stroke="{col}" stroke-width="2.5"/>')
        s.append(f'<circle cx="{x + 24}" cy="{y + 26}" r="14" fill="{col}"/>')
        s.append(f'<text x="{x + 24}" y="{y + 31}" text-anchor="middle" font-size="14" font-weight="bold" fill="#fff">{n}</text>')
        s.append(f'<text x="{x + 46}" y="{y + 31}" font-size="14.5" font-weight="bold" fill="{INK}">{escape(t)}</text>')
        for j, line in enumerate(textwrap.wrap(body, 30)[:6]):
            s.append(f'<text x="{x + 16}" y="{y + 62 + j * 18}" font-size="12.5" fill="{MUTED}">{escape(line)}</text>')
    for r in (0, 1):
        for i in range(3):
            x = pos[r * 4 + i][0] + bw
            y = rows_y[r] + bh / 2
            s.append(f'<path d="M{x + 2} {y} L{x + gap - 4} {y}" stroke="{MUTED}" stroke-width="2" marker-end="url(#a)"/>')
    cx4 = pos[3][0] + bw / 2
    cx5 = pos[4][0] + bw / 2
    ymid = (rows_y[0] + bh + rows_y[1]) / 2
    s.append(f'<path d="M{cx4} {rows_y[0] + bh} L{cx4} {ymid} L{cx5} {ymid} L{cx5} {rows_y[1] - 2}" fill="none" stroke="{MUTED}" '
             f'stroke-width="2" marker-end="url(#a)"/>')
    ly = H - 30
    for k, (col, label) in enumerate(((BLUE, "statistics"), (ORANGE, "AI"), (GREEN, "plain code and checks"), (PEOPLE, "people"))):
        lx = 30 + [0, 110, 170, 350][k]
        s.append(f'<rect x="{lx}" y="{ly - 11}" width="14" height="14" rx="3" fill="none" stroke="{col}" stroke-width="2.5"/>')
        s.append(f'<text x="{lx + 20}" y="{ly + 1}" font-size="12.5" fill="{MUTED}">{label}</text>')
    s.append("</svg>")
    svg = "\n".join(s)
    write(f"how_it_works_{version}.svg", svg)


AGENT_ACTIONS = [
    ("Screen", "Rank providers by risk-adjusted score, priority, eb_ratio_t or eb_upper_t (share billed 99214 or 99215 vs expected), any cutoff.", BLUE),
    ("Look closer", "Evidence card and peer comparison for one provider: billing mix, complexity, sample claims.", GREEN),
    ("Request charts", "Ask a provider for a random sample first, then a targeted one if needed.", GREEN),
    ("Follow up", "Fix deficiencies (unsigned, missing results), or ask for the EHR audit trail.", GREEN),
    ("Check notes", "Notes against claims: problems addressed, orders and results, signatures, copy-forward.", GREEN),
    ("Estimate", "Extrapolate an overpayment from a random sample, flagged when the sample is too thin.", GREEN),
    ("Review", "Chart rule and summary rules first, a model only where they are silent.", GREEN),
    ("Submit findings", "A finding or a stated reason for every candidate; unsupported claims are refused.", GREEN)]


def agent_actions():
    """The agent and the actions it chooses from (the README's main figure)."""
    W, H = 1000, 606
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>', f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{MUTED}"/></marker>'
         f'<marker id="b" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{ORANGE}"/></marker></defs>']
    bw, bh = 290, 96
    pos = [(30, 30), (355, 30), (680, 30), (30, 200), (680, 200), (30, 370), (355, 370), (680, 370)]
    cx, cy, cw, ch = 355, 190, 290, 116
    centers = []
    for (n, body, col), (x, y) in zip(AGENT_ACTIONS, pos):
        s.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="10" fill="#f9fafb" stroke="{col}" stroke-width="2.5"/>')
        s.append(f'<text x="{x + 16}" y="{y + 28}" font-size="14.5" font-weight="bold" fill="{INK}">{escape(n)}</text>')
        for j, line in enumerate(textwrap.wrap(body, 40)[:3]):
            s.append(f'<text x="{x + 16}" y="{y + 52 + j * 17}" font-size="12.5" fill="{MUTED}">{escape(line)}</text>')
        centers.append((x + bw / 2, y + bh / 2, x, y))
    s.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="14" fill="#fff7ed" stroke="{ORANGE}" stroke-width="3"/>')
    s.append(f'<text x="{cx + cw / 2}" y="{cy + 38}" text-anchor="middle" font-size="19" font-weight="bold" fill="{INK}">The agent</text>')
    for j, line in enumerate(["A model picks the next action", "within caps: tool calls, dollars, charts requested"]):
        s.append(f'<text x="{cx + cw / 2}" y="{cy + 64 + j * 18}" text-anchor="middle" font-size="12.5" fill="{MUTED}">{line}</text>')
    s.append(f'<text x="{cx + cw / 2}" y="{cy + 106}" text-anchor="middle" font-size="12" fill="{MUTED}">never sees the answer key</text>')
    for (mx, my, x, y) in centers:                       # a line from the agent to each action, ending at the nearest box edge
        tx = cx + cw / 2
        ty = cy + ch / 2
        if abs(mx - tx) < 5:
            x1, y1, x2, y2 = tx, (cy if my < ty else cy + ch), mx, (y + bh if my < ty else y)
        else:
            x1, y1, x2, y2 = (cx if mx < tx else cx + cw), ty, (x + bw if mx < tx else x), my
        s.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#a)" fill="none"/>')
    chips = [("Simulated providers answer", "complete, partial, late or silent", GREEN, 30), ("Checks before anything is accepted", "citations, numbers, contradictions, leaning", GREEN, 355),
             ("PI teams review the drafts", "nothing is sent or decided automatically", PEOPLE, 680)]
    for t, sub, col, x in chips:
        s.append(f'<rect x="{x}" y="490" width="{bw}" height="56" rx="10" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="6 4"/>')
        s.append(f'<text x="{x + 16}" y="513" font-size="13" font-weight="bold" fill="{INK}">{escape(t)}</text>')
        s.append(f'<text x="{x + 16}" y="533" font-size="12" fill="{MUTED}">{escape(sub)}</text>')
    s.append(f'<path d="M30 248 H12 V518 H30" stroke="{ORANGE}" stroke-width="2.5" fill="none" marker-start="url(#b)" marker-end="url(#b)"/>')       # follow-ups go out, answers come back
    s.append(f'<text x="38" y="478" font-size="11.5" fill="{ORANGE}">follow-up and answer loop</text>')
    key = [(BLUE, "statistics (the screen)"), (GREEN, "plain code and checks"), (ORANGE, "the agent (a model)"), (PEOPLE, "PI teams")]
    kx = 30
    s.append(f'<text x="{kx}" y="586" font-size="12.5" font-weight="bold" fill="{INK}">Key</text>')
    for col, label in key:
        kx += [60, 190, 190, 190][key.index((col, label))]
        s.append(f'<rect x="{kx - 24}" y="574" width="14" height="14" rx="3" fill="none" stroke="{col}" stroke-width="2.5"/>')
        s.append(f'<text x="{kx - 4}" y="586" font-size="12.5" fill="{MUTED}">{label}</text>')
    s.append(f'<text x="{W - 30}" y="586" text-anchor="end" font-size="12.5" fill="{MUTED}">dashed boxes: what surrounds the agent</text>')
    s.append("</svg>")
    write("agent.svg", "\n".join(s))


def workflow_v40():
    """The fixed workflow (v4.0) under the agent figure in the README: code sets the order; a learned formula decides whom to ask, and a demand needs a recovery worth its staff cost."""
    W, H = 1000, 400
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>', f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{MUTED}"/></marker>'
         f'<marker id="b" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{ORANGE}"/></marker></defs>',
         f'<text x="30" y="30" font-size="16" font-weight="bold" fill="{INK}">The fixed workflow (v4.0): code sets the order of the steps</text>']
    steps = [("Screen", "eb_upper_t: share billed 99214 or 99215 against expected, shrunk for small panels. Top 10% of providers.", BLUE),
             ("Ask or skip", "A learned formula (fitted on score 4.0) decides whom to ask for charts.", GREEN),
             ("Request charts", "30 random charts, then one follow-up on any deficiency.", GREEN),
             ("Stop", "No second request: the first sample and its follow-up decide.", GREEN),
             ("Rules decide", "Chart rule and summary rules (4.0) set the leaning; where silent: inconclusive. No model is called.", GREEN),
             ("Demand floor", "Demand only if the payer's estimated recovery covers the staff cost of a demand.", GREEN),
             ("Checks", "Citations and numbers must match the evidence.", GREEN),
             ("PI teams review", "Drafts only. Nothing is sent or decided automatically.", PEOPLE)]
    bw, bh, gap = 205, 118, 28
    pos = [(30 + i * (bw + gap), 112) for i in range(4)] + [(30 + i * (bw + gap), 262) for i in range(4)]
    for (n, body, col), (x, y) in zip(steps, pos):
        s.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="10" fill="#f9fafb" stroke="{col}" stroke-width="2.5"/>')
        s.append(f'<text x="{x + 14}" y="{y + 28}" font-size="14.5" font-weight="bold" fill="{INK}">{escape(n)}</text>')
        for j, line in enumerate(textwrap.wrap(body, 30)[:5]):
            s.append(f'<text x="{x + 14}" y="{y + 50 + j * 16}" font-size="12" fill="{MUTED}">{escape(line)}</text>')
    for i in (0, 1, 2, 4, 5, 6):                         # left to right within a row
        x, y = pos[i]
        s.append(f'<path d="M{x + bw} {y + bh / 2} L{x + bw + gap} {y + bh / 2}" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#a)" fill="none"/>')
    x3, y3 = pos[3]                                      # down from Stop to Rules decide
    s.append(f'<path d="M{x3 + bw / 2} {y3 + bh} V{y3 + bh + 22} H{pos[4][0] + bw / 2} V{pos[4][1]}" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#a)" fill="none"/>')
    cx = pos[2][0]                                       # providers answer: requests go out and answers come back (both ways)
    s.append(f'<rect x="{cx}" y="50" width="{bw * 2 + gap}" height="34" rx="8" fill="none" stroke="{GREEN}" stroke-width="2" stroke-dasharray="6 4"/>')
    s.append(f'<text x="{cx + 14}" y="72" font-size="12.5" font-weight="bold" fill="{INK}">Simulated providers answer every request and follow-up</text>')
    for i in (2, 3):
        x = pos[i][0] + bw / 2
        s.append(f'<path d="M{x} 84 V{pos[i][1] - 2}" stroke="{ORANGE}" stroke-width="2.5" fill="none" marker-start="url(#b)" marker-end="url(#b)"/>')
    s.append("</svg>")
    write("workflow.svg", "\n".join(s))


def score_waterfall():
    """How score 4.0 is built for agent v5.0 on the ten fresh seeds, dollars summed over the seeds: recovery, staff cost, abrasion, net score. The explanation is text in the README (release_table.score_text)."""
    import release_table
    w = release_table.score_parts("A5.0")
    n = w["n"]
    per = lambda x: x
    W, H = 1000, 280
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>', f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="30" y="30" font-size="16" font-weight="bold" fill="{INK}">What sets the score: agent v5.0, ten fresh seeds, dollars summed over the seeds</text>']
    top, bottom = 50, 220
    bars = [("Recovery", per(w["recovery"]), GREEN), ("Staff cost", -per(w["staff"]), ORANGE), ("Abrasion", -per(w["abrasion"]), ORANGE), ("Net score", per(w["score"]), BLUE)]
    low = per(w["score"])
    sc = (bottom - top - 40) / (per(w["recovery"]) - low)
    y0 = top + 24 + per(w["recovery"]) * sc                  # the zero line
    cur = 0.0
    X = [140, 330, 520, 710]
    for (name, v, col), x in zip(bars, X):
        if name == "Net score":
            a0, a1 = 0, v
        else:
            a0, a1 = cur, cur + v
            cur = a1
        ya, yb = y0 - a0 * sc, y0 - a1 * sc
        s.append(f'<rect x="{x}" y="{min(ya, yb):.1f}" width="110" height="{max(abs(yb - ya), 1.5):.1f}" rx="3" fill="none" stroke="{col}" stroke-width="2.5"/>')
        label = f"+${v:,.0f}" if v > 0 else f"-${-v:,.0f}"
        s.append(f'<text x="{x + 55}" y="{min(ya, yb) - 6:.1f}" text-anchor="middle" font-size="13" font-weight="bold" fill="{INK}">{label}</text>')
        s.append(f'<text x="{x + 55}" y="{bottom + 22}" text-anchor="middle" font-size="12.5" fill="{MUTED}">{name}</text>')
    s.append(f'<line x1="120" y1="{y0:.1f}" x2="880" y2="{y0:.1f}" stroke="{LINE}" stroke-width="1"/>')
    s.append("</svg>")
    write("score_waterfall.svg", "\n".join(s))


def mlr_headroom():
    """Fully insured commercial premium and headroom above the ACA floors for the ten largest insurer groups without Kaiser (experiments/mlr_headroom_2024.csv, eval/mlr_headroom.py),
    and UnitedHealth's members by funding arrangement (its FY2025 10-K): the risk-based part is what the table measures, the self-funded part is the extension."""
    import csv
    rows = list(csv.DictReader(open(os.path.join(ROOT, "experiments", "mlr_headroom_2024.csv"))))
    P, H = {}, {}
    for r in rows:
        P[r["group"]] = P.get(r["group"], 0) + float(r["premium"])
        H[r["group"]] = H.get(r["group"], 0) + float(r["headroom"])
    names = {"UNITEDHEALTH GRP": "UnitedHealth", "Elevance Hlth Inc Grp": "Elevance", "HCSC GRP": "HCSC", "CVS Health Group": "CVS Health (Aetna)", "CENTENE CORP GRP": "Centene",
             "Blue Cross and Blue Shield of Florida, Inc.": "Florida Blue", "Cigna Hlth Grp": "Cigna", "Blue Shield of California Group": "Blue Shield of California", "CAREFIRST INC GRP": "CareFirst", "HIGHMARK GRP": "Highmark"}
    top = sorted((g for g in P if g != "KAISER FOUNDATION GRP"), key=lambda g: -P[g])[:10]
    assert set(top) == set(names)
    W, H_ = 1000, 560
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H_}" width="{W}" height="{H_}" {FONT}>', f'<rect width="{W}" height="{H_}" fill="#ffffff"/>',
         f'<text x="30" y="30" font-size="16" font-weight="bold" fill="{INK}">Risk-based commercial: premium and headroom above the ACA floors, 2024</text>',
         f'<text x="30" y="50" font-size="12.5" fill="{MUTED}">Ten largest insurer groups, Kaiser excluded (it bears the cost of care). Headroom = premium x (MLR - floor); floors 80% (individual, small group), 85% (large group).</text>',
         f'<text x="200" y="84" font-size="12.5" font-weight="bold" fill="{INK}">Fully insured premium, $B</text>', f'<text x="620" y="84" font-size="12.5" font-weight="bold" fill="{INK}">Headroom, $B (share of premium)</text>']
    x0, x1, sp, sh = 200, 620, 3.0, 30.0
    for i, g in enumerate(top):
        y = 96 + i * 34
        s.append(f'<text x="{x0 - 10}" y="{y + 15}" text-anchor="end" font-size="12.5" fill="{INK}">{names[g]}</text>')
        w = P[g] / 1e9 * sp
        s.append(f'<rect x="{x0}" y="{y}" width="{w:.1f}" height="22" rx="3" fill="none" stroke="{MUTED}" stroke-width="2"/>')
        s.append(f'<text x="{x0 + w + 6:.1f}" y="{y + 15}" font-size="12" fill="{MUTED}">{P[g] / 1e9:.1f}</text>')
        wh = H[g] / 1e9 * sh
        s.append(f'<rect x="{x1}" y="{y}" width="{wh:.1f}" height="22" rx="3" fill="none" stroke="{BLUE}" stroke-width="2.5"/>')
        s.append(f'<text x="{x1 + wh + 6:.1f}" y="{y + 15}" font-size="12" fill="{MUTED}">{H[g] / 1e9:.1f} ({H[g] / P[g]:.0%})</text>')
    tp, th = sum(P[g] for g in top) / 1e9, sum(H[g] for g in top) / 1e9
    y = 96 + 10 * 34 + 14
    s.append(f'<text x="30" y="{y}" font-size="13" font-weight="bold" fill="{INK}">The ten together: premium ${tp:.0f}B, headroom ${th:.1f}B; one MLR point is ${tp / 100:.1f}B. A ceiling for any cost lever, not a market size.</text>')
    y += 34
    s.append(f'<text x="30" y="{y}" font-size="13" font-weight="bold" fill="{INK}">The extension: self-funded members (UnitedHealth, December 2025, 10-K)</text>')
    rb, fb = 8.165, 21.485
    wtot = 700.0
    s.append(f'<rect x="30" y="{y + 12}" width="{wtot * rb / (rb + fb):.1f}" height="26" rx="3" fill="none" stroke="{BLUE}" stroke-width="2.5"/>')
    s.append(f'<rect x="{30 + wtot * rb / (rb + fb):.1f}" y="{y + 12}" width="{wtot * fb / (rb + fb):.1f}" height="26" rx="3" fill="none" stroke="{GREEN}" stroke-width="2.5" stroke-dasharray="6 4"/>')
    s.append(f'<text x="38" y="{y + 30}" font-size="12" fill="{INK}">risk-based 8.2M</text>')
    s.append(f'<text x="{30 + wtot * rb / (rb + fb) + 10:.1f}" y="{y + 30}" font-size="12" fill="{INK}">fee-based (self-funded) 21.5M: no premium, no MLR, not in the bars above</text>')
    s.append(f'<text x="30" y="{y + 56}" font-size="12" fill="{MUTED}">Same payment integrity problem, different payer of the savings: the employer. Sizing needs claims dollars for these lives, which we do not have yet.</text>')
    s.append("</svg>")
    write("mlr_headroom.svg", "\n".join(s))


def pipeline():
    for v in VERSIONS:
        how_it_works(v)


def _icon(name, x, y, col):
    """Small 26px icons drawn from basic shapes."""
    c = f'fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    g = {"data": f'<rect x="3" y="2" width="16" height="21" rx="2" {c}/><path d="M7 8h8M7 12h8M7 16h5" {c}/>',
         "screen": f'<path d="M2 3h22l-8 9v9l-6-3v-6z" {c}/>',
         "records": f'<path d="M2 7h8l2 3h12v12H2z" {c}/>',
         "write": f'<path d="M4 22l1-6L18 3l5 5L10 21z" {c}/><path d="M15 6l5 5" {c}/>',
         "decide": f'<circle cx="13" cy="13" r="10" {c}/><path d="M17 9l-2 6-6 2 2-6z" {c}/>',
         "eval": f'<path d="M3 22V10M10 22V4M17 22V14M24 22H2" {c}/>'}[name]
    return f'<g transform="translate({x},{y})">{g}</g>'


def progression_cells(rows=None):
    """Headline numbers per version, read from experiments/results.csv (the source of truth)."""
    import csv
    rows = rows or list(csv.DictReader(open(os.path.join(ROOT, "experiments", "results.csv"))))

    def pick(ids, stage):
        return [r for r in rows if r["run_id"] in ids and r["stage"] == stage]

    def tot(rs):
        found = sum(int(r["fn_total"]) - int(r["fn_missed"]) for r in rs)
        up = sum(int(r["fn_total"]) for r in rs)
        fp = sum(int(r["fp_count"]) for r in rs)
        return found, up, fp, sum(int(r["fp_total"]) for r in rs)
    v1 = tot(pick({"261009_2_api"}, "AI"))
    v2 = tot(pick({"261013_12_api", "261013_13_api"}, "AI"))
    v3 = tot(pick({"261013_8_api", "261013_9_api"}, "Agent"))
    v3_h = sum(int(r["honest_requested"]) for r in pick({"261013_8_api", "261013_9_api"}, "Agent"))
    v2_h = sum(int(r["honest_requested"]) for r in pick({"261013_12_api", "261013_13_api"}, "AI"))
    import release_table
    extra = release_table.headline_cells()
    return {**extra, "v1.0": f"Held-out run: {v1[0]} of {v1[1]} upcoders called, {v1[2]} of {v1[3]} honest providers accused (charts were handed over, so optimistic).",
            "v2.0": f"Two reserved seeds: {v2[0]} of {v2[1]} upcoders found, {v2[2]} honest accused; {v2_h} honest providers asked for charts.",
            "v3.0": f"Same two seeds: {v3[0]} of {v3[1]} upcoders found, {v3[2]} honest accused; {v3_h} honest providers asked for charts."}


def progression():
    """One slide: how it works over time, as a table with icons and headline eval results."""
    cells = progression_cells()
    ev = {"v1.x": cells["v1.0"], "v2.x": cells["v2.0"] + " " + cells["v4.0"], "v3.x": cells["v3.0"] + " " + cells["v5.0"]}
    cols = [("data", "Claims"), ("screen", "Screen"), ("records", "Charts"), ("write", "Summaries"), ("decide", "Who decides"),
            ("eval", "Headline results")]
    rows = [("v1.x", "Fixed workflow", ["Provider, patient and claim tables with a stored condition count.", "Top 25 by statistics. Fixed.",
                                      "A sample handed to the AI up front.", "The AI writes it all: facts, citations, next steps.", "Code, in a fixed order."]),
            ("v2.x", "Fixed workflow", ["Plan-shaped claims; conditions derived from them. Harder data from v2.2; data 4.0 (habits) from v4.0.", "eb_ratio_t, top 10% of providers (v2.0: suspicion 5 or higher); eb_upper_t from v4.0.",
                                      "Learned ask-or-skip, 30 random charts, one follow-up; v4.0 stops there.", "Code writes the facts and decides; no model from v2.5.",
                                      "Code, with formulas fitted on net dollars; v4.0 adds a demand floor."]),
            ("v3.x", "Agent", ["Same as v2.x.", "A tool the agent runs with any cutoff, eb_upper_t from v5.0.", "The agent chooses whom to ask, what sample, and whether to follow up; advice arrives in the tool results.",
                              "The agent submits findings; code adds facts and checks.", "The agent, within caps; an upcoding call the chart rule supports is binding."])]
    W, H = 1380, 410
    x0, cw, rh, y0 = 150, 170, 118, 56
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="1000" height="{round(H * 1000 / W)}" {FONT}>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         ]
    for i, (icon, label) in enumerate(cols):
        x = x0 + i * cw
        s.append(_icon(icon, x, 14, BLUE))
        s.append(f'<text x="{x + 34}" y="32" font-size="12.5" font-weight="bold" fill="{INK}">{escape(label)}</text>')
    for r, (v, name, cells) in enumerate(rows):
        y = y0 + r * rh
        s.append(f'<rect x="20" y="{y}" width="{W - 40}" height="{rh - 8}" rx="10" fill="#f9fafb" stroke="{LINE}"/>')
        s.append(f'<text x="34" y="{y + 30}" font-size="18" font-weight="bold" fill="{INK}">{v}</text>')
        for j, line in enumerate(textwrap.wrap(name, 14)):
            s.append(f'<text x="34" y="{y + 52 + j * 16}" font-size="12.5" fill="{MUTED}">{escape(line)}</text>')
        for i, text in enumerate(cells + [ev[v]]):
            x = x0 + i * cw
            width = 24 if i < 5 else 52
            for j, line in enumerate(textwrap.wrap(text, width)[:6]):
                s.append(f'<text x="{x}" y="{y + 24 + j * 16}" font-size="12" fill="{INK if i == 5 else MUTED}">{escape(line)}</text>')
    s.append("</svg>")
    write("progression.svg", "\n".join(s))


def em_levels():
    """How an office-visit level is really chosen and how it is checked later."""
    W, H = 1000, 560
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="30" y="38" font-size="19" font-weight="bold" fill="{INK}">How an office-visit level is chosen, and checked later</text>',
         f'<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
         f'<path d="M0 0 L10 5 L0 10 z" fill="{MUTED}"/></marker></defs>']

    def box(x, y, w, h, col, title, lines, dash=''):
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#f9fafb" stroke="{col}" stroke-width="2.5"{dash}/>')
        s.append(f'<text x="{x + 16}" y="{y + 28}" font-size="14.5" font-weight="bold" fill="{INK}">{escape(title)}</text>')
        for j, line in enumerate(lines):
            s.append(f'<text x="{x + 16}" y="{y + 54 + j * 20}" font-size="12.5" fill="{MUTED}">{escape(line)}</text>')

    def arrow(x1, y1, x2, y2):
        s.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{MUTED}" stroke-width="2" marker-end="url(#a)"/>')

    def line(x1, y1, x2, y2):
        s.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{MUTED}" stroke-width="2"/>')
    s.append(f'<text x="30" y="72" font-size="13" font-weight="bold" fill="{BLUE}">1. At the visit: two ways to support a level</text>')
    box(30, 84, 300, 150, BLUE, "Medical decision making", ["Three elements, two of three must match:",
        "- how serious the problems are", "- how much data was reviewed or ordered",
        "- risk of the treatment (e.g. prescriptions)"])
    s.append(f'<text x="180" y="259" font-size="14" font-style="italic" text-anchor="middle" fill="{MUTED}">or</text>')
    box(30, 272, 300, 100, BLUE, "Total time that day", ["About 10 / 20 / 30 / 40+ minutes of the",
        "doctor's own time for 99212 to 99215.", "History and exam no longer set the level."])
    line(330, 159, 350, 159)
    line(330, 322, 350, 322)
    line(350, 159, 350, 322)
    arrow(350, 240, 422, 240)
    s.append(f'<text x="356" y="228" font-size="12" font-weight="bold" fill="{INK}">higher</text>')
    s.append(f'<text x="356" y="266" font-size="12" font-weight="bold" fill="{INK}">wins</text>')
    s.append(f'<text x="430" y="72" font-size="13" font-weight="bold" fill="{ORANGE}">2. The code on the claim</text>')
    box(430, 84, 190, 288, ORANGE, "Level billed", ["99212  straightforward", "99213  low", "99214  moderate", "99215  high",
        "", "99211 is a nurse visit", "with no decision-making", "requirement."])
    arrow(620, 228, 662, 228)
    s.append(f'<text x="670" y="72" font-size="13" font-weight="bold" fill="{GREEN}">3. After payment: someone re-scores it</text>')
    box(670, 84, 300, 288, GREEN, "Contractors and auditors", ["Pull the record for a sample of visits.",
        "Coders and nurses re-score the note", "against the same rules.", "",
        "Typical finding: the note does not", "support the level (or supports a higher", "one). Big audits extrapolate the", "overpayment from the sample."])
    d = ' stroke-dasharray="6 4"'
    s.append(f'<text x="30" y="404" font-size="13" font-weight="bold" fill="{INK}">Example: one visit that is upcoded</text>')
    box(30, 414, 300, 132, BLUE, "Note supports 99214", ["No time recorded. Problems high,", "data moderate, risk low. The second-",
        "highest element is moderate, so", "the visit justifies 99214."], d)
    box(430, 414, 190, 132, ORANGE, "Billed 99215", ["One level above what", "the note supports:", "upcoded."], d)
    box(670, 414, 300, 132, GREEN, "Audit finds the gap", ["Second-highest is moderate, not high: data", "is from one category (2 labs, 1 outside", "note); high needs at least two. So the", "note supports 99214, not 99215."], d)
    arrow(330, 480, 422, 480)
    arrow(620, 480, 662, 480)
    s.append("</svg>")
    write("em_levels.svg", "\n".join(s))


def cms_mix():
    """Visit mix 99211-99215: CMS GA Family Practice (observed) against the synthetic normal providers."""
    codes = ["99211", "99212", "99213", "99214", "99215"]
    cms = [0.007, 0.010, 0.287, 0.665, 0.031]
    syn = [0.012, 0.012, 0.362, 0.570, 0.044]
    W, H, x0, y0, ph = 640, 340, 70, 60, 220
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="30" y="30" font-size="16" font-weight="bold" fill="{INK}">Share of office visits by level: CMS vs synthetic</text>']
    for v in (0, 0.2, 0.4, 0.6):
        y = y0 + ph - v / 0.7 * ph
        s.append(f'<line x1="{x0}" y1="{y:.0f}" x2="{W - 30}" y2="{y:.0f}" stroke="#e5e7eb"/>')
        s.append(f'<text x="{x0 - 8}" y="{y + 4:.0f}" font-size="11" text-anchor="end" fill="{MUTED}">{int(v * 100)}%</text>')
    gw = (W - 30 - x0) / 5
    for i, c in enumerate(codes):
        for j, (vals, col) in enumerate(((cms, BLUE), (syn, ORANGE))):
            h = vals[i] / 0.7 * ph
            x = x0 + i * gw + 18 + j * 50
            s.append(f'<rect x="{x:.0f}" y="{y0 + ph - h:.1f}" width="44" height="{h:.1f}" fill="{col}"/>')
            s.append(f'<text x="{x + 22:.0f}" y="{y0 + ph - h - 5:.1f}" font-size="11" text-anchor="middle" fill="{INK}">{vals[i] * 100:.1f}%</text>')
        s.append(f'<text x="{x0 + i * gw + gw / 2:.0f}" y="{y0 + ph + 20}" font-size="12.5" text-anchor="middle" fill="{INK}">{c}</text>')
    s.append(f'<rect x="{x0}" y="{H - 38}" width="12" height="12" fill="{BLUE}"/><text x="{x0 + 18}" y="{H - 28}" font-size="12" fill="{MUTED}">CMS, GA Family Practice (observed)</text>')
    s.append(f'<rect x="{x0 + 250}" y="{H - 38}" width="12" height="12" fill="{ORANGE}"/><text x="{x0 + 268}" y="{H - 28}" font-size="12" fill="{MUTED}">Synthetic, normal providers</text>')
    s.append("</svg>")
    write("cms_mix.svg", "\n".join(s))


def results():
    truth = json.load(open(os.path.join(ROOT, "eval", "answer_key", "ground_truth.json")))
    flagged = [r for r in __import__("csv").DictReader(open(os.path.join(ROOT, "reports", "flagged.csv")))]
    ev = run_eval.evaluate(flagged, truth, 25)["Combined list"]
    honest_flagged = ev["hard_neg_flagged"] + ev["normal_flagged"]
    runs = []
    for label, rel in (("AI summaries (chat),\nno records evidence", "experiments/261008_3_cc/summaries_checked.jsonl"),
                       ("AI summaries (chat),\nwith records evidence*", "experiments/261008_4_cc/summaries_checked.jsonl"),
                       ("Live API run,\nwith records evidence*", "experiments/261009_1_api/case_summaries_checked.jsonl")):
        recs = run_eval.load_checked(os.path.join(ROOT, rel))
        L = run_eval.leaning_stats(recs, truth)
        runs.append((label, L["honest_called_upcoding"], L["true_upcoders_called"], L["honest_total"]))
    bars = [("Screen alone\n(no AI review)", honest_flagged, ev["upcoders_found"], honest_flagged)] + runs
    W, H = 920, 470
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="30" y="34" font-size="20" font-weight="bold" fill="{INK}">Honest doctors still accused after review</text>',
         f'<text x="30" y="56" font-size="13" fill="{MUTED}">Of the 25 providers the screen flags, 8 are real (planted) upcoders and 17 are honest. Lower red bars are better.</text>']
    x0, y0, ph, maxv = 80, 100, 250, 17
    for v in range(0, 18, 4):
        y = y0 + ph - ph * v / maxv
        s.append(f'<line x1="{x0}" y1="{y:.0f}" x2="{W - 40}" y2="{y:.0f}" stroke="#eee"/>')
        s.append(f'<text x="{x0 - 8}" y="{y + 4:.0f}" text-anchor="end" font-size="12" fill="{MUTED}">{v}</text>')
    slot = (W - 40 - x0) / len(bars)
    for i, (label, honest, caught, total) in enumerate(bars):
        cx = x0 + slot * (i + 0.5)
        h = ph * honest / maxv
        s.append(f'<rect x="{cx - 70:.0f}" y="{y0 + ph - h:.0f}" width="62" height="{h:.0f}" rx="3" fill="{RED}"/>')
        s.append(f'<text x="{cx - 39:.0f}" y="{y0 + ph - h - 8:.0f}" text-anchor="middle" font-size="16" font-weight="bold" fill="{RED}">{honest}</text>')
        s.append(f'<rect x="{cx + 8:.0f}" y="{y0 + ph - ph * caught / maxv:.0f}" width="62" height="{ph * caught / maxv:.0f}" rx="3" fill="{GREEN}"/>')
        s.append(f'<text x="{cx + 39:.0f}" y="{y0 + ph - ph * caught / maxv - 8:.0f}" text-anchor="middle" font-size="16" font-weight="bold" fill="{GREEN}">{caught}</text>')
        for j, line in enumerate(label.split("\n")):
            s.append(f'<text x="{cx:.0f}" y="{y0 + ph + 24 + j * 16}" text-anchor="middle" font-size="12.5" fill="{INK}">{escape(line)}</text>')
    s += [f'<rect x="{W - 330}" y="72" width="12" height="12" fill="{RED}"/><text x="{W - 312}" y="83" font-size="12" fill="{INK}">honest doctors accused (of 17)</text>',
          f'<rect x="{W - 330}" y="90" width="12" height="12" fill="{GREEN}"/><text x="{W - 312}" y="101" font-size="12" fill="{INK}">real upcoders caught (of 8)</text>',
          f'<text x="30" y="{H - 38}" font-size="11.5" fill="{MUTED}">Synthetic data, one random seed, small counts. The first two AI bars were written by agents in a chat session; the last is the project pipeline itself calling the API.</text>',
          f'<text x="30" y="{H - 20}" font-size="11.5" fill="{MUTED}">*The records-review evidence is generated from the same hidden truth that defines an upcoded visit, so this bar shows a ceiling, not a real-world estimate.</text>',
          "</svg>"]
    write("results.svg", "\n".join(s))
    return bars


def case_card(pid="P0215"):
    import case_summary as cs
    recs = {json.loads(l)["provider_id"]: json.loads(l) for l in open(os.path.join(ROOT, "experiments", "261008_4_cc", "summaries_checked.jsonl"))}
    rec = recs[pid]["summary"]
    d = os.path.join(ROOT, "data", "synthetic")
    chronic, age, cond, claims = cs.load(d)
    docs = cs.load_docs(d)
    import csv
    fl = {r["provider_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "reports", "flagged.csv")))}
    pk = cs.build_packet(pid, fl[pid], chronic, age, cond, claims, cs.peer_rates(claims, chronic), docs, cs.doc_peer_rates(claims, docs))
    unsup = next(t for t in pk["documentation_review"]["by_billed_level"] if t["billed_cpt"] == "99215")
    chart = open(os.path.join(ROOT, "experiments", "261009_1_api", "charts", f"{pid}.svg")).read()
    inner = re.sub(r"^<svg[^>]*>", "", chart.strip()).rsplit("</svg>", 1)[0]
    W, H = 920, 880
    tiles = [(f"{pk['share_99215']:.0%}", "of visits billed at the top code"),
             (f"{pk['expected_share_given_patient_complexity']:.0%}", "expected for these patients"),
             (f"{unsup['unsupported_rate']:.0%}", "of reviewed top-code visits not supported by the records")]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<rect x="12" y="12" width="{W - 24}" height="{H - 24}" rx="14" fill="#f9fafb" stroke="{LINE}"/>',
         f'<text x="36" y="48" font-size="13" fill="{MUTED}">EXAMPLE CASE PAGE (synthetic data)</text>',
         f'<text x="36" y="78" font-size="22" font-weight="bold" fill="{INK}">Provider {pid}</text>',
         f'<rect x="{W - 360}" y="52" width="324" height="32" rx="16" fill="#fee2e2"/>',
         f'<text x="{W - 198}" y="73" text-anchor="middle" font-size="13.5" font-weight="bold" fill="{RED}">Pattern consistent with upcoding (advisory)</text>']
    for i, (big, small) in enumerate(tiles):
        x = 36 + i * 286
        s.append(f'<rect x="{x}" y="104" width="266" height="86" rx="10" fill="#ffffff" stroke="{LINE}"/>')
        s.append(f'<text x="{x + 16}" y="146" font-size="34" font-weight="bold" fill="{ORANGE}">{big}</text>')
        for j, line in enumerate(textwrap.wrap(small, 34)):
            s.append(f'<text x="{x + 16}" y="{168 + j * 15}" font-size="12.5" fill="{MUTED}">{escape(line)}</text>')
    s.append(f'<text x="36" y="226" font-size="14" font-weight="bold" fill="{INK}">What the AI wrote (shortened)</text>')
    text = re.sub(r"\s+", " ", rec["rationale"])
    text = text[:430].rsplit(" ", 1)[0] + " ..."
    for j, line in enumerate(textwrap.wrap(text, 112)):
        s.append(f'<text x="36" y="{250 + j * 19}" font-size="13.5" fill="{INK}">{escape(line)}</text>')
    s.append(f'<text x="36" y="372" font-size="12.5" fill="{MUTED}">Cited claims: {escape(", ".join(rec["cited_claim_ids"][:5]))} ... (each checked against the claims data)</text>')
    s.append(f'<svg x="76" y="388" width="768" height="480" viewBox="0 0 760 470" font-family="Helvetica, Arial, sans-serif" font-size="12">{inner}</svg>')
    s.append("</svg>")
    write("case_card.svg", "\n".join(s))


def funnel():
    import csv
    n_all = sum(1 for _ in csv.DictReader(open(os.path.join(ROOT, "data", "synthetic", "providers.csv"))))
    flagged = [r for r in csv.DictReader(open(os.path.join(ROOT, "reports", "flagged.csv"))) if r["flagged"] == "True"]
    recs = run_eval.load_checked(os.path.join(ROOT, "experiments", "261009_1_api", "case_summaries_checked.jsonl"))
    passed = sum(r["citation_check"]["passed"] for r in recs)
    lean = {"up": 0, "acute": 0, "unclear": 0}
    for r in recs:
        if r["citation_check"]["passed"]:
            k = {"pattern_consistent_with_upcoding": "up", "pattern_consistent_with_high_acuity_panel": "acute"}.get(r["summary"]["leaning"], "unclear")
            lean[k] += 1
    packets = sum(1 for d in os.listdir(os.path.join(ROOT, "reports", "pi_packets")) if os.path.isdir(os.path.join(ROOT, "reports", "pi_packets", d)))
    W, H = 920, 600
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="30" y="34" font-size="20" font-weight="bold" fill="{INK}">From {n_all} doctors to a few cases for recovery</text>',
         f'<text x="30" y="56" font-size="13" fill="{MUTED}">Each step narrows the group with a different tool. People make the final decisions.</text>']

    def bar(x, y, w, h, fill, stroke, big, small, big_col=INK):
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        s.append(f'<text x="{x + 18}" y="{y + 38}" font-size="30" font-weight="bold" fill="{big_col}">{big}</text>')
        for j, line in enumerate(textwrap.wrap(small, int(w / 7.1))):
            s.append(f'<text x="{x + 18}" y="{y + 62 + j * 17}" font-size="13" fill="{MUTED}">{escape(line)}</text>')

    def arrow(x1, y1, x2, y2, label=""):
        s.append(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{MUTED}" stroke-width="2" marker-end="url(#a)"/>')
        if label:
            s.append(f'<text x="{x1 + 10}" y="{(y1 + y2) / 2 + 4}" font-size="12" fill="{MUTED}">{escape(label)}</text>')
    s.append(f'<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{MUTED}"/></marker></defs>')
    bar(30, 80, 860, 84, "#eff6ff", BLUE, f"{n_all} doctors", "Every provider in the data. The statistical screen ranks them by how often they bill the top visit code, adjusted for how sick their patients are.", BLUE)
    arrow(460, 164, 460, 196, "keep the 25 most unusual")
    bar(130, 198, 660, 84, "#eff6ff", BLUE, f"{len(flagged)} flagged for review", "Unusual, not necessarily guilty. Many are honest doctors who treat sicker patients or code high for reasons the claims do not show.", BLUE)
    arrow(460, 282, 460, 314, f"AI writes a case summary for each; the citation check passes {passed} of {len(recs)}")
    cols = [("up", f"{lean['up']}", "look like upcoding", "Move on to recovery.", "#fff7ed", ORANGE),
            ("acute", f"{lean['acute']}", "look like sicker patients", "Set aside: the records support the billing.", "#f0fdf4", GREEN),
            ("unclear", f"{lean['unclear']}", "unclear", "Not enough records to tell. Request more.", "#f9fafb", MUTED)]
    xs = [30, 330, 630]
    for (k, big, title, body, fill, col), x in zip(cols, xs):
        s.append(f'<rect x="{x}" y="318" width="260" height="104" rx="10" fill="{fill}" stroke="{col}" stroke-width="2"/>')
        s.append(f'<text x="{x + 18}" y="360" font-size="30" font-weight="bold" fill="{col}">{big}</text>')
        s.append(f'<text x="{x + 18 + 19 * len(big) + 10}" y="360" font-size="15" font-weight="bold" fill="{INK}">{escape(title)}</text>')
        for j, line in enumerate(textwrap.wrap(body, 34)):
            s.append(f'<text x="{x + 18}" y="{386 + j * 17}" font-size="13" fill="{MUTED}">{escape(line)}</text>')
    arrow(160, 422, 160, 454, "")
    bar(30, 456, 560, 104, "#fff7ed", ORANGE, f"{packets} recovery packets", "Records to request, a reproducible sample, and an overpayment estimator. A person reviews the records and decides what happens next.", ORANGE)
    s.append(f'<text x="620" y="486" font-size="13" font-weight="bold" fill="{INK}">Not accused</text>')
    for j, line in enumerate(textwrap.wrap("The set-aside and unclear cases are not accused of anything. The AI's lean is advice to a reviewer, not a verdict.", 34)):
        s.append(f'<text x="620" y="{506 + j * 17}" font-size="13" fill="{MUTED}">{escape(line)}</text>')
    s.append("</svg>")
    write("funnel.svg", "\n".join(s))


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "docs", "images"), exist_ok=True)
    pipeline()
    agent_actions()
    workflow_v40()
    score_waterfall()
    mlr_headroom()
    progression()
    em_levels()
    cms_mix()
    funnel()
    print("results:", results())
    case_card()
    print("figures written to docs/images/")
