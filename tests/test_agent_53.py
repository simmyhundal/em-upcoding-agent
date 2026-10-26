"""Agent v5.3: the lane-completion gate (issue 208). submit_findings refuses until every provider on the volume screen's table has been taken through request_stratum or set aside with a reason; agent v5.2 does not refuse. Needs the data 4.2 development seed d42_1001 (skipped without it). Run: python tests/test_agent_53.py"""
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import agent_tools as at  # noqa: E402

DATA = os.path.join(ROOT, "data", "synthetic_v2_d42_1001")


def env(version):
    # the office of data 4.2 is built directly, so this test does not depend on office 4.3
    office = at.make_office(DATA, os.path.join(DATA, "view"), "5.2", seed=1)
    return at.Environment(DATA, os.path.join(DATA, "view"), seed=1, version=version, records_budget=22, office=office)


def main():
    if not os.path.isdir(DATA):
        print("skip: data 4.2 development seed d42_1001 is not built")
        return
    e = env("5.3")
    table = [r["provider_id"] for r in e.call("volume_screen", {})["table"]]
    assert len(table) >= 2
    r = e.call("submit_findings", {"findings": []})
    assert "error" in r and set(r["pending"]) == set(table), r
    e.call("request_stratum", {"provider_id": table[0]})
    r = e.call("submit_findings", {"findings": []})
    assert set(r["pending"]) == set(table[1:])
    r = e.call("submit_findings", {"findings": [], "set_aside": [{"provider_id": p, "reason": ""} for p in table[1:]]})
    assert "pending" in r, "an empty reason does not count"
    r = e.call("submit_findings", {"findings": [], "set_aside": [{"provider_id": p, "reason": "office silent and the estimate cannot cover a demand"} for p in table[1:]]})
    assert "pending" not in r, r
    assert "pending" not in env("5.2").call("submit_findings", {"findings": []}), "agent v5.2 must not refuse"
    assert "v53" in vars(env("5.3")) and not env("5.2").v53 and not env("5.1").v52
    print("ok test_agent_53")


if __name__ == "__main__":
    main()
