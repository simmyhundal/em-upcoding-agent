"""Run the investigator agent on a v2 dataset and score its findings (issues 40, 42, 43, 48).

This SPENDS REAL MONEY (an agent loop on Claude Opus 5.5 with a hard dollar cap): get the user's OK first. The run folder holds
the audit log of every tool call, the office transcript, the agent's findings as case summaries (the same shape the workflow
writes), the citation check and a results file with burden on honest doctors counted from the answer key (read here only).

Usage:
    python eval/run_agent.py RUN_ID CODE_RUN [--no-screen] [--max-usd 3.0] [--records-budget 15] [--max-tool-calls 60]
                             [--model-in-tools] [--correlation 0.0] [--version 3.0|3.1|3.2]
                             [--model claude-sonnet-5-5] [--effort low|medium|high]
e.g. python eval/run_agent.py 261013_3_api 261012_1_code
"""
import argparse
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import agent  # noqa: E402
import agent_tools  # noqa: E402
import case_summary as cs  # noqa: E402
import guardrail  # noqa: E402
import llm  # noqa: E402


def model_call(system, user):
    text, usage = llm.sync_call(cs.MODEL, system, user, cs.LLM_SCHEMA)
    return text, llm.cost(cs.MODEL, usage["input_tokens"], usage["output_tokens"])


EVAL_MAX_USD_32 = 1.00   # also the cap for 3.3
EVAL_RECORDS_BUDGET_33 = 22   # v3.3: the top 10% of 216 providers, the workflow v2.3 list (v3.0 to v3.2 default to 15)
#   # issue 92: the dollar cap for v3.2 runs; release 1 agent runs cost $0.24 to $0.51 (docs/agent_cost.md)


def main(run_id, code_run, screen=True, max_usd=None, records_budget=15, max_tool_calls=60, use_model=False, correlation=0.0, client=None,
         version="3.0", model=None, effort="medium", screen_method=None, top_pct=None):
    """version "3.1" runs the v3.1 agent (office 2.1, note tools, lint); the data folder must be data 2.1 (the note package).
    max_usd None: $3 for 3.0 and 3.1 (as run), EVAL_MAX_USD_32 for 3.2. model and effort default to Opus 5.5 at medium (as run); another model
    is priced from src/llm.py so the dollar cap means dollars for that model (issue 92)."""
    if max_usd is None:
        max_usd = EVAL_MAX_USD_32 if version in ("3.2", "3.3", "3.4", "3.5", "5.0", "5.1", "5.2") else 3.0
    model = model or agent.MODEL
    price_scale = llm.PRICES[model][0] / llm.PRICES["claude-opus-5-5"][0]
    data = os.path.join(ROOT, "data", f"synthetic_v2_{code_run}")
    view = os.path.join(data, "view")
    key = json.load(open(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_{code_run}.json")))["providers"]
    roles = {p: v.get("role", "n/a") for p, v in key.items()}         # data 4.2 has no role: "n/a" (the office uses roles only when correlation > 0)
    office = agent_tools.make_office(data, view, version, seed=1, correlation=correlation, roles=roles)         # roles stay out of the environment; the office keeps them only when correlation > 0
    env = agent_tools.Environment(data, view, seed=1, model_call=model_call if use_model else None, records_budget=records_budget,
                                  screen_enabled=screen, office=office, version=version)
    n_prov, n_claims = len(env.claims), sum(len(v) for v in env.claims.values())
    start_text = "Start by screening the claims." + (f" Begin with screen_providers using method {screen_method}" + (f" and top_pct {top_pct}" if top_pct else "") +
                                                      "; you may change it." if screen_method else "")
    task = (f"The claims book has {n_prov} primary care providers and {n_claims:,} office-visit claims (99211 to 99215) for one year. "
            f"Find the providers most likely upcoding. You may request records for at most {records_budget} providers and make at most "
            f"{max_tool_calls} tool calls. {start_text if screen else 'There is no statistical screen: list the providers and decide yourself where to look.'}")
    out = os.path.join(ROOT, "experiments", run_id)
    res = agent.run_agent(env, task, client=client, max_tool_calls=max_tool_calls, max_usd=max_usd, out_dir=out, model=model, effort=effort,
                          price_scale=price_scale)
    if version == "5.2":                                  # the claims-data lane as score 4.2 reads it (src/agent_tools.py lane_record)
        json.dump(env.lane_record(), open(os.path.join(out, "fwa_lane.json"), "w"))
    records = [{"provider_id": pid, "model": res["model"], "summary": s, "citations_checked": False, "source": "agent"}
               for pid, s in env.findings.items()]
    summaries, checked = os.path.join(out, "case_summaries.jsonl"), os.path.join(out, "case_summaries_checked.jsonl")
    with open(summaries, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    cit = guardrail.run(view, summaries, checked)
    asked = env.office.state
    honest_asked = [p for p in asked if roles[p] != "upcoder"]
    called = [p for p, s in env.findings.items() if s["leaning"] == "pattern_consistent_with_upcoding"]
    results = {"run": run_id, "version": version, "screen_run": code_run, "screen_tool": screen, "stop_reason": res["stop_reason"], "tool_calls": res["tool_calls"],
               "estimated_usd": res["estimated_usd"], "providers_with_findings": len(env.findings),
               "providers_called_upcoding": len(called), "upcoders_found": sum(roles[p] == "upcoder" for p in called),
               "honest_called_upcoding": sum(roles[p] != "upcoder" for p in called),
               "upcoders_total": sum(r == "upcoder" for r in roles.values()),
               "records_requests_to_honest": len(honest_asked), "records_requests_total": len(asked),
               "rounds_on_honest": sum(asked[p]["round"] for p in honest_asked), "citation_accuracy": cit["citation_accuracy"]}
    json.dump(results, open(os.path.join(out, "results.json"), "w"), indent=1)
    open(os.path.join(out, "README.md"), "w").write(
        f"# {run_id}\n\nThe investigator agent v{version} (`src/agent.py`, model {res['model']}) on the v2 data of `{code_run}`, "
        f"{'with' if screen else 'WITHOUT'} the statistical screen tool. Caps: ${max_usd:.2f}, {max_tool_calls} tool calls, records for at most "
        f"{records_budget} providers. Office behavior is independent of upcoder status (correlation {correlation}). "
        f"Findings are drafts for human review.\n\n```\n{json.dumps(results, indent=1)}\n```\n\nFiles: `audit.jsonl` (every tool call), "
        f"`office_transcript.jsonl`, `agent_notes.txt`, `case_summaries*.jsonl`. Answer key: "
        f"`eval/answer_key/ground_truth_v2_{code_run}.json` (gitignored). Frozen workflow baseline: `v2.0`.\n")
    return results


if __name__ == "__main__":
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("run_id")
    ap.add_argument("code_run")
    ap.add_argument("--no-screen", action="store_true")
    ap.add_argument("--max-usd", type=float, help="dollar cap (default $3 for 3.0 and 3.1, $1 for 3.2)")
    ap.add_argument("--records-budget", type=int, default=None, help="providers records may be requested for (default 15; 22 for v3.3)")
    ap.add_argument("--max-tool-calls", type=int, default=60)
    ap.add_argument("--model-in-tools", action="store_true")
    ap.add_argument("--correlation", type=float, default=0.0)
    ap.add_argument("--version", default="3.0", choices=["3.0", "3.1", "3.2", "3.3", "3.4", "3.5", "5.0", "5.1", "5.2"])
    ap.add_argument("--model", choices=sorted(llm.PRICES), help="agent model (default Opus 5.5, as every recorded run)")
    ap.add_argument("--effort", default="medium", choices=["low", "medium", "high"])
    ap.add_argument("--screen-method", choices=["zscore", "riskadj", "combined", "priority", "eb_ratio", "eb_ratio_t"], help="name a starting screen in the task text (release 2: eb_ratio)")
    ap.add_argument("--top-pct", type=float, help="with --screen-method: start with the top PCT percent (release 2: 5)")
    a = ap.parse_args()
    print(json.dumps(main(a.run_id, a.code_run, not a.no_screen, a.max_usd, a.records_budget or (EVAL_RECORDS_BUDGET_33 if a.version in ("3.3", "3.4", "3.5", "5.0", "5.1", "5.2") else 15), a.max_tool_calls, a.model_in_tools,
                          a.correlation, version=a.version, model=a.model, effort=a.effort, screen_method=a.screen_method, top_pct=a.top_pct), indent=1))
