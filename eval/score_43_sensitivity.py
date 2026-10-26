"""Score 4.3 proposal: the README rows re-scored under the proposed defaults and one-at-a-time variants (free, from stored runs). Usage: python eval/score_43_sensitivity.py [--write]"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v42 as pool  # noqa: E402
import recovery_43 as r43  # noqa: E402
import score_42 as s42  # noqa: E402
import score_43 as s43  # noqa: E402
import yardstick_s42 as ys  # noqa: E402

VARIANTS = [("score 4.2 (reference, as in the README)", None),
            ("score 4.3 defaults", {}),
            ("  referral collection 85% (the payer recoups by offset itself)", {"COLLECTION_REFERRAL": 0.85}),
            ("  referral cost $2,000", {"REFERRAL_COST": 2000.0}),
            ("  referral cost $0 (as score 4.2)", {"REFERRAL_COST": 276.0}),
            ("  no appeal reduction", {"APPEAL_REDUCTION": 0.0}),
            ("  demand collection 55%", {"COLLECTION_DEMAND": 0.55}),
            ("  gate as score 4.2 (15% of claims)", {"GATE_UNIT": "claim"}),
            ("  no gate (0%)", {"GATE_DOLLAR_RATE": 0.0}),
            ("  copy fee $90", {"C_COPY": 90.0})]


def rows():
    out = []
    for arm, pre in ys.D40:
        out.append((arm, "4.0", [(f"{pre}_{s}", f"f4_{s}") for s in ys.D40_SEEDS]))
    for arm, pre in ys.D42:
        out.append((arm, "4.2", [((f"{pre}{s}" if pre.endswith("_") else f"{pre}_{s}"), f"d42_{s}") for s in pool.TEST]))
    return out


def run():
    res = {}
    for name, over in VARIANTS:
        res[name] = {}
        for arm, data, runs in rows():
            tot = 0.0
            for rid, code in runs:
                if over is None:
                    tot += (ys.s4.from_run(rid, code, ys.r42.params42())["score"] if data == "4.0" else s42.seed_result(rid, code)[0]["score"])
                else:
                    tot += s43.seed_result(rid, code, r43.params43(**over))[0]["score"]
            res[name][f"{arm} ({data})"] = round(tot)
    return res


if __name__ == "__main__":
    r = run()
    cols = list(next(iter(r.values())))
    print("| Variant | " + " | ".join(cols) + " |\n|---|" + "---|" * len(cols))
    for name, d in r.items():
        print(f"| {name} | " + " | ".join(f"${d[c]:,}" for c in cols) + " |")
    if "--write" in sys.argv:
        json.dump(r, open(os.path.join(ROOT, "experiments", "score_43_sensitivity.json"), "w"), indent=1)
