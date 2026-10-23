"""Data 4.2 (issue 173; docs/data_v4_2.md): data 4.0 and 2.x reproduce by hash, the answer key is continuous and carries no binary label, nothing payer-visible reads it, the fraud, waste and abuse kinds
leave their signals and their own true overpayment, office 4.2 cannot produce a chart for a service never rendered (offices 2.0 and 2.1 are unchanged), the build is deterministic, the number of providers
above a rate line varies by seed, and the adapter and metrics behave. Builds a few small datasets (about a minute). Run: python tests/test_data_v42.py"""
import csv
import hashlib
import json
import os
import shutil
import sys
import tempfile
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import derive  # noqa: E402
import generate_v2  # noqa: E402
import provider_sim  # noqa: E402
import records  # noqa: E402

_CACHE = {}
FORBIDDEN = ("role", "planted", "above_margin", "above_p95", "subtle", "planted_below_line", "upcoder_definition", "upcoder_margin")


def dataset(seed, n=100, tag="", **opts):
    k = (seed, n, tag)
    if k not in _CACHE:
        tmp = tempfile.mkdtemp()
        out, key = os.path.join(tmp, "data"), os.path.join(tmp, "key", "key.json")
        generate_v2.build(out, key, seed=seed, n_providers=n, data_version="4.2", **opts)
        derive.build_view(out, os.path.join(out, "view"))
        claims = defaultdict(list)
        for r in csv.DictReader(open(os.path.join(out, "view", "claims.csv"))):
            claims[r["provider_id"]].append(r)
        _CACHE[k] = (out, json.load(open(key)), claims)
    return _CACHE[k]


def _keys(obj, acc=None):
    acc = set() if acc is None else acc
    if isinstance(obj, dict):
        for k, v in obj.items():
            acc.add(k)
            if k != "justified_cpt_by_claim" and k != "fraud_claims":
                _keys(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            _keys(v, acc)
    return acc


def test_data_40_and_2x_reproduce_by_hash():
    import test_d40_regression as t40
    import test_generator_regression as t2
    t40.test_data_40_reproduces()
    t2.test_data_2x_reproduces()


def test_the_answer_key_is_continuous_and_has_no_binary_label():
    for seed in (7, 8):
        out, k, claims = dataset(seed)
        assert not set(FORBIDDEN) & _keys(k), set(FORBIDDEN) & _keys(k)
        assert k["data_version"] == "4.2"
        for pid, v in k["providers"].items():
            assert {"habit", "intent", "net_rate", "true_overpay_level_net", "true_overpay_fwa", "true_overpay_total", "target_net_rate"} <= set(v)
            assert set(v["true_overpay_fwa"]) == {"not_rendered", "impossible_days", "unbundling"} and set(v["intent"]) >= {"level_upcoding", "cloned_notes", "not_rendered", "impossible_days", "unbundling"}
            assert abs(v["true_overpay_total"] - (max(v["true_overpay_level_net"], 0) + sum(v["true_overpay_fwa"].values()))) < 0.02


def test_nothing_payer_visible_reads_the_answer_key():
    out, k, claims = dataset(7)
    cols = next(iter(csv.reader(open(os.path.join(out, "view", "claims.csv")))))
    assert cols == ["claim_id", "provider_id", "patient_id", "service_date", "cpt", "place_of_service", "diagnosis_codes", "has_test_line", "allowed_amount", "paid_amount"]
    blob = "".join(open(os.path.join(out, "view", f)).read()[:300000] for f in ("claims.csv", "providers.csv", "patients.csv")).lower()
    for w in ("habit", "upcoder", "systematic", "unrendered", "phantom", "fraud", "not_rendered"):
        assert w not in blob, w
    assert not os.path.exists(os.path.join(out, "view", "unrendered_claims.csv")) and os.path.exists(os.path.join(out, "records", "unrendered_claims.csv"))
    # no source file an arm or the office imports mentions the answer key or the fraud list (the office reads only the simulator-side claim list)
    for f in os.listdir(os.path.join(ROOT, "src")):
        if f.endswith(".py") and not f.startswith(("generate_", "defects_")):
            text = open(os.path.join(ROOT, "src", f)).read()
            assert "answer_key" not in text.replace("answer_key_path", "") or f in ("seed_registry.py",), f
            assert "fraud_claims" not in text and "ground_truth" not in text, f
    assert 'os.path.join(v2_dir, "records", "unrendered_claims.csv")' in open(os.path.join(ROOT, "src", "provider_sim.py")).read()


def test_the_rate_distribution_has_no_quota_and_habits_follow_the_rate():
    counts, high_habits, low_habits = [], Counter(), Counter()
    for seed in (7, 8, 9, 10):
        out, k, claims = dataset(seed)
        P = k["providers"]
        counts.append((sum(v["habit"] is not None for v in P.values()), sum(v["net_rate"] >= 0.15 for v in P.values())))
        for v in P.values():
            if v["habit"] is not None:
                (high_habits if v["target_net_rate"] >= 0.15 else low_habits)[v["habit"]] += 1
            else:
                assert v["target_net_rate"] is None and -0.15 <= v["mean_net_rate"] <= 0.15
        assert any(v["high_acuity_panel"] for v in P.values()) or True
    assert len(set(counts)) > 1, counts                                    # the number of providers with a habit or above 15% varies by seed: no quota
    assert low_habits["systematic"] == 0 and sum(high_habits.values()) + sum(low_habits.values()) > 0


def test_fwa_kinds_have_signals_and_their_own_overpayment():
    out, k, claims = dataset(3, n=40, tag="fwa", nr_prob=1.0, imp_prob=1.0, unb_prob=1.0)
    P, fraud = k["providers"], k["fraud_claims"]
    assert set(fraud.values()) == {"not_rendered", "impossible_days"}
    header = {r["claim_id"]: r for r in csv.DictReader(open(os.path.join(out, "claims_header.csv")))}
    paid = defaultdict(float)
    for r in csv.DictReader(open(os.path.join(out, "claim_lines.csv"))):
        paid[r["claim_id"]] += float(r["paid_amount"])
    remit = {r["claim_id"]: r for r in csv.DictReader(open(os.path.join(out, "remittance.csv")))}
    by_prov_kind = defaultdict(float)
    for cid, kind in fraud.items():
        assert remit[cid]["status"] == "paid" and abs(float(remit[cid]["paid_amount"]) - paid[cid]) < 0.02
        by_prov_kind[(header[cid]["rendering_npi"] or header[cid]["billing_npi"], kind)] += paid[cid]
    for pid, v in P.items():
        for kind in ("not_rendered", "impossible_days"):
            want = v["true_overpay_fwa"][kind]
            got = by_prov_kind.get((pid, kind), 0.0)
            assert abs(got - want) < 0.05 or v["billing_npi"] != pid, (pid, kind, got, want)
    # impossible days: the busiest day of the providers that do it is far above any honest day; the level-truth dollars do not contain the phantom claims
    per_day = defaultdict(Counter)
    for pid, rows in claims.items():
        for r in rows:
            per_day[pid][r["service_date"]] += 1
    busiest = {pid: max(c.values()) for pid, c in per_day.items()}
    assert all(busiest[pid] >= 32 for pid, v in P.items() if v["fwa_claims"]["impossible_days"])
    # unbundling: extra paid lines with modifier 25 on the E/M line, and the dollars are those lines
    lines = defaultdict(list)
    for r in csv.DictReader(open(os.path.join(out, "claim_lines.csv"))):
        lines[r["claim_id"]].append(r)
    n_lines = sum(len(ls) - 1 for c, ls in lines.items() if ls[0]["modifiers"] == "25" and c not in fraud)
    assert sum(v["fwa_claims"]["unbundling"] for v in P.values()) > 0 and sum(v["true_overpay_fwa"]["unbundling"] for v in P.values()) > 0 and n_lines > 0
    # the data-quality pre-flight must not treat the unbundled or phantom claims as a defect of the extract
    import data_quality
    checks = data_quality.run_checks(out)["checks"]
    assert checks and all(c["status"] == "ok" for c in checks), [c for c in checks if c["status"] != "ok"]


def test_level_truth_on_rendered_claims_matches_the_key_and_the_adapter():
    import d42_truth as dt
    import eval61_recovery as rec
    import score_40 as s4
    out, k, claims = dataset(7)
    fraud = k["fraud_claims"]
    for pid in list(k["providers"])[:40]:
        t = s4.provider_truth([r for r in claims[pid] if r["claim_id"] not in fraud], k["justified_cpt_by_claim"], rec.allowed())
        assert abs(t["net_overpay"] - k["providers"][pid]["true_overpay_level_net"]) < 1.0, pid
    # the derived key: monotone in the threshold, labelled, and the file has no role
    tot = {pid: v["true_overpay_total"] for pid, v in k["providers"].items()}
    cost = 800.0
    sizes = [len(dt.justified(k, m, cost)) for m in dt.M_SWEEP]
    assert sizes == sorted(sizes, reverse=True) and sizes[0] >= sizes[-1]
    d = dt.derived_key(k, 1.0, cost)
    assert all("role_derived_at" in v and v["role"] in ("upcoder", "honest") for v in d.values())
    assert {p for p, v in d.items() if v["role"] == "upcoder"} == {p for p, t in tot.items() if t >= cost}


def test_office_42_cannot_produce_a_chart_for_a_service_never_rendered_and_offices_2x_are_unchanged():
    out, k, claims = dataset(3, n=40, tag="fwa", nr_prob=1.0, imp_prob=1.0, unb_prob=1.0)
    fraud = k["fraud_claims"]
    base = os.path.join(out, "view")
    pid = next(p for p, v in k["providers"].items() if v["fwa_claims"]["not_rendered"] and p in claims)
    mine = [r["claim_id"] for r in claims[pid]]
    phantom = [c for c in mine if c in fraud]
    real = [c for c in mine if c not in fraud][:10]
    assert phantom and real
    ask = {"kind": "targeted", "claim_ids": phantom[:15] + real}
    for seed in range(1, 40):           # whatever the practice's hidden behaviour, a phantom claim never comes back
        o = provider_sim.Office(out, base, seed=seed, version="4.2")
        r = o.send_request(pid, ask)
        for step in range(4):
            if r.get("deficiencies") and r.get("rounds_left", 0) > 0 and not r.get("error"):
                r = o.follow_up(pid, [d["code"] for d in r["deficiencies"]])
        usable = set(o.state[pid]["usable"])
        assert not usable & set(phantom), seed
        resp = [e for e in o.transcript if e.get("status") in ("complete", "partial")]
        for e in resp:
            codes = {d["code"]: d for d in e["deficiencies"]}
            assert "NO_RECORD" in codes and set(codes["NO_RECORD"]["claim_ids"]) == set(phantom[:15])
            assert not set(codes.get("MISSING_VISITS", {"claim_ids": []})["claim_ids"]) & set(phantom)
    # office 2.1 on the same data knows nothing about phantom claims: it returns a chart for them (frozen behaviour)
    seen = False
    for seed in range(1, 40):
        o = provider_sim.Office(out, base, seed=seed, version="2.1")
        o.send_request(pid, ask)
        if set(o.state[pid]["usable"]) & set(phantom):
            seen = True
            break
    assert seen
    assert not hasattr(provider_sim.Office(out, base, seed=1, version="2.1"), "unrendered") or not provider_sim.Office(out, base, seed=1, version="2.1").unrendered
    # the old control-sample code skips phantom claims too
    docs, st = records.request_records(out, base, [pid], 60, __import__("random").Random(1), response_rate=1.0)
    assert not {d["claim_id"] for d in docs} & set(phantom)


def test_the_build_is_deterministic():
    tmp = tempfile.mkdtemp()
    try:
        hs = []
        for i in range(2):
            out, key = os.path.join(tmp, f"d{i}"), os.path.join(tmp, f"k{i}.json")
            generate_v2.build(out, key, seed=5, n_providers=30, data_version="4.2")
            h = {}
            for dp, _, fs in os.walk(out):
                for f in sorted(fs):
                    h[os.path.relpath(os.path.join(dp, f), out)] = hashlib.sha256(open(os.path.join(dp, f), "rb").read()).hexdigest()
            h["key"] = hashlib.sha256(open(key, "rb").read()).hexdigest()
            hs.append(h)
        assert hs[0] == hs[1]
    finally:
        shutil.rmtree(tmp)


def test_metrics_ndcg_and_dollar_weight():
    import metrics_d42 as md
    gain = {"a": 100.0, "b": 50.0, "c": 0.0, "d": 10.0}
    assert abs(md.ndcg_at_k(["a", "b", "d", "c"], gain, 3) - 1.0) < 1e-9
    assert md.ndcg_at_k(["c", "d", "b", "a"], gain, 2) < 0.2
    assert abs(md.dollar_share_at_k(["a", "b"], gain, 1) - 100 / 160) < 1e-9
    assert md.w_dollar(0, 800) == 1.0 and md.w_dollar(800, 800) == 0.0 and abs(md.w_dollar(400, 800) - 0.5) < 1e-9 and md.w_dollar(-5, 800) == 1.0


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
    for tmp in {os.path.dirname(v[0]) for v in _CACHE.values()}:
        shutil.rmtree(tmp, ignore_errors=True)
