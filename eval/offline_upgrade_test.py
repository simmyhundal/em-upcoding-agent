"""Free, offline test of the deterministic upgrades on the recorded runs (no model calls; v2.0 and v3.0 results are not changed).

Upgrades tested (issues 63, 66 and the 18/19 error analysis): conditional next steps (version 2.1 summaries), the pre-submission lint,
estimate reliability, coverage of screened candidates, and the leaning guard. Writes docs/offline_upgrade_test.md.

Usage:
    python eval/offline_upgrade_test.py
"""
import csv
import json
import os
import sys
import tempfile
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import agent_tools as at  # noqa: E402
import case_summary as cs  # noqa: E402
import guardrail  # noqa: E402
import judge_agent_runs as jar  # noqa: E402
import judge_rules  # noqa: E402
import summary_lint  # noqa: E402
import summary_rules as sr  # noqa: E402
import judge_usefulness as ju  # noqa: E402

WORKFLOW_RUNS = [("261013_12_api", "261013_4_code", "flagged_threshold.csv"), ("261013_13_api", "261013_5_code", "flagged_threshold.csv"),
                 ("261013_14_api", "261013_4_code", "flagged.csv"), ("261013_15_api", "261013_5_code", "flagged.csv")]
AGENT_RUNS = [("261013_8_api", "261013_4_code"), ("261013_9_api", "261013_5_code"), ("261013_16_api", "261013_4_code"), ("261013_17_api", "261013_4_code"),
              ("261013_18_api", "261013_5_code"), ("261013_19_api", "261013_5_code")]


def mean(rows):
    return sum(r["score"] for r in rows) / len(rows)


def defects(rows):
    c = Counter()
    for r in rows:
        c.update(r["deductions"].keys())
    return dict(c)


def workflow_part(out):
    out += ["## Workflow summaries regenerated with the version 2.1 changes (from the response cache, free)", "",
            "Same model words (cached), same evidence; only the next steps change (conditional on records, naming claims and counts) and a model-written summary that fails a hard check is repaired by code.", "",
            "| Run | Summaries | Rule-judge mean before | after | Contradictions before | after | Generic next steps before | after | Repaired by the lint |", "|---|---|---|---|---|---|---|---|---|"]
    for rid, code, flagged in WORKFLOW_RUNS:
        data = os.path.join(ROOT, "data", f"synthetic_v2_{code}", f"view_{rid}")
        run = os.path.join(ROOT, "experiments", rid)
        tmp = tempfile.mkdtemp()
        new = cs.run(data, os.path.join(run, flagged), os.path.join(tmp, "s.jsonl"), cache_dir=os.path.join(run, "llm_cache"), batch=False,
                     version="2.1", lint=True, log=lambda *a: None)
        guardrail.run(data, os.path.join(tmp, "s.jsonl"), os.path.join(tmp, "c.jsonl"))
        after = judge_rules.run(data, os.path.join(run, flagged), os.path.join(tmp, "c.jsonl"), os.path.join(tmp, "j.jsonl"), run_dir=run)
        before = [json.loads(line) for line in open(os.path.join(run, "usefulness_rules.jsonl"))]
        bd, ad = defects(before), defects(after)
        out.append(f"| {rid} | {len(after)} | {mean(before):.2f} | {mean(after):.2f} | {bd.get('contradictions', 0)} | {ad.get('contradictions', 0)} | "
                   f"{bd.get('generic_next_steps', 0)} | {ad.get('generic_next_steps', 0)} | {sum(1 for r in new if r.get('lint_repaired'))} |")
    out.append("")


def agent_part(out):
    out += ["## Agent findings from the recorded v3.0 runs", ""]
    rows_lint, est_rows, cov_rows = [], [], []
    for rid, code in AGENT_RUNS:
        run = os.path.join(ROOT, "experiments", rid)
        data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
        view = jar.build_view(rid, code)
        chronic, age, conditions, claims = cs.load(view)
        rates, docs = cs.peer_rates(claims, chronic), cs.load_docs(view)
        peer_doc = cs.doc_peer_rates(claims, docs, cs.control_providers(view)) if docs else None
        facts = cs.load_doc_facts(view)
        flags = {r["provider_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "experiments", code, "flagged.csv")))}
        truth = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code}.json")))["providers"]
        events = [json.loads(line) for line in open(os.path.join(run, "office_transcript.jsonl"))]
        audit = [json.loads(line) for line in open(os.path.join(run, "audit.jsonl"))]
        found = [json.loads(line) for line in open(os.path.join(run, "case_summaries_checked.jsonl"))]
        hard, new_steps_fix, n = Counter(), 0, 0
        for r in found:
            pid = r["provider_id"]
            packet = cs.build_packet(pid, flags[pid], chronic, age, conditions, claims, rates, docs or None, peer_doc, facts)
            ev = summary_lint.evidence_from(events, audit, pid)
            sm = dict(r["summary"])
            sm["next_steps"] = sr.next_steps_21(packet, sm["leaning"], sm["cited_claim_ids"])      # what version 3.1 would have attached
            l = summary_lint.lint(sm, packet, ev)
            n += 1
            for msg in l["hard"]:
                hard[msg.split(" ")[0] if not msg.startswith("leaning") else "leaning"] += 1
            rejected = bool(l["hard"])
            hard["summaries with at least one hard defect"] += rejected
        rows_lint.append((rid, n, hard))
        # estimate reliability: reviewed charts in the 99215 stratum for each estimate the agent requested
        office = jar.replay(rid, code)[2]
        by_cpt = {r["claim_id"]: r["cpt"] for rs in claims.values() for r in rs}
        for a in audit:
            if a["tool"] == "estimate_overpayment":
                pid = a["args"]["provider_id"]
                ids = office.random_claim_ids(pid)
                n215 = sum(1 for c in ids if by_cpt.get(c) == "99215" and c in office.state[pid]["usable"])
                est_rows.append((rid, pid, n215))
        # coverage of screened candidates
        env = at.Environment(data, view, seed=1)             # the recorded runs used the v3.0 tools, so replay their screens with them
        cands = set()
        for a in audit:
            if a["tool"] == "screen_providers":
                res = env.screen_providers(**a["args"])
                cands |= {row[0] for row in res["table"]["rows"] if row[3] and row[2] / row[3] >= at.CANDIDATE_RATIO}
        have = {r["provider_id"] for r in found}
        missing = sorted(c for c in cands if c not in have)
        cov_rows.append((rid, len(cands), len(missing), sum(truth[c]["role"] == "upcoder" for c in missing), sum(truth[c]["role"] == "upcoder" for c in cands)))
    out += ["### Pre-submission lint: hard defects in what the agent wrote (with the version 3.1 conditional next steps attached)", "", "| Run | Summaries | with a hard defect | numbers | leaning | contradictions | accusatory | unreliable estimate |", "|---|---|---|---|---|---|---|---|"]
    for rid, n, h in rows_lint:
        out.append(f"| {rid} | {n} | {h['summaries with at least one hard defect']} | {h['numbers']} | {h['leaning']} | {h['says']} | {h['accusatory']} | {h['quotes']} |")
    low = sum(1 for _, _, k in est_rows if k < at.MIN_STRATUM_REVIEWED)
    out += ["", f"### Estimate reliability: {low} of {len(est_rows)} overpayment estimates rested on fewer than {at.MIN_STRATUM_REVIEWED} reviewed 99215 charts "
            f"(counts: {sorted(Counter(k for _, _, k in est_rows).items())})", "",
            "### Coverage: screened candidates (99215 at 3 or more times expected) the agent neither examined nor explained", "",
            "| Run | Candidates in its screens | Missing from its findings | of which real upcoders | Real upcoders among all candidates |", "|---|---|---|---|---|"]
    for rid, c, m, mu, cu in cov_rows:
        out.append(f"| {rid} | {c} | {m} | {mu} | {cu} |")
    out.append("")


def main():
    out = ["# Offline test of the deterministic upgrades", "", "Generated by `python eval/offline_upgrade_test.py`. No model calls: the recorded v2.0 and v3.0 runs are replayed or "
           "regenerated from the response cache. This shows what the upgrades would catch or fix; it cannot show whether an agent that is held to them finds more upcoders (that needs runs).", ""]
    workflow_part(out)
    agent_part(out)
    open(os.path.join(ROOT, "docs", "offline_upgrade_test.md"), "w").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
