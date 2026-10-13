"""Tools for the investigator agent (issues 39 and 49). Design notes: docs/agent_tools.md.

`Environment` is everything the agent can touch. It reads only payer-visible data: the detector view (claims, patients, providers),
documentation from earlier reviews of a control sample of providers (the peer baseline), and whatever the simulated provider
office returns when the agent asks (src/provider_sim.py). It never reads an answer key, roles, justified levels or the records
universe. Every tool returns a JSON-serializable dict and is recorded in `environment.audit` by the agent loop.

Tools: screen_providers (parameterized, deterministic, free), list_providers (the no-screen ablation), provider_profile,
peer_comparison, request_records / follow_up_records / close_records (the office), hybrid_review (chart rule first, model only
where the rules say nothing), draft_summary (summary plus citation check), estimate_overpayment (random samples only), and
submit_findings (the agent's final list; drafts for human review).
"""
import csv
import json
import os
import statistics
from collections import Counter, defaultdict

import case_summary as cs
import flagging
import guardrail
import pi_estimate as pe
import provider_sim
import records
import summary_rules as sr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED = os.path.join(ROOT, "data", "baselines", "allowed_amounts_ga_fp.json")
CODES = records.CODES
CHART_RULE_RATE, CHART_RULE_MIN = 0.15, 8
SCREEN_ROWS_SHOWN = 30
CUTOFFS = [3, 4, 5, 6, 8, 10]


def _doc_entry(row):
    mins = row["documented_minutes"]
    lvl = max(records.MDM_LEVELS.index(row["documented_mdm_level"]), records.level_from_minutes(mins))
    return lvl, (int(mins) if mins not in ("", None) else None)


class Environment:
    def __init__(self, v2_dir, view_dir, seed=1, model_call=None, records_budget=15, screen_enabled=True,
                 correlation=0.0, roles=None):
        """model_call(system, user) -> (json_text, usd) is used only inside hybrid_review and draft_summary; None = never call a model."""
        self.view_dir, self.model_call, self.records_budget, self.screen_enabled = view_dir, model_call, records_budget, screen_enabled
        self.chronic, self.age, self.conditions, self.claims = cs.load(view_dir)
        self.rates = cs.peer_rates(self.claims, self.chronic)
        self.owner = guardrail.load_claim_owners(view_dir)
        self.rows = {r["provider_id"]: r for r in flagging.flag(view_dir, top_n=25)}
        self.has_test = {}
        for rows in self.claims.values():
            for r in rows:
                self.has_test[r["claim_id"]] = r.get("has_test_line") == "1"
        # prior reviews of a control sample: the peer baseline for documentation rates (read from the view's earlier request)
        self.control, self.docs, self.facts = set(), {}, {}
        req = os.path.join(view_dir, "records_requests.csv")
        doc = os.path.join(view_dir, "documentation.csv")
        if os.path.exists(req) and os.path.exists(doc):
            self.control = {r["provider_id"] for r in csv.DictReader(open(req)) if r["kind"] == "control"}
            for r in csv.DictReader(open(doc)):
                if self.owner.get(r["claim_id"]) in self.control:
                    self.docs[r["claim_id"]] = _doc_entry(r)
                    self.facts[r["claim_id"]] = int(r["documented_data_level"])
        self.office = provider_sim.Office(v2_dir, view_dir, seed=seed, correlation=correlation, roles=roles)
        self.requested = set()
        self.spent_usd = 0.0
        self.findings = {}
        self.summaries = {}

    # ---- helpers ---------------------------------------------------------
    def _peer_doc(self):
        return cs.doc_peer_rates(self.claims, self.docs, self.control) if self.docs else None

    def _packet(self, pid):
        return cs.build_packet(pid, self.rows[pid], self.chronic, self.age, self.conditions, self.claims, self.rates,
                               self.docs or None, self._peer_doc(), self.facts)

    def _absorb(self, pid):
        for row in self.office.documentation_rows():
            self.docs[row["claim_id"]] = _doc_entry(row)
            self.facts[row["claim_id"]] = int(row["documented_data_level"])

    def _chart_rule(self, pid):
        rows = self.claims.get(pid, [])
        got = [r for r in rows if r["claim_id"] in self.docs]
        below = sum(self.docs[r["claim_id"]][0] < CODES.index(r["cpt"]) for r in got)
        no_test = sum(self.facts.get(r["claim_id"], 0) >= 3 and not self.has_test[r["claim_id"]] for r in got)
        n = len(got)
        return {"charts": n, "below_billed": below, "below_billed_rate": round(below / n, 3) if n else None,
                "triggered": n >= CHART_RULE_MIN and below / n > CHART_RULE_RATE,
                "data_without_tests": no_test, "data_without_tests_rate": round(no_test / n, 3) if n else None}

    # ---- tools -----------------------------------------------------------
    def screen_providers(self, method="riskadj", top_n=None, min_score=None, max_flagged=None, min_claims=0):
        """Rank providers by a statistical score and choose a cutoff. method: zscore | riskadj | combined."""
        key = {"zscore": ("z", True), "riskadj": ("z_adj", True), "combined": ("mean_rank", False)}.get(method)
        if not key:
            return {"error": "method must be zscore, riskadj or combined"}
        field, desc = key
        elig = [r for r in self.rows.values() if int(r["n_claims"]) >= min_claims]
        elig.sort(key=lambda r: (-float(r[field]) if desc else float(r[field]), r["provider_id"]))
        if min_score is not None and method != "combined":
            sel = [r for r in elig if float(r[field]) >= min_score]
        else:
            sel = elig[: int(top_n or 25)]
        if max_flagged:
            sel = sel[: int(max_flagged)]
        zs = sorted(float(r["z_adj"]) for r in self.rows.values())
        q = lambda p: round(zs[min(int(p * len(zs)), len(zs) - 1)], 2)
        return {"method": method, "selected": len(sel),
                "table": {"cols": ["provider", "claims", "share_99215", "expected_share", "z", "z_adj", "rank_combined"],
                          "rows": [[r["provider_id"], int(r["n_claims"]), float(r["share_99215"]), float(r["expected_share"]),
                                    float(r["z"]), float(r["z_adj"]), r["rank"]] for r in sel[:SCREEN_ROWS_SHOWN]]},
                "shown": min(len(sel), SCREEN_ROWS_SHOWN),
                "z_adj_distribution": {"providers": len(zs), "p50": q(0.5), "p90": q(0.9), "p95": q(0.95), "p99": q(0.99), "max": zs[-1]},
                "providers_at_or_above_z_adj": {str(c): sum(z >= c for z in zs) for c in CUTOFFS}}

    def list_providers(self, page=1, page_size=40):
        """Plain overview with no scores (the no-screen ablation): claims and code mix per provider, sorted by id."""
        pids = sorted(self.claims)
        chunk = pids[(page - 1) * page_size: page * page_size]
        out = []
        for p in chunk:
            mix = Counter(r["cpt"] for r in self.claims[p])
            n = len(self.claims[p])
            out.append([p, n, round(mix["99215"] / n, 3), round((mix["99214"] + mix["99215"]) / n, 3)])
        return {"table": {"cols": ["provider", "claims", "share_99215", "share_99214_or_99215"], "rows": out},
                "page": page, "pages": (len(pids) + page_size - 1) // page_size}

    def provider_profile(self, provider_id):
        if provider_id not in self.rows:
            return {"error": "unknown provider"}
        return sr.to_card(self._packet(provider_id))

    def peer_comparison(self, provider_id):
        if provider_id not in self.rows:
            return {"error": "unknown provider"}
        p = self._packet(provider_id)
        allmix = Counter(r["cpt"] for rows in self.claims.values() for r in rows)
        tot = sum(allmix.values())
        return {"provider": provider_id, "share_99215": p["share_99215"], "expected_share": p["expected_share_given_patient_complexity"],
                "z": p["z_vs_peers"], "z_adj": p["risk_adjusted_score"],
                "mix": {c: round(p["billed_mix"].get(c, 0) / p["n_claims"], 3) for c in CODES},
                "all_provider_mix": {c: round(allmix[c] / tot, 3) for c in CODES},
                "by_complexity": sr.to_card(p)["by_complexity"]}

    def request_records(self, provider_id, sample, deadline=provider_sim.DEFAULT_DEADLINE):
        if provider_id not in self.rows:
            return {"error": "unknown provider"}
        if provider_id not in self.requested and len(self.requested) >= self.records_budget:
            return {"error": f"records-request budget reached ({self.records_budget} providers)"}
        self.requested.add(provider_id)
        out = self.office.send_request(provider_id, sample, deadline)
        self._absorb(provider_id)
        return out

    def follow_up_records(self, provider_id, addressed_codes, deadline=provider_sim.DEFAULT_DEADLINE, claim_ids=None):
        out = self.office.follow_up(provider_id, addressed_codes, deadline, claim_ids)
        self._absorb(provider_id)
        return out

    def close_records(self, provider_id, reason=""):
        return self.office.close_request(provider_id, reason)

    def _model_summary(self, packet, reason):
        text, usd = self.model_call(__import__("case_summary").SYSTEM, cs.make_prompt(packet, reason))
        self.spent_usd += usd
        return json.loads(text)

    def hybrid_review(self, provider_ids):
        """Chart rule first; the summary rules next; the model only where both say nothing."""
        out = []
        for pid in provider_ids[:20]:
            if pid not in self.rows:
                out.append({"provider": pid, "error": "unknown provider"})
                continue
            chart = self._chart_rule(pid)
            packet = self._packet(pid)
            rule, reason = sr.rule_leaning(packet)
            if chart["triggered"] and rule != sr.UPCODING:
                lean, source, reason = sr.UPCODING, "chart_rule", f"{chart['below_billed']} of {chart['charts']} returned charts support a lower level than billed"
            elif rule:
                lean, source = rule, "summary_rule"
            elif self.model_call:
                m = self._model_summary(packet, reason)
                lean, source = m["leaning"], "model"
                self.summaries[pid] = sr.assemble(packet, lean, m["headline"], m["interpretation"])
            else:
                lean, source = None, "undecided"
            if lean and pid not in self.summaries:
                self.summaries[pid] = sr.assemble(packet, lean)
            out.append({"provider": pid, "leaning": lean, "source": source, "reason": reason, "chart_rule": chart})
        return {"results": out}

    def draft_summary(self, provider_id):
        """The full draft summary for one provider, with the citation check. Uses hybrid_review's decision."""
        if provider_id not in self.summaries:
            r = self.hybrid_review([provider_id])["results"][0]
            if not r.get("leaning"):
                return {"error": "no decision yet: too little evidence, or no model allowed", "review": r}
        s = self.summaries[provider_id]
        chk = guardrail.check({"provider_id": provider_id, "summary": s}, self.owner)["citation_check"]
        return {"provider": provider_id, "summary": s, "citation_check": chk, "status": "draft for human review"}

    def estimate_overpayment(self, provider_id):
        """Extrapolated overpayment from a RANDOM records sample only."""
        st = self.office.state.get(provider_id)
        if not st or not st["requested"]:
            return {"error": "no records request for this provider"}
        if st["sample_kind"] != "random":
            return {"error": "the request was targeted; only a random sample supports extrapolation", "valid_for_extrapolation": False}
        rows = self.claims[provider_id]
        by_cpt = {r["claim_id"]: r["cpt"] for r in rows}
        plan = {"provider_id": provider_id, "frame_sizes": dict(Counter(r["cpt"] for r in rows)),
                "sampled_claims": {c: by_cpt[c] for c in st["requested"]}}
        reviewed = {c: (CODES[self.docs[c][0]] if c in self.docs else "") for c in st["requested"]}
        allowed = {c: v["allowed_amount"] for c, v in json.load(open(ALLOWED))["codes"].items()}
        amounts = {r["claim_id"]: (float(r["allowed_amount"]), float(r["paid_amount"])) for r in rows if r.get("allowed_amount")}
        res = pe.estimate(plan, reviewed, allowed, 0.90, claim_amounts=amounts)
        return {"valid_for_extrapolation": True, "point_estimate": round(res["point_estimate"]), "ci_low": round(res["ci_low"]),
                "ci_high": round(res["ci_high"]), "reviewed_claims": res["reviewed_claims"], "sampled_claims": res["sampled_claims"],
                "caveat": "Draft arithmetic from a simulated review; a real recovery needs human review of the records."}

    def submit_findings(self, findings):
        """findings: [{"provider_id", "leaning", "headline", "interpretation"}]. Stored as drafts; the run ends."""
        bad = [f.get("provider_id") for f in findings if f.get("provider_id") not in self.rows or f.get("leaning") not in
               (sr.UPCODING, sr.HIGH_ACUITY, sr.INCONCLUSIVE)]
        if bad:
            return {"error": f"invalid provider or leaning for: {bad}"}
        for f in findings:
            packet = self._packet(f["provider_id"])
            self.findings[f["provider_id"]] = sr.assemble(packet, f["leaning"], f.get("headline"), f.get("interpretation"))
        return {"accepted": len(findings), "status": "drafts for human review; nothing is sent or decided automatically"}

    # ---- schemas and dispatch -------------------------------------------
    def tool_schemas(self):
        sample = {"type": "object", "description": "kind random or targeted; n; optional cpt (targeted) or claim_ids (targeted)",
                  "properties": {"kind": {"type": "string", "enum": ["random", "targeted"]}, "n": {"type": "integer"},
                                 "cpt": {"type": "string"}, "claim_ids": {"type": "array", "items": {"type": "string"}}},
                  "required": ["kind"]}
        pid = {"provider_id": {"type": "string"}}
        tools = []
        if self.screen_enabled:
            tools.append({"name": "screen_providers", "description":
                          "Rank every provider by a statistical score and pick a cutoff. method zscore|riskadj|combined; select top_n or min_score "
                          "(riskadj/zscore); optional max_flagged and min_claims. Returns a ranked table, the score distribution and how many "
                          "providers sit at or above several cutoffs. Free and deterministic; call it as often as you like.",
                          "input_schema": {"type": "object", "properties": {"method": {"type": "string", "enum": ["zscore", "riskadj", "combined"]},
                                           "top_n": {"type": "integer"}, "min_score": {"type": "number"}, "max_flagged": {"type": "integer"},
                                           "min_claims": {"type": "integer"}}}})
        else:
            tools.append({"name": "list_providers", "description": "List providers with claims counts and 99215 share, 40 per page. No scores.",
                          "input_schema": {"type": "object", "properties": {"page": {"type": "integer"}}}})
        tools += [
            {"name": "provider_profile", "description": "Evidence card for one provider: billing mix, complexity table, sample claims and any records already received.",
             "input_schema": {"type": "object", "properties": pid, "required": ["provider_id"]}},
            {"name": "peer_comparison", "description": "One provider against all providers: mix, scores and 99215 share by patient complexity.",
             "input_schema": {"type": "object", "properties": pid, "required": ["provider_id"]}},
            {"name": "request_records", "description":
             "Ask a provider's office for charts. A random sample supports an overpayment estimate; a targeted one does not. Each provider you ask is a burden on that "
             "practice and counts against a budget. The office may answer incompletely.",
             "input_schema": {"type": "object", "properties": {**pid, "sample": sample, "deadline_days": {"type": "integer"}}, "required": ["provider_id", "sample"]}},
            {"name": "follow_up_records", "description": "Tell the office what was wrong with its last response (deficiency codes from that response). Optional claim_ids narrows scope.",
             "input_schema": {"type": "object", "properties": {**pid, "addressed_codes": {"type": "array", "items": {"type": "string"}},
                              "claim_ids": {"type": "array", "items": {"type": "string"}}}, "required": ["provider_id", "addressed_codes"]}},
            {"name": "close_records", "description": "Close a records request. No response is not evidence of upcoding.",
             "input_schema": {"type": "object", "properties": {**pid, "reason": {"type": "string"}}, "required": ["provider_id"]}},
            {"name": "hybrid_review", "description": "Chart rule first, then the summary rules, and a model only where both say nothing. Up to 20 providers. Needs records already received.",
             "input_schema": {"type": "object", "properties": {"provider_ids": {"type": "array", "items": {"type": "string"}}}, "required": ["provider_ids"]}},
            {"name": "draft_summary", "description": "Draft case summary for a provider already reviewed, with the citation check.",
             "input_schema": {"type": "object", "properties": pid, "required": ["provider_id"]}},
            {"name": "estimate_overpayment", "description": "Overpayment estimate for a provider from a RANDOM records sample.",
             "input_schema": {"type": "object", "properties": pid, "required": ["provider_id"]}},
            {"name": "submit_findings", "description": "Submit your final findings and end the run. leaning is one of pattern_consistent_with_upcoding, "
             "pattern_consistent_with_high_acuity_panel, inconclusive. Include every provider you looked at closely; only 'upcoding' ones go to recovery.",
             "input_schema": {"type": "object", "properties": {"findings": {"type": "array", "items": {"type": "object", "properties": {
                 "provider_id": {"type": "string"}, "leaning": {"type": "string"}, "headline": {"type": "string"},
                 "interpretation": {"type": "string"}}, "required": ["provider_id", "leaning"]}}}, "required": ["findings"]}}]
        return tools

    def call(self, name, args):
        args = args or {}
        fn = {"screen_providers": lambda: self.screen_providers(**args) if self.screen_enabled else {"error": "tool not available"},
              "list_providers": lambda: self.list_providers(**args) if not self.screen_enabled else {"error": "tool not available"},
              "provider_profile": lambda: self.provider_profile(args["provider_id"]),
              "peer_comparison": lambda: self.peer_comparison(args["provider_id"]),
              "request_records": lambda: self.request_records(args["provider_id"], args["sample"], args.get("deadline_days", provider_sim.DEFAULT_DEADLINE)),
              "follow_up_records": lambda: self.follow_up_records(args["provider_id"], args["addressed_codes"], claim_ids=args.get("claim_ids")),
              "close_records": lambda: self.close_records(args["provider_id"], args.get("reason", "")),
              "hybrid_review": lambda: self.hybrid_review(args["provider_ids"]),
              "draft_summary": lambda: self.draft_summary(args["provider_id"]),
              "estimate_overpayment": lambda: self.estimate_overpayment(args["provider_id"]),
              "submit_findings": lambda: self.submit_findings(args["findings"])}.get(name)
        if fn is None:
            return {"error": f"unknown tool {name}"}
        try:
            return fn()
        except (KeyError, TypeError, ValueError) as e:
            return {"error": f"bad arguments: {e}"}
