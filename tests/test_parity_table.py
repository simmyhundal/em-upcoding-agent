"""The features-mirror rule (docs/versioning.md): every row of every release's feature table has both a workflow and an agent cell, and a row that is one-sided (n/a, not built,
moved, do not build, or built in only one stream) states a reason. Run: python tests/test_parity_table.py"""
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ONE_SIDED = re.compile(r"^\s*(n/a|not built|moved|do not build|\*\*do not build\*\*)", re.I)


def problems(text):
    """List of problems in the feature tables of a versioning page: tables whose header starts with 'Feature' and has four columns (feature, workflow, agent, reason)."""
    out, lines = [], text.splitlines()
    i = 0
    while i < len(lines):
        head = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        if lines[i].startswith("|") and head and head[0].lower().startswith("feature") and len(head) == 4 and i + 1 < len(lines) and set(lines[i + 1].replace("|", "").strip()) <= set("-: "):
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                name = cells[0] if cells else "?"
                if len(cells) != 4:
                    out.append(f"{name}: expected 4 cells, found {len(cells)}")
                else:
                    feat, w, a, why = cells
                    if not w or not a:
                        out.append(f"{feat}: a stream has no cell")
                    elif (ONE_SIDED.match(w) or ONE_SIDED.match(a)) and not why:
                        out.append(f"{feat}: one-sided without a stated reason")
                j += 1
            i = j
        else:
            i += 1
    return out


def test_every_feature_row_has_both_streams_and_a_reason_when_one_sided():
    assert problems(open(os.path.join(ROOT, "docs", "versioning.md")).read()) == []


def test_the_check_catches_the_failures_it_is_for():
    head = "| Feature | v9.0 workflow | v9.0 agent | Reason if one-sided |\n|---|---|---|---|\n"
    assert problems(head + "| ok | built | built | |\n| ok2 | n/a: no loop | built | agent loop only |\n") == []
    assert any("no cell" in p for p in problems(head + "| missing agent | built |  | |\n"))
    assert any("without a stated reason" in p for p in problems(head + "| one sided | built | not built | |\n"))
    assert any("without a stated reason" in p for p in problems(head + "| na | n/a | built | |\n"))
    assert any("expected 4 cells" in p for p in problems(head + "| short | built | built |\n"))


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
