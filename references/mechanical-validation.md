# Code checks and agent judgment

Use the dependency-free Python 3.9+ [validator](../scripts/validate_case.py) for prepared decision cases. It validates declared data, not the world. A pass is neither a decision nor authorization. Do not ask users to fill in this internal contract.

## Workflow

1. The agent determines whether exploration is needed, investigates available facts, and authors a small case. For an interactive comparison, branch table, or saved decision, serialize the declared model using the format below. A brief conversational answer or an already settled choice does not require creating a JSON file.
2. Run `python <skill-dir>/scripts/validate_case.py case.json --report check.json`. Add `--state state.json` before consuming restored state or recording a decision/application. Fix data errors before presenting interactive controls. Re-run after changing options, conditions, results, evidence metadata, or state. Invalid restored data must not block a fresh comparison: ignore it, preserve historical records separately, and validate the fresh state.
3. The agent independently reviews causal relevance, evidence support, option completeness, natural-language intent/qualifications, meaningful scope changes, and current authorization. Correct data if necessary and rerun code. A fabricated `source_ref` or an agent-added `kind: explicit` cannot establish consent. Preserve the user's original words and actual source; this script never interprets a message or chooses an option.
4. For an interactive artifact, test its actual controls/results following [presentation.md](presentation.md). A model-data pass does not prove renderer wiring. Generate the view from the validated data when practical; otherwise check that the view agrees with it.
5. Report mechanical, semantic, and UI checks separately, with evidence and unresolved limits. If Python or a browser cannot run, mark that layer `not_run`, use the available text surface, and do not claim a pass. Do not install a toolchain just to answer a simple question.

## Version 1 executable contract

See the complete [memory data fixture](../evals/fixtures/memory-case.json) and [preview-state fixture](../evals/fixtures/memory-state.json). These are synthetic data, not observed traces. The existing HTML fixture is tested separately; it is not automatically regenerated from this JSON.

Required top-level fields (unknown fields rejected to catch misspellings):

| Field | Format and mechanical check |
| --- | --- |
| `schema_version` | Integer `1`; separate from content revision |
| `decision_id`, `scope`, `question`, `input`, `event` | Nonempty strings; scope equality is exact, semantic equivalence is agent judgment |
| `revision` | Positive integer; the agent increments it for material changes |
| `options` | Nonempty list of `{id, label}`; unique IDs |
| `controls` | List of `{id, values, effects}`; unique nonempty string values; `effects` maps applicable option IDs to affected result-field names |
| `claims` | List of `{id, text, kind, ...metadata}`. Kinds: `observed`, `inferred`, `illustrative`, `unknown` |
| `cases` | List of `{id, option_id, when, results, claim_ids}`. `when` maps exactly the applicable controls to allowed values; `results` maps stable field names to nonempty strings; nonempty `claim_ids` must reference claims |

Observed claims require nonempty `source`, `run`, `input`, and `environment`. Inferred claims require `source`; unknown claims require `limitations`. All kinds may include these metadata strings and `limitations`. Code checks presence and references only, not whether a source exists, supports the claim, or represents the claimed environment. Agent review checks each result against its referenced claims.

Every declared option/condition combination must appear exactly once. Limit: 1000 combinations; larger cases fail with `coverage_limit` instead of silently sampling. Split large cases into coherent decisions. Continuous inputs need explicitly labeled representative values; this is coverage of those values, not the full domain. Conditional/coupled inputs must be expressed as coherent discrete scenarios or separate cases, not an impossible Cartesian product. This version does not infer constraints.

For each control value, at least one comparison with all other conditions held fixed must change a declared affected field. Equal outcomes in some contexts remain allowed. Entirely invariant controls must be removed or values merged; never fabricate an effect to pass. String differences can be cosmetic: an agent still checks substantive meaning. Code cannot discover a causal relationship or decide which conditions should be declared.

## State contract

Required fields: `decision_id`, `revision`, `scope`, `status`, `preview_option_id`, `selected_option_id`, `response`, `conditions`. IDs/revision/scope must match the current case. Option IDs may be null, otherwise they must exist. `conditions` stores a partial map of option ID → applicable control ID → allowed value, keeping option state isolated.

- `exploring`: selected option and response must both be null.
- `decided` / `applied`: selected option and response required.
- `needs-review`: current-case record parked for agent review; no permission to apply. Historical mismatched records stay separate.
- A non-null response is `{kind: "explicit", text, source_ref, decision_id, revision, scope}` and must bind to the current case. Code checks metadata, never whether the user's words actually select that option. Qualified or novel answers must be represented faithfully by revising/adding options, not squeezed into existing labels.
- `applied` also requires a nonempty `application_evidence` reference. Only use it after checking the actual implementation; its presence does not prove success.

This checks snapshots, not an authenticated event log or transition history. It does not detect a material edit made without a revision bump, verify message delivery, authenticate a user, discover host capabilities, or enforce execution permissions. Determine capabilities from actual host tools; unknown support is not true. No output from this validator should itself trigger an external action.

Exit code 0 means mechanical pass; 1 means invalid input/contract. JSON output always distinguishes `mechanical`, `semantic: not_evaluated`, and `ui: not_evaluated`. It reports the first actionable error with `code`, `path`, and `message`; fix and rerun. A malformed JSON file, duplicate JSON key, or non-JSON constant is rejected.
