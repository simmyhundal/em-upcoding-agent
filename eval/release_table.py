"""The README's second results table: workflow v2.2 and v2.3 and agent v3.2 and v3.3 on data 2.2 (releases 2 and 3), rendered from experiments/release23_table.json.

The JSON is written by `python eval/release_table.py --compute [--key-root PATH]` from the saved run folders and the (gitignored) answer keys, and committed, the way
experiments/results.csv is; the README block is rendered from the JSON so it cannot drift from it (tests/test_release_table.py).
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "experiments", "release23_table.json")
R2 = [1515, 1616, 1717, 1818, 1919, 2020, 2121, 2222, 2323, 2424]
R3 = [2525, 2626, 2727, 2828, 2929, 3030, 3131, 3232, 3333, 3434]
# (row label, seed set, code run prefix, run prefix)
ROWS = [("Workflow v2.2", "release 2 seeds", "r2", "r2w", R2), ("Agent v3.2", "release 2 seeds", "r2", "r2a", R2),
        ("Workflow v2.2", "release 3 seeds", "r3", "r3w2", R3), ("Workflow v2.3", "release 3 seeds", "r3", "r3w", R3), ("Agent v3.3", "release 3 seeds", "r3", "r3a", R3)]


def compute(key_root=ROOT):
    out = []
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
    json.dump(out, open(PATH, "w"), indent=1)
    return out


def rows():
    return json.load(open(PATH))


def markdown():
    r = rows()
    lines = ["| Arm | Seeds | Upcoders found | Honest practices accused | Honest practices asked for charts | Requests and follow-ups sent to practices |", "|---|---|---|---|---|---|"]
    for x in r:
        lines.append(f"| {x['arm']} | {x['seeds']} | {x['found']} of {x['upcoders']} | {x['accused']} | {x['asked']} | {x['requests']} |")
    lines += ["", "Harder data (honest coding noise, group billing, data defects), ten seeds in each set, 8 planted upcoders each. The release 2 comparison was an unplanned ten-seed look, so it "
              "carries no significance claim; on the later pre-registered ten seeds workflow v2.3 and agent v3.3 are not significantly different. "
              "Details: [release 2](docs/release2_results.md), [release 3](docs/release3_results.md)."]
    return "\n".join(lines)


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
