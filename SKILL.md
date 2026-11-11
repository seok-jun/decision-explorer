---
name: behavior-explorer
description: Explore concrete behavior on explicit understanding requests or at question, completion, and approval/merge handoffs with consequential boundaries; not ordinary debugging, general teaching, or trivial edits.
metadata:
  version: "0.3.0"
---

# Behavior Explorer
Help the user understand the behavior they need and delegate the rest to explicit verification.
Use the user's language; understanding or bounded delegation is the outcome, not a required decision.

## Start and scope
Respond to explicit requests to understand a specific task, including not knowing where to look.
At question, completion, and approval/merge handoffs, check for a meaningful behavior boundary.
Do not add exploration to ordinary debugging, general teaching, trivial edits, or settled work the user asks to apply without explanation.
Handoffs are opportunities, not mandatory understanding gates; preserve authorized work and urgency.

## Select entry points
Consider differences from agreed requirements or existing behavior; concrete effects hard to undo or discover later; and unsupported assumptions that change outcomes, scope, or verification.
Keep a candidate only if knowing it could change expected results, verification, or delegation. Merge overlapping boundaries; do not speculate about the user's ignorance or score candidates numerically.
Start with 0–1 entry points, at most 3 for independent important boundaries; these are starting values, not validated thresholds. With none, add nothing.

## First view
State the important behavior fact first, then offer a concrete optional entry point, not “learn more.”
At completion handoffs, translate outcome identifiers into plain behavior and compare the delivered scope with the agreed requirement. If automatic recovery excludes a failure that needs manual reprocessing, say that boundary and requirement deviation explicitly; a test name or `manual_reprocess` identifier alone is not disclosure.
Separate unmet requirements from unexecuted checks: passing the remaining tests does not resolve a known scope mismatch. Offer a concrete optional entry point for that boundary without making exploration a completion gate.
Example: “응답이 없어도 서버 처리는 끝났을 수 있습니다.” → “같은 요청이 두 번 처리되는 조건”.
Aim initially for 600 characters of body text; this is a starting budget, never a reason to omit material limits, unknowns, or requirement deviations.

## Fix the case
Identify the user's question, concrete input, relevant state, result, comparison condition, evidence, and limits; no formal case contract is required.
Investigate available facts rather than asking the user to choose an answer; correct an already visible misconception immediately.
Name cases by their outcome difference in the shortest words a developer would say aloud: “재시도 함 / 재시도 안 함”.
Never use experiment-role names (“기준 실행 / 대조 실행”, baseline, contrast, control) or explanatory phrases (“다시 보내면 될 수도 있는 실패”) as case names.
Explicitly state when a displayed value is the same in both runs: “재시도 한도는 둘 다 3회입니다.” Do not leave equality to inference.

## Answer the question asked
Why: conditions producing the result. Why not: expected event and blocking condition.
What if: the changed condition and resulting difference. Other effects: propagation and its boundary.
Which option: consequences and costs in the same case, with the user's priorities; do not invent alternatives.

## Evidence and limits
Distinguish claims as observed (checked in a specified run), inferred (reasoned from sources), illustrative (authored example), or unknown (not established); depth and evidence status are independent.
A PASS is not a trace; a log summary is a summary. State mock inputs, executed paths, uncaptured values, and environment limits.
Do not fabricate values, paths, timings, or executions. Missing records do not establish that an event never happened.
Real function outputs can be observed while harness-produced sequencing and worker/scheduler behavior remain inferred; label each separately.

## Checkable claims
Link conclusion-bearing claims to exact code or raw-record locations and actually compare a key claim against an existing test, raw log, or explicit contract.
For important inferences or unknowns, state what observation would disprove the explanation. If running a comparison, choose the changed variable and falsifying observation before execution.
Use a one-variable comparison when suitable and feasible; delegation does not require two runs. New agent-authored tests and pointers alone are not independent verification.
If execution is unavailable, explain from cited code with inference labels and preserve unknowns; do not block access to deeper explanation.

## Choose the representation
Use chat for short answers. Generate HTML only when keeping position across repeated value/event comparisons or state tracking can reduce navigation and memory work.
Read [replay HTML](references/replay-html.md) before capture or generation; use the aligned two-run form, not free-form simulation.
Reuse existing reproduction paths where possible, account for setup cost, and remove temporary capture code after use without disturbing unrelated work.

## Move through exploration
Answer one question at a time; allow direct movement to causes, conditions, another case, code, or evidence, without a fixed ladder or required lesson.
Prediction before revealing an answer is opt-in, never a risk-based requirement. Keep evidence and important limits visible.
After exploration, optionally invite one line in the user's own words: “원하면 이해한 내용을 한 줄로 말해 주세요.” Never require it or delay work for it; correct only the mistaken part.

## Stop and delegate
Stop when the needed boundary is understood or the remaining scope and verification criteria are delegated. Respect a request to stop without further teaching.
Keep unresolved claims unresolved; do not rename them completed verification. Continue requested implementation within existing authority.

## Action boundaries
Exploration controls are not execution instructions. Preserve qualifications in conditional answers rather than reducing them to a simple option.
Add no approval process, decision-state storage/restoration, validator, or mandatory quiz. Do not expand task authorization.

## Evaluation
Use [the light evaluation protocol](references/evaluation.md) when evaluating this draft and [the ten cases](evals/evals.json) when reviewing routing and behavior.
Compare with concise ordinary handoffs; record mistakes, unknowns, time, and delegation accuracy. Satisfaction and clicks alone do not establish comprehension gains.
Read [sources](references/sources.md) for provenance and limits, not as runtime dependencies.
