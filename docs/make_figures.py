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


def pipeline():
    steps = [("1", "Billing data", "Fake (synthetic) claims modelled on public Medicare numbers", BLUE),
             ("2", "Statistical screen", "Flags doctors who bill the top visit code unusually often, adjusted for how sick their patients are", BLUE),
             ("3", "Review list", "The 25 most unusual providers go to a reviewer", BLUE),
             ("4", "AI case summary", "An AI writes a short explanation and cites the exact claims it relies on", ORANGE),
             ("5", "Citation check", "Plain code rejects any summary that cites a claim that does not exist or belongs to someone else", GREEN),
             ("6", "Case page", "One page per provider: the summary, its citations and a chart against peers", ORANGE),
             ("7", "Recovery packet", "Draft material for the team that recovers money: records to request and a sample plan", ORANGE)]
    W, H = 920, 500
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="30" y="34" font-size="20" font-weight="bold" fill="{INK}">How the project works</text>',
         f'<text x="30" y="56" font-size="13" fill="{MUTED}">Statistics decide who gets flagged. The AI explains. Code checks the AI. People decide what happens next.</text>']
    bw, bh, gap = 200, 120, 18
    pos = [(30 + i * (bw + gap), 80) for i in range(4)] + [(30 + i * (bw + gap) + (bw + gap) / 2, 300) for i in range(3)]
    for (n, title, body, col), (x, y) in zip(steps, pos):
        s.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh + 30}" rx="10" fill="#f9fafb" stroke="{col}" stroke-width="2"/>')
        s.append(f'<circle cx="{x + 24}" cy="{y + 26}" r="14" fill="{col}"/>')
        s.append(f'<text x="{x + 24}" y="{y + 31}" text-anchor="middle" font-size="14" font-weight="bold" fill="#fff">{n}</text>')
        s.append(f'<text x="{x + 46}" y="{y + 31}" font-size="14" font-weight="bold" fill="{INK}">{escape(title)}</text>')
        for j, line in enumerate(textwrap.wrap(body, 30)[:6]):
            s.append(f'<text x="{x + 16}" y="{y + 62 + j * 18}" font-size="12.5" fill="{MUTED}">{escape(line)}</text>')
    for i in range(3):
        x = pos[i][0] + bw
        s.append(f'<path d="M{x + 2} 160 L{x + gap - 4} 160" stroke="{MUTED}" stroke-width="2" marker-end="url(#a)"/>')
    s.append(f'<path d="M{pos[3][0] + bw / 2} {pos[3][1] + bh + 30} L{pos[3][0] + bw / 2} 275 L{pos[4][0] + bw / 2} 275 L{pos[4][0] + bw / 2} 298" '
             f'fill="none" stroke="{MUTED}" stroke-width="2" marker-end="url(#a)"/>')
    for i in range(4, 6):
        x = pos[i][0] + bw
        s.append(f'<path d="M{x + 2} 380 L{x + gap - 4} 380" stroke="{MUTED}" stroke-width="2" marker-end="url(#a)"/>')
    s.append(f'<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
             f'<path d="M0 0 L10 5 L0 10 z" fill="{MUTED}"/></marker></defs>')
    s += [f'<rect x="30" y="472" width="14" height="14" rx="3" fill="none" stroke="{BLUE}" stroke-width="2"/>',
          f'<text x="50" y="484" font-size="12" fill="{MUTED}">statistics</text>',
          f'<rect x="130" y="472" width="14" height="14" rx="3" fill="none" stroke="{ORANGE}" stroke-width="2"/>',
          f'<text x="150" y="484" font-size="12" fill="{MUTED}">AI and write-ups</text>',
          f'<rect x="270" y="472" width="14" height="14" rx="3" fill="none" stroke="{GREEN}" stroke-width="2"/>',
          f'<text x="290" y="484" font-size="12" fill="{MUTED}">safety check</text>', "</svg>"]
    write("pipeline.svg", "\n".join(s))


def results():
    truth = json.load(open(os.path.join(ROOT, "eval", "answer_key", "ground_truth.json")))
    flagged = [r for r in __import__("csv").DictReader(open(os.path.join(ROOT, "reports", "flagged.csv")))]
    ev = run_eval.evaluate(flagged, truth, 25)["Combined list"]
    honest_flagged = ev["hard_neg_flagged"] + ev["normal_flagged"]
    runs = []
    for label, rel in (("AI summaries (chat),\nno records evidence", "experiments/cold_agent_25_rerun/summaries_checked.jsonl"),
                       ("AI summaries (chat),\nwith records evidence*", "experiments/cold_agent_25_docs/summaries_checked.jsonl"),
                       ("Live API run,\nwith records evidence*", "reports/live/case_summaries_checked.jsonl")):
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
    recs = {json.loads(l)["provider_id"]: json.loads(l) for l in open(os.path.join(ROOT, "experiments", "cold_agent_25_docs", "summaries_checked.jsonl"))}
    rec = recs[pid]["summary"]
    d = os.path.join(ROOT, "data", "synthetic")
    chronic, age, cond, claims = cs.load(d)
    docs = cs.load_docs(d)
    import csv
    fl = {r["provider_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "reports", "flagged.csv")))}
    pk = cs.build_packet(pid, fl[pid], chronic, age, cond, claims, cs.peer_rates(claims, chronic), docs, cs.doc_peer_rates(claims, docs))
    unsup = next(t for t in pk["documentation_review"]["by_billed_level"] if t["billed_cpt"] == "99215")
    chart = open(os.path.join(ROOT, "reports", "charts", f"{pid}.svg")).read()
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
    recs = run_eval.load_checked(os.path.join(ROOT, "reports", "live", "case_summaries_checked.jsonl"))
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
    funnel()
    print("results:", results())
    case_card()
    print("figures written to docs/images/")
