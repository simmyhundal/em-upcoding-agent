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
V41_PATH = os.path.join(ROOT, "experiments", "v41_fresh_results.json")
V51_PATH = os.path.join(ROOT, "experiments", "v51_fresh_results.json")
V42_PATH = os.path.join(ROOT, "experiments", "v42_test_results.json")
V42_ARMS = [("W4.1", "Workflow v4.1"), ("W4.2", "Workflow v4.2"), ("A5.2", "Agent v5.2")]       # ten data 4.2 test seeds (4700 + 37j), score 4.2; W4.1 re-run on them
V4_ARMS = [("W2.5 (frozen)", "Workflow v2.5", V4_PATH), ("W4.0", "Workflow v4.0", V4_PATH), ("A5.0", "Agent v5.0", V4_PATH),
           ("W4.1 (H23, list 4)", "Workflow v4.1", V41_PATH), ("A5.1", "Agent v5.1", V51_PATH)]


def arm_results(key):
    """Per-seed results of one arm on the ten test seeds (5555 to 6464) from the results file that holds it."""
    for k, _, path in V4_ARMS:
        if k == key:
            return json.load(open(path))[key]
    raise KeyError(key)


def v4_rows():
    """Workflow v2.5 (frozen), workflow v4.0, agent v5.0, workflow v4.1 and agent v5.1 on the ten data 4.0 test seeds (5555 to 6464), scored by score 4.0 (docs/score_40.md), from experiments/v4_fresh_results.json,
    v41_fresh_results.json and v51_fresh_results.json."""
    out = []
    for key, label, _ in V4_ARMS:
        v = list(arm_results(key).values())
        out.append({"arm": label, "seeds": "data 4.0 seeds", "found": sum(x["found"] for x in v), "upcoders": sum(x["upcoders"] for x in v),
                    "accused": sum(x["honest_called"] for x in v), "net_per_seed": round(sum(x["score"] for x in v) / len(v)), "net_total": sum(x["score"] for x in v)})
    return out


def v42_rows():
    """Workflow v4.1 (re-run), workflow v4.2 and agent v5.2 on the ten data 4.2 test seeds, scored by score 4.2 (docs/score_42.md). On data 4.2 nothing is planted: `upcoders` is the number of providers
    whose true overpayment is at least the cost of pursuing them (m = 1) and `found` the ones sent a demand."""
    res = json.load(open(V42_PATH))
    out = []
    for key, label in V42_ARMS:
        v = list(res[key].values())
        out.append({"arm": label, "seeds": "data 4.2 seeds", "found": sum(x["justified_called"] for x in v), "upcoders": sum(x["justified"] for x in v), "accused": sum(x["demands"] - x["justified_called"] for x in v),
                    "net_per_seed": round(sum(x["score"] for x in v) / len(v)), "net_total": sum(x["score"] for x in v), "lane": sum(x["lane_demands"] for x in v), "impossible": sum(x["impossible_providers"] for x in v)})
    return out


CHECK_PATH = os.path.join(ROOT, "experiments", "score_40_check.json")
CHECK_KEY = {("Workflow v2.2", "release 2 seeds"): ("r2", "W2.2"), ("Agent v3.2", "release 2 seeds"): ("r2", "A3.2"), ("Workflow v2.2", "release 3 seeds"): ("r3", "W2.2"),
             ("Workflow v2.3", "release 3 seeds"): ("r3", "W2.3"), ("Agent v3.3", "release 3 seeds"): ("r3", "A3.3"), ("Workflow v2.4", "release 4 seeds"): ("r4", "GL"),
             ("Agent v3.4", "release 4 seeds"): ("r4", "A3.4"), ("Workflow v2.5", "release 5 seeds"): ("r5", "W2.5"), ("Agent v3.5", "release 5 seeds"): ("r5", "A3.5")}


def stored_scores(arm, seeds_label):
    """(score 2.5, score 4.0), dollars summed over the ten seeds, recomputed from the stored run folders of releases 2 to 5 (experiments/score_40_check.json, eval/score_40_check.py), so a row's
    recall, precision and both scores all come from the same runs. None for rows without such a check."""
    key = CHECK_KEY.get((arm, seeds_label))
    if not key:
        return None
    rs = [r for r in json.load(open(CHECK_PATH)) if "base" in r and (r["set"], r["arm"]) == key]
    return sum(r["r5_net"] for r in rs), sum(r["base"]["score"] for r in rs)


def dollars(x):
    return "n/a" if x is None else f"-${-round(x):,}" if round(x) < 0 else f"${round(x):,}"


TABLE_ROWS = [("Workflow v2.5", "release 5 seeds", "2.2, release 5"), ("Agent v3.5", "release 5 seeds", "2.2, release 5")]


def r1_total(arm):
    import dollar_reward as dr
    code = {"Workflow v2.1": "W2.1", "Agent v3.1": "A3.1"}[arm]
    rs = [x for x in json.load(open(os.path.join(ROOT, "experiments", "release5_dollar_results.json"))) if x["set"] == "r1" and x["arm"] == code]
    return dr.net(dr.add(rs))


def markdown():
    """Three sets of rows: v2.1 and v3.1 (release 1), v2.5 and v3.5 (release 5), v2.5, v4.0 and v5.0 (data 4.0). Dollars are summed over each set's ten seeds."""
    d = {(x["arm"], x["seeds"]): x for x in rows()}
    from scoreboard import pct
    gl = "docs/glossary.md#results-columns"
    hov = lambda text, tip: f'[{text}]({gl} "{tip}")'
    lines = ["| Version | " + hov("Data, seeds", "Data version and the ten seeds. Compare rows within one data and seed set.")
             + " | " + hov("Upcoders found (recall)", "Planted upcoders found.") + " | " + hov("Calls that were upcoders (precision)", "Calls that were upcoders.")
             + " | " + hov("Score 2.5", "Release 5's score: the overpayment a sample supports (90% lower bound) minus request, review and false-accusation costs. Sum over ten seeds. Applied to release 1 after the fact.")
             + " | " + hov("Score 4.0", "Recovery minus staff-hours cost minus provider abrasion (docs/score_40.md). Sum over ten seeds.")
             + " | " + hov("Score 4.2", "Score 4.0 with no copy fee, a visit the office has no record of counted as overpaid, and fraud included (docs/score_42.md). Sum over ten seeds.") + " |", "|---|---|---|---|---|---|---|"]
    for arm, seeds, label in TABLE_ROWS:
        x = d[(arm, seeds)]
        sc = stored_scores(arm, seeds)
        s25, s40 = sc if sc else (r1_total(arm), None)
        lines.append(f"| {arm} | {label} | {pct(x['found'], x['upcoders'])} | {pct(x['found'], x['found'] + x['accused'])} | {dollars(s25)} | {dollars(s40)} | n/a |")
    for x in v4_rows():
        if x["arm"] in ("Workflow v2.5", "Workflow v4.0", "Agent v5.0"):         # their rows are in docs/v4_v5_results.md; the README keeps the table short (7,000-character cap)
            continue
        label = x["arm"]
        lines.append(f"| {label} | 4.0, test | {pct(x['found'], x['upcoders'])} | {pct(x['found'], x['found'] + x['accused'])} | n/a | {dollars(x['net_total'])} | n/a |")
    for x in v42_rows():
        lines.append(f"| {x['arm']} | 4.2, test | {pct(x['found'], x['upcoders'])} | {pct(x['found'], x['found'] + x['accused'])} | n/a | n/a | {dollars(x['net_total'])} |")
    lines += ["", "Hover over a column title for its definition ([glossary](docs/glossary.md#results-columns)). Every run and release: [results](docs/results.md), [release 1](docs/eval61.md), [5](docs/release5_results.md), [v4.0 and v5.0](docs/v4_v5_results.md), [v4.1](docs/w41_fresh_result.md), [v5.1](docs/a51_fresh_result.md), [v4.2 and v5.2](docs/v42_test_result.md)."]
    return "\n".join(lines)


def score_parts_42(arm):
    """Totals over the ten data 4.2 test seeds for one arm of experiments/v42_test_results.json, the staff cost split by activity at score 4.2's prices (src/recovery_42.py)."""
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import recovery_42 as r42
    p = r42.params42()
    m = p["MINUTES"]
    import recovery_40 as r
    v = list(json.load(open(V42_PATH))[arm].values())
    S = lambda f: sum(x[f] for x in v)
    charts = S("charts") * m["coder_per_chart"] / 60 * r.hourly("coder", p)
    admin = S("rounds") * (m["admin_per_round"] / 60 * r.hourly("admin", p) + p["C_COPY"])
    demand = S("demands") * (m["investigator_per_demand"] / 60 * r.hourly("investigator", p) + m["nurse_per_demand"] / 60 * r.hourly("nurse", p))
    return {"n": len(v), "recovery": S("recovered"), "recovery_lane": S("recovered_fwa"), "staff": S("staff_cost"), "abrasion": S("abrasion"), "score": S("score"), "found": S("justified_called"), "upcoders": S("justified"),
            "demands": S("demands"), "lane_demands": S("lane_demands"), "rounds": S("rounds"), "charts_n": S("charts"), "charts": charts, "admin": admin, "demand": demand, "triage": S("staff_cost") - charts - admin - demand}


def score_parts(arm):
    """Totals over the ten fresh seeds for one arm of experiments/v4_fresh_results.json, with the staff cost split by activity (src/recovery_40.py prices)."""
    sys.path.insert(0, os.path.join(ROOT, "src"))
    import recovery_40 as r
    p = r.params()
    m = p["MINUTES"]
    v = list(arm_results(arm).values())
    S = lambda f: sum(x[f] for x in v)
    charts = S("charts") * m["coder_per_chart"] / 60 * r.hourly("coder", p)
    admin = S("rounds") * (m["admin_per_round"] / 60 * r.hourly("admin", p) + p["C_COPY"])
    demand = S("demands") * (m["investigator_per_demand"] / 60 * r.hourly("investigator", p) + m["nurse_per_demand"] / 60 * r.hourly("nurse", p))
    return {"n": len(v), "recovery": S("recovered"), "staff": S("staff_cost"), "abrasion": S("abrasion"), "score": S("score"), "found": S("found"), "upcoders": S("upcoders"),
            "demands": S("demands"), "rounds": S("rounds"), "charts_n": S("charts"), "charts": charts, "admin": admin, "demand": demand, "triage": S("staff_cost") - charts - admin - demand}


def score_text(arm="A5.2"):
    """The README's three bullets under the score chart, dollars summed over the ten test seeds (experiments/v4_fresh_results.json, v41_ and v51_fresh_results.json)."""
    w = score_parts_42(arm) if arm in dict(V42_ARMS) else score_parts(arm)
    f = lambda x: f"${x:,.0f}"
    if arm in dict(V42_ARMS):
        return (f"- **Recovery +{f(w['recovery'])}:** {f(w['recovery_lane'])} of it from the visits-per-day check ({w['lane_demands']} of its demands), the rest from reviewing billing levels; {w['demands']} demands in all.\n"
                f"- **Staff cost -{f(w['staff'])}:** chart review {f(w['charts'])} ({w['charts_n']} charts), requests {f(w['admin'])} ({w['rounds']} rounds), demand work {f(w['demand'])}, triage and model dollars {f(w['triage'])}.\n"
                f"- **Abrasion -{f(w['abrasion'])}:** the cost to providers of requests and demands, weighted by how little they overbilled.\n"
                f"- **Net score {dollars(w['score'])}** over ten seeds.")
    return (f"- **Recovery +{f(w['recovery'])}:** {w['found']} of {w['upcoders']} upcoders found, {w['demands']} demands, about {f(w['recovery'] / max(w['demands'], 1))} recovered per demand.\n"
            f"- **Staff cost -{f(w['staff'])}:** chart review {f(w['charts'])} ({w['charts_n']} charts), requests and copy fees {f(w['admin'])} ({w['rounds']} rounds), demand work {f(w['demand'])}, triage and model dollars {f(w['triage'])}.\n"
            f"- **Abrasion -{f(w['abrasion'])}:** the cost to providers of requests and demands; no honest provider was demanded from.\n"
            f"- **Net score {dollars(w['score'])}** over ten seeds.")


def tldr():
    """The README's summary, rendered from experiments/v4_fresh_results.json (data 4.0), release5_results.json (release 5) and v42_test_results.json (data 4.2, ten test seeds, score 4.2, summed)."""
    w25, w40, a50, w41, a51 = v4_rows()
    w41b, w42, a52 = v42_rows()
    lane = score_parts_42("W4.2")
    return (f"On data 4.0 (ten test seeds, score 4.0) the old workflow v2.5 scores {dollars(w25['net_total'])}; "
            f"workflow v4.1 ({dollars(w41['net_total'])}) and agent v5.1 ({dollars(a51['net_total'])}) find {w41['found']} and {a51['found']} of {w41['upcoders']} upcoders, but one seed carries each total. "
            f"Data 4.2 adds fraud. On ten new test seeds workflow v4.1 scores {dollars(w41b['net_total'])}; workflow v4.2 ({dollars(w42['net_total'])}) and agent v5.2 ({dollars(a52['net_total'])}) add a check on visits billed per day, "
            f"which gives {round(100 * lane['recovery_lane'] / lane['recovery'])}% of their recovery. That signal is clean by construction in the synthetic data: read the gain as what a reviewer does with a clean signal, not as a forecast for real claims.")


def headline_cells():
    """Short per-version results for the progression slide: {"v4.1": text, "v5.1": text}."""
    w25, w40, a50, w41, a51 = v4_rows()
    w41b, w42, a52 = v42_rows()
    return {"v4.2": f"Data 4.2, ten test seeds: {w42['lane']} of {w42['impossible']} providers billing impossible visits per day demanded from, {dollars(w42['net_total'])} in all (v4.1: {dollars(w41b['net_total'])}).",
            "v5.2": f"Agent, same seeds: {a52['lane']} of {a52['impossible']} such providers demanded from, {dollars(a52['net_total'])} in all."}


if __name__ == "__main__":
    if "--compute" in sys.argv:
        kr = sys.argv[sys.argv.index("--key-root") + 1] if "--key-root" in sys.argv else ROOT
        print(json.dumps(compute(kr), indent=1))
    else:
        print(markdown())
