# Case contract

Use this content model to keep different surfaces equivalent. Do not show every field permanently. For branch tables, interactive cases, or saved state, use the [executable contract](mechanical-validation.md) to check the declared model in code; brief conversation can use this checklist alone.

| Field | Content |
| --- | --- |
| Decision identity | Short stable ID and content revision when handling interactive or durable state |
| Question | The practical choice the person needs to make |
| Scope | Operation, affected users/data, and conditions to which the answer applies |
| Reason for asking | The unresolved priority or authority; not the agent's missing investigation |
| Starting point | Current behavior, if established; otherwise mark unknown |
| Case input | Small concrete input and relevant initial state |
| Event/action | What happened or is assumed to happen, and where the choice occurs |
| Alternatives | Stable option IDs, behavior, user-visible result, system effect, and conditions |
| Evidence | Claim, evidence kind, source/run reference, and relevant limitations |
| Boundary | A changed condition that alters the outcome; optional if no useful boundary is known |
| Control dependencies | Applicable option IDs, allowed values, affected result fields, invariant fields, and per-option state/reset behavior for each adjustable condition |
| Open questions | Missing facts and what would resolve them |
| Decision record | Explicit answer, applicable scope, revision, rationale if provided, and status |

An option label such as “retry” is not sufficient: retry count, timing, and prior side effects may change its meaning. Include these only to the degree necessary for this decision. Do not invent parameter choices just to complete the case.

Example dependency map: asking again uses the user's ability to supply the missing information; retrying a lookup uses the outcome of that retry. Do not expose the first as an active retry-path control. Shared controls are appropriate only when they have a genuine effect in each path where they are shown. Keep conditions with different meanings under different state keys even if their labels or values happen to match.

## Evidence and scope

Evidence labels apply to individual claims. One diagram can contain an observed timeout, an inferred next step, and an illustrative response. Cite the actual file/run/document when available. An agent's own authored explanation is not independent validation.

For probabilistic behavior, show observed examples or measured ranges with their sampling limits; do not present one model response as the guaranteed result. If comparable branch executions are available, specify which inputs and conditions are held constant and which differ.

Separate diagnostic facts from user values. “The operation completed twice” is a factual claim. “A delay is preferable to duplicate execution” is a priority or requirement. A test can check the first; the user's product context establishes the second.

## Minimal durable record, when needed

```json
{
  "decision_id": "memory-timeout-policy",
  "revision": 1,
  "status": "exploring",
  "scope": "Read-only memory lookup timeout during chat",
  "preview_option_id": null,
  "selected_option_id": null,
  "explicit_response": null,
  "open_questions": []
}
```

This is a conceptual example, not the executable validator format or a new storage system. When validating a project record, adapt it to the executable state contract while preserving its original meaning and provenance. Use a project's existing format when it can express the same distinctions. Keep preview in a separate field; do not promote it to selected automatically. Retain option meanings alongside a durable record or point to the versioned case.

An answer like “B, but retry only once” changes the proposed behavior. Resolve it as a revised choice; do not record plain B and lose the qualification. An answer that clearly supplies all needed direction does not need another ceremony.
