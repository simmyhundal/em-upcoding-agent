"""Compare the deterministic judge (v2.1) with the LLM judge (j1, j2) provider by provider, over every run with both scores.

Usage:
    python eval/compare_judges.py
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _rank(v):
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def _pearson(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
    return num / den if den else float("nan")


def main():
    reg = json.load(open(os.path.join(ROOT, "experiments", "runs.json")))
    llm, rules = [], []
    for r in reg["runs"]:
        e = r.get("ai") or r
        if not (e.get("usefulness") and e.get("usefulness_rules")):
            continue
        a = {x["provider_id"]: x["score"] for x in map(json.loads, open(os.path.join(ROOT, e["usefulness"])))}
        b = {x["provider_id"]: x["score"] for x in map(json.loads, open(os.path.join(ROOT, e["usefulness_rules"])))}
        for p in a.keys() & b.keys():
            llm.append(a[p])
            rules.append(b[p])
    n = len(llm)
    print(f"{n} summaries scored by both judges")
    print(f"mean LLM judge {sum(llm) / n:.2f}; mean rule judge {sum(rules) / n:.2f}")
    print(f"Pearson {_pearson(llm, rules):.2f}; Spearman {_pearson(_rank(llm), _rank(rules)):.2f}")
    print("rule score given LLM score:", {k: round(sum(r for l, r in zip(llm, rules) if l == k) / max(sum(1 for l in llm if l == k), 1), 2) for k in range(1, 6)})


if __name__ == "__main__":
    main()
