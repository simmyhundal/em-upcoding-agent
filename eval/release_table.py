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


def markdown():
    r = rows()
    from scoreboard import pct
    lines = ["| Version | Data model | Upcoders found (recall) | Calls that were upcoders (precision) | Net $ per seed |", "|---|---|---|---|---|"]
    for x in r:
        model = "Easy" if x["seeds"] == "release 1 seeds" else "Hard"
        lines.append(f"| {x['arm']} | {model} | {pct(x['found'], x['upcoders'])} | {pct(x['found'], x['found'] + x['accused'])} | ${x['net_per_seed']:,} |")
    lines += ["", "**Data model.** Easy (release 1, data 2.1): clean coding, documentation generated from the true visit level, clone signs planted in notes. Hard (releases 2 to 5, data 2.2): adds honest coding noise "
              "(honest providers sometimes bill one level up), group billing and incident-to billing, truncated diagnoses, claims lag, corrections that change a level, and injected data defects. "
              "**Recall** is upcoders found out of those planted; **precision** is upcoders found out of all providers called upcoding. **Net $** is the overpayment a records sample supports for the "
              "upcoders found (90% lower bound) minus request and false-accusation costs, so compare rows within one seed set only. Each release has its own ten seeds: "
              "[1](docs/eval61.md), [2](docs/release2_results.md), [3](docs/release3_results.md), [4](docs/release4_results.md), [5](docs/release5_results.md); [every run](docs/results.md)."]
    return "\n".join(lines)


def tldr():
    """The README's TL;DR, rendered from experiments/release5_results.json (release 5 fresh test, ten seeds)."""
    d = json.load(open(os.path.join(ROOT, "experiments", "release5_results.json")))
    n = len(d["A3.5"]["per_seed"])
    net = {k: sum(v["per_seed"]) / n for k, v in d.items()}
    return (f"A fixed workflow and an AI agent both screen providers, request charts and draft cases for PI teams. On ten fresh seeds ({d['A3.5']['upcoders']} planted upcoders), the latest agent (v3.5) and workflow (v2.5) "
            f"each earn about ${net['A3.5'] / 1000:.0f}k net per seed and are not reliably different; the release 3 workflow earned ${net['W2.3'] / 1000:.0f}k on the same seeds. "
            f"The gain is lower cost (fewer requests and fewer false accusations), not more catches: each still finds under half of the upcoders ({d['W2.5']['found']} and {d['A3.5']['found']} of {d['A3.5']['upcoders']}), "
            "far from the 12.5% miss-rate target.")


def headline_cells():
    """Short per-version results for the progression slide: {"v2.3": text, "v3.3": text}."""
    d = {(x["arm"], x["seeds"]): x for x in rows()}
    w2, w3, a3 = d[("Workflow v2.2", "release 3 seeds")], d[("Workflow v2.3", "release 3 seeds")], d[("Agent v3.3", "release 3 seeds")]
    return {"v2.3": f"Harder data, ten later seeds: {w3['found']} of {w3['upcoders']} upcoders found, {w3['accused']} honest accused ({w2['found']} of {w2['upcoders']} for v2.2).",
            "v3.3": f"Same data and seeds: {a3['found']} of {a3['upcoders']} upcoders found, {a3['accused']} honest accused; not significantly different from v2.3."}


if __name__ == "__main__":
    if "--compute" in sys.argv:
        kr = sys.argv[sys.argv.index("--key-root") + 1] if "--key-root" in sys.argv else ROOT
        print(json.dumps(compute(kr), indent=1))
    else:
        print(markdown())
