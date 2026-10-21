"""The data 4.0 development pool for the workflow's RL loop (issue to be linked): 100 seeds in ten batches of ten, plus seed 42 kept as a smoke seed.

Batch 1 is the ten seeds already built for issues 124 to 127 (1515, 1616, ..., 2424). Batches 2 to 10 are 90 new seeds 3000, 3021, ..., 4869 (step 21), none of them 5555 or above:
**fresh seeds start at 5555 in steps of 101 and are never built, run or tuned on here.** Free (code runs only). Usage: python eval/dev_pool_v4.py [--build] [BATCH ...]"""
import multiprocessing as mp
import sys

import make_d4_dev as md

BATCH1 = list(range(1515, 2425, 101))
NEW = [3000 + 21 * j for j in range(90)]
BATCHES = [BATCH1] + [NEW[i:i + 10] for i in range(0, 90, 10)]
SMOKE = 42
assert all(s < 5555 for b in BATCHES for s in b) and len({s for b in BATCHES for s in b}) == 100


def seeds(upto):
    """Seeds of batches 1 .. upto (1-based)."""
    return [s for b in BATCHES[:upto] for s in b]


if __name__ == "__main__":
    which = [int(a) for a in sys.argv[1:] if a.isdigit()] or list(range(1, 11))
    todo = [s for b in which for s in BATCHES[b - 1]]
    if "--build" in sys.argv:
        with mp.get_context("spawn").Pool(3) as pool:
            print(pool.map(md.build, todo, chunksize=1))
    else:
        for i, b in enumerate(BATCHES, 1):
            print(i, b)
