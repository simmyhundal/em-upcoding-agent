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
import defects_v22
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


# Data 2.2 defaults (issue 74). Illustrative, not calibrated to a published coding-error rate; chosen on the development seed 42 for
# plausibility and for keeping honest noise below the upcoder margin (docs/data_v2_2.md). Frozen data versions never read these.
V22_DEFAULTS = {"honest_miscode_rate": 0.08, "honest_up_share": 0.5, "honest_miscode_spread": 0.4, "honest_miscode_max": 0.12,
                "upcoder_fraction": g1.UPCODER_FRACTION, "subtle_upcoder_share": 0.25, "subtle_upcoder_fraction": (0.08, 0.12),
                "upcoder_margin": 0.06, "upcoder_definition": "payer", "group_billing": True, "rendering_omitted_share": 0.3,
                "dx_cap": 0, "dx_cap_months": tuple(range(1, 13)),
                "correction_level_change_share": 0.25, "correction_up_share": 0.4,
                "defect_duplicate_share": 0.0, "defect_orphan_share": 0.0, "defect_unknown_member_share": 0.0, "defect_no_rendering_share": 0.0,
                "control_totals": True}


def _beta_rate(nrng, mean, cv, cap):
    """One provider's honest miscode rate: Beta with the given mean and coefficient of variation, capped. cv 0 gives the mean."""
    if mean <= 0:
        return 0.0
    if cv <= 0:
        return min(mean, cap)
    kappa = mean * (1 - mean) / ((cv * mean) ** 2) - 1
    kappa = max(kappa, 0.5)
    return float(min(nrng.beta(mean * kappa, (1 - mean) * kappa), cap))


def build(out_dir, answer_key_path=DEFAULT_KEY, seed=42, n_providers=216, upcoder_rate=8 / 216, hard_neg_rate=8 / 216,
          clone_share=None, n_upcoders=None, n_hard_neg=None, data_version="2.0", clone_signal_strength=0.7, **v22):
    """Write plan tables and the records universe to out_dir; the answer key goes outside it.
    data_version "2.1" also writes the note package (docs/data_v2_1.md); claims and the universe stay identical to 2.0 for the same seed.
    data_version "2.2" is 2.1 plus honest coding noise and an upcoder defined as above the honest baseline (docs/data_v2_2.md); keyword
    arguments override V22_DEFAULTS. With every noise parameter at zero a 2.2 build reproduces 2.1 claims and records exactly."""
    if data_version == "4.0":                     # data 4.0 (issue 124) lives in generate_v4.py and uses its own random streams; nothing below runs for it
        import generate_v4
        n_up_ = n_upcoders if n_upcoders is not None else max(1, int(round(n_providers * upcoder_rate)))
        n_hn_ = n_hard_neg if n_hard_neg is not None else max(1, int(round(n_providers * hard_neg_rate)))
        if clone_share is not None:               # left unset, data 4.0 uses its own default (1 cloner in 8, not data 2.x's 0.5)
            v22 = {**v22, "clone_share": clone_share}
        return generate_v4.build(out_dir, answer_key_path, seed=seed, n_providers=n_providers, n_upcoders=n_up_, n_hard_neg=n_hn_,
                                 clone_signal_strength=clone_signal_strength, **v22)
    if data_version == "4.2":                     # data 4.2 (issue 173) lives in generate_v42.py: no planted upcoders, so n_upcoders and n_hard_neg are ignored
        import generate_v42
        if clone_share is not None:
            v22 = {**v22, "clone_share": clone_share}
        return generate_v42.build(out_dir, answer_key_path, seed=seed, n_providers=n_providers, clone_signal_strength=clone_signal_strength, **v22)
    if data_version == "4.3":                     # data 4.3 (issue 197) lives in generate_v43.py: no planted upcoders, so n_upcoders and n_hard_neg are ignored (docs/data_v4_3.md)
        import generate_v43
        if clone_share is not None:
            v22 = {**v22, "clone_share": clone_share}
        return generate_v43.build(out_dir, answer_key_path, seed=seed, n_providers=n_providers, clone_signal_strength=clone_signal_strength, **v22)
    if clone_share is None:
        clone_share = 0.5                         # the data 2.x default, unchanged
    v22_on = data_version == "2.2"
    unknown = set(v22) - set(V22_DEFAULTS) - {"defect_profile"}
    if unknown or (v22 and not v22_on):
        raise ValueError(f"unknown or data-2.2-only options: {sorted(v22)}")
    profile = v22.pop("defect_profile", None)
    if profile is not None and profile not in defects_v22.DEFECT_PROFILES:
        raise ValueError(f"defect_profile must be one of {sorted(defects_v22.DEFECT_PROFILES)}")
    cfg = {**V22_DEFAULTS, **(defects_v22.DEFECT_PROFILES[profile] if profile else {}), **v22}
    nrng = np.random.default_rng([seed, 19])      # data 2.2 only: honest coding noise and subtle-upcoder choice; its own stream
    crng = np.random.default_rng([seed, 29])      # data 2.2 only: which replacement claims change the level and in which direction
    orng = np.random.default_rng([seed, 23])      # data 2.2 only: which claims leave the rendering NPI blank; its own stream, so toggling it moves nothing else
    ng = notes_v21.NoteGen(seed, clone_signal_strength) if data_version in ("2.1", "2.2") else None
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
    subtle = set()
    if v22_on and cfg["subtle_upcoder_share"] > 0 and up_idx:
        subtle = set(nrng.choice(up_idx, size=int(round(cfg["subtle_upcoder_share"] * len(up_idx))), replace=False).tolist())

    # ---- phase 1: providers and their member panels
    provs, members = [], []
    tin_pool = []
    for i, role in enumerate(roles):
        npi = f"1{(i + 1):09d}"
        volume = int(np.clip(rng.lognormal(np.log(g1.VOLUME_MEDIAN), g1.VOLUME_SIGMA), g1.VOLUME_MIN, g1.VOLUME_MAX))
        if role == "upcoder":
            volume = max(volume, 250)
        mult = g1.HARD_NEG_LAM_MULT if role == "hard_negative" else 1.0
        frac_range = (cfg["subtle_upcoder_fraction"] if i in subtle else cfg["upcoder_fraction"]) if v22_on else g1.UPCODER_FRACTION
        up = float(rng.uniform(*frac_range)) if role == "upcoder" else 0.0
        lam = g1.PARAMS["lam_mu"] * mult * np.exp(rng.normal(0, g1.PARAMS["lam_sigma"]))
        n_pat = max(20, int(volume / g1.VISITS_PER_PATIENT))
        chronic = np.minimum(rng.poisson(lam, size=n_pat), 8)
        eta = rng.normal(0, g1.PARAMS["eta_sigma"])
        top_shift = rng.normal(0, g1.PARAMS["top_sigma"])
        if not tin_pool or rng.random() < 0.35:
            tin_pool.append(f"{rng.integers(10 ** 8, 10 ** 9)}")
        provs.append({"npi": npi, "role": role, "volume": volume, "up": up, "eta": float(eta), "top_shift": float(top_shift),
                      "chronic": chronic, "tin": tin_pool[-1], "clones": i in cloners, "member_ids": [], "subtle": i in subtle,
                      "miscode": _beta_rate(nrng, cfg["honest_miscode_rate"], cfg["honest_miscode_spread"], cfg["honest_miscode_max"]) if v22_on else 0.0})
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

    # data 2.2: a group billing for several clinicians bills under an organizational NPI (starts with 2); the clinician stays the rendering provider
    org_npi = {}
    if v22_on and cfg["group_billing"]:
        size = {}
        for P in provs:
            size[P["tin"]] = size.get(P["tin"], 0) + 1
        for P in provs:
            if size[P["tin"]] >= 2:
                org_npi.setdefault(P["tin"], f"2{len(org_npi) + 1:09d}")
    for P in provs:
        P["billing"] = org_npi.get(P["tin"], P["npi"])

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
    dx_cut = 0                                   # data 2.2: claims whose delivered diagnosis list was shortened by --dx-cap
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
        if v22_on and P["miscode"] > 0:           # honest coding noise on visits not deliberately upgraded
            slip = (nrng.random(vol) < P["miscode"]) & (billed == just)
            goes_up = nrng.random(vol) < cfg["honest_up_share"]
            billed = np.where(slip & goes_up & (just < 4), just + 1, np.where(slip & ~goes_up & (just > 0), just - 1, billed))
        P["n_up_visits"], P["n_down_visits"] = int((billed > just).sum()), int((billed < just).sum())
        if v22_on:      # the provider's true propensity to bill above the justified level: its parameters over its visit mix, not one year's draw
            f_, ru = P["up"], P["miscode"] * cfg["honest_up_share"]
            P["true_up"] = float(np.where(just == 0, ru, np.where(just <= 3, f_ + (1 - f_) * ru, 0.0)).mean())
        # data 2.2: a clinician billing under their own NPI often leaves the rendering field blank (it equals billing)
        omit = (orng.random(vol) < cfg["rendering_omitted_share"]) if (v22_on and cfg["rendering_omitted_share"] > 0 and P["billing"] == P["npi"]) \
            else np.zeros(vol, dtype=bool)
        corr_chg = (crng.random(vol) < cfg["correction_level_change_share"]) if v22_on and cfg["correction_level_change_share"] > 0 else np.zeros(vol, dtype=bool)
        corr_up = crng.random(vol) < cfg["correction_up_share"] if v22_on and cfg["correction_level_change_share"] > 0 else np.zeros(vol, dtype=bool)
        final_b = billed.copy()                    # the level of the live claim for each visit (a correction can change it)
        P["n_corrections"], P["n_corr_up"], P["n_corr_down"] = 0, 0, 0
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
            dx_out = dx[:cfg["dx_cap"]] if (v22_on and cfg["dx_cap"] and date_.month in cfg["dx_cap_months"]) else dx   # the extract keeps fewer
            dx_cut += len(dx_out) < len(dx)
            headers.append({"claim_id": claim_id, "member_id": m["member_id"], "billing_npi": P["billing"],
                            "rendering_npi": "" if omit[v] else P["npi"], "claim_frequency": 1, "original_claim_id": "",
                            "service_date": date_.isoformat(),
                            **{f"dx{k + 1}": (dx_out[k] if k < len(dx_out) else "") for k in range(6)}})
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
                new_rows = [{**r, "claim_id": new_id} for r in line_rows]
                paid2 = total_paid
                if corr_chg[v]:                           # data 2.2: the corrected claim moves the E/M level by one
                    B2 = int(np.clip(B + (1 if corr_up[v] else -1), 0, 4))
                    if B2 == B:                           # at the edge of the range: go the other way instead
                        B2 = int(np.clip(B - (1 if corr_up[v] else -1), 0, 4))
                    a2 = allowed[CODES[B2]]
                    new_rows[0].update({"cpt": CODES[B2], "billed_amount": round(a2 * 2.5, 2), "allowed_amount": a2, "paid_amount": round(a2 * 0.8, 2)})
                    paid2 = sum(r["paid_amount"] for r in new_rows)
                    final_b[v] = B2
                    P["n_corr_up"] += int(B2 > B)
                    P["n_corr_down"] += int(B2 < B)
                P["n_corrections"] += 1
                lines.extend(new_rows)
                remit.append({"claim_id": new_id, "status": "paid", "paid_amount": round(paid2, 2), "adjustment_amount": 0.0,
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

        if v22_on:                                    # rates are of the live claims, so a downward correction counts for the provider
            P["n_up_visits"], P["n_down_visits"] = int((final_b > just).sum()), int((final_b < just).sum())

    # ---- data 2.2: control totals of the clean extract, then the delivered-extract defects (issue 80)
    ctotals, defect_rec = None, {}
    if v22_on:
        if cfg["control_totals"]:
            ctotals = defects_v22.control_totals(headers, remit)
        if any(cfg[k] for k in defects_v22.DEFECT_OPTIONS):
            defect_rec, cid = defects_v22.inject(headers, lines, remit, universe, truth, cfg, np.random.default_rng([seed, 31]), cid)

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
    if ctotals is not None:
        defects_v22.write_control_totals(os.path.join(out_dir, "control_totals.csv"), ctotals)
    if ng is not None:
        for name, rows, cols in (("visit_notes", ng.notes, notes_v21.NOTE_COLS), ("note_authentication", ng.auth, notes_v21.AUTH_COLS),
                                 ("note_orders", ng.orders, notes_v21.ORDER_COLS), ("note_results", ng.results, notes_v21.RESULT_COLS),
                                 ("audit_trail", ng.audit, notes_v21.AUDIT_COLS)):
            _write_csv(os.path.join(out_dir, "records", f"{name}.csv"), rows, cols)
    v22_key = {}
    if v22_on:
        honest = [P for P in provs if P["role"] != "upcoder"]
        baseline = sum(P["n_up_visits"] / P["volume"] for P in honest) / len(honest) if honest else 0.0
        for P in provs:
            P["up_rate"], P["down_rate"] = P["n_up_visits"] / P["volume"], P["n_down_visits"] / P["volume"]
            P["planted"] = P["role"]
        # The two tests use each provider's TRUE propensity (true_upcode_rate), not the share of one year's visits that happened to be billed high: small
        # practices otherwise cross the line by luck (a first version of this definition labeled 11 honest doctors upcoders on 8 seeds).
        # The realised rates stay in the key for the screens' side of the story.
        honest_true = [P["true_up"] for P in provs if P["planted"] != "upcoder"]
        true_base = float(np.mean(honest_true)) if honest_true else 0.0
        p95 = float(np.percentile(honest_true, 95)) if honest_true else 0.0
        if cfg["upcoder_definition"] not in ("payer", "margin"):
            raise ValueError("upcoder_definition must be payer or margin")
        for P in provs:
            # role by the stated definition (issue 74, docs/data_v2_2.md). margin: true rate above the honest mean by at least the margin.
            # payer: that AND above the 95th percentile of the honest providers' true rates (a peer-percentile outlier a payer's screen would call,
            # confirmed as material by a sample review).
            P["above_margin"] = P["true_up"] - true_base >= cfg["upcoder_margin"]
            P["above_p95"] = P["true_up"] > p95
            is_up = P["above_margin"] and (P["above_p95"] or cfg["upcoder_definition"] == "margin")
            P["role"] = "upcoder" if is_up else ("hard_negative" if P["planted"] == "hard_negative" else "normal")
        v22_key = {"honest_baseline_upcode_rate": round(baseline, 4), "honest_baseline_true_rate": round(true_base, 4), "honest_p95_true_rate": round(p95, 4), "upcoder_margin": cfg["upcoder_margin"],
                   "upcoder_definition": cfg["upcoder_definition"],
                   "defects": {**({"dx_truncation": {"cap": cfg["dx_cap"], "months": list(cfg["dx_cap_months"]), "claims_shortened": dx_cut}}
                                  if cfg["dx_cap"] else {}), **defect_rec,
                               **({"control_totals": {"file": "control_totals.csv", "months": len(ctotals)}} if ctotals is not None else {})},
                   "defect_profile": profile, "noise": {k: cfg[k] for k in ("honest_miscode_rate", "honest_up_share", "honest_miscode_spread", "honest_miscode_max",
                                                 "subtle_upcoder_share")}}
    with open(answer_key_path, "w") as f:
        json.dump({"seed": seed, "clone_share": clone_share, "data_version": data_version, **v22_key,
                   **({"clone_signal_strength": clone_signal_strength, "cloned_visits": ng.cloned} if ng is not None else {}),
                   "providers": {P["npi"]: {"role": P["role"], "upgrade_fraction": round(P["up"], 3),
                                            **({"billing_npi": P["billing"], "group_tin": P["tin"]} if v22_on else {}),
                                            "clones_notes": P["clones"],
                                            **({"planted": P["planted"], "subtle": P["subtle"], "honest_miscode_rate": round(P["miscode"], 4),
                                                "upcode_rate": round(P["up_rate"], 4), "true_upcode_rate": round(P["true_up"], 4), "downcode_rate": round(P["down_rate"], 4),
                                                "above_margin": bool(P["above_margin"]), "above_p95": bool(P["above_p95"]),
                                                "planted_below_line": bool(P["planted"] == "upcoder" and P["role"] != "upcoder"),
                                                "corrections": P["n_corrections"], "corrections_up": P["n_corr_up"], "corrections_down": P["n_corr_down"]} if v22_on else {}),
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
    ap.add_argument("--clone-share", type=float, default=None, help="share of upcoders whose documentation is cloned to match billing (data 2.x default 0.5; data 4.0 default 0.125)")
    ap.add_argument("--answer-key", default=DEFAULT_KEY)
    ap.add_argument("--data-version", default="2.0", choices=["2.0", "2.1", "2.2", "4.0", "4.2", "4.3"],
                    help="2.1 also writes the note package; 2.2 adds honest coding noise; 4.0 provider upcoding rates and habits (generate_v4.py); 4.2 no planted role (generate_v42.py); 4.3 docs/data_v4_3.md")
    ap.add_argument("--clone-signal-strength", type=float, default=0.7, help="data 2.1: chance each clone signal appears on a cloned visit")
    g = ap.add_argument_group("data 2.2 (issue 74); defaults in V22_DEFAULTS")
    g.add_argument("--honest-miscode-rate", type=float, help="mean share of an honest provider's visits billed off the justified level")
    g.add_argument("--honest-up-share", type=float, help="share of those miscodes that go up (the rest go down)")
    g.add_argument("--honest-miscode-spread", type=float, help="provider-to-provider coefficient of variation of the miscode rate (Beta)")
    g.add_argument("--honest-miscode-max", type=float, help="cap on any provider's honest miscode rate")
    g.add_argument("--upcoder-fraction", type=float, nargs=2, metavar=("LO", "HI"), help="range of visits an upcoder bills one level up")
    g.add_argument("--subtle-upcoder-share", type=float, help="share of upcoders drawn from the subtle range instead")
    g.add_argument("--subtle-upcoder-fraction", type=float, nargs=2, metavar=("LO", "HI"), help="the subtle range")
    g.add_argument("--upcoder-definition", choices=["payer", "margin"], help="payer (default): above the honest 95th percentile AND at least the margin above the honest mean; margin: the second test alone")
    g.add_argument("--upcoder-margin", type=float, help="an upcoder's upcoding rate exceeds the honest baseline by at least this")
    g.add_argument("--dx-cap", type=int, help="keep only the first N diagnosis positions in the delivered extract (the claim had more); 0 = off")
    g.add_argument("--dx-cap-months", type=int, nargs="+", help="service months (1 to 12) the cap applies to; default all")
    g.add_argument("--correction-level-change-share", type=float, help="share of replacement (corrected) claims that change the E/M level by one")
    g.add_argument("--correction-up-share", type=float, help="share of level-changing corrections that go up (the rest go down)")
    g.add_argument("--defect-profile", choices=sorted(defects_v22.DEFECT_PROFILES), help="named set of defect shares (explicit --defect-* options override it)")
    g.add_argument("--defect-duplicate-share", type=float, help="issue 80: share of paid claims delivered twice under a new claim id")
    g.add_argument("--defect-orphan-share", type=float, help="issue 80: share of replacements and voids whose original is missing from the extract")
    g.add_argument("--defect-unknown-member-share", type=float, help="issue 80: share of claims whose member id does not join to eligibility")
    g.add_argument("--defect-no-rendering-share", type=float, help="issue 80: share of group-billed claims with the rendering NPI blank")
    g.add_argument("--control-totals", action=argparse.BooleanOptionalAction, default=None, help="write control_totals.csv (claims and paid dollars by month)")
    g.add_argument("--group-billing", action=argparse.BooleanOptionalAction, default=None,
                   help="groups of 2 or more clinicians bill under an organizational NPI (the clinician stays the rendering provider)")
    g.add_argument("--rendering-omitted-share", type=float, help="share of single-clinician claims with the rendering NPI left blank (it equals billing)")
    g43 = ap.add_argument_group("data 4.3 (issue 197; docs/data_v4_3.md)")
    g43.add_argument("--holdout-family", action="append", dest="holdout_families", help="data 4.3: switch off one mechanism family (repeatable; names in docs/data_v4_3.md)")
    g43.add_argument("--years", type=int, help="data 4.3: length of the date range in calendar years (default 1)")
    a = ap.parse_args()
    opts = {k: (tuple(v) if isinstance(v, list) else v) for k, v in vars(a).items()
            if (k in V22_DEFAULTS or k == "defect_profile") and v is not None}
    if a.data_version == "4.3":
        opts.update({k: (tuple(v) if isinstance(v, list) else v) for k, v in (("holdout_families", a.holdout_families), ("years", a.years)) if v is not None})
    elif a.holdout_families or a.years:
        ap.error("--holdout-family and --years are data 4.3 options")
    out = build(a.out_dir, a.answer_key, a.seed, a.providers, a.upcoder_rate, a.hard_neg_rate, a.clone_share,
                data_version=a.data_version, clone_signal_strength=a.clone_signal_strength, **opts)
    print(f"wrote {len(out)} providers to {a.out_dir}; answer key at {a.answer_key}")
