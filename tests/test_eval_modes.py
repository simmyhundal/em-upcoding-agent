"""Evaluation modes (issue 207): presets, gate 1 lists, gate 2 sign-off and the stage helpers. Free. Run: python tests/test_eval_modes.py"""
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import eval_modes as em  # noqa: E402


def test_presets_are_complete_and_the_first_is_the_reported_setting():
    assert em.PRESETS["accept_all"]["gate1"]["kind"] == "accept_all" and em.PRESETS["accept_all"]["gate2"]["kind"] == "accept_all"
    for cfg in em.PRESETS.values():
        assert cfg["stage"] in ("screen", "records", "full") and "gate1" in cfg and "gate2" in cfg


def test_gate2_functions():
    assert em.gate2_fn({"kind": "accept_all"}) is None
    f = em.gate2_fn({"kind": "min_estimate", "usd": 1000.0})
    assert f("p", 1000.0) and not f("p", 999.99)
    g = em.gate2_fn({"kind": "reject_fraction", "fraction": 0.5, "seed": 3})
    assert 0 < sum(g("p", 1.0) for _ in range(200)) < 200


def test_a_vetoed_list_is_deterministic_and_smaller():
    code = "d42_1001"
    if not os.path.exists(em._list_path(code, "eb_upper_t_10")):
        print("skip: d42_1001 is not built")
        return
    a = em.write_list(code, "eb_upper_t_10", "testveto", veto_fraction=0.5, veto_seed=7)
    ids = lambda n: [r["provider_id"] for r in __import__("csv").DictReader(open(em._list_path(code, n))) if r["flagged"] == "True"]
    first = ids(a)
    os.remove(em._list_path(code, a))
    em.write_list(code, "eb_upper_t_10", "testveto", veto_fraction=0.5, veto_seed=7)
    assert ids(a) == first and len(first) < len(ids("eb_upper_t_10"))
    os.remove(em._list_path(code, a))


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
