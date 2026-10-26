"""Data 4.3 (issue 197; data card docs/data_v4_3.md): the files and columns of data 4.2, the answer key's schema (every field the scorer, oracle and metrics read, no binary label), determinism per seed,
data 4.3 with every option off equals data 4.2, held-out mechanism families, the public behaviour of office 4.3 (a chart can come back for a visit the payer cannot otherwise verify, some charts come
back only after the claim is asked about again, chart rows keep office 4.2's columns), and earlier data versions and offices unchanged. Builds a few small datasets.
Run: python tests/test_data_v43.py"""
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import derive  # noqa: E402
import generate_v2  # noqa: E402
import generate_v43  # noqa: E402
import provider_sim  # noqa: E402

FORBIDDEN = ("role", "planted", "above_margin", "above_p95", "subtle", "planted_below_line", "upcoder_definition", "upcoder_margin")
FWA_ON = dict(nr_prob=1.0, imp_prob=1.0, unb_prob=1.0, pad_prob=1.0, fabricate_prob=1.0)
_CACHE, _TMP = {}, []


def dataset(seed, n=60, tag="", version="4.3", **opts):
    k = (seed, n, tag, version)
    if k not in _CACHE:
        tmp = tempfile.mkdtemp()
        _TMP.append(tmp)
        out, key = os.path.join(tmp, "data"), os.path.join(tmp, "key", "key.json")
        generate_v2.build(out, key, seed=seed, n_providers=n, data_version=version, **opts)
        derive.build_view(out, os.path.join(out, "view"))
        claims = defaultdict(list)
        for r in csv.DictReader(open(os.path.join(out, "view", "claims.csv"))):
            claims[r["provider_id"]].append(r)
        _CACHE[k] = (out, json.load(open(key)), claims)
    return _CACHE[k]


def _tree(out):
    h = {}
    for dp, _, fs in os.walk(out):
        for f in sorted(fs):
            p = os.path.join(dp, f)
            h[os.path.relpath(p, out)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h


def _cols(path):
    return next(iter(csv.reader(open(path))))


def _keys(obj, acc=None):
    acc = set() if acc is None else acc
    if isinstance(obj, dict):
        for k, v in obj.items():
            acc.add(k)
            if k not in ("justified_cpt_by_claim", "fraud_claims", "fraud_claim_mechanism", "date_batched_claims"):
                _keys(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            _keys(v, acc)
    return acc


def test_earlier_data_versions_and_offices_reproduce():
    import test_d40_regression as t40
    import test_d42_regression as t42
    import test_generator_regression as t2
    t2.test_data_2x_reproduces()
    t40.test_data_40_reproduces()
    t42.test_data_42_reproduces()
    t42.test_offices_20_21_42_reproduce()


def test_with_every_option_off_data_43_equals_data_42():
    for seed, n, extra in ((7, 40, {}), (3, 30, dict(nr_prob=1.0, imp_prob=1.0, unb_prob=1.0))):
        tmp = tempfile.mkdtemp()
        try:
            generate_v2.build(os.path.join(tmp, "a"), os.path.join(tmp, "ka.json"), seed=seed, n_providers=n, data_version="4.2", **extra)
            generate_v2.build(os.path.join(tmp, "b"), os.path.join(tmp, "kb.json"), seed=seed, n_providers=n, data_version="4.3", **{**generate_v43.OFF_43, "stream_family": 42, **extra})
            assert _tree(os.path.join(tmp, "a")) == _tree(os.path.join(tmp, "b"))
            ka, kb = json.load(open(os.path.join(tmp, "ka.json"))), json.load(open(os.path.join(tmp, "kb.json")))
            assert ka["justified_cpt_by_claim"] == kb["justified_cpt_by_claim"] and ka["fraud_claims"] == kb["fraud_claims"]
            for pid, v in ka["providers"].items():
                assert all(kb["providers"][pid][f] == v[f] for f in v if f != "intent"), pid
        finally:
            shutil.rmtree(tmp)


def test_same_files_and_columns_as_data_42_plus_the_office_files():
    out2, _, _ = dataset(7, n=40, version="4.2")
    out3, _, _ = dataset(7, n=40)
    f2, f3 = set(_tree(out2)), set(_tree(out3))
    assert f2 <= f3 and f3 - f2 == {os.path.join("records", "office_chart_plan.csv"), os.path.join("records", "office_profiles.csv")}, f3 ^ f2
    for f in f2:
        if f.endswith(".csv"):
            assert _cols(os.path.join(out2, f)) == _cols(os.path.join(out3, f)), f
    assert _cols(os.path.join(out3, "records", "office_chart_plan.csv")) == generate_v43.PLAN_COLS
    assert _cols(os.path.join(out3, "records", "office_profiles.csv")) == ["npi", "behavior"]
    # chart element levels are never blank; documented minutes are a whole number or blank
    for r in csv.DictReader(open(os.path.join(out3, "records", "records_universe.csv"))):
        assert all(r[k] != "" and 0 <= int(r[k]) <= 4 for k in ("problems_level", "data_level", "risk_level")), r
        assert r["documented_minutes"] == "" or int(r["documented_minutes"]) >= 0


def test_the_answer_key_keeps_the_scorer_schema_and_has_no_binary_label():
    for seed in (7, 8):
        out, k, claims = dataset(seed)
        assert not set(FORBIDDEN) & _keys(k), set(FORBIDDEN) & _keys(k)
        assert k["data_version"] == "4.3" and "parameters" not in k
        assert {"fraud_claims", "justified_cpt_by_claim", "fraud_claim_mechanism", "fabricated_chart_claims", "date_batched_claims", "holdout_families"} <= set(k)
        assert set(k["fraud_claims"].values()) <= {"not_rendered", "impossible_days"} and set(k["fraud_claim_mechanism"]) == set(k["fraud_claims"])
        assert set(k["fabricated_chart_claims"]) <= set(k["fraud_claims"])
        for pid, v in k["providers"].items():
            assert {"habit", "intent", "net_rate", "true_overpay_level_net", "true_overpay_level_gross", "true_overpay_fwa", "true_overpay_total", "target_net_rate",
                    "fwa_mechanisms", "legit_volume", "extra_rendered_visits", "fabricates_charts", "dx_coding", "in_house_lab", "office_behavior"} <= set(v)
            assert set(v["true_overpay_fwa"]) == {"not_rendered", "impossible_days", "unbundling"}
            assert set(v["intent"]) >= {"level_upcoding", "cloned_notes", "not_rendered", "impossible_days", "unbundling", "fabricated_charts", "diagnosis_inflation", "unneeded_tests"}
            assert abs(v["true_overpay_total"] - (max(v["true_overpay_level_net"], 0) + sum(v["true_overpay_fwa"].values()))) < 0.02
        # the level truth on rendered claims of the view matches the key (what eval/d42_truth.py and score 4.2 compute)
        import eval61_recovery as rec
        import score_40 as s4
        for pid in list(k["providers"])[:30]:
            t = s4.provider_truth([r for r in claims[pid] if r["claim_id"] not in k["fraud_claims"]], k["justified_cpt_by_claim"], rec.allowed())
            assert abs(t["net_overpay"] - k["providers"][pid]["true_overpay_level_net"]) < 1.0, pid


def test_nothing_payer_visible_reads_the_answer_key():
    out, k, claims = dataset(3, n=40, tag="fwa", **FWA_ON)
    assert _cols(os.path.join(out, "view", "claims.csv")) == ["claim_id", "provider_id", "patient_id", "service_date", "cpt", "place_of_service", "diagnosis_codes", "has_test_line",
                                                                "allowed_amount", "paid_amount"]
    blob = "".join(open(os.path.join(out, "view", f)).read()[:300000] for f in ("claims.csv", "providers.csv", "patients.csv")).lower()
    blob += open(os.path.join(out, "records", "visit_notes.csv")).read().lower()
    for w in ("habit", "upcoder", "systematic", "unrendered", "phantom", "fraud", "not_rendered", "fabricat", "reconstruct", "never rendered", "ghost", "padded"):
        assert w not in blob, w
    for f in ("office_chart_plan.csv", "office_profiles.csv", "unrendered_claims.csv"):
        assert not os.path.exists(os.path.join(out, "view", f)) and os.path.exists(os.path.join(out, "records", f))
    for f in os.listdir(os.path.join(ROOT, "src")):
        if f.endswith(".py") and not f.startswith(("generate_", "defects_")):
            text = open(os.path.join(ROOT, "src", f)).read()
            assert "fraud_claims" not in text and "ground_truth" not in text and "fabricated_chart" not in text, f


def test_data_quality_preflight_stays_ok():
    import data_quality
    for args in ((8, 60, ""), (3, 40, "fwa")):
        out, _, _ = dataset(args[0], n=args[1], tag=args[2], **(FWA_ON if args[2] else {}))
        checks = data_quality.run_checks(out)["checks"]
        assert checks and all(c["status"] in ("ok", "not_available") for c in checks), [c for c in checks if c["status"] not in ("ok", "not_available")]


def _run_office(out, pid, ask, version, seed, follow=4):
    o = provider_sim.Office(out, os.path.join(out, "view"), seed=seed, version=version)
    r = o.send_request(pid, ask)
    for _ in range(follow):
        if r.get("error") or not r.get("deficiencies") or r.get("rounds_left", 0) <= 0:
            break
        r = o.follow_up(pid, [d["code"] for d in r["deficiencies"]])
    return o


def test_office_43_can_return_a_chart_for_a_claim_office_42_has_no_record_of():
    out, k, claims = dataset(3, n=40, tag="fwa", **FWA_ON)
    fraud, fab = k["fraud_claims"], set(k["fabricated_chart_claims"])
    assert fab and set(fraud) - fab
    pid = next(p for p in claims if any(r["claim_id"] in fab for r in claims[p]) and any(r["claim_id"] in fraud and r["claim_id"] not in fab for r in claims[p]))
    mine = [r["claim_id"] for r in claims[pid]]
    ask = {"kind": "targeted", "claim_ids": [c for c in mine if c in fab][:8] + [c for c in mine if c in fraud and c not in fab][:8] + [c for c in mine if c not in fraud][:8]}
    got43, nr43, late = set(), set(), False
    o42_keys = None
    for seed in range(1, 25):
        o = _run_office(out, pid, ask, "4.3", seed)
        got43 |= set(o.state[pid]["usable"])
        for e in o.transcript:
            for d in e.get("deficiencies", []):
                if d["code"] == "NO_RECORD":
                    nr43 |= set(d["claim_ids"])
        first = next((e for e in o.transcript if e.get("status") == "complete" and e.get("round") == 1), None)
        if first is not None and set(first["usable_claim_ids"]) & fab != set(o.state[pid]["usable"]) & fab:
            late = True
        o42 = _run_office(out, pid, ask, "4.2", seed)
        assert not set(o42.state[pid]["usable"]) & set(fraud)                        # office 4.2: never a chart for these claims
        if o42.state[pid]["usable"] and o42_keys is None:
            o42_keys = set(next(iter(o42.state[pid]["usable"].values())))
        for row in o.state[pid]["usable"].values():                                  # office 4.3 chart rows keep office 4.2's columns, and a chart is a chart
            assert o42_keys is None or set(row) == o42_keys
            assert row["documented_mdm_level"] in ("minimal", "straightforward", "low", "moderate", "high")
    assert got43 & fab, "office 4.3 never returned a chart for those claims"
    assert nr43 and nr43 <= set(fraud) - fab                                          # the others are still reported as no record
    assert late, "no chart arrived only after a second ask"


def test_office_43_chart_rows_write_like_office_42_rows():
    import records
    out, k, claims = dataset(8)
    pids = sorted(claims)[:6]
    rows = []
    for pid in pids:
        o = _run_office(out, pid, {"kind": "random", "n": 20}, "4.3", 1)
        o.request_audit_trail(pid, sorted(o.state[pid]["usable"])[:5]) if o.state[pid]["usable"] else None
        rows += o.documentation_rows()
    tmp = tempfile.mkdtemp()
    _TMP.append(tmp)
    records.write_docs(os.path.join(tmp, "documentation.csv"), rows)          # raises if a row carries a column office 4.2 rows do not have
    import note_checks
    assert _cols(os.path.join(tmp, "documentation.csv")) == records.DOC_COLS + note_checks.NOTE_DOC_COLS
    assert {r["auth_status"] for r in rows} <= {"signed", "e_signed", "unsigned", "illegible", "attested", "amended"}


def test_holdout_families_switch_a_mechanism_off():
    out, k, _ = dataset(3, n=40, tag="hold", holdout_families=("padded_days", "fabricated_charts"), **FWA_ON)
    assert k["holdout_families"] == ["padded_days", "fabricated_charts"]
    assert "padded_days" not in set(k["fraud_claim_mechanism"].values()) and not k["fabricated_chart_claims"]
    assert not any(v["fwa_mechanisms"]["padded_days"] or v["fabricates_charts"] for v in k["providers"].values())
    try:
        generate_v43.config({"holdout_families": ("no_such_family",)})
        raise AssertionError("an unknown family must be refused")
    except ValueError:
        pass
    assert set(generate_v43.FAMILIES) >= {"shared_npi", "coverage", "compressed_schedule", "quick_visit_days", "date_batching", "ghost_panel", "spike_days", "padded_days", "unbundling",
                                         "fabricated_charts", "diagnosis_inflation", "sparse_diagnoses"}


def test_the_build_is_deterministic_and_seeds_differ():
    tmp = tempfile.mkdtemp()
    try:
        hs = []
        for i, seed in enumerate((5, 5, 6)):
            out, key = os.path.join(tmp, f"d{i}"), os.path.join(tmp, f"k{i}.json")
            generate_v2.build(out, key, seed=seed, n_providers=30, data_version="4.3")
            h = _tree(out)
            h["key"] = hashlib.sha256(open(key, "rb").read()).hexdigest()
            hs.append(h)
        assert hs[0] == hs[1] and hs[0]["claims_header.csv"] != hs[2]["claims_header.csv"]
    finally:
        shutil.rmtree(tmp)


def test_the_build_command_and_the_pools():
    tmp = tempfile.mkdtemp()
    try:
        r = subprocess.run([sys.executable, os.path.join(ROOT, "src", "generate_v2.py"), os.path.join(tmp, "out"), "--seed", "11", "--providers", "25", "--data-version", "4.3",
                            "--answer-key", os.path.join(tmp, "key", "k.json"), "--holdout-family", "spike_days"], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        k = json.load(open(os.path.join(tmp, "key", "k.json")))
        assert k["data_version"] == "4.3" and k["holdout_families"] == ["spike_days"]
    finally:
        shutil.rmtree(tmp)
    import dev_pool_v43 as pool
    import make_d43_dev
    assert pool.DEV == [1003 + 41 * j for j in range(100)] and pool.CONFIRM == [1004 + 41 * j for j in range(100)]
    assert pool.TEST == [6003 + 41 * j for j in range(10)] and pool.RESERVED == [7003 + 41 * j for j in range(10)]
    for s in (pool.TEST[0], pool.RESERVED[0], pool.CONFIRM[0]):
        try:
            make_d43_dev.build(s)
            raise AssertionError(f"seed {s} must not be built without its flag")
        except AssertionError as e:
            assert "not in a buildable" in str(e), e


if __name__ == "__main__":
    try:
        for name, fn in list(globals().items()):
            if name.startswith("test_"):
                fn()
                print("ok", name)
    finally:
        for tmp in _TMP:
            shutil.rmtree(tmp, ignore_errors=True)
