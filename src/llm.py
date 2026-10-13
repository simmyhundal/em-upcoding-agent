"""Shared Anthropic calls for the writer (case_summary.py) and the judge (eval/judge_usefulness.py).

Four things live here so both steps behave the same way:
  * `sync_call`: one request, with the server-side refusal fallback (not allowed inside a batch).
  * `batch_call`: many requests through the Message Batches API at half price. Nothing here is latency-sensitive, so the
    writer and the judge both use it. A request that errors, expires or is refused inside a batch is retried once
    synchronously (a refusal then gets the server-side fallback); a canceled one raises.
  * a response cache keyed by a hash of (model, effort, max_tokens, schema, system prompt, user prompt), stored under the run
    folder: re-running unchanged inputs costs nothing and returns identical text (Opus 5.5 takes no temperature setting, so this
    is the only way to make a repeat run reproducible). Any change to the model, settings or prompt is a different key, so a
    cache is never reused across prompt or model changes.
  * usage and cost logging: every call's token counts and an estimated dollar cost, so spend is measured, not guessed.

Prices ($ per million tokens, input / output) are the published list prices for the two models used; batch calls are billed at
half. Estimates only: check the Console for the real bill.
"""
import hashlib
import json
import os
import time

FALLBACK_BETA = "server-side-fallback-2026-07-01"
PRICES = {"claude-opus-5-5": (4.00, 20.00), "claude-sonnet-5-5": (2.00, 10.00)}
BATCH_DISCOUNT = 0.5


def cost(model, input_tokens, output_tokens, batch=False):
    pin, pout = PRICES[model]
    usd = (input_tokens * pin + output_tokens * pout) / 1e6
    return usd * (BATCH_DISCOUNT if batch else 1.0)


def _usage(msg):
    u = msg.usage
    return {"input_tokens": u.input_tokens, "output_tokens": u.output_tokens,
            "cache_read_input_tokens": getattr(u, "cache_read_input_tokens", 0) or 0,
            "cache_creation_input_tokens": getattr(u, "cache_creation_input_tokens", 0) or 0}


def _params(model, system, user, schema, max_tokens, effort):
    return {"model": model, "max_tokens": max_tokens, "system": system,
            "messages": [{"role": "user", "content": user}],
            "output_config": {"effort": effort, "format": {"type": "json_schema", "schema": schema}}}


def _text(msg):
    if msg.stop_reason == "refusal":
        raise RuntimeError(f"model refused: {getattr(msg, 'stop_details', None)}")
    return next(b.text for b in msg.content if b.type == "text")


def sync_call(model, system, user, schema, max_tokens=4000, effort="medium", client=None):
    """One request with the server-side refusal fallback. Returns (text, usage)."""
    import anthropic
    client = client or anthropic.Anthropic()
    p = _params(model, system, user, schema, max_tokens, effort)
    resp = client.beta.messages.create(**p, betas=[FALLBACK_BETA], extra_body={"fallbacks": "default"})
    return _text(resp), _usage(resp)


def count_tokens(model, system, user, client=None):
    """Free token count for one request (the call is not billed)."""
    import anthropic
    client = client or anthropic.Anthropic()
    r = client.messages.count_tokens(model=model, system=system, messages=[{"role": "user", "content": user}])
    return r.input_tokens


def batch_call(items, model, schema, max_tokens=4000, effort="medium", client=None, poll_seconds=30, log=None):
    """items: list of (custom_id, system, user). Returns {custom_id: (text, usage, via)}, via in batch|sync-retry."""
    import anthropic
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request
    client = client or anthropic.Anthropic()
    by_id = {cid: (system, user) for cid, system, user in items}
    if not by_id:
        return {}
    batch = client.messages.batches.create(requests=[
        Request(custom_id=cid, params=MessageCreateParamsNonStreaming(**_params(model, s, u, schema, max_tokens, effort)))
        for cid, (s, u) in by_id.items()])
    if log:
        log(f"batch {batch.id} submitted with {len(by_id)} requests")
    while True:
        batch = client.messages.batches.retrieve(batch.id)
        if batch.processing_status == "ended":
            break
        time.sleep(poll_seconds)
    out = {}
    for res in client.messages.batches.results(batch.id):
        cid, r = res.custom_id, res.result
        if r.type == "succeeded" and r.message.stop_reason != "refusal":
            out[cid] = (_text(r.message), _usage(r.message), "batch")
        elif r.type == "canceled":
            raise RuntimeError(f"batch request {cid} was canceled")
        else:                                       # errored, expired or refused: retry once, synchronously
            s, u = by_id[cid]
            text, usage = sync_call(model, s, u, schema, max_tokens, effort, client)
            out[cid] = (text, usage, "sync-retry")
    missing = set(by_id) - set(out)
    for cid in missing:                             # no result returned for a request: retry it too
        s, u = by_id[cid]
        text, usage = sync_call(model, s, u, schema, max_tokens, effort, client)
        out[cid] = (text, usage, "sync-retry")
    return out


def write_usage(path, model, rows):
    """rows: [(custom_id, usage, via)] -> usage jsonl with estimated dollars; returns the total estimate."""
    total = 0.0
    with open(path, "w") as f:
        for cid, usage, via in rows:
            usd = cost(model, usage["input_tokens"], usage["output_tokens"], batch=(via == "batch"))
            total += usd
            f.write(json.dumps({"id": cid, "model": model, "via": via, **usage, "estimated_usd": round(usd, 5)}) + "\n")
    return total


def cache_key(model, system, user, schema, max_tokens, effort):
    blob = json.dumps({"model": model, "effort": effort, "max_tokens": max_tokens, "schema": schema,
                       "system": system, "user": user}, sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()


def run_requests(items, model, schema, cache_dir=None, batch=True, max_tokens=4000, effort="medium", client=None,
                 poll_seconds=30, log=print):
    """items: [(custom_id, system, user)] -> {custom_id: (text, usage, via)}, via in cache|batch|sync|sync-retry.

    Cached requests are answered from `cache_dir` at no cost; the rest go to the API (one batch, or one call each when
    batch=False) and are written back to the cache."""
    out, todo = {}, []
    for cid, system, user in items:
        key = cache_key(model, system, user, schema, max_tokens, effort)
        path = os.path.join(cache_dir, key + ".json") if cache_dir else None
        if path and os.path.exists(path):
            hit = json.load(open(path))
            out[cid] = (hit["text"], {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 0,
                                      "cache_creation_input_tokens": 0}, "cache")
        else:
            todo.append((cid, system, user, path))
    if log and items:
        log(f"{len(items)} requests: {len(items) - len(todo)} from cache, {len(todo)} to the API ({'batch' if batch else 'sync'})")
    if todo:
        if batch:
            got = batch_call([(c, s, u) for c, s, u, _ in todo], model, schema, max_tokens, effort, client, poll_seconds,
                             log=log)
        else:
            got = {}
            for c, s, u, _ in todo:
                text, usage = sync_call(model, s, u, schema, max_tokens, effort, client)
                got[c] = (text, usage, "sync")
        for cid, _, _, path in todo:
            out[cid] = got[cid]
            if path:
                os.makedirs(cache_dir, exist_ok=True)
                json.dump({"text": got[cid][0]}, open(path, "w"))
    return out
