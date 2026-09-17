---
name: academic-clarity
description: Audit or revise defensive framing in English and Chinese academic papers and course essays while preserving evidence boundaries, argument, and author voice. Use for unnecessary disclaimers, repeated caveats, prebuttals, and result excuses; not for general writing, personal articles, fact-checking, or AI detection.
license: MIT
metadata:
  version: "1.1.1"
  status: local-candidate
---

# Academic Clarity

Local candidate 1.1.1. The GitHub-only publication target is `vannyben7/writing-skills`, under `skills/academic-clarity`. The candidate status does not assert that publication has occurred.

Make the supported argument easier to read while keeping what the text actually says. Work in the original language and academic register unless the user requests a change. Apply to empirical, qualitative, theoretical, interpretive, and course-essay prose; an essay's reasoned position is an authorial commitment, not an empirical finding to invent or remove.

## Scope and mode

- **Audit only:** When the user asks to inspect, diagnose, or audit without rewriting, identify issues and recommend actions. Leave the manuscript unchanged. Give replacement text only if requested; an audit does not silently become a cleanup.
- **Revise:** A request to rewrite, polish, or clean up authorizes ordinary edits within the supplied scope. Complete clear edits directly; no preliminary contract, manuscript lock, or repeated approval is required. Retain genuinely ambiguous passages, mark `QUERY`, and finish independent edits.
- **Full paper:** Review the supplied manuscript across sections, including material captions and notes. Do not claim to have checked absent sections. Respect any supplied project locks, rubric, terminology, and tracking requirements.

This is a defensive-framing and evidence-boundary task, not a general writing or fact-checking service. Personal articles normally use `human-writing` alone; do not add an academic audit simply because another editor is available. Do not score novelty, acceptance prospects, research quality, or AI authorship. If a sentence's factual truth cannot be established from supplied material, preserve its status or flag a focused query. A style request does not authorize new evidence, citations, experiments, external searches of an unpublished manuscript, or a different thesis.

## Protected information

Before editing, identify the following in the provided passage and its available context. For a short passage this is an internal check, not a mandatory report.

- The proposition and its certainty: possibility, probability, observation, interpretation, or established result. Preserve warranted strong claims as well as cautious ones; neither upgrade nor weaken them merely for tone.
- Association versus causation; causal identification assumptions; necessary versus sufficient conditions; negation, comparisons, and quantifiers.
- Population, case, sample, time, setting, comparison, and applicability; representativeness; novelty and priority claims.
- Evidence status: intended, proposed, authorized, reported, self-reported, observed, implemented, measured, or inferred. A plan is not delivery; a participant's account is not independent verification.
- Negative and null findings, counterexamples, rivals, contradictions, non-adoption, and trade-offs. These may constitute the finding itself.
- Method, provenance, ethical, consent, disclosure, and reproducibility detail; source limitations; direct quotations, citations and their support relationships; numbers, units, dates, and cross-references.
- The author's stated position, conceptual distinctions, and characteristic register. Do not invent enthusiasm, criticism, personal experience, or consensus to make prose sound more human.

Do not fill missing measurements or source details with plausible specifics. When a claim appears unsupported, flag the evidence gap; do not manufacture support or silently replace it with a different claim. Edits may remove rhetorical praise only when no defined or evidenced property is lost.

## Decide in context

Read at least the whole provided paragraph and any supplied evidence it relies on. Use D1–D14 in [references/taxonomy.md](references/taxonomy.md) when classifying candidates; their cue phrases are prompts to inspect, not banned strings. No minimum number of edits is required.

For each candidate, ask:

1. What does the sentence add: a proposition, a boundary, an inference, a contrast, or only repeated framing?
2. What specific information or logical relationship would be lost by changing it?
3. Would the new wording alter any protected information above? Does its citation still support the same proposition?
4. Is the qualification needed here for a reader to interpret this claim correctly?

Describe an observable reading problem, such as a duplicated scope statement, a delayed subject, or an unsupported explanation. Do not infer that an author is anxious or predict that reviewers will distrust, reject, or reward the wording.

Assign a disposition:

| Disposition | Use when |
|---|---|
| `KEEP` | The passage already works or contains information that the proposed edit would lose. Necessary cautions are valid outcomes. |
| `TIGHTEN` | Wording repeats a function; the same proposition and all distinct limits can be expressed more economically. |
| `REFRAME` | The proposition should remain, but sentence order or emphasis obscures it. |
| `RELOCATE` | Another supplied location serves the information better and the local inference stays properly qualified. Name that destination. |
| `CUT` | Only redundant framing disappears; no unique proposition, boundary, citation role, or logical link is lost. |
| `QUERY` | Meaning, support, or required context is missing, and choosing a revision would decide substance for the author. Retain the original and state exactly what is unresolved. |

Optionally classify a passage as `NECESSARY_CAVEAT`, `DEFENSIVE`, `MIXED`, or `CLEAN`; the disposition explains what to do. A taxonomy hit alone cannot justify deletion.

## Rewrite without changing the inference

Use the shortest revision that solves the observed problem. A clear factual or argumentative opening often helps, but a condition may need to lead: “Among respondents who completed both waves…” prevents a broader interpretation from the first word.

Preserve propositions, not necessarily the original sentence divisions. After removing defensive wrappers, read the adjacent sentences together. A definition and its implication, or a result and its qualification, may read more clearly as a connected sentence rather than isolated statements. Join them only when the source already establishes that relationship and each restriction retains its scope. Repair this local flow within the requested framing edit; do not expand it into an unrelated whole-paper stylistic rewrite.

There is **no numerical limit on caveats per claim**. Sample, causal, source, measurement, and temporal restrictions may be independent. Preserve every material restriction, even if several occupy one sentence. Compress only repetition of the same function. “May” and “in this sample” usually do different work.

Positive scope is useful only when it preserves the excluded inference. “We studied three firms” does not convey that those firms are unrepresentative. “The variables were associated” may still need “the design does not identify a causal effect.” Preserve an explicit negative statement when it carries that distinction.

Keep source status, causal limits, and rivals beside the inference they qualify. Methods or Limitations may hold fuller detail, with a concise local boundary where needed. Abstracts, captions, topic sentences, and conclusions may be read alone, so useful repetition across them is not automatically redundant. Never relocate all caution merely to make a contribution sound stronger.

Report a disappointing or null result without apology. Retain an explanatory hypothesis as a hypothesis; do not turn “may reflect measurement error” into a verified diagnosis. Keep a documented reason for an omitted experiment or source when it affects interpretation or reproducibility.

Write in the language and disciplinary style of the text. Chinese expressions such as “然而”“因此”“综上”“值得注意的是”“在一定程度上” are not prohibited. Preserve the contrast, inference, synthesis, emphasis, or uncertainty they actually express; tighten only demonstrable padding. Do not impose English sentence order or casual language on Chinese scholarship. Preserve an author's first-person or impersonal stance unless asked to change it.

Ordinary use needs no voice profile or private samples. Apply a profile only when the user selects it for this task, following [references/voice-and-composition.md](references/voice-and-composition.md). `enabled: false` stays disabled unless the user explicitly requests temporary use or reenabling; naming it alone does not activate it. “Ignore this time” means do not load or apply it and do not change saved state. Evidence defaults to a paraphrase plus sample locator; do not retain private verbatim samples without permission. Academic Clarity can use the same portable profile as `human-writing` without invoking that skill.

For an explicitly requested combined pass, use original → `academic-clarity` → `human-writing` → semantic comparison with the original. The reference defines the optional shared handoff. Neither companion invocation nor a handoff artifact is compulsory, and the sequence is one bounded pass, not an automatic loop.

## Verify the revision

Compare each changed proposition with its original and supplied support. Check that certainty, causality, polarity, scope, representativeness, novelty, and evidence status are preserved; check citation attachment, quotations, numbers, and author stance. If an edit fails, restore the protected detail, revise again, or leave that passage as `QUERY`.

For a full manuscript, also check that qualifications remain accessible where claims recur, conceptual roles remain stable, and moved material has a real destination. Count repeated phrases only when it helps locate a problem; frequency is not a deletion target or evidence of improvement.

Read [examples/before-after.md](examples/before-after.md) when a close case involves several qualifications, an evidence-status distinction, an uncertain explanation, or Chinese academic register. Examples are semantic mappings using their stated inputs, not templates from which to borrow facts.

## Proportionate output

For a short **revision**, return the revised passage first. Add a brief note only for a material decision, retained boundary, or unresolved query; honor “text only.” Do not force a table, score, or lengthy audit onto a sentence-level request.

For a short **audit**, give the disposition and concrete reason for each meaningful issue. It is acceptable to say that the passage should remain unchanged and identify its useful cautions.

For a **full audit** or an explicitly detailed report, use an editable table:

| Location | Original excerpt | D-code / function | Reading problem | Disposition | Information to preserve | Recommendation |
|---|---|---|---|---|---|---|

Add a rewrite column only when requested. Summarize the most consequential changes, important `KEEP` decisions, and unresolved queries; avoid padding to a quota. Rank by risk of misinterpretation and obstruction of the argument, not imagined reviewer psychology. For a full revision, deliver the revised text or requested file plus a concise change and integrity summary. Tracked changes are required only when requested or specified by the project.

A defensive-writing score is optional and only useful when requested. Label any 0–10 score as a subjective editorial heuristic tied to visible examples and the amount of text reviewed. It is not a validated scale, a probability of AI authorship, or a publication forecast. Do not optimize a score at the expense of evidence or voice.

Source provenance, selectively adopted ideas, and rejected rules are documented in [references/sources-and-design.md](references/sources-and-design.md).
