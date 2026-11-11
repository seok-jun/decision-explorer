# Aligned two-run HTML replay

## When it is worth generating
Use when the question requires repeated comparison of the same values/events or tracking state across a sequence, and keeping position can reduce remembering and searching.
Prefer chat or a small table for a short answer. Do not generate HTML just because a handoff occurred or a numerical threshold was crossed.
Start from [the working example](../assets/replay-example.html) and [its raw trace](../assets/replay-example-trace.json); these are copied experiment artifacts, not a general renderer or data contract.
The example embeds its trace and includes the same-data table used in evaluation. Its internal run IDs are not user-facing case names.
Its abbreviated source paths and command are historical provenance, not a complete reproduction recipe; resolve exact locations for a new case.

## Minimum data to establish before rendering
- Provenance: code version, actual function/path called, command, inputs, relevant settings, environment, and mocks.
- Comparison: one changed variable and explicit equality or other differences in remaining conditions.
- Events: run and event IDs, order, meaningful event kind, and raw-record location.
- State: values needed for the question, capture point, and before/after values only where actually captured.
- Alignment: meaningful correspondence key and unmatched events, with uncertainty stated.
- Limits: uncaptured intervals/values, unexecuted paths, timing uncertainty, and inferred links.
The example JSON alone does not contain all provenance; read its HTML metadata as well. Never fill missing metadata by guessing.

## Alignment rule
Align by event meaning plus the relevant identity, such as retry decision at attempt number, not equal array index or step number alone.
Switching cases preserves the semantic event position and the fields being inspected. Keep unmatched positions in the union of events.
Show “대응 사건 없음” or “기록 없음” where appropriate; absence in a trace alone does not prove nonexecution.
If correspondence is uncertain, show that limit instead of manufacturing a match.

## UI contract
- Previous/next event; jump to the first difference; switch case while keeping position.
- Show the current event and relevant captured values, including captured before/after state when available; mark changed values without relying only on color.
- Provide raw records and exact code locations on demand; keep evidence kinds and material limits visible.
- No autoplay, arbitrary input, free-form simulation, or controls that execute target code.
- Use keyboard-operable controls, visible focus, disabled end controls, and readable narrow layouts.
Before delivering a generated/adapted page, check navigation, first difference, switching at matched and unmatched events, labels, and raw/source access in a browser when available; report unverified behavior honestly.
If HTML is unavailable or disproportionate, return the same essential facts and limits in chat/table form.

## Wording
Use the shortest spoken developer wording for the outcome difference: “재시도 함 / 재시도 안 함”.
Never name cases baseline/contrast/control, “기준 실행 / 대조 실행”, or long explanatory phrases such as “다시 보내면 될 수도 있는 실패”.
Keep identifiers secondary to plain labels and use consistent field names across views.
Explicitly say when a value is identical: “재시도 한도는 둘 다 3회입니다.” A non-highlighted field is not a sufficient statement of equality.
Keep conditions and uncertainty in explanatory text rather than overloading case names.

## Evidence tags in plain words
- “실행 확인 / checked in this run”: the recorded value or output, only within the actual invocation and environment.
- “코드 추정 / inferred from code”: an unexecuted path, causal link, or worker/scheduler sequence inferred from sources or a harness.
- “가상 예시 / illustrative example”: authored to explain a possibility, never presented as captured execution.
- “미확인 / not checked”: evidence does not establish the claim.
“입력 / supplied input” and “계산 / calculated” can clarify provenance; calculated values are not raw observations.
The harness may record real function outputs while its loop supplies successive attempts. Label that sequencing as inferred for the real application; do not claim worker reexecution, real network failure, or backoff observation.

## Capture hygiene
Prefer a narrow existing test/reproduction path and the real function over reimplementing behavior. Fix the changed condition and falsifying observation before a comparison.
Account for dependency/JDK setup, temporary code, capture, generation, and opening time; do not call capture cheap without including these costs.
Keep temporary capture additions identifiable, preserve raw output needed for claims, and remove only your temporary capture code after use, including on failure where possible.
Check the target diff for leftovers without reverting user work; disclose anything cleanup could not remove. Stay within task permissions for setup and repository changes.
Record what actually ran, what the harness supplied, mocks, exact commands, and environment changes. A passing test is not an execution trace.
