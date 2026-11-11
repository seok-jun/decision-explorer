# Presentation and interaction

Choose from actual capabilities, not the host's product name. Keep the decision content independent of the surface. Match the user's language and requested output.

## Surface selection

| Available capability | Use |
| --- | --- |
| Supported in-conversation visualization | A contained case with alternative previews and an optional boundary control. If an available visualization skill governs this surface, read and follow it. |
| Local HTML creation and a browser | A self-contained HTML comparison when materially useful. Use the authorized output location. No network service is required. |
| Plain chat or CLI | A short input/action chain and side-by-side outcome table. Accept a text answer. |
| Native question/response tool | Use it for a clear decision after presenting context if it fits the workflow; never require its presence. |
| No execution or evidence access | Explain from supplied material, label assumptions, and state what cannot be checked. |

If a richer surface is unavailable or fails, provide the same core choices, consequences, scope, and uncertainty in text. Do not ask the user to install software merely to make the decision. Avoid producing both a long textual report and a duplicate visual.

## Initial view

Show one case and one decision. The useful content is:

1. Concrete input and event.
2. The choice at the relevant step.
3. Consequences that differ between the alternatives.
4. A meaningful boundary condition or unresolved fact.
5. A clear way to reply, investigate, or propose something else.

Provide 2–3 choices initially where appropriate; do not prune a materially different alternative just to fit the layout. Show a recommendation only when it follows from known priorities, with its reason. An initial preview may be selected for display, but label it “preview, not decided”; do not portray it as the user's preference or the current policy.

Prefer a stable visual with changing results over rebuilding the whole diagram for every option. Avoid decorative motion, dense dashboards, generic quality scores, and mandatory prediction quizzes. The user may inspect evidence or skip directly to a response.

## Interactive contract

- Show only conditions relevant to the active option. Changing options must update the control label, valid choices, and result dependencies together. Hide irrelevant controls rather than leaving a working-looking no-op.
- Retain values separately for each option or explicitly reset them to a valid initial value on return. Do not reinterpret an A-only value as a B condition. Validate each restored condition against its own option's allowed values.
- Preview and boundary controls change only local presentation. They must not execute business actions, contact services, or silently launch real branch runs.
- Ordinary browser interaction is not an agent response channel. Clearly state whether a selection has been transmitted. Never display “sent”, “saved”, or “applied” merely because the screen changed.
- Where the host supports a documented response API, follow that API and the current authorization rules. Do not invent a host bridge or require `window.openai` on other platforms.
- If delivery is absent or unverified, use explicit chat replies. A “copy response” helper may export the ID, revision, chosen direction, scope, and user's qualifications; copying is not sending or approving.
- If a copy helper is used, provide visible selectable text when clipboard access fails. Never end at a silent failure.
- Validate restored state against decision ID, revision, and current option IDs. Ignore mismatches and do not restore an old approval as a new answer.
- If local state is stored, save only what is necessary and avoid sensitive material. Do not require persistence for a one-off comparison.
- Keep essential alternatives and outcomes available in a static fallback if JavaScript is unavailable; an inert default-only preview is insufficient.
- Use native labeled controls, keyboard navigation, meaningful focus, readable contrast, responsive reflow, and concise live updates for changed results. Escape source data as text; do not inject retrieved HTML or scripts.

## Interaction verification before delivery

1. Write a small option/condition/result matrix. Identify which result fields should change and which should remain stable. Do not require every field to change: an initial response may stay the same while later processing changes.
2. Open the generated artifact in a real browser when available. Select each option and exercise every finite condition value. For larger input spaces, test each meaningful outcome class and boundary, and record the sampled coverage.
3. Assert that only relevant controls are visible and keyboard-accessible. Check changes in substantive results such as the next action, user-visible outcome, system effect, or unresolved information. A label, counter, color, or selected value changing alone does not pass.
4. Switch A → B → A. Confirm the chosen preservation/reset behavior and no cross-option state leakage. Check old/foreign stored state, missing delivery APIs, and the preview-versus-decision boundary when those features exist.
5. Inspect the result at narrow and wide widths and check the static fallback. Record actual checks and limitations. If browser execution is unavailable, source/DOM checks are partial evidence only; provide the complete text alternative.

If different control values legitimately have equivalent consequences, merge those values, remove the control, or explain the invariance as static context. Do not rewrite outcomes just to pass a visual-difference assertion. A dependency or option-meaning change requires a new case revision.

## Replay versus explanation

Distinguish **viewing a recorded trace**, **running a new branch**, and **an authored scenario**. Replaying computation can call external services again, incur cost, or repeat side effects. Version 0.1 does not run those experiments automatically. Request or perform appropriate evidence gathering only within the active task's authorization and a suitable isolated environment.

## Text fallback shape

```text
[decision ID / revision, when needed]
Input → event → choice point
Scope: ...

Option | User-visible result | System effect | Condition/evidence
A      | ...                 | ...           | ...
B      | ...                 | ...           | ...

Boundary: if ... changes, ... changes.
Reply with a direction, another approach, or the information you need first.
```

Do not force this exact template when a shorter explanation is enough. The same core information must remain available across surfaces.
