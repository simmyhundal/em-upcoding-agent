"""Derive conditions and a risk score from claims, and collapse plan tables into the detector view.

What a plan does: map ICD-10 diagnosis codes on a member's accepted claims, across every provider the member saw during a
lookback window, to condition flags and a risk score. This module does that over the full synthetic year.

Mapping used (ILLUSTRATIVE, not CMS-HCC): the twelve chronic conditions the generator draws from, each with a made-up weight.
A real CMS-HCC or HHS-HCC mapping needs the published or licensed tables; this stand-in only demonstrates the step. The
risk score is the sum of weights over distinct conditions, and `condition_count` is the number of distinct conditions.

Circularity (state it plainly): diagnoses come from the same claims as the visit levels. A doctor who inflates diagnoses to
justify high codes would also look sicker to this step. The synthetic data does not model diagnosis inflation, so that effect
is absent here; a real screen has to live with it.

View rules (see docs/v2_schemas.md):
  * one row per visit: a replacement (frequency 7) supersedes its original; voids (8) and denied claims are dropped
  * a visit belongs to its rendering provider
  * conditions and risk come from all of a member's accepted claims, whichever provider billed them
  * the detector view carries `chronic_condition_count` (the derived condition_count), so the v1 detectors run unchanged

Reads only plan tables; never the records universe or the answer key.

Usage:
    python src/derive.py V2_DIR VIEW_DIR
"""
import csv
import os
import sys
from collections import defaultdict

# ICD-10 code -> (condition, illustrative weight). Same codes the generator draws from.
CONDITION_MAP = {
    "I10": ("hypertension", 0.10), "E11.9": ("type 2 diabetes", 0.30), "E78.5": ("hyperlipidemia", 0.05),
    "J44.9": ("COPD", 0.35), "I50.9": ("heart failure", 0.45), "N18.3": ("chronic kidney disease", 0.30),
    "F32.9": ("depression", 0.25), "E66.9": ("obesity", 0.15), "M19.90": ("osteoarthritis", 0.10),
    "J45.909": ("asthma", 0.20), "E03.9": ("hypothyroidism", 0.08), "I48.91": ("atrial fibrillation", 0.30),
}
EM_CODES = {"99211", "99212", "99213", "99214", "99215"}
TEST_CODES = {"80053", "85025"}
DX_COLS = [f"dx{i}" for i in range(1, 7)]


def _rows(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def accepted_visits(v2_dir):
    """Return {visit_id: {...}} after replacement, void and denial rules. visit_id is the original claim id."""
    header = {r["claim_id"]: r for r in _rows(os.path.join(v2_dir, "claims_header.csv"))}
    status = {r["claim_id"]: r["status"] for r in _rows(os.path.join(v2_dir, "remittance.csv"))}
    lines = defaultdict(list)
    for r in _rows(os.path.join(v2_dir, "claim_lines.csv")):
        lines[r["claim_id"]].append(r)
    voided = {h["original_claim_id"] for h in header.values() if h["claim_frequency"] == "8"}
    out = {}
    for cid, h in header.items():
        if h["claim_frequency"] == "8" or cid in voided:
            continue
        visit_id = h["original_claim_id"] or cid         # a replacement keeps its original's visit id
        if status.get(cid) != "paid":                    # denied or reversed claims do not count
            continue
        em = [x for x in lines[cid] if x["cpt"] in EM_CODES]
        if not em:
            continue
        out[visit_id] = {"claim_id": cid, "member_id": h["member_id"], "provider_id": h["rendering_npi"],
                         "service_date": h["service_date"], "cpt": em[0]["cpt"], "place_of_service": em[0]["place_of_service"],
                         "diagnosis_codes": ";".join(h[c] for c in DX_COLS if h[c]),
                         "has_test_line": any(x["cpt"] in TEST_CODES for x in lines[cid]),
                         "allowed_amount": float(em[0]["allowed_amount"]), "paid_amount": float(em[0]["paid_amount"])}
    return out


def derive_members(visits):
    """member_id -> {conditions, condition_count, risk_score}, from diagnosis codes on the member's accepted visits."""
    seen = defaultdict(set)
    for v in visits.values():
        for code in v["diagnosis_codes"].split(";"):
            if code in CONDITION_MAP:
                seen[v["member_id"]].add(code)
    return {m: {"conditions": ";".join(CONDITION_MAP[c][0] for c in sorted(codes)),
                "condition_count": len(codes), "risk_score": round(sum(CONDITION_MAP[c][1] for c in codes), 2)}
            for m, codes in seen.items()}


def build_view(v2_dir, view_dir):
    """Write providers.csv, patients.csv, claims.csv (v1 shapes, derived from plan tables) to view_dir."""
    os.makedirs(view_dir, exist_ok=True)
    visits = accepted_visits(v2_dir)
    derived = derive_members(visits)
    members = {r["member_id"]: r for r in _rows(os.path.join(v2_dir, "members.csv"))}
    n_claims, pats = defaultdict(int), defaultdict(set)
    for v in visits.values():
        n_claims[v["provider_id"]] += 1
        pats[v["provider_id"]].add(v["member_id"])
    used = sorted({v["member_id"] for v in visits.values()})
    with open(os.path.join(view_dir, "patients.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["patient_id", "provider_id", "age", "chronic_condition_count", "conditions", "risk_score"])
        for m in used:
            d = derived.get(m, {"conditions": "", "condition_count": 0, "risk_score": 0.0})
            w.writerow([m, members[m]["pcp_npi"], 2024 - int(members[m]["birth_year"]), d["condition_count"],
                        d["conditions"], d["risk_score"]])
    with open(os.path.join(view_dir, "providers.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["provider_id", "specialty", "state", "n_claims", "n_patients"])
        for r in _rows(os.path.join(v2_dir, "providers.csv")):
            w.writerow([r["npi"], r["specialty"], r["state"], n_claims.get(r["npi"], 0), len(pats.get(r["npi"], ()))])
    with open(os.path.join(view_dir, "claims.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["claim_id", "provider_id", "patient_id", "service_date", "cpt", "place_of_service", "diagnosis_codes",
                    "has_test_line", "allowed_amount", "paid_amount"])
        for vid in sorted(visits):
            v = visits[vid]
            w.writerow([vid, v["provider_id"], v["member_id"], v["service_date"], v["cpt"], v["place_of_service"],
                        v["diagnosis_codes"], int(v["has_test_line"]), v["allowed_amount"], v["paid_amount"]])
    return len(visits)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    print(f"{build_view(sys.argv[1], sys.argv[2])} visits -> {sys.argv[2]}")
