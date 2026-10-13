"""Tests for the scoreboard thresholds and README freshness. Run: python tests/test_scoreboard.py"""
import os
import sys

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "eval"))
sys.path.insert(0, os.path.join(ROOT, "docs"))
import scoreboard as sb  # noqa: E402


def test_threshold_logic_and_edge_cases():
    assert sb.judge((1, 8), "fn") and not sb.judge((2, 8), "fn")                    # 12.5% is the limit, inclusive
    assert sb.judge((26, 208), "fp") and not sb.judge((27, 208), "fp")             # 26/208 = 12.5% exactly
    assert sb.judge((0, 8), "fn") and sb.judge((0, 208), "fp")
    assert sb.judge(0.8, "prec") and not sb.judge(0.79, "prec")
    assert sb.judge(1.0, "cite") and not sb.judge(0.99, "cite")
    assert sb.judge(4.0, "useful") and not sb.judge(3.99, "useful")
    assert sb.judge(None, "fn") is None                                            # not scored: excluded


def test_total_ignores_unscored_evals():
    assert sb.total([True, False, None, True, None]) == "2 / 3"
    assert sb.total([None, None]) == "0 / 0"


def test_readme_table_is_rendered_from_the_results_file():
    text = open(os.path.join(ROOT, "README.md")).read()
    start = text.index("<!-- scoreboard:start -->") + len("<!-- scoreboard:start -->")
    end = text.index("<!-- scoreboard:end -->")
    assert text[start:end].strip() == sb.markdown_from_csv().strip(), "README table is stale: run python docs/update_readme.py"


def test_results_file_matches_the_saved_outputs():
    import json
    reg = json.load(open(os.path.join(ROOT, "experiments", "runs.json")))
    needed = [os.path.join(ROOT, d["truth"]) for d in reg["datasets"].values()]
    if not all(os.path.exists(p) for p in needed):
        print("skipped: answer keys are gitignored; regenerate them first")
        return
    import csv
    now = sb.compute()
    committed = list(csv.DictReader(open(sb.CSV_PATH)))
    assert len(now) == len(committed)
    for a, b in zip(now, committed):
        assert {k: str(v) for k, v in a.items()} == b, f"experiments/results.csv is stale for {b['run_id']} {b['stage']}: run python eval/scoreboard.py --write"


def test_results_rows_have_the_metadata_columns():
    import csv
    rows = list(csv.DictReader(open(sb.CSV_PATH)))
    assert set(sb.COLUMNS) == set(rows[0])
    for r in rows:
        assert " " not in r["run_id"] and r["seed_status"] in ("development", "held-out") and r["source"] in ("api", "cc", "code")
        assert r["data_version"] in ("v1", "v2") and r["data_description"] and r["upcoder_rate"] and r["upcoder_clone_level"]
        if r["stage"] == "AI":
            assert r["agents"] != ""


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
