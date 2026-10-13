"""Scoreboard: every run against the thresholds, generated from the saved outputs (never typed by hand).

Reads experiments/runs.json. For each run it computes five evals, marks each pass or fail against its threshold, and totals the
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
    python eval/scoreboard.py            # prints the markdown table
"""
import csv
import json
import os

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
    return {"fn": (d["n_up"] - found, d["n_up"]), "fp": (honest, d["n_honest"]), "prec": prec}


def _ai_cells(d, r):
    recs = run_eval.load_checked(_load(r["checked"]))
    L = run_eval.leaning_stats(recs, d["truth"])
    cells = {"fn": (d["n_up"] - L["true_upcoders_called"], d["n_up"]),
             "fp": (L["honest_called_upcoding"], L["honest_total"]), "prec": L["precision"],
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
            "prec": (found / len(selected)) if selected else None}


def _row(run, seed, stage, tuning, records, cells):
    cells = {**{k: None for k in ("fn", "fp", "prec", "cite", "useful")}, **cells}
    if cells["fp"] and cells["fp"][1] == 0:       # no honest doctors were in scope: the rate is undefined
        cells["fp"] = None
    oks = {k: judge(cells[k], k) for k in cells}
    text = {k: None for k in cells}
    text["fn"] = f"{cells['fn'][0] / cells['fn'][1]:.1%}<br>({cells['fn'][0]} / {cells['fn'][1]})"
    if cells["fp"]:
        text["fp"] = f"{cells['fp'][0] / cells['fp'][1]:.1%}<br>({cells['fp'][0]} / {cells['fp'][1]})"
    if cells["prec"] is not None:
        text["prec"] = f"{cells['prec']:.0%}"
    if cells["cite"] is not None:
        text["cite"] = f"{cells['cite']:.0%}"
    if cells["useful"] is not None:
        text["useful"] = f"{cells['useful']:.2f}"
    return {"run": run, "seed": seed, "stage": stage, "tuning": tuning, "records": records, "text": text, "ok": oks,
            "total": total(oks.values())}


def compute(registry_path=None):
    """One row for the screen and, for runs with AI summaries, a second row for the AI's selection."""
    reg = json.load(open(registry_path or os.path.join(ROOT, "experiments", "runs.json")))
    data = {}
    for key, d in reg["datasets"].items():
        truth = json.load(open(_load(d["truth"])))
        rows = list(csv.DictReader(open(_load(d["flagged"]))))
        ev = run_eval.evaluate(rows, truth, TOP_N)
        roles = [v["role"] for v in truth["providers"].values()]
        data[key] = {"truth": truth, "ev": ev, "rows": rows, "n_up": roles.count("upcoder"),
                     "n_honest": len(roles) - roles.count("upcoder"), "seed": d["seed"]}
    out = []
    for r in reg["runs"]:
        d = data[r["dataset"]]
        name = r["run"] + (f"<br>{r['note']}" if r.get("note") else "")
        if r.get("bold"):
            name = f"**{r['run']}**" + (f"<br>{r['note']}" if r.get("note") else "")
        screen_tuning = (f"Z-score of risk-adjusted coding >= {r['min_suspicion']:g}" if r.get("min_suspicion") is not None
                         else f"Top {TOP_N} upcoding outliers")
        out.append(_row(name, d["seed"], "Screen", screen_tuning, "No", _screen_cells(d, r)))
        for rule in r.get("rules", []):
            sent = [x["provider_id"] for x in csv.DictReader(open(_load(rule["sent"]))) if x["flagged"] == "True"]
            roles = d["truth"]["providers"]
            honest_sent = sum(roles[p]["role"] != "upcoder" for p in sent)
            selected = [x["provider_id"] for x in csv.DictReader(open(_load(rule["selected"])))]
            out.append(_row(name, d["seed"], "Rules", rule["tuning"], "Yes", _selection_cells(d, selected, honest_sent)))
        if r.get("ai") and r["kind"] == "v2":
            out.append(_row(name, d["seed"], "AI", f"AI calls upcoding (screen: {screen_tuning[0].lower() + screen_tuning[1:]})", "Yes",
                            _ai_cells(d, r["ai"])))
        if r["kind"] == "summaries":
            out.append(_row(name, d["seed"], "AI", f"AI calls upcoding (screen: {screen_tuning[0].lower() + screen_tuning[1:]})",
                            "Yes" if r["records"] else "No", _ai_cells(d, r)))
    return out


def cell(text, ok):
    return "–" if ok is None else f"{PASS if ok else FAIL} {text}"


def markdown(registry_path=None):
    rows = compute(registry_path)
    head = ("| Run | Seed | Screen / AI | Tuning | Records evidence | False negative rate | False positive rate "
            "| Precision of upcoding calls | Citations valid | Case Summary Usefulness (1-5) "
            "| Evals passed |\n|---|---|---|---|---|---|---|---|---|---|---|")
    thr = ("| **Threshold** | | | | | at most 12.5% | at most 12.5% | at least 80% (proposed) | 100% "
           "| at least 4 | |")
    lines = [head, thr]
    for r in rows:
        cells = " | ".join(cell(r["text"][k], r["ok"][k]) for k in ("fn", "fp", "prec", "cite", "useful"))
        lines.append(f"| {r['run']} | {r['seed']} | {r['stage']} | {r['tuning']} | {r['records']} | {cells} | **{r['total']}** |")
    return "\n".join(lines)


if __name__ == "__main__":
    print(markdown())
