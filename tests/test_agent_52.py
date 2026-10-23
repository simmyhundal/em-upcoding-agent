"""Agent v5.2: the claims-data lane tools, their refusals and the scoring of a lane record. Needs the data 4.2 development seed d42_1001 (skipped without it). Run: python tests/test_agent_52.py"""
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import agent_tools as at  # noqa: E402

DATA = os.path.join(ROOT, "data", "synthetic_v2_d42_1001")


def env(version="5.2"):
    return at.Environment(DATA, os.path.join(DATA, "view"), seed=1, version=version, records_budget=22, office=at.make_office(DATA, os.path.join(DATA, "view"), version, seed=1))


def main():
    if not os.path.isdir(DATA):
        print("skip: data 4.2 development seed d42_1001 is not built")
        return
    e = env()
    names = [t["name"] for t in e.tool_schemas()]
    assert {"volume_screen", "request_stratum", "send_demand"} <= set(names)
    assert not ({"volume_screen", "request_stratum", "send_demand"} & {t["name"] for t in env("5.1").tool_schemas()}), "agent v5.1 must not gain the lane tools"
    assert env("5.1").call("volume_screen", {}).get("error") == "tool not available"
    v = e.call("volume_screen", {})
    assert v["flagged"] >= 1 and all(r["busiest_day_visits"] >= 30 for r in v["table"])
    # a provider that is not on the table is refused
    ordinary = next(p for p in e.claims if p not in {r["provider_id"] for r in v["table"]})
    assert "error" in e.call("request_stratum", {"provider_id": ordinary})
    # send_demand before request_stratum is refused
    pid = v["table"][0]["provider_id"]
    assert "error" in e.call("send_demand", {"provider_id": pid})
    r = e.call("request_stratum", {"provider_id": pid})
    assert r["sampled"] == 30 and r["recommended"] in ("DEMAND", "NO DEMAND")
    assert "error" in e.call("request_stratum", {"provider_id": pid}), "once per provider"
    d = e.call("send_demand", {"provider_id": pid})
    assert ("error" in d) == (r["recommended"] == "NO DEMAND")
    # the lane record carries what score 4.2 needs and nothing from the answer key
    rec = e.lane_record()["providers"][pid]
    assert set(rec) >= {"stratum_ids", "sample_ids", "no_record", "levels", "estimate", "demand"}
    assert "role" not in json.dumps(rec) and "true_overpay" not in json.dumps(rec)
    # the office is 4.2: a never-rendered claim is reported NO_RECORD
    assert e.office.unrendered, "office 4.2 should know the never-rendered claims"
    print("ok test_agent_52")


if __name__ == "__main__":
    main()
