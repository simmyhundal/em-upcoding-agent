"""Release 5 fresh test harness (issue 109), workflow arms: W2.3 (reference), GL (v2.4 default) and W2.5 (learned ask-or-skip and escalation fitted on dollars, src/policy_25.json) on
the same fresh seed. Free (no model). Data 2.2, 216 doctors, 8 planted upcoders, 8 hard negatives, half clone notes; seeds 4545, 4646, ..., 5454 (step 101), posted on issue 109
before any was generated. Each step is skipped when its output exists.

Usage: python eval/run_release5.py 4545
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_release3 as dev  # noqa: E402
import make_v2_office_workflow_runs as ow  # noqa: E402
import make_v2_runs as mk  # noqa: E402
import run_release2 as r2  # noqa: E402
import workflow_policy_24 as p24  # noqa: E402

NOTE = "release 5 evaluation (issue 109): seed {s}, 216 doctors, 8 planted upcoders, half clone notes, data 2.2 defaults"
TIER1_N = 11
SEEDS = [4545, 4646, 4747, 4848, 4949, 5050, 5151, 5252, 5353, 5454]
ARMS = {"W23": ("r5w23", "2.3", None), "GL": ("r5gl", "2.4", p24.ARMS["GL"]), "W25": ("r5w25", "2.5", None)}


def build(seed):
    code = f"r5_{seed}"
    if not r2.done(code, "README.md"):
        mk.run((code, seed, 216, 8, 8, 0.5, NOTE.format(s=seed)), data_version="2.2", screens=("eb_ratio",))
        print("built", code, flush=True)
    return code, dev.write_flagged(code, "eb_ratio_t", 10)


def run_seed(seed):
    code, name = build(seed)
    out = {"seed": seed}
    for arm, (pre, version, opts) in ARMS.items():
        rid = f"{pre}_{seed}"
        if not r2.done(rid, "case_summaries_checked.jsonl"):
            ow.run(rid, code, name, NOTE.format(s=seed) + f"; workflow {arm}", version=version, tier1_n=TIER1_N, **({"policy24": opts} if opts is not None else {}))
        out[arm] = r2.score(rid, code)
    return out


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT, ".env"))
    res = run_seed(int(sys.argv[1]))
    json.dump(res, open(os.path.join(ROOT, "experiments", f"r5_results_{sys.argv[1]}.json"), "w"), indent=1)
    print(json.dumps(res, indent=1))
