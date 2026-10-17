"""Tests for data 2.2 (issues 74 and later). Run: python tests/test_v22.py"""
import filecmp
import json
import os
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
import generate_v2  # noqa: E402


def build(version, seed=5, **opts):
    tmp = tempfile.mkdtemp()
    out, key = os.path.join(tmp, "d"), os.path.join(tmp, "k", "key.json")
    generate_v2.build(out, key, seed=seed, n_providers=40, n_upcoders=4, n_hard_neg=4, clone_share=0.5, data_version=version, **opts)
    return out, json.load(open(key))


def same_files(a, b):
    bad = []
    for root, _, files in os.walk(a):
        for f in files:
            pa = os.path.join(root, f)
            pb = os.path.join(b, os.path.relpath(pa, a))
            if not os.path.exists(pb) or not filecmp.cmp(pa, pb, shallow=False):
                bad.append(os.path.relpath(pa, a))
    return bad


def test_zero_noise_reproduces_data_2_1_exactly():
    a, ka = build("2.1")
    b, kb = build("2.2", honest_miscode_rate=0.0, subtle_upcoder_share=0.0, group_billing=False, rendering_omitted_share=0.0,
                  correction_level_change_share=0.0, control_totals=False)
    assert same_files(a, b) == []
    assert ka["justified_cpt_by_claim"] == kb["justified_cpt_by_claim"]
    assert {p: v["role"] for p, v in ka["providers"].items()} == {p: v["role"] for p, v in kb["providers"].items()}


def test_options_are_refused_on_frozen_versions():
    for version in ("2.0", "2.1"):
        try:
            build(version, honest_miscode_rate=0.1)
        except ValueError:
            continue
        raise AssertionError("frozen data versions must not accept data 2.2 options")


def test_noise_bills_honest_visits_off_level_and_roles_follow_the_margin():
    out, key = build("2.2", seed=6, honest_miscode_rate=0.12, subtle_upcoder_share=0.5, upcoder_definition="margin")
    P = key["providers"]
    honest = [v for v in P.values() if v["planted"] != "upcoder"]
    assert sum(v["upcode_rate"] for v in honest) / len(honest) > 0.02 and sum(v["downcode_rate"] for v in honest) / len(honest) > 0.02
    base, margin = key["honest_baseline_true_rate"], key["upcoder_margin"]
    for v in P.values():
        assert (v["role"] == "upcoder") == (v["true_upcode_rate"] - base >= margin), v
    assert all("planted" in v and "honest_miscode_rate" in v for v in P.values())


def test_payer_definition_needs_both_the_percentile_and_the_margin_on_true_rates():
    out, key = build("2.2", seed=6, honest_miscode_rate=0.12, subtle_upcoder_share=0.5)
    P, base, p95, margin = key["providers"], key["honest_baseline_true_rate"], key["honest_p95_true_rate"], key["upcoder_margin"]
    assert key["upcoder_definition"] == "payer"
    honest = sorted(v["true_upcode_rate"] for v in P.values() if v["planted"] != "upcoder")
    assert abs(p95 - honest[int(0.95 * (len(honest) - 1))]) < 0.02                    # the 95th percentile of the honest true rates (interpolated)
    for v in P.values():
        assert (v["role"] == "upcoder") == (v["true_upcode_rate"] - base >= margin and v["true_upcode_rate"] > p95), v
        assert v["above_p95"] == (v["true_upcode_rate"] > p95) and v["planted_below_line"] == (v["planted"] == "upcoder" and v["role"] != "upcoder")
    # the label does not depend on one year's luck: an honest provider never crosses, and every default-range planted upcoder does
    assert all(v["role"] != "upcoder" for v in P.values() if v["planted"] != "upcoder")
    assert all(v["role"] == "upcoder" for v in P.values() if v["planted"] == "upcoder")
    # the margin-only definition labels a superset
    _, k2 = build("2.2", seed=6, honest_miscode_rate=0.12, subtle_upcoder_share=0.5, upcoder_definition="margin")
    up1 = {p for p, v in P.items() if v["role"] == "upcoder"}
    up2 = {p for p, v in k2["providers"].items() if v["role"] == "upcoder"}
    assert up1 <= up2
    try:
        build("2.2", upcoder_definition="nope")
    except ValueError:
        return
    raise AssertionError("unknown definition accepted")


def test_frozen_keys_carry_no_data_22_fields():
    _, key = build("2.1")
    assert "honest_baseline_upcode_rate" not in key
    assert all("planted" not in v for v in key["providers"].values())


def _rows(path):
    import csv
    return list(csv.DictReader(open(path)))


def _view(out):
    import derive
    view = os.path.join(out, "view")
    derive.build_view(out, view)
    return view


def test_group_billing_uses_organizational_npis_and_visits_stay_with_the_clinician():
    out, key = build("2.2", seed=7, rendering_omitted_share=0.0)
    hdr = _rows(os.path.join(out, "claims_header.csv"))
    npis = {r["npi"] for r in _rows(os.path.join(out, "providers.csv"))}
    org = [h for h in hdr if h["billing_npi"] not in npis]
    assert org and all(h["billing_npi"].startswith("2") and h["rendering_npi"] in npis for h in org)
    view = _view(out)
    rend = {h["claim_id"]: h["rendering_npi"] for h in hdr if h["claim_frequency"] == "1"}
    claims = _rows(os.path.join(view, "claims.csv"))
    assert claims and all(c["provider_id"] in npis and c["provider_id"] == rend[c["claim_id"]] for c in claims)
    import derive
    ent = derive.billing_entity(view)
    assert all(ent[p] == key["providers"][p]["billing_npi"] for p in ent)               # actions go to the billing entity


def test_blank_rendering_falls_back_to_billing_and_is_reported():
    import json
    out, _ = build("2.2", seed=7, rendering_omitted_share=0.6)
    hdr = _rows(os.path.join(out, "claims_header.csv"))
    blank = [h for h in hdr if not h["rendering_npi"]]
    assert blank and all(h["billing_npi"].startswith("1") for h in blank)             # only single-clinician billing omits rendering
    view = _view(out)
    rep = json.load(open(os.path.join(view, "attribution.json")))
    assert rep["fallback_to_billing"] > 0 and 0 < rep["share_fallback_to_billing"] < 1 and rep["unattributed"] == 0
    # the same data with nothing omitted gives the same visits attributed to the same clinicians
    out0, _ = build("2.2", seed=7, rendering_omitted_share=0.0)
    a = {c["claim_id"]: c["provider_id"] for c in _rows(os.path.join(view, "claims.csv"))}
    b = {c["claim_id"]: c["provider_id"] for c in _rows(os.path.join(_view(out0), "claims.csv"))}
    assert a == b
    cpt = lambda v: {c["claim_id"]: c["cpt"] for c in _rows(os.path.join(v, "claims.csv"))}
    assert cpt(view) == cpt(os.path.join(out0, "view"))                              # blanking rendering moves no billed level


def test_org_billing_with_blank_rendering_cannot_be_attributed():
    import derive
    out, _ = build("2.2", seed=7, rendering_omitted_share=0.0)
    path = os.path.join(out, "claims_header.csv")
    rows = _rows(path)
    org_rows = [r for r in rows if r["billing_npi"].startswith("2")][:5]
    for r in org_rows:
        r["rendering_npi"] = ""
    import csv
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    stats = {}
    derive.accepted_visits(out, stats)
    assert 0 < stats["unattributed"] <= 5


def test_dx_cap_truncates_only_the_delivered_extract_and_moves_nothing_else():
    a, ka = build("2.2", seed=8)
    b, kb = build("2.2", seed=8, dx_cap=2, dx_cap_months=(1, 2, 3, 4, 5, 6))
    ha, hb = _rows(os.path.join(a, "claims_header.csv")), _rows(os.path.join(b, "claims_header.csv"))
    assert len(ha) == len(hb)
    cut = 0
    for x, y in zip(ha, hb):
        dxa = [x[f"dx{k}"] for k in range(1, 7) if x[f"dx{k}"]]
        dxb = [y[f"dx{k}"] for k in range(1, 7) if y[f"dx{k}"]]
        if int(x["service_date"][5:7]) <= 6:
            assert dxb == dxa[:2]
        else:
            assert dxb == dxa                                                    # months outside the cap are untouched
        cut += (dxb != dxa) and x["claim_frequency"] == "1"          # replacements and voids copy their original's list
    assert cut > 0 and kb["defects"]["dx_truncation"]["claims_shortened"] == cut
    assert filecmp.cmp(os.path.join(a, "claim_lines.csv"), os.path.join(b, "claim_lines.csv"), shallow=False)
    assert filecmp.cmp(os.path.join(a, "records", "visit_notes.csv"), os.path.join(b, "records", "visit_notes.csv"), shallow=False)
    assert ka["justified_cpt_by_claim"] == kb["justified_cpt_by_claim"] and "dx_truncation" in kb["defects"] and "dx_truncation" not in ka["defects"]


def test_corrections_change_the_level_and_the_view_keeps_the_live_claim():
    import derive
    out, key = build("2.2", seed=9, correction_level_change_share=1.0, correction_up_share=0.0)
    hdr = {h["claim_id"]: h for h in _rows(os.path.join(out, "claims_header.csv"))}
    em = {}
    for r in _rows(os.path.join(out, "claim_lines.csv")):
        if r["cpt"].startswith("992"):
            em[r["claim_id"]] = r["cpt"]
    pairs = [(h["original_claim_id"], cid) for cid, h in hdr.items() if h["claim_frequency"] == "7"]
    assert pairs and all(em[new] < em[old] or em[old] == "99211" and em[new] > em[old] for old, new in pairs)    # all go down (up only at the floor)
    view = _view(out)
    v = {c["claim_id"]: c["cpt"] for c in _rows(os.path.join(view, "claims.csv"))}
    live = [old for old, new in pairs if old in v]
    assert live and all(v[old] == em[new] for old, new in pairs if old in v)                                       # the view shows the corrected level
    st = derive.correction_stats(out)
    assert sum(x["corrections"] for x in st.values()) == len(pairs)
    assert sum(x["level_down"] for x in st.values()) == sum(p["corrections_down"] for p in key["providers"].values())
    assert sum(p["corrections"] for p in key["providers"].values()) == len(pairs)


def test_correction_option_moves_no_other_billed_level():
    a, _ = build("2.2", seed=9, correction_level_change_share=0.0)
    b, _ = build("2.2", seed=9, correction_level_change_share=0.5)
    ha, hb = _rows(os.path.join(a, "claims_header.csv")), _rows(os.path.join(b, "claims_header.csv"))
    assert ha == hb                                                                     # same claims, same ids, same dates, same diagnoses
    la = {r["claim_id"]: r["cpt"] for r in _rows(os.path.join(a, "claim_lines.csv"))}
    lb = {r["claim_id"]: r["cpt"] for r in _rows(os.path.join(b, "claim_lines.csv"))}
    changed = {c for c in la if la[c] != lb[c]}
    assert changed and all(hb_["claim_frequency"] == "7" for hb_ in hb if hb_["claim_id"] in changed)


def _delivered_totals(out):
    import defects_v22
    return defects_v22.control_totals(_rows(os.path.join(out, "claims_header.csv")), _rows(os.path.join(out, "remittance.csv")))


def test_control_totals_match_a_clean_extract_exactly():
    out, key = build("2.2", seed=10)
    ct = {r["service_month"]: {"claims": int(r["claims"]), "paid_usd": float(r["paid_usd"])} for r in _rows(os.path.join(out, "control_totals.csv"))}
    assert ct == _delivered_totals(out) and key["defects"]["control_totals"]["months"] == len(ct) and "duplicates" not in key["defects"]


def test_injected_defects_are_in_the_data_and_recorded_in_the_key():
    import derive
    import json
    out, key = build("2.2", seed=10, defect_duplicate_share=0.05, defect_orphan_share=0.5, defect_unknown_member_share=0.04,
                     defect_no_rendering_share=0.2)
    d = key["defects"]
    hdr = {h["claim_id"]: h for h in _rows(os.path.join(out, "claims_header.csv"))}
    members = {m["member_id"] for m in _rows(os.path.join(out, "members.csv"))}
    assert d["duplicates"]["count"] > 0
    for dup, orig in d["duplicates"]["pairs"]:
        a, b = hdr[dup], hdr[orig]
        assert (a["member_id"], a["service_date"], a["billing_npi"], a["dx1"]) == (b["member_id"], b["service_date"], b["billing_npi"], b["dx1"])
    assert d["orphans"]["missing_originals"] and all(o not in hdr for o in d["orphans"]["missing_originals"])
    assert all(hdr[c]["original_claim_id"] in d["orphans"]["missing_originals"] for c in d["orphans"]["replacements"])
    assert d["unknown_member"]["count"] > 0 and all(hdr[c]["member_id"] not in members for c in d["unknown_member"]["claim_ids"])
    assert d["no_rendering"]["count"] > 0 and all(hdr[c]["rendering_npi"] == "" and hdr[c]["billing_npi"].startswith("2") for c in d["no_rendering"]["claim_ids"])
    # the delivered extract no longer matches the plan's control totals, by exactly the injected claims
    ct = {r["service_month"]: int(r["claims"]) for r in _rows(os.path.join(out, "control_totals.csv"))}
    delivered = {m: v["claims"] for m, v in _delivered_totals(out).items()}
    assert sum(delivered.values()) - sum(ct.values()) == d["duplicates"]["count"] - len(d["orphans"]["missing_originals"])
    assert delivered != ct
    # the detector view drops what cannot be joined or attributed and says how many
    view = _view(out)
    rep = json.load(open(os.path.join(view, "attribution.json")))
    assert rep["member_not_in_eligibility"] > 0 and rep["unattributed"] > 0
    assert not {c["claim_id"] for c in _rows(os.path.join(view, "claims.csv"))} & set(d["unknown_member"]["claim_ids"])
    assert key["justified_cpt_by_claim"].get(d["duplicates"]["pairs"][0][0])                                 # duplicates carry a justified level


def test_defects_are_refused_on_frozen_versions_and_leave_other_streams_alone():
    a, _ = build("2.2", seed=11)
    b, _ = build("2.2", seed=11, defect_duplicate_share=0.1)
    ha, hb = _rows(os.path.join(a, "claims_header.csv")), _rows(os.path.join(b, "claims_header.csv"))
    assert hb[:len(ha)] == ha                                                       # duplicates are appended; nothing before them moves
    try:
        build("2.1", defect_duplicate_share=0.1)
    except ValueError:
        return
    raise AssertionError("defects must not be accepted on data 2.1")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
