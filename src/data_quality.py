"""Data-quality pre-flight (issue 81): checks on the delivered plan extract, run once per data load before any screen.

It reads the delivered plan tables (claims_header, claim_lines, remittance, members, providers) and, if present, the plan's
control totals (`control_totals.csv`). It never reads an answer key. Each check returns a status of ok, warn or block, the
numbers behind it and a plain sentence; the report also carries global flags and per-provider flags so a finding can be
weakened or held ("38% of this provider's claims lacked a rendering NPI").

Checks (thresholds are fixed here, calibrated only on clean data, see docs/data_quality.md):
  control_totals   delivered claims and paid dollars by service month against the plan's control totals
  em_mix           delivered E/M level mix against the Family Practice benchmark (informational: a large gap is a warning to look)
  dx_per_claim     diagnosis codes per claim, by month; a pile-up at a maximum below the extract's column count suggests truncation
  rendering_npi    share of claims with a blank rendering NPI; a blank under an organizational biller cannot be attributed to a clinician
  member_join      share of claims whose member id joins to eligibility
  duplicates       paid claims identical in member, date, biller, diagnoses and E/M line under different claim ids
  chains           replacement and void claims whose original is missing from the extract
  claims_lag       the latest months against earlier months (immature recent months)

The agent never requests data from the plan; a person does. A suspected extract problem holds or lowers the confidence of the findings
that depend on it (`hold_decision`).

Usage:
    python src/data_quality.py V2_DIR [--out RUN_DIR]       # prints the report; writes RUN_DIR/data_quality.json when --out is given
"""
import csv
import json
import os
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EM = ("99211", "99212", "99213", "99214", "99215")
DX_COLS = [f"dx{i}" for i in range(1, 7)]
CONTROL_WARN, CONTROL_BLOCK = 0.001, 0.05           # relative difference in claims or dollars in any month
MIX_TVD_WARN = 0.15                                  # total variation distance from the benchmark mix
CAP_MIN_SHARE = 0.15                                 # share of a month's claims at its maximum diagnosis count, below the column count
UNATTRIBUTED_WARN, UNATTRIBUTED_BLOCK = 0.005, 0.20
JOIN_WARN, JOIN_BLOCK = 0.999, 0.90
DUPLICATE_WARN = 0.004                               # natural collisions in clean synthetic data are about 0.1% (docs/data_quality.md)
ORPHAN_WARN = 0.0
LAG_RATIO_WARN = 0.7
PROVIDER_SHARE_FLAG = 0.02                           # per-provider flags: share of claims, with at least MIN_CLAIMS_FLAG claims
MIN_CLAIMS_FLAG = 3
PROVIDER_CAP_SHARE = 0.25
ORDER = {"ok": 0, "not_available": 0, "warn": 1, "block": 2}


def _rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def _check(cid, title, status, detail, numbers=None):
    return {"id": cid, "title": title, "status": status, "detail": detail, "numbers": numbers or {}}


def _pct(x):
    return f"{100 * x:.1f}%"


def load(v2_dir):
    t = {"headers": _rows(os.path.join(v2_dir, "claims_header.csv")), "lines": _rows(os.path.join(v2_dir, "claim_lines.csv")),
         "remit": _rows(os.path.join(v2_dir, "remittance.csv")), "members": {r["member_id"] for r in _rows(os.path.join(v2_dir, "members.csv"))},
         "npis": {r["npi"] for r in _rows(os.path.join(v2_dir, "providers.csv"))}}
    path = os.path.join(v2_dir, "control_totals.csv")
    t["control"] = ({r["service_month"]: {"claims": int(r["claims"]), "paid_usd": float(r["paid_usd"])} for r in _rows(path)}
                    if os.path.exists(path) else None)
    return t


def check_control_totals(t):
    if t["control"] is None:
        return _check("control_totals", "Control totals", "not_available", "No control totals file was delivered, so claim counts and paid dollars cannot be reconciled.")
    paid = {r["claim_id"]: float(r["paid_amount"]) for r in t["remit"] if r["status"] == "paid"}
    got = defaultdict(lambda: {"claims": 0, "paid_usd": 0.0})
    for h in t["headers"]:
        g = got[h["service_date"][:7]]
        g["claims"] += 1
        g["paid_usd"] += paid.get(h["claim_id"], 0.0)
    bad, worst = {}, 0.0
    for m in sorted(set(t["control"]) | set(got)):
        c, d = t["control"].get(m, {"claims": 0, "paid_usd": 0.0}), got.get(m, {"claims": 0, "paid_usd": 0.0})
        rc = (d["claims"] - c["claims"]) / max(c["claims"], 1)
        rd = (d["paid_usd"] - c["paid_usd"]) / max(c["paid_usd"], 1.0)
        worst = max(worst, abs(rc), abs(rd))
        if abs(rc) > CONTROL_WARN or abs(rd) > CONTROL_WARN:
            bad[m] = {"claims_control": c["claims"], "claims_delivered": d["claims"], "claims_diff": d["claims"] - c["claims"],
                      "paid_usd_diff": round(d["paid_usd"] - c["paid_usd"], 2)}
    status = "block" if worst > CONTROL_BLOCK else ("warn" if bad else "ok")
    detail = ("Delivered claims and paid dollars match the control totals in every month." if not bad else
              f"{len(bad)} of {len(t['control'])} months differ from the control totals; the largest relative difference is {_pct(worst)}.")
    return _check("control_totals", "Control totals", status, detail, {"months_mismatched": bad, "worst_relative_difference": round(worst, 5)})


def check_em_mix(t):
    path = os.path.join(ROOT, "data", "baselines", "em_specialty_baselines.json")
    if not os.path.exists(path):
        return _check("em_mix", "E/M mix", "not_available", "No benchmark file.")
    bench = json.load(open(path))["specialties"]["Family Practice"]["mean_level_mix"]
    c = Counter(r["cpt"] for r in t["lines"] if r["cpt"] in EM)
    n = sum(c.values())
    mix = {k: c[k] / n for k in EM}
    tvd = sum(abs(mix[k] - bench[k]) for k in EM) / 2
    status = "warn" if tvd > MIX_TVD_WARN else "ok"
    return _check("em_mix", "E/M mix against the Family Practice benchmark", status,
                  f"The delivered E/M mix is {_pct(tvd)} away from the Family Practice benchmark (total variation distance; informational, the synthetic data is calibrated only roughly).",
                  {"mix": {k: round(v, 4) for k, v in mix.items()}, "benchmark": bench, "total_variation_distance": round(tvd, 4)})


def check_dx(t):
    by_month = defaultdict(Counter)
    for h in t["headers"]:
        if h["claim_frequency"] != "1":
            continue
        by_month[h["service_date"][:7]][sum(1 for c in DX_COLS if h[c])] += 1
    total = Counter()
    suspect, per_month = {}, {}
    for m, c in sorted(by_month.items()):
        n, mx = sum(c.values()), max(c)
        share = c[mx] / n
        per_month[m] = {"claims": n, "max_codes": mx, "share_at_max": round(share, 3)}
        total.update(c)
        if mx < len(DX_COLS) and share >= CAP_MIN_SHARE:
            suspect[m] = {"cap": mx, "share_at_cap": round(share, 3)}
    n = sum(total.values())
    dist = {str(k): round(total[k] / n, 4) for k in sorted(total)}
    detail = ("Diagnosis codes per claim look uncapped: every month reaches the extract's full width or has no pile-up at a lower maximum." if not suspect else
              f"In {len(suspect)} of {len(by_month)} months the number of diagnosis codes per claim stops at {sorted({v['cap'] for v in suspect.values()})} "
              f"with {_pct(min(v['share_at_cap'] for v in suspect.values()))} or more of claims exactly at that maximum, below the {len(DX_COLS)} the extract can hold: "
              "diagnoses may be truncated, which would make sicker panels look healthier.")
    return _check("dx_per_claim", "Diagnosis codes per claim", "warn" if suspect else "ok", detail,
                  {"distribution": dist, "by_month": per_month, "suspected_cap_months": suspect})


def attribution(t):
    """Per header: (clinician or None, billing, blank rendering?, billing is an organization?)."""
    out = []
    for h in t["headers"]:
        r, b = h["rendering_npi"], h["billing_npi"]
        out.append((r or (b if b in t["npis"] else None), b, not r, b not in t["npis"]))
    return out


def check_rendering(t, att=None):
    att = att or attribution(t)
    n = len(att)
    blank = sum(1 for a in att if a[2])
    unattr = sum(1 for a in att if a[2] and a[3])
    org = Counter(a[1] for a in att if a[3])
    org_blank = Counter(a[1] for a in att if a[3] and a[2])
    ents = {b: round(org_blank[b] / org[b], 3) for b in org if org_blank[b] / org[b] >= PROVIDER_SHARE_FLAG and org_blank[b] >= MIN_CLAIMS_FLAG}
    share = unattr / n
    status = "block" if share > UNATTRIBUTED_BLOCK else ("warn" if share > UNATTRIBUTED_WARN else "ok")
    detail = (f"{_pct(blank / n)} of claims have a blank rendering NPI; {_pct(share)} of all claims are blank under an organizational biller and cannot be attributed to a clinician "
              f"(single-clinician claims fall back to the billing NPI). Billing entities with a high blank share: {len(ents)}.")
    return _check("rendering_npi", "Rendering NPI", status, detail,
                  {"blank_share": round(blank / n, 4), "unattributable_share": round(share, 4), "fallback_to_billing_share": round((blank - unattr) / n, 4),
                   "entities_flagged": ents})


def check_members(t):
    n = len(t["headers"])
    bad = [h["claim_id"] for h in t["headers"] if h["member_id"] not in t["members"]]
    rate = 1 - len(bad) / n
    status = "block" if rate < JOIN_BLOCK else ("warn" if rate < JOIN_WARN else "ok")
    return _check("member_join", "Member join to eligibility", status,
                  f"{_pct(rate)} of claims join to eligibility ({len(bad):,} do not).", {"join_rate": round(rate, 5), "unmatched_claims": len(bad)})


def check_duplicates(t):
    paid = {r["claim_id"] for r in t["remit"] if r["status"] == "paid"}
    em_line = {}
    for r in t["lines"]:
        if r["cpt"] in EM and r["claim_id"] not in em_line:
            em_line[r["claim_id"]] = (r["cpt"], r["paid_amount"])
    seen, dup = {}, []
    for h in t["headers"]:
        cid = h["claim_id"]
        if h["claim_frequency"] != "1" or cid not in paid or cid not in em_line:
            continue
        key = (h["member_id"], h["service_date"], h["billing_npi"], h["rendering_npi"], *(h[c] for c in DX_COLS), em_line[cid])
        if key in seen:
            dup.append((cid, seen[key]))
        else:
            seen[key] = cid
    rate = len(dup) / max(len(seen) + len(dup), 1)
    return _check("duplicates", "Duplicate claims", "warn" if rate > DUPLICATE_WARN else "ok",
                  f"{len(dup):,} paid claims ({_pct(rate)}) repeat another claim's member, date, biller, diagnoses and E/M line under a new claim id.",
                  {"duplicate_claims": len(dup), "rate": round(rate, 5), "pairs": [list(p) for p in dup[:200]]}), dup


def check_chains(t):
    ids = {h["claim_id"] for h in t["headers"]}
    kids = [h for h in t["headers"] if h["claim_frequency"] in ("7", "8")]
    orphans = [h["claim_id"] for h in kids if h["original_claim_id"] not in ids]
    rate = len(orphans) / max(len(kids), 1)
    return _check("chains", "Replacement and void chains", "warn" if rate > ORPHAN_WARN else "ok",
                  f"{len(orphans):,} of {len(kids):,} replacement and void claims ({_pct(rate)}) have no original claim in the extract.",
                  {"orphans": len(orphans), "rate": round(rate, 5), "claim_ids": orphans[:200]})


def check_lag(t):
    by = Counter(h["service_date"][:7] for h in t["headers"] if h["claim_frequency"] == "1")
    months = sorted(by)
    if len(months) < 6:
        return _check("claims_lag", "Immature recent months", "not_available", "Fewer than six months of claims.")
    base = sorted(by[m] for m in months[:-2])[len(months[:-2]) // 2]
    late = {m: round(by[m] / base, 3) for m in months[-2:] if by[m] / base < LAG_RATIO_WARN}
    return _check("claims_lag", "Immature recent months", "warn" if late else "ok",
                  ("The two latest months are about as large as earlier months." if not late else
                   f"The latest months {sorted(late)} hold {min(late.values()):.0%} or less of a typical earlier month: recent claims may not have arrived yet."),
                  {"latest_vs_median": {m: round(by[m] / base, 3) for m in months[-2:]}})


def run_checks(v2_dir):
    t = load(v2_dir)
    att = attribution(t)
    dup_check, dups = check_duplicates(t)
    checks = [check_control_totals(t), check_em_mix(t), check_dx(t), check_rendering(t, att), check_members(t), dup_check, check_chains(t), check_lag(t)]
    status = max((c["status"] for c in checks), key=lambda s: ORDER[s])
    status = "ok" if status == "not_available" else status
    by = {c["id"]: c for c in checks}
    # per-provider flags (clinician ids): sentences a reviewer can read next to a finding
    prov = defaultdict(list)
    claims_of = Counter()
    month_of_claim = {}
    for h, a in zip(t["headers"], att):
        if h["claim_frequency"] == "1" and a[0]:
            claims_of[a[0]] += 1
            month_of_claim[h["claim_id"]] = (a[0], h["service_date"][:7])
    suspect = by["dx_per_claim"]["numbers"]["suspected_cap_months"]
    if suspect:
        in_susp = Counter(p for p, m in month_of_claim.values() if m in suspect)
        for p, k in in_susp.items():
            if k / claims_of[p] >= PROVIDER_CAP_SHARE:
                caps = sorted({v["cap"] for v in suspect.values()})
                prov[p].append({"flag": "dx_truncation", "detail": f"{_pct(k / claims_of[p])} of this provider's claims fall in months where diagnosis codes look capped at {caps}; risk adjustment may understate its patients' conditions"})
    ents = by["rendering_npi"]["numbers"]["entities_flagged"]
    if ents:
        members_of = defaultdict(set)
        for h in t["headers"]:
            if h["rendering_npi"] and h["billing_npi"] in ents:
                members_of[h["billing_npi"]].add(h["rendering_npi"])
        for e, share in ents.items():
            for p in members_of.get(e, ()):
                prov[p].append({"flag": "rendering_missing", "detail": f"{_pct(share)} of the claims billed by this provider's group lacked a rendering NPI, so some of its visits cannot be attributed to a clinician and its counts may be incomplete"})
    dup_prov = Counter()
    if dups:
        idx = {h["claim_id"]: a[0] for h, a in zip(t["headers"], att)}
        for d, _ in dups:
            if idx.get(d):
                dup_prov[idx[d]] += 1
    for p, k in dup_prov.items():
        if k >= MIN_CLAIMS_FLAG and k / claims_of[p] >= PROVIDER_SHARE_FLAG:
            prov[p].append({"flag": "duplicates", "detail": f"{_pct(k / claims_of[p])} of this provider's claims ({k}) look like duplicates of other claims"})
    bad_members = Counter()
    for h, a in zip(t["headers"], att):
        if a[0] and h["member_id"] not in t["members"]:
            bad_members[a[0]] += 1
    for p, k in bad_members.items():
        if k >= MIN_CLAIMS_FLAG and k / claims_of[p] >= PROVIDER_SHARE_FLAG:
            prov[p].append({"flag": "unknown_member", "detail": f"{_pct(k / claims_of[p])} of this provider's claims ({k}) have a member id that does not join to eligibility"})
    flags = [f"{c['title']}: {c['detail']}" for c in checks if c["status"] in ("warn", "block")]
    return {"status": status, "checks": checks, "global_flags": flags, "per_provider": dict(prov),
            "truncation_suspected": bool(suspect), "claims": len(t["headers"]),
            "policy": "A suspected extract problem holds findings that depend on it: an upcoding finding for an affected provider needs chart evidence, "
                      "and every held finding carries the data caveat. The agent never requests data from the plan; a person does."}


def hold_decision(report, provider_id, charts_received=0, min_charts=8):
    """Whether findings for this provider are affected: {"affected", "reasons", "needs_chart_evidence", "caveat"}.
    Findings that rest on risk adjustment are held unless charts (`min_charts` or more received) carry the finding."""
    flags = (report or {}).get("per_provider", {}).get(provider_id, [])
    reasons = [f["detail"] for f in flags]
    affected = bool(flags)
    return {"affected": affected, "reasons": reasons, "needs_chart_evidence": affected and charts_received < min_charts,
            "caveat": ("Data caveat (low confidence): " + "; ".join(reasons) + ". A person should ask the plan for a full re-extract before relying on the screen score.") if affected else ""}


def apply_holds(records, report, charts_by_provider, min_charts=8):
    """Workflow v2.2: apply the hold policy to checked summaries (a list of {"provider_id", "summary"}). An affected provider's summary gets the data caveat;
    an upcoding leaning without enough charts becomes inconclusive. Returns (records, held provider ids). The input is not modified."""
    out, held = [], []
    for r in records:
        h = hold_decision(report, r["provider_id"], charts_by_provider.get(r["provider_id"], 0), min_charts)
        if not h["affected"]:
            out.append(r)
            continue
        s = dict(r["summary"])
        s["rationale"] = (s["rationale"] + " " + h["caveat"]).strip()
        if s["leaning"] == "pattern_consistent_with_upcoding" and h["needs_chart_evidence"]:
            s["leaning"] = "inconclusive"
            s["headline"] = "Held for a data problem: " + s["headline"]
            held.append(r["provider_id"])
        out.append({**r, "summary": s, "data_quality_hold": True})
    return out, held


def write_report(report, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "data_quality.json")
    json.dump(report, open(path, "w"), indent=1)
    return path


def short(report, provider_id=None):
    """The compact form the agent sees: overall status, check statuses and sentences, global flags, and one provider's flags if asked."""
    out = {"status": report["status"], "truncation_suspected": report["truncation_suspected"],
           "checks": [{"id": c["id"], "status": c["status"], "detail": c["detail"]} for c in report["checks"]],
           "global_flags": report["global_flags"], "providers_with_flags": len(report["per_provider"]), "policy": report["policy"]}
    if provider_id:
        out["provider"] = {"provider_id": provider_id, "flags": report["per_provider"].get(provider_id, [])}
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    rep = run_checks(sys.argv[1])
    print(json.dumps(short(rep), indent=1))
    if "--out" in sys.argv:
        print("->", write_report(rep, sys.argv[sys.argv.index("--out") + 1]))
