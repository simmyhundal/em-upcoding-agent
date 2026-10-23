"""Issue 100: the agent's Environment never holds the answer key's roles. `Environment` takes no `roles` (or `correlation`), the office is built outside it by `agent_tools.make_office`,
and at correlation 0 the office never receives roles. No attribute reachable from an Environment, and no tool result, contains a role or the word upcoder from the answer key.
Run: python tests/test_agent_roles.py"""
import inspect
import json
import os
import sys
import tempfile

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import agent_tools as at  # noqa: E402
import derive  # noqa: E402
import generate_v2 as g  # noqa: E402

KEY = os.path.join(tempfile.mkdtemp(), "answer_key", "ground_truth_v2.json")
D = tempfile.mkdtemp()
g.build(D, KEY, seed=17, n_providers=40, n_upcoders=5, n_hard_neg=3, data_version="2.1")
VIEW = os.path.join(D, "view")
derive.build_view(D, VIEW)
TRUTH = json.load(open(KEY))["providers"]
ROLES = {p: v["role"] for p, v in TRUTH.items()}
BAD_WORDS = ("upcoder", "hard_negative", "ground_truth", "answer_key")


def _reachable(root):
    """Every object reachable from root through attributes, dict values and keys, lists, tuples and sets (each object once)."""
    seen, stack, out = set(), [root], []
    while stack:
        o = stack.pop()
        if id(o) in seen:
            continue
        seen.add(id(o))
        out.append(o)
        if isinstance(o, dict):
            stack += list(o.keys()) + list(o.values())
        elif isinstance(o, (list, tuple, set, frozenset)):
            stack += list(o)
        elif hasattr(o, "__dict__") and not inspect.ismodule(o) and not inspect.isclass(o) and not callable(o):
            stack += list(vars(o).values())
    return out


def test_environment_takes_no_roles_or_correlation():
    params = inspect.signature(at.Environment.__init__).parameters
    assert "roles" not in params and "correlation" not in params and "office" in params


def test_office_gets_no_roles_at_correlation_zero_and_keeps_them_only_for_a_correlation_test():
    assert at.make_office(D, VIEW, "3.1", roles=ROLES).roles == {}
    assert at.make_office(D, VIEW, "3.1", correlation=0.5, roles=ROLES).roles == ROLES
    assert at.make_office(D, VIEW, "3.1").v21 and not at.make_office(D, VIEW, "3.0").v21


def test_nothing_reachable_from_the_environment_holds_the_answer_key():
    for version in ("3.0", "3.1", "3.2", "3.4"):
        e = at.Environment(D, VIEW, seed=1, version=version, office=at.make_office(D, VIEW, version, roles=ROLES))
        assert e.office.roles == {} and not hasattr(e, "roles") and not hasattr(e, "correlation")
        for o in _reachable(e):
            if isinstance(o, str):
                assert o not in ("upcoder", "hard_negative") and not any(w in o for w in ("ground_truth", "answer_key"))
            if isinstance(o, dict):
                assert o != ROLES and "roles" not in o and "truth" not in o


def test_no_tool_result_mentions_a_role():
    e = at.Environment(D, VIEW, seed=1, version="3.4", records_budget=22, office=at.make_office(D, VIEW, "3.4", roles=ROLES))
    top = e.call("screen_providers", {"method": "riskadj", "top_n": 5})["table"]["rows"][0][0]
    calls = [("screen_providers", {"method": "riskadj", "top_n": 5}), ("provider_profile", {"provider_id": top}), ("peer_comparison", {"provider_id": top}),
             ("request_records", {"provider_id": top, "sample": {"kind": "random", "n": 20}}), ("hybrid_review", {"provider_ids": [top]}), ("note_checks", {"provider_id": top}),
             ("estimate_overpayment", {"provider_id": top}), ("advise_next_step", {"provider_id": top}), ("data_quality", {}), ("draft_summary", {"provider_id": top}),
             ("submit_findings", {"findings": [{"provider_id": top, "leaning": "inconclusive", "headline": "h", "interpretation": "x"}]})]
    text = json.dumps([e.call(name, args) for name, args in calls], default=str) + json.dumps(e.tool_schemas(), default=str) + json.dumps(e.budget_status(), default=str)
    assert len(text) > 1000 and not any(w in text for w in BAD_WORDS), [w for w in BAD_WORDS if w in text]


def test_default_office_is_the_same_as_an_explicit_one():
    a = at.Environment(D, VIEW, seed=1, version="3.1")
    b = at.Environment(D, VIEW, seed=1, version="3.1", office=at.make_office(D, VIEW, "3.1"))
    pid = sorted(a.claims)[0]
    ra, rb = a.office.send_request(pid, {"kind": "random", "n": 10}, 30), b.office.send_request(pid, {"kind": "random", "n": 10}, 30)
    assert json.dumps(ra, sort_keys=True, default=str) == json.dumps(rb, sort_keys=True, default=str)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
