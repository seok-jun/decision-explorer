# Design provenance

Draft date: 2026-11-11. This package follows the supplied round-2 agreement, the round-1 reference corrections/deletion list, and the author's first experiment report. Bibliographic descriptions below are carried from those inputs, not a new literature review. None establishes the effectiveness of this skill.

## Evidence
- [Rozenblit & Keil, 2002](https://cogdevlab.yale.edu/sites/default/files/files/rozenblit%20%26%20keil%20%202002.pdf): illusion of explanatory depth; motivates checking a related judgment instead of relying only on “I understand.” Not a trial of this workflow.
- [Tversky, Morrison & Bétrancourt, 2002, Animation: Can It Facilitate?](https://www.tc.columbia.edu/faculty/bt2158/faculty-profile/files/_Morrison_Betrancourt_AnimationCanitfacilitate.pdf): informs content-matched comparison with static views and user-paced inspection; not a claim that all interaction is ineffective.
- [Ainsworth, 2006, DeFT](https://nottingham-repository.worktribe.com/output/23577631): a framework for multiple representations, including the work of relating them; informs consistent names and limited views, not a measured benefit here.
- [Shen & Tamkin, How AI Impacts Skill Formation](https://arxiv.org/abs/2601.20245), [research account](https://www.anthropic.com/research/AI-assistance-coding-skills): the supplied correction describes n=52 and reduced comprehension in a new-library task. Randomized AI access does not make observed interaction patterns causal evidence for mandatory prediction or this workflow.
- [Buçinca et al., 2021](https://arxiv.org/abs/2102.09692): cognitive forcing and overreliance, with experience costs in the studied setting; not proof that quizzes improve code understanding.
- [Buçinca et al., CHI 2025](https://kgajos.seas.harvard.edu/papers/bucinca2025contrastive.pdf): contrastive explanation in an exercise-selection task; motivates comparing a plausible user alternative, not arbitrary A/B cases or generalized coding effects.
- [Comprehension Debt in GenAI-Assisted Software Engineering Projects](https://arxiv.org/abs/2604.13277): the corrected source concerns 621 reflection entries from 207 students, not a practitioner-team intervention trial.
- [Cognitive Debt in the GenAI Era](https://arxiv.org/abs/2610.37888): the corrected source is a review of 76 gray-literature items containing practitioner voices, not evidence that proposed mitigations work.
- The supplied correction identifies [arXiv 2607.10856](https://arxiv.org/abs/2607.10856) as *How Do Practitioners Build SE Agents?*; do not cite it as a comprehension-debt study.
- The author report (n=1, one case) is local design input. See [evaluation](evaluation.md) for the result and limits; no timings or quantitative effect estimates were supplied.

## Design inspiration
- [Whyline, initial Alice project](https://www.cs.cmu.edu/~NatProg/whyline.html) and [Ko & Myers, ICSE 2008](https://doi.org/10.1145/1368088.1368130): start from concrete why/why-not questions. Keep Alice and Java debugging contexts distinct; do not transfer speedups to general comprehension. Missing events require path reasoning, not just replay.
- [Shneiderman, 1996](https://vis.csail.mit.edu/classes/6.859/readings/pdfs/Shneiderman-TheEyesHaveIt.pdf): information exploration principles, not a law requiring a whole-system overview before every answer.
- [Lawrance et al., information foraging in debugging](https://web.engr.oregonstate.edu/~burnett/Reprints/TSE-IFT-2013-asprinted.pdf): motivates predictable entry-point wording and attention to navigation cost, not universal superiority of navigation cost over information amount.
- [Bret Victor, Learnable Programming](https://worrydream.com/LearnableProgramming/): inspectable state and immediate feedback; executable models are not equivalent to authored text-swapping HTML.
- [Fok & Weld, 2024](https://onlinelibrary.wiley.com/doi/10.1002/aaai.12182): a perspective on verification in AI-advised decisions, not an intervention evaluation of this skill.
- [Visual Planning Skills](https://github.com/parthjshah95/visual-planning-skills/blob/main/skills/visual-plan/SKILL.md), [Effective HTML](https://github.com/plannotator/effective-html), and [Plannotator](https://github.com/backnotprop/plannotator): concrete entry points, focused disposable views, and returning to conversation; not evidence of learning gains or required integrations.
- Internal debate/review is design provenance, not empirical evidence: `debate-r2-codex.md` and `debate-r1-codex.md` under `C:/Users/jun/AppData/Local/Temp/claude/5e852864ddc03412/9bc23f0f-a7db-4bee-b7bf-b6c48a6c4af6/scratchpad/`.
- The v0.2 predecessor at `C:/Users/jun/.codex/cache/mh-workflow-c61fcc8/workflow/skills/decision-explorer` supplied claim-level evidence labels, investigation before preference questions, and exploration/action separation. Decision contracts, persistence, validators, runners, and old fixtures are deliberately not carried forward.
- Osmani essays, output styles, rr/Replay and code-city adoption histories are not used as effectiveness evidence; adoption confounds integration cost, distribution, and work fit.

## Implementation reference
- `C:/mhwt/behavior-replay/replay.html` and `trace.json` are copied unchanged as [replay-example.html](../assets/replay-example.html) and [replay-example-trace.json](../assets/replay-example-trace.json). `EXPERIMENT.md` supplied the comparison protocol; it is not bundled as another fixture.
- The example records code version `590e6779`, real decision-function outputs, supplied failure inputs, and harness sequencing. It does not record real worker/scheduler execution, network failures, or backoff timing. Historical abbreviated paths/commands need resolution for reproduction.
- [LangGraph time travel](https://docs.langchain.com/oss/python/langgraph/use-time-travel): a reminder that execution replay/branching may rerun external calls; this package only inspects captured runs and does not integrate LangGraph.
- [CopilotKit human-in-the-loop reference](https://github.com/CopilotKit/CopilotKit/blob/main/examples/v2/docs/reference/use-human-in-the-loop.mdx): distinguishes an explicit response from local preview; no bridge, response payload, or decision-state machinery is adopted.
- [What-If Tool](https://pair-code.github.io/what-if-tool/): a reference for inspecting input differences, not a license to simulate unrecorded software behavior or evidence of comprehension gains.
