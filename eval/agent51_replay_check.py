"""Free end-to-end check of the paid path for agent v5.1, on a development seed (below 5555) that has a near-miss extension. The scripted agent of eval/agent51_parity.py runs on the live environment and its
tool calls are recorded; the same calls are then fed through the real loop (`run_agent.main`, which writes audit.jsonl and the summaries) by a stub client that makes no API call; the run is rebuilt the way the
paid runner scores it (`judge_agent_runs.main` replays audit.jsonl against a fresh office, then `score_40.from_run`); and the score must equal the live environment's. A scratch run id is used and deleted.
Usage: python3 eval/agent51_replay_check.py [SEED ...]   (default 3672 and 4008)"""
import itertools
import json
import os
import shutil
import sys
from types import SimpleNamespace as NS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import agent51_parity as par  # noqa: E402
import judge_agent_runs as jar  # noqa: E402
import run_agent  # noqa: E402
import score_40 as s4  # noqa: E402


class StubClient:
    """Emits the recorded tool calls one per turn; makes no API call."""
    def __init__(self, calls):
        self.calls, self.ids = list(calls), itertools.count()
        self.messages = self

    def create(self, **kw):
        usage = NS(input_tokens=1, output_tokens=1, cache_read_input_tokens=0, cache_creation_input_tokens=0)
        if not self.calls:
            return NS(content=[NS(type="text", text="done")], stop_reason="end_turn", usage=usage)
        name, args = self.calls.pop(0)
        return NS(content=[NS(type="tool_use", id=f"t{next(self.ids)}", name=name, input=args)], stop_reason="tool_use", usage=usage)


def check(seed):
    assert seed < 5555
    code, rid = f"d4_{seed}", f"scratchreplay_{seed}"
    trace = []
    env, asked, extended, called, res = par.scripted(seed, trace=trace)
    live = par.agent_score(env, code, called, len(env.findings))
    calls = list(trace)
    first_submit = next(i for i, (n, _) in enumerate(calls) if n == "submit_findings")
    for pid in sorted(extended):                         # a refused request (a second extension, and one of 80 charts) must be logged but never replayed against the office
        calls.insert(first_submit, ("request_records", {"provider_id": pid, "sample": {"kind": "random", "n": 80}}))
        calls.insert(first_submit, ("request_records", {"provider_id": pid, "sample": {"kind": "random", "n": 30}}))
    try:
        run_agent.main(rid, code, version="5.1", screen_method="eb_upper_t", top_pct=10, records_budget=22, client=StubClient(calls), max_usd=1.0)
        jar.main(rid, code, "5.1")
        stored = s4.from_run(rid, code)
    finally:
        shutil.rmtree(os.path.join(ROOT, "experiments", rid), ignore_errors=True)
        shutil.rmtree(os.path.join(ROOT, "data", f"synthetic_v2_{code}", f"view_{rid}"), ignore_errors=True)
    ok = abs(stored["score"] - live["score"]) < 0.01 and stored["rounds"] == live["rounds"] and stored["charts"] == live["charts"] and stored["demands"] == live["demands"]
    print(seed, "extended", sorted(extended), "| live score", round(live["score"], 2), "stored-path score", round(stored["score"], 2), "| rounds", live["rounds"], stored["rounds"], "charts", live["charts"], stored["charts"],
          "demands", live["demands"], stored["demands"], "| MATCH" if ok else "| MISMATCH")
    return ok


if __name__ == "__main__":
    seeds = [int(a) for a in sys.argv[1:]] or [3672, 4008]
    sys.exit(0 if all([check(s) for s in seeds]) else 1)
