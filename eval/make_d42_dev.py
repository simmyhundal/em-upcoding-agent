"""Build data 4.2 development seeds (issue 173): code runs d42_<seed>. Free (no model). The test and reserved pools are never built here; the confirm pool only with --confirm.
Usage: python eval/make_d42_dev.py [--confirm] [--first N] [seed ...]      (no seeds: the first 20 development seeds, or all 100 with --first 100)"""
import multiprocessing as mp
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v42 as pool  # noqa: E402
import make_v2_runs as mk  # noqa: E402
import run_release2 as r2  # noqa: E402

NOTE = "data 4.2 seed {s} (issue 173): 216 providers, a continuous net rate for every provider, habits by rate, fraud/waste/abuse kinds, no planted role"


def build(seed):
    assert seed in pool.DEV or seed in pool.CONFIRM, f"seed {seed} is not in a buildable data 4.2 pool (test and reserved pools are never generated)"
    code = f"d42_{seed}"
    if not r2.done(code, "README.md"):
        mk.run((code, seed, 216, 0, 0, None, NOTE.format(s=seed)), data_version="4.2", screens=("eb_ratio",))
    return code


if __name__ == "__main__":
    args = sys.argv[1:]
    confirm = "--confirm" in args
    first = 20
    if "--first" in args:
        k = args.index("--first")
        first = int(args[k + 1])
        args = args[:k] + args[k + 2:]
    seeds = [int(a) for a in args if a.isdigit()] or (pool.CONFIRM[:first] if confirm else pool.DEV[:first])
    with mp.get_context("spawn").Pool(4) as p:
        print(p.map(build, seeds, chunksize=1))
