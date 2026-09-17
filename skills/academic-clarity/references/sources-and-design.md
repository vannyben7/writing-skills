# Source provenance and design decisions

Academic Clarity local candidate 1.1.0, prepared 2026-09-17. Renamed from the local Academic Defensive Writing Auditor candidate at the user's request. Repository descriptions, SKILL files, and licenses were inspected directly. This is a design record, not an empirical evaluation report or a claim of endorsement by the upstream authors. Source repository names below identify historical attribution. The user-selected publication target is `vannyben7/writing-skills`, under `skills/academic-clarity`; its configuration does not assert completed publication.

## Baseline

[Worigin0314/academic-defensive-writing-auditor](https://github.com/Worigin0314/academic-defensive-writing-auditor), locally installed 1.0.0, supplies the original baseline name, D1–D14 taxonomy, installer, and MIT license. The local snapshot is the revision baseline; no claim is made that it equals the latest upstream commit. Its existing `LICENSE` is retained unmodified.

Retained: defensive-writing focus; necessary scientific caution; protocol facts over generic fairness assertions; no explanation of weak results without support. Changed: a one-caveat maximum, fixed reviewer-reaction fields, required numeric score and edit quotas, English-only style guidance, and examples whose replacements inserted facts missing from their inputs. This candidate also protects warranted strong claims from unnecessary weakening.

## Selective external research

| Primary source | Adopted idea | Not adopted |
|---|---|---|
| [lensback940701/Evidence-Bound-Press-Conference-Revision-Skill — SKILL.md](https://github.com/lensback940701/Evidence-Bound-Press-Conference-Revision-Skill/blob/main/SKILL.md) | Treat source status and inferential limits as editing constraints; make retained cautions and uncertain decisions visible. | Its manuscript-lock prerequisite, obligatory contract before every edit, special Dalian manuscript guardrails, and default tracked-document deliverables. These requirements do not fit every paragraph or course essay. |
| [Evidence-Bound triage and regression reference](https://github.com/lensback940701/Evidence-Bound-Press-Conference-Revision-Skill/blob/main/references/triage-and-regression.md) | Check candidate function, potential information loss, and semantic drift; retain distinct restrictions and locally necessary qualifiers. Use the six editorial dispositions from the accompanying skill. | A separate new D1–D8 numbering scheme; this package keeps its existing D1–D14 meanings. No scanner or audit CSV dependency was copied. |
| [Kiterlin/anti-defensive-writing — SKILL.md](https://github.com/Kiterlin/anti-defensive-writing/blob/main/SKILL.md) | Reduce uninformative wrappers; inspect what a limitation contributes; use supplied scope details to improve clarity. | General instructions to put every claim first, use positive framing regardless of excluded inference, or ban contrastive scaffolding. Its examples can introduce a mechanism, setting, or interpretation missing from the original sentence; those mappings were not adopted. |

Both researched repositories provide MIT licenses: [Evidence-Bound license](https://github.com/lensback940701/Evidence-Bound-Press-Conference-Revision-Skill/blob/main/LICENSE), [Kiterlin license](https://github.com/Kiterlin/anti-defensive-writing/blob/main/LICENSE). Their attribution and license notices are included in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Adapted guidance is restated for this package; external examples, scripts, and project-specific controls were not copied.

## Candidate-specific additions

The user requirements for this iteration motivated native English/Chinese examples, research-paper/course-essay scope, optional evidence-linked author profiles, a lightweight composition handoff with `human-writing`, proportionate outputs, and an explicit ban on presenting editorial scores as AI probabilities. Profile evidence defaults to paraphrase and locator; activation is explicit and respects disabled/ignore states. One shared portable profile supports both skills. These are local design decisions, not features claimed for the researched projects.

Distribution is GitHub-only. The inherited npm publication workflow was removed from this candidate, while `private: true` and the local installer remain. Historical upstream URLs are retained solely for attribution; current repository, issue tracker, homepage, and directory metadata use the user-selected `vannyben7/writing-skills` destination.

Examples are checked as semantic mappings: all measurements and factual context appear in each example's input; an unsupported property becomes a focused query; multiple constraints stay independent; deliberate non-edits cover useful Chinese transitions, negative findings, author stance, and formal guarantees. These checks support internal consistency only. Independent baseline/candidate behavioral evaluation remains separate.
