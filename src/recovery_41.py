"""Score 4.1 (S4.1), first step (issue 146): score 4.0's pricing with a plan-type PROFILE on top. Nothing in recovery_40.py changes; S4.0 stays frozen so every S4.0 number stays comparable.

Profiles (each is score 4.0's parameter dict with overrides; the source or "assumption" of every override is in docs/score_41.md):
  medicare_like         score 4.0 exactly: records copy fee $90 per request round (CMS Transmittal 786, a Medicare contractor pays the provider for copies).
  commercial_no_copy    copy fee $0: many commercial provider contracts require records for audits at no charge (ASSUMPTION, not yet checked against contracts; issue 146).
Later steps of S4.1 (look-back window, extrapolation allowed by contract, appeals, collection rate, SIU hours cap) add profiles or parameters here.
"""
import recovery_40 as r4

PROFILES = {"medicare_like": {}, "commercial_no_copy": {"C_COPY": 0.0}}
DEFAULT_PROFILE = "commercial_no_copy"


def params41(profile=DEFAULT_PROFILE, **over):
    """Parameter dict for score 4.1 under a profile; pass it as `p` to the score 4.0 functions (recovery_40.recovery, staff_cost; eval/score_40.from_run)."""
    return r4.params(**{**PROFILES[profile], **over})
