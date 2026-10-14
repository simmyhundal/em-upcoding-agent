"""Claim-versus-note checks on a returned note package (data v2.1; issue 57). Payer-visible inputs only.

A note package is what a records request returns for one visit: the note, its signature record, the orders and results, and (only
on a second-tier request) the audit trail. The checks compare it with the claim (diagnoses, lab lines, date) and with the provider's
other returned notes. They flag what a reviewer would flag; none of them proves anything alone, because honest providers also use
templates, copy forward, sign late and miss orders at a baseline rate. Rates, not single flags, are the signal.
"""
import csv
import os
import re
from collections import Counter, defaultdict
from datetime import date

LATE_DAYS = 7
DUP_JACCARD = 0.6
MIN_NOTES_FOR_PATTERNS = 8
TIME_REPEAT_SHARE = 0.25
PASTE_HEAVY = 4
BULK_DAYS = 3
SIGNALS = ["problems", "data", "unsigned", "late", "time_repeat", "duplicate", "bulk_created", "paste_heavy"]


def _rows(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def load_notes(v2_dir):
    """claim_id -> package (note, auth, orders, results, audit). Reads the records universe: for use by the simulator and tests only."""
    base = os.path.join(v2_dir, "records")
    notes = {r["claim_id"]: {"note": r} for r in _rows(os.path.join(base, "visit_notes.csv"))}
    by_note = {p["note"]["note_id"]: p for p in notes.values()}
    for r in _rows(os.path.join(base, "note_authentication.csv")):
        by_note[r["note_id"]]["auth"] = r
    for p in notes.values():
        p["orders"], p["results"] = [], {}
    for r in _rows(os.path.join(base, "note_orders.csv")):
        by_note[r["note_id"]]["orders"].append(r)
    res = {r["order_id"]: r for r in _rows(os.path.join(base, "note_results.csv"))}
    for p in notes.values():
        p["results"] = {o["order_id"]: res[o["order_id"]] for o in p["orders"] if o["order_id"] in res}
    for r in _rows(os.path.join(base, "audit_trail.csv")):
        by_note[r["note_id"]]["audit"] = r
    return notes


def _days(a, b):
    return (date.fromisoformat(a[:10]) - date.fromisoformat(b[:10])).days


def _shingles(text, k=4):
    w = re.sub(r"[\d]+", "#", text.lower()).split()
    return {" ".join(w[i:i + k]) for i in range(max(1, len(w) - k + 1))}


def visit_flags(pkg, claim, with_audit=False):
    """Per-visit flags against the claim. claim: a detector-view claims row (diagnosis_codes, has_test_line, service_date)."""
    n, a = pkg["note"], pkg["auth"]
    dx = set(claim["diagnosis_codes"].split(";"))
    addressed = [c for c in n["problems_addressed"].split(";") if c]
    f = {"problems": bool(set(addressed) - dx) or (int(n["problems_level"]) >= 3 and len(addressed) < 2),
         "data": int(n["data_level"]) >= 3 and not pkg["orders"] and not int(n["outside_records_reviewed"]) and claim.get("has_test_line") != "1",
         "unsigned": a["status"] in ("unsigned", "illegible"),
         "late": bool(a["signed_date"]) and _days(a["signed_date"], n["service_date"]) > LATE_DAYS}
    if with_audit and "audit" in pkg:
        au = pkg["audit"]
        f["bulk_created"] = _days(au["created_ts"], n["service_date"]) > BULK_DAYS
        f["paste_heavy"] = int(au["copy_paste_events"]) >= PASTE_HEAVY
    return f


def provider_signals(items, with_audit=False):
    """items: [(package, claim_row)] for one provider's returned notes. Returns {signal: rate} (None when too few notes)."""
    n = len(items)
    if n < MIN_NOTES_FOR_PATTERNS:
        return {k: None for k in SIGNALS}
    flags = [visit_flags(p, c, with_audit) for p, c in items]
    out = {k: sum(f.get(k, False) for f in flags) / n for k in ("problems", "data", "unsigned", "late")}
    mins = Counter(p["note"]["documented_minutes"] for p, _ in items if p["note"]["documented_minutes"] != "")
    out["time_repeat"] = (max(mins.values()) / sum(mins.values())) if sum(mins.values()) >= MIN_NOTES_FOR_PATTERNS else None
    sh = [_shingles(p["note"]["note_text"]) for p, _ in items]
    members = [p["note"]["member_id"] for p, _ in items]
    dup = 0
    for i in range(n):
        for j in range(n):
            if i != j and members[i] != members[j] and len(sh[i] & sh[j]) / len(sh[i] | sh[j]) >= DUP_JACCARD:
                dup += 1
                break
    out["duplicate"] = dup / n
    if with_audit:
        out["bulk_created"] = sum(f.get("bulk_created", False) for f in flags) / n
        out["paste_heavy"] = sum(f.get("paste_heavy", False) for f in flags) / n
    else:
        out["bulk_created"] = out["paste_heavy"] = None
    return out


NOTE_DOC_COLS = ["note_id", "note_text", "problems_addressed", "time_statement", "outside_records_reviewed", "auth_status", "service_date",
                 "signed_date", "order_count", "results_present", "created_ts", "last_edited_ts", "copy_paste_events", "template_id"]


def pkg_from_doc_row(row, claim):
    """Rebuild a note package from one returned documentation row (data v2.1) and its claim row."""
    pkg = {"note": {"note_id": row["note_id"], "problems_addressed": row["problems_addressed"], "problems_level": row["documented_problems_level"],
                    "data_level": row["documented_data_level"], "outside_records_reviewed": row["outside_records_reviewed"] or "0",
                    "service_date": row["service_date"], "documented_minutes": row["documented_minutes"], "note_text": row["note_text"],
                    "member_id": claim["patient_id"]},
           "auth": {"status": row["auth_status"], "signed_date": row["signed_date"]},
           "orders": [{}] * int(row["order_count"] or 0)}
    if row.get("created_ts"):
        pkg["audit"] = {"created_ts": row["created_ts"], "last_edited_ts": row["last_edited_ts"], "copy_paste_events": row["copy_paste_events"]}
    return pkg


def signals_from_docs(rows, claims_by_id, with_audit=False):
    """Provider-level signal rates from returned documentation rows (those carrying note columns). rows: one provider's rows."""
    items = [(pkg_from_doc_row(r, claims_by_id[r["claim_id"]]), claims_by_id[r["claim_id"]]) for r in rows
             if r.get("note_id") and r["claim_id"] in claims_by_id]
    sig = provider_signals(items, with_audit=with_audit and any("audit" in p for p, _ in items))
    sig["notes"] = len(items)
    return sig


def flagged_claims(rows, claims_by_id, signal, limit=5, with_audit=False):
    """Claim ids of returned notes that show `signal` (problems, data, unsigned, late, bulk_created, paste_heavy)."""
    out = []
    for r in rows:
        if not r.get("note_id") or r["claim_id"] not in claims_by_id:
            continue
        pkg = pkg_from_doc_row(r, claims_by_id[r["claim_id"]])
        if visit_flags(pkg, claims_by_id[r["claim_id"]], with_audit).get(signal):
            out.append(r["claim_id"])
    return out[:limit]
