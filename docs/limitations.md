# Limitations

[Back to the README](../README.md)



## Limitations
- **Version 1 only: the inputs were unrealistic and the AI saw records a payer would not have yet.** A payer normally screens on claims data alone. Medical records (the equivalent of this project's `documentation.csv`) reach a payer only after it requests them from the fee-for-service primary care physician, and that request usually comes after a provider is already suspected. Here, a records sample is handed to the AI *before* it decides. It stands in for a first records request, but the order of events is not how it works in practice.
- **Why that matters.** The AI's filtering power comes largely from that sample. With it the AI accused 0 of 17 honest doctors; without it (the chat-session runs) it accused 14 of 17. So read the results as what the AI can do once records are in hand, not as detection from claims alone. Put another way, in version 1 the AI turns a records sample into a cited, checkable case file, and it is also the filter that decides which flagged doctors move on, but its accuracy rests on that sample.
- **Fixed in versions 2 and 3.** [Milestone 5](https://github.com/simmyhundal/em-upcoding-agent/milestone/5) rebuilt the inputs the way a payer would receive them and models records requests as a later step. The "Does it work?" results are version 1; versions 2 and 3 are in the sections below and in the Eval table.
- **The documentation signal is cleaner than real records.** In this data the documented level is a noisy copy of the hidden truth, and the documented minutes are filled in to match it exactly, so time never disagrees with the decision-making level. Real records are messier: upcoding practices may also inflate the documentation, and time and decision making are recorded independently. Version 2 addresses this (separate MDM elements, independent time, cloned notes); it is used for the version 2 and version 3 results.
- **Other limits.** Synthetic data from one generator; two seeds; the usefulness score comes from an AI grader and is below its target; the citation check confirms cited visits exist, not that each one supports its sentence.

