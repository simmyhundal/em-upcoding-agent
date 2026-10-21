"""The README's second results table: workflow v2.2 to v2.5 and agent v3.2 to v3.5 on data 2.2 (releases 2 to 5), rendered from experiments/release23_table.json.

The table now starts with the four release 1 versions (from experiments/results.csv) and every row carries net dollars per seed (the release 5 score: experiments/release5_dollar_results.json,
experiments/release5_results.json). The JSON is written by `python eval/release_table.py --compute [--key-root PATH]` from the saved run folders and the (gitignored) answer keys, and committed, the way
experiments/results.csv is; the README block is rendered from the JSON so it cannot drift from it (tests/test_release_table.py).
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "eval"))
PATH = os.path.join(ROOT, "experiments", "release23_table.json")
R2 = [1515, 1616, 1717, 1818, 1919, 2020, 2121, 2222, 2323, 2424]
R3 = [2525, 2626, 2727, 2828, 2929, 3030, 3131, 3232, 3333, 3434]
R4 = [3535, 3636, 3737, 3838, 3939, 4040, 4141, 4242, 4343, 4444]
R5 = [4545, 4646, 4747, 4848, 4949, 5050, 5151, 5252, 5353, 5454]
# (row label, seed set, code run prefix, run prefix)
ROWS = [("Workflow v2.2", "release 2 seeds", "r2", "r2w", R2), ("Agent v3.2", "release 2 seeds", "r2", "r2a", R2),
        ("Workflow v2.2", "release 3 seeds", "r3", "r3w2", R3), ("Workflow v2.3", "release 3 seeds", "r3", "r3w", R3), ("Agent v3.3", "release 3 seeds", "r3", "r3a", R3),
        ("Workflow v2.4", "release 4 seeds", "r4", "r4gl", R4), ("Agent v3.4", "release 4 seeds", "r4", "r4a", R4),
        ("Workflow v2.5", "release 5 seeds", "r5", "r5w25", R5), ("Agent v3.5", "release 5 seeds", "r5", "r5a", R5)]


DOLLAR_SET = {"release 2 seeds": "r2", "release 3 seeds": "r3", "release 4 seeds": "r4"}
DOLLAR_ARM = {"Workflow v2.2": "W2.2", "Agent v3.2": "A3.2", "Workflow v2.3": "W2.3", "Agent v3.3": "A3.3", "Workflow v2.4": "GL", "Agent v3.4": "A3.4"}
R5_ARM = {"Workflow v2.5": "W2.5", "Agent v3.5": "A3.5", "Workflow v2.3": "W2.3"}
R1 = [("Workflow v2.0", 0, "W2.0"), ("Workflow v2.1", 1, "W2.1"), ("Agent v3.0", 2, "A3.0"), ("Agent v3.1", 3, "A3.1")]


def net_per_seed(seeds_label, arm):
    """Net dollars per seed (eval/dollar_reward.py: option 2, 90% lower bound) for one table row."""
    import dollar_reward as dr
    if seeds_label == "release 5 seeds":
        per = json.load(open(os.path.join(ROOT, "experiments", "release5_results.json")))[R5_ARM[arm]]["per_seed"]
        return sum(per) / len(per)
    key = {"release 1 seeds": "r1"}.get(seeds_label) or DOLLAR_SET[seeds_label]
    name = DOLLAR_ARM.get(arm) or dict((a, c) for a, _, c in R1)[arm]
    rows = [r for r in json.load(open(os.path.join(ROOT, "experiments", "release5_dollar_results.json"))) if r["set"] == key and r["arm"] == name]
    return dr.net(dr.add(rows)) / len(rows)


def release1_rows():
    import scoreboard
    rows = scoreboard.read_csv(scoreboard.CSV_PATH)
    out = []
    for label, i, _ in R1:
        a = scoreboard._arm(rows, scoreboard.ARMS[i][1], scoreboard.ARMS[i][2])
        out.append({"arm": label, "seeds": "release 1 seeds", "found": a["found"], "upcoders": a["of"], "accused": a["accused"], "asked": a["asked"], "requests": a["rounds"]})
    return out


def compute(key_root=ROOT):
    out = release1_rows()
    for label, which, code, pre, seeds in ROWS:
        found = up = honest = asked = rounds = 0
        for s in seeds:
            key = json.load(open(os.path.join(key_root, "eval", "answer_key", f"ground_truth_v2_{code}_{s}.json")))["providers"]
            roles = {p for p, v in key.items() if v["role"] == "upcoder"}
            called = {x["provider_id"] for x in map(json.loads, open(os.path.join(ROOT, "experiments", f"{pre}_{s}", "case_summaries_checked.jsonl")))
                      if x["summary"]["leaning"] == "pattern_consistent_with_upcoding"}
            found, up, honest = found + len(called & roles), up + len(roles), honest + len(called - roles)
            seen = set()
            for line in open(os.path.join(ROOT, "experiments", f"{pre}_{s}", "office_transcript.jsonl")):
                e = json.loads(line)
                if e.get("action") in ("send_request", "follow_up") and "error" not in e:
                    rounds += 1
                    if e["provider_id"] not in roles:
                        seen.add(e["provider_id"])
            asked += len(seen)
        out.append({"arm": label, "seeds": which, "found": found, "upcoders": up, "accused": honest, "asked": asked, "requests": rounds})
    for r in out:
        r["net_per_seed"] = round(net_per_seed(r["seeds"], r["arm"]))
    json.dump(out, open(PATH, "w"), indent=1)
    return out


def rows():
    return json.load(open(PATH))


V4_PATH = os.path.join(ROOT, "experiments", "v4_fresh_results.json")
V4_ARMS = [("W2.5 (frozen)", "Workflow v2.5"), ("W4.0", "Workflow v4.0"), ("A5.0", "Agent v5.0")]


def v4_rows():
    """Workflow v2.5 (frozen), workflow v4.0 and agent v5.0 on the ten fresh data 4.0 seeds (5555 to 6464), scored by score 4.0 (docs/score_40.md), from experiments/v4_fresh_results.json."""
    d = json.load(open(V4_PATH))
    out = []
    for key, label in V4_ARMS:
        v = list(d[key].values())
        out.append({"arm": label, "seeds": "data 4.0 seeds", "found": sum(x["found"] for x in v), "upcoders": sum(x["upcoders"] for x in v),
                    "accused": sum(x["honest_called"] for x in v), "net_per_seed": round(sum(x["score"] for x in v) / len(v))})
    return out


def markdown():
    r = rows()
    from scoreboard import pct
    gl = "docs/glossary.md#results-columns"
    hov = lambda text, tip: f'[{text}]({gl} "{tip}")'
    lines = ["| Version | " + hov("Data model", "Easy: release 1, clean coding and planted clone signs. Hard: releases 2 to 5, adds coding noise, group billing, lagged claims and data defects. Data 4.0: every provider has a true upcoding rate and 8 have a habit.")
             + " | " + hov("Upcoders found (recall)", "Upcoders found out of those planted.") + " | " + hov("Calls that were upcoders (precision)", "Upcoders found out of all providers called upcoding.")
             + " | " + hov("Net $ per seed (RL score)", "Overpayment a records sample supports (90% lower bound) minus costs. Compare rows within one seed set only. The last three rows use score 4.0, which also charges staff time.") + " |", "|---|---|---|---|---|"]
    names = [x["arm"] for x in r]
    for x in r:
        model = "Easy" if x["seeds"] == "release 1 seeds" else "Hard"
        label = f"{x['arm']} ({x['seeds'].replace(' seeds', '')})" if names.count(x["arm"]) > 1 else x["arm"]       # the same version in two releases' seed sets
        lines.append(f"| {label} | {model} | {pct(x['found'], x['upcoders'])} | {pct(x['found'], x['found'] + x['accused'])} | ${x['net_per_seed']:,} |")
    lines += ["| **Score 4.0 on data 4.0 (fresh seeds)** | | | | |"]
    for x in v4_rows():
        label = f"{x['arm']} (frozen, for reference)" if x["arm"] == "Workflow v2.5" else x["arm"]
        lines.append(f"| {label} | Data 4.0 | {pct(x['found'], x['upcoders'])} | {pct(x['found'], x['found'] + x['accused'])} | -${-x['net_per_seed']:,} |")
    lines += ["", "Hover over a column title for its definition ([glossary](docs/glossary.md#results-columns)). Compare rows within one seed set only: "
              "releases [1](docs/eval61.md), [2](docs/release2_results.md), [3](docs/release3_results.md), [4](docs/release4_results.md), [5](docs/release5_results.md), [v4.0 and v5.0](docs/v4_v5_results.md); [every run](docs/results.md)."]
    return "\n".join(lines)


def score_parts(arm):
    """Totals over the ten fresh seeds for one arm of experiments/v4_fresh_results.json, with the staff cost split by activity (src/recovery_40.py prices)."""
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import recovery_40 as r
    p = r.params()
    m = p["MINUTES"]
    v = list(json.load(open(V4_PATH))[arm].values())
    S = lambda f: sum(x[f] for x in v)
    charts = S("charts") * m["coder_per_chart"] / 60 * r.hourly("coder", p)
    admin = S("rounds") * (m["admin_per_round"] / 60 * r.hourly("admin", p) + p["C_COPY"])
    demand = S("demands") * (m["investigator_per_demand"] / 60 * r.hourly("investigator", p) + m["nurse_per_demand"] / 60 * r.hourly("nurse", p))
    return {"n": len(v), "recovery": S("recovered"), "staff": S("staff_cost"), "abrasion": S("abrasion"), "score": S("score"), "found": S("found"), "upcoders": S("upcoders"),
            "demands": S("demands"), "rounds": S("rounds"), "charts_n": S("charts"), "charts": charts, "admin": admin, "demand": demand, "triage": S("staff_cost") - charts - admin - demand}


def score_text(arm="A5.0"):
    """The README's three bullets under the score chart: what is behind each term, dollars per seed, from experiments/v4_fresh_results.json."""
    w = score_parts(arm)
    n = w["n"]
    f = lambda x: f"${x / n:,.0f}"
    return (f"- **Recovery +{f(w['recovery'])}:** {w['found']} of {w['upcoders']} upcoders found in all ten seeds, {w['demands']} demands, about ${w['recovery'] / max(w['demands'], 1):,.0f} recovered per demand.\n"
            f"- **Staff cost -{f(w['staff'])}:** chart review {f(w['charts'])}, requests and copy fees {f(w['admin'])}, demand work {f(w['demand'])}, triage and model dollars {f(w['triage'])}.\n"
            f"- **Abrasion -{f(w['abrasion'])}:** the cost to providers of requests and demands, weighted down for providers that really upcode; no honest provider was demanded from.")


def tldr():
    """The README's TL;DR, rendered from experiments/v4_fresh_results.json (ten fresh data 4.0 seeds, score 4.0) and experiments/release5_results.json (release 5)."""
    w25, w40, a50 = v4_rows()
    d = json.load(open(os.path.join(ROOT, "experiments", "release5_results.json")))
    net = {k: sum(v["per_seed"]) / len(v["per_seed"]) for k, v in d.items()}
    return (f"A fixed workflow and an AI agent both screen providers, request charts and draft cases for PI teams. On the old data (release 5), both earned about ${net['A3.5'] / 1000:.0f}k net per seed and found under half of the upcoders. "
            f"Data 4.0 and score 4.0 are harder and honest about staff time: on ten fresh seeds, the old workflow loses ${-w25['net_per_seed']:,} per seed, while the new workflow (v4.0) loses ${-w40['net_per_seed']:,} "
            f"and the new agent (v5.0) ${-a50['net_per_seed']:,}. Each finds {w40['found']} of {w40['upcoders']} upcoders and accuses no honest provider. "
            "Both are far better than before and still not above zero.")


def headline_cells():
    """Short per-version results for the progression slide: {"v4.0": text, "v5.0": text}."""
    w25, w40, a50 = v4_rows()
    return {"v4.0": f"Data 4.0, ten fresh seeds: {w40['found']} of {w40['upcoders']} found, {w40['accused']} honest accused, -${-w40['net_per_seed']:,} per seed (v2.5: -${-w25['net_per_seed']:,}).",
            "v5.0": f"Agent, same data 4.0 seeds: {a50['found']} of {a50['upcoders']} found, {a50['accused']} honest accused, -${-a50['net_per_seed']:,} per seed."}


if __name__ == "__main__":
    if "--compute" in sys.argv:
        kr = sys.argv[sys.argv.index("--key-root") + 1] if "--key-root" in sys.argv else ROOT
        print(json.dumps(compute(kr), indent=1))
    else:
        print(markdown())
