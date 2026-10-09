"""Score case-summary usefulness (1-5) with an LLM judge, using eval/rubric.md.

The judge sees the rubric, the evidence packet and the summary. It does NOT see the answer key. A different model from the
summary writer is used by default so the writer does not grade itself. Summaries that failed the citation guardrail score 1
without a model call. The judge is itself an LLM, so treat the scores as a rough rubric check, not a human review.

Usage:
    python eval/judge_usefulness.py DATA_DIR FLAGGED_CSV CHECKED_SUMMARIES_JSONL OUT_JSONL [--limit N]
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

JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "claude-sonnet-5-5")
SCHEMA = {"type": "object",
          "properties": {"score": {"type": "integer", "enum": [1, 2, 3, 4, 5]},
                         "justification": {"type": "string"},
                         "problems": {"type": "array", "items": {"type": "string"}}},
          "required": ["score", "justification", "problems"], "additionalProperties": False}
SYSTEM = """You grade case summaries written for a Special Investigations Unit reviewing outpatient E/M billing (synthetic data).
Score each summary from 1 to 5 using the rubric. Judge only from the evidence packet and the summary. Check that numbers and
claims in the summary match the packet, that cited claims fit the sentences citing them, and that the wording is cautious. Do not
reward length. Be a demanding but fair grader, and name concrete problems."""


def rubric_text():
    return open(os.path.join(HERE, "rubric.md")).read()


def judge_prompt(packet, summary):
    return (f"RUBRIC\n{rubric_text()}\n\nEVIDENCE PACKET (JSON)\n{json.dumps(packet, indent=1)}\n\n"
            f"SUMMARY TO GRADE (JSON)\n{json.dumps(summary, indent=1)}\n\nReturn the score, a short justification and a list of problems.")


def call_anthropic(system, user):
    import anthropic
    client = anthropic.Anthropic()
    resp = client.beta.messages.create(
        model=JUDGE_MODEL, max_tokens=2000, betas=[cs.FALLBACK_BETA], extra_body={"fallbacks": "default"},
        output_config={"effort": "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
        system=system, messages=[{"role": "user", "content": user}])
    if resp.stop_reason == "refusal":
        raise RuntimeError(f"judge refused: {getattr(resp, 'stop_details', None)}")
    return next(b.text for b in resp.content if b.type == "text")


def run(data_dir, flagged_csv, checked_path, out_path, limit=None, llm=call_anthropic):
    chronic, age, conditions, claims = cs.load(data_dir)
    rates, docs = cs.peer_rates(claims, chronic), cs.load_docs(data_dir)
    peer_doc = cs.doc_peer_rates(claims, docs) if docs else None
    flags = {r["provider_id"]: r for r in csv.DictReader(open(flagged_csv))}
    records = [json.loads(line) for line in open(checked_path) if line.strip()]
    if limit:
        records = records[:limit]
    out = []
    for r in records:
        pid = r["provider_id"]
        if not r["citation_check"]["passed"]:
            out.append({"provider_id": pid, "score": 1, "justification": "rejected by the citation guardrail", "problems": [],
                        "judge": None})
            continue
        packet = cs.build_packet(pid, flags[pid], chronic, age, conditions, claims, rates, docs, peer_doc)
        res = json.loads(llm(SYSTEM, judge_prompt(packet, r["summary"])))
        out.append({"provider_id": pid, **res, "judge": JUDGE_MODEL})
    with open(out_path, "w") as f:
        for row in out:
            f.write(json.dumps(row) + "\n")
    return out


def summarize(rows):
    scores = [r["score"] for r in rows]
    return {"n": len(scores), "mean": sum(scores) / len(scores) if scores else None,
            "distribution": {k: scores.count(k) for k in (1, 2, 3, 4, 5)}}


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
    a = ap.parse_args()
    rows = run(a.data_dir, a.flagged_csv, a.checked_summaries, a.out_jsonl, a.limit)
    print(summarize(rows))
