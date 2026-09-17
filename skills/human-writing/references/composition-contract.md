# Composition contract

Human Writing works alone. It can also accept a handoff from `academic-clarity`
or another editor without loading or invoking that skill. The caller owns the larger
workflow; do not create a recursive audit/rewrite loop. When both skills are
requested, use original → academic-clarity → human-writing → original semantic
comparison. This describes an optional composition, not a required dependency.

## Read the handoff as constraints

Accept ordinary prose, a table, or a structured object. Useful fields are:

| Field | Meaning |
| --- | --- |
| `mode`, `language`, `genre`, `audience` | Requested work and context |
| `protected_claims` | Claim IDs and the actor, assertion, scope, comparison, certainty, and negation to retain |
| `protected_spans` | Exact strings, formulas, citation keys, or other immutable material |
| `citation_roles` | Which proposition each citation supports, qualifies, exemplifies, or disputes |
| `permitted_changes` | For example: paragraph order and syntax, or sentence edits only |
| `unresolved_issues` | Unverified sources, ambiguous relations, or missing evidence |
| `profile` | A user-selected profile path or an explicit instruction to ignore profiles; retain any explicit single-turn override of a disabled profile |

These field names are suggestions, not a required schema. Map equivalent headings
such as “保留的科学边界”, “must preserve”, or “claim ledger” to the same constraints.
Do not discard a usable handoff because its headings differ.

Both skills use the same optional profile model: `profile_id`, `format_version`,
`updated_at`, `enabled`, `subject_type`, `status`, `sample_evidence`, `common`,
`languages`, `genres`, `language_genre`, `calibration`, and `limitations`. See
[Style profiles](style-profiles.md) for the field meanings. Evidence defaults to
paraphrase plus locator; retain exact snippets only with user permission. Keep real
profiles outside both shared skill packages, separate self/target/synthetic sources,
and apply only the relevant language and genre observations.

Honor `enabled: false`; a named path alone does not activate that profile. Only an
explicit temporary override applies it for this turn without changing saved state.
An explicit persistent enable request may change that exact flag. Ignore-this-time
means no profile loading, application, or saved mutation. Persist a default only
when the user explicitly requests it.

## Apply it

Read the source as well as the handoff. A handoff can omit a source detail; omission
does not authorize its removal. Lock exact spans, map claims to citations, and edit
the authorized prose using the paragraph→sentence→word workflow. The user's current
instruction and preservation of meaning override stylistic preferences.

Keep limitations that academic-clarity or another editor retained for scientific
reasons. Remove a defensive wrapper only when its entire propositional content
survives. Do not introduce a
new reviewer, objection, comparison, caveat, or claim that a limitation has been
resolved. A pattern ID never authorizes deleting a protected claim.

If the handoff contradicts the source, identify the exact conflict and preserve the
source pending a decision; continue with independent edits. A request for stronger
voice does not resolve a factual disagreement. If the user explicitly authorizes
a substantive change, document it as such instead of reporting exact fidelity.

## Return and verify

Compare the final revision with the original, not only the previous editor's draft.
Omission from an intermediate version does not authorize dropping an original claim.

Return only the caller's requested revision or findings. When an issue must be
surfaced, give the claim/span ID and the unresolved difference in a short separate
note. If a change log is requested, map material restructuring to retained claims;
do not manufacture an “all checks passed” label without comparison.

For example, if `C2` says “association only in the urban subgroup” and citation `[7]`
supports `C2`, both that restriction and citation role must survive. “The intervention
improves outcomes [7]” fails the contract even if it sounds more direct.
