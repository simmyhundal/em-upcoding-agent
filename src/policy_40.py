"""Workflow v4.0's ask-or-skip (issue 131), shared by the workflow (eval/workflow_policy_40.py) and agent v5.0 (src/agent_tools.py, as advice): a ridge model of the net value of asking a listed
provider under score 4.0, fitted on development batches 1 to 4 (eval/fit_ask_40.py, src/policy_40_ask.json). Inputs are what the payer sees before asking (policy_25.ask_vector)."""
import json
import os

import policy_25 as p25

ASK_MODEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "policy_40_ask.json")


def load_ask(path=None):
    return json.load(open(path or ASK_MODEL))


def predict(model, row):
    """Predicted net dollars (score 4.0) of asking this listed provider for charts."""
    x = p25.ask_vector(row)
    z = [(v - m) / s for v, m, s in zip(x, model["mu"], model["sd"])]
    return model["beta"][0] + sum(b * v for b, v in zip(model["beta"][1:], z))


def ask_linear(model, row):
    return predict(model, row) > 0
