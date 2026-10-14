"""Deterministic number check for case summaries (replaces the model's job of "do the numbers match the packet?").

Pulls every number out of a summary's text (headline, rationale, next steps) and checks each against the numbers the model was
shown: the evidence card, the packet it was built from, and the facts code stated. Claim IDs, provider and patient IDs, CPT and
ICD codes and dates are ignored. A number matches if it equals a packet number to the precision written (3.4 matches 3.44), or
a packet fraction written as a percentage (0.143 matches 14.3% or 14%). Anything else is reported as unverified: it may be a
slip, or an honest derived figure (a sum or ratio) the model computed itself; a reviewer decides which.

Usage:
    python eval/numcheck.py   # runs a self-check
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
import summary_rules as sr  # noqa: E402

IGNORE = [r"\bC\d{7}\b", r"\bP\d{4}(?:-N\d{4})?\b", r"(?<![\w.])\d{5}(?!\d)", r"\b\d{10}\b", r"\b[A-Z]\d{2}(?:\.\d+)?\b", r"\b\d{4}-\d{2}-\d{2}\b",
          r"\b[A-Z]\d{2}\.\d+\b"]
NUM = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?")


def _strip(text):
    for pat in IGNORE:
        text = re.sub(pat, " ", text)
    return text


def numbers_in(text):
    """[(value, decimals, literal)] for each number in text."""
    out = []
    for m in NUM.finditer(_strip(text)):
        whole, frac = m.group(1).replace(",", ""), m.group(2) or ""
        out.append((float(whole + frac), len(frac) - 1 if frac else 0, m.group(0)))
    return out


def _collect(obj, acc):
    if isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        acc.add(float(obj))
    elif isinstance(obj, str):
        for v, _, _ in numbers_in(obj):
            acc.add(v)
    elif isinstance(obj, dict):
        for v in obj.values():
            _collect(v, acc)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _collect(v, acc)


def allowed_numbers(packet, extra_text=""):
    acc = set()
    _collect(extra_text, acc)
    _collect(packet, acc)
    _collect(sr.to_card(packet), acc)
    _collect(sr.facts(packet), acc)
    return acc


def _matches(v, d, allowed):
    tol = 0.5 * 10 ** -d + 1e-9
    return any(abs(a - v) <= tol or abs(a * 100 - v) <= tol or abs(a - v * 100) <= tol * 100 for a in allowed)


def verify(summary, packet, extra_text=""):
    """extra_text: tool outputs the author saw (judge v2); numbers in them count as matched."""
    text = " ".join([summary["headline"], summary["rationale"], *summary["next_steps"]])
    allowed = allowed_numbers(packet, extra_text)
    nums = numbers_in(text)
    bad = sorted({lit for v, d, lit in nums if not _matches(v, d, allowed)})
    return {"numbers": len(nums), "unverified": bad}


if __name__ == "__main__":
    pk = {"n_claims": 621, "share_99215": 0.1423, "documentation_review": {"by_billed_level": []}}
    allowed = {621.0, 0.1423}
    assert _matches(14.2, 1, allowed) and _matches(14, 0, allowed) and _matches(621, 0, allowed) and not _matches(15.9, 1, allowed)
    assert [lit for _, _, lit in numbers_in("C0012345 billed 99215 for P0001-N0012 on 2024-03-02 (E11.9): 3 of 12, 1,234")] == ["3", "12", "1,234"]
    assert [lit for _, _, lit in numbers_in("The 99215s from 1000000043 and 99214 claims, 7 of them")] == ["7"]
    print("numcheck self-check ok")
