"""Payment Integrity case packet: what the PI team needs after an investigator decides to pursue a provider.

For each selected provider this writes, under OUT_DIR/<provider>/:
  dossier.md               provider facts, why flagged, the case summary, evidence chart, documentation review, limits
  record_request_list.csv  a seeded random sample of the provider's billed claims to request records for
  sampling_plan.md + plan.json   frame, sample sizes, seed, formula, and how the estimate is computed (see pi_estimate.py)
  (with --example) reviewed_example.csv + example_estimate.md   a SIMULATED review, built from the synthetic
                           documentation sample, to show the arithmetic end to end
and OUT_DIR/tracker.csv, a status row per provider.

This is draft material for human review. It does not make findings, draft demand letters, or decide payment
suspension or referral; those need people and legal review. Uses only agent-visible files, never the answer key.

Usage:
    python src/pi_packet.py DATA_DIR FLAGGED_CSV CHECKED_SUMMARIES_JSONL CHARTS_DIR ALLOWED_JSON OUT_DIR
        [--select upcoding|all] [--codes 99215,99214] [--margin 0.10] [--confidence 0.90] [--example]
"""
import argparse
import csv
import json
import math
import os
import random

import case_summary as cs
import pi_estimate as pe

CENSUS_MAX = 30          # frames this small are reviewed in full
Z = {0.90: 1.645, 0.95: 1.960}
TRACKER_COLUMNS = ["provider_id", "status", "requested_on", "records_received", "reviewed", "notice_sent", "resolved", "notes"]
REQUEST_COLUMNS = ["claim_id", "service_date", "patient_id", "patient_age", "billed_cpt", "diagnosis_codes",
                   "place_of_service", "date_requested", "date_received", "status"]


def sample_size(N, margin=0.10, confidence=0.90, p=0.5):
    """Sample size for a proportion within +/- margin, with finite population correction. Small frames: census."""
    if N <= CENSUS_MAX:
        return N
    n0 = Z[confidence] ** 2 * p * (1 - p) / margin ** 2
    return min(N, math.ceil(n0 / (1 + (n0 - 1) / N)))


def make_plan(pid, claims, codes, margin, confidence):
    rng = random.Random(f"pi-v1:{pid}")
    frame = {c: sorted(r["claim_id"] for r in claims if r["cpt"] == c) for c in codes}
    sizes, sampled = {}, {}
    for c, ids in frame.items():
        n = sample_size(len(ids), margin, confidence) if ids else 0
        sizes[c] = n
        for cid in rng.sample(ids, n):
            sampled[cid] = c
    return {"provider_id": pid, "seed": f"pi-v1:{pid}", "margin": margin, "confidence": confidence, "census_max": CENSUS_MAX,
            "frame_sizes": {c: len(v) for c, v in frame.items()}, "sample_sizes": sizes, "sampled_claims": sampled}


def plan_markdown(plan, allowed):
    rows = [f"| {c} | {plan['frame_sizes'][c]} | {plan['sample_sizes'][c]} | "
            f"{'all claims (frame is small)' if plan['frame_sizes'][c] <= plan['census_max'] else 'random sample'} |"
            for c in plan["frame_sizes"]]
    amts = ", ".join(f"{c} ${v['allowed_amount']:.2f}" for c, v in allowed["codes"].items())
    return "\n".join([
        f"# Sampling plan for {plan['provider_id']}", "",
        "| Billed code | Claims in frame | Claims to review | Method |", "|---|---|---|---|", *rows, "",
        f"- Seed `{plan['seed']}` (the sample is reproducible).",
        f"- Size rule: proportion within +/-{plan['margin']:.0%} at {plan['confidence']:.0%} confidence, assuming 50% "
        f"(the conservative case), with finite-population correction; frames of {plan['census_max']} or fewer are reviewed in full.",
        "",
        "## After the records come back",
        "1. A reviewer fills `supported_cpt` for each requested claim in a copy of `record_request_list.csv` "
        "(blank = records not received / not reviewed).",
        "2. Run `python src/pi_estimate.py plan.json reviewed.csv ALLOWED_JSON` to extrapolate an overpayment estimate "
        "with a confidence interval.",
        f"- Allowed amounts used (GA Family Practice average, CMS public file): {amts}. Real recoupment uses each claim's actual allowed amount.",
        "- Per-claim overpayment = allowed(billed) - allowed(supported) when the supported level is lower; underbilling is ignored.",
        "- The estimate is only as good as the review. Missing records, a non-random sample or a wrong frame change the answer."]) + "\n"


def dossier(packet, flag_row, record, chart_rel, plan):
    s, chk = record["summary"], record["citation_check"]
    docs = packet.get("documentation_review")
    lines = [f"# Payment Integrity dossier: {packet['provider_id']}", "",
             "> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal "
             "review is needed before any provider contact, notice or recoupment.", "",
             "## Provider overview", "",
             "| | |", "|---|---|",
             f"| Specialty / state | {packet['specialty']}, {packet['state']} (synthetic) |",
             f"| Claims / patients | {packet['n_claims']:,} / {packet['n_patients']:,} |",
             f"| Billed mix (99211 to 99215) | " + " / ".join(f"{packet['billed_mix'][c]:,}" for c in pe.CODES) + " |",
             f"| 99215 share | {packet['share_99215']:.1%} |",
             f"| Expected 99215 share given patient complexity | {packet['expected_share_given_patient_complexity']:.1%} |",
             f"| Screen scores | z vs peers {packet['z_vs_peers']:.2f}; risk-adjusted {packet['risk_adjusted_score']:.2f}; flagged by {packet['flagged_by']} |",
             "", "## Case summary (advisory)", "",
             f"**{s['headline']}**", "", f"Leaning: {cs_label(s['leaning'])}. Citations checked: {chk['n_valid']}/{chk['n_cited']} valid.", "",
             s["rationale"], "", "## Evidence chart", "", f"![99215 share by patient complexity]({chart_rel})", ""]
    if docs:
        lines += ["## Records-review sample so far", "",
                  f"Documentation is on file for {docs['claims_with_documentation']:,} claims "
                  f"({docs['share_of_claims_documented']:.0%} of this provider's claims).", "",
                  "| Billed | Documented | Documentation below billed level | Rate | All-provider rate |", "|---|---|---|---|---|"]
        for t in docs["by_billed_level"]:
            ap = t["all_provider_unsupported_rate"]
            lines.append(f"| {t['billed_cpt']} | {t['documented_claims']} | {t['documentation_does_not_support_billed_level']} | "
                         f"{t['unsupported_rate']:.1%} | {'n/a' if ap is None else f'{ap:.1%}'} |")
        lines.append("")
    lines += ["## Recommended next steps for Payment Integrity", "",
              f"1. Request records for the sampled claims in `record_request_list.csv` "
              f"({sum(plan['sample_sizes'].values())} claims across {', '.join(plan['frame_sizes'])}).",
              "2. Review the records against E/M documentation rules and record the supported level for each claim.",
              "3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).",
              "4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for "
              "the PI team, compliance and counsel. Nothing here drafts those.",
              "", "Suggested follow-ups from the case summary:", ""] + [f"- {x}" for x in s["next_steps"]]
    lines += ["", "## Limits", "",
              "- Synthetic data; no real claims or providers.",
              "- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.",
              "- The records-review sample is partial and was simulated for this project.",
              "- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments."]
    return "\n".join(lines) + "\n"


def cs_label(lean):
    return {"pattern_consistent_with_upcoding": "pattern consistent with upcoding",
            "pattern_consistent_with_high_acuity_panel": "pattern consistent with a high-acuity panel",
            "inconclusive": "inconclusive"}.get(lean, lean)


def simulate_review(plan, docs):
    """SIMULATED review: supported level = documented level where documentation exists, else blank."""
    out = {}
    for cid in plan["sampled_claims"]:
        out[cid] = pe.CODES[docs[cid][0]] if cid in docs else ""
    return out


def build(data_dir, flagged_csv, checked_path, charts_dir, allowed_path, out_dir, select="upcoding",
          codes=("99215",), margin=0.10, confidence=0.90, example=False):
    chronic, age, conditions, claims = cs.load(data_dir)
    docs = cs.load_docs(data_dir)
    rates, peer_doc = cs.peer_rates(claims, chronic), (cs.doc_peer_rates(claims, docs) if docs else None)
    allowed_doc = json.load(open(allowed_path))
    allowed = {c: v["allowed_amount"] for c, v in allowed_doc["codes"].items()}
    flags = {r["provider_id"]: r for r in csv.DictReader(open(flagged_csv))}
    records = [json.loads(line) for line in open(checked_path) if line.strip()]
    if select == "upcoding":
        records = [r for r in records if r["citation_check"]["passed"]
                   and r["summary"]["leaning"] == "pattern_consistent_with_upcoding"]
    os.makedirs(out_dir, exist_ok=True)
    tracker = []
    for rec in records:
        pid = rec["provider_id"]
        pdir = os.path.join(out_dir, pid)
        os.makedirs(pdir, exist_ok=True)
        plan = make_plan(pid, claims[pid], list(codes), margin, confidence)
        by_id = {r["claim_id"]: r for r in claims[pid]}
        with open(os.path.join(pdir, "record_request_list.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=REQUEST_COLUMNS)
            w.writeheader()
            for cid in sorted(plan["sampled_claims"]):
                r = by_id[cid]
                w.writerow({"claim_id": cid, "service_date": r["service_date"], "patient_id": r["patient_id"],
                            "patient_age": age[r["patient_id"]], "billed_cpt": r["cpt"], "diagnosis_codes": r["diagnosis_codes"],
                            "place_of_service": r["place_of_service"], "status": "not requested"})
        json.dump(plan, open(os.path.join(pdir, "plan.json"), "w"), indent=1)
        open(os.path.join(pdir, "sampling_plan.md"), "w").write(plan_markdown(plan, allowed_doc))
        packet = cs.build_packet(pid, flags[pid], chronic, age, conditions, claims, rates, docs, peer_doc)
        chart_rel = os.path.relpath(os.path.join(charts_dir, f"{pid}.svg"), pdir)
        open(os.path.join(pdir, "dossier.md"), "w").write(dossier(packet, flags[pid], rec, chart_rel, plan))
        if example and docs:
            reviewed = simulate_review(plan, docs)
            with open(os.path.join(pdir, "reviewed_example.csv"), "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["claim_id", "supported_cpt"])
                for cid in sorted(reviewed):
                    w.writerow([cid, reviewed[cid]])
            res = pe.estimate(plan, reviewed, allowed, confidence)
            open(os.path.join(pdir, "example_estimate.md"), "w").write(
                "# SIMULATED worked example (not a real review)\n\nSupported levels come from the synthetic documentation "
                "sample; sampled claims without documentation count as records not received.\n\n```\n"
                + pe.render(pid, res) + "\n```\n")
        tracker.append({"provider_id": pid, "status": "not started", "notes": ""})
    with open(os.path.join(out_dir, "tracker.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=TRACKER_COLUMNS)
        w.writeheader()
        for t in tracker:
            w.writerow({**{c: "" for c in TRACKER_COLUMNS}, **t})
    return [r["provider_id"] for r in records]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for name in ("data_dir", "flagged_csv", "checked_summaries", "charts_dir", "allowed_json", "out_dir"):
        ap.add_argument(name)
    ap.add_argument("--select", default="upcoding", choices=["upcoding", "all"])
    ap.add_argument("--codes", default="99215")
    ap.add_argument("--margin", type=float, default=0.10)
    ap.add_argument("--confidence", type=float, default=0.90, choices=[0.90, 0.95])
    ap.add_argument("--example", action="store_true")
    a = ap.parse_args()
    done = build(a.data_dir, a.flagged_csv, a.checked_summaries, a.charts_dir, a.allowed_json, a.out_dir, a.select,
                 tuple(a.codes.split(",")), a.margin, a.confidence, a.example)
    print(f"{len(done)} packets -> {a.out_dir}: {' '.join(done)}")
