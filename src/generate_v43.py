"""Data 4.3: a messier volume signal, structured chart variability, office realism and the data 4.2 calibration (issues 197, 220, 201, 137, 144).

SEALED until the release 4.3 test is done (docs/process.md, "Sealed data design"): the mechanisms and parameters are described in docs/sealed/data_v43_design.md; the public data card is docs/data_v4_3.md.

A sibling of generate_v42.py with its own random streams ([seed, 43, k] by default); generate_v2.py, generate_v4.py, generate_v42.py, notes_v21.py and the other generators are not changed, so data 2.x, 4.0 and 4.2
reproduce byte for byte (tests/test_generator_regression.py, tests/test_d40_regression.py, tests/test_d42_regression.py). With every data 4.3 option at its "off" setting (OFF_43) and the 4.2 stream
family (stream_family=42, a test-only switch) a 4.3 build writes the same data files as a 4.2 build (tests/test_data_v43.py).

What is new against data 4.2 (details in the sealed design page):
  * legitimate high volume: mid-level visits billed under a physician's number, coverage for an absent colleague, compressed clinic schedules, quick-visit clinic days, and service dates batched by
    a billing error (some corrected later by a replacement claim);
  * suspicious volume that overlaps the honest tail: spike days and phantom visits padded onto many ordinary days, beside data 4.2's ghost-member panel;
  * claims-based confounders: diagnosis inflation and sparse diagnosis coding;
  * the lab or test line calibrated: a weaker link to the true complexity, practices without an in-house lab (the test is ordered in the note but not on the claim), unneeded tests on upcoded visits;
  * per-provider time recording, recalibrated habit shares, an optional multi-year range with drift;
  * chart variability: contradictory or missing elements, rounded or ranged time, late signatures and addenda, honest template boilerplate and stale copied-forward problems;
  * office realism (simulator-side files read by office version 4.3): charts fabricated for visits that never happened (instead of an automatic "no record"), signatures added when a request
    arrives, notes that change between two answers, coder disagreement that depends on the case, and response behaviour profiles per practice;
  * mechanism families that can be switched off one by one (`holdout_families`), so a whole family can be kept out of development and used for a held-out test.
"""
import csv  # noqa: F401  (kept for parity with the 4.2 module's imports)
import hashlib
import json
import os
from datetime import date, timedelta

import numpy as np

import defects_v22
import generate_synthetic as g1
import generate_v2 as g2
import generate_v4 as g4
import generate_v42 as g42
import notes_v21

CODES = g1.CODES
level_of = g4.level_of
DENIAL, REPLACE, VOID = g2.DENIAL_SHARE, g2.REPLACEMENT_SHARE, g2.VOID_SHARE
FWA_KINDS = ("not_rendered", "impossible_days", "unbundling")
BEHAVIORS = ("cooperative", "slow", "sloppy", "evasive")

# ---- defaults: the full realism set (values and their reasons: docs/sealed/data_v43_design.md)
V43_DEFAULTS = {
    **g42.V42_DEFAULTS,
    # calibration (issues 137 and 144)
    "high_habit_shares": {"systematic": 0.30, "opportunistic": 0.45, "template": 0.25}, "low_habit_shares": {"opportunistic": 0.65, "template": 0.35},
    "time_recorded_mean": 0.65, "time_recorded_kappa": 6.0,          # per-provider share of visits with total time recorded ~ Beta(mean, kappa); kappa 0 = the flat 4.2 share
    "test_link": 0.5,                                                 # 1.0 = the data 4.2 lab line (driven by the true data element only)
    "lab_rate_mean": 0.30, "lab_rate_kappa": 5.0,                     # provider test propensity for the part of the lab line not driven by the true data element
    "in_house_lab_share": 0.70,                                       # 1.0 = every practice bills its tests on the visit's claim
    "unneeded_test_prob": 0.35, "unneeded_test_share": (0.3, 0.8),    # share of systematic or opportunistic providers that add a test to upcoded visits, and how often
    "years": 1,                                                       # length of the date range in calendar years (volume scales with it)
    # legitimate high volume (issue 197)
    "shared_npi_prob": 0.08, "shared_npi_share": (0.25, 0.75),
    "coverage_prob": 0.06, "coverage_days": (5, 15),
    "compressed_prob": 0.15, "compressed_days": (2, 3), "compressed_max_per_day": 26,
    "quick_day_prob": 0.10, "quick_days": (1, 4), "quick_visits": (10, 32),
    "batch_prob": 0.05, "batch_days": (1, 3), "batch_window": 8, "batch_take": 0.6, "batch_correct_share": 0.5,
    # suspicious volume overlapping the honest tail (issue 197); nr_* (ghost panel) and unb_* (unbundling) come from data 4.2
    "nr_prob": 0.025, "nr_share": (0.03, 0.10), "ghost_share": 0.15,
    "imp_prob": 0.02, "imp_days": (3, 10), "imp_visits": (8, 26),
    "pad_prob": 0.025, "pad_days": (20, 70), "pad_per_day": (1, 4),
    # charts for visits that never happened (issues 220 and 201)
    "fabricate_prob": 0.5, "fabricate_share": (0.6, 1.0), "fabricate_late_round": 0.4,
    # claims-based confounders (issue 197)
    "dx_inflate_prob_habit": 0.30, "dx_inflate_prob_other": 0.02, "dx_inflate_share": (0.3, 0.7),
    "sparse_dx_prob": 0.12,
    # chart variability (issue 220)
    "contradict_share": 0.08, "missing_element_share": 0.03, "time_round_share": 0.35, "time_range_share": 0.08, "stale_copy_share": 0.10,
    "boilerplate_share": 0.5,
    "late_sign_share": 0.04, "addendum_share_honest": 0.03, "addendum_share_habit": 0.10, "addendum_share_fabricated": 0.25,
    "sign_on_request_honest": 0.30, "sign_on_request_habit": 0.45, "sign_on_request_fabricated": 0.70,
    "amend_on_release_honest": 0.10, "amend_on_release_habit": 0.50, "amend_on_release_fabricated": 0.60,
    "coder_case": True, "coder_base": 0.05, "coder_borderline": 0.28, "coder_scale": 0.6, "coder_thin": 0.05, "coder_contradiction": 0.10, "coder_max": 0.45,
    # office response profiles (issue 201)
    "office_profiles": True, "office_group_share": 0.7,
    # held-out mechanism families (issue 197)
    "holdout_families": (),
    # test-only: the random-stream family (43 = data 4.3's own streams; 42 = data 4.2's, used only to check that 4.3 with every option off equals 4.2)
    "stream_family": 43,
}

# every data 4.3 option at its "off" setting: what data 4.2 does
OFF_43 = {
    "high_habit_shares": g42.V42_DEFAULTS["high_habit_shares"], "low_habit_shares": g42.V42_DEFAULTS["low_habit_shares"],
    "time_recorded_kappa": 0.0, "time_recorded_mean": g2.TIME_PRESENT, "test_link": 1.0, "in_house_lab_share": 1.0, "unneeded_test_prob": 0.0, "years": 1,
    "shared_npi_prob": 0.0, "coverage_prob": 0.0, "compressed_prob": 0.0, "quick_day_prob": 0.0, "batch_prob": 0.0,
    "nr_prob": g42.V42_DEFAULTS["nr_prob"], "nr_share": g42.V42_DEFAULTS["nr_share"], "ghost_share": g42.V42_DEFAULTS["ghost_share"],
    "imp_prob": g42.V42_DEFAULTS["imp_prob"], "imp_days": g42.V42_DEFAULTS["imp_days"], "imp_visits": g42.V42_DEFAULTS["imp_visits"],
    "pad_prob": 0.0, "fabricate_prob": 0.0, "dx_inflate_prob_habit": 0.0, "dx_inflate_prob_other": 0.0, "sparse_dx_prob": 0.0,
    "contradict_share": 0.0, "missing_element_share": 0.0, "time_round_share": 0.0, "time_range_share": 0.0, "stale_copy_share": 0.0, "boilerplate_share": 0.0,
    "late_sign_share": 0.0, "addendum_share_honest": 0.0, "addendum_share_habit": 0.0, "addendum_share_fabricated": 0.0,
    "sign_on_request_honest": 0.0, "sign_on_request_habit": 0.0, "sign_on_request_fabricated": 0.0,
    "amend_on_release_honest": 0.0, "amend_on_release_habit": 0.0, "amend_on_release_fabricated": 0.0,
    "coder_case": False, "office_profiles": False,
}

# mechanism families and the options that switch each one off (holdout_families)
FAMILIES = {
    "shared_npi": {"shared_npi_prob": 0.0},
    "coverage": {"coverage_prob": 0.0},
    "compressed_schedule": {"compressed_prob": 0.0},
    "quick_visit_days": {"quick_day_prob": 0.0},
    "date_batching": {"batch_prob": 0.0},
    "ghost_panel": {"nr_prob": 0.0},
    "spike_days": {"imp_prob": 0.0},
    "padded_days": {"pad_prob": 0.0},
    "unbundling": {"unb_prob": 0.0},
    "fabricated_charts": {"fabricate_prob": 0.0},
    "diagnosis_inflation": {"dx_inflate_prob_habit": 0.0, "dx_inflate_prob_other": 0.0},
    "sparse_diagnoses": {"sparse_dx_prob": 0.0},
    "lab_realism": {"test_link": 1.0, "in_house_lab_share": 1.0},
    "unneeded_tests": {"unneeded_test_prob": 0.0},
    "chart_variability": {"contradict_share": 0.0, "missing_element_share": 0.0, "time_round_share": 0.0, "time_range_share": 0.0, "stale_copy_share": 0.0},
    "template_boilerplate": {"boilerplate_share": 0.0},
    "late_amended": {"late_sign_share": 0.0, "addendum_share_honest": 0.0, "addendum_share_habit": 0.0, "addendum_share_fabricated": 0.0,
                     "sign_on_request_honest": 0.0, "sign_on_request_habit": 0.0, "sign_on_request_fabricated": 0.0,
                     "amend_on_release_honest": 0.0, "amend_on_release_habit": 0.0, "amend_on_release_fabricated": 0.0},
    "case_coder_disagreement": {"coder_case": False},
    "office_profiles": {"office_profiles": False},
}
FLAT_CODER = 0.15                       # records.CODER_NOISE: the flat disagreement of offices 2.x and 4.2
INFLATE_CODES = [code for _, code in g1.CONDITIONS]
INFLATE_W = np.array([1.0, 3.0, 0.5, 3.0, 3.0, 3.0, 2.0, 1.0, 1.0, 1.5, 0.5, 2.0])     # risk-heavy conditions are the ones added
BOILERPLATE = "Medication reconciliation completed; risks, benefits and alternatives of the plan discussed."
ADDENDUM = " Addendum: assessment clarified after review of the visit."
PLAN_COLS = ["claim_id", "available_from_round", "coder_disagreement", "signs_on_request", "release_levels"]


class NoteGen43(g4.NoteGen40):
    """The data 4.0 note generator on data 4.3's own note stream (data 4.2 and 2.1 notes use [seed, 17])."""

    def __init__(self, seed, strength, force_template, stream_family=43):
        super().__init__(seed, strength, force_template)
        if stream_family != 42:
            self.rng = np.random.default_rng([seed, stream_family, 17])


def _shares_pick(u, shares):
    names = list(shares)
    p = np.array([shares[k] for k in names], dtype=float)
    return names[min(int(np.searchsorted(np.cumsum(p / p.sum()), u, side="right")), len(names) - 1)]


def _beta(rng_u, mean, kappa):
    """A Beta(mean, kappa) draw from a generator (always draws, so toggling kappa never shifts the stream)."""
    a, b = max(mean * max(kappa, 1e-6), 1e-3), max((1 - mean) * max(kappa, 1e-6), 1e-3)
    x = float(rng_u.beta(a, b))
    return x if kappa > 0 else float(mean)


def config(opts):
    """The full configuration of a build: defaults, then a defect profile, then explicit options, then the held-out families switched off."""
    unknown = set(opts) - set(V43_DEFAULTS) - {"defect_profile"}
    if unknown:
        raise ValueError(f"unknown data 4.3 options: {sorted(unknown)}")
    opts = dict(opts)
    profile = opts.pop("defect_profile", None)
    cfg = {**V43_DEFAULTS, **(defects_v22.DEFECT_PROFILES[profile] if profile else {}), **opts}
    bad = set(cfg["holdout_families"]) - set(FAMILIES)
    if bad:
        raise ValueError(f"unknown mechanism families: {sorted(bad)}; known: {sorted(FAMILIES)}")
    for fam in cfg["holdout_families"]:
        cfg.update(FAMILIES[fam])
    return cfg, profile


def config_hash(cfg):
    blob = json.dumps({k: (list(v) if isinstance(v, tuple) else v) for k, v in sorted(cfg.items())}, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()[:16]


def build(out_dir, answer_key_path=g2.DEFAULT_KEY, seed=42, n_providers=216, **opts):
    """Write the data 4.3 tables, records universe, note package and simulator-side office files to out_dir and the answer key (outside it) to answer_key_path."""
    cfg, profile = config(opts)
    if os.path.commonpath([os.path.abspath(out_dir), os.path.abspath(answer_key_path)]) == os.path.abspath(out_dir):
        raise ValueError("answer_key_path must be outside out_dir so agents reading the data cannot see it")
    os.makedirs(os.path.dirname(os.path.abspath(answer_key_path)), exist_ok=True)
    SF = int(cfg["stream_family"])
    R = lambda k: np.random.default_rng([seed, SF, k])
    rng, prng, zrng, drng, orng, nrng, hrng, crng, mrng, rrng, grng, arng, frng, urng = (R(k) for k in range(14))     # the data 4.2 roles, on this family
    brng = R(50)          # new per-provider attributes (a fixed number of draws per provider)
    vrng = R(51)          # chart variability (post-processing of the universe and the note package)
    xrng = R(52)          # diagnosis confounders
    erng = R(53)          # extra rendered visits (coverage, quick-visit days) and date batching
    pdrng = R(54)         # padded phantom visits and fabrication choices
    lrng = R(55)          # lab line, unneeded tests, coder disagreement plan
    qrng = R(56)          # office profiles and coverage pairs
    allowed = g2._allowed()
    t_base = np.array(g1.PARAMS["thresholds"], dtype=float)
    beta = g1.PARAMS["beta"]
    years = int(cfg["years"])

    # ---- phase 0: what each provider is (data 4.2's draws, then data 4.3's own)
    attrs = []
    for i in range(n_providers):
        a = {}
        a["hard_neg"] = bool(arng.random() < cfg["hard_neg_share"])
        a["tail"] = bool(arng.random() < cfg["tail_share"])
        z_rate, u_habit, u_clone = arng.normal(), arng.random(), arng.random()
        a["rate"] = float(min(cfg["tail_floor"] + np.exp(np.log(cfg["tail_median"]) + cfg["tail_sigma"] * z_rate), cfg["tail_cap"])) if a["tail"] else None
        a["habit"] = (_shares_pick(u_habit, cfg["high_habit_shares"] if a["rate"] >= cfg["high_rate"] else cfg["low_habit_shares"])) if a["tail"] else None
        a["clones"] = bool(a["tail"] and a["habit"] != "template" and u_clone < cfg["clone_share"])
        fw = {}
        for kind, prob in (("nr", cfg["nr_prob"]), ("imp", cfg["imp_prob"]), ("unb", cfg["unb_prob"])):
            fw[kind] = bool(arng.random() < prob)
        fw["nr_share"] = float(arng.uniform(*cfg["nr_share"]))
        fw["imp_days"] = int(arng.integers(cfg["imp_days"][0], cfg["imp_days"][1] + 1))
        fw["unb_share"] = float(arng.uniform(*cfg["unb_share"]))
        a["fwa"] = fw
        attrs.append(a)
    for a in attrs:                                   # data 4.3's attributes: a fixed number of draws per provider, whatever the options
        u = brng.random(16)
        habit_up = a["habit"] in ("systematic", "opportunistic")
        a["shared_npi"] = bool(u[0] < cfg["shared_npi_prob"])
        a["shared_share"] = float(cfg["shared_npi_share"][0] + u[1] * (cfg["shared_npi_share"][1] - cfg["shared_npi_share"][0]))
        a["covers"] = bool(u[2] < cfg["coverage_prob"])
        a["compressed"] = bool(u[3] < cfg["compressed_prob"])
        a["clinic_k"] = int(cfg["compressed_days"][0] + int(u[4] * (cfg["compressed_days"][1] - cfg["compressed_days"][0] + 1)))
        a["clinic_perm"] = [int(x) for x in np.argsort(brng.random(5))]
        a["quick"] = bool(u[5] < cfg["quick_day_prob"])
        a["batch"] = bool(u[6] < cfg["batch_prob"])
        a["fwa"]["pad"] = bool(u[7] < cfg["pad_prob"])
        a["fabricates"] = bool(u[8] < cfg["fabricate_prob"]) and (a["fwa"]["nr"] or a["fwa"]["imp"] or a["fwa"]["pad"])
        a["fab_share"] = float(cfg["fabricate_share"][0] + u[9] * (cfg["fabricate_share"][1] - cfg["fabricate_share"][0]))
        p_inf = cfg["dx_inflate_prob_habit"] if habit_up else cfg["dx_inflate_prob_other"]
        a["dx_inflate"] = bool(u[10] < p_inf)
        a["dx_inflate_share"] = float(cfg["dx_inflate_share"][0] + u[11] * (cfg["dx_inflate_share"][1] - cfg["dx_inflate_share"][0]))
        a["dx_sparse"] = bool((not a["dx_inflate"]) and u[12] < cfg["sparse_dx_prob"])
        a["in_house_lab"] = bool(u[13] < cfg["in_house_lab_share"])
        a["unneeded"] = bool(habit_up and u[14] < cfg["unneeded_test_prob"])
        a["unneeded_share"] = float(cfg["unneeded_test_share"][0] + u[15] * (cfg["unneeded_test_share"][1] - cfg["unneeded_test_share"][0]))
        a["time_share"] = _beta(brng, cfg["time_recorded_mean"], cfg["time_recorded_kappa"])
        a["lab_rate"] = _beta(brng, cfg["lab_rate_mean"], cfg["lab_rate_kappa"])
    force_template = []

    # ---- phase 1: providers and their member panels (data 4.2's draws)
    provs, members, tin_pool = [], [], []
    for i, a in enumerate(attrs):
        npi = f"1{(i + 1):09d}"
        volume = int(np.clip(rng.lognormal(np.log(g1.VOLUME_MEDIAN), g1.VOLUME_SIGMA), g1.VOLUME_MIN, g1.VOLUME_MAX))
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
        base_volume = volume
        volume = int(round(volume * years * (1.0 + (a["shared_share"] if a["shared_npi"] else 0.0))))      # mid-level visits under the physician's number; the panel is the same
        provs.append({"npi": npi, "volume": volume, "base_volume": base_volume, "eta": float(eta), "top_shift": float(top_shift), "chronic": chronic, "tin": tin_pool[-1], "clones": a["clones"],
                      "member_ids": [], "habit": a["habit"], "target": target, "mean_net": mean_net, "gross": gross, "hard_neg": a["hard_neg"], "fwa": a["fwa"], "a": a})
        base = len(members)
        for j, c in enumerate(chronic):
            order = rng.choice(len(g1.CONDITIONS), size=min(int(c), len(g1.CONDITIONS)), replace=False, p=g1.CONDITION_WEIGHT / g1.CONDITION_WEIGHT.sum())
            age = int(np.clip(rng.normal(52 + 4 * (c - 1.5), 15), 18, 96))
            members.append({"member_id": f"M{len(members) + 1:07d}", "birth_year": 2024 - age, "sex": "F" if rng.random() < 0.55 else "M", "pcp_npi": npi,
                            "_chronic": int(c), "_dx": [g1.CONDITIONS[k][1] for k in order]})
            provs[-1]["member_ids"].append(base + j)
    ng = NoteGen43(seed, cfg["clone_signal_strength"], force_template, SF)

    org_npi = {}
    size = {}
    for P in provs:
        size[P["tin"]] = size.get(P["tin"], 0) + 1
    if cfg["group_billing"]:
        for P in provs:
            if size[P["tin"]] >= 2:
                org_npi.setdefault(P["tin"], f"2{len(org_npi) + 1:09d}")
    for P in provs:
        P["billing"] = org_npi.get(P["tin"], P["npi"])

    days_all = [date(2024, 1, 1) + timedelta(days=k) for k in range(366 * years + 1)]
    weekdays = [d for d in days_all if d.weekday() < 5 and d.year < 2024 + years]
    W = len(weekdays)
    wd = np.array([d.weekday() for d in weekdays])
    for m in members:
        if mrng.random() < 0.92:
            lo, hi = 0, W - 1
        else:
            lo = int(mrng.integers(0, W // 2))
            hi = int(mrng.integers(lo + W // 4, W))
        m["_lo"], m["_hi"] = lo, min(hi, W - 1)
        m["coverage_start"], m["coverage_end"] = weekdays[m["_lo"]].isoformat(), weekdays[m["_hi"]].isoformat()
        m["product_line"] = g2.PRODUCT_LINE

    # ---- phase 1b: clinic schedules, coverage pairs, office profiles (data 4.3's own streams)
    n_prov = len(provs)
    by_tin = {}
    for pi_, P in enumerate(provs):
        by_tin.setdefault(P["tin"], []).append(pi_)
    for P in provs:
        a = P["a"]
        P["clinic"] = np.ones(W, dtype=bool)
        if a["compressed"]:
            k_days = min(5, max(a["clinic_k"], int(np.ceil(P["volume"] / (52.0 * years * cfg["compressed_max_per_day"])))))     # a very busy practice keeps enough clinic days
            keep = set(a["clinic_perm"][:k_days])
            P["clinic"] = np.isin(wd, list(keep))
        P["absent"] = np.zeros(W, dtype=bool)
        P["covering"] = []                 # [(colleague index, [days])]
    for pi_, P in enumerate(provs):
        u_partner, u_start, u_len = qrng.random(), qrng.random(), qrng.random()
        if not P["a"]["covers"] or n_prov < 2:
            continue
        mates = [q for q in by_tin[P["tin"]] if q != pi_] or [q for q in range(n_prov) if q != pi_]
        qi = mates[min(int(u_partner * len(mates)), len(mates) - 1)]
        blen = int(cfg["coverage_days"][0] + int(u_len * (cfg["coverage_days"][1] - cfg["coverage_days"][0] + 1)))
        start = int(u_start * max(W - blen, 1))
        block = list(range(start, min(start + blen, W)))
        provs[qi]["absent"][block] = True
        P["covering"].append((qi, block))
    entity_beh = {}
    for P in provs:                                   # response behaviour per practice: shared within a billing entity most of the time (office version 4.3)
        u_ent, u_own, u_mix = qrng.random(), qrng.random(), qrng.random()
        ent = P["billing"]
        if ent not in entity_beh:
            entity_beh[ent] = _shares_pick(u_ent, {"cooperative": 0.55, "slow": 0.15 + (0.10 if size[P["tin"]] >= 4 else 0.0), "sloppy": 0.20, "evasive": 0.10})
        a = P["a"]
        phantom = a["fwa"]["nr"] or a["fwa"]["imp"] or a["fwa"]["pad"]
        if phantom and a["fabricates"]:
            mix = {"cooperative": 0.45, "slow": 0.35, "sloppy": 0.15, "evasive": 0.05}
        elif phantom:
            mix = {"cooperative": 0.25, "slow": 0.25, "sloppy": 0.20, "evasive": 0.30}
        elif a["habit"] in ("systematic", "opportunistic"):
            mix = {"cooperative": 0.45, "slow": 0.15, "sloppy": 0.25, "evasive": 0.15}
        else:
            mix = None
        if mix is not None:
            P["behavior"] = _shares_pick(u_mix, mix) if u_own >= cfg["office_group_share"] * 0.5 else entity_beh[ent]
        else:
            P["behavior"] = entity_beh[ent] if u_own < cfg["office_group_share"] else _shares_pick(u_mix, {"cooperative": 0.55, "slow": 0.15, "sloppy": 0.20, "evasive": 0.10})

    def snap(d, lo, hi, ok):
        """The nearest allowed day to d inside [lo, hi] (d itself when allowed or when none is)."""
        if ok[d]:
            return d
        for step in range(1, hi - lo + 2):
            for c in (d - step, d + step):
                if lo <= c <= hi and ok[c]:
                    return c
        return d

    # ---- phase 2: visits
    headers, lines, remit, universe, truth = [], [], [], [], {}
    plan_rows = []
    fraud_claims, fraud_mech, fabricated_ids, batched = {}, {}, [], {}
    cid = 0
    dx_cut = 0
    seen_by = {}
    prev_dx = {}
    for pi, P in enumerate(provs):
        a = P["a"]
        vol = P["volume"]
        t = t_base.copy()
        t[-1] += P["top_shift"]
        guest = grng.random(vol) < cfg["guest_visit_share"]
        home_idx = np.array(P["member_ids"])
        own_choice = grng.integers(0, len(home_idx), size=vol)
        other_prov = grng.integers(0, n_prov, size=vol)
        other_choice = grng.random(vol)
        mem_base = np.empty(vol, dtype=int)
        for v in range(vol):
            if guest[v] and n_prov > 1:
                Q = provs[(pi + 1 + int(other_prov[v]) % (n_prov - 1)) % n_prov]
                mem_base[v] = Q["member_ids"][int(other_choice[v] * len(Q["member_ids"]))]
            else:
                mem_base[v] = home_idx[own_choice[v]]
        d_base = np.array([int(drng.integers(members[k]["_lo"], members[k]["_hi"] + 1)) for k in mem_base], dtype=int)
        ok_day = P["clinic"] & ~P["absent"]
        if not ok_day.all():
            d_base = np.array([snap(int(d), members[int(k)]["_lo"], members[int(k)]["_hi"], ok_day) for d, k in zip(d_base, mem_base)], dtype=int)

        # extra rendered visits: coverage for an absent colleague, quick-visit clinic days
        ex_mem, ex_d, ex_z, ex_kind = [], [], [], []
        used_md = set(zip(mem_base.tolist(), d_base.tolist()))
        for qi, block in P["covering"]:
            Q = provs[qi]
            n_c = int(round(Q["volume"] * len(block) / max(W, 1)))
            q_ids = Q["member_ids"]
            for _ in range(n_c):
                for _try in range(10):
                    k = int(q_ids[int(erng.integers(len(q_ids)))])
                    d_ = int(block[int(erng.integers(len(block)))])
                    if (k, d_) not in used_md:
                        break
                used_md.add((k, d_))
                ex_mem.append(k)
                ex_d.append(d_)
                ex_z.append(np.nan)
                ex_kind.append("coverage")
        n_qd = int(erng.integers(cfg["quick_days"][0], cfg["quick_days"][1] + 1))
        qd_days = [int(x) for x in erng.choice(np.flatnonzero(ok_day) if ok_day.any() else np.arange(W), size=n_qd, replace=False)] if a["quick"] else []
        for day in qd_days:
            n_q = int(erng.integers(cfg["quick_visits"][0], cfg["quick_visits"][1] + 1))
            cover = [int(k) for k in home_idx if members[int(k)]["_lo"] <= day <= members[int(k)]["_hi"]] or [int(k) for k in home_idx]
            order = erng.permutation(len(cover))
            for j in range(n_q):
                k = cover[int(order[j % len(order)])]
                ex_mem.append(k)
                ex_d.append(day)
                ex_z.append(float(erng.uniform(t[0] - 0.8, t[1] - 0.05)))      # a short, low-complexity visit
                ex_kind.append("quick")
                used_md.add((k, day))
        n_ex = len(ex_mem)
        V = vol + n_ex
        mem_idx = np.concatenate([mem_base, np.array(ex_mem, dtype=int)]) if n_ex else mem_base
        d_idx = np.concatenate([d_base, np.array(ex_d, dtype=int)]) if n_ex else d_base
        for k in set(mem_idx.tolist()):
            seen_by.setdefault(k, set()).add(P["npi"])

        # date batching: some visits near a batch day carry the batch day as their service date on the original claim
        batch_of = {}
        if a["batch"]:
            n_bd = int(erng.integers(cfg["batch_days"][0], cfg["batch_days"][1] + 1))
            cand_days = np.flatnonzero(ok_day) if ok_day.any() else np.arange(W)
            taken_md = set()
            for b in sorted(int(x) for x in erng.choice(cand_days, size=min(n_bd, len(cand_days)), replace=False)):
                win = np.flatnonzero((d_idx > b - cfg["batch_window"]) & (d_idx < b))
                pick = win[erng.random(len(win)) < cfg["batch_take"]]
                for v in pick.tolist():
                    k = int(mem_idx[v])
                    if (k, b) in used_md or (k, b) in taken_md or v in batch_of:
                        continue
                    taken_md.add((k, b))
                    batch_of[v] = b

        # phantom claims: ghost panel (4.2), spike days, padded days
        f_mem, f_d, f_kind, f_mech = [], [], [], []
        fw = P["fwa"]
        if fw["nr"]:
            n_nr = max(cfg["nr_min"], int(round(fw["nr_share"] * vol)))
            ghosts = frng.choice(home_idx, size=min(max(3, int(round(cfg["ghost_share"] * len(home_idx)))), len(home_idx)), replace=False)
            used = set()
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
                f_mech.append("ghost_panel")
        if fw["imp"]:
            for day in frng.choice(W, size=min(fw["imp_days"], W), replace=False):
                cover = [int(k) for k in home_idx if members[int(k)]["_lo"] <= day <= members[int(k)]["_hi"]] or [int(k) for k in home_idx]
                n_day = int(frng.integers(cfg["imp_visits"][0], cfg["imp_visits"][1] + 1))
                order = frng.permutation(len(cover))
                for j in range(n_day):
                    f_mem.append(cover[int(order[j % len(order)])])
                    f_d.append(int(day))
                    f_kind.append("impossible_days")
                    f_mech.append("spike_days")
        if fw["pad"]:
            cand = np.flatnonzero(ok_day) if ok_day.any() else np.arange(W)
            n_pd = int(pdrng.integers(cfg["pad_days"][0], cfg["pad_days"][1] + 1))
            for day in sorted(int(x) for x in pdrng.choice(cand, size=min(n_pd, len(cand)), replace=False)):
                cover = [int(k) for k in home_idx if members[int(k)]["_lo"] <= day <= members[int(k)]["_hi"] and (int(k), day) not in used_md] or [int(k) for k in home_idx]
                n_day = int(pdrng.integers(cfg["pad_per_day"][0], cfg["pad_per_day"][1] + 1))
                order = pdrng.permutation(len(cover))
                for j in range(min(n_day, len(cover))):
                    f_mem.append(cover[int(order[j])])
                    f_d.append(day)
                    f_kind.append("not_rendered")
                    f_mech.append("padded_days")
        nf = len(f_mem)
        fab = np.zeros(nf, dtype=bool)
        fab_round = np.ones(nf, dtype=int)
        u_fab, u_round = pdrng.random(nf), pdrng.random(nf)
        if a["fabricates"]:
            fab = u_fab < a["fab_share"]
            fab_round = np.where(u_round < cfg["fabricate_late_round"], 2, 1)
        n_tot = V + nf
        all_mem = np.concatenate([mem_idx, np.array(f_mem, dtype=int)]) if nf else mem_idx
        true_chronic = np.array([members[k]["_chronic"] for k in all_mem])
        z0_all = beta * true_chronic + P["eta"] + zrng.logistic(size=n_tot)
        for j in range(n_ex):
            if not np.isnan(ex_z[j]):
                z0_all[vol + j] = ex_z[j]                            # quick visits: their own low complexity
        z0 = z0_all[:V]
        u_date = d_idx / max(W - 1, 1)
        out_u = orng.random(V)
        accepted = ~((out_u < DENIAL) | ((out_u >= DENIAL + REPLACE) & (out_u < DENIAL + REPLACE + VOID)))
        n_acc = max(int(accepted.sum()), 1)

        shift = 0.0
        if P["habit"] in ("systematic", "template"):
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
        selected = np.zeros(V, dtype=bool)
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
        up_p, dn_p = (P["gross"] + P["mean_net"]) / 2, (P["gross"] - P["mean_net"]) / 2
        r_up, r_dn = nrng.random(V), nrng.random(V)
        free = ~selected & (billed == just)
        billed = np.where(free & (r_up < up_p) & (just < 4), just + 1, np.where(free & (r_up >= up_p) & (r_dn < dn_p) & (just > 0), just - 1, billed))
        corr_ok = P["habit"] is None
        corr_chg = (crng.random(V) < cfg["correction_level_change_share"]) if (corr_ok and cfg["correction_level_change_share"] > 0) else np.zeros(V, dtype=bool)
        corr_up = crng.random(V) < cfg["correction_up_share"]
        omit = (rrng.random(n_tot) < cfg["rendering_omitted_share"]) if (cfg["rendering_omitted_share"] > 0 and P["billing"] == P["npi"]) else np.zeros(n_tot, dtype=bool)
        final_b = billed.copy()
        if nf:
            just_all = np.concatenate([just, level_of(z0_all[V:], t)])
            billed_all = np.concatenate([billed, just_all[V:]])
            out_u_all = np.concatenate([out_u, np.full(nf, 0.5)])
            d_all = np.concatenate([d_idx, np.array(f_d, dtype=int)])
        else:
            just_all, billed_all, out_u_all, d_all = just, billed, out_u, d_idx
        unb_on = np.zeros(n_tot, dtype=bool)
        if fw["unb"]:
            unb_on[:V] = urng.random(V) < fw["unb_share"]
        P["n_corrections"], P["n_corr_up"], P["n_corr_down"], P["n_date_corr"] = 0, 0, 0, 0
        elem_noise = rrng.normal(0, cfg["element_sd"], size=(n_tot, 3))
        time_noise = rrng.normal(0, cfg["time_sd"], size=n_tot)
        pad_u, risk_u = rrng.random(n_tot), rrng.random(n_tot)
        pad_off = rrng.integers(0, cfg["time_pad_over"], size=n_tot)
        fwa_over = {"not_rendered": 0.0, "impossible_days": 0.0, "unbundling": 0.0}
        fwa_n = {"not_rendered": 0, "impossible_days": 0, "unbundling": 0}
        mech_n = {"ghost_panel": 0, "spike_days": 0, "padded_days": 0}
        P["unneeded_paid"], P["n_fabricated"] = 0.0, 0
        habit_up = P["habit"] in ("systematic", "opportunistic")
        for v in range(n_tot):
            is_f = v >= V
            m = members[all_mem[v]]
            cid += 1
            claim_id = f"C{cid:07d}"
            dx = list(m["_dx"][:5])
            if mrng.random() < 0.45 or not dx:
                dx.append(g1.ACUTE_DX[int(mrng.integers(len(g1.ACUTE_DX)))][1])
            dx = dx[:6]
            # claims-based confounders: sparse coding lists only the first conditions; inflation adds conditions the member does not have
            u_sp, u_inf, u_inf2 = xrng.random(3)
            if a["dx_sparse"]:
                chronic_dx = [c for c in dx if c in INFLATE_CODES]
                acute = [c for c in dx if c not in INFLATE_CODES]
                keep = 1 if u_sp < 0.5 else 2
                dx = (chronic_dx[:keep] + acute) or dx[:1]
            if a["dx_inflate"] and u_inf < a["dx_inflate_share"]:
                missing = [i_ for i_, c in enumerate(INFLATE_CODES) if c not in dx]
                if missing:
                    w_ = INFLATE_W[missing] / INFLATE_W[missing].sum()
                    n_add = 1 if u_inf2 < 0.6 else 2
                    add = [INFLATE_CODES[missing[int(i_)]] for i_ in xrng.choice(len(missing), size=min(n_add, len(missing)), replace=False, p=w_)]
                    chronic_dx = [c for c in dx if c in INFLATE_CODES] + add
                    acute = [c for c in dx if c not in INFLATE_CODES]
                    dx = (chronic_dx + acute)[:6]
            true_day = int(d_all[v])
            date_ = weekdays[true_day]
            claim_day = batch_of.get(v, true_day) if not is_f else true_day
            claim_date = weekdays[claim_day]
            L, B = int(just_all[v]), int(billed_all[v])
            truth[claim_id] = CODES[B] if is_f else CODES[L]
            if is_f:
                fraud_claims[claim_id] = f_kind[v - V]
                fraud_mech[claim_id] = f_mech[v - V]
            z_v = z0_all[v] + (shift if not is_f else 0.0)
            els_true = [int(np.clip(level_of(z_v + elem_noise[v, j], t), 0, 4)) for j in range(3)]
            els = list(els_true)
            data_true = els_true[1]
            p_true = g2.LAB_IF_DATA_HIGH if data_true >= 3 else g2.LAB_IF_DATA_LOW
            q_lab = float(np.clip(a["lab_rate"] * (0.5 + 0.25 * m["_chronic"]), 0.02, 0.9))
            p_lab = p_true if cfg["test_link"] >= 1.0 else cfg["test_link"] * p_true + (1 - cfg["test_link"]) * q_lab
            lab = rrng.random() < p_lab
            u_unneeded = lrng.random()
            unneeded = bool((not is_f) and a["unneeded"] and B > L and not lab and u_unneeded < a["unneeded_share"])
            lab = lab or unneeded
            time_rec = rrng.random() < a["time_share"]
            tlevel = int(np.clip(level_of(z_v + time_noise[v], t), 0, 4))
            minutes = int(rrng.integers(g2.MINUTE_BANDS[tlevel][0], g2.MINUTE_BANDS[tlevel][1] + 1)) if time_rec else ""
            fabricated = bool(is_f and fab[v - V])
            if P["clones"] and B > L:
                els, tlevel = [B, B, B], B
                minutes = int(rrng.integers(g2.MINUTE_BANDS[tlevel][0], g2.MINUTE_BANDS[tlevel][1] + 1)) if time_rec else ""
            elif P["habit"] == "opportunistic" and B > L:
                if time_rec and pad_u[v] < cfg["time_pad_prob"]:
                    tlevel = B
                    minutes = g2.MINUTE_BANDS[B][0] + int(pad_off[v])
                if risk_u[v] < cfg["risk_inflate_prob"]:
                    els[2] = max(els[2], B)
            if fabricated:                                   # a chart written for a visit that never happened: two of the three elements and the time support the bill
                j_low = int(vrng.integers(3))
                els = [max(e, B) if j != j_low else e for j, e in enumerate(els)]
                if time_rec:
                    tlevel = B
                    minutes = int(vrng.integers(g2.MINUTE_BANDS[B][0], g2.MINUTE_BANDS[B][1] + 1))
            urow = {"claim_id": claim_id, "problems_level": els[0], "data_level": els[1], "risk_level": els[2], "documented_minutes": minutes}
            universe.append(urow)

            em_allowed = allowed[CODES[B]]
            dx_out = dx[:cfg["dx_cap"]] if (cfg["dx_cap"] and claim_date.month in cfg["dx_cap_months"]) else dx
            dx_cut += len(dx_out) < len(dx)
            headers.append({"claim_id": claim_id, "member_id": m["member_id"], "billing_npi": P["billing"], "rendering_npi": "" if omit[v] else P["npi"],
                            "claim_frequency": 1, "original_claim_id": "", "service_date": claim_date.isoformat(),
                            **{f"dx{k + 1}": (dx_out[k] if k < len(dx_out) else "") for k in range(6)}})
            mods = "25" if ((lab and mrng.random() < 0.05) or unb_on[v]) else ""
            line_rows = [{"claim_id": claim_id, "line_no": 1, "cpt": CODES[B], "modifiers": mods, "units": 1, "place_of_service": "11", "dx_pointer": "1",
                          "billed_amount": round(em_allowed * 2.5, 2), "allowed_amount": em_allowed, "paid_amount": round(em_allowed * 0.8, 2)}]
            lab_code = None
            unneeded_paid = 0.0
            if lab:
                code, price = g2.LAB_CODES[int(mrng.integers(len(g2.LAB_CODES)))]
                lab_code = code
                if a["in_house_lab"]:                        # an outside lab bills the test on its own claim, which is not in this extract
                    line_rows.append({"claim_id": claim_id, "line_no": 2, "cpt": code, "modifiers": "", "units": 1, "place_of_service": "11", "dx_pointer": "1",
                                      "billed_amount": round(price * 2.5, 2), "allowed_amount": price, "paid_amount": round(price * 0.8, 2)})
                    if unneeded:
                        unneeded_paid = round(price * 0.8, 2)
            unb_paid = 0.0
            if unb_on[v]:
                code, price = (lab_code, dict(g2.LAB_CODES)[lab_code]) if lab_code else g2.LAB_CODES[int(urng.integers(len(g2.LAB_CODES)))]
                line_rows.append({"claim_id": claim_id, "line_no": len(line_rows) + 1, "cpt": code, "modifiers": "", "units": 1, "place_of_service": "11", "dx_pointer": "1",
                                  "billed_amount": round(price * 2.5, 2), "allowed_amount": price, "paid_amount": round(price * 0.8, 2)})
                unb_paid = round(price * 0.8, 2)
            lines.extend(line_rows)
            ng.add_visit(claim_id, None, m, P, L, B, els, els_true, minutes, tlevel, lab_code, date_, dx)
            contra = _vary_chart(cfg, vrng, ng, urow, P, a, m, dx, is_f, fabricated, habit_up, date_, prev_dx)
            # the office plan (simulator side): when the chart can be produced, how hard it is to read, what happens when the request arrives
            u_c = vrng.random(3)
            if cfg["coder_case"]:
                gap_t = float(np.min(np.abs(z_v - t)))
                thin = (urow["documented_minutes"] == "") and len([c for c in ng.notes[-1]["problems_addressed"].split(";") if c]) <= 1
                p_coder = cfg["coder_base"] + cfg["coder_borderline"] * float(np.exp(-gap_t / cfg["coder_scale"])) + (cfg["coder_thin"] if thin else 0.0) + (cfg["coder_contradiction"] if contra else 0.0)
                p_coder = round(min(p_coder, cfg["coder_max"]), 3)
            else:
                p_coder = FLAT_CODER
            auth = ng.auth[-1]
            sor_p = cfg["sign_on_request_fabricated"] if fabricated else (cfg["sign_on_request_habit"] if habit_up else cfg["sign_on_request_honest"])
            signs = int((auth["status"] == "unsigned" or (fabricated and fab_round[v - V] == 2)) and u_c[0] < sor_p)
            amr_p = cfg["amend_on_release_fabricated"] if fabricated else (cfg["amend_on_release_habit"] if habit_up else cfg["amend_on_release_honest"])
            release = ""
            if auth["status"] in ("unsigned", "illegible") and u_c[1] < amr_p:
                rel = [max(int(urow[k]), B) if u_c[2] < 0.7 or k == "risk_level" else int(urow[k]) for k in ("problems_level", "data_level", "risk_level")]
                release = ";".join(str(x) for x in rel)
            avail = (int(fab_round[v - V]) if fabricated else 0) if is_f else 1
            if fabricated:
                fabricated_ids.append(claim_id)
                P["n_fabricated"] += 1
            if is_f or p_coder != FLAT_CODER or signs or release:
                plan_rows.append({"claim_id": claim_id, "available_from_round": avail, "coder_disagreement": p_coder, "signs_on_request": signs, "release_levels": release})
            total_paid = sum(r["paid_amount"] for r in line_rows)
            u = out_u_all[v]
            batched_here = (not is_f) and v in batch_of
            if batched_here:
                batched[claim_id] = date_.isoformat()
            u_bc = erng.random() if batched_here else 1.0
            if u < DENIAL:
                remit.append({"claim_id": claim_id, "status": "denied", "paid_amount": 0.0, "adjustment_amount": round(total_paid, 2), "denial_reason": "CO-16 claim lacks information"})
            elif u < DENIAL + REPLACE or (batched_here and u >= DENIAL + REPLACE + VOID and u_bc < cfg["batch_correct_share"]):
                remit.append({"claim_id": claim_id, "status": "reversed", "paid_amount": 0.0, "adjustment_amount": round(total_paid, 2), "denial_reason": "replaced"})
                cid += 1
                new_id = f"C{cid:07d}"
                headers.append({**headers[-1], "claim_id": new_id, "claim_frequency": 7, "original_claim_id": claim_id,
                                **({"service_date": date_.isoformat()} if batched_here else {})})          # a correction carries the true date of service
                new_rows = [{**r, "claim_id": new_id} for r in line_rows]
                paid2 = total_paid
                if corr_chg[v] and u < DENIAL + REPLACE:
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
                P["n_date_corr"] += int(batched_here)
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
            if is_f:
                fwa_over[f_kind[v - V]] += round(total_paid, 2)
                fwa_n[f_kind[v - V]] += 1
                mech_n[f_mech[v - V]] += 1
            elif unb_paid and (u >= DENIAL + REPLACE + VOID or DENIAL <= u < DENIAL + REPLACE):
                fwa_over["unbundling"] += unb_paid
                fwa_n["unbundling"] += 1
            if unneeded_paid and (u >= DENIAL + REPLACE + VOID or DENIAL <= u < DENIAL + REPLACE):
                P["unneeded_paid"] += unneeded_paid
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
        P["fwa_over"], P["fwa_n"], P["n_phantom"], P["mech_n"] = fwa_over, fwa_n, nf, mech_n
        P["extra"] = {"shared_npi": int(P["volume"] - P["base_volume"] * years), "coverage": sum(1 for k in ex_kind if k == "coverage"), "quick_visit_days": sum(1 for k in ex_kind if k == "quick")}
        P["n_batched"] = len(batch_of)

    ctotals, defect_rec = None, {}
    if cfg["control_totals"]:
        ctotals = defects_v22.control_totals(headers, remit)
    if any(cfg[k] for k in defects_v22.DEFECT_OPTIONS):
        defect_rec, cid = defects_v22.inject(headers, lines, remit, universe, truth, cfg, np.random.default_rng([seed, SF, 31]), cid)

    # ---- write (the data 4.2 files and columns, plus the simulator-side office files of version 4.3)
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
                  [{"cpt": c, "allowed_amount": a_} for c, a_ in allowed.items()] + [{"cpt": c, "allowed_amount": p} for c, p in g2.LAB_CODES], ["cpt", "allowed_amount"])
    g2._write_csv(os.path.join(out_dir, "reference", "place_of_service.csv"), [{"code": "11", "description": "Office"}], ["code", "description"])
    g2._write_csv(os.path.join(out_dir, "reference", "specialty_peer_groups.csv"), [{"specialty": "Family Practice", "peer_group": "GA Family Practice office-based"}], ["specialty", "peer_group"])
    g2._write_csv(os.path.join(out_dir, "records", "records_universe.csv"), universe, ["claim_id", "problems_level", "data_level", "risk_level", "documented_minutes"])
    g2._write_csv(os.path.join(out_dir, "records", "unrendered_claims.csv"), [{"claim_id": c} for c in sorted(fraud_claims)], ["claim_id"])
    if ctotals is not None:
        defects_v22.write_control_totals(os.path.join(out_dir, "control_totals.csv"), ctotals)
    for name, rows, cols in (("visit_notes", ng.notes, notes_v21.NOTE_COLS), ("note_authentication", ng.auth, notes_v21.AUTH_COLS), ("note_orders", ng.orders, notes_v21.ORDER_COLS),
                             ("note_results", ng.results, notes_v21.RESULT_COLS), ("audit_trail", ng.audit, notes_v21.AUDIT_COLS)):
        g2._write_csv(os.path.join(out_dir, "records", f"{name}.csv"), rows, cols)
    office_files = SF != 42 or any(cfg[k] for k in ("coder_case", "office_profiles", "fabricate_prob")) or plan_rows and any(r["signs_on_request"] or r["release_levels"] for r in plan_rows)
    if office_files:
        g2._write_csv(os.path.join(out_dir, "records", "office_chart_plan.csv"), plan_rows, PLAN_COLS)
        g2._write_csv(os.path.join(out_dir, "records", "office_profiles.csv"),
                      [{"npi": P["npi"], "behavior": P["behavior"]} for P in provs] if cfg["office_profiles"] else [], ["npi", "behavior"])

    for P in provs:
        P["up_rate"], P["down_rate"] = P["live_up"] / max(P["n_acc"], 1), P["live_down"] / max(P["n_acc"], 1)
    shared = sum(1 for s in seen_by.values() if len(s) >= 2) / max(len(seen_by), 1)
    providers_key = {}
    for P in provs:
        a = P["a"]
        fo, fn, fw = P["fwa_over"], P["fwa_n"], P["fwa"]
        fwa_total = round(sum(fo.values()), 2)
        providers_key[P["npi"]] = {
            "habit": P["habit"], "uses_template": bool(ng.prov.get(P["npi"], {}).get("template")), "clones_notes": P["clones"],
            "intent": {"level_upcoding": P["habit"] in ("systematic", "opportunistic"), "cloned_notes": P["clones"], "not_rendered": bool(fw["nr"] or fw["pad"]),
                       "impossible_days": bool(fw["imp"]), "unbundling": bool(fw["unb"]), "fabricated_charts": bool(P["n_fabricated"] > 0),
                       "diagnosis_inflation": a["dx_inflate"], "unneeded_tests": a["unneeded"]},
            "target_net_rate": None if P["target"] is None else round(P["target"], 4), "mean_net_rate": round(P["mean_net"], 4),
            "net_rate": round(P["up_rate"] - P["down_rate"], 4), "up_rate": round(P["up_rate"], 4), "down_rate": round(P["down_rate"], 4), "honest_miscode_rate": round(P["gross"], 4),
            "true_overpay_level_net": round(P["live_over"], 2), "true_overpay_level_gross": round(P["live_over_gross"], 2),
            "true_overpay_fwa": {k: round(v, 2) for k, v in fo.items()}, "fwa_claims": dict(fn), "n_phantom_claims": P["n_phantom"],
            "true_overpay_total": round(max(P["live_over"], 0.0) + fwa_total, 2),
            "high_acuity_panel": P["hard_neg"], "volume": P["volume"], "billing_npi": P["billing"], "group_tin": P["tin"],
            "corrections": P["n_corrections"], "corrections_up": P["n_corr_up"], "corrections_down": P["n_corr_down"],
            "panel_acuity_shift": round(P["shift"], 2), "provider_effect": round(P["eta"] + P["shift"], 4), "top_shift": round(P["top_shift"], 4),
            # data 4.3
            "fwa_mechanisms": {"ghost_panel": bool(fw["nr"]), "spike_days": bool(fw["imp"]), "padded_days": bool(fw["pad"]), "unbundling": bool(fw["unb"])},
            "fwa_mechanism_claims": dict(P["mech_n"]),
            "fabricates_charts": bool(a["fabricates"]), "fabricated_chart_claims": P["n_fabricated"],
            "legit_volume": {"shared_npi": a["shared_npi"], "covers_colleague": bool(P["covering"]), "absent_covered": bool(P["absent"].any()), "compressed_schedule": a["compressed"],
                             "quick_visit_days": a["quick"], "date_batching": a["batch"]},
            "extra_rendered_visits": dict(P["extra"]), "date_batched_claims": P["n_batched"], "date_corrections": P["n_date_corr"],
            "dx_coding": "inflated" if a["dx_inflate"] else ("sparse" if a["dx_sparse"] else "typical"),
            "in_house_lab": a["in_house_lab"], "orders_unneeded_tests": a["unneeded"], "unneeded_test_paid": round(P["unneeded_paid"], 2),
            "time_recording_share": round(a["time_share"], 4), "office_behavior": P["behavior"] if cfg["office_profiles"] else None}
    with open(answer_key_path, "w") as f:
        json.dump({"seed": seed, "data_version": "4.3", "clone_share": cfg["clone_share"],
                   "defects": {**({"dx_truncation": {"cap": cfg["dx_cap"], "months": list(cfg["dx_cap_months"]), "claims_shortened": dx_cut}} if cfg["dx_cap"] else {}), **defect_rec,
                               **({"control_totals": {"file": "control_totals.csv", "months": len(ctotals)}} if ctotals is not None else {})},
                   "defect_profile": profile,
                   "config_profile": "default" if config_hash(cfg) == config_hash(config({})[0]) else "custom", "config_hash": config_hash(cfg), "holdout_families": list(cfg["holdout_families"]), "years": years,
                   "clone_signal_strength": cfg["clone_signal_strength"], "cloned_visits": ng.cloned, "members_seen_by_two_or_more_providers": round(shared, 4),
                   "fraud_claims": fraud_claims, "fraud_claim_mechanism": fraud_mech, "fabricated_chart_claims": sorted(fabricated_ids), "date_batched_claims": batched,
                   "providers": providers_key, "justified_cpt_by_claim": truth}, f)
    return prov_rows


def _vary_chart(cfg, vrng, ng, urow, P, a, m, dx, is_f, fabricated, habit_up, date_, prev_dx):
    """Structured chart variability on the visit just written (universe row and the last note package rows). Returns True when the chart contradicts its own note.
    Draws a fixed number of numbers per visit from vrng, whatever the options."""
    note, auth, audit = ng.notes[-1], ng.auth[-1], ng.audit[-1]
    u = vrng.random(12)
    j_el = int(vrng.integers(3))
    contra = False
    keys = ("problems_level", "data_level", "risk_level")
    # contradictory or missing elements: the structured level disagrees with what the note says (the note text is not changed)
    if u[0] < cfg["contradict_share"]:
        step = (1 if u[1] < 0.5 else -1) * (1 if u[2] < 0.75 else 2)
        urow[keys[j_el]] = int(np.clip(int(urow[keys[j_el]]) + step, 0, 4))
        contra = True
    elif u[3] < cfg["missing_element_share"]:
        urow[keys[j_el]] = 0
        contra = True
    # honest template boilerplate that documents more risk than the visit needed
    if P["habit"] is None and a is not None and ng.prov.get(P["npi"], {}).get("template") and u[4] < cfg["boilerplate_share"] and not is_f:
        urow["risk_level"] = int(min(int(urow["risk_level"]) + 1, 4))
        note["note_text"] = note["note_text"] + " " + BOILERPLATE
    # time: rounded, or stated only as a range (then the structured minutes are blank)
    mins = urow["documented_minutes"]
    if mins != "":
        mins = int(mins)
        if u[5] < cfg["time_range_share"]:
            lo = max(5, 5 * (mins // 5) - 5 * int(u[6] < 0.5))
            hi = lo + 10
            text = note["note_text"]
            for old in (f" Total time on the date of the encounter: {note['documented_minutes']} minutes.", f" Face-to-face time with the patient: {note['documented_minutes']} minutes."):
                text = text.replace(old, f" Total time approximately {lo} to {hi} minutes.")
            note["note_text"], note["time_statement"], note["documented_minutes"] = text, "range", ""
            urow["documented_minutes"] = ""
        elif u[7] < cfg["time_round_share"]:
            unit = 15 if u[8] < 0.3 else 5
            r_ = max(unit, int(round(mins / unit)) * unit)
            if str(note["documented_minutes"]) == str(mins):
                note["note_text"] = note["note_text"].replace(f": {mins} minutes.", f": {r_} minutes.")
                note["documented_minutes"] = r_
            urow["documented_minutes"] = r_
    # stale copied-forward problems: a problem from the patient's earlier note that is not on this claim
    pkey = (P["npi"], m["member_id"])
    stale = [c for c in prev_dx.get(pkey, []) if c not in dx]
    if stale and not is_f and u[9] < cfg["stale_copy_share"]:
        note["problems_addressed"] = ";".join([c for c in note["problems_addressed"].split(";") if c] + [stale[0]])
    prev_dx[pkey] = list(dx)
    # late signatures and addenda
    if auth["status"] in ("signed", "e_signed") and u[10] < cfg["late_sign_share"]:
        lag = 8 + int(37 * u[11])
        auth["signed_date"] = (date_ + timedelta(days=lag)).isoformat()
        audit["last_edited_ts"] = f"{auth['signed_date']}T{audit['last_edited_ts'][11:]}"
    add_p = cfg["addendum_share_fabricated"] if fabricated else (cfg["addendum_share_habit"] if habit_up else cfg["addendum_share_honest"])
    u_add, u_lag, u_ct = vrng.random(3)
    if auth["status"] != "unsigned" and u_add < add_p:
        auth["amended"], auth["amended_date"] = 1, (date_ + timedelta(days=5 + int(80 * u_lag))).isoformat()
        note["note_text"] = note["note_text"] + ADDENDUM
        audit["last_edited_ts"] = f"{auth['amended_date']}T{audit['last_edited_ts'][11:]}"
    if fabricated:                                   # a reconstructed chart: often created well after the date of service, with pasted text
        if u_ct < 0.5:
            audit["created_ts"] = f"{(date_ + timedelta(days=30 + int(240 * u_lag))).isoformat()}T{audit['created_ts'][11:]}"
            if audit["last_edited_ts"][:10] < audit["created_ts"][:10]:
                audit["last_edited_ts"] = audit["created_ts"]
        audit["copy_paste_events"] = int(audit["copy_paste_events"]) + int(6 * u[6])
    return contra
