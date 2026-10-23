"""Score 4.2: recovery with records not provided, stratified recovery, the claims-data lane's screen, and consistency with the score 4.0 adapter. Run: python tests/test_score_42.py"""
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import fwa_lane  # noqa: E402
import recovery_42 as r42  # noqa: E402


def rows(n, paid="100", allowed="120", cpt="99214"):
    return [{"claim_id": f"C{i}", "cpt": cpt, "allowed_amount": allowed, "paid_amount": paid, "service_date": "2024-01-0%d" % (1 + i % 9)} for i in range(n)]


def test_commercial_profile_has_no_copy_fee():
    p = r42.params42()
    assert p["C_COPY"] == 0.0 and p["C_BURDEN"] == 43.84
    import recovery_40 as r4
    assert r4.PARAMS["C_COPY"] == 90.0, "score 4.0 must stay frozen"


def test_stratified_recovery_by_hand():
    # 10 claims in the stratum, sample C0..C3: three NO_RECORD (paid 100 each), one charted at its billed level (0 overpaid)
    # values 100,100,100,0: mean 75, point 10*75 = 750; s2 = 2500; var = 100*(1-4/10)*2500/4 = 37500; half = t(3 df, two-sided 90%) * sqrt(37500)
    import pi_estimate as pe
    p = r42.params42()
    e = r42.recovery_stratified(rows(10), ["C0", "C1", "C2", "C3"], {"C3": 3}, p, no_record={"C0", "C1", "C2"})
    assert abs(e["point"] - 750.0) < 1e-9 and e["mode"] == "extrapolated" and e["no_record"] == 3
    half = pe.t_crit(3, 0.90) * 37500 ** 0.5
    assert abs(e["value"] - (750.0 - half)) < 1e-6


def test_no_record_only_counts_when_reported():
    p = r42.params42()
    e = r42.recovery_stratified(rows(10), ["C0", "C1", "C2", "C3"], {"C3": 3}, p, no_record=set())
    assert e["reviewed"] == 1 and e["value"] == 0.0           # the three silent claims count for nothing


def test_gate_below_error_rate_recovers_only_the_sampled_claims():
    p = r42.params42()
    e = r42.recovery_stratified(rows(40), [f"C{i}" for i in range(10)], {f"C{i}": 3 for i in range(1, 10)}, p, no_record={"C0"})
    assert e["mode"] == "sampled claims only" and abs(e["value"] - 100.0) < 1e-9   # 1 of 10 overpaid (10% < the 15% gate): only that claim's own $100


def test_level_recovery_matches_score_40_when_no_claim_is_missing():
    import recovery_40 as r4
    p4, p2 = r4.params(), r42.params42()
    claims = [{"claim_id": f"C{i}", "cpt": "99215", "allowed_amount": "200", "paid_amount": "160", "service_date": "2024-01-01"} for i in range(60)]
    level = {f"C{i}": (2 if i % 2 == 0 else 4) for i in range(60)}       # half supported at 99213, half at 99215
    ids = [f"C{i}" for i in range(30)]
    a, b = r4.recovery(claims, ids, level, p4), r42.recovery(claims, ids, level, p2)
    assert abs(a["value"] - b["value"]) < 1e-9 and abs(a["point"] - b["point"]) < 1e-9


def test_volume_screen_flags_busiest_day_at_or_above_the_cap():
    def day(n, d):
        return [{"claim_id": f"{d}-{i}", "service_date": d} for i in range(n)]
    cb = {"A": day(29, "2024-01-01") + day(5, "2024-01-02"), "B": day(30, "2024-03-01") + day(31, "2024-03-02"), "C": day(50, "2024-05-05")}
    out = fwa_lane.flag(cb, day_max=30)
    assert [t[0] for t in out] == ["C", "B"] and out[1][2] == ["2024-03-01", "2024-03-02"]
    assert fwa_lane.flag(cb, day_max=30, max_flagged=1)[0][0] == "C"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
