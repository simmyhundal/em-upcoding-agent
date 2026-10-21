"""Data 4.0: provider upcoding rates and habits (issue 124; spec docs/v4_v5_plan.md, parameters and what is easier by construction docs/data_v4_0.md).

A separate module with its own random streams: generate_v2.py, generate_synthetic.py, notes_v21.py, records.py and defects_v22.py are not changed, so data 2.x reproduces exactly
(tests/test_generator_regression.py). `generate_v2.build(..., data_version="4.0")` hands over to `build` here; the tables, the records universe and the note package have the same
layout as data 2.2, so the frozen workflow v2.5 and agent v3.5 run on them unchanged.

What is new:
  * Every provider has a true NET upcoding rate (share of live visits billed above the justified level minus the share billed below).
  * Exactly 8 upcoders (n_upcoders), each with a net rate drawn from 17% to 38% (the 15 to 40% band with a 2-point buffer for denials and noise) and ONE habit:
      systematic     always bills 99214 for 99213-level visits (the provider's panel acuity is set so the share of such visits is its target rate);
      opportunistic  inflates only borderline visits (the ones closest below the next level's cutoff on the continuous complexity), pads the documented time just over
                     the cutoff and inflates the risk element on most upcoded notes;
      template       an EHR default bills 99214 on a share of visits at a lower level; notes share boilerplate but are written for the patient, the chart supports the true level.
    A small share of upcoders (clone_share, default 1 of 8) also clone notes (documented elements and time inflated to the bill, with the data 2.1 clone signals).
  * Non-upcoders have a mean net rate drawn between -15% and +15% (coding noise in both directions); hard negatives (honest high-acuity panels) are kept.
  * Each visit has a continuous complexity (the ordered-logit latent of data 1 and 2, so the calibrated code mix is unchanged) and the justified level is derived from it by the
    same thresholds; the MDM elements and the documented time are noisy readings of that complexity, so a reviewer reading the chart can land on either side of a borderline.
  * Realism: guest visits raised so patients are shared across providers, habit drift over the year (borderline and template selections skew later), time padding, risk inflation.
The answer key keeps a binary `role` (the planted upcoders) and adds the net rate, the habit, the chart-reading rates and the true overpayment dollars. It never reaches the view.
"""
import json
import os

import numpy as np

import defects_v22
import generate_synthetic as g1
import generate_v2 as g2
import notes_v21

CODES = g1.CODES
V40_DEFAULTS = {
    "habit_shares": {"systematic": 3 / 8, "opportunistic": 3 / 8, "template": 2 / 8},   # ASSUMPTION: no published breakdown of upcoding by mechanism was found
    "upcoder_rate_range": (0.18, 0.37),         # net rate of an upcoder (the 15 to 40% band less a 3-point buffer: realized rates stay within 2.5 points of the draw)
    "upcoder_noise": 0.04,                       # gross honest miscode rate of an upcoder's other visits (symmetric)
    "nonupcoder_mean_sd": 0.05, "nonupcoder_mean_max": 0.15,   # mean net rate of a non-upcoder ~ N(0, sd) clipped to +-max
    "honest_miscode_rate": 0.08, "honest_miscode_spread": 0.4, "honest_miscode_max": 0.25, "honest_miscode_floor": 0.02,
    "guest_visit_share": 0.25,                   # 2.2 uses 0.10; more shared patients
    "clone_share": 0.125, "clone_signal_strength": 0.7,
    "element_sd": 0.9, "time_sd": 1.1,           # logit-scale noise of the MDM elements and of the documented time around the visit's complexity
    "time_pad_prob": 0.8, "time_pad_over": 3,    # opportunistic: documented minutes just over the billed level's floor
    "risk_inflate_prob": 0.7,                    # opportunistic: the risk element documented at the billed level
    "drift": 1.0,                                # selection of borderline and template visits skews to later dates (0 = none)
    "template_default": 3,                       # the EHR default level (99214)
    "group_billing": True, "rendering_omitted_share": 0.3, "correction_level_change_share": 0.25, "correction_up_share": 0.4,
    "dx_cap": 0, "dx_cap_months": tuple(range(1, 13)),
    "defect_duplicate_share": 0.0, "defect_orphan_share": 0.0, "defect_unknown_member_share": 0.0, "defect_no_rendering_share": 0.0, "control_totals": True,
}
DENIAL, REPLACE, VOID = g2.DENIAL_SHARE, g2.REPLACEMENT_SHARE, g2.VOID_SHARE


def level_of(z, thresholds):
    return (np.asarray(z)[..., None] > thresholds).sum(axis=-1)


class NoteGen40(notes_v21.NoteGen):
    """The data 2.1 note generator with template-driven providers forced onto fixed templates (boilerplate shared across patients, patient-specific details kept)."""

    def __init__(self, seed, strength, force_template):
        super().__init__(seed, strength)
        self.force_template = set(force_template)

    def _state(self, npi, clones):
        fresh = npi not in self.prov
        st = super()._state(npi, clones)
        if fresh and npi in self.force_template:
            st["template"] = True
        return st


def _habit_counts(n_up, shares):
    names = list(shares)
    raw = np.array([shares[k] for k in names]) * n_up
    counts = np.floor(raw).astype(int)
    for i in np.argsort(-(raw - counts))[: n_up - counts.sum()]:
        counts[i] += 1
    return dict(zip(names, counts.tolist()))


def build(out_dir, answer_key_path=g2.DEFAULT_KEY, seed=42, n_providers=216, n_upcoders=8, n_hard_neg=8, **opts):
    """Write the data 4.0 tables, records universe and note package to out_dir and the answer key (outside it) to answer_key_path."""
    unknown = set(opts) - set(V40_DEFAULTS) - {"defect_profile", "upcoder_rate", "hard_neg_rate"} - {"clone_share"}
    if unknown:
        raise ValueError(f"unknown data 4.0 options: {sorted(unknown)}")
    profile = opts.pop("defect_profile", None)
    opts.pop("upcoder_rate", None)
    opts.pop("hard_neg_rate", None)
    cfg = {**V40_DEFAULTS, **(defects_v22.DEFECT_PROFILES[profile] if profile else {}), **opts}
    if os.path.commonpath([os.path.abspath(out_dir), os.path.abspath(answer_key_path)]) == os.path.abspath(out_dir):
        raise ValueError("answer_key_path must be outside out_dir so agents reading the data cannot see it")
    os.makedirs(os.path.dirname(os.path.abspath(answer_key_path)), exist_ok=True)
    R = lambda k: np.random.default_rng([seed, 40, k])          # own streams; nothing here consumes the data 2.x streams
    rng, prng, zrng, drng, orng, nrng, hrng, crng, mrng, rrng, grng = (R(k) for k in range(11))
    allowed = g2._allowed()
    t_base = np.array(g1.PARAMS["thresholds"], dtype=float)
    beta = g1.PARAMS["beta"]
    n_up, n_hn = n_upcoders, n_hard_neg
    n_normal = n_providers - n_up - n_hn
    roles = ["normal"] * n_normal + ["upcoder"] * n_up + ["hard_negative"] * n_hn
    rng.shuffle(roles)
    up_idx = [i for i, r in enumerate(roles) if r == "upcoder"]
    counts = _habit_counts(n_up, cfg["habit_shares"])
    habit_list = [h for h, c in counts.items() for _ in range(c)]
    rng.shuffle(habit_list)
    habit_of = dict(zip(up_idx, habit_list))
    n_clone = int(round(cfg["clone_share"] * n_up))
    clone_pool = [i for i in up_idx if habit_of[i] != "template"]
    cloners = set(rng.choice(clone_pool, size=min(n_clone, len(clone_pool)), replace=False).tolist()) if n_clone and clone_pool else set()
    force_template = []

    # ---- phase 1: providers and their member panels
    provs, members, tin_pool = [], [], []
    for i, role in enumerate(roles):
        npi = f"1{(i + 1):09d}"
        volume = int(np.clip(rng.lognormal(np.log(g1.VOLUME_MEDIAN), g1.VOLUME_SIGMA), g1.VOLUME_MIN, g1.VOLUME_MAX))
        if role == "upcoder":
            volume = max(volume, 250)
        mult = g1.HARD_NEG_LAM_MULT if role == "hard_negative" else 1.0
        lam = g1.PARAMS["lam_mu"] * mult * np.exp(rng.normal(0, g1.PARAMS["lam_sigma"]))
        n_pat = max(20, int(volume / g1.VISITS_PER_PATIENT))
        chronic = np.minimum(rng.poisson(lam, size=n_pat), 8)
        eta = rng.normal(0, g1.PARAMS["eta_sigma"])
        top_shift = rng.normal(0, g1.PARAMS["top_sigma"])
        if not tin_pool or rng.random() < 0.35:
            tin_pool.append(f"{rng.integers(10 ** 8, 10 ** 9)}")
        if role == "upcoder":
            target = float(prng.uniform(*cfg["upcoder_rate_range"]))
            mean_net, gross = 0.0, cfg["upcoder_noise"]
        else:
            target = None
            mean_net = float(np.clip(prng.normal(0, cfg["nonupcoder_mean_sd"]), -cfg["nonupcoder_mean_max"], cfg["nonupcoder_mean_max"]))
            gross = max(abs(mean_net) + cfg["honest_miscode_floor"], g2._beta_rate(prng, cfg["honest_miscode_rate"], cfg["honest_miscode_spread"], cfg["honest_miscode_max"]))
        habit = habit_of.get(i)
        if habit == "template":
            force_template.append(npi)
        provs.append({"npi": npi, "role": role, "volume": volume, "eta": float(eta), "top_shift": float(top_shift), "chronic": chronic, "tin": tin_pool[-1],
                      "clones": i in cloners, "member_ids": [], "habit": habit, "target": target, "mean_net": mean_net, "gross": gross})
        base = len(members)
        for j, c in enumerate(chronic):
            order = rng.choice(len(g1.CONDITIONS), size=min(int(c), len(g1.CONDITIONS)), replace=False, p=g1.CONDITION_WEIGHT / g1.CONDITION_WEIGHT.sum())
            age = int(np.clip(rng.normal(52 + 4 * (c - 1.5), 15), 18, 96))
            members.append({"member_id": f"M{len(members) + 1:07d}", "birth_year": 2024 - age, "sex": "F" if rng.random() < 0.55 else "M", "pcp_npi": npi,
                            "_chronic": int(c), "_dx": [g1.CONDITIONS[k][1] for k in order]})
            provs[-1]["member_ids"].append(base + j)
    ng = NoteGen40(seed, cfg["clone_signal_strength"], force_template)

    org_npi = {}
    if cfg["group_billing"]:
        size = {}
        for P in provs:
            size[P["tin"]] = size.get(P["tin"], 0) + 1
        for P in provs:
            if size[P["tin"]] >= 2:
                org_npi.setdefault(P["tin"], f"2{len(org_npi) + 1:09d}")
    for P in provs:
        P["billing"] = org_npi.get(P["tin"], P["npi"])

    from datetime import date, timedelta
    weekdays = [date(2024, 1, 1) + timedelta(days=k) for k in range(366)
                if (date(2024, 1, 1) + timedelta(days=k)).weekday() < 5 and (date(2024, 1, 1) + timedelta(days=k)).year == 2024]
    W = len(weekdays)
    for m in members:
        if mrng.random() < 0.92:
            lo, hi = 0, W - 1
        else:
            lo = int(mrng.integers(0, W // 2))
            hi = int(mrng.integers(lo + W // 4, W))
        m["_lo"], m["_hi"] = lo, min(hi, W - 1)
        m["coverage_start"], m["coverage_end"] = weekdays[m["_lo"]].isoformat(), weekdays[m["_hi"]].isoformat()
        m["product_line"] = g2.PRODUCT_LINE

    # ---- phase 2: visits
    headers, lines, remit, universe, truth = [], [], [], [], {}
    cid = 0
    dx_cut = 0
    n_prov = len(provs)
    seen_by = {}
    for pi, P in enumerate(provs):
        vol = P["volume"]
        t = t_base.copy()
        t[-1] += P["top_shift"]
        guest = grng.random(vol) < cfg["guest_visit_share"]
        home_idx = np.array(P["member_ids"])
        own_choice = grng.integers(0, len(home_idx), size=vol)
        other_prov = grng.integers(0, n_prov, size=vol)
        other_choice = grng.random(vol)
        mem_idx = np.empty(vol, dtype=int)
        for v in range(vol):
            if guest[v] and n_prov > 1:
                Q = provs[(pi + 1 + int(other_prov[v]) % (n_prov - 1)) % n_prov]
                mem_idx[v] = Q["member_ids"][int(other_choice[v] * len(Q["member_ids"]))]
            else:
                mem_idx[v] = home_idx[own_choice[v]]
        for k in set(mem_idx.tolist()):
            seen_by.setdefault(k, set()).add(P["npi"])
        true_chronic = np.array([members[k]["_chronic"] for k in mem_idx])
        z0 = beta * true_chronic + P["eta"] + zrng.logistic(size=vol)       # the continuous complexity of each visit
        d_idx = np.array([int(drng.integers(members[k]["_lo"], members[k]["_hi"] + 1)) for k in mem_idx])
        u_date = d_idx / max(W - 1, 1)
        out_u = orng.random(vol)
        accepted = ~((out_u < DENIAL) | ((out_u >= DENIAL + REPLACE) & (out_u < DENIAL + REPLACE + VOID)))     # paid (or replaced by a paid claim): what the view keeps
        n_acc = max(int(accepted.sum()), 1)

        shift = 0.0
        if P["role"] == "upcoder" and P["habit"] in ("systematic", "template"):
            # the provider's coding-style effect is set so the habit's eligible share of visits can reach the target (a legitimate panel property)
            best = (9.0, 0.0)
            for d in np.arange(-3.0, 3.01, 0.05):
                Ld = level_of(z0 + d, t)
                if P["habit"] == "systematic":
                    gap = abs(float(((Ld == 2) & accepted).sum()) / n_acc - P["target"])
                else:
                    elig = float(((Ld < cfg["template_default"]) & accepted).sum()) / n_acc
                    gap = max(0.0, P["target"] / 0.85 - elig) + 0.001 * abs(d)
                if gap < best[0] - 1e-12:
                    best = (gap, float(d))
            shift = best[1]
        z = z0 + shift
        just = level_of(z, t)
        billed = just.copy()
        selected = np.zeros(vol, dtype=bool)
        if P["role"] == "upcoder":
            if P["habit"] == "systematic":
                selected = (just == 2) & True
                billed = np.where(selected, 3, just)
            elif P["habit"] == "opportunistic":
                eligible = accepted & (just >= 1) & (just <= 3)
                gap = t[np.minimum(just, 3)] - z
                key = gap + 0.5 * cfg["drift"] * (1 - u_date)
                n_sel = int(round(P["target"] * n_acc))
                cand = np.flatnonzero(eligible)
                pick = cand[np.argsort(key[cand])[:n_sel]]
                selected[pick] = True
                billed = np.where(selected, np.minimum(just + 1, 4), just)
            else:
                eligible = accepted & (just < cfg["template_default"])
                n_sel = int(round(P["target"] * n_acc))
                cand = np.flatnonzero(eligible)
                w = 0.4 + 1.2 * cfg["drift"] * u_date[cand] if cfg["drift"] else np.ones(len(cand))
                if len(cand):
                    pick = hrng.choice(cand, size=min(n_sel, len(cand)), replace=False, p=w / w.sum())
                    selected[pick] = True
                billed = np.where(selected, cfg["template_default"], just)
        # honest coding noise (every provider; an upcoder's is symmetric)
        up_p, dn_p = (P["gross"] + P["mean_net"]) / 2, (P["gross"] - P["mean_net"]) / 2
        r_up, r_dn = nrng.random(vol), nrng.random(vol)
        free = ~selected & (billed == just)
        billed = np.where(free & (r_up < up_p) & (just < 4), just + 1, np.where(free & (r_up >= up_p) & (r_dn < dn_p) & (just > 0), just - 1, billed))
        upcoded = billed > just
        # corrections: replacement claims of honest providers can move the level (an upcoder's habit is left intact so its net rate is exactly its target)
        corr_ok = P["role"] != "upcoder"
        corr_chg = (crng.random(vol) < cfg["correction_level_change_share"]) if (corr_ok and cfg["correction_level_change_share"] > 0) else np.zeros(vol, dtype=bool)
        corr_up = crng.random(vol) < cfg["correction_up_share"]
        omit = (rrng.random(vol) < cfg["rendering_omitted_share"]) if (cfg["rendering_omitted_share"] > 0 and P["billing"] == P["npi"]) else np.zeros(vol, dtype=bool)
        final_b = billed.copy()
        P["n_corrections"], P["n_corr_up"], P["n_corr_down"] = 0, 0, 0
        elem_noise = rrng.normal(0, cfg["element_sd"], size=(vol, 3))
        time_noise = rrng.normal(0, cfg["time_sd"], size=vol)
        pad_u, risk_u = rrng.random(vol), rrng.random(vol)
        pad_off = rrng.integers(0, cfg["time_pad_over"], size=vol)
        for v in range(vol):
            m = members[mem_idx[v]]
            cid += 1
            claim_id = f"C{cid:07d}"
            dx = list(m["_dx"][:5])
            if mrng.random() < 0.45 or not dx:
                dx.append(g1.ACUTE_DX[int(mrng.integers(len(g1.ACUTE_DX)))][1])
            dx = dx[:6]
            date_ = weekdays[int(d_idx[v])]
            L, B = int(just[v]), int(billed[v])
            truth[claim_id] = CODES[L]
            # records universe: MDM elements and time are noisy readings of the visit's complexity (a borderline can read either way)
            els_true = [int(np.clip(level_of(z[v] + elem_noise[v, j], t), 0, 4)) for j in range(3)]
            els = list(els_true)
            data_true = els_true[1]
            lab = rrng.random() < (g2.LAB_IF_DATA_HIGH if data_true >= 3 else g2.LAB_IF_DATA_LOW)
            time_rec = rrng.random() < g2.TIME_PRESENT
            tlevel = int(np.clip(level_of(z[v] + time_noise[v], t), 0, 4))
            minutes = int(rrng.integers(g2.MINUTE_BANDS[tlevel][0], g2.MINUTE_BANDS[tlevel][1] + 1)) if time_rec else ""
            if P["clones"] and B > L:
                els, tlevel = [B, B, B], B
                minutes = int(rrng.integers(g2.MINUTE_BANDS[tlevel][0], g2.MINUTE_BANDS[tlevel][1] + 1)) if time_rec else ""
            elif P["habit"] == "opportunistic" and B > L:
                if time_rec and pad_u[v] < cfg["time_pad_prob"]:        # time padded just over the billed level's cutoff
                    tlevel = B
                    minutes = g2.MINUTE_BANDS[B][0] + int(pad_off[v])
                if risk_u[v] < cfg["risk_inflate_prob"]:                # "prescription drug management" on most upcoded notes
                    els[2] = max(els[2], B)
            universe.append({"claim_id": claim_id, "problems_level": els[0], "data_level": els[1], "risk_level": els[2], "documented_minutes": minutes})

            em_allowed = allowed[CODES[B]]
            dx_out = dx[:cfg["dx_cap"]] if (cfg["dx_cap"] and date_.month in cfg["dx_cap_months"]) else dx
            dx_cut += len(dx_out) < len(dx)
            headers.append({"claim_id": claim_id, "member_id": m["member_id"], "billing_npi": P["billing"], "rendering_npi": "" if omit[v] else P["npi"],
                            "claim_frequency": 1, "original_claim_id": "", "service_date": date_.isoformat(),
                            **{f"dx{k + 1}": (dx_out[k] if k < len(dx_out) else "") for k in range(6)}})
            mods = "25" if (lab and mrng.random() < 0.05) else ""
            line_rows = [{"claim_id": claim_id, "line_no": 1, "cpt": CODES[B], "modifiers": mods, "units": 1, "place_of_service": "11", "dx_pointer": "1",
                          "billed_amount": round(em_allowed * 2.5, 2), "allowed_amount": em_allowed, "paid_amount": round(em_allowed * 0.8, 2)}]
            lab_code = None
            if lab:
                code, price = g2.LAB_CODES[int(mrng.integers(len(g2.LAB_CODES)))]
                lab_code = code
                line_rows.append({"claim_id": claim_id, "line_no": 2, "cpt": code, "modifiers": "", "units": 1, "place_of_service": "11", "dx_pointer": "1",
                                  "billed_amount": round(price * 2.5, 2), "allowed_amount": price, "paid_amount": round(price * 0.8, 2)})
            lines.extend(line_rows)
            ng.add_visit(claim_id, None, m, P, L, B, els, els_true, minutes, tlevel, lab_code, date_, dx)
            total_paid = sum(r["paid_amount"] for r in line_rows)
            u = out_u[v]
            if u < DENIAL:
                remit.append({"claim_id": claim_id, "status": "denied", "paid_amount": 0.0, "adjustment_amount": round(total_paid, 2), "denial_reason": "CO-16 claim lacks information"})
            elif u < DENIAL + REPLACE:
                remit.append({"claim_id": claim_id, "status": "reversed", "paid_amount": 0.0, "adjustment_amount": round(total_paid, 2), "denial_reason": "replaced"})
                cid += 1
                new_id = f"C{cid:07d}"
                headers.append({**headers[-1], "claim_id": new_id, "claim_frequency": 7, "original_claim_id": claim_id})
                new_rows = [{**r, "claim_id": new_id} for r in line_rows]
                paid2 = total_paid
                if corr_chg[v]:
                    B2 = int(np.clip(B + (1 if corr_up[v] else -1), 0, 4))
                    if B2 == B:
                        B2 = int(np.clip(B - (1 if corr_up[v] else -1), 0, 4))
                    a2 = allowed[CODES[B2]]
                    new_rows[0].update({"cpt": CODES[B2], "billed_amount": round(a2 * 2.5, 2), "allowed_amount": a2, "paid_amount": round(a2 * 0.8, 2)})
                    paid2 = sum(r["paid_amount"] for r in new_rows)
                    final_b[v] = B2
                    P["n_corr_up"] += int(B2 > B)
                    P["n_corr_down"] += int(B2 < B)
                P["n_corrections"] += 1
                lines.extend(new_rows)
                remit.append({"claim_id": new_id, "status": "paid", "paid_amount": round(paid2, 2), "adjustment_amount": 0.0, "denial_reason": ""})
            elif u < DENIAL + REPLACE + VOID:
                remit.append({"claim_id": claim_id, "status": "reversed", "paid_amount": 0.0, "adjustment_amount": round(total_paid, 2), "denial_reason": "voided"})
                cid += 1
                void_id = f"C{cid:07d}"
                headers.append({**headers[-1], "claim_id": void_id, "claim_frequency": 8, "original_claim_id": claim_id})
                remit.append({"claim_id": void_id, "status": "paid", "paid_amount": 0.0, "adjustment_amount": 0.0, "denial_reason": ""})
            else:
                remit.append({"claim_id": claim_id, "status": "paid", "paid_amount": round(total_paid, 2), "adjustment_amount": 0.0, "denial_reason": ""})
        # rates of the live claims the view keeps (accepted visits), the basis score 4.0 measures
        P["n_acc"] = int(accepted.sum())
        P["live_up"] = int(((final_b > just) & accepted).sum())
        P["live_down"] = int(((final_b < just) & accepted).sum())
        P["live_over"] = 0.0
        P["live_over_gross"] = 0.0
        for k in np.flatnonzero(accepted):
            ov = (allowed[CODES[int(final_b[k])]] - allowed[CODES[int(just[k])]]) * 0.8
            P["live_over"] += ov
            P["live_over_gross"] += max(ov, 0.0)
        P["habit_visits"] = int((selected & accepted).sum())
        P["shift"] = shift

    ctotals, defect_rec = None, {}
    if cfg["control_totals"]:
        ctotals = defects_v22.control_totals(headers, remit)
    if any(cfg[k] for k in defects_v22.DEFECT_OPTIONS):
        defect_rec, cid = defects_v22.inject(headers, lines, remit, universe, truth, cfg, np.random.default_rng([seed, 40, 31]), cid)

    # ---- write (same files and columns as data 2.2)
    pcols = ["npi", "taxonomy", "specialty", "state", "zip3", "group_tin", "network_status"]
    prov_rows = [{"npi": P["npi"], "taxonomy": g2.TAXONOMY, "specialty": "Family Practice", "state": "GA", "zip3": f"{300 + int(mrng.integers(0, 32))}", "group_tin": P["tin"],
                  "network_status": "in" if mrng.random() < 0.95 else "out"} for P in provs]
    g2._write_csv(os.path.join(out_dir, "providers.csv"), prov_rows, pcols)
    g2._write_csv(os.path.join(out_dir, "members.csv"), members, ["member_id", "birth_year", "sex", "coverage_start", "coverage_end", "product_line", "pcp_npi"])
    g2._write_csv(os.path.join(out_dir, "claims_header.csv"), headers,
                  ["claim_id", "member_id", "billing_npi", "rendering_npi", "claim_frequency", "original_claim_id", "service_date", "dx1", "dx2", "dx3", "dx4", "dx5", "dx6"])
    g2._write_csv(os.path.join(out_dir, "claim_lines.csv"), lines,
                  ["claim_id", "line_no", "cpt", "modifiers", "units", "place_of_service", "dx_pointer", "billed_amount", "allowed_amount", "paid_amount"])
    g2._write_csv(os.path.join(out_dir, "remittance.csv"), remit, ["claim_id", "status", "paid_amount", "adjustment_amount", "denial_reason"])
    g2._write_csv(os.path.join(out_dir, "reference", "fee_schedule.csv"),
                  [{"cpt": c, "allowed_amount": a} for c, a in allowed.items()] + [{"cpt": c, "allowed_amount": p} for c, p in g2.LAB_CODES], ["cpt", "allowed_amount"])
    g2._write_csv(os.path.join(out_dir, "reference", "place_of_service.csv"), [{"code": "11", "description": "Office"}], ["code", "description"])
    g2._write_csv(os.path.join(out_dir, "reference", "specialty_peer_groups.csv"), [{"specialty": "Family Practice", "peer_group": "GA Family Practice office-based"}], ["specialty", "peer_group"])
    g2._write_csv(os.path.join(out_dir, "records", "records_universe.csv"), universe, ["claim_id", "problems_level", "data_level", "risk_level", "documented_minutes"])
    if ctotals is not None:
        defects_v22.write_control_totals(os.path.join(out_dir, "control_totals.csv"), ctotals)
    for name, rows, cols in (("visit_notes", ng.notes, notes_v21.NOTE_COLS), ("note_authentication", ng.auth, notes_v21.AUTH_COLS), ("note_orders", ng.orders, notes_v21.ORDER_COLS),
                             ("note_results", ng.results, notes_v21.RESULT_COLS), ("audit_trail", ng.audit, notes_v21.AUDIT_COLS)):
        g2._write_csv(os.path.join(out_dir, "records", f"{name}.csv"), rows, cols)

    honest = [P for P in provs if P["role"] != "upcoder"]
    for P in provs:
        P["up_rate"], P["down_rate"] = P["live_up"] / max(P["n_acc"], 1), P["live_down"] / max(P["n_acc"], 1)
    true_base = float(np.mean([P["up_rate"] for P in honest])) if honest else 0.0
    p95 = float(np.percentile([P["up_rate"] for P in honest], 95)) if honest else 0.0
    shared = sum(1 for s in seen_by.values() if len(s) >= 2) / max(len(seen_by), 1)
    with open(answer_key_path, "w") as f:
        json.dump({"seed": seed, "data_version": "4.0", "clone_share": cfg["clone_share"], "habit_counts": counts,
                   "honest_baseline_upcode_rate": round(true_base, 4), "honest_baseline_true_rate": round(true_base, 4), "honest_p95_true_rate": round(p95, 4),
                   "upcoder_definition": "planted", "upcoder_margin": None,
                   "defects": {**({"dx_truncation": {"cap": cfg["dx_cap"], "months": list(cfg["dx_cap_months"]), "claims_shortened": dx_cut}} if cfg["dx_cap"] else {}), **defect_rec,
                               **({"control_totals": {"file": "control_totals.csv", "months": len(ctotals)}} if ctotals is not None else {})},
                   "defect_profile": profile, "noise": {k: cfg[k] for k in ("honest_miscode_rate", "honest_miscode_spread", "honest_miscode_max", "upcoder_noise", "nonupcoder_mean_sd")},
                   "parameters": {k: (list(v) if isinstance(v, tuple) else v) for k, v in cfg.items() if k not in ("dx_cap_months",)},
                   "clone_signal_strength": cfg["clone_signal_strength"], "cloned_visits": ng.cloned, "members_seen_by_two_or_more_providers": round(shared, 4),
                   "providers": {P["npi"]: {"role": P["role"], "habit": P["habit"], "planted": P["role"], "subtle": False, "billing_npi": P["billing"], "group_tin": P["tin"],
                                            "clones_notes": P["clones"], "upgrade_fraction": round(P["target"] or 0.0, 3),
                                            "target_net_rate": None if P["target"] is None else round(P["target"], 4), "mean_net_rate": round(P["mean_net"], 4),
                                            "net_rate": round(P["up_rate"] - P["down_rate"], 4), "honest_miscode_rate": round(P["gross"], 4),
                                            "upcode_rate": round(P["up_rate"], 4), "true_upcode_rate": round(P["up_rate"], 4), "downcode_rate": round(P["down_rate"], 4),
                                            "true_overpay_net": round(P["live_over"], 2), "true_overpay_gross": round(P["live_over_gross"], 2),
                                            "above_margin": bool(P["role"] == "upcoder"), "above_p95": bool(P["up_rate"] > p95), "planted_below_line": False,
                                            "corrections": P["n_corrections"], "corrections_up": P["n_corr_up"], "corrections_down": P["n_corr_down"],
                                            "panel_acuity_shift": round(P["shift"], 2), "provider_effect": round(P["eta"] + P["shift"], 4), "top_shift": round(P["top_shift"], 4), "uses_template": bool(ng.prov.get(P["npi"], {}).get("template"))}
                                   for P in provs},
                   "justified_cpt_by_claim": truth}, f)
    return prov_rows
