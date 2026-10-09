# Payment Integrity dossier: P0002

> Draft for human review. Statistical and records-sample evidence only; not a finding. Compliance or legal review is needed before any provider contact, notice or recoupment.

## Provider overview

| | |
|---|---|
| Specialty / state | Family Practice, GA (synthetic) |
| Claims / patients | 250 / 99 |
| Billed mix (99211 to 99215) | 2 / 2 / 51 / 149 / 46 |
| 99215 share | 18.4% |
| Expected 99215 share given patient complexity | 2.8% |
| Screen scores | z vs peers 1.98; risk-adjusted 5.40; flagged by zscore+riskadj |

## Case summary (advisory)

**Family Practice provider P0002: 99215 share of 18.4% (2.8% expected for this panel), with 11 of 15 documented 99215 claims not supported by the records; pattern consistent with upcoding**

Leaning: pattern consistent with upcoding. Citations checked: 11/11 valid.

P0002 billed 46 of 250 claims (18.4%) as 99215, against 2.8% expected for this patient mix. The excess sits in low-complexity patients. The 99215 share is 18.0% for patients with 0 chronic conditions (all-provider rate 2.1%) and 21.8% for patients with 1 condition (3.4%). For patients with 4 or more conditions it is 14.3%, about the same as peers (13.9%). The sampled low-complexity 99215 claims include visits coded only for routine problems, such as C0000476 (upper respiratory infection, J06.9), C0000498 (follow-up, Z09), C0000462 (rash, R21) and C0000437 (low back pain, M54.50). The records review is the strongest evidence. Of 15 documented 99215 claims, 11 (73.3%) were not supported, against 24.2% for all providers. Examples are C0000455, C0000469 and C0000481, each documented at moderate MDM with 31 to 33 minutes. The 99214 unsupported rate is also high: 16.7% against 8.4%. Some 99215 claims are supported, including C0000541 and C0000593 (high MDM, 42 to 46 minutes), and the high-complexity 99215 claims C0000511 and C0000631 appear plausible. Records exist for only 28.4% of claims, and 15 documented 99215 claims is a modest sample, but the gap from peers is large. Overall the pattern is consistent with upcoding, not with a sicker panel.

## Evidence chart

![99215 share by patient complexity](../../charts/P0002.svg)

## Records-review sample so far

Documentation is on file for 71 claims (28% of this provider's claims).

| Billed | Documented | Documentation below billed level | Rate | All-provider rate |
|---|---|---|---|---|
| 99213 | 19 | 1 | 5.3% | 7.5% |
| 99214 | 36 | 6 | 16.7% | 8.4% |
| 99215 | 15 | 11 | 73.3% | 24.2% |

## Recommended next steps for Payment Integrity

1. Request records for the sampled claims in `record_request_list.csv` (28 claims across 99215).
2. Review the records against E/M documentation rules and record the supported level for each claim.
3. Run the overpayment estimator on the reviewed sample (`sampling_plan.md` explains how).
4. Notice, appeal rights, recoupment, education or corrective action, and any referral are decisions for the PI team, compliance and counsel. Nothing here drafts those.

Suggested follow-ups from the case summary:

- Pull the full records for all 46 billed 99215 claims, starting with those on patients with 0 or 1 chronic condition. Check whether MDM or total time meets the 99215 threshold.
- Expand the records review beyond the current 28.4% sample, especially for 99215 and 99214 claims, to confirm the 73.3% and 16.7% unsupported rates.
- Check for template-driven or cloned notes and for time padding, since unsupported claims cluster at 31 to 33 documented minutes with moderate MDM.
- Compare billing patterns across the same patients over time (for example P0002-N0081: 99213 on C0000417, then 99215 on C0000625), looking for level jumps without any change in condition.
- Check whether the provider's 99214 billing is also inflated, since its unsupported rate is about double the all-provider rate.

## Limits

- Synthetic data; no real claims or providers.
- The leaning is advisory. The flag comes from the statistical screen; the summary explains it.
- The records-review sample is partial and was simulated for this project.
- Allowed amounts are GA Family Practice averages from a public CMS file, not this provider's actual payments.
