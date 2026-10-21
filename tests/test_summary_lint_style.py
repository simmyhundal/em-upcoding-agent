"""The two judged writing defects (issue 116): style_defects finds them, style_repair removes them and never changes the leaning, and lint(style=True) refuses them while the default lint is unchanged.
Run: python tests/test_summary_lint_style.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "src"))
import summary_lint as sl  # noqa: E402

BAD = {"headline": "5 of 5 charts support a lower level; 67% below billed", "rationale": "Provider billed 99215 on 16.4% of claims against 4.0% expected. Provider billed 99215 on 17.4% of claims against 5.0% expected. Done here.",
       "leaning": "pattern_consistent_with_upcoding", "next_steps": [], "cited_claim_ids": []}


def test_defects_are_found_and_clean_text_has_none():
    d = sl.style_defects(BAD)
    assert any(x.startswith("headline figures") for x in d) and "a sentence is repeated" in d
    ok = {**BAD, "headline": "Provider billed 99215 on 16.4% of claims", "rationale": "Provider billed 99215 on 16.4% of claims against 4.0% expected. Other facts follow in this second sentence."}
    assert sl.style_defects(ok) == []


def test_lint_style_flag_moves_the_defects_into_hard_and_default_is_unchanged():
    saved = (sl.summary_numbers.verify, sl.leaning_supported, sl.contradictions, sl.unreliable_estimate_quoted)
    sl.summary_numbers.verify = lambda s, p, e: {"unverified": []}                  # isolate the style checks from the evidence checks
    sl.leaning_supported, sl.contradictions, sl.unreliable_estimate_quoted = (lambda *a, **k: True), (lambda s, p: []), (lambda s, e: False)
    try:
        text = {**BAD, "headline": "ok", "next_steps": ["x"]}
        default = sl.lint(text, {})
        assert "a sentence is repeated" in default["soft"] and "a sentence is repeated" not in default["hard"]
        assert "a sentence is repeated" in sl.lint(text, {}, style=True)["hard"]
    finally:
        sl.summary_numbers.verify, sl.leaning_supported, sl.contradictions, sl.unreliable_estimate_quoted = saved


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
