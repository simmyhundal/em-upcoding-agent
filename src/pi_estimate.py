"""Overpayment estimate from a reviewed sample (Payment Integrity packet, step 3).

Takes the sampling plan written by pi_packet.py, a reviewed CSV (claim_id, supported_cpt) and the allowed amounts, and
extrapolates an overpayment estimate with a confidence interval. Per-claim overpayment is
allowed(billed) - allowed(supported) when the supported level is lower than billed, else 0 (underbilling is ignored).
Claims with a blank supported_cpt are treated as "records not received / not reviewed": by default they are excluded from
the estimate (the response rate is reported); --missing unsupported treats them as supported at one level below billed.

IMPORTANT: in a real case the supported level must come from a human review of the records. This tool only does the
arithmetic. The worked example under reports/pi_packets/ is SIMULATED from the synthetic documentation sample.

Usage:
    python src/pi_estimate.py PLAN_JSON REVIEWED_CSV ALLOWED_JSON [--confidence 0.90] [--missing exclude|unsupported]
"""
import argparse
import csv
import json
import math

LEVEL = {"99211": 0, "99212": 1, "99213": 2, "99214": 3, "99215": 4}
CODES = list(LEVEL)
# Two-sided t critical values, df 1..30 (standard table); beyond 30 use the normal values.
T90 = [6.314, 2.920, 2.353, 2.132, 2.015, 1.943, 1.895, 1.860, 1.833, 1.812, 1.796, 1.782, 1.771, 1.761, 1.753, 1.746,
       1.740, 1.734, 1.729, 1.725, 1.721, 1.717, 1.714, 1.711, 1.708, 1.706, 1.703, 1.701, 1.699, 1.697]
T95 = [12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179, 2.160, 2.145, 2.131, 2.120,
       2.110, 2.101, 2.093, 2.086, 2.080, 2.074, 2.069, 2.064, 2.060, 2.056, 2.052, 2.048, 2.045, 2.042]


def t_crit(df, confidence):
    table, z = {0.90: (T90, 1.645), 0.95: (T95, 1.960)}[confidence]
    return table[df - 1] if 1 <= df <= 30 else z


def overpay(billed, supported, allowed):
    if LEVEL[supported] >= LEVEL[billed]:
        return 0.0
    return allowed[billed] - allowed[supported]


def estimate(plan, reviewed, allowed, confidence=0.90, missing="exclude"):
    """plan: sampling plan dict; reviewed: {claim_id: supported_cpt or ''}; allowed: {cpt: dollars}."""
    billed = plan["sampled_claims"]                       # claim_id -> billed cpt
    strata = {}
    for code, N in plan["frame_sizes"].items():
        vals = []
        for cid, b in billed.items():
            if b != code:
                continue
            s = reviewed.get(cid, "")
            if not s:
                if missing == "unsupported":
                    s = CODES[max(LEVEL[b] - 1, 0)]
                else:
                    continue
            vals.append(overpay(b, s, allowed))
        strata[code] = (N, vals)
    total = var = 0.0
    n_all = k = 0
    detail = {}
    for code, (N, vals) in strata.items():
        n = len(vals)
        if n == 0:
            detail[code] = {"N": N, "n_reviewed": 0}
            continue
        mean = sum(vals) / n
        s2 = (sum((v - mean) ** 2 for v in vals) / (n - 1)) if n > 1 else 0.0
        total += N * mean
        var += N * N * (1 - n / N) * s2 / n
        n_all += n
        k += 1
        detail[code] = {"N": N, "n_reviewed": n, "mean_overpayment": mean,
                        "share_with_overpayment": sum(1 for v in vals if v > 0) / n}
    se = math.sqrt(var)
    df = max(n_all - k, 1)
    half = t_crit(df, confidence) * se
    sampled = len(billed)
    return {"point_estimate": total, "standard_error": se, "confidence": confidence, "df": df,
            "ci_low": max(0.0, total - half), "ci_high": total + half,
            "reviewed_claims": n_all, "sampled_claims": sampled,
            "response_rate": n_all / sampled if sampled else None, "strata": detail, "missing": missing}


def render(provider, res):
    lines = [f"Overpayment estimate for {provider}", "",
             f"- Point estimate: ${res['point_estimate']:,.0f}",
             f"- {int(res['confidence'] * 100)}% confidence interval: ${res['ci_low']:,.0f} to ${res['ci_high']:,.0f} "
             f"(lower limit floored at $0; t with {res['df']} degrees of freedom)",
             f"- Reviewed {res['reviewed_claims']} of {res['sampled_claims']} sampled claims "
             f"({res['response_rate']:.0%} response); missing records handled as: {res['missing']}"]
    for code, d in res["strata"].items():
        if d["n_reviewed"]:
            lines.append(f"- {code}: frame {d['N']}, reviewed {d['n_reviewed']}, mean overpayment per claim "
                         f"${d['mean_overpayment']:,.2f}, {d['share_with_overpayment']:.0%} with an overpayment")
        else:
            lines.append(f"- {code}: frame {d['N']}, no reviewed claims")
    return "\n".join(lines)


def load_reviewed(path):
    with open(path) as f:
        return {r["claim_id"]: (r.get("supported_cpt") or "").strip() for r in csv.DictReader(f)}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("plan_json")
    ap.add_argument("reviewed_csv")
    ap.add_argument("allowed_json")
    ap.add_argument("--confidence", type=float, default=0.90, choices=[0.90, 0.95])
    ap.add_argument("--missing", default="exclude", choices=["exclude", "unsupported"])
    a = ap.parse_args()
    plan = json.load(open(a.plan_json))
    allowed = {c: v["allowed_amount"] for c, v in json.load(open(a.allowed_json))["codes"].items()}
    print(render(plan["provider_id"], estimate(plan, load_reviewed(a.reviewed_csv), allowed, a.confidence, a.missing)))
