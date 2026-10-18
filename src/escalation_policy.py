"""Workflow v2.4's learned stop-or-escalate policy (issue 108, Stage 2), read from a plain JSON rule file (src/policy_24.json).

After a practice's first sample (a random request for 30 charts and a follow-up on any deficiency) the policy picks one of STOP, TARG (a targeted request for 15 charts of the top
code), AUD (an audit-trail request) or BOTH, by maximizing  P_b(found) - kappa P_b(honest called) - lambda P(honest) E[extra rounds_b]  from small logistic and linear models whose
coefficients are in the JSON. Inputs are payer-visible only: what the first sample returned and the screen rank and ratio. The answer key trained the coefficients
(eval/export_policy_24.py) and is never read here. The file records the seeds it was fitted on and lambda; it is frozen before any fresh seed is generated.
"""
import json
import math
import os

import note_checks
import records
from case_summary import BILLED_LEVEL, MDM_LEVELS

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "policy_24.json")
STATE = ["rank", "log_ratio", "charts", "docs99215", "unsupp99215", "notes", "late", "problems", "data", "silent", "first_rounds"]
BRANCHES = ("STOP", "TARG", "AUD", "BOTH")


def load(path=PATH):
    return json.load(open(path))


def state_vector(usable_rows, claim_rows, rank, ratio, rounds):
    """Features after the first sample. usable_rows: the chart rows the office returned (documentation.csv columns); claim_rows: the provider's claims; rank: 1-based."""
    by_id = {r["claim_id"]: r for r in claim_rows}
    got = [r for r in usable_rows if r["claim_id"] in by_id]
    docs = {}
    for r in got:
        mins = r["documented_minutes"]
        docs[r["claim_id"]] = max(MDM_LEVELS.index(r["documented_mdm_level"]), records.level_from_minutes(mins))
    d99215 = [c for c in docs if by_id[c]["cpt"] == "99215"]
    bad = sum(docs[c] < BILLED_LEVEL["99215"] for c in d99215)
    notes = [r for r in got if r.get("note_id")]
    sig = note_checks.signals_from_docs(notes, by_id, with_audit=False) if notes else None
    n_notes = sig["notes"] if sig else 0
    rate = lambda k: (round(sig[k], 3) if sig and sig.get(k) is not None else 0.0) if n_notes >= 8 else 0.0
    return [rank, math.log(max(ratio, 0.05)), len(got), len(d99215), round(bad / len(d99215), 3) if d99215 else 0.0, n_notes, rate("late"), rate("problems"), rate("data"),
            float(len(got) == 0), rounds]


def _sigmoid(z):
    return 1 / (1 + math.exp(-max(min(z, 30), -30)))


def _dot(beta, z):
    return beta[0] + sum(b * v for b, v in zip(beta[1:], z))


def choose(policy, x):
    """The branch with the highest expected reward for state vector x."""
    z = [(v - m) / s for v, m, s in zip(x, policy["mu"], policy["sd"])]
    honest = _sigmoid(_dot(policy["honest"], z))
    best, best_score = "STOP", None
    for b in BRANCHES:
        m = policy["branches"][b]
        score = _sigmoid(_dot(m["found"], z)) - policy["kappa"] * _sigmoid(_dot(m["hc"], z)) - policy["lambda"] * honest * max(_dot(m["extra"], z), 0.0)
        if best_score is None or score > best_score:
            best, best_score = b, score
    return best
