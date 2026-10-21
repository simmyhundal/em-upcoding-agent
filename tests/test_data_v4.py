"""Data 4.0 (issue 124): exactly 8 upcoders with net rates in the band, non-upcoder means in range, each habit leaves its signature, the key never reaches the view, and the key's true overpayment
equals score 4.0's truth computed from the claims. Builds two development seeds (about 15 seconds each). Run: python tests/test_data_v4.py"""
import csv
import json
import os
import shutil
import sys
import tempfile
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import derive  # noqa: E402
import eval61_recovery as rec  # noqa: E402
import generate_v2  # noqa: E402
import records  # noqa: E402
import score_40 as s4  # noqa: E402

_CACHE = {}
LV = {"99211": 0, "99212": 1, "99213": 2, "99214": 3, "99215": 4}


def dataset(seed):
    if seed not in _CACHE:
        tmp = tempfile.mkdtemp()
        out, key = os.path.join(tmp, "data"), os.path.join(tmp, "key", "key.json")
        generate_v2.build(out, key, seed=seed, n_providers=216, n_upcoders=8, n_hard_neg=8, clone_share=0.125, data_version="4.0")
        derive.build_view(out, os.path.join(out, "view"))
        claims = {}
        for r in csv.DictReader(open(os.path.join(out, "view", "claims.csv"))):
            claims.setdefault(r["provider_id"], []).append(r)
        _CACHE[seed] = (out, json.load(open(key)), claims)
    return _CACHE[seed]


def test_eight_upcoders_with_net_rates_in_the_band_and_non_upcoder_means_in_range():
    for seed in (42, 1515):
        out, k, claims = dataset(seed)
        P = k["providers"]
        ups = [p for p, v in P.items() if v["role"] == "upcoder"]
        assert len(ups) == 8 and sum(v["role"] == "hard_negative" for v in P.values()) == 8
        assert Counter(P[p]["habit"] for p in ups) == Counter(k["habit_counts"]) and k["habit_counts"] == {"systematic": 3, "opportunistic": 3, "template": 2}
        for p in ups:
            r = s4.provider_truth(claims[p], k["justified_cpt_by_claim"], rec.allowed())["net_rate"]
            assert 0.15 <= r <= 0.40, (seed, p, P[p]["habit"], r)                # on the live claims of the view, the basis of score 4.0
            assert abs(r - P[p]["target_net_rate"]) < 0.03
        for p, v in P.items():
            if v["role"] != "upcoder":
                assert -0.15 <= v["mean_net_rate"] <= 0.15 and v["habit"] is None
                assert abs(s4.provider_truth(claims[p], k["justified_cpt_by_claim"], rec.allowed())["net_rate"] - v["mean_net_rate"]) < 0.10     # small panels are noisy


def test_the_key_does_not_reach_the_view_and_matches_score_40_truth():
    out, k, claims = dataset(42)
    assert not os.path.commonpath([out, os.path.join(os.path.dirname(out), "key")]) == out
    cols = next(iter(csv.reader(open(os.path.join(out, "view", "claims.csv")))))
    assert cols == ["claim_id", "provider_id", "patient_id", "service_date", "cpt", "place_of_service", "diagnosis_codes", "has_test_line", "allowed_amount", "paid_amount"]
    blob = "".join(open(os.path.join(out, "view", f)).read()[:200000] for f in ("claims.csv", "providers.csv", "patients.csv"))
    assert "habit" not in blob and "upcoder" not in blob and "systematic" not in blob
    for pid in list(k["providers"])[:30]:
        t = s4.provider_truth(claims[pid], k["justified_cpt_by_claim"], rec.allowed())
        assert abs(t["net_overpay"] - k["providers"][pid]["true_overpay_net"]) < 1.0, pid
    assert all(r["claim_id"] in k["justified_cpt_by_claim"] for rows in claims.values() for r in rows)


def _doc_level(u):
    return max(records.mdm_level(int(u["problems_level"]), int(u["data_level"]), int(u["risk_level"])), records.level_from_minutes(u["documented_minutes"]))


def test_each_habit_leaves_its_signature():
    out, k, claims = dataset(42)
    P = k["providers"]
    uni = {r["claim_id"]: r for r in csv.DictReader(open(os.path.join(out, "records", "records_universe.csv")))}
    notes = {r["claim_id"]: r for r in csv.DictReader(open(os.path.join(out, "records", "visit_notes.csv")))}
    audit = {r["note_id"]: r for r in csv.DictReader(open(os.path.join(out, "records", "audit_trail.csv")))}
    J = k["justified_cpt_by_claim"]
    for pid, v in P.items():
        if v["role"] != "upcoder":
            continue
        rows = claims[pid]
        up = [r for r in rows if LV[r["cpt"]] > LV[J[r["claim_id"]]]]
        shows = sum(_doc_level(uni[r["claim_id"]]) < LV[r["cpt"]] for r in up) / len(up)
        if v["habit"] == "systematic":
            lvl2 = [r for r in rows if J[r["claim_id"]] == "99213"]
            assert sum(r["cpt"] == "99214" for r in lvl2) / len(lvl2) > 0.9            # always 99214 for 99213-level visits (up to coding noise)
            assert shows > 0.6                                                        # the chart shows it
        elif v["habit"] == "opportunistic" and not v["clones_notes"]:
            padded = [r for r in up if uni[r["claim_id"]]["documented_minutes"] != ""]
            near = sum(0 <= int(uni[r["claim_id"]]["documented_minutes"]) - records.MIN_FLOOR[LV[r["cpt"]]] <= 2 for r in padded) / max(len(padded), 1)
            assert near > 0.5                                                         # minutes just over the cutoff
            assert shows < 0.6                                                        # padding and risk inflation defeat part of the chart review
        elif v["habit"] == "template":
            assert v["uses_template"] and not v["clones_notes"]
            tids = Counter(audit["N" + r["claim_id"][1:]]["template_id"] for r in rows if ("N" + r["claim_id"][1:]) in audit)
            assert tids.most_common(1)[0][1] / sum(tids.values()) > 0.9              # shared boilerplate across patients
            paste = [int(audit["N" + r["claim_id"][1:]]["copy_paste_events"]) for r in rows[:200] if ("N" + r["claim_id"][1:]) in audit]
            assert sum(paste) / len(paste) < 2.5                                      # no paste-heavy notes: tellable from deliberate cloning
            assert shows > 0.6
    cl = [p for p, v in P.items() if v["clones_notes"]]
    assert len(cl) == 1 and P[cl[0]]["role"] == "upcoder"                             # 10 to 20% of upcoders clone: 1 of 8
    assert k["members_seen_by_two_or_more_providers"] > 0.25                          # patients shared across providers


def test_data_2x_is_untouched():
    import test_generator_regression as t
    t.test_data_2x_reproduces()


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    for tmp in {os.path.dirname(v[0]) for v in _CACHE.values()}:
        shutil.rmtree(tmp, ignore_errors=True)
