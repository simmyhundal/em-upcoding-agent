"""Tests for the data-quality pre-flight and the v3.2 agent tools (issue 81). Run: python tests/test_data_quality.py"""
import csv
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
import agent_tools as at  # noqa: E402
import data_quality as dq  # noqa: E402
import derive  # noqa: E402
import generate_v2 as g  # noqa: E402
import summary_rules as sr  # noqa: E402

_C = {}


def dataset(kind):
    if kind not in _C:
        d = tempfile.mkdtemp()
        opts = {} if kind == "clean" else dict(defect_duplicate_share=0.02, defect_orphan_share=0.5, defect_unknown_member_share=0.02,
                                               defect_no_rendering_share=0.08, dx_cap=3, dx_cap_months=tuple(range(7, 13)))
        key = os.path.join(tempfile.mkdtemp(), "k.json")
        g.build(d, key, seed=31, n_providers=60, n_upcoders=5, n_hard_neg=4, data_version="2.2", **opts)
        derive.build_view(d, os.path.join(d, "view"))
        _C[kind] = (d, json.load(open(key)))
    return _C[kind]


def test_clean_extract_passes_every_check():
    d, _ = dataset("clean")
    rep = dq.run_checks(d)
    assert rep["status"] == "ok" and not rep["global_flags"] and not rep["per_provider"] and not rep["truncation_suspected"]
    assert {c["id"] for c in rep["checks"]} == {"control_totals", "em_mix", "dx_per_claim", "rendering_npi", "member_join", "duplicates", "chains", "claims_lag"}


def test_every_injected_defect_is_found():
    d, key = dataset("defects")
    inj = key["defects"]
    rep = dq.run_checks(d)
    by = {c["id"]: c for c in rep["checks"]}
    assert all(by[k]["status"] == "warn" for k in ("control_totals", "dx_per_claim", "rendering_npi", "member_join", "duplicates", "chains")), {k: v["status"] for k, v in by.items()}
    assert set(by["dx_per_claim"]["numbers"]["suspected_cap_months"]) == {f"2024-{m:02d}" for m in range(7, 13)} and rep["truncation_suspected"]
    assert by["chains"]["numbers"]["orphans"] == len(inj["orphans"]["replacements"]) + len(inj["orphans"]["voids"])
    assert by["member_join"]["numbers"]["unmatched_claims"] == inj["unknown_member"]["count"]
    t = dq.load(d)
    _, dups = dq.check_duplicates(t)
    copies = {p[0] for p in inj["duplicates"]["pairs"]}
    assert copies <= {x[0] for x in dups}                                           # every injected copy is named (natural collisions may add a few)
    mm = by["control_totals"]["numbers"]["months_mismatched"]
    assert sum(v["claims_diff"] for v in mm.values()) == len(inj["duplicates"]["pairs"]) - len(inj["orphans"]["missing_originals"])
    assert rep["per_provider"] and all(f["detail"] for fl in rep["per_provider"].values() for f in fl)


def test_hold_decision_needs_chart_evidence_for_affected_providers():
    d, _ = dataset("defects")
    rep = dq.run_checks(d)
    p = next(iter(rep["per_provider"]))
    h = dq.hold_decision(rep, p, charts_received=0)
    assert h["affected"] and h["needs_chart_evidence"] and h["caveat"].startswith("Data caveat")
    assert not dq.hold_decision(rep, p, charts_received=9)["needs_chart_evidence"]
    assert not dq.hold_decision(rep, "no-such-provider")["affected"]


def test_flagging_preflight_adds_a_column_and_blocks_on_a_block():
    d, _ = dataset("defects")
    out = os.path.join(tempfile.mkdtemp(), "flagged.csv")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "src", "flagging.py"), os.path.join(d, "view"), out, "--preflight", d], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    rows = list(csv.DictReader(open(out)))
    assert "data_quality" in rows[0] and any(x["data_quality"].startswith("Data caveat") for x in rows)
    assert os.path.exists(os.path.join(os.path.dirname(out), "data_quality.json"))
    plain = os.path.join(tempfile.mkdtemp(), "plain.csv")
    subprocess.run([sys.executable, os.path.join(ROOT, "src", "flagging.py"), os.path.join(d, "view"), plain], check=True, capture_output=True)
    assert "data_quality" not in list(csv.DictReader(open(plain)))[0]               # without the option the output is unchanged


def test_v32_tools_exist_only_in_v32_and_hold_upcoding_findings():
    d, _ = dataset("defects")
    view = os.path.join(d, "view")
    e31, e32 = at.Environment(d, view, version="3.1"), at.Environment(d, view, version="3.2", records_budget=10)
    n31, n32 = {t["name"] for t in e31.tool_schemas()}, {t["name"] for t in e32.tool_schemas()}
    assert not ({"data_quality", "flag_data_issue"} & n31) and {"data_quality", "flag_data_issue"} <= n32
    assert "error" in e31.call("data_quality", {}) and "error" in e31.call("flag_data_issue", {"issue": "x", "detail": "y"})
    rep = e32.call("data_quality", {})
    assert rep["status"] == "warn" and rep["truncation_suspected"] and rep["global_flags"]
    pid = next(iter(e32.dq["per_provider"]))
    one = e32.call("data_quality", {"provider_id": pid})
    assert one["provider"]["flags"] and one["provider"]["hold"]["affected"] and one["provider"]["hold"]["needs_chart_evidence"]
    refused = e32.call("submit_findings", {"findings": [{"provider_id": pid, "leaning": sr.UPCODING, "headline": "x", "interpretation": "y"}]})
    assert "held" in refused and pid in refused["held"] and not e32.findings
    ok = e32.call("submit_findings", {"findings": [{"provider_id": pid, "leaning": sr.INCONCLUSIVE}]})
    assert "error" not in ok, ok
    assert "Data caveat" in e32.findings[pid]["rationale"]


def test_flag_data_issue_records_and_holds_without_requesting_data():
    d, _ = dataset("clean")
    view = os.path.join(d, "view")
    e = at.Environment(d, view, version="3.2")
    pid = sorted(e.rows)[0]
    assert "error" in e.call("flag_data_issue", {"issue": "", "detail": "x"}) and "error" in e.call("flag_data_issue", {"issue": "a", "detail": "b", "provider_ids": ["nope"]})
    out = e.call("flag_data_issue", {"issue": "suspected truncation", "detail": "diagnosis counts look capped", "provider_ids": [pid]})
    assert out["recorded"] and "cannot request data" in out["next"] and e.data_issues[0]["provider_ids"] == [pid]
    assert e._hold(pid)["needs_chart_evidence"] and not e._hold(sorted(e.rows)[1])["affected"]
    assert not any("request" in t["name"] and "plan" in t["description"].lower() for t in e.tool_schemas())     # no tool asks the plan for data


def test_a_block_stops_the_workflow_unless_overridden():
    d = tempfile.mkdtemp()
    g.build(d, os.path.join(tempfile.mkdtemp(), "k.json"), seed=32, n_providers=40, n_upcoders=3, n_hard_neg=3, data_version="2.2", defect_unknown_member_share=0.2)
    derive.build_view(d, os.path.join(d, "view"))
    assert dq.run_checks(d)["status"] == "block"
    out = os.path.join(tempfile.mkdtemp(), "flagged.csv")
    cmd = [sys.executable, os.path.join(ROOT, "src", "flagging.py"), os.path.join(d, "view"), out, "--preflight", d]
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode != 0 and "blocked" in (r.stderr + r.stdout) and not os.path.exists(out)
    assert subprocess.run(cmd + ["--continue-on-block"], capture_output=True, text=True).returncode == 0 and os.path.exists(out)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
