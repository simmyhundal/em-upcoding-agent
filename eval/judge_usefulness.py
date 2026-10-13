"""Score case-summary usefulness (1-5) with an LLM judge, using eval/rubric.md.

The judge sees the rubric, the compact evidence card, the summary and the result of a deterministic number check
(eval/numcheck.py, so the model does not have to verify arithmetic). It does NOT see the answer key. A different model from the
summary writer is used by default so the writer does not grade itself. Summaries that failed the citation guardrail score 1
without a model call. The judge is itself an LLM, so treat the scores as a rough rubric check, not a human review.

The judge runs through the Batch API by default (half price) with a response cache and usage logging; --sync sends one request
at a time.

Usage:
    python eval/judge_usefulness.py DATA_DIR FLAGGED_CSV CHECKED_SUMMARIES_JSONL OUT_JSONL [--limit N] [--sync] [--estimate]
                                    [--cache-dir DIR] [--usage-jsonl FILE]
Needs ANTHROPIC_API_KEY (environment or .env).
"""
import argparse
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import case_summary as cs  # noqa: E402
import llm as llm_mod  # noqa: E402
import numcheck  # noqa: E402
import summary_rules as sr  # noqa: E402

JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "claude-sonnet-5-5")
SCHEMA = {"type": "object",
          "properties": {"score": {"type": "integer", "enum": [1, 2, 3, 4, 5]},
                         "justification": {"type": "string"},
                         "problems": {"type": "array", "items": {"type": "string"}}},
          "required": ["score", "justification", "problems"], "additionalProperties": False}
SYSTEM = """You grade case summaries written for a Special Investigations Unit reviewing outpatient E/M billing (synthetic data).
Score each summary from 1 to 5 using the rubric. Judge only from the evidence packet and the summary. Check that numbers and
claims in the summary match the evidence card, that cited claims fit the sentences citing them, and that the wording is cautious. A
script has already checked every number in the summary against the card and lists any it could not match: weigh those, but a
listed number may be a legitimate sum or ratio. Parts of a summary (the numeric facts, the example claims and the next steps) are
written by code from a fixed format, and that is acceptable; judge whether the whole is usable by an investigator. Do not reward
length. Be a demanding but fair grader, and name concrete problems."""


def rubric_text():
    return open(os.path.join(HERE, "rubric.md")).read()


def judge_prompt(packet, summary, check):
    flagged = (f"The number check could not match these numbers in the summary to the card: {', '.join(check['unverified'])}."
               if check["unverified"] else "The number check matched every number in the summary to the card.")
    return (f"RUBRIC\n{rubric_text()}\n\nEVIDENCE CARD (compact JSON)\n{sr.card_json(packet)}\n\n"
            f"SUMMARY TO GRADE (JSON)\n{json.dumps(summary, separators=(',', ':'))}\n\n{flagged}\n\n"
            "Return the score, a short justification and a list of problems.")


def call_anthropic(system, user):
    return llm_mod.sync_call(JUDGE_MODEL, system, user, SCHEMA, max_tokens=2000)[0]


def run(data_dir, flagged_csv, checked_path, out_path, limit=None, llm=None, batch=False, cache_dir=None, usage_path=None,
        estimate=False, assume_output_tokens=300, log=print):
    chronic, age, conditions, claims = cs.load(data_dir)
    rates, docs = cs.peer_rates(claims, chronic), cs.load_docs(data_dir)
    peer_doc = cs.doc_peer_rates(claims, docs, cs.control_providers(data_dir)) if docs else None
    facts = cs.load_doc_facts(data_dir)
    flags = {r["provider_id"]: r for r in csv.DictReader(open(flagged_csv))}
    records = [json.loads(line) for line in open(checked_path) if line.strip()]
    if limit:
        records = records[:limit]
    out, items, meta = {}, [], {}
    for r in records:
        pid = r["provider_id"]
        if not r["citation_check"]["passed"]:
            out[pid] = {"provider_id": pid, "score": 1, "justification": "rejected by the citation guardrail", "problems": [],
                        "judge": None, "unverified_numbers": []}
            continue
        packet = cs.build_packet(pid, flags[pid], chronic, age, conditions, claims, rates, docs, peer_doc, facts)
        check = numcheck.verify(r["summary"], packet)
        meta[pid] = check
        items.append((pid, SYSTEM, judge_prompt(packet, r["summary"], check)))
    if estimate:
        n_in = [llm_mod.count_tokens(JUDGE_MODEL, s, u) for _, s, u in items]
        usd = llm_mod.cost(JUDGE_MODEL, sum(n_in), assume_output_tokens * len(items), batch=True)
        log(f"judge: {len(items)} calls, input {sum(n_in):,} tokens; estimated ${usd:.2f} at batch price assuming "
            f"{assume_output_tokens} output tokens each")
        return {"calls": len(items), "input_tokens": sum(n_in), "estimated_usd": usd}
    if llm is not None:
        got = {pid: (llm(s, u), {"input_tokens": 0, "output_tokens": 0}, "sync") for pid, s, u in items}
    else:
        got = llm_mod.run_requests(items, JUDGE_MODEL, SCHEMA, cache_dir, batch=batch, max_tokens=2000, log=log)
    for pid, (text, _, _) in got.items():
        out[pid] = {"provider_id": pid, **json.loads(text), "judge": JUDGE_MODEL, "unverified_numbers": meta[pid]["unverified"]}
    rows = [out[r["provider_id"]] for r in records]
    with open(out_path, "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")
    if usage_path and got and llm is None:
        total = llm_mod.write_usage(usage_path, JUDGE_MODEL, [(pid, u, via) for pid, (_, u, via) in got.items()])
        log(f"estimated judge spend: ${total:.2f} ({len(got)} model calls; usage in {usage_path})")
    return rows


def summarize(rows):
    scores = [r["score"] for r in rows]
    clean = [r for r in rows if r.get("judge") is not None]
    return {"n": len(scores), "mean": sum(scores) / len(scores) if scores else None,
            "distribution": {k: scores.count(k) for k in (1, 2, 3, 4, 5)},
            "summaries_with_all_numbers_verified": (sum(1 for r in clean if not r.get("unverified_numbers")) / len(clean)) if clean else None}


if __name__ == "__main__":
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    ap = argparse.ArgumentParser()
    for n in ("data_dir", "flagged_csv", "checked_summaries", "out_jsonl"):
        ap.add_argument(n)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--sync", action="store_true", help="one request at a time instead of the Batch API")
    ap.add_argument("--estimate", action="store_true", help="count tokens (free) and print the estimated cost; no billed call")
    ap.add_argument("--cache-dir")
    ap.add_argument("--usage-jsonl")
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.out_jsonl))
    rows = run(a.data_dir, a.flagged_csv, a.checked_summaries, a.out_jsonl, a.limit, batch=not a.sync,
               cache_dir=a.cache_dir or os.path.join(base, "llm_cache_judge"),
               usage_path=a.usage_jsonl or os.path.join(base, "usage_judge.jsonl"), estimate=a.estimate)
    if not a.estimate:
        print(summarize(rows))
