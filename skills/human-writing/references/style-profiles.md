# Optional style profiles

Profiles are portable, editable Markdown or JSON files outside the shared skill.
They describe observable writing choices, not identity, personality, beliefs, or
biographical facts. An ordinary rewrite needs no profile and must remain available.

## Natural-language entry points

| Request | Action |
| --- | --- |
| “学习我的风格：以下是我写的三段文章” / “Learn my style from these samples” | Extract a provisional profile from those samples, then show a small calibration revision. Do not modify the shared skill. |
| “这是我喜欢的文章，不是我写的；学它的论证方式” | Record `target-style` observations, separate from `self` evidence. Do not claim they are the user's established habits. |
| “按 writing-profiles/research.md 改写” / “Rewrite with this profile” | Read that profile and its enabled state; apply its language and genre layers only if enabled or explicitly overridden for this turn. |
| “这个档案虽然停用了，但这次明确使用它，不要修改保存状态” | Use the named disabled profile for this turn only; leave its `enabled` field and saved selection unchanged. |
| “这次不用档案” / “Ignore my profile this time” | Do not read or apply a profile this turn. Keep its file and future selection unchanged. |
| “查看/纠正/补充/切换/停用/删除这个档案” | Apply the specific management action below to the resolved profile. |

No slash command or flag parser is required. A sample supplied to guide one rewrite
can be used transiently without creating a saved profile. If no samples are supplied,
say that a personal profile cannot yet be inferred and continue any requested rewrite
with defaults. Do not label a stock voice or TEST fixture as the user's profile.

## Learn, then calibrate

1. **Resolve evidence.** Read samples the user provided or specifically placed in
   scope. Reuse existing authorization; do not ask again for the same material.
   Do not search private folders, messages, or accounts merely because they exist.
   Record each source's subject type separately: the user's own work (`self`), an
   admired third-party target (`target-style`), or synthetic material (`synthetic-test`).
   Also record translated work or unknown authorship; do not count them as confirmed
   self-writing. Mixed or heavily edited material is weaker evidence.
2. **Extract observations.** Look for paragraph progression, relative space given
   to points, evidence placement, qualification, openings/endings, syntax, register,
   and punctuation. Explain each tendency with sample IDs and paragraph locations.
   Store only an evidence paraphrase and sample locator by default, not the raw
   passage, private facts, names, stories, or distinctive quotations. Authorization
   to read or learn from a sample is not permission to retain its wording. Use exact
   snippets only when the user requests or permits retaining them, and record that
   permission alongside the retained snippet. A locator such as “sample S2, ¶4”
   is enough; a portable profile should not depend on an inaccessible absolute path.
3. **Separate scopes and confidence.** Maintain common observations, language
   layers (`zh`, `en`, or other explicit tags), genre layers (`academic-paper`,
   `course-essay`, `personal-article`), and language×genre exceptions where needed.
   Mark each observation `tentative` or `stable` and distinguish an explicit user
   preference from an inference. Repetition in one essay does not establish a
   universal habit. A few samples remain provisional; stable empirical habits
   need recurring evidence across suitable samples plus user calibration feedback.
   A stated preference can be stable as a preference without claiming validation.
4. **Produce a reviewable profile.** Show the observations, evidence, gaps, and a
   few likely style choices in normal language. If saving was requested, use the
   named path, or a nonconflicting `writing-profiles/<descriptive-id>.md` in the
   working project when none was named. Keep it outside this skill package. Never
   overwrite an unrelated file or an existing profile merely because its name fits.
5. **Calibrate on a small passage.** Apply the provisional observations to one short
   paragraph of the draft or a user-selected passage. Show what changed and which
   profile observations explain it. Invite correction of the profile, not just the
   passage. Record actual feedback; do not assume approval from silence. If the user
   also requested a full rewrite, complete it with the provisional profile and make
   the limited status clear rather than blocking the work for optional feedback.

Calibration verifies preferences for the reviewed context only. It is not proof of
indistinguishability, detector performance, or a validated personal writing model.
Do not mark a profile calibrated until the user has reviewed a calibration example.

## Apply the profile

Choose the explicitly named profile or the one the user has selected in this task.
An explicit “no profile this time” is resolved before profile loading: do not read
or apply any profile or consult a saved profile selector, and do not change saved
state. Do not auto-load a context file, a nearest profile, or an old private sample.
If no selection is available, use the ordinary workflow. A missing named
profile is a stated limitation: continue independent editing with defaults and do
not pretend to have matched it. If exact profile matching is the entire request,
ask for the missing file.

Check the selected profile's `enabled` field before applying observations. If it is
`false`, do not apply the profile merely because the user names or selects it. State
that it is disabled and continue any independent rewrite with defaults. An explicit
instruction to use that disabled profile for this turn authorizes a temporary
override, with no saved mutation. An explicit request to enable it authorizes
updating that exact profile's flag. Neither action makes it the persistent default;
persist a default only when the user explicitly requests that choice. For a legacy
profile with no flag, follow an explicit current selection but do not infer a saved
default or silently add an enabled flag.

Current user constraints and semantic fidelity govern all style choices. Within
those limits, a relevant language×genre observation refines its language or genre
layer; those refine the common layer. Prefer explicit user corrections over older
inferences and stable observations over tentative ones. Explain a consequential
unresolved conflict briefly; do not silently combine incompatible rules.

When the user explicitly asks for restraint grounded in supplied details, you may
compress or remove rhetorical inflation that the passage's concrete details and
own qualifications do not sustain; do not merely substitute equally grand synonyms.
Retain concrete events, actual positions, distinct meaningful beliefs or emotions,
and uncertainty. This is not permission to delete substantive author interpretation.

Chinese samples alone leave the English syntax layer unobserved. An inferred habit
can transfer between languages only as a tentative rhetorical hypothesis, never as
an instruction to copy word order, punctuation rate, or sentence length. A temporary
request for a warmer or more formal tone affects this task, not the saved profile.

Keep profile content out of the article. Learn that a writer often begins with a
concrete observation, for example, without moving the sample's childhood memory,
medical history, employer, private names, favorite metaphor, or quotation into a
different piece. Revisions produced by this skill do not become self-authored sample
evidence unless the user explicitly adopts them for that purpose.

## User control

Resolve the exact profile by its ID/path before a persistent change. If a reference
is ambiguous, ask which profile; any independent prose edit can continue.

- **View:** show the profile and its evidence/confidence/coverage, with its path.
- **Correct:** update the named observation, retain unaffected observations, and
  record the user's correction as stated evidence. Do not average it with a rejected
  inference or preserve private material the user asked to remove.
- **Add samples:** add sample IDs, recompute affected observations, and keep any
  conflicting evidence visible as a limitation. Do not silently promote confidence.
- **Switch:** select the named profile for the current task. Persist a default only
  if asked, using a user-visible project selector outside the shared skill; report
  its exact path. Switching alone does not override `enabled: false`. Do not merge
  two profiles unless requested.
- **Disable/enable:** for an explicit persistent request, set the named profile's
  `enabled` field to `false`/`true`. Disabling also clears a saved selector entry
  pointing to that exact profile, if present, while retaining the profile itself.
  Enabling does not select a default. “This time” means no saved mutation and, when
  ignoring profiles, no profile loading.
- **Delete:** an explicit request authorizes deletion of that exact profile and a
  stale selector entry pointing to it. Do not delete its source samples, other
  profiles, shared skill files, or a whole directory. Prefer recoverable removal
  when available, and state what was removed and whether recovery is possible.

## Portable representation

Use either Markdown with labeled fields/tables or JSON with the following concepts.
The field spellings are a local convention, not a requirement to install a parser.
A Markdown file must remain understandable and editable without a tool.

| Field | Content |
| --- | --- |
| `profile_id`, `format_version`, `updated_at`, `enabled` | Unique local ID, format version, date, and persistent availability |
| `subject_type` | `self`, `target-style`, or `synthetic-test` |
| `status` | `provisional` or `user-calibrated`; a TEST fixture remains `synthetic-test` |
| `sample_evidence` | IDs, language, genre, source subject type/authorship, locator, evidence paraphrase, retention choice, and any exact-snippet permission |
| `common`, `languages`, `genres`, `language_genre` | Observation arrays, each with `id`, `choice`, `evidence`, `stability`, `basis`, and scope limits |
| `calibration` | Passage locator, applied observations, actual user feedback, and date, or `not yet reviewed` |
| `limitations` | Missing language/genre coverage, small samples, contradictory evidence, unknown authorship |

Use sample IDs plus short evidence paraphrases to make an observation reviewable.
Empty arrays and explicit “unobserved” coverage are valid; do not fill gaps with
stereotypes. For machine-readable users, see the deliberately synthetic
[TEST fixture](../assets/TEST-profile.json). It illustrates the fields; it is not
a default profile. Its `enabled: false` must be honored unless a test/demo explicitly
requests temporary use of that disabled fixture; never silently enable it.
