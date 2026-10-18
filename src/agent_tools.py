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
import summary_lint
import summary_rules as sr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED = os.path.join(ROOT, "data", "baselines", "allowed_amounts_ga_fp.json")
CODES = records.CODES
CHART_RULE_RATE, CHART_RULE_MIN = 0.15, 8
SCREEN_ROWS_SHOWN = 30
CUTOFFS = [3, 4, 5, 6, 8, 10]
CANDIDATE_RATIO = 3.0        # version 3.1: a screened provider billing 99215 at this many times its expected share must be examined or explained
MIN_STRATUM_REVIEWED = 8     # version 3.1: an overpayment estimate needs this many reviewed charts in its main stratum to be called reliable


def _doc_entry(row):
    mins = row["documented_minutes"]
    lvl = max(records.MDM_LEVELS.index(row["documented_mdm_level"]), records.level_from_minutes(mins))
    return lvl, (int(mins) if mins not in ("", None) else None)


class Environment:
    def __init__(self, v2_dir, view_dir, seed=1, model_call=None, records_budget=15, screen_enabled=True,
                 correlation=0.0, roles=None, version="3.0"):
        """model_call(system, user) -> (json_text, usd) is used only inside hybrid_review and draft_summary; None = never call a model.
        version "3.1" adds the note package (data v2.1): charts carry notes, a second request is allowed (random first, targeted after),
        and the note_checks and request_audit_trail tools exist. "3.2" is 3.1 plus the data-quality pre-flight, the read-only data_quality tool and
        flag_data_issue (issue 81). "3.0" is the frozen agent."""
        self.v31 = version in ("3.1", "3.2", "3.3")
        self.v32 = version in ("3.2", "3.3")
        self.v33 = version == "3.3"                     # release 3 (issue 99): rules 2.3, the eb_ratio_t screen, a top-10% list; data stays 2.2
        self.dq, self.data_issues, self.held = None, [], set()
        if self.v32:                                    # version 3.2: the data-quality pre-flight runs once per load (issue 81)
            import data_quality
            import screen_methods
            self.dq = data_quality.run_checks(v2_dir)
            self.scores32 = screen_methods.score_core(view_dir)       # eb_ratio and priority, the release 2 candidates (docs/screen_methods.md)
            if self.v33:
                self.scores32 = {**self.scores32, "eb_ratio_t": screen_methods.score_t(view_dir)}      # version 3.3: eb_ratio with the test-line covariate (the workflow v2.3 screen)
        self.note_rows = {}
        self.screen_candidates, self.set_aside, self.tool_calls = set(), {}, []
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
        self.stats = self._provider_stats() if self.v31 else {}
        self.office = provider_sim.Office(v2_dir, view_dir, seed=seed, correlation=correlation, roles=roles, version="2.1" if self.v31 else "2.0")
        self.requested = set()
        self.spent_usd = 0.0
        self.findings = {}
        self.summaries = {}

    # ---- helpers ---------------------------------------------------------
    def _provider_stats(self):
        """Magnitude columns for the screen table (version 3.1): ratio to expected, excess 99215 claims, low-complexity share and dollars."""
        fees = {c: v["allowed_amount"] for c, v in json.load(open(ALLOWED))["codes"].items()}
        out = {}
        for pid, r in self.rows.items():
            n, share, exp = int(r["n_claims"]), float(r["share_99215"]), float(r["expected_share"])
            c215 = [c for c in self.claims[pid] if c["cpt"] == "99215"]
            low = sum(self.chronic.get(c["patient_id"], 0) <= 1 for c in c215) / len(c215) if c215 else 0.0
            excess = (share - exp) * n
            out[pid] = {"ratio": round(share / exp, 2) if exp else 0.0, "excess": round(excess, 1), "low": round(low, 2),
                        "usd": round(max(excess, 0) * (fees["99215"] - fees["99214"]) * 0.8)}
        order_r = sorted(out, key=lambda p: -out[p]["ratio"])
        order_e = sorted(out, key=lambda p: -out[p]["excess"])
        rk_r, rk_e = {p: i for i, p in enumerate(order_r)}, {p: i for i, p in enumerate(order_e)}
        for p in out:                                   # claims-only priority: rank average of ratio and excess claims (docs/priority_score.md)
            out[p]["priority"] = -(rk_r[p] + rk_e[p]) / 2
        return out

    def budget_status(self):
        left = self.records_budget - len(self.requested)
        todo = sorted(p for p in self.screen_candidates if p not in self.requested and p not in self.findings)
        return (f"Records budget: {len(self.requested)} of {self.records_budget} providers asked ({left} left). "
                f"Screened candidates at 3 or more times expected not yet examined: {len(todo)}" + (f" (e.g. {', '.join(todo[:4])})." if todo else "."))

    def _peer_doc(self):
        return cs.doc_peer_rates(self.claims, self.docs, self.control) if self.docs else None

    def _packet(self, pid):
        return cs.build_packet(pid, self.rows[pid], self.chronic, self.age, self.conditions, self.claims, self.rates,
                               self.docs or None, self._peer_doc(), self.facts, self.note_rows or None)

    def _absorb(self, pid):
        for row in self.office.documentation_rows():
            self.docs[row["claim_id"]] = _doc_entry(row)
            self.facts[row["claim_id"]] = int(row["documented_data_level"])
            if row.get("note_id"):
                self.note_rows[row["claim_id"]] = row

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
    def screen_providers(self, method="riskadj", top_n=None, min_score=None, max_flagged=None, min_claims=0, top_pct=None):
        """Rank providers by a statistical score and choose a cutoff. method: zscore | riskadj | combined."""
        key = {"zscore": ("z", True), "riskadj": ("z_adj", True), "combined": ("mean_rank", False)}.get(method)
        if self.v31 and method == "priority":
            key = ("priority", True)
        if self.v32 and method == "eb_ratio" or self.v33 and method == "eb_ratio_t":
            key = (method, True)
        if not key:
            return {"error": "method must be zscore, riskadj or combined" + (" or priority" if self.v31 else "") + (" or eb_ratio" if self.v32 else "") + (" or eb_ratio_t" if self.v33 else "")}
        field, desc = key
        if top_pct is not None:
            if not self.v32:
                return {"error": "top_pct is not available in this version"}
            top_n = flagging.top_n_from_pct(len(self.rows), float(top_pct))       # payers flag a percentile of the panel
        elig = [r for r in self.rows.values() if int(r["n_claims"]) >= min_claims]
        if self.v32 and field in ("priority", "eb_ratio", "eb_ratio_t"):       # version 3.2: the same scores the workflow v2.2 uses, unrounded
            sc = self.scores32[field]
            elig.sort(key=lambda r: (-sc[r["provider_id"]], r["provider_id"]))
        elif field == "priority":
            elig.sort(key=lambda r: (-self.stats[r["provider_id"]]["priority"], r["provider_id"]))
        else:
            elig.sort(key=lambda r: (-float(r[field]) if desc else float(r[field]), r["provider_id"]))
        if min_score is not None and method not in ("combined", "priority", "eb_ratio", "eb_ratio_t"):
            sel = [r for r in elig if float(r[field]) >= min_score]
        else:
            sel = elig[: int(top_n or 25)]
        if max_flagged:
            sel = sel[: int(max_flagged)]
        zs = sorted(float(r["z_adj"]) for r in self.rows.values())
        q = lambda p: round(zs[min(int(p * len(zs)), len(zs) - 1)], 2)
        cols = ["provider", "claims", "share_99215", "expected_share", "z", "z_adj", "rank_combined"]
        extra = lambda r: []
        if self.v31:
            cols += ["ratio_to_expected", "excess_99215", "low_complexity_share", "excess_usd"]
            extra = lambda r: [self.stats[r["provider_id"]][k] for k in ("ratio", "excess", "low", "usd")]
            self.screen_candidates |= {r["provider_id"] for r in sel if self.stats[r["provider_id"]]["ratio"] >= CANDIDATE_RATIO}
        return {"method": method, "selected": len(sel),
                "table": {"cols": cols,
                          "rows": [[r["provider_id"], int(r["n_claims"]), float(r["share_99215"]), float(r["expected_share"]),
                                    float(r["z"]), float(r["z_adj"]), r["rank"]] + extra(r) for r in sel[:SCREEN_ROWS_SHOWN]]},
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
            rule, reason = (sr.rule_leaning_23 if self.v33 else sr.rule_leaning_22 if self.v32 else sr.rule_leaning)(packet)       # 3.2: rules 2.2 as workflow v2.2; 3.3: rules 2.3
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
            item = {"provider": pid, "leaning": lean, "source": source, "reason": reason, "chart_rule": chart}
            ns = (packet.get("documentation_review") or {}).get("note_signals")
            if ns:
                item["note_signals"] = {"notes": ns["notes"], "rates": ns["rates"], "looks_inflated": sr.inflated_notes(packet)}
            out.append(item)
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
        ids = self.office.random_claim_ids(provider_id)
        if not ids:
            return {"error": "the request was targeted; only a random sample supports extrapolation", "valid_for_extrapolation": False}
        rows = self.claims[provider_id]
        by_cpt = {r["claim_id"]: r["cpt"] for r in rows}
        plan = {"provider_id": provider_id, "frame_sizes": dict(Counter(r["cpt"] for r in rows)),
                "sampled_claims": {c: by_cpt[c] for c in ids}}
        reviewed = {c: (CODES[self.docs[c][0]] if c in self.docs else "") for c in ids}
        allowed = {c: v["allowed_amount"] for c, v in json.load(open(ALLOWED))["codes"].items()}
        amounts = {r["claim_id"]: (float(r["allowed_amount"]), float(r["paid_amount"])) for r in rows if r.get("allowed_amount")}
        res = pe.estimate(plan, reviewed, allowed, 0.90, claim_amounts=amounts)
        out = {"valid_for_extrapolation": True, "point_estimate": round(res["point_estimate"]), "ci_low": round(res["ci_low"]),
               "ci_high": round(res["ci_high"]), "reviewed_claims": res["reviewed_claims"], "sampled_claims": res["sampled_claims"],
               "caveat": "Draft arithmetic from a simulated review; a real recovery needs human review of the records."}
        if self.v31:
            strata = {c: d for c, d in res["strata"].items() if d.get("n_reviewed")}
            main = max(strata, key=lambda c: strata[c]["N"] * strata[c].get("mean_overpayment", 0), default=None)
            n_main = strata[main]["n_reviewed"] if main else 0
            out["stratum_reviewed"] = {c: d["n_reviewed"] for c, d in strata.items()}
            out["reliable"] = bool(main is None or n_main >= MIN_STRATUM_REVIEWED)
            if not out["reliable"]:
                out.update({"ci_low": None, "ci_high": None,
                            "note": f"Not reliable: only {n_main} reviewed charts in the {main} stratum (needs {MIN_STRATUM_REVIEWED}). Do not quote the dollar figure or an interval."})
        return out

    def note_checks(self, provider_id):
        """Claim-versus-note signals on the notes already received (version 3.1): rates and example claims."""
        if not self.v31:
            return {"error": "tool not available"}
        import note_checks as nc
        rows = [r for c, r in self.note_rows.items() if self.owner.get(c) == provider_id]
        if not rows:
            return {"error": "no notes received for this provider"}
        by_id = {r["claim_id"]: r for r in self.claims[provider_id]}
        audit = any(r.get("created_ts") for r in rows)
        sig = nc.signals_from_docs(rows, by_id, with_audit=audit)
        return {"notes": sig["notes"], "audit_trail_received": audit, "rates": {k: (round(v, 3) if v is not None else None) for k, v in sig.items() if k in nc.SIGNALS},
                "examples": {k: nc.flagged_claims(rows, by_id, k, 5, audit) for k in ("problems", "late", "unsigned", "data", "bulk_created", "paste_heavy")},
                "reading": "Rates, not proof: honest practices also copy forward, sign late and miss orders at a baseline rate. Fewer than 8 notes gives no pattern signals."}

    def request_audit_trail(self, provider_id, claim_ids):
        if not self.v31:
            return {"error": "tool not available"}
        out = self.office.request_audit_trail(provider_id, claim_ids)
        self._absorb(provider_id)
        return out

    def submit_findings(self, findings, set_aside=None):
        """findings: [{"provider_id", "leaning", "headline", "interpretation"}]. Stored as drafts; the run ends.
        Version 3.1 also needs a reason for every screened candidate it leaves out (set_aside) and refuses summaries that fail the lint."""
        bad = [f.get("provider_id") for f in findings if f.get("provider_id") not in self.rows or f.get("leaning") not in
               (sr.UPCODING, sr.HIGH_ACUITY, sr.INCONCLUSIVE)]
        if bad:
            return {"error": f"invalid provider or leaning for: {bad}"}
        version = "2.1" if self.v31 else "2.0"
        built, problems = {}, {}
        if self.v32:
            held = {}
            for f in findings:
                h = self._hold(f["provider_id"])
                if f["leaning"] == sr.UPCODING and h["affected"] and h["needs_chart_evidence"]:
                    held[f["provider_id"]] = h["reasons"]
            if held:
                return {"error": "these providers' upcoding findings are held by a data problem and charts do not yet carry them (at least 8 charts received); "
                                 "use leaning inconclusive and say why, or obtain charts first", "held": held}
        for f in findings:
            packet = self._packet(f["provider_id"])
            built[f["provider_id"]] = sr.assemble(packet, f["leaning"], f.get("headline"), f.get("interpretation"), version=version)
            if self.v31:
                lint = summary_lint.lint(built[f["provider_id"]], packet, summary_lint.evidence_from(self.office.transcript, self._audit_log(), f["provider_id"]), rules23=self.v33)
                if lint["hard"]:
                    problems[f["provider_id"]] = lint["hard"]
        if self.v31:
            aside = {a["provider_id"]: a.get("reason", "") for a in (set_aside or []) if a.get("provider_id") in self.rows}
            missing = sorted(c for c in self.screen_candidates if c not in built and not aside.get(c))
            if missing:
                return {"error": "every screened provider billing 99215 at 3 or more times its expected share needs a finding or a reason it was set aside",
                        "missing": missing[:20], "how": "add them to findings, or to set_aside with a reason"}
            if problems:
                return {"error": "some findings fail the checks; fix the wording or the leaning and submit again", "problems": problems}
            self.set_aside = aside
        if self.v32:                                    # the data caveat is added after the lint, so its percentages are not read as unmatched figures
            for pid_, s_ in built.items():
                h = self._hold(pid_)
                if h["affected"]:
                    s_["rationale"] = (s_["rationale"] + " " + h["caveat"]).strip()
        self.findings.update(built)
        return {"accepted": len(findings), "status": "drafts for human review; nothing is sent or decided automatically"}

    def _hold(self, pid):
        """Data-quality hold for one provider: flags from the pre-flight or from flag_data_issue (charts received lift the need for chart evidence)."""
        import data_quality
        rep = {"per_provider": {**(self.dq or {}).get("per_provider", {})}}
        for issue in self.data_issues:
            if issue["hold_findings"] and (not issue["provider_ids"] or pid in issue["provider_ids"]):
                rep["per_provider"][pid] = rep["per_provider"].get(pid, []) + [{"flag": "agent_flag", "detail": issue["detail"]}]
        charts = self._chart_rule(pid)["charts"] if pid in self.rows else 0
        return data_quality.hold_decision(rep, pid, charts, MIN_STRATUM_REVIEWED)

    def data_quality(self, provider_id=None):
        """Read-only: the pre-flight's global flags and, for one provider, its flags (version 3.2)."""
        if not self.v32:
            return {"error": "tool not available"}
        import data_quality
        out = data_quality.short(self.dq, provider_id)
        out["issues_you_flagged"] = [{"issue": i["issue"], "providers": i["provider_ids"], "hold": i["hold_findings"]} for i in self.data_issues]
        if provider_id:
            out["provider"]["hold"] = {k: v for k, v in self._hold(provider_id).items() if k != "caveat"}
        return out

    def flag_data_issue(self, issue, detail, provider_ids=None, hold_findings=True):
        """Record a data concern for a person to raise with the plan; optionally hold the affected findings. The agent never requests data itself (version 3.2)."""
        if not self.v32:
            return {"error": "tool not available"}
        if not str(issue).strip() or not str(detail).strip():
            return {"error": "issue and detail are required"}
        bad = [p for p in (provider_ids or []) if p not in self.rows]
        if bad:
            return {"error": f"unknown providers: {bad}"}
        rec = {"issue": str(issue)[:120], "detail": str(detail)[:600], "provider_ids": list(provider_ids or []), "hold_findings": bool(hold_findings)}
        self.data_issues.append(rec)
        return {"recorded": True, "n_issues": len(self.data_issues),
                "next": "A person will raise this with the plan; you cannot request data yourself. "
                        + ("Upcoding findings for the affected providers now need chart evidence." if rec["hold_findings"] else "No findings are held.")}

    def _audit_log(self):
        return [{"tool": t, "args": a, "result": r} for t, a, r in self.tool_calls]

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
                          "input_schema": {"type": "object", "properties": {"method": {"type": "string", "enum": ["zscore", "riskadj", "combined"] + (["priority"] if self.v31 else []) + (["eb_ratio"] if self.v32 else []) + (["eb_ratio_t"] if self.v33 else [])},
                                           "top_n": {"type": "integer"}, "min_score": {"type": "number"}, "max_flagged": {"type": "integer"},
                                           "min_claims": {"type": "integer"},
                                           **({"top_pct": {"type": "number", "description": "select the top PCT percent of providers instead of top_n (payers flag a percentile, for example 5)"}} if self.v32 else {})}}})
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
            *self._v31_tools(),
            *self._v32_tools(),
            {"name": "submit_findings", "description": "Submit your final findings and end the run. leaning is one of pattern_consistent_with_upcoding, "
             "pattern_consistent_with_high_acuity_panel, inconclusive. Include every provider you looked at closely; only 'upcoding' ones go to recovery.",
             "input_schema": {"type": "object", "properties": {"findings": {"type": "array", "items": {"type": "object", "properties": {
                 "provider_id": {"type": "string"}, "leaning": {"type": "string"}, "headline": {"type": "string"},
                 "interpretation": {"type": "string"}}, "required": ["provider_id", "leaning"]}},
                 **({"set_aside": {"type": "array", "description": "screened providers you are leaving out, each with the reason", "items": {"type": "object", "properties": {
                     "provider_id": {"type": "string"}, "reason": {"type": "string"}}, "required": ["provider_id", "reason"]}}} if self.v31 else {})},
              "required": ["findings"]}}]
        return tools

    def _v31_tools(self):
        if not self.v31:
            return []
        pid = {"provider_id": {"type": "string"}}
        return [{"name": "note_checks", "description": "Claim-versus-note signals on the notes already received for a provider: how often the notes address fewer problems "
                 "than their claimed level implies, show data review the claim cannot back, are unsigned, signed late, and (if an audit trail was received) bulk-created or paste-heavy. "
                 "Rates, not proof; example claims are listed.", "input_schema": {"type": "object", "properties": pid, "required": ["provider_id"]}},
                {"name": "request_audit_trail", "description": "Second-tier request for the EHR audit trail of charts already received (created and edited times, paste events). "
                 "Costs a round and the office may refuse.", "input_schema": {"type": "object", "properties": {**pid, "claim_ids": {"type": "array", "items": {"type": "string"}}},
                                                                             "required": ["provider_id", "claim_ids"]}}]

    def _v32_tools(self):
        if not self.v32:
            return []
        return [{"name": "data_quality", "description": "Read-only report from the data-quality pre-flight that ran on the delivered extract: global flags (control totals, "
                 "diagnosis codes per claim, rendering NPIs, member join, duplicates, broken chains, recent months) and, with provider_id, that provider's flags and whether its "
                 "findings are held. A flag can mean the screen score is unreliable for that provider.",
                 "input_schema": {"type": "object", "properties": {"provider_id": {"type": "string"}}}},
                {"name": "flag_data_issue", "description": "Record a data concern for a person to raise with the plan (for example suspected diagnosis truncation). You cannot request "
                 "data from the plan yourself. hold_findings (default true) makes upcoding findings for the listed providers (all if none listed) need chart evidence.",
                 "input_schema": {"type": "object", "properties": {"issue": {"type": "string"}, "detail": {"type": "string"},
                                                                  "provider_ids": {"type": "array", "items": {"type": "string"}}, "hold_findings": {"type": "boolean"}},
                                  "required": ["issue", "detail"]}}]

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
              "note_checks": lambda: self.note_checks(args["provider_id"]),
              "request_audit_trail": lambda: self.request_audit_trail(args["provider_id"], args["claim_ids"]),
              "draft_summary": lambda: self.draft_summary(args["provider_id"]),
              "estimate_overpayment": lambda: self.estimate_overpayment(args["provider_id"]),
              "data_quality": lambda: self.data_quality(args.get("provider_id")),
              "flag_data_issue": lambda: self.flag_data_issue(args["issue"], args["detail"], args.get("provider_ids"), args.get("hold_findings", True)),
              "submit_findings": lambda: self.submit_findings(args["findings"], args.get("set_aside"))}.get(name)
        if fn is None:
            return {"error": f"unknown tool {name}"}
        try:
            out = fn()
        except (KeyError, TypeError, ValueError, AttributeError) as e:      # malformed arguments go back to the model (issue 85)
            return {"error": f"bad arguments: {e}"}
        if name in ("estimate_overpayment", "hybrid_review", "draft_summary", "note_checks", "flag_data_issue"):
            self.tool_calls.append((name, dict(args), json.dumps(out)))
        return out
