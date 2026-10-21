"""Build the data 4.0 DEVELOPMENT seeds (issue 124): code runs d4_<seed> for seed 42 and 1515 to 2424 (step 101). Free (no model). Fresh seeds start at 5555 and are never built here.
Usage: python eval/make_d4_dev.py [seed ...]"""
import multiprocessing as mp
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import make_v2_runs as mk  # noqa: E402
import run_release2 as r2  # noqa: E402

SEEDS = [42] + list(range(1515, 2425, 101))
NOTE = "data 4.0 development seed {s} (issue 124): 216 providers, 8 planted upcoders with habits, 8 hard negatives, 1 cloner"


def build(seed):
    code = f"d4_{seed}"
    if not r2.done(code, "README.md"):
        mk.run((code, seed, 216, 8, 8, 0.125, NOTE.format(s=seed)), data_version="4.0", screens=("eb_ratio",))
    return code


if __name__ == "__main__":
    seeds = [int(a) for a in sys.argv[1:]] or SEEDS
    assert all(s < 5555 for s in seeds), "fresh seeds (5555 and above) are never built for development"
    with mp.Pool(4) as pool:
        print(pool.map(build, seeds))
