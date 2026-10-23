"""Data 4.2: a continuous truth for upcoding and for other fraud, waste and abuse (issue 173; spec docs/data_v4_2.md).

A sibling of generate_v4.py with its own random streams ([seed, 42, k]); generate_v2.py, generate_v4.py and the other generators are not changed, so data 2.x and data 4.0 reproduce byte for byte
(tests/test_generator_regression.py and tests/test_d40_regression.py). The tables, the records universe and the note package keep the data 4.0 layout.

What is new against data 4.0:
  * NO planted role. Every provider draws a true net rate from a mixture: a core near zero with noise in both directions (94.2%) and a heavy right tail (5.8%) whose members have a habit
    (systematic, opportunistic, template-driven) chosen by the rate, not by a quota. The number of providers above any line varies by dataset.
  * Fraud, waste and abuse beyond the level, drawn independently of the rate: services billed but not rendered (phantom claims no chart exists for), impossible visits per day (extra claims
    dated one day), unbundling (an extra separately paid line with modifier 25 on the E/M line). Each has its own true overpayment in dollars.
  * The answer key is continuous and eval-only (net rate, dollars by kind, intent flags, habit) and has no `role`, `planted` or other binary label.
  * `records/unrendered_claims.csv` (simulator side, read only by office version 4.2 and the old control sample) lists the claims no chart can be produced for.
"""
import csv
import json
import os

import numpy as np

import defects_v22
import generate_synthetic as g1
import generate_v2 as g2
import generate_v4 as g4
import notes_v21

CODES = g1.CODES
V42_DEFAULTS = {
    # --- the rate distribution (docs/data_v4_2.md, a)
    "tail_share": 0.058, "tail_floor": 0.06, "tail_median": 0.12, "tail_sigma": 0.8, "tail_cap": 0.45,
    "low_habit_shares": {"opportunistic": 0.6, "template": 0.4}, "high_habit_shares": {"systematic": 3 / 8, "opportunistic": 3 / 8, "template": 2 / 8}, "high_rate": 0.15,
    "hard_neg_share": 8 / 216,
    # --- fraud, waste and abuse beyond the level (docs/data_v4_2.md, b)
    "nr_prob": 0.03, "nr_share": (0.04, 0.15), "ghost_share": 0.08, "nr_min": 3,
    "imp_prob": 0.015, "imp_days": (2, 6), "imp_visits": (32, 50),
    "unb_prob": 0.02, "unb_share": (0.15, 0.50),
}
for _k in ("upcoder_noise", "nonupcoder_mean_sd", "nonupcoder_mean_max", "honest_miscode_rate", "honest_miscode_spread", "honest_miscode_max", "honest_miscode_floor", "guest_visit_share",
           "clone_share", "clone_signal_strength", "element_sd", "time_sd", "time_pad_prob", "time_pad_over", "risk_inflate_prob", "drift", "template_default", "group_billing",
           "rendering_omitted_share", "correction_level_change_share", "correction_up_share", "dx_cap", "dx_cap_months", "defect_duplicate_share", "defect_orphan_share",
           "defect_unknown_member_share", "defect_no_rendering_share", "control_totals"):
    V42_DEFAULTS[_k] = g4.V40_DEFAULTS[_k]
DENIAL, REPLACE, VOID = g2.DENIAL_SHARE, g2.REPLACEMENT_SHARE, g2.VOID_SHARE
level_of = g4.level_of
FWA_KINDS = ("not_rendered", "impossible_days", "unbundling")


def _pick_habit(u, rate, cfg):
    """The habit of a tail provider: chosen by its rate (docs/data_v4_2.md, a), from one uniform draw u."""
    shares = cfg["high_habit_shares"] if rate >= cfg["high_rate"] else cfg["low_habit_shares"]
    names = list(shares)
    p = np.array([shares[k] for k in names], dtype=float)
    return names[min(int(np.searchsorted(np.cumsum(p / p.sum()), u, side="right")), len(names) - 1)]


def build(out_dir, answer_key_path=g2.DEFAULT_KEY, seed=42, n_providers=216, **opts):
    """Write the data 4.2 tables, records universe and note package to out_dir and the answer key (outside it) to answer_key_path."""
    unknown = set(opts) - set(V42_DEFAULTS) - {"defect_profile"}
    if unknown:
        raise ValueError(f"unknown data 4.2 options: {sorted(unknown)}")
    profile = opts.pop("defect_profile", None)
    cfg = {**V42_DEFAULTS, **(defects_v22.DEFECT_PROFILES[profile] if profile else {}), **opts}
    if os.path.commonpath([os.path.abspath(out_dir), os.path.abspath(answer_key_path)]) == os.path.abspath(out_dir):
        raise ValueError("answer_key_path must be outside out_dir so agents reading the data cannot see it")
    os.makedirs(os.path.dirname(os.path.abspath(answer_key_path)), exist_ok=True)
    R = lambda k: np.random.default_rng([seed, 42, k])          # own streams; nothing here consumes the data 2.x or data 4.0 streams
    rng, prng, zrng, drng, orng, nrng, hrng, crng, mrng, rrng, grng, arng, frng, urng = (R(k) for k in range(14))
    allowed = g2._allowed()
    t_base = np.array(g1.PARAMS["thresholds"], dtype=float)
    beta = g1.PARAMS["beta"]

    # ---- phase 0: what each provider is (a rate from the mixture, a habit by rate, FWA kinds); fixed number of draws per provider
    attrs = []
    for i in range(n_providers):
        a = {}
        a["hard_neg"] = bool(arng.random() < cfg["hard_neg_share"])
        a["tail"] = bool(arng.random() < cfg["tail_share"])
        z_rate, u_habit, u_clone = arng.normal(), arng.random(), arng.random()
        a["rate"] = float(min(cfg["tail_floor"] + np.exp(np.log(cfg["tail_median"]) + cfg["tail_sigma"] * z_rate), cfg["tail_cap"])) if a["tail"] else None
        a["habit"] = _pick_habit(u_habit, a["rate"], cfg) if a["tail"] else None
        a["clones"] = bool(a["tail"] and a["habit"] != "template" and u_clone < cfg["clone_share"])
        fw = {}
        for kind, prob in (("nr", cfg["nr_prob"]), ("imp", cfg["imp_prob"]), ("unb", cfg["unb_prob"])):
            fw[kind] = bool(arng.random() < prob)
        fw["nr_share"] = float(arng.uniform(*cfg["nr_share"]))
        fw["imp_days"] = int(arng.integers(cfg["imp_days"][0], cfg["imp_days"][1] + 1))
        fw["unb_share"] = float(arng.uniform(*cfg["unb_share"]))
        a["fwa"] = fw
        attrs.append(a)
    force_template = []

    # ---- phase 1: providers and their member panels
    provs, members, tin_pool = [], [], []
    for i, a in enumerate(attrs):
        npi = f"1{(i + 1):09d}"
        volume = int(np.clip(rng.lognormal(np.log(g1.VOLUME_MEDIAN), g1.VOLUME_SIGMA), g1.VOLUME_MIN, g1.VOLUME_MAX))      # no volume floor tied to the rate
        mult = g1.HARD_NEG_LAM_MULT if a["hard_neg"] else 1.0
        lam = g1.PARAMS["lam_mu"] * mult * np.exp(rng.normal(0, g1.PARAMS["lam_sigma"]))
        n_pat = max(20, int(volume / g1.VISITS_PER_PATIENT))
        chronic = np.minimum(rng.poisson(lam, size=n_pat), 8)
        eta = rng.normal(0, g1.PARAMS["eta_sigma"])
        top_shift = rng.normal(0, g1.PARAMS["top_sigma"])
        if not tin_pool or rng.random() < 0.35:
            tin_pool.append(f"{rng.integers(10 ** 8, 10 ** 9)}")
        if a["tail"]:
            target = a["rate"]
            mean_net, gross = 0.0, cfg["upcoder_noise"]
        else:
            target = None
            mean_net = float(np.clip(prng.normal(0, cfg["nonupcoder_mean_sd"]), -cfg["nonupcoder_mean_max"], cfg["nonupcoder_mean_max"]))
            gross = max(abs(mean_net) + cfg["honest_miscode_floor"], g2._beta_rate(prng, cfg["honest_miscode_rate"], cfg["honest_miscode_spread"], cfg["honest_miscode_max"]))
        if a["habit"] == "template":
            force_template.append(npi)
        provs.append({"npi": npi, "volume": volume, "eta": float(eta), "top_shift": float(top_shift), "chronic": chronic, "tin": tin_pool[-1], "clones": a["clones"], "member_ids": [],
                      "habit": a["habit"], "target": target, "mean_net": mean_net, "gross": gross, "hard_neg": a["hard_neg"], "fwa": a["fwa"]})
        base = len(members)
        for j, c in enumerate(chronic):
            order = rng.choice(len(g1.CONDITIONS), size=min(int(c), len(g1.CONDITIONS)), replace=False, p=g1.CONDITION_WEIGHT / g1.CONDITION_WEIGHT.sum())
            age = int(np.clip(rng.normal(52 + 4 * (c - 1.5), 15), 18, 96))
            members.append({"member_id": f"M{len(members) + 1:07d}", "birth_year": 2024 - age, "sex": "F" if rng.random() < 0.55 else "M", "pcp_npi": npi,
                            "_chronic": int(c), "_dx": [g1.CONDITIONS[k][1] for k in order]})
            provs[-1]["member_ids"].append(base + j)
    ng = g4.NoteGen40(seed, cfg["clone_signal_strength"], force_template)

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
    fraud_claims = {}                        # claim_id -> kind of every phantom claim (no chart can be produced)
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

        # phantom claims: services billed but not rendered (on a few ghost members) and impossible visits per day (extra claims dated one day)
        f_mem, f_d, f_kind = [], [], []
        fw = P["fwa"]
        if fw["nr"]:
            n_nr = max(cfg["nr_min"], int(round(fw["nr_share"] * vol)))
            ghosts = frng.choice(home_idx, size=min(max(3, int(round(cfg["ghost_share"] * len(home_idx)))), len(home_idx)), replace=False)
            used = set()                                     # one phantom claim per member and date: a repeat of the same member, date and service would read as a duplicate claim (a defect of the extract)
            for _ in range(n_nr):
                for _try in range(20):
                    k = int(ghosts[int(frng.integers(len(ghosts)))])
                    d_ = int(frng.integers(members[k]["_lo"], members[k]["_hi"] + 1))
                    if (k, d_) not in used:
                        break
                used.add((k, d_))
                f_mem.append(k)
                f_d.append(d_)
                f_kind.append("not_rendered")
        if fw["imp"]:
            for day in frng.choice(W, size=min(fw["imp_days"], W), replace=False):
                cover = [int(k) for k in home_idx if members[int(k)]["_lo"] <= day <= members[int(k)]["_hi"]] or [int(k) for k in home_idx]
                n_day = int(frng.integers(cfg["imp_visits"][0], cfg["imp_visits"][1] + 1))
                order = frng.permutation(len(cover))
                for j in range(n_day):                       # distinct members within a day while the panel allows it (no duplicate claims)
                    f_mem.append(cover[int(order[j % len(order)])])
                    f_d.append(int(day))
                    f_kind.append("impossible_days")
        nf = len(f_mem)
        n_tot = vol + nf
        all_mem = np.concatenate([mem_idx, np.array(f_mem, dtype=int)]) if nf else mem_idx
        true_chronic = np.array([members[k]["_chronic"] for k in all_mem])
        z0_all = beta * true_chronic + P["eta"] + zrng.logistic(size=n_tot)     # the continuous complexity of each visit
        z0 = z0_all[:vol]
        d_idx = np.array([int(drng.integers(members[k]["_lo"], members[k]["_hi"] + 1)) for k in mem_idx])
        u_date = d_idx / max(W - 1, 1)
        out_u = orng.random(vol)
        accepted = ~((out_u < DENIAL) | ((out_u >= DENIAL + REPLACE) & (out_u < DENIAL + REPLACE + VOID)))     # paid (or replaced by a paid claim): what the view keeps
        n_acc = max(int(accepted.sum()), 1)

        shift = 0.0
        if P["habit"] in ("systematic", "template"):
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
        elif P["habit"] == "template":
            eligible = accepted & (just < cfg["template_default"])
            n_sel = int(round(P["target"] * n_acc))
            cand = np.flatnonzero(eligible)
            w = 0.4 + 1.2 * cfg["drift"] * u_date[cand] if cfg["drift"] else np.ones(len(cand))
            if len(cand):
                pick = hrng.choice(cand, size=min(n_sel, len(cand)), replace=False, p=w / w.sum())
                selected[pick] = True
            billed = np.where(selected, cfg["template_default"], just)
        # honest coding noise (every provider; a habit provider's is symmetric)
        up_p, dn_p = (P["gross"] + P["mean_net"]) / 2, (P["gross"] - P["mean_net"]) / 2
        r_up, r_dn = nrng.random(vol), nrng.random(vol)
        free = ~selected & (billed == just)
        billed = np.where(free & (r_up < up_p) & (just < 4), just + 1, np.where(free & (r_up >= up_p) & (r_dn < dn_p) & (just > 0), just - 1, billed))
        # corrections: replacement claims of honest providers can move the level (a habit provider's habit is left intact so its net rate stays at its draw)
        corr_ok = P["habit"] is None
        corr_chg = (crng.random(vol) < cfg["correction_level_change_share"]) if (corr_ok and cfg["correction_level_change_share"] > 0) else np.zeros(vol, dtype=bool)
        corr_up = crng.random(vol) < cfg["correction_up_share"]
        omit = (rrng.random(n_tot) < cfg["rendering_omitted_share"]) if (cfg["rendering_omitted_share"] > 0 and P["billing"] == P["npi"]) else np.zeros(n_tot, dtype=bool)
        final_b = billed.copy()
        # phantom claims: billed at the justified level of their (imagined) complexity, always paid
        if nf:
            just_all = np.concatenate([just, level_of(z0_all[vol:], t)])
            billed_all = np.concatenate([billed, just_all[vol:]])
            out_u_all = np.concatenate([out_u, np.full(nf, 0.5)])
            d_all = np.concatenate([d_idx, np.array(f_d, dtype=int)])
        else:
            just_all, billed_all, out_u_all, d_all = just, billed, out_u, d_idx
        unb_on = np.zeros(n_tot, dtype=bool)
        if fw["unb"]:
            unb_on[:vol] = urng.random(vol) < fw["unb_share"]
        P["n_corrections"], P["n_corr_up"], P["n_corr_down"] = 0, 0, 0
        elem_noise = rrng.normal(0, cfg["element_sd"], size=(n_tot, 3))
        time_noise = rrng.normal(0, cfg["time_sd"], size=n_tot)
        pad_u, risk_u = rrng.random(n_tot), rrng.random(n_tot)
        pad_off = rrng.integers(0, cfg["time_pad_over"], size=n_tot)
        fwa_over = {"not_rendered": 0.0, "impossible_days": 0.0, "unbundling": 0.0}
        fwa_n = {"not_rendered": 0, "impossible_days": 0, "unbundling": 0}
        for v in range(n_tot):
            is_f = v >= vol
            m = members[all_mem[v]]
            cid += 1
            claim_id = f"C{cid:07d}"
            dx = list(m["_dx"][:5])
            if mrng.random() < 0.45 or not dx:
                dx.append(g1.ACUTE_DX[int(mrng.integers(len(g1.ACUTE_DX)))][1])
            dx = dx[:6]
            date_ = weekdays[int(d_all[v])]
            L, B = int(just_all[v]), int(billed_all[v])
            truth[claim_id] = CODES[B] if is_f else CODES[L]       # a phantom claim is justified at its billed level: its overpayment is in the FWA dollars, not in the level difference
            if is_f:
                fraud_claims[claim_id] = f_kind[v - vol]
            # records universe: MDM elements and time are noisy readings of the visit's complexity (a borderline can read either way)
            els_true = [int(np.clip(level_of(z0_all[v] + (shift if not is_f else 0.0) + elem_noise[v, j], t), 0, 4)) for j in range(3)]
            els = list(els_true)
            data_true = els_true[1]
            lab = rrng.random() < (g2.LAB_IF_DATA_HIGH if data_true >= 3 else g2.LAB_IF_DATA_LOW)
            time_rec = rrng.random() < g2.TIME_PRESENT
            tlevel = int(np.clip(level_of(z0_all[v] + (shift if not is_f else 0.0) + time_noise[v], t), 0, 4))
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
            mods = "25" if ((lab and mrng.random() < 0.05) or unb_on[v]) else ""
            line_rows = [{"claim_id": claim_id, "line_no": 1, "cpt": CODES[B], "modifiers": mods, "units": 1, "place_of_service": "11", "dx_pointer": "1",
                          "billed_amount": round(em_allowed * 2.5, 2), "allowed_amount": em_allowed, "paid_amount": round(em_allowed * 0.8, 2)}]
            lab_code = None
            if lab:
                code, price = g2.LAB_CODES[int(mrng.integers(len(g2.LAB_CODES)))]
                lab_code = code
                line_rows.append({"claim_id": claim_id, "line_no": 2, "cpt": code, "modifiers": "", "units": 1, "place_of_service": "11", "dx_pointer": "1",
                                  "billed_amount": round(price * 2.5, 2), "allowed_amount": price, "paid_amount": round(price * 0.8, 2)})
            unb_paid = 0.0
            if unb_on[v]:                                               # unbundling: an extra separately paid line (a repeat of the lab line, or a lab line the visit did not need)
                code, price = (lab_code, dict(g2.LAB_CODES)[lab_code]) if lab_code else g2.LAB_CODES[int(urng.integers(len(g2.LAB_CODES)))]
                line_rows.append({"claim_id": claim_id, "line_no": len(line_rows) + 1, "cpt": code, "modifiers": "", "units": 1, "place_of_service": "11", "dx_pointer": "1",
                                  "billed_amount": round(price * 2.5, 2), "allowed_amount": price, "paid_amount": round(price * 0.8, 2)})
                unb_paid = round(price * 0.8, 2)
            lines.extend(line_rows)
            ng.add_visit(claim_id, None, m, P, L, B, els, els_true, minutes, tlevel, lab_code, date_, dx)
            total_paid = sum(r["paid_amount"] for r in line_rows)
            u = out_u_all[v]
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
            if is_f:                               # the whole paid claim is an overpayment (always paid: out_u = 0.5)
                fwa_over[f_kind[v - vol]] += round(total_paid, 2)
                fwa_n[f_kind[v - vol]] += 1
            elif unb_paid and (u >= DENIAL + REPLACE + VOID or DENIAL <= u < DENIAL + REPLACE):
                fwa_over["unbundling"] += unb_paid
                fwa_n["unbundling"] += 1
        # level rates of the live claims the view keeps (accepted normal visits), the basis score 4.0 measures
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
        P["fwa_over"], P["fwa_n"], P["n_phantom"] = fwa_over, fwa_n, nf

    ctotals, defect_rec = None, {}
    if cfg["control_totals"]:
        ctotals = defects_v22.control_totals(headers, remit)
    if any(cfg[k] for k in defects_v22.DEFECT_OPTIONS):
        defect_rec, cid = defects_v22.inject(headers, lines, remit, universe, truth, cfg, np.random.default_rng([seed, 42, 31]), cid)

    # ---- write (same files and columns as data 2.2 and 4.0, plus the simulator-side list of claims no chart exists for)
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
    g2._write_csv(os.path.join(out_dir, "records", "unrendered_claims.csv"), [{"claim_id": c} for c in sorted(fraud_claims)], ["claim_id"])
    if ctotals is not None:
        defects_v22.write_control_totals(os.path.join(out_dir, "control_totals.csv"), ctotals)
    for name, rows, cols in (("visit_notes", ng.notes, notes_v21.NOTE_COLS), ("note_authentication", ng.auth, notes_v21.AUTH_COLS), ("note_orders", ng.orders, notes_v21.ORDER_COLS),
                             ("note_results", ng.results, notes_v21.RESULT_COLS), ("audit_trail", ng.audit, notes_v21.AUDIT_COLS)):
        g2._write_csv(os.path.join(out_dir, "records", f"{name}.csv"), rows, cols)

    for P in provs:
        P["up_rate"], P["down_rate"] = P["live_up"] / max(P["n_acc"], 1), P["live_down"] / max(P["n_acc"], 1)
    shared = sum(1 for s in seen_by.values() if len(s) >= 2) / max(len(seen_by), 1)
    providers_key = {}
    for P in provs:
        fo, fn, fw = P["fwa_over"], P["fwa_n"], P["fwa"]
        fwa_total = round(sum(fo.values()), 2)
        providers_key[P["npi"]] = {
            "habit": P["habit"], "uses_template": bool(ng.prov.get(P["npi"], {}).get("template")), "clones_notes": P["clones"],
            "intent": {"level_upcoding": P["habit"] in ("systematic", "opportunistic"), "cloned_notes": P["clones"], "not_rendered": bool(fw["nr"]),
                       "impossible_days": bool(fw["imp"]), "unbundling": bool(fw["unb"])},
            "target_net_rate": None if P["target"] is None else round(P["target"], 4), "mean_net_rate": round(P["mean_net"], 4),
            "net_rate": round(P["up_rate"] - P["down_rate"], 4), "up_rate": round(P["up_rate"], 4), "down_rate": round(P["down_rate"], 4), "honest_miscode_rate": round(P["gross"], 4),
            "true_overpay_level_net": round(P["live_over"], 2), "true_overpay_level_gross": round(P["live_over_gross"], 2),
            "true_overpay_fwa": {k: round(v, 2) for k, v in fo.items()}, "fwa_claims": dict(fn), "n_phantom_claims": P["n_phantom"],
            "true_overpay_total": round(max(P["live_over"], 0.0) + fwa_total, 2),
            "high_acuity_panel": P["hard_neg"], "volume": P["volume"], "billing_npi": P["billing"], "group_tin": P["tin"],
            "corrections": P["n_corrections"], "corrections_up": P["n_corr_up"], "corrections_down": P["n_corr_down"],
            "panel_acuity_shift": round(P["shift"], 2), "provider_effect": round(P["eta"] + P["shift"], 4), "top_shift": round(P["top_shift"], 4)}
    with open(answer_key_path, "w") as f:
        json.dump({"seed": seed, "data_version": "4.2", "clone_share": cfg["clone_share"],
                   "defects": {**({"dx_truncation": {"cap": cfg["dx_cap"], "months": list(cfg["dx_cap_months"]), "claims_shortened": dx_cut}} if cfg["dx_cap"] else {}), **defect_rec,
                               **({"control_totals": {"file": "control_totals.csv", "months": len(ctotals)}} if ctotals is not None else {})},
                   "defect_profile": profile,
                   "parameters": {k: (list(v) if isinstance(v, tuple) else v) for k, v in cfg.items() if k not in ("dx_cap_months",)},
                   "clone_signal_strength": cfg["clone_signal_strength"], "cloned_visits": ng.cloned, "members_seen_by_two_or_more_providers": round(shared, 4),
                   "fraud_claims": fraud_claims, "providers": providers_key, "justified_cpt_by_claim": truth}, f)
    return prov_rows
