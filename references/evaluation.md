# Light evaluation of v0.3

## Two-week log
For two weeks, log only the first eligible handoff each day; skip days without one rather than selecting favorable cases.
Alternate concise ordinary handoffs and this skill across eligible cases, with comparable access to code, logs, and follow-up questions.
Use these time budgets as starting values, not guaranteed completion times or validated thresholds:
1. Before viewing, spend about 20 seconds recording one expected behavior, or “unknown”.
2. After viewing, spend about 40 seconds predicting a related condition not directly shown and why, or stating delegated scope and verification criteria.
3. Spend about 40 seconds checking against an existing test, raw log, contract, or check already needed for the task.
4. Spend about 10 seconds recording correct / wrong / unchecked, total elapsed time, and additional questions.
Include capture/setup, generation, opening, and follow-up costs in total time; record whether an offered entry point was used or ignored.
Keep errors in reasoning separate from a coincidentally correct outcome; check whether delegated claims match their verification coverage.
If evidence is unavailable or checking takes longer, leave the result unchecked. Do not build evaluation infrastructure to force a verdict.
Prediction is evaluation participation, not a mandatory product quiz. An optional one-line restatement may reveal a misconception; correct only that part.
Mostly unchecked results mean inconclusive evaluation. Satisfaction or click counts alone cannot establish success.
This log informs local adoption, not causal effectiveness, long-term retention, or generalization to other developers.

## Replayer versus table
Use the same captured runs, wording, evidence, and limits in an aligned replayer and a concise table.
Ask where the first difference occurs and which values differ; separately ask which later calls change and what the records cannot establish.
Assign the first view for each question before answering, using different views across the two questions; reverse allocation with another participant when possible.
Record per-question elapsed time, repeated lookups/comparison trips, final answer, mistaken beliefs and corrections; note prior exposure and learning carryover.
Specifically check confusion between harness calls and actual worker/scheduler execution, network failure, or backoff timing.
Kill criterion: if even a favorable case does not reduce backtracking/comparison work versus the table, drop the replayer as the v0.3 centerpiece; speed alone does not save it.
Also drop that central role if it adds cost without comparison benefit or encourages confusion between observation and inference.
A failure does not reject selective understanding as a whole; a success does not justify a general replay framework.

## First experiment: author report, n=1, one retry case
Source: the author's report supplied for this draft and the original EXPERIMENT.md protocol; no measured effect size or raw timing log was supplied.
The author found aligned two-run replay easier to understand than the same-data table; retain the HTML direction for further testing, not as proven superiority.
Wording obstructed understanding more than layout: “기준 실행 / 대조 실행” was unclear; “다시 보내면 될 수도 있는 실패” was too long; “재시도 함 / 재시도 안 함” worked.
Failure to state equality led to the mistaken belief that the retry limit had been raised to 3; it was 3 in both runs.
The answer was mostly correct, but a one-line restatement exposed a wrong belief. This motivates an optional check, not compulsory testing or a measured accuracy claim.
Capturing real function outputs required a temporary test file in the target repository and JDK setup. The harness loop, not the worker/scheduler, generated the attempt sequence.
The copied HTML records the temporary test as removed; this draft did not rerun capture or independently inspect the target repository cleanup.
Author involvement, one favorable case, wording revisions, and possible carryover limit inference. No controlled layout effect, quantitative comparison savings, or general comprehension benefit is established.
