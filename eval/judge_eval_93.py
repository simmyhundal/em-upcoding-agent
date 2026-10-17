"""Issue 93: evaluate the rule judge j3.2 and a deterministic summary writer on the stored release 1 runs (#61), for free, and write
docs/rule_judge_32.md.

No model is called. Four parts:
  1. j3.2 against j2.3 on every stored #61 summary (workflow v2.0 and v2.1, agent v3.0 and v3.1): scores, the checklist, evidence tiers, citation
     facts checked, and agreement with the stored LLM judge scores (the only other judge there is until the human spot check is done).
  2. Mutation tests: good stored summaries (j3.2 score 5) with one known defect injected; the share each judge catches and the mean score drop.
  3. Writer ablation: every model-written workflow summary replaced by the deterministic fallback (rule leaning, else inconclusive; text by code),
     and every agent finding re-assembled in code from its structured leaning; outcomes and judge scores against the stored ones.
  4. The human spot-check sheet (docs/human_spot_check.csv), written once; eval/spot_check_93.py scores it when filled in.

Usage:
    python eval/judge_eval_93.py
"""
import csv
import json
import os
import random
import re
import shutil
import statistics
import sys
import tempfile
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import case_summary as cs  # noqa: E402
import guardrail  # noqa: E402
import judge_rules as j23  # noqa: E402
import judge_rules_32 as j32  # noqa: E402
import judge_usefulness as ju  # noqa: E402
import summary_rules as sr  # noqa: E402

SCRATCH = tempfile.mkdtemp(prefix="judge93_")
ARMS = {("v2", "v2.0"): "W2.0", ("v2", "v2.1"): "W2.1", ("agent", "v3.0"): "A3.0", ("agent", "v3.1"): "A3.1"}


def jl(path):
    return [json.loads(x) for x in open(path) if x.strip()]


def runs():
    reg = json.load(open(os.path.join(ROOT, "experiments", "runs.json")))
    out = []
    for r in reg["runs"]:
        arm = ARMS.get((r["kind"], r.get("version")))
        if r["dataset"].startswith("e") and arm:
            ds = reg["datasets"][r["dataset"]]
            code = ds["flagged"].split("/")[1]
            out.append({"rid": r["run"], "arm": arm, "key": r["dataset"], "code": code, "truth": os.path.join(ROOT, ds["truth"]),
                        "view": os.path.join(ROOT, "data", f"synthetic_v2_{code}", f"view_{r['run']}"),
                        "flagged": os.path.join(ROOT, "experiments", code, "flagged.csv"), "dir": os.path.join(ROOT, "experiments", r["run"])})
    return out


def packets_j23(view, flagged):
    """The packet exactly as j2.3 builds it (no note package), so j2.3 scores reproduce."""
    chronic, age, conditions, claims = cs.load(view)
    rates = cs.peer_rates(claims, chronic)
    docs = cs.load_docs(view)
    peer_doc = cs.doc_peer_rates(claims, docs, cs.control_providers(view)) if docs else None
    facts = cs.load_doc_facts(view)
    flags = {r["provider_id"]: r for r in csv.DictReader(open(flagged))}
    return lambda pid: cs.build_packet(pid, flags[pid], chronic, age, conditions, claims, rates, docs or None, peer_doc, facts)


class Run:
    """Everything needed to judge one stored run's summaries."""
    def __init__(self, r):
        self.r = r
        self.p32 = j32.packets(r["view"], r["flagged"])
        self.p23 = packets_j23(r["view"], r["flagged"])
        self.facts = j32.load_claim_facts(r["view"])
        self.evidence = {}
        self.roles = {p: v["role"] for p, v in json.load(open(r["truth"]))["providers"].items()}

    def ev(self, pid):
        if pid not in self.evidence:
            self.evidence[pid] = ju.tool_evidence(self.r["dir"], pid)
        return self.evidence[pid]

    def score32(self, rec):
        return j32.score_summary(rec, self.p32(rec["provider_id"]), self.ev(rec["provider_id"]), self.facts)

    def score23(self, rec):
        return j23.score_summary(rec, self.p23(rec["provider_id"]), self.ev(rec["provider_id"]))


def checked(view, recs):
    """Run the citation guardrail on summary records (as the pipeline does) and return the checked records."""
    a, b = os.path.join(SCRATCH, "s.jsonl"), os.path.join(SCRATCH, "c.jsonl")
    with open(a, "w") as f:
        f.writelines(json.dumps(x) + "\n" for x in recs)
    guardrail.run(view, a, b)
    return jl(b)


def spearman(x, y):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        rk = [0.0] * len(v)
        i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                rk[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return rk
    a, b = rank(x), rank(y)
    ma, mb = statistics.mean(a), statistics.mean(b)
    num = sum((p - ma) * (q - mb) for p, q in zip(a, b))
    den = (sum((p - ma) ** 2 for p in a) * sum((q - mb) ** 2 for q in b)) ** 0.5
    return num / den if den else float("nan")


# ---- mutations ----------------------------------------------------------------------------------------------------

def _sentences(text):
    return re.split(r"(?<=[.!?])\s+", text)


def mutate(kind, rec, packet):
    """Return a mutated copy of the record, or None when the mutation does not apply. Each injects one known defect."""
    m = json.loads(json.dumps(rec))
    sm = m["summary"]
    share = f"{packet['share_99215'] * 100:.1f}%"
    tier = j32.evidence_tier(packet)
    d = packet.get("documentation_review") or {}
    if kind == "swap a number":
        if share not in sm["rationale"]:
            return None
        sm["rationale"] = sm["rationale"].replace(share, f"{packet['share_99215'] * 100 + 7.3:.1f}%", 1)
    elif kind == "flip the leaning to upcoding on weak evidence":
        if sm["leaning"] == sr.UPCODING or tier in ("charts_show_upcoding", "notes_look_inflated"):
            return None
        sm["leaning"] = sr.UPCODING
    elif kind == "flip an upcoding leaning to high acuity":
        if sm["leaning"] != sr.UPCODING:
            return None
        sm["leaning"] = sr.HIGH_ACUITY
    elif kind == "delete the chart evidence":
        if not d.get("claims_with_documentation"):
            return None
        keep = [s for s in _sentences(sm["rationale"]) if not re.search(r"Records came back|documented 99215 claims|No documented 99215", s)]
        if len(keep) == len(_sentences(sm["rationale"])):
            return None
        sm["rationale"] = " ".join(keep)
    elif kind == "delete the expected share":
        new = re.sub(r" against an expected [\d.]+% given patient complexity", "", sm["rationale"], count=1)
        if new == sm["rationale"]:
            return None
        sm["rationale"] = new
    elif kind == "repeat a sentence":
        s = next((x for x in _sentences(sm["rationale"]) if len(x) > 40), None)
        if not s:
            return None
        sm["rationale"] = sm["rationale"] + " " + s
    elif kind == "generic next steps":
        sm["next_steps"] = ["Review the provider's records.", "Consider further action if warranted."]
    elif kind == "wrong fact about a cited claim":
        new = re.sub(r"\baged (\d+)\b", lambda g: f"aged {int(g.group(1)) + 11}", sm["rationale"], count=1)
        if new == sm["rationale"]:
            return None
        sm["rationale"] = new
    elif kind == "accusatory word":
        sm["rationale"] += " This proves fraud."
    elif kind == "dollars without an estimate":
        sm["rationale"] += " The extrapolated overpayment is $12,400."
    elif kind == "understate a strong signal":
        if sm["leaning"] == sr.UPCODING or j32.ratio(packet) < 3:
            return None
        sm["rationale"] += " The signal is modest."
    elif kind == "certainty on weak evidence":
        if tier == "charts_show_upcoding":
            return None
        sm["rationale"] += " The records clearly confirm the pattern."
    return m


MUTATIONS = ["swap a number", "flip the leaning to upcoding on weak evidence", "flip an upcoding leaning to high acuity", "delete the chart evidence",
             "delete the expected share", "repeat a sentence", "generic next steps", "wrong fact about a cited claim", "accusatory word",
             "dollars without an estimate", "understate a strong signal", "certainty on weak evidence"]


def caught32(base, mut):
    return mut["score"] <= base["score"] - 1 or any(base["checklist"][k] and mut["checklist"][k] is False for k in j32.CHECKLIST)


def main():
    R = runs()
    L = ["# Rule judge j3.2 and a deterministic writer, tested on the stored release 1 runs (issue 93)", "", "[Back to the README](../README.md)", "",
         "Generated by `python eval/judge_eval_93.py`. Free: no model is called. The judge itself is `eval/judge_rules_32.py` (its table of checks "
         "is in the file's docstring); j2.3 (`eval/judge_rules.py`) is unchanged and still reproduces its stored scores. The #61 datasets are "
         "development data now: these results can shape the judge, and the human spot check is still needed to say whether either judge measures "
         "what a reviewer needs.", ""]
    S = []

    # 1. j3.2 against j2.3 and the LLM judge
    per = defaultdict(list)
    repro = Counter()
    by_source = defaultdict(lambda: defaultdict(list))
    cl_pass = defaultdict(Counter)
    cl_n = defaultdict(Counter)
    tiers = defaultdict(Counter)
    ded = defaultdict(Counter)
    cit_checked = cit_bad = 0
    pairs = defaultdict(list)
    note_fix = [0, 0]
    stored_by_run, cache = {}, {}
    for r in R:
        J = Run(r)
        cache[r["rid"]] = J
        recs = jl(os.path.join(r["dir"], "case_summaries_checked.jsonl"))
        stored_by_run[r["rid"]] = recs
        old = {x["provider_id"]: x for x in jl(os.path.join(r["dir"], "usefulness_rules.jsonl"))}
        llm = {x["provider_id"]: x["score"] for x in jl(os.path.join(r["dir"], "usefulness.jsonl"))} if os.path.exists(os.path.join(r["dir"], "usefulness.jsonl")) else {}
        for rec in recs:
            pid = rec["provider_id"]
            a23 = J.score23(rec)
            repro[(a23["score"] == old[pid]["score"])] += 1
            a = J.score32(rec)
            src = "model-written" if rec.get("source", "agent") in ("llm", "llm+repair", "agent") else "rule-written"
            per[r["arm"]].append((a23["score"], a["score"]))
            by_source[r["arm"]][src].append(a["score"])
            tiers[r["arm"]][a["evidence_tier"]] += 1
            for k in a["deductions"]:
                ded[r["arm"]][k] += 1
            for k in j32.CHECKLIST:
                if a["checklist"][k] is not None:
                    cl_n[r["arm"]][k] += 1
                    cl_pass[r["arm"]][k] += bool(a["checklist"][k])
            cit_checked += a["citation_facts_checked"]
            cit_bad += sum(1 for p in a["problems"] if ": text says " in p)
            if pid in llm:
                pairs["j2.3"].append((a23["score"], llm[pid]))
                pairs["j3.2"].append((a["score"], llm[pid]))
            if a23.get("unverified_numbers"):
                note_fix[0] += 1
                note_fix[1] += not a["unverified_numbers"]
    total = sum(repro.values())
    L += ["## 1. j3.2 on every stored #61 summary", "",
          f"j2.3 recomputed here matches its stored score on {repro[True]} of {total} summaries (the frozen judge is unchanged).", "",
          "| Arm | Summaries | j2.3 mean | j3.2 mean | j3.2 mean, model-written | j3.2 mean, rule-written | Evidence tiers |", "|---|---|---|---|---|---|---|"]
    for arm in ("W2.0", "W2.1", "A3.0", "A3.1"):
        xs = per[arm]
        bs = by_source[arm]
        L.append(f"| {arm} | {len(xs)} | {statistics.mean(a for a, _ in xs):.2f} | {statistics.mean(b for _, b in xs):.2f} | "
                 + (f"{statistics.mean(bs['model-written']):.2f}" if bs["model-written"] else "–") + " | "
                 + (f"{statistics.mean(bs['rule-written']):.2f}" if bs["rule-written"] else "–") + " | "
                 + ", ".join(f"{k.replace('_', ' ')} {v}" for k, v in tiers[arm].most_common()) + " |")
    L += ["", "Checklist pass rates (share of the summaries where the item applies):", "",
          "| Item | " + " | ".join(("W2.0", "W2.1", "A3.0", "A3.1")) + " |", "|---|---|---|---|---|"]
    for k in j32.CHECKLIST:
        L.append(f"| {k.replace('_', ' ')} | " + " | ".join(f"{cl_pass[a][k] / cl_n[a][k]:.0%}" if cl_n[a][k] else "n/a" for a in ("W2.0", "W2.1", "A3.0", "A3.1")) + " |")
    L += ["", "Most frequent j3.2 deductions: " + "; ".join(f"{a}: " + ", ".join(f"{k} {v}" for k, v in ded[a].most_common(4)) for a in ("W2.0", "W2.1", "A3.0", "A3.1")) + ".",
          "", f"Citation support: {cit_checked:,} stated facts about cited claims were checked; {cit_bad} did not match the claim, patient or chart rows.",
          f"The note-package fix: {note_fix[0]} summaries had numbers j2.3 could not match; for {note_fix[1]} of them j3.2 matches every number (mostly the note-check percentages)."]
    corr = {k: spearman([a for a, _ in v], [b for _, b in v]) for k, v in pairs.items()}
    L += ["", f"Agreement with the stored LLM judge scores (Spearman, {len(pairs['j3.2'])} summaries): j2.3 {corr['j2.3']:.2f}, j3.2 {corr['j3.2']:.2f}. "
          "Neither judge has been checked against a person, so this says only how far the two kinds of judge agree, not which is right."]
    xs = [b for a in per.values() for _, b in a]
    S.append(f"j3.2 scores the {len(xs)} stored #61 summaries at {statistics.mean(xs):.2f} on average (j2.3: {statistics.mean(a for v in per.values() for a, _ in v):.2f}); "
             f"its checklist shows what the score hides, for example the size of the excess is stated in "
             f"{sum(cl_pass[a]['excess_stated'] for a in cl_pass) / max(1, sum(cl_n[a]['excess_stated'] for a in cl_n)):.0%} of summaries. "
             f"Agreement with the LLM judge: {corr['j3.2']:.2f} (j2.3 {corr['j2.3']:.2f}).")

    # 2. mutations
    rng = random.Random(93)
    base = []
    for r in R:
        J = cache[r["rid"]]
        for rec in stored_by_run[r["rid"]]:
            if rec["citation_check"]["passed"]:
                s = J.score32(rec)
                if s["score"] == 5:
                    base.append((r["rid"], rec, s))
    rng.shuffle(base)
    base = base[:300]
    res = defaultdict(lambda: {"n": 0, "c23": 0, "c32": 0, "d23": [], "d32": []})
    for rid, rec, s32 in base:
        J = cache[rid]
        pk = J.p32(rec["provider_id"])
        s23 = J.score23(rec)
        for kind in MUTATIONS:
            m = mutate(kind, rec, pk)
            if m is None:
                continue
            m32, m23 = J.score32(m), J.score23(m)
            x = res[kind]
            x["n"] += 1
            x["c32"] += caught32(s32, m32)
            x["c23"] += m23["score"] <= s23["score"] - 1
            x["d32"].append(s32["score"] - m32["score"])
            x["d23"].append(s23["score"] - m23["score"])
    L += ["", "## 2. Mutation tests", "",
          f"{len(base)} stored summaries that j3.2 scores 5 (sampled across the four arms), each given one known defect. Caught means the score drops by "
          "at least 1 or, for j3.2, a checklist item that passed now fails; j2.3 has no checklist.", "",
          "| Defect injected | Summaries | j2.3 caught | j3.2 caught | Mean score drop j2.3 / j3.2 |", "|---|---|---|---|---|"]
    tot = [0, 0, 0]
    for kind in MUTATIONS:
        x = res[kind]
        if not x["n"]:
            L.append(f"| {kind} | 0 | – | – | – |")
            continue
        tot = [tot[0] + x["n"], tot[1] + x["c23"], tot[2] + x["c32"]]
        L.append(f"| {kind} | {x['n']} | {x['c23'] / x['n']:.0%} | {x['c32'] / x['n']:.0%} | {statistics.mean(x['d23']):.2f} / {statistics.mean(x['d32']):.2f} |")
    L += ["", "Two things the table shows about the score itself. A single unmatched number costs 0.5, which rounds away (as in j2.3), so j3.2 catches a "
          "swapped share mostly through the checklist (observed and expected share no longer match the evidence). And deleting the chart sentences is "
          "rarely caught because the same counts are usually stated again elsewhere (the note-check sentence gives the number of returned notes), "
          "which is partly a real limit of the check.",
          "", f"Overall: j2.3 caught {tot[1] / tot[0]:.0%} and j3.2 {tot[2] / tot[0]:.0%} of {tot[0]} mutated summaries. "
          "The data-caveat mutation is not in this table: no release 1 summary carries a caveat (the pre-flight is new in release 2); a unit test covers it "
          "(`tests/test_judge_rules_32.py`). A judge that catches a planted defect can still miss real ones; the human check is the test of that."]
    S.append(f"Mutation tests: j3.2 catches {tot[2] / tot[0]:.0%} of {tot[0]} injected defects, j2.3 {tot[1] / tot[0]:.0%}.")

    # 3. writer ablation
    L += ["", "## 3. Should the writer be deterministic? Ablation on the stored runs", ""]
    rows3 = []
    for arm in ("W2.0", "W2.1"):
        st = {"stored": [0, 0, 0], "det": [0, 0, 0], "s_stored": [], "s_det": [], "cl_stored": Counter(), "cl_det": Counter(), "n": 0, "changed": 0, "lost": 0, "spared": 0}
        for r in R:
            if r["arm"] != arm:
                continue
            J = cache[r["rid"]]
            recs = stored_by_run[r["rid"]]
            writer_pk = {}
            dry = cs.run(r["view"], os.path.join(r["dir"], "flagged_threshold.csv"), os.path.join(SCRATCH, "dry.jsonl"), dry_run=True,
                         version="2.1" if arm == "W2.1" else "2.0", log=lambda *a: None)
            for x in dry:
                writer_pk[x["provider_id"]] = x["packet"]
            det = []
            for rec in recs:
                if rec["source"] == "rules":
                    det.append({k: rec[k] for k in ("provider_id", "model", "summary", "source", "rule_leaning", "rule_reason")} | {"citations_checked": False})
                else:
                    pk = writer_pk[rec["provider_id"]]
                    lean = sr.rule_leaning(pk)[0] or sr.INCONCLUSIVE
                    det.append({"provider_id": rec["provider_id"], "model": "rules", "summary": sr.assemble(pk, lean, version="2.1" if arm == "W2.1" else "2.0"),
                                "citations_checked": False, "source": "rules (ablation)", "rule_leaning": lean, "rule_reason": rec["rule_reason"]})
            det = checked(r["view"], det)
            for a, b in zip(recs, det):
                role = J.roles[a["provider_id"]]
                for which, rec in (("stored", a), ("det", b)):
                    if rec["summary"]["leaning"] == sr.UPCODING:
                        st[which][0 if role == "upcoder" else 1] += 1
                    s = J.score32(rec)
                    st["s_" + which].append(s["score"])
                    for k in j32.CHECKLIST:
                        st["cl_" + which][k] += bool(s["checklist"][k])
                st["n"] += 1
                if a["summary"]["leaning"] != b["summary"]["leaning"]:
                    st["changed"] += 1
                    st["lost"] += a["summary"]["leaning"] == sr.UPCODING and role == "upcoder"
                    st["spared"] += a["summary"]["leaning"] == sr.UPCODING and role != "upcoder"
        rows3.append((arm, st))
    L += ["Workflow: every model-written summary replaced by what code alone writes (the evidence rule's leaning, else inconclusive; facts, examples "
          "and next steps by code), on the same charts.", "",
          "| Arm | Summaries | Leanings changed | Upcoders called (stored / deterministic) | Honest doctors called (stored / deterministic) | j3.2 mean (stored / deterministic) | Excess stated (stored / deterministic) |",
          "|---|---|---|---|---|---|---|"]
    for arm, st in rows3:
        L.append(f"| {arm} | {st['n']} | {st['changed']} | {st['stored'][0]} / {st['det'][0]} | {st['stored'][1]} / {st['det'][1]} | "
                 f"{statistics.mean(st['s_stored']):.2f} / {statistics.mean(st['s_det']):.2f} | {st['cl_stored']['excess_stated'] / st['n']:.0%} / {st['cl_det']['excess_stated'] / st['n']:.0%} |")
    w21 = dict(rows3)["W2.1"]
    w20 = dict(rows3)["W2.0"]
    L += ["", f"For workflow v2.1, a deterministic writer would have called {w21['det'][0]} upcoders instead of {w21['stored'][0]} and {w21['det'][1]} honest "
          f"doctors instead of {w21['stored'][1]}. For the older v2.0 prompt it would have dropped {w20['lost']} true upcoding calls and "
          f"{w20['spared']} false ones. The judge scores are not a fair contest: the deterministic text is built by the same rules that j2.3 uses, "
          "and partly by the evidence logic j3.2 checks, so it is expected to score well."]
    st = {"free": [], "struct": [], "cl_free": Counter(), "cl_struct": Counter(), "n": 0}
    for r in R:
        if r["arm"] != "A3.1":
            continue
        J = cache[r["rid"]]
        recs = stored_by_run[r["rid"]]
        struct = checked(r["view"], [{"provider_id": x["provider_id"], "model": "rules", "source": "structured (ablation)", "citations_checked": False,
                                      "summary": sr.assemble(J.p32(x["provider_id"]), x["summary"]["leaning"], version="2.1")} for x in recs])
        for a, b in zip(recs, struct):
            for which, rec in (("free", a), ("struct", b)):
                s = J.score32(rec)
                st[which].append(s["score"])
                for k in j32.CHECKLIST:
                    st["cl_" + which][k] += bool(s["checklist"][k])
            st["n"] += 1
    L += ["", f"Agent v3.1: each finding's leaning kept, its text assembled in code instead of from the agent's headline and interpretation "
          f"(the structured findings #60 proposes). Outcomes are identical by construction (same leanings). On {st['n']} findings: j3.2 mean "
          f"{statistics.mean(st['free']):.2f} free text against {statistics.mean(st['struct']):.2f} assembled; checklist passes "
          + ", ".join(f"{k.replace('_', ' ')} {st['cl_free'][k] / st['n']:.0%} / {st['cl_struct'][k] / st['n']:.0%}" for k in ("leaning_explained", "excess_stated", "chart_state", "next_step_fits_leaning"))
          + " (free / assembled)."]
    S.append(f"Writer ablation: for workflow v2.1 a deterministic writer calls {w21['det'][0]} upcoders and {w21['det'][1]} honest doctors against "
             f"{w21['stored'][0]} and {w21['stored'][1]} as stored; the judge cannot settle the choice, because code-written text is partly graded by its own rules.")

    # 4. spot-check sheet
    sheet = os.path.join(ROOT, "docs", "human_spot_check.csv")
    if not os.path.exists(sheet):
        pool = {"W2.1 model": [], "W2.1 rules": [], "A3.1": []}
        for r in R:
            for rec in stored_by_run[r["rid"]]:
                k = "A3.1" if r["arm"] == "A3.1" else ("W2.1 model" if r["arm"] == "W2.1" and rec["source"] != "rules" else "W2.1 rules" if r["arm"] == "W2.1" else None)
                if k:
                    pool[k].append((r, rec))
        pick = []
        for k, n in (("W2.1 model", 9), ("W2.1 rules", 8), ("A3.1", 8)):
            items = sorted(pool[k], key=lambda t: (t[0]["rid"], t[1]["provider_id"]))
            pick += random.Random(f"spot-93-{k}").sample(items, n)
        random.Random("spot-93-order").shuffle(pick)
        with open(sheet, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["item", "run_id", "provider_id", "evidence", "headline", "leaning", "rationale", "next_steps",
                        "your_score_1_to_5", "leaning_explained", "observed_vs_expected", "excess_stated", "chart_state", "next_step_fits_leaning", "notes"])
            for i, (r, rec) in enumerate(pick, 1):
                pk = cache[r["rid"]].p32(rec["provider_id"])
                d = pk.get("documentation_review") or {}
                r215 = j32._rows(pk, ("99215",))
                evidence = (f"{pk['n_claims']} claims; billed 99215 on {pk['share_99215']:.1%} against an expected {pk['expected_share_given_patient_complexity']:.1%} "
                            f"({j32.ratio(pk):.1f} times); {d.get('claims_with_documentation', 0)} charts returned"
                            + (f"; {r215[0]['documentation_does_not_support_billed_level']} of {r215[0]['documented_claims']} documented 99215 below the billed level" if r215 else ""))
                sm = rec["summary"]
                w.writerow([i, r["rid"], rec["provider_id"], evidence, sm["headline"], sm["leaning"], sm["rationale"], " | ".join(sm["next_steps"]),
                            "", "", "", "", "", "", ""])
    L += ["", "## 4. Human spot check", "", f"Not done yet. The sheet `docs/human_spot_check.csv` holds 25 stored summaries (9 model-written and 8 rule-written "
              "from workflow v2.1, 8 from agent v3.1) with the evidence a reviewer needs; instructions in [human_spot_check.md](human_spot_check.md). "
              "`python eval/spot_check_93.py` reports agreement with j3.2 and the LLM judge once it is filled in."]
    L += ["", "## 5. What the release 2 evaluation uses", "",
          "- **Judge:** j3.2 only (Simmy's decision); report its checklist items beside the score, since the score alone hides what a summary leaves out "
          "(for example the size of the excess).",
          f"- **Workflow writer:** not fully deterministic. On the stored v2.1 runs it would have lost {w21['stored'][0] - w21['det'][0]} of {w21['stored'][0]} "
          "upcoder calls, the one where the model read notes that claim data review the claims do not show. Rules 2.2 (#91) already decide the other "
          "ambiguous cases by rule with no leaning changed, so W2.2 keeps the model for that one case.",
          "- **Agent writer:** free-text findings as in v3.1. Assembling the text in code keeps the leanings (outcomes unchanged by construction) and "
          "scores higher on j3.2, but j3.2 shares logic with that code, the assembled text states the size of the excess less often, and telling the "
          "model its text is discarded may change what it does, which only a paid run can show. Left for #60 after the human check."]
    S.append("Human spot check: the 25-summary sheet is ready; agreement can be measured only after Simmy fills it in.")

    L[6:6] = ["## Summary", ""] + [f"- {x}" for x in S] + [""]
    out = os.path.join(ROOT, "docs", "rule_judge_32.md")
    open(out, "w").write("\n".join(L) + "\n")
    print("\n".join(L))
    shutil.rmtree(SCRATCH, ignore_errors=True)


if __name__ == "__main__":
    main()
