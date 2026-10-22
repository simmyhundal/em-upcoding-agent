"""Workflow v4.0's ask-or-skip (issue 131), shared by the workflow (eval/workflow_policy_40.py) and agent v5.0 (src/agent_tools.py, as advice): a ridge model of the net value of asking a listed
provider under score 4.0, fitted on development batches 1 to 4 (eval/fit_ask_40.py, src/policy_40_ask.json). Inputs are what the payer sees before asking (policy_25.ask_vector)."""
import json
import math
import os

import policy_25 as p25

ASK_MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "policy_40_ask.json")


def load_ask(path=None):
    return json.load(open(path or ASK_MODEL))


ASK_FEATURES_41 = ["rank", "screen_score", "log_claims", "share_hi", "n_hi", "share_99215"]


def ask_vector_41(row, claims):
    """Ask features built on the eb_upper_t screen (workflow v4.1, issue 132): the shrunk score, the panel size, and the observed share and count of visits billed 99214 or 99215 from the
    provider's own claims in the extract (what the payer sees before asking). The v4.0 vector leans on 99215-only quantities (ratio, excess claims, adjusted z) that data 4.0's habits barely move."""
    n = max(len(claims), 1)
    hi = sum(1 for c in claims if c["cpt"] in ("99214", "99215"))
    top = sum(1 for c in claims if c["cpt"] == "99215")
    return [int(row["rank"]), float(row["screen_score"]), math.log(n), hi / n, float(hi), top / n]


def predict(model, row, claims=None):
    """Predicted net dollars (score 4.0) of asking this listed provider for charts."""
    x = ask_vector_41(row, claims or []) if model.get("features_version") == "4.1" else p25.ask_vector(row)
    z = [(v - m) / s for v, m, s in zip(x, model["mu"], model["sd"])]
    return model["beta"][0] + sum(b * v for b, v in zip(model["beta"][1:], z))


def ask_linear(model, row, claims=None):
    return predict(model, row, claims) > model.get("margin", 0.0)
