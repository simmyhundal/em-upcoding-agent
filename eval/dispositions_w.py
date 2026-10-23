"""Disposition table for a stored workflow run (issue 66, the workflow mirror of the agent's `set_aside`). Free: reads only what the payer sees in the run folder
(experiments/<rid>/: the flagged file, office_transcript.jsonl, case_summaries_checked.jsonl, demand_floor.json) and, for the ask model, src/policy_40.py. No key of roles is read.

It is a post-hoc table, not a refusal gate: the workflow's code already decides every provider; this writes down, for each provider on the screen list, what was decided and why.
Writes experiments/<rid>/dispositions.csv, one row per provider on the screen list (for a short-list run, the full list the short one was cut from; providers beyond the short list are `not listed`).

Usage: python3 eval/dispositions_w.py RID [RID ...]        (writes the CSV, prints the share of listed providers with a stated reason)
       python3 eval/dispositions_w.py --batches 5,6 wlh8 wlh22 wlh23_n4   (run-id prefix plus development seeds of those batches)
       python3 eval/dispositions_w.py --fresh fr40                         (the ten fresh workflow runs)
"""
import csv
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import policy_40 as pol40  # noqa: E402

UPCODING = "pattern_consistent_with_upcoding"
COLUMNS = ["provider_id", "rank", "screen_score", "on_list", "ask_decision", "ask_reason", "ask_predicted_value", "ask_matches_policy", "charts_requested", "charts_usable", "rounds",
           "rules_leaning", "rules_reason", "demand_floor_withdrawn", "floor_estimate", "floor_cost", "disposition", "disposition_reason", "reason_stated"]


def _read(path):
    return [json.loads(x) for x in open(path) if x.strip()]


def run_spec(rid):
    """The workflow policy options a stored run used, from the loop's registry (eval/w_loop.py) or the frozen v4.0; None when unknown (then the ask rule is inferred)."""
    try:
        import w_loop as wl
        import workflow_policy_40 as wp40
    except Exception:
        return None
    if rid.startswith("fr40_"):
        return wp40.FROZEN_V40
    name = rid.rsplit("_", 1)[0]
    for k, v in wl.VERSIONS.items():
        if f"wl{k.lower()}" == name:
            return v
    return None


def _screen_files(run_dir, root=ROOT, full_list_file=None):
    files = [f for f in glob.glob(os.path.join(run_dir, "flagged_*.csv")) if not f.endswith("flagged_threshold.csv")]
    if len(files) != 1:
        raise SystemExit(f"{run_dir}: expected one screen file flagged_<screen>.csv, found {files}")
    short = files[0]
    full = short
    m = re.match(r"^(flagged_.*)_top\d+\.csv$", os.path.basename(short))
    if full_list_file:
        full = full_list_file
    elif m:                                                   # a short-list run: the full list lives in the data's own folder (README: "Screen from `experiments/<code>/`")
        found = re.search(r"Screen from `experiments/([^/`]+)/`", open(os.path.join(run_dir, "README.md")).read())
        cand = os.path.join(root, "experiments", found.group(1), m.group(1) + ".csv") if found else ""
        if os.path.exists(cand):
            full = cand
    return short, full


def _fmt(v):
    return f"${v:,.0f}" if v >= 0 else f"-${-v:,.0f}"


def build(run_dir, spec=None, claims_file=None, ask_model=None, root=ROOT, full_list_file=None):
    """Rows of the disposition table for the run folder `run_dir`. `spec` = the run's policy options (None: inferred); `claims_file` only for ask models built on claims (features 4.1)."""
    short, full = _screen_files(run_dir, root, full_list_file)
    listed_ids = [r["provider_id"] for r in csv.DictReader(open(short)) if r["flagged"] == "True"]
    all_rows = list(csv.DictReader(open(full)))
    on_screen = [r for r in all_rows if r["flagged"] == "True"]
    summaries = {r["provider_id"]: r for r in _read(os.path.join(run_dir, "case_summaries_checked.jsonl"))}
    floor = json.load(open(os.path.join(run_dir, "demand_floor.json"))) if os.path.exists(os.path.join(run_dir, "demand_floor.json")) else {"floor": None, "withdrawn": {}}
    first, last, asked = {}, {}, set()
    for e in _read(os.path.join(run_dir, "office_transcript.jsonl")):
        pid = e.get("provider_id")
        if e.get("action") == "send_request":
            asked.add(pid)
        if e.get("action") in ("send_request", "follow_up", "audit_trail") and "error" not in e:
            last[pid] = {"requested": e.get("requested_total", 0), "usable": e.get("usable_total", 0), "rounds": e.get("round", 0)}
    ask = (spec or {}).get("w40", {}).get("ask") if spec else None
    model = None
    if ask in (None, "linear"):
        mp = ask_model or ((spec or {}).get("w40", {}).get("ask_model")) or pol40.ASK_MODEL
        model = pol40.load_ask(mp)
    claims = {}
    if model and model.get("features_version") == "4.1" and claims_file:
        for r in csv.DictReader(open(claims_file)):
            claims.setdefault(r["provider_id"], []).append(r)
    rows = []
    for rank0, r in enumerate(on_screen):
        pid = r["provider_id"]
        on_list = pid in listed_ids
        out = {"provider_id": pid, "rank": r["rank"], "screen_score": r.get("screen_score", ""), "on_list": "yes" if on_list else "no"}
        pred, matches = "", ""
        if not on_list:
            out.update(ask_decision="skipped", ask_reason=f"not listed: outside the short list of the first {len(listed_ids)} providers of the screen list")
        else:
            was_asked = pid in asked
            out["ask_decision"] = "asked" if was_asked else "skipped"
            if ask == "all":
                out["ask_reason"] = "policy asks every listed provider"
                matches = was_asked
            elif isinstance(ask, int) and not isinstance(ask, bool):
                inside = listed_ids.index(pid) < ask
                out["ask_reason"] = f"{'inside' if inside else 'outside'} the first {ask} asked"
                matches = inside == was_asked
            elif model is not None:
                v = pol40.predict(model, r, claims.get(pid))
                m = model.get("margin", 0.0)
                pred = round(v, 2)
                out["ask_reason"] = f"ask model predicts net value {_fmt(v)} of asking, {'above' if v > m else 'not above'} the margin {_fmt(m)}: {'ask' if v > m else 'skip'}"
                matches = (v > m) == was_asked
            else:
                out["ask_reason"] = ""
        out["ask_predicted_value"], out["ask_matches_policy"] = pred, matches
        ch = last.get(pid, {})
        out["charts_requested"], out["charts_usable"], out["rounds"] = ch.get("requested", 0), ch.get("usable", 0), ch.get("rounds", 0)
        s = summaries.get(pid)
        withdrawn = pid in floor["withdrawn"]
        out["rules_leaning"] = s.get("rule_leaning", "") if s else ""
        out["rules_reason"] = s.get("rule_reason", "") if s else ""
        out["demand_floor_withdrawn"] = "yes" if withdrawn else "no"
        out["floor_estimate"] = floor["withdrawn"][pid] if withdrawn else ""
        out["floor_cost"] = round(floor["floor"], 2) if withdrawn and floor["floor"] is not None else ""
        if not on_list:
            disp, why = "not examined", out["ask_reason"]
        elif s is None:
            disp, why = "not examined", out["ask_reason"] or ""
        elif withdrawn:
            disp = "examined and set aside"
            why = f"rules called upcoding ({out['rules_reason']}); no demand: estimated recovery (lower bound {_fmt(out['floor_estimate'])}) is below the staff cost of a demand ({_fmt(out['floor_cost'])})"
        elif s["summary"]["leaning"] == UPCODING:
            disp = "demanded"
            why = f"rules call upcoding ({out['rules_reason']}); estimated recovery covers the cost of a demand" + (f" ({_fmt(floor['floor'])})" if floor["floor"] is not None else "")
        elif out["ask_decision"] == "asked":
            disp = "examined and set aside"
            why = f"{out['charts_usable']} of {out['charts_requested']} charts usable; rules leaning {out['rules_leaning'] or s['summary']['leaning']}: {out['rules_reason']}"
        else:
            disp, why = "not examined", out["ask_reason"]
        if disp == "examined and set aside" and not out["rules_reason"]:
            why = ""                                                   # no reason string from the rules: counts as no stated reason
        if disp == "demanded" and not out["rules_reason"]:
            why = ""
        out["disposition"], out["disposition_reason"] = disp, why
        out["reason_stated"] = "yes" if why.strip() else "no"
        rows.append(out)
    return rows


def write(rid, root=ROOT):
    run_dir = os.path.join(root, "experiments", rid)
    rows = build(run_dir, run_spec(rid), claims_file=_claims_file(rid, root))
    with open(os.path.join(run_dir, "dispositions.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    return rows


def _claims_file(rid, root=ROOT):
    seed = rid.rsplit("_", 1)[1]
    for code in (f"d4_{seed}", f"f4_{seed}"):
        p = os.path.join(root, "data", f"synthetic_v2_{code}", "view", "claims.csv")
        if os.path.exists(p) and ((code[0] == "f") == rid.startswith("fr")):
            return p
    return None


def share(rows):
    """(listed providers, listed providers with a stated reason, ask decisions that disagree with the policy re-derived here)."""
    listed = [r for r in rows if r["on_list"] == "yes"]
    return len(listed), sum(r["reason_stated"] == "yes" for r in listed), sum(r["ask_matches_policy"] is False for r in listed)


if __name__ == "__main__":
    args = sys.argv[1:]
    rids = []
    if "--batches" in args:
        import dev_pool_v4 as pool
        i = args.index("--batches")
        seeds = sum([pool.BATCHES[int(b) - 1] for b in args[i + 1].split(",")], [])
        rids = [f"{p}_{s}" for p in args[i + 2:] for s in seeds]
    elif "--fresh" in args:
        rids = [f"{args[-1]}_{5555 + 101 * i}" for i in range(10)]
    else:
        rids = args
    tot = [0, 0, 0, 0, 0]
    for rid in rids:
        rows = write(rid)
        n, ok, bad = share(rows)
        tot = [tot[0] + n, tot[1] + ok, tot[2] + bad, tot[3] + len(rows), tot[4] + sum(r["disposition"] == "demanded" for r in rows)]
    print(f"{len(rids)} runs: {tot[3]} rows, {tot[0]} listed providers, {tot[1]} with a stated reason ({100 * tot[1] / max(tot[0], 1):.1f}%), {tot[2]} ask decisions not matching the re-derived policy, {tot[4]} demanded")
