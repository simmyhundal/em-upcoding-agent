"""Score 4.0 (issue 125): parity with the frozen release 5 value when its two changes are off, netting, the extrapolation gate, abrasion weight, truth from claims, and that the
release 5 module and its published numbers are untouched. Run: python tests/test_score_40.py   (the data-dependent tests skip when the gitignored data is absent)"""
import csv
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import score_40 as s  # noqa: E402

ALLOWED = {"99211": 45.0, "99212": 75.0, "99213": 110.0, "99214": 165.0, "99215": 230.0}


def _claims(n13, n14, n15):
    rows, i = [], 0
    for cpt, n in (("99213", n13), ("99214", n14), ("99215", n15)):
        for _ in range(n):
            i += 1
            rows.append({"claim_id": f"C{i}", "provider_id": "P", "cpt": cpt, "allowed_amount": str(ALLOWED[cpt]), "paid_amount": str(ALLOWED[cpt] * 0.8)})
    return rows


def test_abrasion_weight_is_linear_between_zero_and_the_upcoder_floor():
    assert s.abrasion_weight(-0.2) == 1.0 and s.abrasion_weight(0.0) == 1.0
    assert abs(s.abrasion_weight(0.075) - 0.5) < 1e-9 and s.abrasion_weight(0.15) == 0.0 and s.abrasion_weight(0.4) == 0.0
    assert abs(s.abrasion_weight(0.10) - (1 - 0.10 / 0.15)) < 1e-9                    # a provider that truly overbilled 10% carries a third of the abrasion


def test_underpayment_is_negative_and_netting_lowers_the_value():
    assert s.overpay_signed("99214", "99215", ALLOWED, (165.0, 132.0)) < 0 < s.overpay_signed("99215", "99214", ALLOWED, (230.0, 184.0))
    rows = _claims(20, 20, 20)
    level = {r["claim_id"]: (1 if int(r["claim_id"][1:]) % 2 else 4) for r in rows}          # half supported at 99212 (overpaid), half at 99215 (99215 claims: exact)
    for r in rows:                                                                             # make the 99213 claims underpaid in half the sample: supported 99214
        if r["cpt"] == "99213" and int(r["claim_id"][1:]) % 4 == 0:
            level[r["claim_id"]] = 3
    ids = {r["claim_id"] for r in rows}
    from eval61_recovery import ROOT as _  # noqa: F401  (module import check only)
    import eval61_recovery as rec
    real = rec.allowed
    rec.allowed = lambda: ALLOWED
    try:
        net = s.recovery(rows, ids, level, s.params(GATE=False, NETTING=True))
        gross = s.recovery(rows, ids, level, s.params(GATE=False, NETTING=False))
    finally:
        rec.allowed = real
    assert net["point"] < gross["point"] and net["value"] <= gross["value"]


def test_gate_decides_between_extrapolation_and_sampled_claims_only():
    import eval61_recovery as rec
    real = rec.allowed
    rec.allowed = lambda: ALLOWED
    rows = _claims(0, 100, 0)
    ids = {r["claim_id"] for r in rows[:20]}
    try:
        low = {c: (3 if i == 0 else 3) for i, c in enumerate(ids)}                                  # supported = billed: no errors
        one = dict(low)
        for c in sorted(ids)[:2]:
            one[c] = 2                                                                             # 2 of 20 = 10% error rate, below the 15% gate
        many = dict(low)
        for c in sorted(ids)[:6]:
            many[c] = 2                                                                            # 30%: gate opens
        a = s.recovery(rows, ids, one, s.params())
        b = s.recovery(rows, ids, many, s.params())
        c_off = s.recovery(rows, ids, one, s.params(GATE=False))
    finally:
        rec.allowed = real
    assert a["mode"] == "sampled claims only" and b["mode"] == "extrapolated" and c_off["mode"] == "extrapolated"
    assert a["value"] == a["point"] > 0                                                             # below the gate: exactly the sampled claims' own overpayment, no projection
    assert abs(c_off["point"] - 5 * a["point"]) < 1e-6                                                         # the projected point estimate scales 20 sampled claims to a frame of 100


def test_one_sided_bound_is_less_conservative_than_the_release_5_bound():
    assert s.t_value(10, "one_sided_90") < s.t_value(10, "two_sided_90") and abs(s.t_value(10, "one_sided_90") - 1.372) < 1e-9


def test_release_5_module_and_published_numbers_are_untouched():
    src = open(os.path.join(ROOT, "eval", "dollar_reward.py")).read()
    assert 'RECOVERY = "doc_denial"' in src and "C_COPY, C_BURDEN, C_REVIEW, C_FALSE = 90.0, 43.84, 158.0, 2000.0" in src and 'BOUND = "ci_low"' in src
    assert "score_40" not in src                                                                   # the frozen module knows nothing of score 4.0
    rows = json.load(open(os.path.join(ROOT, "experiments", "release5_dollar_results.json")))
    assert len(rows) == 21 * 10 + 0 or len(rows) > 200


def _have(code, rid):
    return os.path.isdir(os.path.join(ROOT, "data", f"synthetic_v2_{code}", f"view_{rid}")) and os.path.exists(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code}.json"))


def test_parity_with_release_5_when_gate_and_netting_are_off():
    if not _have("r4_3535", "r4a_3535"):
        print("skipped (no stored run data)")
        return
    import dollar_reward as dr
    for rid, code in (("r4a_3535", "r4_3535"), ("r4w23_3636", "r4_3636")):
        if not _have(code, rid):
            continue
        c = s.from_run(rid, code, s.params(GATE=False, NETTING=False))
        d = dr.from_run(rid, code)
        assert abs((c["recovered"] - c["recovered_from_non_upcoders"]) - d["value_downcode"]) < 1e-6, (rid, c["recovered"], d["value_downcode"])
        assert c["found"] == d["found"]


def test_release_5_published_values_reproduce_on_stored_runs():
    if not _have("r4_3535", "r4a_3535"):
        print("skipped (no stored run data)")
        return
    import dollar_reward as dr
    rows = {(r["set"], r["seed"], r["arm"]): r for r in json.load(open(os.path.join(ROOT, "experiments", "release5_dollar_results.json")))}
    for rid, code, arm in (("r4a_3535", "r4_3535", "A3.4"), ("r4gl_3636", "r4_3636", "GL")):
        pub = rows[("r4", int(code.split("_")[1]), arm)]
        now = dr.from_run(rid, code)
        assert abs(now["value"] - pub["value"]) < 1e-6 and now["found"] == pub["found"] and now["all_rounds"] == pub["all_rounds"]


def test_truth_from_claims_tracks_the_answer_key_rates():
    if not _have("r5_4545", "r5w25_4545"):
        print("skipped (no stored run data)")
        return
    code = "r5_4545"
    k = s.load_key(code)
    claims = {}
    for r in csv.DictReader(open(os.path.join(ROOT, "data", f"synthetic_v2_{code}", "view", "claims.csv"))):
        claims.setdefault(r["provider_id"], []).append(r)
    import eval61_recovery as rec
    diffs = []
    for pid, rows in claims.items():
        t = s.provider_truth(rows, k["justified_cpt_by_claim"], rec.allowed())
        v = k["providers"][pid]
        diffs.append(abs(t["net_rate"] - (v["true_upcode_rate"] - v["downcode_rate"])))
    assert sum(diffs) / len(diffs) < 0.03 and max(diffs) < 0.10          # the key counts visits before corrections and claims lag; the claims are what was billed


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
