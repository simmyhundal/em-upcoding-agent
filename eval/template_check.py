"""Detect templated or near-duplicate case summaries.

A run where most rationales are filled from a template makes quality scores meaningless. This reports two things:
  * boilerplate share: after replacing numbers, claim IDs and provider IDs with placeholders, a sentence that appears
    in at least BOILERPLATE_MIN_SHARE of all summaries is boilerplate; the metric is the average share of each
    summary's sentences that are boilerplate;
  * pairwise similarity: word-3-gram Jaccard similarity between normalised rationales (median and 90th percentile).
A run is flagged when the average boilerplate share or the 90th-percentile similarity is high. A single shared caveat
sentence (for example "no clinical documentation is in the packet") is normal and does not trip the flag on its own.

Usage:
    python eval/template_check.py CHECKED_SUMMARIES_JSONL
"""
import itertools
import json
import re
import sys
from collections import Counter

BOILERPLATE_MIN_SHARE = 0.40
FLAG_BOILERPLATE_SHARE = 0.30
FLAG_P90_SIMILARITY = 0.50
MIN_SUMMARIES = 5


def normalise(text):
    s = text.lower()
    s = re.sub(r"\bc\d{7}\b", "#id", s)
    s = re.sub(r"\bp\d{4}(?:-n\d{4})?\b", "#pid", s)
    s = re.sub(r"\d+(?:\.\d+)?%?", "#", s)
    return re.sub(r"\s+", " ", s).strip()


def sentences(text):
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+", text) if len(x.strip()) > 3]


def shingles(text, k=3):
    words = normalise(text).split()
    return {" ".join(words[i:i + k]) for i in range(max(1, len(words) - k + 1))}


def check(rationales):
    n = len(rationales)
    if n < MIN_SUMMARIES:
        return {"n": n, "flagged": False, "note": f"fewer than {MIN_SUMMARIES} summaries; check skipped"}
    per = [[normalise(x) for x in sentences(r)] for r in rationales]
    freq = Counter(s for sl in per for s in set(sl))
    boiler = {s for s, c in freq.items() if c / n >= BOILERPLATE_MIN_SHARE}
    shares = [sum(1 for s in sl if s in boiler) / len(sl) for sl in per if sl]
    sh = [shingles(r) for r in rationales]
    sims = sorted(len(a & b) / len(a | b) for a, b in itertools.combinations(sh, 2))
    out = {"n": n, "boilerplate_sentences": len(boiler),
           "mean_boilerplate_share": sum(shares) / len(shares),
           "median_similarity": sims[len(sims) // 2], "p90_similarity": sims[int(len(sims) * 0.9)]}
    out["flagged"] = out["mean_boilerplate_share"] >= FLAG_BOILERPLATE_SHARE or out["p90_similarity"] >= FLAG_P90_SIMILARITY
    return out


def describe(res):
    if "note" in res:
        return res["note"]
    verdict = "TEMPLATED - do not score quality on this run" if res["flagged"] else "no templating detected"
    return (f"{verdict} (boilerplate share {res['mean_boilerplate_share']:.0%}, "
            f"similarity median {res['median_similarity']:.2f} / p90 {res['p90_similarity']:.2f})")


if __name__ == "__main__":
    recs = [json.loads(line)["summary"]["rationale"] for line in open(sys.argv[1]) if line.strip()]
    print(describe(check(recs)))
