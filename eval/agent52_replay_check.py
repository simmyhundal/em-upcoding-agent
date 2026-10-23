"""Free end-to-end check of the paid path for agent v5.2 on development seeds of data 4.2. The scripted agent of eval/agent52_parity.py runs on the live environment and its tool calls are recorded; the same calls
are fed through the real loop (`run_agent.main`, which writes audit.jsonl, fwa_lane.json and the summaries) by a stub client that makes no API call; the run is rebuilt as the paid runner scores it
(`judge_agent_runs.main` replays audit.jsonl against a fresh office, then `score_42.seed_result`); the score must equal the live environment's. A scratch run id is used and deleted.
Usage: python3 eval/agent52_replay_check.py [SEED ...]   (default 1001 and 1038)"""
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import agent51_replay_check as r51  # noqa: E402  (the stub client)
import agent52_parity as par  # noqa: E402
import judge_agent_runs as jar  # noqa: E402
import run_agent  # noqa: E402
import score_42 as s42  # noqa: E402


def check(seed):
    code, rid = f"d42_{seed}", f"scratchreplay52_{seed}"
    trace = []
    env, asked, extended, called, lane, demands, res = par.scripted(seed, trace=trace)
    live = par.agent_score(env, code, called | demands, len(env.findings))
    try:
        run_agent.main(rid, code, version="5.2", screen_method="eb_upper_t", top_pct=10, records_budget=22, client=r51.StubClient(list(trace)), max_usd=1.0)
        jar.main(rid, code, "5.2")
        stored = s42.seed_result(rid, code)[0]
    finally:
        shutil.rmtree(os.path.join(ROOT, "experiments", rid), ignore_errors=True)
        shutil.rmtree(os.path.join(ROOT, "data", f"synthetic_v2_{code}", f"view_{rid}"), ignore_errors=True)
    ok = abs(stored["score"] - live["score"]) < 1.0 and stored["demands"] == live["demands"] and stored["lane_demands"] == live["lane_demands"]
    print(seed, "lane", sorted(lane), "demands", sorted(demands), "| live score", round(live["score"], 2), "stored-path score", round(stored["score"], 2), "| demands", live["demands"], stored["demands"],
          "| rounds", live["rounds"], stored["rounds"], "charts", live["charts"], stored["charts"], "| MATCH" if ok else "| MISMATCH")
    return ok


if __name__ == "__main__":
    seeds = [int(a) for a in sys.argv[1:]] or [1001, 1038]
    sys.exit(0 if all([check(s) for s in seeds]) else 1)
