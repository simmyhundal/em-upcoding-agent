"""Generate synthetic v2 data: plan-shaped tables (members, providers, claim header and lines, remittance, reference),
plus a hidden records universe that only a records request can reveal. See docs/v2_schemas.md.

Same calibrated visit-level model as src/generate_synthetic.py (v1 stays runnable for comparison), with these changes:
  * diagnoses are generated on claims; conditions are never stored on members (see src/derive.py)
  * visits can be rendered by a provider other than the member's PCP
  * header/line/remittance structure, with replacement and void claims, denials, modifiers and lab lines
  * the base rate of upcoding is configurable (--providers N --upcoder-rate R)
  * MDM elements and documented minutes are separate and can disagree; the documented level is derived by rule
    (src/records.py), not generated directly
  * some upcoders clone documentation (--clone-share): on upgraded visits the documented elements and minutes are inflated to
    the billed level while the claim facts (diagnoses, lab lines) stay as they were

Usage:
    python src/generate_v2.py OUT_DIR [--seed 42] [--providers 216] [--upcoder-rate 0.037] [--hard-neg-rate 0.037]
                              [--clone-share 0.5] [--answer-key eval/answer_key/ground_truth_v2.json]
"""
import argparse
import csv
import json
import os
from datetime import date, timedelta

import numpy as np

import generate_synthetic as g1
import notes_v21

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_KEY = os.path.join(ROOT, "eval", "answer_key", "ground_truth_v2.json")
CODES = g1.CODES
LAB_CODES = [("80053", 10.56), ("85025", 7.77)]
GUEST_VISIT_SHARE = 0.10        # visits where the member sees a provider other than the home PCP
REPLACEMENT_SHARE = 0.02
VOID_SHARE = 0.01
DENIAL_SHARE = 0.03
PRODUCT_LINE = "Medicare Advantage"
TAXONOMY = "207Q00000X"
MINUTE_BANDS = g1.DOC_MINUTES   # typical minutes by level; also used to read time back to a level
TIME_PRESENT = 0.65             # share of visits where total time is recorded
LAB_IF_DATA_HIGH, LAB_IF_DATA_LOW = 0.90, 0.10
ELEMENT_NAMES = ["problems", "data", "risk"]


def _allowed():
    path = os.path.join(ROOT, "data", "baselines", "allowed_amounts_ga_fp.json")
    return {c: v["allowed_amount"] for c, v in json.load(open(path))["codes"].items()}


def _write_csv(path, rows, cols):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def build(out_dir, answer_key_path=DEFAULT_KEY, seed=42, n_providers=216, upcoder_rate=8 / 216, hard_neg_rate=8 / 216,
          clone_share=0.5, n_upcoders=None, n_hard_neg=None, data_version="2.0", clone_signal_strength=0.7):
    """Write plan tables and the records universe to out_dir; the answer key goes outside it.
    data_version "2.1" also writes the note package (docs/data_v2_1.md); claims and the universe stay identical to 2.0 for the same seed."""
    ng = notes_v21.NoteGen(seed, clone_signal_strength) if data_version == "2.1" else None
    if os.path.commonpath([os.path.abspath(out_dir), os.path.abspath(answer_key_path)]) == os.path.abspath(out_dir):
        raise ValueError("answer_key_path must be outside out_dir so agents reading the data cannot see it")
    os.makedirs(os.path.dirname(os.path.abspath(answer_key_path)), exist_ok=True)
    rng = np.random.default_rng(seed)
    mrng = np.random.default_rng([seed, 11])      # lines, remittance, replacements: its own stream
    rrng = np.random.default_rng([seed, 13])      # records universe: its own stream
    allowed = _allowed()
    n_up = n_upcoders if n_upcoders is not None else max(1, int(round(n_providers * upcoder_rate)))
    n_hn = n_hard_neg if n_hard_neg is not None else max(1, int(round(n_providers * hard_neg_rate)))
    n_normal = n_providers - n_up - n_hn
    roles = ["normal"] * n_normal + ["upcoder"] * n_up + ["hard_negative"] * n_hn
    rng.shuffle(roles)
    n_clone = int(round(clone_share * n_up))
    clone_flags = {}
    up_idx = [i for i, r in enumerate(roles) if r == "upcoder"]
    cloners = set(rng.choice(up_idx, size=n_clone, replace=False).tolist()) if n_clone else set()

    # ---- phase 1: providers and their member panels
    provs, members = [], []
    tin_pool = []
    for i, role in enumerate(roles):
        npi = f"1{(i + 1):09d}"
        volume = int(np.clip(rng.lognormal(np.log(g1.VOLUME_MEDIAN), g1.VOLUME_SIGMA), g1.VOLUME_MIN, g1.VOLUME_MAX))
        if role == "upcoder":
            volume = max(volume, 250)
        mult = g1.HARD_NEG_LAM_MULT if role == "hard_negative" else 1.0
        up = float(rng.uniform(*g1.UPCODER_FRACTION)) if role == "upcoder" else 0.0
        lam = g1.PARAMS["lam_mu"] * mult * np.exp(rng.normal(0, g1.PARAMS["lam_sigma"]))
        n_pat = max(20, int(volume / g1.VISITS_PER_PATIENT))
        chronic = np.minimum(rng.poisson(lam, size=n_pat), 8)
        eta = rng.normal(0, g1.PARAMS["eta_sigma"])
        top_shift = rng.normal(0, g1.PARAMS["top_sigma"])
        if not tin_pool or rng.random() < 0.35:
            tin_pool.append(f"{rng.integers(10 ** 8, 10 ** 9)}")
        provs.append({"npi": npi, "role": role, "volume": volume, "up": up, "eta": float(eta), "top_shift": float(top_shift),
                      "chronic": chronic, "tin": tin_pool[-1], "clones": i in cloners, "member_ids": []})
        base = len(members)
        for j, c in enumerate(chronic):
            order = rng.choice(len(g1.CONDITIONS), size=min(int(c), len(g1.CONDITIONS)), replace=False,
                               p=g1.CONDITION_WEIGHT / g1.CONDITION_WEIGHT.sum())
            age = int(np.clip(rng.normal(52 + 4 * (c - 1.5), 15), 18, 96))
            members.append({"member_id": f"M{len(members) + 1:07d}", "birth_year": 2024 - age,
                            "sex": "F" if rng.random() < 0.55 else "M", "pcp_npi": npi,
                            "_chronic": int(c), "_dx": [g1.CONDITIONS[k][1] for k in order]})
            provs[-1]["member_ids"].append(base + j)
        clone_flags[npi] = i in cloners

    weekdays = [date(2024, 1, 1) + timedelta(days=k) for k in range(366)
                if (date(2024, 1, 1) + timedelta(days=k)).weekday() < 5 and (date(2024, 1, 1) + timedelta(days=k)).year == 2024]
    W = len(weekdays)
    for m in members:
        if mrng.random() < 0.92:
            lo, hi = 0, W - 1
        else:                                     # partial-year coverage
            lo = int(mrng.integers(0, W // 2))
            hi = int(mrng.integers(lo + W // 4, W))
        m["_lo"], m["_hi"] = lo, min(hi, W - 1)
        m["coverage_start"], m["coverage_end"] = weekdays[m["_lo"]].isoformat(), weekdays[m["_hi"]].isoformat()
        m["product_line"] = PRODUCT_LINE

    # ---- phase 2: visits
    headers, lines, remit, universe, truth = [], [], [], [], {}
    cid = 0
    n_prov = len(provs)
    for pi, P in enumerate(provs):
        vol = P["volume"]
        guest = rng.random(vol) < GUEST_VISIT_SHARE
        home_idx = np.array(P["member_ids"])
        own_choice = rng.integers(0, len(home_idx), size=vol)
        other_prov = rng.integers(0, n_prov, size=vol)
        other_choice = rng.random(vol)
        mem_idx = np.empty(vol, dtype=int)
        for v in range(vol):
            if guest[v] and n_prov > 1:
                Q = provs[(pi + 1 + int(other_prov[v]) % (n_prov - 1)) % n_prov]    # never the same provider
                mem_idx[v] = Q["member_ids"][int(other_choice[v] * len(Q["member_ids"]))]
            else:
                mem_idx[v] = home_idx[own_choice[v]]
        true_chronic = np.array([members[k]["_chronic"] for k in mem_idx])
        just = g1.justified_levels(rng, true_chronic, P["eta"], g1.PARAMS, P["top_shift"])
        billed = just.copy()
        if P["up"] > 0:
            up = (rng.random(vol) < P["up"]) & (just >= 1)
            billed = np.where(up, np.minimum(just + 1, 4), just)
        for v in range(vol):
            m = members[mem_idx[v]]
            cid += 1
            claim_id = f"C{cid:07d}"
            dx = list(m["_dx"][:5])
            if mrng.random() < 0.45 or not dx:
                dx.append(g1.ACUTE_DX[int(mrng.integers(len(g1.ACUTE_DX)))][1])
            dx = dx[:6]
            date_ = weekdays[int(mrng.integers(m["_lo"], m["_hi"] + 1))]
            L, B = int(just[v]), int(billed[v])
            truth[claim_id] = CODES[L]

            # records universe: MDM elements, time, claim facts
            els = [L, L, L]
            odd = int(rrng.integers(0, 3))
            els[odd] = int(np.clip(L + int(rrng.choice([-2, -1, 1, 2])), 0, 4))
            data_true = els[1]
            els_true = list(els)
            lab = rrng.random() < (LAB_IF_DATA_HIGH if data_true >= 3 else LAB_IF_DATA_LOW)
            time_rec = rrng.random() < TIME_PRESENT
            tlevel = int(np.clip(L + int(rrng.choice([-1, 0, 1], p=[0.15, 0.7, 0.15])), 0, 4))
            if P["clones"] and B > L:                 # cloned documentation: inflate the note to the billed level
                els = [B, B, B]
                tlevel = B
            minutes = int(rrng.integers(MINUTE_BANDS[tlevel][0], MINUTE_BANDS[tlevel][1] + 1)) if time_rec else ""
            universe.append({"claim_id": claim_id, "problems_level": els[0], "data_level": els[1], "risk_level": els[2],
                             "documented_minutes": minutes})

            # claim header and lines (original claim)
            em_allowed = allowed[CODES[B]]
            headers.append({"claim_id": claim_id, "member_id": m["member_id"], "billing_npi": P["npi"],
                            "rendering_npi": P["npi"], "claim_frequency": 1, "original_claim_id": "",
                            "service_date": date_.isoformat(),
                            **{f"dx{k + 1}": (dx[k] if k < len(dx) else "") for k in range(6)}})
            mods = "25" if (lab and mrng.random() < 0.05) else ""
            line_rows = [{"claim_id": claim_id, "line_no": 1, "cpt": CODES[B], "modifiers": mods, "units": 1,
                          "place_of_service": "11", "dx_pointer": "1", "billed_amount": round(em_allowed * 2.5, 2),
                          "allowed_amount": em_allowed, "paid_amount": round(em_allowed * 0.8, 2)}]
            lab_code = None
            if lab:
                code, price = LAB_CODES[int(mrng.integers(len(LAB_CODES)))]
                lab_code = code
                line_rows.append({"claim_id": claim_id, "line_no": 2, "cpt": code, "modifiers": "", "units": 1,
                                  "place_of_service": "11", "dx_pointer": "1", "billed_amount": round(price * 2.5, 2),
                                  "allowed_amount": price, "paid_amount": round(price * 0.8, 2)})
            lines.extend(line_rows)
            if ng is not None:
                ng.add_visit(claim_id, None, m, P, L, B, els, els_true, minutes, tlevel, lab_code, date_, dx)
            total_paid = sum(r["paid_amount"] for r in line_rows)
            u = mrng.random()
            if u < DENIAL_SHARE:
                remit.append({"claim_id": claim_id, "status": "denied", "paid_amount": 0.0, "adjustment_amount": round(total_paid, 2),
                              "denial_reason": "CO-16 claim lacks information"})
            elif u < DENIAL_SHARE + REPLACEMENT_SHARE:        # original replaced by a corrected claim with the same content
                remit.append({"claim_id": claim_id, "status": "reversed", "paid_amount": 0.0, "adjustment_amount": round(total_paid, 2),
                              "denial_reason": "replaced"})
                cid += 1
                new_id = f"C{cid:07d}"
                headers.append({**headers[-1], "claim_id": new_id, "claim_frequency": 7, "original_claim_id": claim_id})
                for r in line_rows:
                    lines.append({**r, "claim_id": new_id})
                remit.append({"claim_id": new_id, "status": "paid", "paid_amount": round(total_paid, 2), "adjustment_amount": 0.0,
                              "denial_reason": ""})
            elif u < DENIAL_SHARE + REPLACEMENT_SHARE + VOID_SHARE:   # original voided
                remit.append({"claim_id": claim_id, "status": "reversed", "paid_amount": 0.0, "adjustment_amount": round(total_paid, 2),
                              "denial_reason": "voided"})
                cid += 1
                void_id = f"C{cid:07d}"
                headers.append({**headers[-1], "claim_id": void_id, "claim_frequency": 8, "original_claim_id": claim_id})
                remit.append({"claim_id": void_id, "status": "paid", "paid_amount": 0.0, "adjustment_amount": 0.0, "denial_reason": ""})
            else:
                remit.append({"claim_id": claim_id, "status": "paid", "paid_amount": round(total_paid, 2), "adjustment_amount": 0.0,
                              "denial_reason": ""})

    # ---- write
    pcols = ["npi", "taxonomy", "specialty", "state", "zip3", "group_tin", "network_status"]
    prov_rows = [{"npi": P["npi"], "taxonomy": TAXONOMY, "specialty": "Family Practice", "state": "GA",
                  "zip3": f"{300 + int(mrng.integers(0, 32))}", "group_tin": P["tin"],
                  "network_status": "in" if mrng.random() < 0.95 else "out"} for P in provs]
    _write_csv(os.path.join(out_dir, "providers.csv"), prov_rows, pcols)
    _write_csv(os.path.join(out_dir, "members.csv"), members,
               ["member_id", "birth_year", "sex", "coverage_start", "coverage_end", "product_line", "pcp_npi"])
    _write_csv(os.path.join(out_dir, "claims_header.csv"), headers,
               ["claim_id", "member_id", "billing_npi", "rendering_npi", "claim_frequency", "original_claim_id", "service_date",
                "dx1", "dx2", "dx3", "dx4", "dx5", "dx6"])
    _write_csv(os.path.join(out_dir, "claim_lines.csv"), lines,
               ["claim_id", "line_no", "cpt", "modifiers", "units", "place_of_service", "dx_pointer", "billed_amount",
                "allowed_amount", "paid_amount"])
    _write_csv(os.path.join(out_dir, "remittance.csv"), remit,
               ["claim_id", "status", "paid_amount", "adjustment_amount", "denial_reason"])
    _write_csv(os.path.join(out_dir, "reference", "fee_schedule.csv"),
               [{"cpt": c, "allowed_amount": a} for c, a in allowed.items()] + [{"cpt": c, "allowed_amount": p} for c, p in LAB_CODES],
               ["cpt", "allowed_amount"])
    _write_csv(os.path.join(out_dir, "reference", "place_of_service.csv"),
               [{"code": "11", "description": "Office"}], ["code", "description"])
    _write_csv(os.path.join(out_dir, "reference", "specialty_peer_groups.csv"),
               [{"specialty": "Family Practice", "peer_group": "GA Family Practice office-based"}], ["specialty", "peer_group"])
    _write_csv(os.path.join(out_dir, "records", "records_universe.csv"), universe,
               ["claim_id", "problems_level", "data_level", "risk_level", "documented_minutes"])
    if ng is not None:
        for name, rows, cols in (("visit_notes", ng.notes, notes_v21.NOTE_COLS), ("note_authentication", ng.auth, notes_v21.AUTH_COLS),
                                 ("note_orders", ng.orders, notes_v21.ORDER_COLS), ("note_results", ng.results, notes_v21.RESULT_COLS),
                                 ("audit_trail", ng.audit, notes_v21.AUDIT_COLS)):
            _write_csv(os.path.join(out_dir, "records", f"{name}.csv"), rows, cols)
    with open(answer_key_path, "w") as f:
        json.dump({"seed": seed, "clone_share": clone_share, "data_version": data_version,
                   **({"clone_signal_strength": clone_signal_strength, "cloned_visits": ng.cloned} if ng is not None else {}),
                   "providers": {P["npi"]: {"role": P["role"], "upgrade_fraction": round(P["up"], 3),
                                            "clones_notes": P["clones"],
                                            **({"uses_template": bool(ng.prov.get(P["npi"], {}).get("template"))} if ng is not None else {})}
                                   for P in provs},
                   "justified_cpt_by_claim": truth}, f)
    return prov_rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--providers", type=int, default=216)
    ap.add_argument("--upcoder-rate", type=float, default=8 / 216)
    ap.add_argument("--hard-neg-rate", type=float, default=8 / 216)
    ap.add_argument("--clone-share", type=float, default=0.5, help="share of upcoders whose documentation is cloned to match billing")
    ap.add_argument("--answer-key", default=DEFAULT_KEY)
    ap.add_argument("--data-version", default="2.0", choices=["2.0", "2.1"], help="2.1 also writes the note package")
    ap.add_argument("--clone-signal-strength", type=float, default=0.7, help="data 2.1: chance each clone signal appears on a cloned visit")
    a = ap.parse_args()
    out = build(a.out_dir, a.answer_key, a.seed, a.providers, a.upcoder_rate, a.hard_neg_rate, a.clone_share,
                data_version=a.data_version, clone_signal_strength=a.clone_signal_strength)
    print(f"wrote {len(out)} providers to {a.out_dir}; answer key at {a.answer_key}")
