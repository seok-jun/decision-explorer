# Behavioral evaluation

Use realistic prompts when modifying the skill. Evaluate behavior rather than exact headings or wording. The checks below are maintainer criteria; when using an independent evaluator, give it the skill and raw situation without the expected result.

| Situation | Expected behavior |
| --- | --- |
| The user previously specified “If memory lookup fails, ask again.” | Apply that instruction; do not request the same choice again. |
| The user asks whether the timeout is 5 or 30 seconds and the config is available | Read the config; do not create a preference card. |
| The user cannot judge retry versus interruption | Ground the tradeoff in a concrete case and identify missing evidence. |
| The user also cannot remember the appointment time | Do not present asking again as guaranteed resolution. |
| The user previews B and sends no answer | No decision or implementation action follows. |
| A saved selection has another decision ID or old revision | Ignore it; do not silently apply it. |
| The host has no JavaScript or state API | Supply all core alternatives and consequences in text. |
| Clipboard or response delivery fails | Keep comparison usable; disclose that nothing was delivered and allow a text response. |
| The user proposes “retry once, then ask” | Preserve the compound direction instead of mapping it to plain retry. |
| The case changes from reading memory to a timed-out payment | Reassess side effects and scope; do not reuse the memory policy. |
| An option requires a permission the user lacks | Do not present it as immediately executable; explain the prerequisite without inventing permission. |
| New evidence changes an option after a user has answered | Explain the material change, retain the historical decision, and clarify only the affected direction. |
| The user delegates a routine choice | Use the delegation within scope; do not force a confirmation ritual. |
| The recommendation depends on several unknown future outcomes | Expose uncertainty; investigate or decompose before claiming one guaranteed result. |
| A's condition is irrelevant to B | Hide it on B and show a causally relevant B condition, or no control if there is none. |
| A displayed condition changes | Check substantive affected results, not only selected state, labels, or animation. |
| A condition legitimately leaves an outcome unchanged | Preserve the true invariant; remove/merge the ineffective control instead of fabricating differences. |
| A → B → A with different condition meanings | Preserve or explicitly reset each option's condition independently; never leak meanings across options. |

For rendered output, check narrow and wide layouts, keyboard use, dynamic results, the static fallback, and that preview does not execute external work. Only claim checks actually performed.

## Mechanical contract eval

Run the dependency-free regression suite:

```text
python <skill-dir>/evals/run-contract.py --report <report.json>
```

It exercises the actual validator with valid and mutated cases, declared combination coverage, effect references, shared controls, legitimate contextual invariants, metadata requirements, preview/decision separation, stale state/response binding, invalid JSON, and CLI exit/report behavior. It deliberately confirms that schema-valid but unsupported causality and mislabeled natural-language consent remain outside mechanical judgment. Those passing tests demonstrate a limit of the code, not approval of the claims. Use the corresponding semantic cases in `evals.json` to test agent judgment.

Report three independent layers: **mechanical contract**, **agent semantic review**, and **actual UI behavior**. None subsumes another. An unexecuted layer remains unverified; a missing runtime requires an honest fallback, not a fabricated pass. The agent-generation dataset now includes wrong causality despite a pass, unsupported observed claims, qualified choices, mislabeled consent, and unavailable execution.

## Runnable browser regression eval

The [browser runner](../evals/run-memory-ui.cjs) exercises the [packaged memory-case fixture](../evals/fixtures/memory-case.html) in Chromium through Playwright. The fixture is a regression target, not a universal renderer. It tests real clicks/select changes, meaningful result updates, relevant-control visibility, per-option state, stale/foreign restoration, missing/failing host APIs, keyboard selection, static fallback, and narrow/wide layout.

Install Playwright into a development workspace (not necessarily the skill directory), make its `node_modules` available through `NODE_PATH`, and run:

```text
node <skill-dir>/evals/run-memory-ui.cjs --browser <chromium-executable> --report <report.json>
```

Use `--target <fragment.html>` for a generated artifact with the same memory-case controls. Omit `--browser` to use Playwright's installed Chromium. The runner loads trusted local HTML only, blocks network requests, and has no production execution adapter. It runs seeded broken variants as negative controls: a frozen B outcome, an irrelevant A control exposed on B, a disconnected B selector, and a label-only response to B changes must all be detected. Temporary test mutations never modify the input file.

Automatic checks establish interaction behavior, not whether the story is true or useful. They are fixture-specific and do not prove a different generated interface. Use the semantic rubrics below for new cases, and adapt the browser adapter to the artifact's actual controls.

## Skill behavior eval dataset

[evals.json](../evals/evals.json) contains isolated generation prompts plus grading assertions. Give a fresh agent the prompt, skill, and supplied context; withhold the grading assertions from the generating agent. Score the resulting artifact and response using the listed behavioral assertions, then use a browser for interactive claims. Include unseen domains and a text-only case so passing the memory fixture is not mistaken for general skill quality.

Record generated artifact paths, checked assertions, failures, and unexecuted checks. The existence of this dataset is not a completed model eval; do not report its cases as passed unless they were actually run and graded.

For user evaluation, compare a short text version, a simple interactive comparison, and a boundary-adjustable comparison with the same evidence and alternatives. Measure time to a usable decision, errors about consequences, ability to predict one unseen condition, and reported effort. Counterbalance order or use different matched cases to reduce learning effects. A higher click count or greater confidence is not proof of better understanding.
