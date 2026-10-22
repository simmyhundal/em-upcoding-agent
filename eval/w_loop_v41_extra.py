"""Side statistics for the workflow v4.1 hypotheses (issue 132): what the extra requests did. Free; reads stored run folders only."""
import json
import os
import statistics as st
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v4 as pool  # noqa: E402


def probe_stats(name, seeds):
    asked = ext = blocked = called = hi_small = n_hi = 0
    for s in seeds:
        d = os.path.join(ROOT, "experiments", f"wl{name.lower()}_{s}")
        pl = json.load(open(os.path.join(d, "probe_log.json"))) if os.path.exists(os.path.join(d, "probe_log.json")) else {}
        asked += len(pl)
        ext += sum(v["extended"] for v in pl.values())
        blocked += sum(v["blocked"] for v in pl.values())
        n_hi += sum(v["n_hi"] for v in pl.values())
        called += sum(1 for x in open(os.path.join(d, "case_summaries_checked.jsonl")) if json.loads(x)["summary"]["leaning"] == "pattern_consistent_with_upcoding" and json.loads(x)["provider_id"] in pl)
    return {"asked": asked, "extended": ext, "blocked": blocked, "called_before_floor_or_after": called, "mean_hi_charts_at_probe": n_hi / max(asked, 1)}


def withdrawn(name, seeds):
    w = 0
    for s in seeds:
        p = os.path.join(ROOT, "experiments", f"wl{name.lower()}_{s}", "demand_floor.json")
        if os.path.exists(p):
            w += len(json.load(open(p))["withdrawn"])
    return w


if __name__ == "__main__":
    name = sys.argv[1]
    for tag, b in (("B1-4", range(1, 5)), ("B5-6", range(5, 7))):
        seeds = sum([pool.BATCHES[i - 1] for i in b], [])
        print(tag, probe_stats(name, seeds), "withdrawn by floor", withdrawn(name, seeds))
