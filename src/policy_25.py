"""Workflow v2.5's learned policy (issue 109): ask-or-skip and stop-or-escalate, both fitted on net dollars (src/policy_25.json).

Before any request, a ridge model of the net dollars of asking a practice (from screen rank, log ratio, excess claims, log claims, screen score and adjusted z) says ask when the
prediction is above zero. After the first sample, one ridge model per branch (STOP, TARG, AUD, BOTH) predicts net dollars from the state vector; the best branch is taken.
Payer-visible inputs only. The answer key trained the coefficients (eval/export_policy_25.py) and is never read here.
"""
import json
import math
import os

import escalation_policy as ep

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "policy_25.json")
ASK_FEATURES = ["rank", "log_ratio", "excess", "log_claims", "screen_score", "z_adj"]
BRANCHES = ep.BRANCHES


def load(path=PATH):
    return json.load(open(path))


def ask_vector(flagged_row):
    """Pre-ask features from one row of the screen's flagged file."""
    exp, share, n = float(flagged_row["expected_share"]), float(flagged_row["share_99215"]), int(flagged_row["n_claims"])
    ratio = share / exp if exp else 0.0
    return [int(flagged_row["rank"]), math.log(max(ratio, 0.05)), n * (share - exp), math.log(n), float(flagged_row["screen_score"]), float(flagged_row["z_adj"])]


def _predict(model, x):
    z = [(v - m) / s for v, m, s in zip(x, model["mu"], model["sd"])]
    return model["beta"][0] + sum(b * v for b, v in zip(model["beta"][1:], z))


def ask(policy, x):
    return _predict(policy["ask"], x) > 0


def choose(policy, x):
    """The branch with the highest predicted net dollars for the state vector x."""
    return max(BRANCHES, key=lambda b: _predict(policy["branches"][b], x))
