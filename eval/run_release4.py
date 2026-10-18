"""Release 4 fresh test harness (issue 108): workflow v2.3 (reference) against three workflow v2.4 variants on the same fresh seed. Workflow only (about $0.01 a seed); the agent
is not part of this test. Data 2.2, 216 doctors, 8 planted upcoders, 8 hard negatives, half clone notes; seeds 3535, 3636, ..., 4444 (step 101).

  W23  workflow v2.3 as released (eb_ratio_t top 10%, hand-set two-tier policy, rules 2.3)
  G    v2.3 with the light tier gated at ratio >= 2.5 (selected on issue 102)
  L    v2.3 with the learned stop-or-escalate formula (src/policy_24.json, lambda 0.05) after the first sample, on the whole list
  GL   both
Each step is skipped when its output exists. The seeds, arms and rule were posted on issue 108 before any seed was generated.

Usage: python eval/run_release4.py 3535
"""
import argparse
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

NOTE = "release 4 evaluation (issue 108): seed {s}, 216 doctors, 8 planted upcoders, half clone notes, data 2.2 defaults"
TIER1_N = 11
SEEDS = [3535, 3636, 3737, 3838, 3939, 4040, 4141, 4242, 4343, 4444]


def run_seed(seed, code=None, prefix="r4"):
    code = code or f"r4_{seed}"
    if not r2.done(code, "README.md"):
        mk.run((code, seed, 216, 8, 8, 0.5, NOTE.format(s=seed)), data_version="2.2", screens=("eb_ratio",))
        print("built", code, flush=True)
    name = dev.write_flagged(code, "eb_ratio_t", 10)
    out = {"seed": seed}
    for arm in ("W23", "G", "L", "GL"):
        rid = f"{prefix}{arm.lower()}_{seed}"
        if not r2.done(rid, "case_summaries_checked.jsonl"):
            if arm == "W23":
                ow.run(rid, code, name, NOTE.format(s=seed) + "; workflow v2.3", version="2.3", tier1_n=TIER1_N)
            else:
                ow.run(rid, code, name, NOTE.format(s=seed) + f"; workflow v2.4 variant {arm}", version="2.4", tier1_n=TIER1_N, policy24=p24.ARMS[arm])
        out[arm] = r2.score(rid, code)
    return out


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT, ".env"))
    ap = argparse.ArgumentParser()
    ap.add_argument("seed", type=int)
    ap.add_argument("--smoke-code", help="a development code run to use instead of generating a fresh seed (prefix r4smoke)")
    a = ap.parse_args()
    res = run_seed(a.seed, a.smoke_code, "r4smoke" if a.smoke_code else "r4")
    path = os.path.join(ROOT, "experiments", f"r4_results_{'smoke_' if a.smoke_code else ''}{a.seed}.json")
    json.dump(res, open(path, "w"), indent=1)
    print(json.dumps(res, indent=1))
