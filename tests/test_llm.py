"""Tests for the shared LLM layer with a fake Anthropic client (no API call). Run: python tests/test_llm.py"""
import json
import os
import sys
import tempfile
from types import SimpleNamespace as NS

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import llm  # noqa: E402

SCHEMA = {"type": "object", "properties": {"a": {"type": "string"}}, "required": ["a"], "additionalProperties": False}


def _msg(text, stop="end_turn", i=100, o=20):
    return NS(stop_reason=stop, content=[NS(type="text", text=text)], usage=NS(input_tokens=i, output_tokens=o))


class FakeClient:
    """Mimics the batch calls we use; `refuse` makes one request come back refused, `error` makes one error."""
    def __init__(self, refuse=(), error=()):
        self.refuse, self.error, self.batches, self.sync_calls = set(refuse), set(error), [], []
        self.messages = NS(batches=NS(create=self._create, retrieve=lambda bid: NS(processing_status="ended", id=bid),
                                      results=self._results))
        self.beta = NS(messages=NS(create=self._sync))

    def _create(self, requests):
        self.batches.append([r["custom_id"] if isinstance(r, dict) else r["custom_id"] for r in requests])
        self._reqs = requests
        return NS(id="b1")

    def _results(self, bid):
        for r in self._reqs:
            cid = r["custom_id"]
            if cid in self.error:
                yield NS(custom_id=cid, result=NS(type="errored"))
            elif cid in self.refuse:
                yield NS(custom_id=cid, result=NS(type="succeeded", message=_msg("", stop="refusal")))
            else:
                yield NS(custom_id=cid, result=NS(type="succeeded", message=_msg(json.dumps({"a": cid}))))

    def _sync(self, **kw):
        self.sync_calls.append(kw)
        return _msg(json.dumps({"a": "sync"}))


def test_batch_returns_every_request_and_retries_refused_and_errored_synchronously():
    c = FakeClient(refuse={"r2"}, error={"r3"})
    items = [(f"r{i}", "sys", f"user {i}") for i in range(1, 5)]
    out = llm.run_requests(items, "claude-opus-5-5", SCHEMA, cache_dir=None, batch=True, client=c, poll_seconds=0, log=None)
    assert set(out) == {"r1", "r2", "r3", "r4"}
    assert [out[k][2] for k in ("r1", "r2", "r3", "r4")] == ["batch", "sync-retry", "sync-retry", "batch"]
    assert len(c.batches) == 1 and len(c.sync_calls) == 2
    assert c.sync_calls[0]["extra_body"] == {"fallbacks": "default"}          # the refusal retry gets the server-side fallback


def test_cache_makes_a_repeat_run_free_and_a_changed_prompt_a_miss():
    d = tempfile.mkdtemp()
    items = [("r1", "sys", "u1"), ("r2", "sys", "u2")]
    c1 = FakeClient()
    first = llm.run_requests(items, "claude-opus-5-5", SCHEMA, d, True, client=c1, poll_seconds=0, log=None)
    c2 = FakeClient()
    again = llm.run_requests(items, "claude-opus-5-5", SCHEMA, d, True, client=c2, poll_seconds=0, log=None)
    assert [v[0] for v in first.values()] == [v[0] for v in again.values()] and not c2.batches
    assert all(v[2] == "cache" and v[1]["input_tokens"] == 0 for v in again.values())
    c3 = FakeClient()
    llm.run_requests([("r1", "sys", "u1 CHANGED"), ("r2", "sys", "u2")], "claude-opus-5-5", SCHEMA, d, True, client=c3,
                     poll_seconds=0, log=None)
    assert c3.batches == [["r1"]]                                              # only the changed prompt goes out
    c4 = FakeClient()
    llm.run_requests(items, "claude-sonnet-5-5", SCHEMA, d, True, client=c4, poll_seconds=0, log=None)
    assert len(c4.batches[0]) == 2                                             # another model never reuses the cache


def test_cost_and_usage_log():
    assert abs(llm.cost("claude-opus-5-5", 1_000_000, 1_000_000) - 24.0) < 1e-9
    assert abs(llm.cost("claude-opus-5-5", 1_000_000, 1_000_000, batch=True) - 12.0) < 1e-9
    path = os.path.join(tempfile.mkdtemp(), "u.jsonl")
    total = llm.write_usage(path, "claude-sonnet-5-5", [("a", {"input_tokens": 1000, "output_tokens": 500}, "batch"),
                                                         ("b", {"input_tokens": 0, "output_tokens": 0}, "cache")])
    rows = [json.loads(line) for line in open(path)]
    assert len(rows) == 2 and rows[1]["estimated_usd"] == 0 and abs(total - (1000 * 2 + 500 * 10) / 1e6 * 0.5) < 1e-9


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
