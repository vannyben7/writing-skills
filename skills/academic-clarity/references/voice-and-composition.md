# Optional voice calibration and composition

Academic Clarity works without a profile or another skill. Use this reference only for a user-selected profile, samples explicitly supplied as style guidance, or a requested combined pass with `human-writing`. Do not search private folders, messages, or accounts for samples. Do not require users to provide personal writing to obtain an ordinary edit.

## One portable profile, explicit selection

Accept the same portable Markdown or JSON profile as `human-writing`; equivalent headings are acceptable. There is no Academic Clarity-specific profile schema, parser, or companion dependency. Profiles belong outside shared skill packages. Reading a profile to apply it does not authorize updating it, saving a new profile, or copying source samples into the package.

| Shared field | Meaning |
|---|---|
| `profile_id`, `format_version`, `updated_at`, `enabled` | Local identity, format version, date, and persistent availability. |
| `subject_type` | `self`, `target-style`, or `synthetic-test`; these evidence types remain distinct. |
| `status` | `provisional`, `user-calibrated`, or `synthetic-test`; no calibration is inferred from silence. |
| `sample_evidence` | Sample ID, language, genre, authorship, `subject_type`, locator, evidence paraphrase, and retention choice; distinguish self/target/synthetic evidence per sample as well as at profile level. |
| `common`, `languages`, `genres`, `language_genre` | Scoped observations with `id`, `choice`, `evidence`, `stability`, `basis`, and scope limits. |
| `calibration` | Reviewed passage, applied observations, actual user feedback and date, or an explicit unreviewed status. |
| `limitations` | Missing coverage, limited samples, contradictions, and unknown authorship. |

Apply only a profile explicitly selected by the user for the current task. Do not auto-load the nearest file, a prior private sample, or a demonstration fixture. If none is selected, use the supplied draft's register and current instructions. If a selected file is unavailable, state that limitation and continue independent editing; do not claim a personal style match.

`enabled: false` remains disabled even when the user names the profile. Only an explicit request to use that disabled profile temporarily or reenable it changes this decision. Temporary use does not alter the saved field. A request to reenable persistently changes only the resolved profile's enabled flag, not the saved default or selector; naming alone is not reenabling. Persist a default only on explicit request. If the wording is ambiguous, leave it disabled and complete independent work.

“Ignore this time” means do not load or apply any profile or consult a profile selector for this task; leave saved profile contents and selectors unchanged. A view-only request may inspect a profile without applying or activating it. Persistent correction, switching, disabling, or deletion requires that specific user request and a resolved target; applying a profile does not imply those mutations.

## Evidence, privacy, and scope

Profile evidence defaults to a brief paraphrase plus a sample locator such as `S2, paragraph 4`. Do not retain private verbatim passages, distinctive quotations, names, or facts in a saved profile without the user's permission. A sample provided to guide one rewrite may be used transiently; that alone is not permission to save the sample or create a lasting profile. No collection of additional private samples is needed for this audit.

Keep self-authored evidence separate from third-party target style and synthetic tests. A synthetic example is never evidence about the user. Model-edited prose is not self-authored evidence unless the user explicitly adopts it for that purpose. Do not infer identity, beliefs, experiences, or demographic traits from stylistic observations.

Use only the language and genre layers supported by the selected profile. Chinese samples do not establish English syntax preferences. A possible transfer of rhetorical organization across languages remains a tentative hypothesis, not permission to transfer word order, punctuation frequency, or sentence length. Distinguish `academic-paper`, `course-essay`, and `personal-article` coverage. Personal articles normally use `human-writing` alone; a profile's personal-article layer does not expand Academic Clarity into a general writing service.

Explicit user corrections take precedence over older inferred observations. Relevant language×genre observations refine broader layers; stable observations are more dependable than tentative ones within their supported scope. A stated preference is not empirical proof of an established habit. Do not fill missing coverage with a stock personality or mark a profile calibrated without actual feedback.

A profile controls expression only. It cannot supply a new belief, strengthen a causal claim, remove a necessary limitation, or transplant a sample's anecdote into the manuscript. Preserve the original author stance even when a profile favors first-person or more direct prose.

## Optional shared handoff

For an explicitly requested combined pass, the sequence is:

`original → academic-clarity → human-writing → semantic comparison with original`

Keep the original available through the final check. Both skills work independently; neither invocation, a handoff artifact, nor an automatic repeat cycle is required. If the user requests a different sequence, respect it and still compare the final text against the original. Return after the requested pass and identify any remaining issue.

Accept a short note, table, or structured object. These are the same optional headings used by `human-writing`; map equivalent wording to them rather than demanding exact spelling:

| Field | Meaning |
|---|---|
| `mode`, `language`, `genre`, `audience` | Requested work and context. |
| `protected_claims` | Claim IDs, actor, assertion, scope, comparison, certainty, and negation to retain. Include independent sample, causal, source, and representativeness limits. |
| `protected_spans` | Exact strings, formulas, citation keys, or other immutable manuscript material. |
| `citation_roles` | Which proposition a citation supports, qualifies, exemplifies, or disputes. |
| `permitted_changes` | Authorized degree of reordering, syntax revision, or local editing. |
| `unresolved_issues` | Ambiguous relations, unverified sources, missing evidence, or a retained `QUERY`. |
| `profile` | A user-selected profile path or an explicit instruction to ignore profiles; selection remains subject to enabled state and scope. |

Read the source as well as the handoff. An omitted item in the handoff does not authorize removing it from the source. Maintain null findings, rivals, counterexamples, reproducibility detail, citation roles, and local qualifications through the style pass. Remove a wrapper only when its propositional content survives. A pattern ID or a request for stronger voice never overrides a protected claim.

If the source and handoff disagree, identify the specific conflict and preserve the source pending clarification while completing independent edits. If the user explicitly authorizes a substantive change, record it as a substantive change rather than describing exact fidelity. A brief internal list often suffices for a short passage; save a separate handoff only when useful and within the requested deliverable.

The final check compares certainty, causality, negation, scope, evidence status, citation attachment, numbers, and author stance against the original. Restore lost information or leave a focused unresolved note; do not start an unbounded audit/rewrite loop.
