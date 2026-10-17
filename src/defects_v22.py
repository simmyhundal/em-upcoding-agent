"""Data 2.2: inject delivered-extract defects so data-quality checks can be tested (issue 80).

The synthetic data is clean, so any data-quality check would pass trivially. These defects are applied to the plan tables after
generation, each with its own share, and every injected defect is recorded in the answer key so the checks can be graded:

  duplicates      an extra copy of a paid claim under a new claim id (double billing or a double load)
  orphans         a replacement or void whose original claim is missing from the extract
  unknown_member  a claim whose member id does not join to eligibility (members.csv)
  no_rendering    a group-billed claim with the rendering NPI left blank, so no clinician can be named
  dx truncation   `--dx-cap` in generate_v2.py (applied while the header is written)
  control totals  `control_totals.csv`: claim counts and paid dollars by service month, as the plan says it delivered (computed from the
                  clean extract); the delivered tables no longer match it after the defects above

Defaults are all zero. Own random stream, so nothing else in the data moves. Never reads or writes the agent-visible view.
"""
import csv
import os

import numpy as np

# Named defect profiles for the release 2 evaluation runs with defects (docs/release2_plan.md). "moderate" is an extract with ordinary problems
# a plan would find and fix; "severe" is the graded stress dataset of issue 80. Explicit options override a profile.
DEFECT_PROFILES = {
    "moderate": {"defect_duplicate_share": 0.005, "defect_orphan_share": 0.10, "defect_unknown_member_share": 0.003,
                 "defect_no_rendering_share": 0.02, "dx_cap": 4, "dx_cap_months": (10, 11, 12)},
    "severe": {"defect_duplicate_share": 0.01, "defect_orphan_share": 0.30, "defect_unknown_member_share": 0.005,
               "defect_no_rendering_share": 0.03, "dx_cap": 3, "dx_cap_months": (7, 8, 9, 10, 11, 12)},
}
DEFECT_OPTIONS = ("defect_duplicate_share", "defect_orphan_share", "defect_unknown_member_share", "defect_no_rendering_share")


def control_totals(headers, remit):
    """{service month: {"claims": header rows, "paid_usd": paid dollars}} over the rows given."""
    paid = {r["claim_id"]: float(r["paid_amount"]) for r in remit if r["status"] == "paid"}
    out = {}
    for h in headers:
        m = h["service_date"][:7]
        o = out.setdefault(m, {"claims": 0, "paid_usd": 0.0})
        o["claims"] += 1
        o["paid_usd"] += paid.get(h["claim_id"], 0.0)
    return {m: {"claims": v["claims"], "paid_usd": round(v["paid_usd"], 2)} for m, v in sorted(out.items())}


def write_control_totals(path, totals):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["service_month", "claims", "paid_usd"])
        for m, v in totals.items():
            w.writerow([m, v["claims"], v["paid_usd"]])


def inject(headers, lines, remit, universe, truth, cfg, rng, next_claim_number):
    """Apply the defects to the lists in place. Returns the answer-key record of what was injected."""
    n = lambda key: cfg.get(key, 0.0) or 0.0
    rec = {}
    paid_ids = {r["claim_id"] for r in remit if r["status"] == "paid"}
    children = {h["original_claim_id"] for h in headers if h["original_claim_id"]}
    lines_by = {}
    for r in lines:
        lines_by.setdefault(r["claim_id"], []).append(r)
    uni = {u["claim_id"]: u for u in universe}
    originals = [h for h in headers if h["claim_frequency"] == 1 and h["claim_id"] in paid_ids and h["claim_id"] not in children]

    # duplicates: a second paid copy under a new id
    pairs = []
    cid = next_claim_number
    if n("defect_duplicate_share") > 0:
        pick = rng.random(len(originals)) < n("defect_duplicate_share")
        paid_of = {r["claim_id"]: r for r in remit}
        for h, hit in zip(originals, pick):
            if not hit:
                continue
            cid += 1
            new = f"C{cid:07d}"
            headers.append({**h, "claim_id": new})
            lines.extend({**r, "claim_id": new} for r in lines_by[h["claim_id"]])
            remit.append({**paid_of[h["claim_id"]], "claim_id": new})
            if h["claim_id"] in uni:
                universe.append({**uni[h["claim_id"]], "claim_id": new})
            truth[new] = truth.get(h["claim_id"])
            pairs.append([new, h["claim_id"]])
        rec["duplicates"] = {"count": len(pairs), "pairs": pairs}

    dup_ids = {c for p in pairs for c in p}      # a duplicated claim and its copy stay identical in every other respect

    # orphans: remove the original of some replacements and voids
    if n("defect_orphan_share") > 0:
        by_id = {h["claim_id"]: h for h in headers}
        kids = [h for h in headers if h["claim_frequency"] in (7, 8) and h["original_claim_id"] in by_id]
        hit = rng.random(len(kids)) < n("defect_orphan_share")
        gone = {h["original_claim_id"]: h for h, x in zip(kids, hit) if x}
        headers[:] = [h for h in headers if h["claim_id"] not in gone]
        lines[:] = [r for r in lines if r["claim_id"] not in gone]
        remit[:] = [r for r in remit if r["claim_id"] not in gone]
        rec["orphans"] = {"replacements": sorted(h["claim_id"] for h in gone.values() if h["claim_frequency"] == 7),
                          "voids": sorted(h["claim_id"] for h in gone.values() if h["claim_frequency"] == 8),
                          "missing_originals": sorted(gone)}

    # unknown member: the member id no longer joins to eligibility
    if n("defect_unknown_member_share") > 0:
        cands = [h for h in headers if h["claim_frequency"] == 1 and h["claim_id"] in paid_ids and h["claim_id"] not in children
                 and h["claim_id"] not in dup_ids]
        hit = rng.random(len(cands)) < n("defect_unknown_member_share")
        ids = []
        for i, (h, x) in enumerate(zip(cands, hit)):
            if x:
                h["member_id"] = f"M9{i:06d}"
                ids.append(h["claim_id"])
        rec["unknown_member"] = {"count": len(ids), "claim_ids": ids}

    # no rendering NPI on group-billed claims
    if n("defect_no_rendering_share") > 0:
        cands = [h for h in headers if h["claim_frequency"] == 1 and h["claim_id"] in paid_ids and h["claim_id"] not in children
                 and h["billing_npi"].startswith("2") and h["rendering_npi"] and h["claim_id"] not in dup_ids]
        hit = rng.random(len(cands)) < n("defect_no_rendering_share")
        ids = []
        for h, x in zip(cands, hit):
            if x:
                h["rendering_npi"] = ""
                ids.append(h["claim_id"])
        rec["no_rendering"] = {"count": len(ids), "claim_ids": ids}
    return rec, cid
