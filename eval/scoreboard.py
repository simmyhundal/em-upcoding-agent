"""Scoreboard: every run against the thresholds, generated from the saved outputs (never typed by hand).

Reads experiments/runs.json. For each run it computes five evals, marks each pass or fail against its threshold, and totals the
evals passed out of those that apply. A dash means not scored or not applicable and is left out of the total.

Evals and thresholds:
  1. Upcoders caught: at least 7 of 8. (Screen rows: upcoders in the top 25. AI rows: upcoders the AI called upcoding.)
  2. Hard negatives wrongly accused: lower than the plain z-score's count on the same data (0 always passes). Hard negatives are
     honest doctors with sicker patients. (Screen rows: flagged. AI rows: called upcoding.)
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
MIN_UPCODERS_FRACTION = 7 / 8
MIN_USEFULNESS = 4.0
MIN_PRECISION = 0.80   # proposed
TOP_N = 25
PASS, FAIL = "✓", "✗"


def judge(value, z_value, kind):
    """Pass/fail for one eval. kind in upcoders|hard|prec|cite|useful|templ."""
    if value is None:
        return None
    if kind == "upcoders":
        return value[0] / value[1] >= MIN_UPCODERS_FRACTION
    if kind == "hard":
        return value[0] < z_value or value[0] == 0
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
        data[key] = {"truth": truth, "ev": ev, "rows": rows, "n_up": roles.count("upcoder"), "n_hn": roles.count("hard_negative"),
                     "z_hard": ev["Plain z-score"]["hard_neg_flagged"], "label": d["label"]}
    out = []
    for r in reg["runs"]:
        d = data[r["dataset"]]
        cells = {"upcoders": None, "hard": None, "prec": None, "cite": None, "useful": None, "templ": None}
        text = {k: "–" for k in cells}
        if r["kind"] == "screen" and r.get("min_suspicion") is not None:
            sel = [x["provider_id"] for x in d["rows"] if float(x["z_adj"]) >= r["min_suspicion"]]
            sc = run_eval.score(sel, d["truth"])
            cells["upcoders"] = (sc["upcoder"]["flagged"], d["n_up"])
            cells["hard"] = (sc["hard_negative"]["flagged"], d["n_hn"])
            cells["prec"] = (sc["upcoder"]["flagged"] / len(sel)) if sel else None
        elif r["kind"] == "screen":
            c = d["ev"]["Combined list"]
            cells["upcoders"] = (c["upcoders_found"], d["n_up"])
            cells["hard"] = (c["hard_neg_flagged"], d["n_hn"])
            cells["prec"] = c["upcoders_found"] / TOP_N
        else:
            recs = run_eval.load_checked(_load(r["checked"]))
            L = run_eval.leaning_stats(recs, d["truth"])
            cells["upcoders"] = (L["true_upcoders_called"], d["n_up"])
            cells["hard"] = (L["table"]["hard_negative"]["upcoding"], d["n_hn"])
            cells["prec"] = L["precision"]
            cells["cite"] = run_eval.citation_stats(recs)["accuracy"]
            cells["templ"] = template_check.check([x["summary"]["rationale"] for x in recs])["flagged"]
            if r.get("usefulness"):
                rows = [json.loads(line) for line in open(_load(r["usefulness"])) if line.strip()]
                cells["useful"] = sum(x["score"] for x in rows) / len(rows)
        oks = {k: judge(cells[k], d["z_hard"], k) for k in cells}
        text["upcoders"] = f"{cells['upcoders'][0]} / {cells['upcoders'][1]}"
        text["hard"] = f"{cells['hard'][0]} / {cells['hard'][1]}"
        if cells["prec"] is not None:
            text["prec"] = f"{cells['prec']:.0%}"
        if cells["cite"] is not None:
            text["cite"] = f"{cells['cite']:.0%}"
        if cells["useful"] is not None:
            text["useful"] = f"{cells['useful']:.2f}"
        if cells["templ"] is not None:
            text["templ"] = "templated" if cells["templ"] else "none"
        out.append({"label": r["label"], "text": text, "ok": oks, "total": total(oks.values())})
    z = ", ".join(f"{d['label']}: {d['z_hard']}" for d in data.values())
    return out, z


def markdown(registry_path=None):
    rows, z = compute(registry_path)
    head = ("| Run | Upcoders caught | Hard negatives wrongly accused | Precision of upcoding calls | Citations valid "
            "| Case Summary Usefulness (1-5) | No templating | Evals passed |\n|---|---|---|---|---|---|---|---|")
    thr = (f"| **Threshold** | at least 7 of 8 | lower than the plain z-score's count ({z}) | at least 80% (proposed) | 100% "
           f"| at least 4 | none | every eval that applies |")
    lines = [head, thr]
    for r in rows:
        cells = " | ".join(f"{r['text'][k]} {mark(r['ok'][k])}".strip() if r["ok"][k] is not None else "–"
                           for k in ("upcoders", "hard", "prec", "cite", "useful", "templ"))
        lines.append(f"| {r['label']} | {cells} | **{r['total']}** |")
    return "\n".join(lines)


if __name__ == "__main__":
    print(markdown())
