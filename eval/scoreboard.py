"""Scoreboard: every run against the thresholds, generated from the saved outputs (never typed by hand).

Reads experiments/runs.json. For each run it computes five evals, marks each pass or fail against its threshold, and totals the
evals passed out of those that apply. A dash means not scored or not applicable and is left out of the total.

Evals and thresholds:
  1. False negative rate: at most 12.5% of the real upcoders are missed. (Screen rows: upcoders not flagged. AI rows: upcoders
     the AI did not call upcoding.)
  2. False positive rate: at most 12.5% of the honest doctors are wrongly accused. Honest means every non-upcoder in the data,
     including ordinary doctors and doctors with sicker patients. (Screen rows: flagged. AI rows: called upcoding.)
  3. Precision of "upcoding" calls: at least 80% of the doctors called upcoding really are upcoders (PROPOSED threshold: the
     original targets ignored the many ordinary honest doctors who get flagged). Screen rows: upcoders among the top 25.
  4. Citations valid: 100% of cited claims exist and belong to the provider.
  5. Case Summary Usefulness (1-5): average of at least 4 (LLM judge).
  6. No templating: the templating check finds none.

Usage:
    python eval/scoreboard.py            # prints the markdown table
"""
import csv
import json
import os

import run_eval
import template_check

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_RATE = 0.125       # false negative rate and false positive rate
MIN_USEFULNESS = 4.0
MIN_PRECISION = 0.80   # proposed
TOP_N = 25
PASS, FAIL = "✓", "✗"


def judge(value, kind):
    """Pass/fail for one eval. kind in fn|fp|prec|cite|useful|templ."""
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
    if kind == "templ":
        return not value
    raise ValueError(kind)


def mark(ok):
    return "–" if ok is None else (PASS if ok else FAIL)


def total(oks):
    app = [o for o in oks if o is not None]
    return f"{sum(app)} / {len(app)}"


def _load(path):
    return os.path.join(ROOT, path)


def compute(registry_path=None):
    reg = json.load(open(registry_path or os.path.join(ROOT, "experiments", "runs.json")))
    data = {}
    for key, d in reg["datasets"].items():
        truth = json.load(open(_load(d["truth"])))
        rows = list(csv.DictReader(open(_load(d["flagged"]))))
        ev = run_eval.evaluate(rows, truth, TOP_N)
        roles = [v["role"] for v in truth["providers"].values()]
        data[key] = {"truth": truth, "ev": ev, "rows": rows, "n_up": roles.count("upcoder"),
                     "n_honest": len(roles) - roles.count("upcoder"), "label": d["label"]}
    out = []
    for r in reg["runs"]:
        d = data[r["dataset"]]
        cells = {"fn": None, "fp": None, "prec": None, "cite": None, "useful": None, "templ": None}
        text = {k: "–" for k in cells}
        if r["kind"] == "screen" and r.get("min_suspicion") is not None:
            sel = [x["provider_id"] for x in d["rows"] if float(x["z_adj"]) >= r["min_suspicion"]]
            sc = run_eval.score(sel, d["truth"])
            found = sc["upcoder"]["flagged"]
            honest = sc["hard_negative"]["flagged"] + sc["normal"]["flagged"]
            prec = (found / len(sel)) if sel else None
        elif r["kind"] == "screen":
            c = d["ev"]["Combined list"]
            found, honest, prec = c["upcoders_found"], c["hard_neg_flagged"] + c["normal_flagged"], c["upcoders_found"] / TOP_N
        else:
            recs = run_eval.load_checked(_load(r["checked"]))
            L = run_eval.leaning_stats(recs, d["truth"])
            found, honest, prec = L["true_upcoders_called"], L["honest_called_upcoding"], L["precision"]
            cells["cite"] = run_eval.citation_stats(recs)["accuracy"]
            cells["templ"] = template_check.check([x["summary"]["rationale"] for x in recs])["flagged"]
            if r.get("usefulness"):
                rows = [json.loads(line) for line in open(_load(r["usefulness"])) if line.strip()]
                cells["useful"] = sum(x["score"] for x in rows) / len(rows)
        cells["fn"] = (d["n_up"] - found, d["n_up"])
        cells["fp"] = (honest, d["n_honest"])
        cells["prec"] = prec
        oks = {k: judge(cells[k], k) for k in cells}
        text["fn"] = f"{cells['fn'][0] / cells['fn'][1]:.1%} ({cells['fn'][0]} / {cells['fn'][1]})"
        text["fp"] = f"{cells['fp'][0] / cells['fp'][1]:.1%} ({cells['fp'][0]} / {cells['fp'][1]})"
        if cells["prec"] is not None:
            text["prec"] = f"{cells['prec']:.0%}"
        if cells["cite"] is not None:
            text["cite"] = f"{cells['cite']:.0%}"
        if cells["useful"] is not None:
            text["useful"] = f"{cells['useful']:.2f}"
        if cells["templ"] is not None:
            text["templ"] = "templated" if cells["templ"] else "none"
        out.append({"label": r["label"], "text": text, "ok": oks, "total": total(oks.values())})
    return out


def markdown(registry_path=None):
    rows = compute(registry_path)
    head = ("| Run | False negative rate | False positive rate | Precision of upcoding calls | Citations valid "
            "| Case Summary Usefulness (1-5) | No templating | Evals passed |\n|---|---|---|---|---|---|---|---|")
    thr = ("| **Threshold** | at most 12.5% | at most 12.5% | at least 80% (proposed) | 100% "
           "| at least 4 | none | every eval that applies |")
    lines = [head, thr]
    for r in rows:
        cells = " | ".join(f"{r['text'][k]} {mark(r['ok'][k])}".strip() if r["ok"][k] is not None else "–"
                           for k in ("fn", "fp", "prec", "cite", "useful", "templ"))
        lines.append(f"| {r['label']} | {cells} | **{r['total']}** |")
    return "\n".join(lines)


if __name__ == "__main__":
    print(markdown())
