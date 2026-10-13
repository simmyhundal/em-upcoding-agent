"""Simulated provider office: multi-round records requests, deficiencies and follow-ups (issue 47).

A real records request is a conversation: the plan asks, the office answers (often incompletely), the plan says what was wrong,
and this repeats until the plan has usable charts or closes the request. This module plays the office.

What the plan side sees (payer-visible): each response's status, free text, the claim IDs that came back usable, structured
deficiencies, days elapsed and the sample kind. What it never sees: the office's hidden behavior (cooperative, slow, sloppy,
evasive), the records universe, or any answer key. Behavior is drawn independently of upcoder status by default; `correlation`
raises the chance that upcoders get evasive or sloppy behavior (a perfect "stalls means guilty" link would be easier by
construction). Only the simulator reads the records universe; the agent tools see only what comes back.

Response types (illustrative, not legal guidance): complete, partial, wrong_content, missing_signature, wrong_dates, illegible,
clarification_requested, extension, objection, no_response. Non-response is never evidence of upcoding on its own: a provider
with no usable charts ends non_responsive and the summary step treats too few charts as inconclusive.

Sample kinds: "random" (a seeded random sample of the provider's visits) supports extrapolating to an overpayment estimate;
"targeted" (a chosen code, or a list of claim IDs) does not, and the label travels with the result.

Caps: at most MAX_ROUNDS rounds per provider (the first request plus follow-ups) and MAX_DAYS elapsed days per provider.
"""
import csv
import json
import os
import random
from collections import defaultdict

import records

MAX_ROUNDS = 3
MAX_DAYS = 120
DEFAULT_DEADLINE = 30
BEHAVIOR_MIX = {"cooperative": 0.55, "slow": 0.15, "sloppy": 0.20, "evasive": 0.10}
GUILTY_MIX = {"evasive": 0.5, "sloppy": 0.3, "slow": 0.1, "cooperative": 0.1}   # used when correlation > 0
DAYS = {"cooperative": (10, 25), "slow": (25, 60), "sloppy": (10, 40), "evasive": (20, 50)}
# probability of each response type on the first round, and on later rounds, per behavior
FIRST = {
    "cooperative": {"complete": 0.80, "partial": 0.12, "wrong_content": 0.05, "missing_signature": 0.03},
    "slow": {"extension": 0.55, "no_response": 0.15, "complete": 0.30},
    "sloppy": {"partial": 0.30, "wrong_content": 0.25, "missing_signature": 0.20, "wrong_dates": 0.10, "illegible": 0.10, "complete": 0.05},
    "evasive": {"objection": 0.35, "no_response": 0.30, "clarification_requested": 0.20, "partial": 0.15},
}
LATER = {
    "cooperative": {"complete": 0.95, "partial": 0.05},
    "slow": {"complete": 0.80, "partial": 0.20},
    "sloppy": {"complete": 0.55, "partial": 0.30, "wrong_content": 0.15},
    "evasive": {"no_response": 0.45, "objection": 0.25, "partial": 0.20, "complete": 0.10},
}
TEXT = {
    "complete": "Enclosed are the requested records.",
    "partial": "We have sent what we could locate; some visits are not included.",
    "wrong_content": "Enclosed is the billing ledger for the requested visits.",
    "missing_signature": "Enclosed are the notes; some are not signed or attested.",
    "wrong_dates": "Enclosed are notes for the patients; the dates of service differ from your list.",
    "illegible": "Enclosed are scanned notes.",
    "clarification_requested": "Please clarify which visits you want and the purpose of the request.",
    "extension": "We need additional time to gather these records.",
    "objection": "We object to this request as broader than the minimum necessary.",
    "no_response": "",
}
DEFICIENCY_TEXT = {
    "MISSING_VISITS": "Some requested visits were not returned.",
    "WRONG_CONTENT": "The documents sent are not clinical notes for the visits.",
    "MISSING_SIGNATURE": "Notes lack a signature or attestation.",
    "WRONG_DATES": "Dates of service do not match the request.",
    "ILLEGIBLE": "Documents could not be read.",
    "SCOPE_UNCLEAR": "The office asked which visits are wanted.",
    "EXTENSION": "The office asked for more time.",
    "OBJECTION": "The office objects to the scope of the request.",
    "NO_RESPONSE": "No response by the deadline.",
}
STATUS_TO_CODE = {"wrong_content": "WRONG_CONTENT", "missing_signature": "MISSING_SIGNATURE", "wrong_dates": "WRONG_DATES",
                  "illegible": "ILLEGIBLE", "clarification_requested": "SCOPE_UNCLEAR", "extension": "EXTENSION",
                  "objection": "OBJECTION", "no_response": "NO_RESPONSE"}
FIXABLE_BY_FOLLOWUP = {"MISSING_SIGNATURE": 0.8, "WRONG_DATES": 0.7, "ILLEGIBLE": 0.6}


def _rows(path):
    with open(path) as f:
        return list(csv.DictReader(f))


class Office:
    def __init__(self, v2_dir, view_dir, seed=1, correlation=0.0, roles=None):
        """roles: optional {provider_id: role}, used ONLY to draw hidden behavior when correlation > 0 (evaluation use)."""
        self.seed = seed
        self.universe = {r["claim_id"]: r for r in _rows(os.path.join(v2_dir, "records", "records_universe.csv"))}
        self.claims = defaultdict(list)
        for r in _rows(os.path.join(view_dir, "claims.csv")):
            self.claims[r["provider_id"]].append(r)
        self.correlation, self.roles = correlation, roles or {}
        self.state = {}
        self.transcript = []

    # ---- hidden behavior -------------------------------------------------
    def _behavior(self, pid):
        rng = random.Random(f"{self.seed}:behavior:{pid}")
        mix = BEHAVIOR_MIX
        if self.correlation > 0 and self.roles.get(pid) == "upcoder" and rng.random() < self.correlation:
            mix = GUILTY_MIX
        return rng.choices(list(mix), weights=list(mix.values()))[0]

    def _st(self, pid):
        if pid not in self.state:
            self.state[pid] = {"behavior": self._behavior(pid), "round": 0, "day": 0, "requested": [], "sample_kind": None,
                               "usable": {}, "pending": defaultdict(list), "closed": None, "late": None}
        return self.state[pid]

    # ---- plan-side actions ----------------------------------------------
    def send_request(self, pid, sample, deadline=DEFAULT_DEADLINE):
        """sample: {"kind": "random", "n": N} | {"kind": "targeted", "cpt": "99215", "n": N} | {"kind": "targeted", "claim_ids": [...]}"""
        st = self._st(pid)
        if st["round"] > 0:
            return self._err(pid, "a request is already open; use follow_up or close_request")
        rows = sorted(self.claims.get(pid, []), key=lambda r: r["claim_id"])
        if not rows:
            return self._err(pid, "unknown provider or no claims")
        rng = random.Random(f"{self.seed}:sample:{pid}")
        kind = sample.get("kind", "random")
        if "claim_ids" in sample:
            ids = [c for c in sample["claim_ids"] if any(r["claim_id"] == c for r in rows)][:200]
            kind = "targeted"
        else:
            pool = [r["claim_id"] for r in rows if sample.get("cpt") in (None, r["cpt"])]
            if sample.get("cpt"):
                kind = "targeted"
            ids = rng.sample(pool, min(int(sample.get("n", 30)), len(pool)))
        st["requested"], st["sample_kind"] = ids, kind
        return self._round(pid, st, deadline, addressed=None)

    def follow_up(self, pid, addressed_codes, deadline=DEFAULT_DEADLINE, claim_ids=None):
        """Tell the office what was wrong. claim_ids narrows the scope (helps with objections and clarifications)."""
        st = self._st(pid)
        if st["round"] == 0:
            return self._err(pid, "no open request")
        if st["closed"]:
            return self._err(pid, "request is closed")
        if st["round"] >= MAX_ROUNDS or st["day"] >= MAX_DAYS:
            return self._err(pid, "round or day cap reached; close the request")
        if claim_ids:
            st["requested"] = [c for c in st["requested"] if c in set(claim_ids)] or st["requested"]
        return self._round(pid, st, deadline, addressed=set(addressed_codes or []))

    def close_request(self, pid, reason=""):
        st = self._st(pid)
        n_req, n_use = len(st["requested"]), len(st["usable"])
        end = "non_responsive" if n_use == 0 else ("complete" if n_use >= 0.9 * max(n_req, 1) else "partial")
        st["closed"] = end
        out = {"provider_id": pid, "end_state": end, "usable_charts": n_use, "requested": n_req, "rounds": st["round"],
               "days": st["day"], "sample_kind": st["sample_kind"], "reason": reason,
               "note": "No response is not evidence of upcoding; it only means this provider cannot be judged from charts."}
        self.transcript.append({"action": "close_request", **out})
        return out

    # ---- internals --------------------------------------------------------
    def _err(self, pid, msg):
        return {"provider_id": pid, "error": msg}

    def _draw(self, rng, table):
        return rng.choices(list(table), weights=list(table.values()))[0]

    def _round(self, pid, st, deadline, addressed):
        rng = random.Random(f"{self.seed}:round:{pid}:{st['round']}")
        beh = st["behavior"]
        first = st["round"] == 0
        st["round"] += 1
        lo, hi = DAYS[beh]
        delay = rng.randint(lo, hi)
        released = []
        if addressed:                                             # fix what the office was told was wrong
            for code in list(st["pending"]):
                if code in addressed and rng.random() < FIXABLE_BY_FOLLOWUP.get(code, 0.0):
                    released += st["pending"].pop(code)
        if st["late"] and not first:                              # a response that missed the last deadline arrives now
            kind_of_response = st["late"]
            st["late"] = None
        else:
            table = FIRST[beh] if first else LATER[beh]
            if addressed and "EXTENSION" in addressed:
                table = {"complete": 0.8, "partial": 0.2} if beh == "slow" else table
            kind_of_response = self._draw(rng, table)
        status = kind_of_response
        if delay > deadline and status not in ("extension", "no_response") and not first:
            st["late"], status = status, "no_response"
        elif delay > deadline and first and status not in ("extension", "no_response") and rng.random() < 0.5:
            st["late"], status = status, "no_response"
        st["day"] += min(delay, deadline) if status == "no_response" else delay
        missing_ids, unusable_ids, deficiencies = [], [], []
        remaining = [c for c in st["requested"] if c not in st["usable"]]
        if status in ("complete", "partial"):
            got = remaining if status == "complete" else rng.sample(remaining, max(1, int(len(remaining) * rng.uniform(0.4, 0.7))))
            for c in got:
                st["usable"][c] = records.read_chart(self.universe[c], rng)
            missing_ids = [c for c in remaining if c not in st["usable"]]
            if missing_ids:
                deficiencies.append({"code": "MISSING_VISITS", "text": DEFICIENCY_TEXT["MISSING_VISITS"], "claim_ids": missing_ids})
        elif status in ("missing_signature", "wrong_dates", "illegible"):
            held = remaining[: max(1, int(len(remaining) * 0.8))]
            st["pending"][STATUS_TO_CODE[status]] += held
            unusable_ids = held
            deficiencies.append({"code": STATUS_TO_CODE[status], "text": DEFICIENCY_TEXT[STATUS_TO_CODE[status]], "claim_ids": held})
        elif status in STATUS_TO_CODE:
            code = STATUS_TO_CODE[status]
            deficiencies.append({"code": code, "text": DEFICIENCY_TEXT[code], "claim_ids": remaining if code != "EXTENSION" else []})
        for c in released:                                        # fixed by the office this round
            st["usable"][c] = records.read_chart(self.universe[c], rng)
        text = TEXT.get(status, "")
        if status == "extension":
            text += f" We expect to respond within {rng.randint(20, 45)} days."
        resp = {"provider_id": pid, "round": st["round"], "status": status, "text": text, "deficiencies": deficiencies,
                "usable_claim_ids": sorted(st["usable"]), "usable_total": len(st["usable"]), "requested_total": len(st["requested"]),
                "unusable_claim_ids": sorted(unusable_ids), "days_elapsed_total": st["day"], "sample_kind": st["sample_kind"],
                "rounds_left": max(MAX_ROUNDS - st["round"], 0), "days_left": max(MAX_DAYS - st["day"], 0)}
        self.transcript.append({"action": "send_request" if first else "follow_up", "deadline": deadline, **resp})
        return resp

    # ---- outputs ---------------------------------------------------------
    def documentation_rows(self, kinds=("random", "targeted")):
        """Usable chart readings in the documentation.csv shape, for providers whose sample kind is in `kinds`."""
        out = []
        for pid, st in self.state.items():
            if st["sample_kind"] in kinds:
                out += list(st["usable"].values())
        return out

    def end_states(self):
        return {pid: ("closed:" + st["closed"] if st["closed"] else "open") for pid, st in self.state.items()}

    def write_transcript(self, path):
        with open(path, "w") as f:
            for row in self.transcript:
                f.write(json.dumps(row) + "\n")
