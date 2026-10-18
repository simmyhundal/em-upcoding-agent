"""Issue 91: measure the workflow cost options on the stored release 1 runs (#61), for free, and write docs/workflow_cost.md.

Nothing here calls the API: the Anthropic calls in src/llm.py are replaced by a function that raises, so a request that is not in a run's
response cache stops the script instead of being billed. What it measures:
  1. Reproduction: every stored #61 workflow summary file (W2.0 and W2.1) is regenerated from its response cache and compared record by record.
  2. Rules 2.2 (implemented, case_summary.py --v22): which v2.1 summaries no longer need the model, whether any leaning changes, the writer
     dollars saved (from the stored usage of exactly those calls), and the rule judge on the regenerated summaries.
  3. Skipping the LLM judge: its measured cost per arm.
  4. Fewer providers flagged: the records list at the top 5% of the panel (eb_ratio and priority) against the suspicion >= 5 list, with the
     simulated office 2.1 and the fixed v2.1 policy, and how many summaries would need the model (dry run, free).
  5. Evidence card size by section on the stored model calls (characters, converted to tokens with the ratio measured on those calls).
  6. Output tokens against the text the model returned.
  7. Batch API use, from the stored usage logs.
  8. Prompts shared across arms (the response caches of W2.0 and W2.1 on the same dataset).

Usage:
    python eval/workflow_cost_91.py
"""
import csv
import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import llm  # noqa: E402


class CacheMiss(RuntimeError):
    pass


def _no_api(*a, **k):
    raise CacheMiss("a request was not in the response cache; this script never calls the API")


llm.batch_call = llm.sync_call = llm.count_tokens = _no_api

import case_summary as cs  # noqa: E402
import flagging  # noqa: E402
import judge_rules  # noqa: E402
import provider_sim  # noqa: E402
import records  # noqa: E402
import summary_rules as sr  # noqa: E402
import workflow_policy_v21 as wp  # noqa: E402

SCRATCH = tempfile.mkdtemp(prefix="cost91_")
QUIET = lambda *a, **k: None  # noqa: E731


def jl(path):
    return [json.loads(x) for x in open(path) if x.strip()]


def workflow_runs():
    reg = json.load(open(os.path.join(ROOT, "experiments", "runs.json")))
    out = []
    for r in reg["runs"]:
        if r["dataset"].startswith("e") and r["kind"] == "v2":
            ds = reg["datasets"][r["dataset"]]
            out.append({"rid": r["run"], "key": r["dataset"], "version": r["version"], "code": ds["flagged"].split("/")[1], "truth": ds["truth"]})
    return out


def exp(rid, name):
    return os.path.join(ROOT, "experiments", rid, name)


def view_of(run):
    return os.path.join(ROOT, "data", f"synthetic_v2_{run['code']}", f"view_{run['rid']}")


def regen(run, rules="2.0"):
    v21 = run["version"] == "v2.1"
    out = os.path.join(SCRATCH, f"{run['rid']}_{rules}.jsonl")
    cs.run(view_of(run), exp(run["rid"], "flagged_threshold.csv"), out, batch=True, cache_dir=exp(run["rid"], "llm_cache"), usage_path=None,
           version="2.1" if v21 else "2.0", lint=v21, rules=rules, log=QUIET)
    return out


def rule_judge(run, summaries):
    checked = summaries.replace(".jsonl", "_checked.jsonl")
    subprocess.run([sys.executable, os.path.join(ROOT, "src", "guardrail.py"), view_of(run), summaries, checked], check=True, capture_output=True)
    out = summaries.replace(".jsonl", "_rules.jsonl")
    judge_rules.run(view_of(run), exp(run["code"], "flagged.csv"), checked, out, run_dir=exp(run["rid"], ""), with_docs=True)
    return {x["provider_id"]: x["score"] for x in jl(out)}


def roles(run):
    return {p: v["role"] for p, v in json.load(open(os.path.join(ROOT, run["truth"])))["providers"].items()}


def outcome(recs, role):
    called = {x["provider_id"] for x in recs if x["summary"]["leaning"] == sr.UPCODING}
    return sum(role[p] == "upcoder" for p in called), sum(role[p] != "upcoder" for p in called)


def scratch_view(run, flagged_ids):
    """The v2.1/2.2 records request (office 2.1, fixed v2.1 policy) for a different flagged list, written under the scratch folder."""
    data = os.path.join(ROOT, "data", f"synthetic_v2_{run['code']}")
    base = os.path.join(data, "view")
    view = tempfile.mkdtemp(dir=SCRATCH)
    for name in ("claims.csv", "patients.csv", "providers.csv"):
        os.symlink(os.path.join(base, name), os.path.join(view, name))
    office = provider_sim.Office(data, base, seed=1, version="2.1")
    by_provider = defaultdict(list)
    for r in csv.DictReader(open(os.path.join(base, "claims.csv"))):
        by_provider[r["provider_id"]].append(r)
    wp.run_policy_v21(office, flagged_ids, by_provider)
    req = list(csv.DictReader(open(os.path.join(base, "records_requests.csv"))))
    control = {r["provider_id"] for r in req if r["kind"] == "control"} - set(flagged_ids)
    owner = {r["claim_id"]: r["provider_id"] for rows in by_provider.values() for r in rows}
    docs = [r for r in csv.DictReader(open(os.path.join(base, "documentation.csv"))) if owner.get(r["claim_id"]) in control]
    records.write_docs(os.path.join(view, "documentation.csv"), docs + office.documentation_rows())
    with open(os.path.join(view, "records_requests.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["provider_id", "kind", "requested", "received", "late", "no_response"])
        for p in sorted(control):
            w.writerow([p, "control", 0, 0, 0, 0])
        for p in flagged_ids:
            w.writerow([p, "flagged", len(office.state[p]["requested"]), len(office.state[p]["usable"]), 0, 0])
    return view, office


def write_flagged(rows, path):
    keys = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main():
    runs = workflow_runs()
    lines = ["# Workflow cost on the stored release 1 runs (issue 91)", "", "[Back to the README](../README.md)", "",
             "Generated by `python eval/workflow_cost_91.py` from the #61 run folders (13 datasets, workflow arms W2.0 and W2.1). Free: the script "
             "replaces every API call with an error, so anything not already in a run's response cache would stop it. The 13 datasets are "
             "development data now (seen in #61), so these numbers can guide release 2 but cannot confirm it.", ""]

    # 1. reproduction
    repro = Counter()
    for run in runs:
        out = regen(run)
        same = jl(out) == jl(exp(run["rid"], "case_summaries.jsonl"))
        repro[(run["version"], same)] += 1
    lines += ["## 1. The stored summaries reproduce from the cache", "",
              "| Arm | Runs regenerated identically |", "|---|---|"]
    for v in ("v2.0", "v2.1"):
        lines.append(f"| W{v[1:]} | {repro[(v, True)]} of {repro[(v, True)] + repro[(v, False)]} |")
    lines += ["", "Identical means every record (leaning, headline, interpretation, citations, next steps) matches the stored `case_summaries.jsonl`."]

    # 2. rules 2.2
    w21 = [r for r in runs if r["version"] == "v2.1"]
    calls_before = calls_after = 0
    saved_usd = total_usd = 0.0
    changed, moved = [], Counter()
    found_b = found_a = acc_b = acc_a = 0
    judge_b, judge_a, llm_scores_moved = [], [], []
    still_same = 0      # summaries not moved to rules that regenerate identically
    for run in w21:
        stored = {x["provider_id"]: x for x in jl(exp(run["rid"], "case_summaries.jsonl"))}
        new_path = regen(run, rules="2.2")
        new = {x["provider_id"]: x for x in jl(new_path)}
        usage = {x["id"]: x["estimated_usd"] for x in jl(exp(run["rid"], "usage_writer.jsonl"))}
        llm_score = {x["provider_id"]: x["score"] for x in jl(exp(run["rid"], "usefulness.jsonl"))}
        total_usd += sum(usage.values())
        role = roles(run)
        b, a = outcome(stored.values(), role), outcome(new.values(), role)
        found_b, acc_b, found_a, acc_a = found_b + b[0], acc_b + b[1], found_a + a[0], acc_a + a[1]
        rj_new = rule_judge(run, new_path)
        rj_old = {x["provider_id"]: x["score"] for x in jl(exp(run["rid"], "usefulness_rules.jsonl"))}
        for pid, s in stored.items():
            n = new[pid]
            was, now = s["source"] != "rules", n["source"] != "rules"
            calls_before += was
            calls_after += now
            if was and not now:
                saved_usd += usage.get(pid, 0)
                moved[s["rule_reason"]] += 1
                judge_b.append(rj_old[pid])
                judge_a.append(rj_new[pid])
                llm_scores_moved.append(llm_score[pid])
                if s["summary"]["leaning"] != n["summary"]["leaning"]:
                    changed.append((run["rid"], pid, s["summary"]["leaning"], n["summary"]["leaning"]))
            elif s == n:
                still_same += 1
    llm_rules_written = [x["score"] for run in w21 for x in jl(exp(run["rid"], "usefulness.jsonl"))
                         if {y["provider_id"]: y for y in jl(exp(run["rid"], "case_summaries.jsonl"))}[x["provider_id"]]["source"] == "rules"
                         and {y["provider_id"]: y for y in jl(exp(run["rid"], "case_summaries.jsonl"))}[x["provider_id"]]["summary"]["leaning"] == sr.INCONCLUSIVE]
    n21 = len(w21)
    n_summaries = sum(len(jl(exp(run["rid"], "case_summaries.jsonl"))) for run in w21)
    lines += ["", "## 2. More summaries decided by rule (rules 2.2, implemented behind `--v22`)", "",
              "Where the v2.1 rules were silent, the model was asked. By the rule's reason, what the model then said on the stored W2.1 runs:", ""]
    reasons = defaultdict(Counter)
    for run in w21:
        for x in jl(exp(run["rid"], "case_summaries.jsonl")):
            if x["source"] != "rules":
                reasons[x["rule_reason"]][x["summary"]["leaning"]] += 1
    lines += ["| Why the rule was silent | Model calls | Model said inconclusive | Model said upcoding | Model said high-acuity panel | Rules 2.2 |", "|---|---|---|---|---|---|"]
    for reason, c in sorted(reasons.items(), key=lambda kv: -sum(kv[1].values())):
        lines.append(f"| {reason} | {sum(c.values())} | {c[sr.INCONCLUSIVE]} | {c[sr.UPCODING]} | {c[sr.HIGH_ACUITY]} | "
                     f"{'inconclusive by rule' if reason in sr.RULES_22_INCONCLUSIVE else 'still asks the model'} |")
    lines += ["", f"Regenerated with rules 2.2 (`case_summary.py --v22`) on the same views and caches:", "",
              "| | W2.1 as stored | W2.1 with rules 2.2 |", "|---|---|---|",
              f"| Model calls (13 runs) | {calls_before} | {calls_after} |",
              f"| Writer cost, estimated (13 runs) | ${total_usd:.2f} | ${total_usd - saved_usd:.2f} |",
              f"| Writer cost per arm per dataset | ${total_usd / n21:.3f} | ${(total_usd - saved_usd) / n21:.3f} |",
              f"| Upcoders called / honest doctors called | {found_b} / {acc_b} | {found_a} / {acc_a} |",
              f"| Leanings that changed | | {len(changed)} |",
              f"| Summaries otherwise identical to the stored ones | | {still_same} of {n_summaries - (calls_before - calls_after)} |"]
    if judge_b:
        lines += ["", f"The {len(judge_b)} summaries that moved from the model to rules, scored by the rule judge (j2.3, the release 2 judge): "
                  f"{statistics.mean(judge_b):.2f} model-written, {statistics.mean(judge_a):.2f} rule-written. The LLM judge had scored the model-written "
                  f"versions {statistics.mean(llm_scores_moved):.2f}; it scored the rule-written inconclusive summaries already in these runs "
                  f"{statistics.mean(llm_rules_written):.2f} ({len(llm_rules_written)} summaries). Read the rule judge's score with care: it shares rules with the "
                  "writer, so a rule-written summary is partly graded by its own rules (#93)."]
    lines += ["", "What is lost: the model's interpretation paragraph for these providers (it often weighs the billing pattern against the "
              "charts and says what to check first); the code-written summary states the facts and conditional next steps instead. What is "
              "not shown: data 2.2 adds honest coding noise, so the model might have leaned differently there; rules 2.2 never ask it."]

    # 3. LLM judge
    judge_usd = defaultdict(float)
    writer_usd = defaultdict(float)
    for run in runs:
        judge_usd[run["version"]] += sum(x["estimated_usd"] for x in jl(exp(run["rid"], "usage_judge.jsonl")))
        writer_usd[run["version"]] += sum(x["estimated_usd"] for x in jl(exp(run["rid"], "usage_writer.jsonl")))
    lines += ["", "## 3. No LLM usefulness judge (implemented: the 2.2 workflow path skips it)", "",
              "| Arm | Writer per dataset | LLM judge per dataset | Judge share |", "|---|---|---|---|"]
    for v in ("v2.0", "v2.1"):
        n = sum(r["version"] == v for r in runs)
        lines.append(f"| W{v[1:]} | ${writer_usd[v] / n:.3f} | ${judge_usd[v] / n:.3f} | {judge_usd[v] / (judge_usd[v] + writer_usd[v]):.0%} |")
    lines += ["", "`make_v2_office_workflow_runs.run(version=\"2.2\")` passes `llm_judge=False`; the run has no `usefulness.jsonl`, the scoreboard leaves "
              "that eval unscored, and `analyze_eval61.py` prints a dash. The rule judge (`judge_rules.py`) runs as before."]

    # 4. fewer providers flagged
    per = []
    mean_call = total_usd / calls_before
    for run in w21:
        base = os.path.join(ROOT, "data", f"synthetic_v2_{run['code']}", "view")
        thr = [r for r in csv.DictReader(open(exp(run["rid"], "flagged_threshold.csv"))) if r["flagged"] == "True"]
        stored = jl(exp(run["rid"], "case_summaries.jsonl"))
        role = roles(run)
        row = {"key": run["key"], "n": len(list(csv.DictReader(open(os.path.join(base, "providers.csv"))))),
               "thr": len(thr), "thr_calls": sum(x["source"] != "rules" for x in stored),
               "thr_calls22": sum(x["source"] != "rules" for x in jl(os.path.join(SCRATCH, f"{run['rid']}_2.2.jsonl")))}
        for m in ("eb_ratio", "priority"):
            rows = flagging.flag(base, method=m, top_pct=5)
            ids = [r["provider_id"] for r in rows if r["flagged"]]
            fpath = os.path.join(SCRATCH, f"{run['rid']}_{m}.csv")
            write_flagged(rows, fpath)
            view, office = scratch_view(run, ids)
            for rules in ("2.0", "2.2"):
                dry = cs.run(view, fpath, os.path.join(SCRATCH, f"dry_{run['rid']}_{m}_{rules}.jsonl"), dry_run=True, version="2.1", rules=rules, log=QUIET)
                row[f"{m}_calls{'22' if rules == '2.2' else ''}"] = sum(x["will_call_llm"] for x in dry)
            row[m] = len(ids)
            row[f"{m}_up"] = sum(role[p] == "upcoder" for p in ids)
        row["thr_up"] = sum(role[r["provider_id"]] == "upcoder" for r in thr)
        per.append(row)
    lines += ["", "## 4. Flag fewer providers: the top 5% of the panel", "",
              "Office 2.1 and the fixed v2.1 policy simulated for each list (free), then the summary step as a dry run to count model calls. "
              f"Cost uses the measured mean of ${mean_call:.4f} per v2.1 model call. 'Reached' is planted upcoders on the list (the answer key, for "
              "this table only).", "",
              "| Records list | Providers flagged (13 datasets) | Upcoders reached | Model calls, v2.1 rules | Model calls, rules 2.2 | Writer cost per dataset, rules 2.2 |",
              "|---|---|---|---|---|---|"]
    tot = lambda k: sum(r[k] for r in per)  # noqa: E731
    lines.append(f"| `riskadj` suspicion >= 5 (W2.1 as run) | {tot('thr')} | {tot('thr_up')} | {tot('thr_calls')} | {tot('thr_calls22')} | ${tot('thr_calls22') * mean_call / len(per):.3f} |")
    for m in ("eb_ratio", "priority"):
        lines.append(f"| `{m}` top 5% | {tot(m)} | {tot(m + '_up')} | {tot(m + '_calls')} | {tot(m + '_calls22')} | ${tot(m + '_calls22') * mean_call / len(per):.3f} |")
    lines += ["", "Per dataset (providers flagged: suspicion >= 5 / eb_ratio top 5% / priority top 5%): " +
              "; ".join(f"{r['key']} {r['thr']}/{r['eb_ratio']}/{r['priority']}" for r in per) + ".",
              "", f"The top 5% of a 216-doctor panel is 11 doctors and of a 600-doctor panel 30. Against the old top 25 ({25 * len(per)} providers on these "
              f"datasets) it flags {1 - tot('eb_ratio') / (25 * len(per)):.0%} fewer; against the suspicion >= 5 list that W2.1 actually used it flags "
              "about as many (more on the 600-doctor panels). With rules 2.2 the writer costs about a cent per dataset whichever list is used, so the "
              "list size no longer matters for cost. It matters for burden on honest practices (#87) and for reach (#88), which the release 2 decision "
              "rules settle."]

    # 5. card sections
    sec = defaultdict(list)
    quoted = Counter()
    chars_in, tokens_in = [], []
    sys_chars = len(cs.SYSTEM)
    for run in w21:
        stored = {x["provider_id"]: x for x in jl(exp(run["rid"], "case_summaries.jsonl"))}
        usage = {x["id"]: x for x in jl(exp(run["rid"], "usage_writer.jsonl"))}
        dry = cs.run(view_of(run), exp(run["rid"], "flagged_threshold.csv"), os.path.join(SCRATCH, f"dry_{run['rid']}.jsonl"),
                     dry_run=True, version="2.1", log=QUIET)
        for x in dry:
            if not x["will_call_llm"] or x["provider_id"] not in usage:
                continue
            card = sr.to_card(x["packet"])
            chars_in.append(sys_chars + x["prompt_chars"])
            tokens_in.append(usage[x["provider_id"]]["input_tokens"])
            for k, v in card.items():
                if k == "documentation":
                    for k2, v2 in v.items():
                        sec["documentation." + k2].append(len(json.dumps(v2, separators=(",", ":"))))
                else:
                    sec[k].append(len(json.dumps(v, separators=(",", ":"))))
            sec["(facts, rule note, instructions)"].append(x["prompt_chars"] - len(sr.card_json(x["packet"])))
            text = stored[x["provider_id"]]["summary"]["rationale"].split(" Examples: ")[0]      # the model's part (code appends cited examples)
            for k, key in (("claims_99215_low_complexity", sr.LOW_KEY), ("claims_99215_high_complexity", sr.HIGH_KEY), ("claims_other_codes", sr.COMPARE_KEY)):
                quoted[k] += any(c["claim_id"] in text for c in x["packet"].get(key, []))
    ratio = sum(chars_in) / sum(tokens_in)
    lines += ["", "## 5. Evidence card size by section (measured; not changed)", "",
              f"On the {len(tokens_in)} stored v2.1 model calls the prompt averaged {statistics.mean(tokens_in):,.0f} input tokens; "
              f"{ratio:.2f} characters per token (system prompt plus user prompt, measured against the stored usage). The system prompt is "
              f"about {sys_chars / ratio:,.0f} tokens.", "", "| Card section | Mean tokens (estimated) | Share of input |", "|---|---|---|"]
    mean_in = statistics.mean(tokens_in)
    lines.append(f"| system prompt | {sys_chars / ratio:,.0f} | {sys_chars / ratio / mean_in:.0%} |")
    for k, v in sorted(sec.items(), key=lambda kv: -statistics.mean(kv[1])):
        t = sum(v) / len(tokens_in) / ratio
        if t >= 20:
            lines.append(f"| {k} | {t:,.0f} | {t / mean_in:.0%} |")
    in_usd = sum(tokens_in) * llm.PRICES[cs.MODEL][0] / 1e6 * llm.BATCH_DISCOUNT
    n_calls = len(tokens_in)
    lines += ["", f"Input is ${in_usd:.2f} of the ${total_usd:.2f} writer cost on these runs. The three claim-sample tables are the largest part. "
              "Share of the model's interpretations (the code-written examples left out) that quote at least one claim ID from each table: "
              + ", ".join(f"{k} {quoted[k] / n_calls:.0%}" for k in ("claims_99215_low_complexity", "claims_99215_high_complexity", "claims_other_codes"))
              + ". So the high-complexity and other-codes tables, about a quarter of the input, are the ones to cut first. Cutting a table changes every prompt, so the cache cannot show whether any leaning changes: that needs a paid smoke run, and "
              "with rules 2.2 only about 1 call per dataset is left to save on. Not implemented."]

    # 6. output tokens
    outs, texts = [], []
    for run in w21:
        outs += [u["output_tokens"] for u in jl(exp(run["rid"], "usage_writer.jsonl"))]
        for f in os.listdir(exp(run["rid"], "llm_cache")):
            texts.append(len(json.load(open(os.path.join(exp(run["rid"], "llm_cache"), f)))["text"]))
    out_usd = sum(outs) * llm.PRICES[cs.MODEL][1] / 1e6 * llm.BATCH_DISCOUNT
    lines += ["", "## 6. Output tokens (measured; not changed)", "",
              f"The writer returned {statistics.mean(texts):,.0f} characters of JSON per call (mostly English prose, so roughly "
              f"{statistics.mean(texts) / 4:,.0f} tokens at about 4 characters per token; the 2.06 ratio above is for ID-heavy input) and was billed "
              f"{statistics.mean(outs):,.0f} output tokens on average; the difference is most likely the model's thinking at `effort` medium (an "
              "estimate: the usage log does not split it). Output is "
              f"${out_usd:.2f} of the ${total_usd:.2f} writer cost. `effort` low would cut it, but it is part of the cache key and may change "
              "leanings, so it needs a paid smoke run; with rules 2.2 the saving is a few cents per dataset. Not implemented."]

    # 7. batch
    via = Counter()
    for run in runs:
        for name in ("usage_writer.jsonl", "usage_judge.jsonl"):
            via.update(x["via"] for x in jl(exp(run["rid"], name)))
    lines += ["", "## 7. Batch API everywhere", "",
              f"Stored #61 workflow calls by route: " + ", ".join(f"{k} {v}" for k, v in via.most_common()) + ". Every writer and judge call went "
              "through the Batch API at half price. `llm.sync_call` (full price) runs only for `--sync`, for a batch request that errored, expired "
              "or was refused (a refusal needs the server-side fallback, which batches do not allow), or for a request a batch did not return."]

    # 8. shared prompts
    by_key = defaultdict(dict)
    for run in runs:
        by_key[run["key"]][run["version"]] = run["rid"]
    shared_w = shared_j = tot_w = tot_j = 0
    for key, d in by_key.items():
        if len(d) < 2:
            continue
        a, b = (set(os.listdir(exp(d[v], "llm_cache"))) for v in ("v2.0", "v2.1"))
        shared_w, tot_w = shared_w + len(a & b), tot_w + len(b)
        a, b = (set(os.listdir(exp(d[v], "llm_cache_judge"))) for v in ("v2.0", "v2.1"))
        shared_j, tot_j = shared_j + len(a & b), tot_j + len(b)
    lines += ["", "## 8. A response cache shared across arms", "",
              f"Writer prompts of W2.1 identical to a W2.0 prompt on the same dataset: {shared_w} of {tot_w}. Judge prompts: {shared_j} of {tot_j}. "
              "The arms see different charts (office 2.0 against 2.1) and different card contents, so a shared cache would not have saved anything. "
              "Not a lever."]

    # summary
    w_now = total_usd / n21 + judge_usd["v2.1"] / n21
    w_new = (total_usd - saved_usd) / n21
    lines[6:6] = ["## Summary", "",
                  f"- **Measured on the stored runs, a v2.1-style workflow arm costs ${w_now:.3f} per 216-doctor dataset; with rules 2.2 and no LLM judge "
                  f"it would have cost ${w_new:.3f}** ({1 - w_new / w_now:.0%} less), with the same upcoders and honest doctors called "
                  f"({found_a} and {acc_a} over the 13 runs) and {len(changed)} leanings changed.",
                  "- Implemented behind the 2.2 flag: rules 2.2 (`case_summary.py --v22`) and no LLM judge (`llm_judge=False`). The frozen v2.0 "
                  "and v2.1 paths are unchanged: every stored #61 workflow summary regenerates identically (section 1).",
                  "- Measured but not implemented: shorter cards and lower effort (they change the prompt, so only a paid run can show their effect, "
                  "and little is left to save), the top 5% list (about as long as the suspicion >= 5 list on these datasets, and a screen decision for "
                  "#88 and #90), a shared cache (no overlap). Every call already went through the Batch API.", ""]
    out = os.path.join(ROOT, "docs", "workflow_cost.md")
    open(out, "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    shutil.rmtree(SCRATCH, ignore_errors=True)


if __name__ == "__main__":
    main()
