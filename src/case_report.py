"""Build one readable markdown page per flagged provider: the case summary, its cited claims, and the evidence chart.

Inputs are the guardrail-checked summaries and the SVG charts. Output is plain markdown that links to the chart.
Rejected summaries (failed citation check) get a banner instead of the analysis text.

Usage:
    python src/case_report.py CHECKED_SUMMARIES_JSONL CHARTS_DIR OUT_DIR
"""
import json
import os
import sys

LEAN = {"pattern_consistent_with_upcoding": "Pattern consistent with upcoding",
        "pattern_consistent_with_high_acuity_panel": "Pattern consistent with a high-acuity panel",
        "inconclusive": "Inconclusive"}


def render(record, chart_rel):
    s, chk = record["summary"], record["citation_check"]
    lines = [f"# {record['provider_id']}: {s['headline']}", ""]
    if not chk["passed"]:
        lines += [f"> **Rejected by the citation guardrail** ({chk['reason']}). The text below is not reliable.", ""]
    lines += [f"**Leaning (advisory):** {LEAN.get(s['leaning'], s['leaning'])}", "",
              "## Why", "", s["rationale"], "",
              "## Evidence chart", "", f"![99215 share by patient complexity]({chart_rel})", "",
              "## Cited claims", "", ", ".join(f"`{c}`" for c in s["cited_claim_ids"]) or "none", "",
              "## Suggested next steps", ""]
    lines += [f"- {x}" for x in s["next_steps"]]
    lines += ["", "---",
              f"Citations checked: {chk['n_valid']}/{chk['n_cited']} valid. Synthetic data. The leaning is advisory; "
              "the flag comes from the statistical screen, and no clinical documentation is available beyond the sampled "
              "records-review facts shown in the packet."]
    return "\n".join(lines) + "\n"


def build(checked_path, charts_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    records = [json.loads(line) for line in open(checked_path) if line.strip()]
    index = ["# Case reports", "", "| Provider | Leaning | Citations | Page |", "|---|---|---|---|"]
    for r in records:
        pid = r["provider_id"]
        chart = os.path.join(charts_dir, f"{pid}.svg")
        rel = os.path.relpath(chart, out_dir)
        with open(os.path.join(out_dir, f"{pid}.md"), "w") as f:
            f.write(render(r, rel))
        c = r["citation_check"]
        index.append(f"| {pid} | {LEAN.get(r['summary']['leaning'], r['summary']['leaning'])} | "
                     f"{'passed' if c['passed'] else 'REJECTED'} | [{pid}.md]({pid}.md) |")
    with open(os.path.join(out_dir, "index.md"), "w") as f:
        f.write("\n".join(index) + "\n")
    return len(records)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    print(f"{build(*sys.argv[1:])} case reports -> {sys.argv[3]}")
