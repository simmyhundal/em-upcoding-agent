"""Scoreboard: every run against the thresholds, generated from the saved outputs (never typed by hand).

Reads experiments/runs.json and writes experiments/results.csv, the source of truth for results; the README table is rendered from
that file. For each run it computes five evals, marks each pass or fail against its threshold, and totals the
evals passed out of those that apply. A dash means not scored or not applicable and is left out of the total.

Evals and thresholds:
  1. False negative rate: at most 12.5% of the real upcoders are missed. (Screen rows: upcoders not flagged. AI rows: upcoders
     the AI did not call upcoding.)
  2. False positive rate: at most 12.5% of the honest doctors are wrongly accused, counted out of the honest doctors that step
     actually faced. Screen rows: honest doctors flagged out of all honest doctors in the data. AI rows: honest doctors the AI
     called upcoding out of the honest doctors the screen sent to it. "Honest" means every non-upcoder, ordinary doctors and
     doctors with sicker patients alike.
  3. Precision of "upcoding" calls: at least 80% of the doctors called upcoding really are upcoders (PROPOSED threshold: the
     original targets ignored the many ordinary honest doctors who get flagged). Screen rows: upcoders among the top 25.
  4. Citations valid: 100% of cited claims exist and belong to the provider.
  5. Case Summary Usefulness (1-5): average of at least 4 (LLM judge).

Usage:
    python eval/scoreboard.py --write    # recompute from saved outputs and rewrite experiments/results.csv (needs the answer keys)
    python eval/scoreboard.py            # prints the README table, rendered from experiments/results.csv
"""
import csv
import json
import os
import sys

import run_eval

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_RATE = 0.125       # false negative rate and false positive rate
MIN_USEFULNESS = 4.0
MIN_PRECISION = 0.80   # proposed
TOP_N = 25
PASS, FAIL = "🟩", "🟥"   # green = passed the threshold, red = failed


def judge(value, kind):
    """Pass/fail for one eval. kind in fn|fp|prec|cite|useful."""
    if value is None:
        return None
    if kind == "fn":                       # value = (missed upcoders, all upcoders)
        return value[0] / value[1] <= MAX_RATE
    if kind == "fp":                       # value = (honest doctors accused, all honest doctors)
        return value[0] / value[1] <= MAX_RATE
    if kind == "prec":
        return value >= MIN_PRECISION
    if kind == "cite":
        return value == 1.0
    if kind == "useful":
        return value >= MIN_USEFULNESS
    raise ValueError(kind)


def total(oks):
    app = [o for o in oks if o is not None]
    return f"{sum(app)} / {len(app)}"


def _load(path):
    return os.path.join(ROOT, path)


def _screen_cells(d, r):
    """Cells for a screen row: the top 25, or every doctor at or above the run's suspicion threshold."""
    if r.get("min_suspicion") is not None:
        sel = [x["provider_id"] for x in d["rows"] if float(x["z_adj"]) >= r["min_suspicion"]]
        sc = run_eval.score(sel, d["truth"])
        found = sc["upcoder"]["flagged"]
        honest = sc["hard_negative"]["flagged"] + sc["normal"]["flagged"]
        prec = (found / len(sel)) if sel else None
    else:
        c = d["ev"]["Combined list"]
        found, honest, prec = c["upcoders_found"], c["hard_neg_flagged"] + c["normal_flagged"], c["upcoders_found"] / TOP_N
        sel = [x["provider_id"] for x in d["rows"] if x["flagged"] == "True"]
    return {"fn": (d["n_up"] - found, d["n_up"]), "fp": (honest, d["n_honest"]), "prec": prec, "called": sel}


def _ai_cells(d, r):
    recs = run_eval.load_checked(_load(r["checked"]))
    L = run_eval.leaning_stats(recs, d["truth"])
    cells = {"fn": (d["n_up"] - L["true_upcoders_called"], d["n_up"]),
             "fp": (L["honest_called_upcoding"], L["honest_total"]), "prec": L["precision"],
             "called": [x["provider_id"] for x in recs if x["summary"]["leaning"] == "pattern_consistent_with_upcoding"],
             "cite": run_eval.citation_stats(recs)["accuracy"],
             "useful": None}
    if r.get("usefulness"):
        rows = [json.loads(line) for line in open(_load(r["usefulness"])) if line.strip()]
        cells["useful"] = sum(x["score"] for x in rows) / len(rows)
    return cells


def _selection_cells(d, selected, honest_sent):
    """Cells for a rules row: providers a rule flagged among those the screen sent for records. False negatives count against
    all upcoders; false positives count against the honest doctors that were sent (the ones the rule faced)."""
    sc = run_eval.score(selected, d["truth"])
    found = sc["upcoder"]["flagged"]
    honest = sc["hard_negative"]["flagged"] + sc["normal"]["flagged"]
    return {"fn": (d["n_up"] - found, d["n_up"]), "fp": (honest, honest_sent),
            "prec": (found / len(selected)) if selected else None, "called": list(selected)}


COLUMNS = ["run_id", "stage", "tuning", "records_evidence", "code_version", "seed", "seed_status", "source", "agents", "data_version",
           "data_description", "upcoder_rate", "upcoder_clone_level",
           "fn_missed", "fn_total", "fn_rate", "fn_pass", "fp_count", "fp_total", "fp_rate", "fp_pass",
           "precision", "precision_pass", "citations_valid", "citations_pass", "usefulness", "usefulness_pass",
           "evals_passed", "evals_applicable",
           "honest_requested", "request_rounds_total", "request_rounds_honest", "request_rounds_called",
           "overpaid_usd", "reached_usd", "reached_share", "notes"]
CSV_PATH = os.path.join(ROOT, "experiments", "results.csv")
VERDICT = {True: "pass", False: "fail", None: ""}


FEES = None


def _fees():
    global FEES
    if FEES is None:
        FEES = {c: v["allowed_amount"] for c, v in json.load(open(os.path.join(ROOT, "data", "baselines", "allowed_amounts_ga_fp.json")))["codes"].items()}
    return FEES


def _overpaid(d):
    """Provider -> dollars paid above what the justified levels would have paid (answer key; evaluation only). Cached per dataset.
    Uses each claim's own allowed and paid amounts when the data has them (v2), else fee-schedule averages at an 80% paid share (v1)."""
    if "overpaid" in d:
        return d["overpaid"]
    just = d["truth"]["justified_cpt_by_claim"]
    fees, out = _fees(), {}
    for r in csv.DictReader(open(_load(d["meta"]["view"] + "/claims.csv"))):
        j = just.get(r["claim_id"])
        if j and r["cpt"] > j:
            if r.get("allowed_amount"):
                allowed, paid = float(r["allowed_amount"]), float(r["paid_amount"])
                share = paid / allowed if allowed else 0.8
            else:
                allowed, share = fees[r["cpt"]], 0.8
            out[r["provider_id"]] = out.get(r["provider_id"], 0.0) + max(allowed - fees[j], 0.0) * share
    d["overpaid"] = out
    return out


def _dollars(d, called):
    """(dollars overpaid to all upcoders, dollars sitting with the upcoders in `called`)."""
    over = _overpaid(d)
    roles = d["truth"]["providers"]
    total = sum(v for p, v in over.items() if roles[p]["role"] == "upcoder")
    reached = sum(v for p, v in over.items() if p in set(called) and roles[p]["role"] == "upcoder")
    return total, reached


def _rounds(d, sent, called, transcript=None):
    """Honest doctors who received a records request, and request rounds (first request plus each follow-up): total, on honest
    doctors, on providers finally called upcoding. Single-draw workflows send one round per provider; office runs count transcripts."""
    roles = d["truth"]["providers"]
    if transcript and os.path.exists(_load(transcript)):
        per = {}
        for line in open(_load(transcript)):
            e = json.loads(line)
            if e.get("action") in ("send_request", "follow_up") and "error" not in e:
                per[e["provider_id"]] = per.get(e["provider_id"], 0) + 1
        sent = list(per)
    else:
        per = {p: 1 for p in sent}
    honest = [p for p in sent if roles[p]["role"] != "upcoder"]
    return {"honest_requested": len(honest), "request_rounds_total": sum(per.values()),
            "request_rounds_honest": sum(per[p] for p in honest), "request_rounds_called": sum(per.get(p, 0) for p in called)}


def _row(meta, stage, tuning, records, cells, d=None, sent=None, transcript=None):
    """One results row: run metadata plus the raw numbers and a pass/fail for each eval."""
    cells = dict(cells)
    called = cells.pop("called", None)
    cells = {**{k: None for k in ("fn", "fp", "prec", "cite", "useful")}, **cells}
    if cells["fp"] and cells["fp"][1] == 0:       # no honest doctors were in scope: the rate is undefined
        cells["fp"] = None
    oks = {k: judge(cells[k], k) for k in cells}
    app = [o for o in oks.values() if o is not None]
    fn, fp = cells["fn"], cells["fp"]
    f = lambda v, nd=6: "" if v is None else round(v, nd)
    extra = {"honest_requested": "", "request_rounds_total": "", "request_rounds_honest": "", "request_rounds_called": "",
             "overpaid_usd": "", "reached_usd": "", "reached_share": ""}
    if d is not None and called is not None:
        total, reached = _dollars(d, called)
        extra.update({"overpaid_usd": round(total), "reached_usd": round(reached), "reached_share": round(reached / total, 4) if total else ""})
        if sent is not None:
            extra.update(_rounds(d, sent, called, transcript))
    return {**meta, "stage": stage, "tuning": tuning, "records_evidence": records,
            "fn_missed": fn[0], "fn_total": fn[1], "fn_rate": f(fn[0] / fn[1]), "fn_pass": VERDICT[oks["fn"]],
            "fp_count": "" if fp is None else fp[0], "fp_total": "" if fp is None else fp[1],
            "fp_rate": "" if fp is None else f(fp[0] / fp[1]), "fp_pass": VERDICT[oks["fp"]],
            "precision": f(cells["prec"]), "precision_pass": VERDICT[oks["prec"]],
            "citations_valid": f(cells["cite"]), "citations_pass": VERDICT[oks["cite"]],
            "usefulness": f(cells["useful"], 2), "usefulness_pass": VERDICT[oks["useful"]],
            "evals_passed": sum(app), "evals_applicable": len(app), **extra}


def _agents(r):
    """Separate model calls (or chat agents) that wrote summaries for an AI row; rules-written summaries do not count."""
    if r.get("agents") is not None:
        return r["agents"]
    recs = [json.loads(line) for line in open(_load((r.get("ai") or r)["checked"])) if line.strip()]
    return sum(1 for x in recs if x.get("source", "llm") == "llm")


def compute(registry_path=None):
    """One row for the screen and, for runs with more stages, further rows (rules, AI, hybrid). Needs the answer keys."""
    reg = json.load(open(registry_path or os.path.join(ROOT, "experiments", "runs.json")))
    data = {}
    for key, d in reg["datasets"].items():
        truth = json.load(open(_load(d["truth"])))
        rows = list(csv.DictReader(open(_load(d["flagged"]))))
        ev = run_eval.evaluate(rows, truth, TOP_N)
        roles = [v["role"] for v in truth["providers"].values()]
        data[key] = {"truth": truth, "ev": ev, "rows": rows, "n_up": roles.count("upcoder"), "n_all": len(roles),
                     "n_honest": len(roles) - roles.count("upcoder"), "seed": d["seed"], "meta": d}
    out = []
    for r in reg["runs"]:
        d = data[r["dataset"]]
        ds = d["meta"]
        ver = r.get("version") or ("v2.0" if r["kind"] in ("v2", "agent") else "v1.0")
        clone = d["truth"].get("clone_share")
        meta = {"run_id": r["run"], "code_version": ver, "seed": d["seed"], "seed_status": ds["seed_status"], "source": r["source"],
                "agents": "", "data_version": ds["data_version"], "data_description": reg["data_descriptions"][ds["data_version"]],
                "upcoder_rate": f"{d['n_up'] / d['n_all']:.1%} ({d['n_up']} of {d['n_all']})",
                "upcoder_clone_level": "n/a" if clone is None else f"{clone:.0%}", "notes": r.get("notes", "")}
        lc = lambda t: t[0].lower() + t[1:]
        screen_tuning = (f"Z-score of risk-adjusted coding >= {r['min_suspicion']:g}" if r.get("min_suspicion") is not None
                         else f"Top {TOP_N} upcoding outliers")
        ai_tuning = f"AI calls upcoding (screen: {lc(screen_tuning)})"
        if r["kind"] == "agent":
            # Milestone 6: the agent chose its own screening, so there is no fixed Screen row. Its false positives count the honest
            # providers it reported on; false negatives count against all upcoders.
            out.append(_row({**meta, "agents": 1}, "Agent", r["tuning"], "Yes", _ai_cells(d, r), d, transcript=r["transcript"], sent=[]))
            continue
        out.append(_row(meta, "Screen", screen_tuning, "No", _screen_cells(d, r), d))
        for rule in r.get("rules", []):
            sent = [x["provider_id"] for x in csv.DictReader(open(_load(rule["sent"]))) if x["flagged"] == "True"]
            roles = d["truth"]["providers"]
            honest_sent = sum(roles[p]["role"] != "upcoder" for p in sent)
            selected = [x["provider_id"] for x in csv.DictReader(open(_load(rule["selected"])))]
            out.append(_row(meta, "Rules", rule["tuning"], "Yes", _selection_cells(d, selected, honest_sent), d, sent=sent))
        if r.get("ai") and r["kind"] == "v2":
            sent_file = r.get("sent") or r["rules"][0]["sent"]
            sent_v2 = [x["provider_id"] for x in csv.DictReader(open(_load(sent_file))) if x["flagged"] == "True"]
            out.append(_row({**meta, "agents": _agents(r)}, "AI", ai_tuning, "Yes", _ai_cells(d, r["ai"]), d, sent=sent_v2,
                            transcript=r["ai"].get("transcript")))
            if r.get("rules"):
                # Hybrid (issue 49): the chart rule decides first; where it is silent the summary rules and model decide.
                # Computed from the saved outputs: union of the chart rule's providers and the AI step's upcoding calls.
                chart = {x["provider_id"] for x in csv.DictReader(open(_load(r["rules"][0]["selected"])))}
                ai_up = {x["provider_id"] for x in map(json.loads, open(_load(r["ai"]["checked"])))
                         if x["summary"]["leaning"] == "pattern_consistent_with_upcoding"}
                sent = [x["provider_id"] for x in csv.DictReader(open(_load(r["rules"][0]["sent"]))) if x["flagged"] == "True"]
                honest_sent = sum(d["truth"]["providers"][p]["role"] != "upcoder" for p in sent)
                out.append(_row(meta, "Hybrid", "Chart rule first, then summary rules and model", "Yes",
                                _selection_cells(d, sorted(chart | ai_up), honest_sent), d, sent=sent))
        if r["kind"] == "summaries":
            out.append(_row({**meta, "agents": _agents(r)}, "AI", ai_tuning, "Yes" if r["records"] else "No", _ai_cells(d, r), d))
    return out


def write_csv(path=CSV_PATH, registry_path=None):
    rows = compute(registry_path)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    return rows


def read_csv(path=CSV_PATH):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def _cell(row, kind):
    """Rendered cell: a coloured square for pass/fail, then the value; a dash when not scored."""
    verdict = row[{"fn": "fn_pass", "fp": "fp_pass", "prec": "precision_pass", "cite": "citations_pass", "useful": "usefulness_pass"}[kind]]
    if not verdict:
        return "–"
    sq = PASS if verdict == "pass" else FAIL
    if kind == "fn":
        return f"{sq} {int(row['fn_missed']) / int(row['fn_total']):.1%}<br>({row['fn_missed']} / {row['fn_total']})"
    if kind == "fp":
        return f"{sq} {int(row['fp_count']) / int(row['fp_total']):.1%}<br>({row['fp_count']} / {row['fp_total']})"
    if kind == "prec":
        return f"{sq} {float(row['precision']):.0%}"
    if kind == "cite":
        return f"{sq} {float(row['citations_valid']):.0%}"
    return f"{sq} {float(row['usefulness']):.2f}"


def _blank(v):
    return v if v != "" else "–"


def _usd(v):
    return f"${int(v):,}" if v != "" else "–"


def _rounds_cell(r):
    return f"{r['request_rounds_honest']} / {r['request_rounds_total']}" if r["request_rounds_total"] != "" else "–"


def _reached_cell(r):
    return f"{_usd(r['reached_usd'])} ({float(r['reached_share']):.0%})" if r["reached_usd"] != "" and r["reached_share"] != "" else "–"


def markdown_from_csv(path=CSV_PATH):
    """The README table, rendered from the committed results file (the source of truth), never recomputed."""
    rows = read_csv(path)
    head = ("| Run | Seed | Seed status | Source | Agents | Code version | Data version | Upcoders in data | Upcoder clone level "
            "| Screen / AI | Tuning | Records evidence | False negative rate | False positive rate | Precision of upcoding calls "
            "| Citations valid | Case Summary Usefulness (1-5) | Evals passed | Evals scored | Honest doctors sent records requests "
            "| Request rounds (honest / total) | Dollars overpaid to upcoders | Dollars at stake in upcoders called |\n" + "|---" * 23 + "|")
    thr = "| **Threshold** |" + " |" * 11 + " at most 12.5% | at most 12.5% | at least 80% (proposed) | 100% | at least 4 | | | | | | |"
    lines = [head, thr]
    for r in rows:
        lines.append(f"| {r['run_id']} | {r['seed']} | {r['seed_status']} | {r['source']} | {r['agents'] or '–'} | {r['code_version']} "
                     f"| {r['data_version']} | {r['upcoder_rate']} | {r['upcoder_clone_level']} | {r['stage']} | {r['tuning']} "
                     f"| {r['records_evidence']} | " + " | ".join(_cell(r, k) for k in ("fn", "fp", "prec", "cite", "useful"))
                     + f" | **{r['evals_passed']}** | {r['evals_applicable']} | {_blank(r['honest_requested'])} | {_rounds_cell(r)} | {_usd(r['overpaid_usd'])} | {_reached_cell(r)} |")
    descs = {}
    for r in rows:
        descs.setdefault(r["data_version"], r["data_description"])
    lines += ["", "Columns: **Seed status**: development = the seed used to build and tune the workflow, held-out = generated or scored after "
              "those settings were frozen, reserved = held back and never looked at until the Milestone 6 evaluation. **Source**: api = the project's own pipeline calling the API, cc = mimicked with Claude Code "
              "agents, code = no model. **Evals scored**: how many of the evals applied to that row (a screen row has 3; an AI row has 4, or 5 when the usefulness judge ran), so compare passes only between rows with the same count; the templating check was removed, which lowered AI rows' count by one. **Agents**: separate model calls or chat agents that wrote summaries (code-written ones do not count). "
              "**Upcoders in data**: the share of providers that are real upcoders (the prevalence; \"baseline\" is used only for a comparison arm). **Honest doctors sent records requests** and **Request rounds**: the burden on practices (a round is the first request or one follow-up). **Dollars overpaid to upcoders**: what upcoders were paid above what the justified levels would have paid (answer key). **Dollars at stake in upcoders called**: the same dollars for only the upcoders that stage called, an upper bound on what recovery could reach. **Upcoder clone level**: the share of upcoders whose notes "
              "are cloned to match the bill. Source of truth: `experiments/results.csv`.", ""]
    lines += [f"- **{k}**: {v}" for k, v in sorted(descs.items())]
    return "\n".join(lines)


SQ = {"pass": PASS, "fail": FAIL, "": ""}


def markdown_compact(path=CSV_PATH):
    """A short headline view for the README: one row per run and stage with the key numbers. The full table is docs/results.md."""
    rows = read_csv(path)
    head = ("| Run | Version | Seed status | Stage | Tuning | Upcoders found | Honest doctors accused | Precision | Usefulness (1-5) | Evals passed |\n"
            "|---|---|---|---|---|---|---|---|---|---|")
    lines = [head]
    for r in rows:
        found = f"{SQ[r['fn_pass']]} {int(r['fn_total']) - int(r['fn_missed'])} of {r['fn_total']}"
        acc = f"{SQ[r['fp_pass']]} {r['fp_count']} of {r['fp_total']}" if r["fp_total"] else "–"
        prec = f"{SQ[r['precision_pass']]} {float(r['precision']):.0%}" if r["precision_pass"] else "–"
        use = f"{SQ[r['usefulness_pass']]} {float(r['usefulness']):.2f}" if r["usefulness_pass"] else "–"
        lines.append(f"| {r['run_id']} | {r['code_version']} | {r['seed_status']} | {r['stage']} | {r['tuning']} | {found} | {acc} | {prec} | {use} "
                     f"| {r['evals_passed']} of {r['evals_applicable']} |")
    lines += ["", "Green means the threshold was met, red that it was missed. Thresholds: at most 12.5% of upcoders missed, at most 12.5% of honest "
              "doctors accused, precision at least 80% (proposed), usefulness at least 4. The full table (data version, upcoder rate, clone level, "
              "agents, request rounds, dollars) is in [docs/results.md](docs/results.md); the source of truth is `experiments/results.csv` "
              "([columns](docs/results_table.md))."]
    return "\n".join(lines)


def markdown(registry_path=None):
    return markdown_compact(CSV_PATH)


if __name__ == "__main__":
    if "--write" in sys.argv:
        print(f"{len(write_csv())} rows -> {CSV_PATH}")
    else:
        print(markdown())
