"""Tests for the workflow 2.4 candidate policies (issue 102). Run: python tests/test_release4.py"""
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "eval"))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, HERE)
import workflow_policy_23 as p23  # noqa: E402
import workflow_policy_24 as p24  # noqa: E402
from test_release3 import FakeOffice  # noqa: E402

p23.cloning_signs = lambda rows, by_id: len(rows) >= 8 and sum(r["late"] == "1" for r in rows) / len(rows) >= 0.12     # the fake office returns only a late flag
CLAIMS = {p: [{"claim_id": f"{p}-{i}", "cpt": "99214" if i < 12 else "99215"} for i in range(40)] for p in ("a", "b", "c", "d")}
RATIO = {"a": 5.0, "b": 2.0, "c": 4.0, "d": 2.0}


class Silent(FakeOffice):
    def send_request(self, pid, sample, deadline=30):
        self.log.append((pid, sample["kind"]))
        self.state[pid] = {"round": 1, "usable": {}}
        return {"ok": True}


def test_defaults_reproduce_policy_23():
    a, b = FakeOffice(late=0.0), FakeOffice(late=0.0)
    p23.run_policy_23(a, ["a", "b", "c", "d"], CLAIMS, 2)
    p24.run_policy_24(b, ["a", "b", "c", "d"], CLAIMS, 2, RATIO)
    assert a.log == b.log


def test_gate_applies_to_the_light_tier_unless_gate_all():
    o = FakeOffice(late=0.0)
    p24.run_policy_24(o, ["a", "b", "c", "d"], CLAIMS, 2, RATIO, gate_t=3.0)
    asked = {x[0] for x in o.log}
    assert asked == {"a", "b", "c"}                                   # b is tier 1 (not gated); d is light tier with ratio 2 < 3
    o = FakeOffice(late=0.0)
    p24.run_policy_24(o, ["a", "b", "c", "d"], CLAIMS, 2, RATIO, gate_t=3.0, gate_all=True)
    assert {x[0] for x in o.log} == {"a", "c"}


def test_stop_silent_closes_without_a_targeted_request():
    o = Silent(late=0.0)
    p24.run_policy_24(o, ["a", "b"], CLAIMS, 2, RATIO, stop_silent=True)
    assert [x[1] for x in o.log] == ["random", "random"]
    o = Silent(late=0.0)
    p24.run_policy_24(o, ["a"], CLAIMS, 1, RATIO)
    assert ("a", "targeted") in o.log


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
