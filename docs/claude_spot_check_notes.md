# A reading of the spot-check sheet by Claude (not a person)

[Back to the README](../README.md)

Issues [#93](https://github.com/simmyhundal/em-upcoding-agent/issues/93) and [#19](https://github.com/simmyhundal/em-upcoding-agent/issues/19) need a person's judgment of the 25 summaries in `docs/human_spot_check.csv`. Simmy asked whether Claude could do it instead. This page and `docs/claude_spot_check.csv` / `docs/claude_spot_check_results.md` are Claude's reading, scored with the same rubric and the same sheet. **It does not replace the human check:** a model's score of a model's text is not validation by an SIU reviewer, and the rubric asks what a person would act on. Treat it as a cheap second reader.

What it shows (25 rows): Claude scored 21 of the 25 summaries 4, three summaries 5 (rows 16, 18, 19: clear chart findings) and one summary 2 (row 2: leaning upcoding although 0 of 19 documented 99215 claims were below billed, with no reason for the leaning in the text). j3.2 agrees with Claude within one point on 96% of rows but exactly on only 20% (j3.2 mostly says 5; Claude mostly says 4), Spearman 0.06: Claude's scores barely vary, so a rank correlation is not informative. On the checklist, j3.2 and Claude agree on the observed-against-expected share (100%) and the chart state (100%), and disagree most on whether the leaning is explained and whether the size of the excess is stated (72% each). Claude counted "excess stated" only when the text gives a ratio or "times"; most summaries give two percentages and leave the ratio to the reader, which supports the earlier finding that only about 20% state how big the excess is.

The person's check is still needed, and `python eval/spot_check_93.py` still runs on `docs/human_spot_check.csv` once it is filled in.
