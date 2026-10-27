"""Score 4.3: collected dollars, the dollar gate, the referral class and the staff cost, checked by hand, and consistency with score 4.2 when every 4.3 change is switched off. Run: python tests/test_score_43.py"""
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import recovery_40 as r4  # noqa: E402
import recovery_43 as r43  # noqa: E402


def test_defaults_are_the_signed_off_values():
    p = r43.params43()
    assert (p["COLLECTION_REFERRAL"], p["COLLECTION_DEMAND"], p["APPEAL_REDUCTION"], p["REFERRAL_COST"], p["GATE_UNIT"], p["GATE_DOLLAR_RATE"], p["C_COPY"]) == (0.25, 0.68, 0.15, 4000.0, "dollar", 0.05, 0.0)


def test_collected_by_hand():
    p = r43.params43()
    assert abs(r43.collected(10000.0, p) - 5780.0) < 1e-9            # 10,000 x (1 - 15%) x 68%
    assert abs(r43.collected(10000.0, p, referral=True) - 2500.0) < 1e-9    # a referral's rate is net of appeals: 10,000 x 25%


def _rows(n):
    return [{"claim_id": f"C{i}", "cpt": "99214", "allowed_amount": "120", "paid_amount": "100", "service_date": "2024-01-01"} for i in range(n)]


def test_dollar_gate_by_hand():
    p = r43.params43()
    v = r4.overpay_signed("99214", "99213", r4.allowed(), (120.0, 100.0))        # one claim billed 99214 and supported at 99213
    assert v > 0
    rows = _rows(100)
    ids = [f"C{i}" for i in range(10)]
    for k, want in ((1, "sampled claims only"), (2, "extrapolated"), (4, "extrapolated")):
        level = {c: (2 if i < k else 3) for i, c in enumerate(ids)}             # k claims supported one level lower, the rest as billed
        e = r43.recovery(rows, ids, level, p)
        share = k * v / (10 * 100.0)                                            # net overpayment over the sample's paid dollars
        assert (share >= 0.05) == (want == "extrapolated"), (k, share)
        assert e["mode"] == want, (k, e["mode"], share)
    claim = r43.params43(GATE_UNIT="claim")                                     # score 4.2's gate: 15% of claims overpaid
    one = {c: (2 if i < 1 else 3) for i, c in enumerate(ids)}                   # 1 of 10 claims: 10% of claims, below 15%
    two = {c: (2 if i < 2 else 3) for i, c in enumerate(ids)}                   # 2 of 10: 20%, above
    assert r43.recovery(rows, ids, one, claim)["mode"] == "sampled claims only" and r43.recovery(rows, ids, two, claim)["mode"] == "extrapolated"


def test_staff_cost_adds_referral_and_appeal_handling():
    p = r43.params43()
    total, parts = r43.staff_cost(0, 0, 0, 0, 1, 0.0, p)
    assert abs(parts["referrals"] - 4000.0) < 1e-9
    assert abs(parts["appeal handling"] - 1 * 0.17 * 3.0 * r4.hourly("coder", p)) < 1e-9
    total2, _ = r43.staff_cost(0, 0, 0, 1, 0, 0.0, p)
    assert abs(total2 - (r4.staff_cost(0, 0, 0, 1, 0, p)[0] + 0.17 * 3.0 * r4.hourly("coder", p))) < 1e-9


def test_consistent_with_score_42_when_every_change_is_off():
    rid, code = "d42wlh28_1001", "d42_1001"
    if not os.path.isdir(os.path.join(ROOT, "experiments", rid)) or not os.path.isdir(os.path.join(ROOT, "data", f"synthetic_v2_{code}")):
        print("skip: d42_1001 and its stored run are not built")
        return
    import score_42 as s42
    import score_43 as s43
    p = r43.params43(APPEAL_REDUCTION=0.0, COLLECTION_DEMAND=1.0, COLLECTION_REFERRAL=1.0, REFERRAL_COST=r4.staff_cost(0, 0, 0, 1, 0, r43.params43())[0], P_APPEAL=0.0, GATE_UNIT="claim")
    a = s43.seed_result(rid, code, p)[0]["score"]
    b = s42.seed_result(rid, code)[0]["score"]
    assert abs(a - b) < 0.5, (a, b)


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
