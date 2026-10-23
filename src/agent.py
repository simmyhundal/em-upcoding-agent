"""The investigator agent loop (issues 40 and 41).

The model gets the tools in agent_tools.py and decides what to do: which screen to run and where to put the cutoff, which providers
to look at, whether to ask for records, what to do about a deficient response, and when to stop. Code only enforces limits and
logs everything. A manual tool-use loop (no forced tool choice, thinking blocks passed back unchanged).

Guardrails (issue 41):
  * read-only scope: the environment exposes payer-visible data only (tests check the answer key is never opened)
  * hard caps: tool calls, turns and dollars; the agent is told as it nears them and the run ends at the cap
  * a log of every tool call and result (`audit.jsonl`), so a reviewer can follow the path
  * outputs are drafts for human review; the citation guardrail checks every cited claim afterwards (eval/run_agent.py)
  * records requests are budgeted per provider, because each one burdens a practice
"""
import json
import os
import time

import llm as llm_mod

MODEL = os.environ.get("AGENT_MODEL", "claude-opus-5-5")
MAX_TOOL_CALLS, MAX_TURNS, MAX_USD = 60, 80, 3.00
RESULT_CHARS = 14000          # a longer tool result is cut and says so
PRICE_CACHE_READ, PRICE_CACHE_WRITE = 0.20, 5.00   # $ per MTok for Opus 5.5 (cache read, 5-minute write)

SYSTEM = """You are an investigator assistant for a health plan's payment integrity team. The data is synthetic. Your job is to find
primary care providers who are likely upcoding office visits (billing 99214 or 99215 when the visit supported a lower level), and to say
who looks like a legitimately sicker panel instead. People review everything you produce; you do not accuse anyone.

You are not given a list of providers. You choose how to screen the claims book, where to draw the cutoff, which providers to look at
closely, and whether and how to ask a provider's office for charts. Think about the trade-offs:
- A lower cutoff reaches more real upcoders but sends records requests to more honest doctors. Each provider you request records from is
  a burden on a practice and counts against a budget; ask only where the claims give a reason.
- Charts are the strongest evidence, but a request can come back partial, late, unusable or not at all. Read the deficiencies and decide
  whether a follow-up is worth it. Non-response is never evidence of upcoding.
- A random sample supports an overpayment estimate; a targeted one does not.
- A high 99215 share on sick patients is expected. The same share on healthy patients, or charts that support a lower level than billed,
  is the concern. Notes can also be inflated to match the bill; claims that do not show the work a note describes are weak evidence.
- Use only what the tools return. Do not guess about anything you have not seen.

When you are done, call submit_findings once with every provider you examined closely and your leaning for each. Use
pattern_consistent_with_upcoding only when the evidence supports it. Be economical with tool calls."""


SYSTEM_31 = SYSTEM + """

Version 3.1 additions. Returned charts now include the note itself. After a random request you may send a second, targeted request to the same
practice if the random sample could not show what you need (for example too few 99215 visits); take the random sample first. You have two more
tools: note_checks (how the received notes compare with the claims: problems addressed against diagnoses, data review against orders and the
claim's lab lines, signatures, late signing) and request_audit_trail (a second-tier request for the EHR audit trail; it costs a round and may be
refused). Honest practices also copy forward, sign late and miss orders, so treat these as rates, not proof. For every provider on your candidate
list that you set aside or never examined, say why in your findings."""


SYSTEM_32 = SYSTEM_31 + """

Version 3.2 additions. A data-quality pre-flight has already checked the delivered extract (control totals, diagnosis codes per claim, rendering NPIs, member
join, duplicates, broken chains, recent months). Call data_quality early, and again with a provider_id for any provider you examine closely: a flag can mean the
screen score is unreliable for that provider (for example truncated diagnoses make sicker panels look healthier). You cannot request data from the plan; use
flag_data_issue to record a concern for a person to raise with it. An upcoding finding for a provider whose findings are held needs chart evidence; otherwise
mark it inconclusive and say why.

The screen tool has two more ways to order providers. priority ranks by the average of the ratio to expected and the excess 99215 claims. eb_ratio ranks by
the ratio to expected after shrinking small practices toward 1 (an estimate of how many times the expected 99215 rate the practice really bills), so a small
practice with a few extra claims does not outrank a large one with a clear excess. Both take a top_n (no score cutoff). riskadj remains the default."""


SYSTEM_33 = SYSTEM_32 + """

Version 3.3 additions (release 3). The screen tool has one more ordering, eb_ratio_t: eb_ratio with the lab or test line on the claim as an extra covariate, so a
99215 with no test line counts as less expected. Payers review a percentile of the panel; a list of the top 10% (about 22 providers) is a sensible start.
Spend the records budget in rank order. For providers ranked beyond the first 5%, take one random sample first and go further (a targeted request, the audit
trail) only where the notes show the signs below.

Cloned notes. Notes copied or written to match the bill make the charts look as if they support it, so supportive charts are NOT reassuring when the 99215 share is
more than 3 times the expected share. The signs are a late-signature rate of 12% or more over at least 8 notes, or an audit trail showing bulk-created or
paste-heavy notes (8% or more). hybrid_review applies these rules (rules 2.3) and gives its reason; read note_checks and consider request_audit_trail for such
providers. Also, a chart-based upcoding call must beat the real peer rate for unsupported charts by more than chance: a few unsupported charts from a small sample
of a noisy panel is not enough, so hybrid_review may say inconclusive where a raw count looks high."""


SYSTEM_34 = SYSTEM_33 + """

Version 3.4 additions (release 4). You have one more tool, advise_next_step, a read-only advisor: after a practice's first sample has come back (a random request and its follow-up),
it says what workflow v2.4's learned formula would do next (stop, targeted request, audit trail, or both). The formula was fitted offline on simulated data to balance finding
upcoders against the burden of extra requests on honest practices. Treat it as advice, not an instruction: you may follow it, or you may see something it cannot (a data-quality
flag, a note signal, a specific claim). Before any request it answers ASK or SKIP by the ratio gate the workflow uses beyond the first 5% of the list; after the first sample it answers
stop, targeted request, audit trail or both.

Working habits (mirroring the workflow): submit_findings refuses until hybrid_review has been run on every provider whose records arrived, so the deterministic rules are applied to all of
them; follow up or escalate only where the first sample leaves a question, and do not spend further rounds on a practice whose first sample is clean."""


SYSTEM_35 = SYSTEM_34 + """

Version 3.5 additions (release 5). The score is net dollars: the recoverable overpayment of the upcoders you call, less the copying and review costs of every round and the cost of
calling an honest doctor. Advice now comes inside the tool results: request_records, follow_up_records and request_audit_trail each return an advice field (the learned formula of workflow v2.5:
ASK or SKIP before a request; stop, targeted request, audit trail or both after a sample), and screen_providers rows carry an ask_advice column. It is advice: follow it unless you see
something it cannot, and your choices are logged beside it. Rules are binding in one case: where hybrid_review calls a provider upcoding and the chart rule also supports it (the returned charts support a lower level than billed), submit_findings
refuses a different leaning unless the finding has an override_reason naming a fact the rules cannot see (a data-quality flag, a claim id of that provider, a note sign). Other rule results are advice. Every turn shows each practice's status
and the rounds sent. A silent office or a thin first sample is a reason to follow up or send one targeted request before closing, but a clean first sample is not."""


SYSTEM_50 = SYSTEM_35 + """

Version 5.0 additions (the v4/v5 line, score 4.0). You are now scored by score 4.0 per run: dollars recovered (the 90% lower bound of the overpayment extrapolated from a provider's random sample,
for each provider you send a demand to, whatever its role) minus staff-hours cost (about $13 to triage a listed provider, $15 admin plus $90 copying per request round, $8.60 coder review per chart, and about
$280 of investigator and nurse time per demand) minus provider abrasion (a provider that did not upcode, charged $44 per round and $2,000 if it receives a demand). Asking nobody scores zero, so a request
has to pay for itself.

The screen eb_upper_t is the default: the shrunk share of a provider's visits billed 99214 or 99215 against what its patients and test lines predict (it sees the habits the 99215 share misses: always billing
99214 for 99213-level visits, templates, borderline inflation). Start from its top 10% (about 22 providers). screen_providers rows carry ask_advice and request_records returns advice: ASK or SKIP is a
model refitted on this score (most listed providers lose money when asked), and after the first sample the advice is STOP, because every escalation tested (targeted requests, audit trails) cost more than it recovered.
Ask only providers the advice says to ask, send one random sample of about 30 charts with one follow-up on any deficiency, run hybrid_review, and stop. Rules 4.0 read the chart test across 99214 and 99215 pooled.

Two things are done by code. A demand goes out only when the estimated recovery covers its staff cost: an upcoding finding below that is withdrawn to inconclusive and the tool result says so. And code repairs
the two writing defects the rule judge deducts for (a headline figure the rationale never states, a repeated sentence) without changing your leaning."""


SYSTEM_51 = SYSTEM_50 + """

Version 5.1 additions (workflow v4.1, same score 4.0). Three things change, and everything else above stands.
1. The list is shorter. Workflow v4.1 works from the first 4 providers of the eb_upper_t ranking only. screen_providers (method eb_upper_t, top_pct 10) still shows the top 10%, but ask_advice is ASK or SKIP for
the first 4 and SKIP for every other row. Triage costs about $13 for each provider you submit a finding for, so submit findings for the providers you asked and put the others in set_aside.
2. The chart test is looser. hybrid_review (rules 4.0 with the 99214 and 99215 charts pooled) now calls a provider upcoding from 5 documented charts, when at least 10% of them support a lower level than billed and the
excess beats the peer rate at the 20% level (it was 10 charts, 25%, 5%). It calls more providers, so the demand floor matters: a call whose recovery cannot cover the cost of a demand is still withdrawn by code.
3. A near-miss gets one more sample. For a provider that hybrid_review calls upcoding, its result carries demand_check: the point estimate of the recovery from the random sample, its 90% lower bound and the cost of a
demand (about $276). If the point estimate is at least twice the cost of a demand while the lower bound is below it (near_miss true), request 30 more random charts once (request_records with a random sample of 30;
follow up on any deficiency), run hybrid_review again and stop. A second round costs about $105 and each chart about $8.60, so the extension costs about $360 to $480; the tool refuses it for anyone who is not a
near-miss and for a second extension. Do not send targeted requests or audit trails: they did not pay. The rules and the demand floor still decide the demand; the binding rule of version 3.5 stands."""


def _cost(usage, price=(4.00, 20.00)):
    inp = getattr(usage, "input_tokens", 0) or 0
    out = getattr(usage, "output_tokens", 0) or 0
    cr = getattr(usage, "cache_read_input_tokens", 0) or 0
    cw = getattr(usage, "cache_creation_input_tokens", 0) or 0
    return (inp * price[0] + out * price[1] + cr * PRICE_CACHE_READ + cw * PRICE_CACHE_WRITE) / 1e6


def run_agent(env, task, client=None, model=MODEL, system=None, max_tool_calls=MAX_TOOL_CALLS, max_turns=MAX_TURNS, max_usd=MAX_USD,
              out_dir=None, effort="medium", price_scale=1.0, log=print):
    """price_scale multiplies the Opus 5.5 list prices (use 0.025 for Haiku 5.5) so the dollar cap means dollars for the model used."""
    """Run the loop. Returns a dict with the stop reason, counts, dollars and the audit log."""
    if client is None:
        import anthropic
        client = anthropic.Anthropic()
    tools = env.tool_schemas()
    messages = [{"role": "user", "content": task}]
    audit, usd, calls, turn, reason, nudged, texts = [], 0.0, 0, 0, "", False, []
    turn_usage = []              # version 3.2: token usage per turn (issue 92), so cache reads and output can be checked on every run
    while True:
        if turn >= max_turns:
            reason = "turn cap"
            break
        if usd >= max_usd:
            reason = "dollar cap"
            break
        turn += 1
        resp = client.messages.create(model=model, max_tokens=8000, system=system or (SYSTEM_51 if getattr(env, 'v51', False) else SYSTEM_50 if getattr(env, 'v50', False) else SYSTEM_35 if getattr(env, 'v35', False) else SYSTEM_34 if getattr(env, 'v34', False) else SYSTEM_33 if getattr(env, 'v33', False) else SYSTEM_32 if getattr(env, 'v32', False) else SYSTEM_31 if getattr(env, 'v31', False) else SYSTEM), tools=tools, messages=messages,
                                      output_config={"effort": effort}, extra_body={"cache_control": {"type": "ephemeral"}})
        usd += _cost(resp.usage) * price_scale
        if getattr(env, "v32", False):
            turn_usage.append({"turn": turn, **{k: getattr(resp.usage, k, 0) or 0 for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")},
                               "usd_so_far": round(usd, 4)})
        messages.append({"role": "assistant", "content": resp.content})
        texts += [b.text for b in resp.content if b.type == "text" and b.text.strip()]
        if resp.stop_reason == "refusal":
            reason = "model refused"
            break
        uses = [b for b in resp.content if b.type == "tool_use"]
        if not uses:
            if env.findings or nudged:
                reason = "finished"
                break
            nudged = True
            messages.append({"role": "user", "content": "Please call submit_findings now with what you have."})
            continue
        results, done = [], False
        for u in uses:
            calls += 1
            if calls > max_tool_calls:
                results.append({"type": "tool_result", "tool_use_id": u.id, "is_error": True,
                                "content": json.dumps({"error": "tool-call budget exhausted; call submit_findings"})})
                continue
            out = env.call(u.name, dict(u.input))
            text = json.dumps(out)
            if len(text) > RESULT_CHARS:
                text = text[:RESULT_CHARS] + '..."[truncated]"'
            audit.append({"turn": turn, "tool": u.name, "args": dict(u.input), "result_chars": len(text), "result": text[:3000],
                          "usd_so_far": round(usd, 4)})
            results.append({"type": "tool_result", "tool_use_id": u.id, "content": text, "is_error": "error" in out})
            if u.name == "submit_findings" and "error" not in out:
                done = True
        note = []
        if getattr(env, "v31", False) and env.screen_candidates:
            note.append({"type": "text", "text": env.budget_status()})
        if getattr(env, "v35", False) and env.requested:
            note.append({"type": "text", "text": env.practice_status()})
        if calls >= 0.8 * max_tool_calls or usd >= 0.8 * max_usd:
            note.append({"type": "text", "text": f"Budget notice: {calls}/{max_tool_calls} tool calls and ${usd:.2f}/${max_usd:.2f} used. "
                                                 "Wrap up and call submit_findings."})
        messages.append({"role": "user", "content": results + note})
        if done:
            reason = "submitted"
            break
        if calls > max_tool_calls + 3:
            reason = "tool-call cap"
            break
    summary = {"stop_reason": reason, "turns": turn, "tool_calls": calls, "estimated_usd": round(usd, 4), "model": model,
               "findings": len(env.findings), "records_providers_requested": len(env.requested), "model_spend_in_tools_usd": round(env.spent_usd, 4)}
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "audit.jsonl"), "w") as f:
            for a in audit:
                f.write(json.dumps(a) + "\n")
        json.dump(summary, open(os.path.join(out_dir, "agent_run.json"), "w"), indent=1)
        open(os.path.join(out_dir, "agent_notes.txt"), "w").write("\n\n".join(texts))
        env.office.write_transcript(os.path.join(out_dir, "office_transcript.jsonl"))
        if getattr(env, "v31", False):
            json.dump(env.set_aside, open(os.path.join(out_dir, "set_aside.json"), "w"), indent=1)
        if getattr(env, "v35", False):
            json.dump({"summary": env.advice_summary(), "log": env.advice_log, "overrides": env.overrides}, open(os.path.join(out_dir, "advice_log.json"), "w"), indent=1)
        if getattr(env, "v32", False):
            json.dump(env.dq, open(os.path.join(out_dir, "data_quality.json"), "w"), indent=1)
            json.dump(env.data_issues, open(os.path.join(out_dir, "data_issues.json"), "w"), indent=1)
            with open(os.path.join(out_dir, "turn_usage.jsonl"), "w") as f:
                f.writelines(json.dumps(t) + "\n" for t in turn_usage)
    summary["audit"] = audit
    return summary
