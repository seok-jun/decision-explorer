# Design provenance

Reviewed 2026-11-11. Sources inform the workflow; they are not required runtime dependencies, instructions to install software, or proof of effectiveness for coding decisions. No source code was copied into this package.

- [Visual Planning Skills — visual-plan](https://github.com/parthjshah95/visual-planning-skills/blob/main/skills/visual-plan/SKILL.md): concrete visual plans, practical consequence-based questions, alternate answers, and explicit return through chat. This skill narrows scope to one active decision and does not adopt preselected recommendations as user decisions.
- [Effective HTML](https://github.com/plannotator/effective-html) and [its catalog](https://www.effectivehtml.com/catalog): focused, disposable interfaces and exporting human input. The lesson is to use a purpose-fit representation, not require HTML everywhere.
- [Plannotator](https://github.com/backnotprop/plannotator): a review surface and feedback return path. Such infrastructure is optional for this skill.
- [CopilotKit human-in-the-loop reference](https://github.com/CopilotKit/CopilotKit/blob/main/examples/v2/docs/reference/use-human-in-the-loop.mdx): explicit response events and continuation. A local preview is not that response event.
- [LangGraph time travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel): replay and branching can run nodes and external calls again. Distinguish inspecting a saved trace from executing another path.
- [What-If Tool](https://pair-code.github.io/what-if-tool/): input-condition exploration. Its model inspection setting does not establish effectiveness for software design decisions.
- [Buçinca et al., CHI 2025](https://kgajos.seas.harvard.edu/papers/bucinca2025contrastive.pdf): contrastive explanations improved independent decision skills in the studied exercise-selection task. This motivates comparison but is not validation of this skill.
- [Buçinca et al., 2021](https://arxiv.org/abs/2102.09692): cognitive forcing reduced overreliance in the study, with a subjective-experience tradeoff. Do not impose mandatory prediction quizzes.
- [Fok and Weld, 2024](https://onlinelibrary.wiley.com/doi/10.1002/aaai.12182): a perspective emphasizing verification in AI-advised decisions. Link consequences to inspectable evidence rather than treating plausible explanations as proof.

The initial design also incorporates an independent Astra xhigh review of the proposal and illustrative prototype: causal completeness, investigate-before-asking, scope boundaries, preview versus decision, state identity/versioning, delivery uncertainty, and text fallback. That review was not a cross-platform execution test or a user study.
