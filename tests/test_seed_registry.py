"""The seed registry (issue 176) is consistent, matches the development pool, and its checks raise. Free. Run: python tests/test_seed_registry.py"""
import copy
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import dev_pool_v4 as dp  # noqa: E402
import seed_registry as sr  # noqa: E402
import seed_registry_report as rep  # noqa: E402

REG = sr.load()


def pools(data=None):
    return [p for p in REG["pools"] if data is None or p["data_version"] == data]


def raises(fn, *a, **k):
    try:
        fn(*a, **k)
    except sr.SeedRegistryError as e:
        return str(e)
    raise AssertionError("expected SeedRegistryError")


def test_fields_and_vocabulary():
    ids = [p["id"] for p in pools()]
    assert len(ids) == len(set(ids))
    for p in pools():
        assert p["status"] in sr.STATUSES and p["kind"] in sr.KINDS, p["id"]
        assert p["seeds"] and len(p["seeds"]) == len(set(p["seeds"])), p["id"]
        for u in p["uses"]:
            assert u["role"] in sr.ROLES, (p["id"], u)
            assert {"arm", "role", "date", "reference", "note", "second_use"} <= set(u), (p["id"], u)
            assert set(u.get("seeds", p["seeds"])) <= set(p["seeds"]), (p["id"], u)
    for word in ("fit", "select", "confirm", "test", "burned", "fresh"):
        assert word in REG["vocabulary"]


def test_no_overlap_between_pools_of_the_same_data_version():
    for data in {p["data_version"] for p in pools()}:
        seen = {}
        for p in pools(data):
            for s in p["seeds"]:
                assert s not in seen, f"data {data} seed {s} is in both {seen[s]} and {p['id']}"
                seen[s] = p["id"]


def test_data_4_pools_match_the_development_pool_and_the_run_scripts():
    by = {p["id"]: p["seeds"] for p in pools("4.0")}
    assert by["D4.0-DEV-A"] == dp.seeds(4)
    assert by["D4.0-DEV-B"] == dp.BATCHES[4] + dp.BATCHES[5]
    assert by["D4.0-DEV-C"] == sum(dp.BATCHES[6:10], [])
    assert by["D4.0-SMOKE"] == [dp.SMOKE]
    assert by["D4.0-TEST-1"] == [5555 + 101 * i for i in range(10)]
    assert by["D4.0-TEST-2"] == [6565 + 101 * i for i in range(10)]
    dev = sum(dp.BATCHES, [])
    assert sorted(by["D4.0-DEV-A"] + by["D4.0-DEV-B"] + by["D4.0-DEV-C"]) == sorted(dev)
    assert all(s < 5555 for s in dev)
    assert next(p for p in pools("4.0") if p["id"] == "D4.0-TEST-2")["status"] == "reserved"
    assert next(p for p in pools("4.0") if p["id"] == "D4.0-TEST-2")["uses"] == []


def test_data_2_2_release_pools():
    by = {p["id"]: p["seeds"] for p in pools("2.2")}
    for pid, first in (("D2.2-REL2", 1515), ("D2.2-REL3", 2525), ("D2.2-REL4", 3535), ("D2.2-REL5", 4545)):
        assert by[pid] == [first + 101 * i for i in range(10)], pid


def test_no_arm_fits_or_selects_on_a_seed_it_also_confirms_or_tests_on():
    for p in pools():
        for a in p["uses"]:
            for b in p["uses"]:
                if a is b or not a.get("done", True) or not b.get("done", True):
                    continue
                if sr.canonical(REG, a["arm"]) == sr.canonical(REG, b["arm"]) and a["role"] in ("fit", "select") and b["role"] in ("confirm", "test"):
                    both = set(a.get("seeds", p["seeds"])) & set(b.get("seeds", p["seeds"]))
                    assert not both, f"{p['id']}: {a['arm']} {a['role']} and {b['role']} on {sorted(both)}"


def test_test_pools_are_never_fitted_or_selected_on():
    for p in pools():
        if p["kind"] == "test":
            assert not [u for u in p["uses"] if u["role"] in ("fit", "select")], p["id"]


def test_seeds_md_is_up_to_date():
    with open(os.path.join(ROOT, "docs", "seeds.md")) as f:
        assert f.read() == rep.render(REG), "docs/seeds.md is stale: run python eval/seed_registry_report.py --write"


def test_check_run_raises_on_a_reserved_pool():
    msg = raises(sr.check_run, "4.0", [6565], "W4.1", "test")
    assert "reserved" in msg
    raises(sr.check_run, "4.0", [6565, 5555], "W4.1", "test", second_use=True)
    raises(sr.check_development, "4.0", [6565])
    raises(sr.check_development, "4.0", [5555])


def test_check_run_raises_on_a_confirm_that_overlaps_a_fit():
    msg = raises(sr.check_run, "4.0", [1515], "H8", "confirm")  # H8's ask model was fitted on batches 1 to 4
    assert "fitted or selected" in msg
    raises(sr.check_run, "4.0", [1515], "W4.0", "test")  # alias of H8
    sr.check_run("4.0", dp.BATCHES[4], "H8", "confirm")  # batch 5 is out of sample for H8's model
    raises(sr.check_run, "4.0", dp.BATCHES[4], "H13", "fit")  # H13 was read as a confirm on batch 5
    sr.check_development("4.0", dp.seeds(10))
    sr.check_development("4.0", [42])


def test_check_run_second_use_and_data_version_keying():
    reg = copy.deepcopy(REG)
    # a new workflow arm on the burned test pool is a second use of the line
    msg = raises(sr.check_run, "4.0", [5555], "W4.2", "test", reg=reg)
    assert "second use" in msg
    sr.check_run("4.0", [5555], "W4.2", "test", second_use=True, reg=reg)
    sr.check_run("4.0", [5555], "W4.0", "test", reg=reg)  # replay of a recorded arm
    sr.check_run("4.0", [5555, 6464], "W4.1", "test", second_use=True, reg=reg)
    raises(sr.check_run, "4.0", [5555], "W4.1", "test", reg=reg)  # recorded as a second use: the flag must match
    raises(sr.check_run, "4.0", [5555], "W4.0", "test", second_use=True, reg=reg)  # recorded as a first use
    # a fresh pool allows only a test
    reg["pools"].append({"id": "X", "data_version": "4.0", "seeds": [9999], "kind": "test", "status": "fresh", "status_date": None, "status_note": "", "uses": []})
    raises(sr.check_run, "4.0", [9999], "W4.2", "select", reg=reg)
    sr.check_run("4.0", [9999], "W4.2", "test", reg=reg)
    # the same number in another data version is another dataset
    assert sr.describe("2.2", 1515)["pool"] == "D2.2-REL2" and sr.describe("4.0", 1515)["pool"] == "D4.0-DEV-A"
    raises(sr.check_run, "2.2", [6565], "W4.2", "test")  # not in any 2.2 pool
    d = sr.describe("4.0", 3630)
    assert d["pool"] == "D4.0-DEV-B" and ("H22", "select", True, False) in d["uses"]
    assert sr.describe("4.0", 123456) is None


def test_the_wired_scripts_compile_and_their_registry_calls_pass():
    import ast
    for f in ("w_loop.py", "run_v41_fresh.py", "run_v4_fresh.py", "run_v5_fresh_agent.py"):
        src = open(os.path.join(ROOT, "eval", f)).read()
        ast.parse(src, f)
        assert "seed_registry" in src, f
    t1 = [5555 + 101 * i for i in range(10)]
    for arm in ("W2.5", "W4.0"):  # eval/run_v4_fresh.py workflow
        sr.check_run("4.0", t1, arm, "test")
    for version in ("3.5", "5.0"):  # eval/run_v5_fresh_agent.py
        sr.check_run("4.0", t1, "A" + version, "test")
    for arm in ("W4.1", "H8_n4"):  # eval/run_v41_fresh.py
        sr.check_run("4.0", t1, arm, "test", second_use=True)
    sr.check_development("4.0", dp.seeds(10) + [dp.SMOKE])  # eval/w_loop.py evaluate


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
