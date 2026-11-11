# Worked example: memory lookup timeout

All details below are illustrative. They describe no verified repository behavior.

## Case

- Decision: `memory-timeout-policy`, revision 1.
- Scope: a read-only lookup of prior conversation fails during chat. This does not cover a missing record, denied access, conflicting records, or a timed-out write.
- Input: “어제 말한 약속, 몇 시였지?”
- Initial state: the current message contains no appointment time; it is assumed to exist only in the unavailable prior conversation.
- Event: the lookup times out.
- Question: “이전 대화를 가져오지 못했을 때, 사용자에게 필요한 정보를 다시 물을까, 복구 후 재시도를 안내할까?”
- Why a person may need to decide: the product must balance repeated user effort against interrupted conversation. If the product already specifies this policy, apply it without reopening the question.

## Initial comparison

| Choice | User sees | Subsequent behavior | Limit |
| --- | --- | --- | --- |
| Ask for missing information | “이전 대화를 불러오지 못했어요. 약속 시간을 알고 계시면 알려주세요.” | Wait for information; continue only with information actually supplied | Asking which appointment alone does not recover its time. If the user also forgot, the original request remains unresolved. |
| Explain interruption and allow retry | “이전 대화를 불러오지 못했어요. 잠시 후 다시 시도해 주세요.” | A user retry performs another lookup | Neither recovery nor the appointment's presence is guaranteed. |

Both response texts and future paths are illustrative. Neither option should fabricate the missing time. Do not invent current storage behavior or claim either response has been sent.

## Boundary exploration

Use a different condition for each path. These are illustrative inputs, not observed facts.

| Active path | Visible condition | Values and expected consequence |
| --- | --- | --- |
| Ask again | Can the user provide the time? | Unknown → wait; remembers and supplies → continue with supplied information, original-record match unknown; also forgot → unresolved. |
| Retry guidance | What happens after the user retries? | Unknown → outcome unknown; lookup succeeds and provides the time → answer from the record; another timeout → unresolved. |

Hide the user's-memory control in the retry path. It does not change that path's lookup result. Keep separate values for the two controls and verify A → B → A. On B, changing the retry condition must change the subsequent processing and outcome; only changing the selector or its label is insufficient.

The first response can remain unchanged while the subsequent outcome changes. Neither path's illustrative success should be presented as a measured probability, an automatically executed retry, or an actual backend result.

The control exposes a causal limit; it is not a measured probability or a simulated backend.

## Follow-up examples

- “재시도하면 보통 해결돼?” → inspect appropriate available logs/tests before recommending retries. If unavailable, mark effectiveness unknown.
- “한 번 재시도하고 안 되면 물어봐.” → consider this as a qualified third direction, investigate necessary constraints, and preserve the qualification when recording it.
- Clicking either preview without sending a response → remains exploring.
- “A로 구현해. 다만 모르면 모른다고 말해.” → explicit scoped direction; continue the authorized implementation without asking for the same decision again.

## Acceptance condition

If implementation is requested and the direction is confirmed: “When lookup fails and the user cannot supply the appointment time, the system does not claim to know the time.” Choose a relevant verification method based on the actual code. Do not invent executable tests for this illustrative example.
