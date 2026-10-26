"""The data 4.3 seed pools (issue 197; release plan docs/release_v43_plan.md): a development pool of 100, a confirm pool of 100, a test pool of 10 and a reserved pool of 10. Registry: experiments/seed_registry.json
(keyed by data version). Seed numbers repeat across data versions on purpose (data 4.2 seed 1741 and data 4.3 seed 1741 are different datasets); inside data 4.3 they do not collide.
Only the development pool (and, when asked, the confirm pool) is ever built by eval/make_d43_dev.py; the test and reserved pools are named here and NOT generated before the freeze. Free (code runs only)."""
DEV = [1003 + 41 * j for j in range(100)]         # 1003 .. 5062
CONFIRM = [1004 + 41 * j for j in range(100)]     # 1004 .. 5063
TEST = [6003 + 41 * j for j in range(10)]         # 6003 .. 6372
RESERVED = [7003 + 41 * j for j in range(10)]     # 7003 .. 7372
FIRST20 = DEV[:20]
BATCHES = [DEV[i:i + 10] for i in range(0, 100, 10)]
_all = DEV + CONFIRM + TEST + RESERVED
assert len(set(_all)) == 220
