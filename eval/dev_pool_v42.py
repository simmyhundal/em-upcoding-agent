"""The data 4.2 seed pools (issue 173): a development pool of 100, a confirm pool of 100, a test pool of 10 and a reserved pool of 10. Registry: experiments/seed_registry.json (keyed by data version).
Seed numbers repeat across data versions on purpose (data 4.0 seed 1515 and data 4.2 seed 1515 are different datasets); inside data 4.2 they do not collide, and all are below 5555.
Only the development pool (and, when asked, the confirm pool) is ever built; the test and reserved pools are named here and NOT generated. Free (code runs only)."""
DEV = [1001 + 37 * j for j in range(100)]         # 1001 .. 4664
CONFIRM = [1002 + 37 * j for j in range(100)]     # 1002 .. 4665
TEST = [4700 + 37 * j for j in range(10)]         # 4700 .. 5033
RESERVED = [5100 + 37 * j for j in range(10)]     # 5100 .. 5433
FIRST20 = DEV[:20]
BATCHES = [DEV[i:i + 10] for i in range(0, 100, 10)]
_all = DEV + CONFIRM + TEST + RESERVED
assert len(set(_all)) == 220 and max(_all) < 5555
