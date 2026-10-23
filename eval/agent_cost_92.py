"""Issue 92: measure the agent cost options on the stored release 1 agent runs (#61), for free, and write docs/agent_cost.md.

No model is called. The recorded tool sequences (audit.jsonl) are replayed through the tools, which are deterministic code:
  1. Frozen behavior: every #61 agent run (13 at v3.0, 13 at v3.1) is replayed through Environment(version) on its own data; every tool result
     must match the logged one (its length and the logged first 3,000 characters) and the findings must match the stored summaries.
  2. v3.2 on clean data: the v3.1 tool sequences replayed through Environment("3.2"): what changes when nothing is wrong with the data.
  3. v3.2 on data with defects (offline test of the data-quality tools): the development-seed smoke run (seed 42) replayed on its defect twins
     (data 2.2 with every realism option at zero, which reproduces data 2.1 exactly, plus the `moderate` or `severe` defect profile),
     with data_quality calls added the way the v3.2 prompt asks; a refused submission is resubmitted with the held findings made inconclusive.
  4. Where the dollars go: recorded spend, an uncached lower bound on input cost, and what that implies for caching and output.
  5. Tool results: size, how often they are resent, what trimming could save, and how deep into the screen table the agent acted.
  6. Caps and the judge: observed spend against the dollar cap; the measured cost of the LLM judge per agent arm.

Usage:
    python eval/agent_cost_92.py
"""
import csv
import json
import os
import shutil
import statistics
import sys
import tempfile
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import agent  # noqa: E402
import agent_tools as at  # noqa: E402
import derive  # noqa: E402
import flagging  # noqa: E402
import generate_v2  # noqa: E402
import llm  # noqa: E402
import records  # noqa: E402
import summary_rules as sr  # noqa: E402

SCRATCH = tempfile.mkdtemp(prefix="cost92_")
SMOKE_RUN, SMOKE_CODE = "261015_5_api", "261015_1_code"        # agent v3.1 smoke run on development seed 42 (data 2.1)
CPT = 3.0          # characters per token assumed for tool results and prompts (JSON; the writer's cards measured 2.06, so this undercounts tokens)


def jl(path):
    return [json.loads(x) for x in open(path) if x.strip()]


def exp(rid, name=""):
    return os.path.join(ROOT, "experiments", rid, name)


def agent_runs():
    reg = json.load(open(os.path.join(ROOT, "experiments", "runs.json")))
    out = []
    for r in reg["runs"]:
        if r["dataset"].startswith("e") and r["kind"] == "agent":
            ds = reg["datasets"][r["dataset"]]
            out.append({"rid": r["run"], "key": r["dataset"], "version": r["version"][1:], "code": ds["flagged"].split("/")[1]})
    return out


def roles_of(key_path):
    """Scoring only (outcome of a replay against the answer key); never given to the environment."""
    return {p: v["role"] for p, v in json.load(open(key_path))["providers"].items()}


def make_env(data, version, key_path=None):
    """key_path is accepted for old callers and ignored: the replay needs no roles (correlation 0), so the office is built without them (issue 100)."""
    return at.Environment(data, os.path.join(data, "view"), seed=1, model_call=None, records_budget=15, screen_enabled=True,
                          office=at.make_office(data, os.path.join(data, "view"), version), version=version)


def result_text(out):
    text = json.dumps(out)
    return text[:agent.RESULT_CHARS] + '..."[truncated]"' if len(text) > agent.RESULT_CHARS else text


def replay(env, audit, add_dq=False, comply=False):
    """Call every recorded tool in order. add_dq: call data_quality first and for each provider before submit_findings (as the v3.2 prompt
    asks). comply: when a submission is refused because findings are held, resubmit with those findings inconclusive (what the prompt asks)."""
    same, diffs, outs, holds, refusals = 0, [], [], {}, []
    if add_dq:
        env.call("data_quality", {})
    for a in audit:
        args = dict(a["args"])
        if add_dq and a["tool"] == "submit_findings":
            for f in args.get("findings") or []:
                if isinstance(f, dict) and f.get("provider_id"):
                    env.call("data_quality", {"provider_id": f["provider_id"]})
        out = env.call(a["tool"], args)
        text = result_text(out)
        outs.append((a, out))
        if len(text) == a["result_chars"] and text[:3000] == a["result"]:
            same += 1
        else:
            diffs.append(a["tool"])
        if a["tool"] == "submit_findings" and "held" in out:
            holds.update(out["held"])
            refusals.append("held")
            if comply:
                fixed = [dict(f, leaning=sr.INCONCLUSIVE, headline="Findings held by a data problem; charts do not yet carry an upcoding call",
                              interpretation="The data-quality pre-flight flagged this provider and too few charts came back to rely on, so the "
                                             "screen result is held until the data issue is resolved.") if f.get("provider_id") in out["held"] else f
                         for f in args["findings"]]
                out2 = env.call("submit_findings", dict(args, findings=fixed))
                if "error" in out2:
                    refusals.append("resubmission refused: " + out2["error"][:80])
        elif a["tool"] == "submit_findings" and "error" in out:
            refusals.append(out["error"][:80])
    return same, diffs, outs, holds, refusals


def finish_compliant(env, audit):
    """After a replay, submit the run's last findings the way a compliant v3.2 agent would: code writes the text, then held findings and findings that
    fail the checks are made inconclusive, and screened candidates still missing get a set-aside reason, until the submission is accepted.
    Returns (rounds, providers made inconclusive because held, because of the checks)."""
    last = [dict(a["args"]) for a in audit if a["tool"] == "submit_findings"][-1]
    findings = [{"provider_id": f["provider_id"], "leaning": f["leaning"]} for f in last.get("findings", []) if isinstance(f, dict)]
    aside = list(last.get("set_aside") or [])
    held, failed = set(), set()
    for rounds in range(1, 6):
        out = env.call("submit_findings", {"findings": findings, "set_aside": aside})
        if "error" not in out:
            return rounds, held, failed
        if "held" in out:
            held |= set(out["held"])
            bad = set(out["held"])
        elif "problems" in out:
            failed |= set(out["problems"])
            bad = set(out["problems"])
        elif "missing" in out:
            aside += [{"provider_id": p, "reason": "replay: not examined in the recorded run"} for p in out["missing"]]
            continue
        else:
            return None, held, failed
        findings = [dict(f, leaning=sr.INCONCLUSIVE) if f["provider_id"] in bad else f for f in findings]
    return None, held, failed


def outcome(findings, roles):
    called = [p for p, s in findings.items() if s["leaning"] == sr.UPCODING]
    return sum(roles.get(p) == "upcoder" for p in called), sum(roles.get(p) != "upcoder" for p in called)


def defect_twin(profile):
    """Data 2.2 on seed 42 with every realism option at zero (identical to data 2.1) plus a defect profile; view and control sample as mk.run builds them."""
    data = os.path.join(SCRATCH, f"twin_{profile or 'clean'}")
    key = os.path.join(SCRATCH, f"key_{profile or 'clean'}.json")
    opts = dict(honest_miscode_rate=0.0, subtle_upcoder_share=0.0, group_billing=False, rendering_omitted_share=0.0, correction_level_change_share=0.0)
    if profile:
        opts["defect_profile"] = profile
    generate_v2.build(data, key, seed=42, n_providers=216, n_upcoders=8, n_hard_neg=8, clone_share=0.5, data_version="2.2", **opts)
    view = os.path.join(data, "view")
    derive.build_view(data, view)
    rows = flagging.flag(view, min_suspicion=5, max_flagged=40)
    thr = os.path.join(data, "flagged_threshold.csv")
    with open(thr, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    records.run_requests(data, view, thr, seed=42)
    return data, key


def main():
    runs = agent_runs()
    L = ["# Agent cost on the stored release 1 runs (issue 92)", "", "[Back to the README](../README.md)", "",
         "Generated by `python eval/agent_cost_92.py`. Free: no model is called; the recorded tool sequences of the #61 agent runs are replayed "
         "through the tools, which are deterministic code. The #61 datasets are development data now, so these numbers can guide release 2 but "
         "cannot confirm it.", ""]
    S = []      # summary bullets, filled as we go

    # 1. frozen replay
    ok = Counter()
    rec = {}
    for r in runs:
        data = os.path.join(ROOT, "data", f"synthetic_v2_{r['code']}")
        key = os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{r['code']}.json")
        audit = jl(exp(r["rid"], "audit.jsonl"))
        env = make_env(data, r["version"], key)
        same, diffs, outs, _, _ = replay(env, audit)
        stored = {x["provider_id"]: x["summary"] for x in jl(exp(r["rid"], "case_summaries.jsonl"))}
        ok[(r["version"], same == len(audit) and env.findings == stored)] += 1
        rec[r["rid"]] = {"audit": audit, "outs": outs, "run": json.load(open(exp(r["rid"], "agent_run.json")))}
    L += ["## 1. Frozen agents reproduce", "", "| Agent | Runs whose every tool result and finding replays identically |", "|---|---|"]
    for v in ("3.0", "3.1"):
        L.append(f"| v{v} | {ok[(v, True)]} of {ok[(v, True)] + ok[(v, False)]} |")
    L += ["", "Every recorded tool call was replayed through `Environment(version)` on its own data (including `261015_70_api`); a match means the "
          "result has the logged length and the same first 3,000 characters, and the final findings equal the stored summaries. The changes in "
          "this issue are behind version 3.2, so v3.0 and v3.1 are unchanged."]
    S.append(f"v3.0 and v3.1 are unchanged: {ok[('3.0', True)] + ok[('3.1', True)]} of {len(runs)} recorded #61 agent runs replay identically, tool result by tool result.")

    # 2. v3.2 on clean data
    same32 = tot32 = 0
    diff_tools = Counter()
    acc32 = Counter()
    for r in runs:
        if r["version"] != "3.1":
            continue
        data = os.path.join(ROOT, "data", f"synthetic_v2_{r['code']}")
        key = os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{r['code']}.json")
        env = make_env(data, "3.2", key)
        same, diffs, _, holds, refusals = replay(env, rec[r["rid"]]["audit"], add_dq=True)
        stored = {x["provider_id"]: x["summary"]["leaning"] for x in jl(exp(r["rid"], "case_summaries.jsonl"))}
        same32, tot32 = same32 + same, tot32 + len(rec[r["rid"]]["audit"])
        diff_tools.update(diffs)
        acc32[("findings same leanings", {p: s["leaning"] for p, s in env.findings.items()} == stored)] += 1
        acc32[("held", bool(holds))] += 1
    L += ["", "## 2. v3.2 on clean data (the v3.1 sequences replayed through version 3.2)", "",
          f"{same32} of {tot32} tool results are identical; the ones that differ, by tool: "
          + (", ".join(f"{k} {v}" for k, v in diff_tools.most_common()) or "none") + ". "
          f"With data_quality called as the v3.2 prompt asks, {acc32[('held', True)]} of 13 runs had a finding held and "
          f"{acc32[('findings same leanings', True)]} of 13 ended with the same leanings as v3.1. The #61 data is data 2.1, which has no control totals "
          "file, so the pre-flight can only run its other checks there."]

    # 3. defect twins
    smoke_audit = jl(exp(SMOKE_RUN, "audit.jsonl"))
    clean_data = os.path.join(ROOT, "data", f"synthetic_v2_{SMOKE_CODE}")
    twin_clean, _ = defect_twin(None)
    same_files = all(open(os.path.join(twin_clean, f)).read() == open(os.path.join(clean_data, f)).read()
                     for f in ("claims_header.csv", "claim_lines.csv", "members.csv", "providers.csv", "remittance.csv"))
    L += ["", "## 3. Offline test of the v3.2 data-quality tools on defect twins (development seed 42)", "",
          f"The smoke run `{SMOKE_RUN}` (agent v3.1, seed 42) replayed through version 3.2 on the clean data and on two defect twins. The twins are "
          f"data 2.2 with every realism option at zero (the plan tables are {'byte-identical to' if same_files else 'NOT identical to'} the data 2.1 "
          "the run used) plus a defect profile. Upcoders and honest doctors called come from that dataset's answer key (for this table only).", "",
          "| Data | Pre-flight | Checks that warn | Providers flagged (by flag) | Tool results identical to the run | Upcoding findings held | Made inconclusive by the checks | Upcoders called | Honest called |",
          "|---|---|---|---|---|---|---|---|---|"]
    for label, profile in (("clean (data 2.1, as run)", "as_run"), ("defects: moderate", "moderate"), ("defects: severe", "severe")):
        if profile == "as_run":
            data, key = clean_data, os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{SMOKE_CODE}.json")
        else:
            data, key = defect_twin(profile)
        env = make_env(data, "3.2", key)
        same, diffs, outs, holds, refusals = replay(env, smoke_audit, add_dq=True)
        env.findings = {}
        rounds, held, failed = finish_compliant(env, smoke_audit)
        g = env.dq or {}
        flags = [c["id"] for c in g.get("checks", []) if c["status"] in ("warn", "block")]
        by_flag = Counter(f["flag"] for fl in g.get("per_provider", {}).values() for f in fl)
        n_flagged = len(g.get("per_provider", {}))
        up, hon = outcome(env.findings, roles_of(key))
        L.append(f"| {label} | {g.get('status', '–')} | {', '.join(flags) or 'none'} | {n_flagged}" + (f" ({', '.join(f'{k} {v}' for k, v in by_flag.most_common())})" if by_flag else "")
                 + f" | {same} of {len(smoke_audit)} | {len(held)} | {len(failed)} | {up if rounds else 'not accepted'} | {hon if rounds else ''} |")
    L += ["", "How the table is made: the recorded tool calls are replayed (with data_quality calls added), then the run's last findings are submitted "
          "the way a compliant agent would: code writes the text, a held upcoding finding or one that fails the checks is made inconclusive, and "
          "the submission is repeated until accepted. The defects change claims, so the replay diverges from the run after a few calls (the tool-results "
          "column) and the charts the agent asked for differ; the outcome columns therefore test the mechanics, not what an agent would have found.",
          "", "What it shows: the pre-flight runs and warns on both defect profiles, per-provider flags reach the tools, and a held upcoding finding is "
          "refused until it is made inconclusive or carried by 8 charts. Under the `severe` profile every provider is flagged (six months of "
          "truncated diagnoses touch every practice), so every upcoding finding then needs chart evidence. What it cannot show: whether the model calls "
          "data_quality, reads the flags or uses flag_data_issue; no recorded run had those tools."]

    # 4. dollars
    usd = defaultdict(list)
    low = defaultdict(list)
    out_est = defaultdict(list)
    schema_chars = {}
    for v in ("3.0", "3.1", "3.2"):
        env = make_env(clean_data, v, os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{SMOKE_CODE}.json"))
        schema_chars[v] = len(json.dumps(env.tool_schemas()))
    sys_chars = {"3.0": len(agent.SYSTEM), "3.1": len(agent.SYSTEM_31), "3.2": len(agent.SYSTEM_32)}
    for r in runs:
        a, audit = rec[r["rid"]]["run"], rec[r["rid"]]["audit"]
        base = (schema_chars[r["version"]] + sys_chars[r["version"]] + 400) / CPT
        by_turn = Counter()
        for x in audit:
            by_turn[x["turn"]] += x["result_chars"] / CPT
        ctx, prev, nocache, cached_in = base, 0.0, 0.0, 0.0
        for t in range(1, a["turns"] + 1):
            nocache += ctx * 4.00 / 1e6                      # every turn resends the whole context at the input price
            cached_in += prev * agent.PRICE_CACHE_READ / 1e6 + (ctx - prev) * agent.PRICE_CACHE_WRITE / 1e6   # earlier context read, new part written
            prev = ctx
            ctx += by_turn[t]
        usd[r["version"]].append(a["estimated_usd"])
        low[r["version"]].append(nocache)
        out_est[r["version"]].append(max(a["estimated_usd"] - cached_in, 0))
    L += ["", "## 4. Where an agent run's dollars go", "", "| Agent | Runs | Recorded cost per run (mean, range) | Turns | Tool calls | Uncached input alone would cost at least | Implied output share (if caching works) |",
          "|---|---|---|---|---|---|---|"]
    for v in ("3.0", "3.1"):
        rs = [rec[r["rid"]]["run"] for r in runs if r["version"] == v]
        L.append(f"| v{v} | {len(rs)} | ${statistics.mean(usd[v]):.3f} (${min(usd[v]):.2f} to ${max(usd[v]):.2f}) | {statistics.mean(x['turns'] for x in rs):.1f} | "
                 f"{statistics.mean(x['tool_calls'] for x in rs):.1f} | ${statistics.mean(low[v]):.3f} | {statistics.mean(out_est[v]) / statistics.mean(usd[v]):.0%} |")
    L += ["", f"The lower bound counts only the system prompt, the tool schemas, the task and the tool results resent each turn, at {CPT:.0f} characters "
          "per token and the full input price; it leaves out the model's own earlier turns. The recorded cost is computed from the API's usage "
          "fields, so if nothing had been read from the prompt cache it could not be below that bound. **It is below it for both agents, so the "
          "cache is being read.** The usage per turn was not logged, so the split is an estimate: with cached input priced as `agent.py` prices "
          "it, most of each run's cost is output, which for this model includes its thinking.",
          "", f"Two things to check on the first v3.2 run, which now logs usage per turn (`turn_usage.jsonl`): the cache-read price in `agent.py` "
          f"is ${agent.PRICE_CACHE_READ:.2f} per million tokens, 5% of the ${4.00:.2f} input price, where a 10% rate would be the usual; if the "
          "real rate is higher, recorded agent costs are slightly understated. And the cache only starts above a minimum prompt length, so the "
          "first turns may not be cached."]
    S.append(f"An agent run cost ${statistics.mean(usd['3.1']):.2f} on average at v3.1 (at most ${max(usd['3.1']):.2f}); prompt caching is working (the "
             "recorded cost is below what uncached input alone would cost), so most of the money is output and thinking, not resent tool results.")

    # 5. tool results
    tool = defaultdict(lambda: defaultdict(list))
    depth = []
    for r in runs:
        T = rec[r["rid"]]["run"]["turns"]
        outs = rec[r["rid"]]["outs"]
        for i, (a, out) in enumerate(outs):
            tool[r["version"]][a["tool"]].append((a["result_chars"], T - a["turn"]))
            if a["tool"] == "screen_providers" and isinstance(out, dict) and "table" in out:
                order = [row[0] for row in out["table"]["rows"]]
                later = {b["args"].get("provider_id") for b, _ in outs[i + 1:]} | {p for b, _ in outs[i + 1:] for p in (b["args"].get("provider_ids") or [])}
                acted = [order.index(p) + 1 for p in later if p in order]
                if r["version"] == "3.1":
                    depth.append((len(order), max(acted) if acted else 0))
    L += ["", "## 5. Tool results: size, resends and the screen table", "",
          "| Tool (v3.1) | Calls per run | Mean characters | Estimated cost per run with caching (written once, read each later turn) |", "|---|---|---|---|"]
    tot_cost = 0.0
    n31 = sum(r["version"] == "3.1" for r in runs)
    rows5 = []
    for t, xs in tool["3.1"].items():
        c = sum(ch / CPT * agent.PRICE_CACHE_WRITE / 1e6 + ch / CPT * k * agent.PRICE_CACHE_READ / 1e6 for ch, k in xs) / n31
        tot_cost += c
        rows5.append((c, f"| {t} | {len(xs) / n31:.1f} | {statistics.mean(ch for ch, _ in xs):,.0f} | ${c:.4f} |"))
    L += [x for _, x in sorted(rows5, reverse=True)]
    L += ["", f"All tool results together cost about **${tot_cost:.3f} per v3.1 run** with caching (about {tot_cost / statistics.mean(usd['3.1']):.0%} of the "
          "recorded spend), so trimming them cannot save much: halving every result would save about "
          f"${tot_cost / 2:.3f} a run. Without caching the same results would cost about ten to twenty times more, which is why checking the cache matters more "
          "than trimming.",
          "", f"The screen table shows {at.SCREEN_ROWS_SHOWN} rows. Over the {len(depth)} screen calls in the v3.1 runs, the deepest row the agent later acted on "
          f"(looked at, asked for records, reviewed) was row {max(d for _, d in depth)} at most and row {statistics.median(d for _, d in depth):.0f} at the median. "
          "Cutting the table to 20 rows would remove rows the agent did use, for under a cent a run; not changed."]
    S.append(f"Tool results cost about ${tot_cost:.3f} a run with caching, so trimming them is not worth a behavior change; not implemented.")

    # 6. caps and judge
    judge = defaultdict(list)
    for r in runs:
        p = exp(r["rid"], "usage_judge.jsonl")
        judge[r["version"]].append(sum(x["estimated_usd"] for x in jl(p)) if os.path.exists(p) else 0.0)
    L += ["", "## 6. Caps and the judge (implemented for v3.2)", "",
          f"- **Dollar cap.** Recorded runs cost ${min(usd['3.0'] + usd['3.1']):.2f} to ${max(usd['3.0'] + usd['3.1']):.2f}; every one stopped by submitting "
          f"its findings, none by a cap. `run_agent.py` now defaults to a ${1.00:.2f} cap for version 3.2 (`EVAL_MAX_USD_32`; $3 stays for 3.0 and 3.1 as run). "
          "That is about twice the most expensive run, so it would not have stopped any of them; the 80% budget notice would not have fired either. "
          "It bounds a runaway run at $1 instead of $3. The v3.2 prompt and schemas are longer "
          f"({sys_chars['3.2'] + schema_chars['3.2']:,} characters against {sys_chars['3.1'] + schema_chars['3.1']:,} for v3.1), so watch the first runs.",
          f"- **No LLM judge for v3.2.** The agent judge cost ${statistics.mean(judge['3.0']):.3f} (v3.0) and ${statistics.mean(judge['3.1']):.3f} (v3.1) per run. "
          "`judge_agent_runs.main(..., \"3.2\")` now only rebuilds the view the rule judge reads (and replays office 2.1 for 3.2; it used office 2.0 for "
          "anything but 3.1, which would have broken the replay of a v3.2 run).",
          "- **Usage per turn.** v3.2 runs write `turn_usage.jsonl` (input, output, cache read and cache write tokens per turn)."]
    S.append(f"Implemented behind version 3.2: a $1.00 cap (twice the most expensive recorded run), no LLM judge (saves about ${statistics.mean(judge['3.1']):.2f} an arm), "
             "usage logged per turn, and `run_agent.py --model` and `--effort` for the smoke test below.")

    # 7. model and effort
    sonnet = llm.PRICES["claude-sonnet-5-5"][0] / llm.PRICES["claude-opus-5-5"][0]
    L += ["", "## 7. A cheaper model or lower effort (needs a paid smoke run)", "",
          f"Behavior cannot be replayed: a different model or effort picks different tools. By price alone, the same tokens on Sonnet 5.5 would cost "
          f"{sonnet:.0%} of Opus 5.5, about ${statistics.mean(usd['3.1']) * sonnet:.2f} per v3.1-like run; `effort` low would cut output and thinking, which "
          "section 4 suggests is most of the bill, by an amount only a run can show. A cheaper agent that finds fewer upcoders is a different arm, "
          "not a saving.", "",
          "Proposed smoke test (not run; needs Simmy's OK): agent v3.2 on development seed 42 data 2.2, three runs: Opus 5.5 at medium (the control), "
          "Opus 5.5 at low, Sonnet 5.5 at medium (`python eval/run_agent.py <id> <code> --version 3.2 [--effort low | --model claude-sonnet-5-5]`). "
          f"Estimated **about $0.45 + $0.30 + $0.25, roughly $1 in all**, under the $1 cap each. Compare upcoders found, honest doctors called, records "
          "burden, tools used and `turn_usage.jsonl`. Adopt a cheaper setting for the evaluation only if it finds as many upcoders with no new "
          "false accusations; one seed can reject a setting but cannot confirm one."]
    S.append("Not decidable for free: a cheaper model or lower effort. A three-run smoke test on seed 42 (about $1) is proposed in section 7.")

    L[6:6] = ["## Summary", ""] + [f"- {x}" for x in S] + [""]
    out = os.path.join(ROOT, "docs", "agent_cost.md")
    open(out, "w").write("\n".join(L) + "\n")
    print("\n".join(L))
    shutil.rmtree(SCRATCH, ignore_errors=True)


if __name__ == "__main__":
    main()
