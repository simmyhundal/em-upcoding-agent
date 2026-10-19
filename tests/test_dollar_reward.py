"""The dollar reward and its recovery model (issue 109, release 5). Run: python tests/test_dollar_reward.py"""
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "eval"))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import dollar_reward as dr  # noqa: E402


def claims(n=40):
    rows = []
    for i in range(n):
        rows.append({"claim_id": f"C{i:03d}", "provider_id": "P", "patient_id": f"M{i:03d}", "cpt": "99215" if i < 30 else "99213", "service_date": "2024-03-01", "diagnosis_codes": "I10",
                     "has_test_line": "0", "allowed_amount": "170.0", "paid_amount": "136.0"})
    return rows


def words(cid):
    import random
    rng = random.Random(cid)
    return " ".join("".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(6)) for _ in range(30))        # 30 different words per note: no duplicated text


def note(cid, signed="2024-03-02", problems_addressed="I10", text=None):
    return {"claim_id": cid, "note_id": "N" + cid, "note_text": text or words(cid), "problems_addressed": problems_addressed,
            "documented_problems_level": "1", "documented_data_level": "1", "documented_mdm_level": "moderate", "documented_minutes": "", "outside_records_reviewed": "0",
            "service_date": "2024-03-01", "signed_date": signed, "auth_status": "signed", "order_count": "0", "results_present": "0", "created_ts": "", "last_edited_ts": "",
            "copy_paste_events": "", "template_id": ""}


def test_documentation_denial_adds_value_only_for_flagged_99215_and_never_reduces_it():
    cl = claims()
    ids = [f"C{i:03d}" for i in range(20)]
    level = {c: 3 for c in ids}                                              # every chart supports 99214: a level difference on each 99215
    clean = {c: note(c) for c in ids}
    late = {c: note(c, signed="2024-03-30") if i % 2 == 0 else note(c) for i, c in enumerate(ids)}       # half signed late
    base = dr.point_estimate("P", cl, set(ids), level, clean, "downcode")
    assert base > 0
    assert dr.point_estimate("P", cl, set(ids), level, clean, "doc_denial") == base                    # no sign, no denial
    denied = dr.point_estimate("P", cl, set(ids), level, late, "doc_denial")
    assert denied > base                                                                                # flagged claims are denied in full
    assert dr.flagged_notes(late, {r["claim_id"]: r for r in cl}) == {c for i, c in enumerate(ids) if i % 2 == 0}


def test_duplicate_text_flags_notes_and_the_bound_is_below_the_point_estimate():
    cl = claims()
    ids = [f"C{i:03d}" for i in range(20)]
    same = {c: note(c, text="patient with multiple chronic conditions presents for comprehensive review of complex problems and prescription drug management " * 2) for c in ids}
    assert dr.flagged_notes(same, {r["claim_id"]: r for r in cl}) == set(ids)
    level = {c: 3 for c in ids}
    low = dr.point_estimate("P", cl, set(ids), level, same, "doc_denial")
    old = dr.BOUND
    dr.BOUND = "point"
    try:
        point = dr.point_estimate("P", cl, set(ids), level, same, "doc_denial")
    finally:
        dr.BOUND = old
    assert 0 <= low <= point


def test_no_random_charts_means_no_value():
    cl = claims()
    assert dr.point_estimate("P", cl, set(), {}, {}, "doc_denial") == 0.0


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
