"""Statistics of the data 4.2 development seeds for docs/data_v4_2.md (issue 173), written to docs/data_v4_2_stats.md. Free.
The distribution of true rates, the share of providers above thresholds (by rate and in dollars), the fraud, waste and abuse counts and dollars, the signals (claims per provider per day),
the chart-reading table and the drift as in docs/data_v4_0_stats.md, and how the frozen screens rank true overpayment. Rates come from every built development seed (the answer keys only);
the claim-level tables from the first N seeds (default 20).
Usage: python eval/data_v42_stats.py [N]"""
import csv
import json
import os
import statistics as st
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "eval"))
import d42_truth as dt  # noqa: E402
import dev_pool_v42 as pool  # noqa: E402
import dev_release3 as dev  # noqa: E402
import eval61_recovery as rec  # noqa: E402
import metrics_d42 as md  # noqa: E402
import records  # noqa: E402
import score_40 as s4  # noqa: E402

LV = {"99211": 0, "99212": 1, "99213": 2, "99214": 3, "99215": 4}
OUT = os.path.join(ROOT, "docs", "data_v4_2_stats.md")
BINS = [("below -10%", -9, -0.10), ("-10% to -5%", -0.10, -0.05), ("-5% to 0", -0.05, 0.0), ("0 to 5%", 0.0, 0.05), ("5% to 10%", 0.05, 0.10), ("10% to 15%", 0.10, 0.15),
        ("15% to 25%", 0.15, 0.25), ("25% to 35%", 0.25, 0.35), ("35% and above", 0.35, 9)]


def doc_level(u):
    return max(records.mdm_level(int(u["problems_level"]), int(u["data_level"]), int(u["risk_level"])), records.level_from_minutes(u["documented_minutes"]))


def built(seeds):
    return [s for s in seeds if os.path.exists(os.path.join(ROOT, "eval", "answer_key", f"ground_truth_v2_d42_{s}.json")) and os.path.isdir(os.path.join(ROOT, "data", f"synthetic_v2_d42_{s}", "view"))]


def main(n_claim_seeds=20):
    seeds = built(pool.DEV)
    cseeds = built(pool.DEV[:n_claim_seeds])
    cost = dt.pursuit_cost()
    bins = Counter()
    per_seed = []
    habit_rows = defaultdict(list)
    kinds = {k: {"providers": [], "claims": [], "dollars": [], "per_provider": []} for k in md.FWA}
    disagree = Counter()
    comp = Counter()                                   # who is justified at m = 1, by why
    tot_level = tot_fwa = 0.0
    all_n = 0
    t_by_m = defaultdict(list)
    for s in seeds:
        k = dt.load_key(f"d42_{s}")
        P = k["providers"]
        net = {pid: v["net_rate"] for pid, v in P.items()}
        T = dt.totals(k)
        all_n += len(P)
        for r in net.values():
            for name, lo, hi in BINS:
                if lo <= r < hi:
                    bins[name] += 1
        per_seed.append({"seed": s, "ge5": sum(r >= 0.05 for r in net.values()), "ge15": sum(r >= 0.15 for r in net.values()), "ge25": sum(r >= 0.25 for r in net.values()), "ge35": sum(r >= 0.35 for r in net.values()),
                         "tail": sum(v["habit"] is not None for v in P.values()), "level": sum(max(v["true_overpay_level_net"], 0) for v in P.values()),
                         "fwa": sum(sum(v["true_overpay_fwa"].values()) for v in P.values()), "hard": sum(v["high_acuity_panel"] for v in P.values())})
        tot_level += per_seed[-1]["level"]
        tot_fwa += per_seed[-1]["fwa"]
        for m in dt.M_SWEEP:
            t_by_m[m].append(len(dt.justified(k, m, cost)))
        for pid, v in P.items():
            if v["habit"]:
                habit_rows[v["habit"] + (" (cloner)" if v["clones_notes"] else "")].append((net[pid], v["true_overpay_level_net"], v["target_net_rate"]))
            fw = v["true_overpay_fwa"]
            any_fwa = sum(fw.values()) > 0
            for kind in md.FWA:
                if v["intent"][kind]:
                    kinds[kind]["providers"].append(1)
                    kinds[kind]["claims"].append(v["fwa_claims"][kind])
                    kinds[kind]["dollars"].append(fw[kind])
            high = net[pid] >= 0.15
            just = T[pid] >= cost
            if just:
                lvl_ok = max(v["true_overpay_level_net"], 0) >= cost
                comp["net rate 15% or more" if high else ("net rate 5% to 15%" if net[pid] >= 0.05 else ("net rate below 5% (a large panel with noise)" if lvl_ok else "fraud, waste and abuse dollars carry it over the line"))] += 1
                comp["of which have a habit"] += v["habit"] is not None
                comp["of which have any FWA"] += sum(fw.values()) > 0
            disagree["rate >= 15% and dollars >= pursuit cost"] += high and just
            disagree["rate >= 15% but dollars below pursuit cost"] += high and not just
            disagree["rate below 15% but dollars >= pursuit cost (level only)"] += (not high) and (max(v["true_overpay_level_net"], 0) >= cost)
            disagree["dollars >= pursuit cost from FWA only (level dollars below it)"] += (max(v["true_overpay_level_net"], 0) < cost) and (sum(fw.values()) >= cost)
    # claim-level tables
    reading = defaultdict(Counter)
    drift = defaultdict(lambda: [0, 0, 0, 0])
    day_honest, day_imp, shared = [], [], []
    listed = defaultdict(lambda: Counter())
    screen_rows = defaultdict(list)
    for s in cseeds:
        code = f"d42_{s}"
        data = os.path.join(ROOT, "data", f"synthetic_v2_{code}")
        k = dt.load_key(code)
        J, P = k["justified_cpt_by_claim"], k["providers"]
        fraud = k["fraud_claims"]
        shared.append(k["members_seen_by_two_or_more_providers"])
        claims = defaultdict(list)
        for r in csv.DictReader(open(os.path.join(data, "view", "claims.csv"))):
            claims[r["provider_id"]].append(r)
        uni = {r["claim_id"]: r for r in csv.DictReader(open(os.path.join(data, "records", "records_universe.csv")))}
        for pid, rows in claims.items():
            v = P[pid]
            days = Counter(r["service_date"] for r in rows)
            (day_imp if v["intent"]["impossible_days"] else day_honest).append(max(days.values()))
            for r in rows:
                if r["claim_id"] in fraud:
                    continue
                b, j = LV[r["cpt"]], LV[J[r["claim_id"]]]
                hab = v["habit"] + (" (cloner)" if v["clones_notes"] else "") if v["habit"] else None
                grp = "correctly billed" if b == j else ("downcoded" if b < j else (hab + ", upcoded" if hab else "honest noise, upcoded"))
                u = uni.get(r["claim_id"])
                if u is None:
                    continue
                d = doc_level(u)
                reading[grp]["higher" if d > b else ("as billed" if d == b else "lower")] += 1
                if v["habit"] and b > j:
                    h = drift[v["habit"]]
                    h[0] += r["service_date"] >= "2024-07-01"
                    h[1] += 1
            if v["habit"]:
                h = drift[v["habit"]]
                h[2] += sum(r["service_date"] >= "2024-07-01" for r in rows if r["claim_id"] not in fraud)
                h[3] += sum(1 for r in rows if r["claim_id"] not in fraud)
        for method in ("eb_ratio_t", "eb_upper_t"):
            name = dev.write_flagged(code, method, 10)
            for kind, val in md.screen_metrics(code, f"flagged_{name}.csv", ks=(22,)).items():
                screen_rows[(method, kind)].append(val)
    L = ["# Data 4.2 development seeds: what the generator produced", "", "[Back to the README](../README.md) · [data 4.2](data_v4_2.md)", "",
         f"Generated by `python eval/data_v42_stats.py`. Free. {len(seeds)} development seeds built ({pool.DEV[0]} to {pool.DEV[-1]} step 37 where built), each 216 providers, no planted role. "
         "Rates are net (billed above minus below the justified level) on the live rendered claims the detector view keeps, the basis of score 4.0 (a phantom claim is justified at its billed level). "
         f"Claim-level tables use the first {len(cseeds)} seeds. The pursuit cost used for the dollar threshold is ${cost:,.0f} (30 charts, two rounds, one demand, triage, score 4.0's prices).", "",
         "## True net rate of every provider", "", f"All {all_n:,} providers of {len(seeds)} datasets.", "", "| Realized net rate | Providers | Share |", "|---|---|---|"]
    for name, lo, hi in BINS:
        L.append(f"| {name} | {bins[name]:,} | {bins[name] / all_n:.1%} |")
    ge = lambda key: [x[key] for x in per_seed]
    L += ["", "Providers per dataset at or above a rate (the count varies by seed; there is no quota):", "", "| At or above | Mean | Min | Max |", "|---|---|---|---|"]
    for lab, key in (("5%", "ge5"), ("15%", "ge15"), ("25%", "ge25"), ("35%", "ge35"), ("with a habit (tail draws)", "tail"), ("honest high-acuity panels", "hard")):
        L.append(f"| {lab} | {st.mean(ge(key)):.1f} | {min(ge(key))} | {max(ge(key))} |")
    n15 = sum(ge("ge15"))
    L += ["", f"**{n15} providers of {all_n:,} ({n15 / all_n:.1%}) are at or above 15% net**, about {st.mean(ge('ge15')):.1f} per dataset (data 4.0 planted exactly 8).", "",
          "## Habits (the tail)", "", "| Habit | Providers | Net rate: min / mean / max | Level overpayment per provider (mean, median) |", "|---|---|---|---|"]
    for h in sorted(habit_rows):
        r = [x[0] for x in habit_rows[h]]
        o = [x[1] for x in habit_rows[h]]
        L.append(f"| {h} | {len(r)} | {min(r):.1%} / {st.mean(r):.1%} / {max(r):.1%} | ${st.mean(o):,.0f}, ${st.median(o):,.0f} |")
    L += ["", "## Dollars available and who is worth pursuing", "",
          f"Per dataset (mean over {len(seeds)}): level overpayment (net per provider, floored at 0) ${tot_level / len(seeds):,.0f}; fraud, waste and abuse ${tot_fwa / len(seeds):,.0f}. "
          "Level dollars include the small positive net of honest noise.", "", "Providers per dataset that are *justified* (true overpayment at least m times the pursuit cost):", "", "| m | 0 (any) | 0.5 | 1 | 2 | 4 |", "|---|---|---|---|---|---|",
          "| mean providers | " + " | ".join(f"{st.mean(t_by_m[m]):.1f}" for m in dt.M_SWEEP) + " |", "",
          "The two views of 'worth pursuing' disagree (all providers of all datasets):", "", "| Group | Providers |", "|---|---|"]
    for lab, c in disagree.items():
        L.append(f"| {lab} | {c} |")
    nj = sum(t_by_m[1.0])
    L += ["", f"Who is justified at m = 1 ({nj} providers in {len(seeds)} datasets; the dollar line is generous to large panels, so a rate-based reading is stricter):", "", "| Why | Providers | Share |", "|---|---|---|"]
    for lab in ("net rate 15% or more", "net rate 5% to 15%", "net rate below 5% (a large panel with noise)", "fraud, waste and abuse dollars carry it over the line"):
        L.append(f"| {lab} | {comp[lab]} | {comp[lab] / max(nj, 1):.0%} |")
    L += ["", "## Fraud, waste and abuse", "", "| Kind | Providers per dataset | Claims per provider (mean) | Dollars per provider (mean, median) | Dollars per dataset |", "|---|---|---|---|---|"]
    for kind in md.FWA:
        d = kinds[kind]
        if d["dollars"]:
            L.append(f"| {kind.replace('_', ' ')} | {len(d['providers']) / len(seeds):.1f} | {st.mean(d['claims']):.0f} | ${st.mean(d['dollars']):,.0f}, ${st.median(d['dollars']):,.0f} | ${sum(d['dollars']) / len(seeds):,.0f} |")
    if day_honest and day_imp:
        L += ["", f"Claims per provider per day (the busiest day of each provider, first {len(cseeds)} seeds): providers without the impossible-days kind have a median of {st.median(day_honest):.0f}, a 99th percentile of "
              f"{sorted(day_honest)[int(0.99 * len(day_honest))]} and a maximum of {max(day_honest)}; providers with it have a minimum of {min(day_imp)} and a median of {st.median(day_imp):.0f}."]
    L += ["", f"Members seen by two or more providers: {st.mean(shared):.0%}." if shared else "", "", "## How the frozen screens rank true overpayment", "",
          f"Top-10% lists (22 providers) of the first {len(cseeds)} seeds: NDCG at 22 on true overpayment (linear gain) and the share of the dollars in the list.", "",
          "| Screen | Gain | NDCG@22 | Share of dollars in the list |", "|---|---|---|---|"]
    for (method, kind), vals in screen_rows.items():
        L.append(f"| {method} | {kind} | {st.mean(v['ndcg@22'] for v in vals):.2f} | {st.mean(v['share@22'] for v in vals):.0%} |")
    L += ["", "## What a returned chart shows", "", "How the chart reads (the supported level by the decision-making or time rule, as the arms read it) against the billed level, over every rendered visit of the seeds above.", "",
          "| Visits | Count | Chart shows the upcoding (reads lower than billed) | Reads as billed | Reads higher than billed |", "|---|---|---|---|---|"]
    order = [g for g in sorted(reading) if g not in ("correctly billed", "downcoded", "honest noise, upcoded")] + ["honest noise, upcoded", "correctly billed", "downcoded"]
    for g in order:
        c = reading.get(g)
        if not c:
            continue
        n = sum(c.values())
        L.append(f"| {g} | {n:,} | {c['lower'] / n:.0%} | {c['as billed'] / n:.0%} | {c['higher'] / n:.0%} |")
    L += ["", "## Drift over the year", "", "Share of a habit provider's upcoded visits dated in the second half of 2024, against the share of all its visits in that half.", "", "| Habit | Upcoded visits in H2 | All visits in H2 |", "|---|---|---|"]
    for h, (a, b, c_, d_) in sorted(drift.items()):
        L.append(f"| {h} | {a / max(b, 1):.0%} | {c_ / max(d_, 1):.0%} |")
    open(OUT, "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 20)
