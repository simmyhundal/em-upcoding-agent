# Payment Integrity dossier: P0095

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 1,015 / 394 |
| Billed mix (99211 to 99215) | 17 / 19 / 406 / 476 / 97 |
| 99215 share | 9.6% |
| Expected 99215 share given patient complexity | 2.3% |
| Screen scores | z vs peers 0.62; risk-adjusted 5.51; flagged by riskadj |

## Case summary (advisory)

**P0095 (Family Practice, GA): 99215 share well above complexity-adjusted expectation, and 25 of 27 documented 99215 claims are unsupported; pattern consistent with upcoding**

Leaning: pattern consistent with upcoding. Citations checked: 8/8 valid.

P0095 billed 99215 on 9.6% of 1,015 claims versus an expected 2.3% given patient complexity (risk-adjusted score 5.51), although the raw peer z-score is only 0.62. The excess is concentrated in the simplest patients. 99215 share is 6.8% at 0 chronic conditions (peers 2.1%) and 11.3% at 1 condition (peers 3.4%). At 4+ conditions the provider is at or below peers. The sampled low-complexity 99215s include routine-looking diagnoses such as URI (C0048602, C0048948), low back pain (C0048625, C0049007) and rash (C0048730). Documentation is the strongest signal. 25 of 27 documented 99215 claims (92.6%) do not support the billed level, against 24.2% across all providers; examples are C0048719 and C0049258, both documented as moderate MDM at about 35 minutes. The 99214 unsupported rate is also elevated (22.1% vs 8.4%). Only a few 99215s are documented as supported (e.g., C0048506, high MDM, 46 minutes). Caveats: 27 documented 99215s is a modest sample, records cover about 30% of claims, documentation is noisy, and the claim lists are random samples. This is a pattern consistent with upcoding, not a finding of fraud.

## Evidence chart

![99215 share by patient complexity](../../charts/P0095.svg)

## Records-review sample so far

Documentation is on file for 303 claims (30% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 132 | 13 | 9.8% | 7.5% |
| 99214 | 131 | 29 | 22.1% | 8.4% |
| 99215 | 27 | 25 | 92.6% | 24.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (41 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Pull full records for the 25 unsupported 99215 claims and confirm MDM level and time against 2021+ E/M guidelines.
- Expand documentation review to more undocumented 99215 claims, prioritizing 0-1 chronic-condition patients, to firm up the 92.6% rate.
- Review the 99214 claims with low documented MDM (e.g., C0049073, C0049119) to assess whether level inflation extends beyond 99215.
- Check whether time-based billing, prolonged services, or same-day procedures could explain any high-level codes.
- Compare this provider's E/M mix over time and against same-practice colleagues for template or EHR-default effects.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
