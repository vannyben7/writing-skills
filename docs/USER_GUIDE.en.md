# User guide

[Home](../README.md) · [中文指南](USER_GUIDE.zh-CN.md) · [Evaluation record](../EVALUATION.md) · [Maintenance](MAINTENANCE.md)

For **Human Writing 2.12.1** and **Academic Clarity 1.1.1**. This is a functional experimental release. Overall writing superiority, personal style matching, and AI-detector outcomes have not been established.

Start with sections 2 and 3 if you just want to try a paragraph. Profiles and combined editing are optional.

## 1. What am I installing?

A skill is a folder of instructions and supporting material that an AI assistant reads when doing a task. Its entry point is `SKILL.md`.

These skills are not a new language model, a standalone writing app, a plagiarism checker, or an AI detector. They do not train a personal model. You still need a compatible client and model access. Installing instruction files does not provide a subscription or grant permission to read or modify your documents.

| Your task | Choose | Important boundary |
| --- | --- | --- |
| Improve paragraph progression, repetitive syntax, or how an existing position comes through | `human-writing` | Do not invent facts, beliefs, emotions, anecdotes, or sensory detail |
| Remove repeated defensive framing from a paper or course essay | `academic-clarity` | Preserve distinct sample, causal, source, and scope limitations |
| Edit a personal article or reflective piece | Usually `human-writing` alone | Do not turn it into academic prose merely because another skill exists |
| Understand the problems before deciding on edits | The relevant skill in audit-only mode | Do not silently rewrite or save files |
| Address both academic framing and prose organization | Explicitly request one combined pass | Keep the original available and stop after the requested pass |

Both skills work without samples or profiles. Clear writing can remain unchanged. Strong authorial voice does not require added first-person phrases or a forced alternation of short and long sentences; it can come from the source's priorities and reasoning.

<a id="install"></a>

## 2. Three-minute starting route

This is a short checklist, not a promise about download or generation time.

### Check the prerequisites

You need a client that can load skills or read a complete local skill folder, working access to a model, and a passage you have permission to share. Use a short, non-sensitive passage first.

Here, “client” means the application, command-line tool, or editor extension you use to interact with the AI—not either of these skills.

The Codex examples below are client-specific, not universal instructions for every chat product. Current official documentation describes project discovery through `.agents/skills`, explicit or task-matched invocation, installation from other repositories, and restarting when newly installed skills do not appear. See [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills), checked on 2026-09-18.

### Option A: ask the installer

In Codex with `skill-installer` available, send this as a message, not a terminal command:

```text
Use skill-installer to install these directories from the GitHub repository
vannyben7/writing-skills:
- skills/human-writing
- skills/academic-clarity

Check for existing skills first. Do not overwrite a same-named directory.
If one exists, report its location and version so I can choose what to do.
Install the complete skill folders only, without additional paid tools or services.
Report the actual installation paths and versions when finished.
```

Remove one line if you want only one skill. Where supported, select the installer in the client's skill picker; Codex CLI and IDE also support `$skill-installer`. Downloading may require GitHub access and local permission.

Do not assume the installer uses a particular directory: ask it to report the actual destination. An existing environment may use `.codex/skills`, but that is not this guide's universal default.

### Option B: copy into your writing project

Download and extract [this repository](https://github.com/vannyben7/writing-skills), or use an existing local checkout. Copy the entire selected folder into your writing project's `.agents/skills` directory:

```text
your-writing-project/
└── .agents/
    └── skills/
        ├── human-writing/
        │   ├── SKILL.md
        │   └── all supporting files and folders
        └── academic-clarity/
            ├── SKILL.md
            └── all supporting files and folders
```

Keep references, assets, and hidden metadata. Copying only `SKILL.md` loses supporting rules. Stop if the destination already exists; compare versions and local changes before replacing anything.

For macOS/Linux shell users, this example skips existing destinations, including symbolic links. Replace the source placeholder and run it from the intended writing project. Windows users can perform the same non-overwriting copy with a file manager.

```bash
writing_skills_source="/path/to/writing-skills"
for skill_name in human-writing academic-clarity; do
  source_dir="$writing_skills_source/skills/$skill_name"
  destination=".agents/skills/$skill_name"
  if [ ! -f "$source_dir/SKILL.md" ]; then
    printf 'Source missing: %s\n' "$source_dir"
  elif [ -e "$destination" ] || [ -L "$destination" ]; then
    printf 'Already exists; not copied: %s\n' "$destination"
  else
    mkdir -p .agents/skills && cp -R "$source_dir" "$destination"
  fi
done
```

Check the working directory before copying; do not run concurrent copies. Other clients may use different discovery directories. This repository does not ask you to install a paid tool, npm package, or separate service.

There is no repository-root Claude marketplace. The marketplace metadata inside the Human Writing subfolder is local to that package. Academic Clarity's optional Node installer copies instruction files; it is not the writing engine and is not needed for this route.

### Option C: try it without installation

A file-capable client can read a downloaded complete skill folder directly:

```text
Read SKILL.md in the human-writing folder I have provided, and load the references
needed for this task. Then revise the passage below in your reply only.
Do not modify any files.
```

Actually provide an accessible folder or location. A name, a typed local path that the client cannot access, or a link alone does not prove that the skill was loaded. A plain chat interface without skill or file access will not acquire this repository's rules merely because you mention its name.

### Confirm discovery and try a paragraph

Ask the assistant to report the skill's actual name, version, and readable path. If Codex has not discovered it, restart and check the folder placement and permissions. Same-named skills do not automatically merge; select the intended source. [Official discovery guidance](https://learn.chatgpt.com/docs/build-skills)

Then try:

```text
Use human-writing to revise this course-essay paragraph.
Improve the connection between the argument and evidence.
Preserve every fact, citation, qualification, and my existing position.
Return the revised text only. Do not use a profile or change files.

[Paste the passage here.]
```

In Codex CLI / IDE, `$human-writing` is an explicit skill mention. Other clients have their own picker or invocation mechanism. Compare the reply with the original before applying it to more of your work.

<a id="modes"></a>

## 3. Be clear about the action and deliverable

### Audit only

Use this when you want to make the editorial decisions yourself:

```text
Use academic-clarity to audit these two paragraphs.
Identify repeated defensive framing and explain which limitations must remain.
Do not rewrite the passage or modify files. KEEP is a valid outcome.

[Paste the passage.]
```

You may see these dispositions:

| Label | Meaning |
| --- | --- |
| `KEEP` | The passage works, or the proposed change would lose information |
| `TIGHTEN` | Compress repetition without changing the proposition or its limits |
| `REFRAME` | Change order or emphasis while keeping the same claim |
| `RELOCATE` | Move information to a specific supplied destination while retaining needed local limits |
| `CUT` | Remove framing that contributes no distinct information or relationship |
| `QUERY` | Preserve an unresolved passage and ask what its meaning or support is |

These are editorial decisions, not scores. A source that cannot be verified is not automatically false and should not silently disappear.

### Rewrite in the reply

```text
Use human-writing to revise this personal article.
Keep my hesitation, humor, and concrete details. Add no experiences or feelings.
Return the revised English prose only, without a score or file changes.

[Paste the passage.]
```

The skills work in the source language unless you request otherwise. Revision is not automatic translation. Ask for explanations, alternatives, or a comparison table if you want them; these are not compulsory outputs.

### Save a revised file

A separate output file is a useful first step:

```text
Use human-writing to read draft.md and save a revised copy as draft.revised.md.
Keep the original unchanged. If the destination already exists, stop and ask.
Edit prose only; preserve YAML, citation keys, formulas, code, and link targets.
Summarize material changes and unresolved issues.
```

If you want an in-place edit, explicitly name the file and authorized scope. Merely giving a path as the source does not mean “overwrite it.”

YAML in the example refers to metadata that may appear at the start of a file. Citation keys, code, and link targets are also more than prose wording; omit these details when your plain-text document has none.

Reading and writing permissions, Word tracked changes, PDF extraction, and layout preservation depend on the client and its document tools. These skills do not supply document converters. Inspect formatted documents after editing.

### A reusable request template

```text
Skill: human-writing or academic-clarity
Language and genre: for example, an English course essay
Action: audit only / revise in the reply / save to a named file
Reader and purpose:
Allowed changes: for example, reorder paragraphs but add no claims
Must preserve: facts, citations, uncertainty, terminology, my position
Profile: none this time / the exact selected path and any temporary override
Deliverable:

Source:
...
```

For a short task, you do not need every field. The source, requested action, and protected information matter most.

<a id="examples"></a>

## 4. Worked examples

These examples are newly written, synthetic illustrations—not real research, evaluation cases, private samples, or recorded model outputs. They show possible edits, not guaranteed results.

### Human Writing: foreground an existing argument

Before:

> This essay considers scheduling policy. When schedules change unpredictably, employees may struggle to plan care. Six interviewees mentioned last-minute shift changes. Four of those six said they had cancelled care arrangements as a result. I argue that scheduling policies should be assessed not only by staffing costs but also by employees' ability to organize their lives.

One possible revision:

> I argue that scheduling policies should be assessed not only by staffing costs but also by employees' ability to organize their lives. When schedules change unpredictably, employees may struggle to plan care: six interviewees mentioned last-minute shift changes, and four of those six said they had cancelled care arrangements as a result.

The existing position moves forward; related evidence stays together. Six, four, “may,” and “said” remain. The revision does not turn interview accounts into independently verified outcomes or invent another employee's story.

### Academic Clarity: remove framing, keep the boundary

Before:

> It is important to note that the study included only 48 students from two urban schools, so the results do not represent other schools. It should also be emphasized that participation frequency was associated with final grades, but this association does not establish causation.

One possible revision:

> The study included only 48 students from two urban schools, so the results do not represent other schools. Participation frequency was associated with final grades, but this association does not establish causation.

This assumes the opening phrases add only repeated framing in context. The sample, setting, representativeness limit, association, and causal limit remain. “Participation improves grades” would not be an equivalent revision. A phrase such as “it is important to note” is not a banned string.

### Several caveats may all be necessary

> Among the 24 respondents who completed both surveys, reported confidence increased. The convenience sample does not represent all students, and the before–after comparison does not identify a causal effect.

`KEEP` is reasonable. The population, completion condition, reported outcome, representativeness limit, and causal limit serve different purposes. There is no quota requiring their removal.

### Check every revision against the original

Look for changes to numbers, units, ranges, time, negation, comparisons, certainty, causal inference, and evidence status. A plan is not an implementation; self-report is not an independent measurement. Check that each citation still supports, qualifies, or disputes the same proposition. Preserve meaningful beliefs, emotions, irony, and uncertainty without inventing new ones.

For a long document, work in coherent sections with enough context, then check cross-section consistency. A series of fluent isolated sentences can still misstate the overall argument.

<a id="profiles"></a>

## 5. Optional style profiles

A profile is an editable Markdown or JSON file outside the shared skill package. It records supported observations about expression, not personality, identity, biography, or a trained imitation model.

You can skip profiles entirely. A sample may guide one revision without being saved.

### Learn from authorized samples, then calibrate

```text
Use human-writing to examine these three course-essay passages I wrote.
Show provisional observations with sample and paragraph references and clear gaps.
Try them on the short draft I will provide next.
Do not inspect other files or save a profile or sample text yet.
```

If you later want a saved profile, explicitly request the path and retention limits:

```text
Save the provisional observations I have confirmed to writing-profiles/course.md
in my writing project, outside the shared skill folders.
If the file exists, ask before replacing it.
Retain evidence paraphrases and sample locators only, not verbatim samples or
private names and facts. Do not mark an unreviewed calibration as validated.
```

A few samples support tentative observations. Calibration means you review a small application and correct the observations; silence does not establish approval. A stated preference is evidence of that preference, not proof of a long-term habit.

Profiles distinguish common observations, language layers, genres, and language-by-genre exceptions. Chinese samples do not establish English syntax preferences, and course-essay habits need not apply to personal articles.

### Separate your work from an admired target

```text
This is someone else's article that I admire, not my own writing.
Record target-style observations about how it develops evidence and counterexamples.
Do not copy its experiences, opinions, distinctive wording, or private details
into my draft.
```

The source categories are `self`, `target-style`, and `synthetic-test`. Translated, heavily edited, or uncertain-authorship material needs appropriate labeling. Model-edited prose does not automatically become evidence of your own unaided writing habits.

### Select, inspect, disable, or ignore

| Request | Expected behavior |
| --- | --- |
| “Use this enabled profile for this passage; do not update it” | Apply only its relevant language and genre observations |
| “Show this profile, its evidence and limitations, without applying it” | Inspect without activating or changing it |
| “Correct this observation / add these authorized samples” | Make the requested scoped update; preserve unresolved conflicts |
| “Switch to this other profile for this task” | Select it for the task; do not silently merge profiles or save a default |
| “Disable this exact profile, keeping the file” | Set `enabled: false`; clear a saved selector pointing to it if one exists |
| “Although disabled, explicitly use it this time only” | Apply a temporary override without changing saved state |
| “Ignore profiles this time” | Do not load or apply one, consult a selector, or alter saved state |
| “Reenable this profile, but do not make it the default” | Change its enabled flag only |
| “Save this profile as my default” | Persist a visible selection only because requested; do not implicitly change a disabled flag |
| “Delete this exact profile, not its samples or other profiles” | Remove only the resolved profile and stale association; explain recoverability |

Naming a disabled profile alone does not activate it. Applying a profile does not authorize editing it. If a selected file is missing, the assistant should say so and continue independent editing where useful, not claim a successful personal style match.

In this version, an explicit request for restraint grounded in supplied details can justify compressing rhetorical inflation the passage's details and qualifications do not sustain. This is not permission to delete substantive interpretation: actual positions, distinct beliefs or emotions, concrete events, and uncertainty must remain.

### Privacy is more than a local file location

The skill instructions call for authorized material only, evidence paraphrases plus locators by default, and permission before retaining exact snippets. They do not authorize searching private folders for more samples.

The model provider and client may still process supplied text remotely. A local profile file does not prove local-only inference, and a “do not save samples” request is not a substitute for the provider's data policies. Redact sensitive material and check permission to share unpublished or third-party work.

Keep actual profiles and samples outside this public repository and the shared skill folders. Review locators and retained snippets for private information before migration or sharing. The bundled [TEST profile](../skills/human-writing/assets/TEST-profile.json) is disabled synthetic demonstration material, never your profile.

See the complete [profile protocol](../skills/human-writing/references/style-profiles.md) and [Academic Clarity compatibility rules](../skills/academic-clarity/references/voice-and-composition.md). These are behavioral instructions, not a security enforcement layer. Verify important saved-state changes in the actual file.

<a id="combine"></a>

## 6. Use both skills only when the task needs both

```text
Perform one combined pass on this academic passage:
academic-clarity first, then human-writing.
Carry forward all protected claims, citation roles, and unresolved questions.
The second pass must read the original as well as the intermediate draft.
Finally compare with the original and return the finished passage plus any
necessary unresolved issue. Do not loop, use a profile, or change files.
```

The sequence is original → Academic Clarity → Human Writing → semantic comparison with the original.

For a short passage, a brief handoff note is enough. For complex material, useful headings include protected claims, exact spans, citation roles, permitted changes, unresolved issues, and the selected profile or instruction to ignore it. No separate file or companion installation is required for either skill alone.

Omission from the intermediate draft does not authorize dropping information from the original. A style pass must not silently resolve an unverified source or strengthen a conclusion. See the [composition contract](../skills/human-writing/references/composition-contract.md).

<a id="troubleshooting"></a>

## 7. Troubleshooting

| Problem | First checks |
| --- | --- |
| Skill missing after installation | Correct project and discovery directory? A complete folder with `SKILL.md` directly inside? Read permission? Restart if discovery has not updated |
| Duplicate skill names | Check source paths and select one; keep backups outside discovery directories rather than expecting merging |
| Result looks like an ordinary generic reply | Ask which actual skill file and version were read; a name alone does not load unavailable resources |
| An unwanted skill was selected automatically | Specify the desired skill/task; use the client's skill controls for persistent disabling, which is different from disabling a profile |
| Too much rewriting or an overly casual tone | Specify genre and allowed scope; try audit-only first and identify valuable original passages |
| A fact or citation changed | Keep the original, point out the exact mismatch, and request restoration; clarify genuinely ambiguous source material |
| Profile is disabled | Explicitly authorize temporary use if intended, or request no profile; do not assume naming it reenables it |
| No file was saved | Check client write permission and format support; name an explicit output path |
| Word, PDF, or tracked changes are needed | Use suitable client document tools and verify the resulting file; these skills are not converters |
| Network error, timeout, or quota limit | Check the download/model service and whether output already completed before rerunning the whole job |
| Output differs from the example | Examples are not fixed answers. Check meaning, task, model, and version rather than matching wording |
| An AI-detector score did not change | Detector performance is not a goal or acceptance criterion of this project |

<a id="versions"></a>

## 8. Versions, backups, migration, and rollback

Read the installed skill's `metadata.version` in `SKILL.md`, not just the repository heading. Some instruction files retain candidate wording from their evaluated source; the public distribution is a functional experimental release, not an upstream official update.

For an update:

1. Record the actual installed path, version, source revision, and your local changes.
2. Back up the whole old skill folder outside discovery locations. Back up private profiles separately.
3. Obtain the new version in a separate location and read its changes and [evaluation record](../EVALUATION.md).
4. Do not blindly overwrite a same-named directory. After deciding to replace it, move the old copy out of discovery and install the complete new folder.
5. Refresh discovery, confirm the actual version, and try a short non-sensitive passage.
6. To roll back, move the new copy aside and restore the complete previous folder. Do not delete manuscripts, samples, or profiles.

These are reviewable manual steps, not a claim that the repository provides an automatic rollback command. Updating a repository checkout does not automatically update a separately copied installation. Symlinks or other separately configured managers may behave differently.

If migrating from `humanizer` or `academic-defensive-writing-auditor`, inspect the old package and customizations, then deliberately update your prompts and workflow references. The new versions are not guaranteed drop-in equivalents. Avoid ambiguous use of both old and new copies; do not delete an existing skill without an explicit decision.

The current two skills share a portable profile model, but arbitrary third-party legacy profiles are not guaranteed to migrate automatically. Check source categories, language/genre coverage, enabled state, saved selectors, evidence locators, and retained private snippets. Applying a profile is not migration authorization.

See [MAINTENANCE.md](MAINTENANCE.md) for repository maintenance and release procedures. This guide does not require scheduled tasks, paid tools, or automatic updates.

## 9. Costs, network access, and dependencies

The instruction packages do not supply a model account or their own billing service. Your client/provider's current subscription, usage, rate-limit, network, and privacy rules still apply. The repository does not promise a particular price or free model usage.

GitHub installation normally needs network access. Generation depends on your model deployment; local files do not make a cloud model offline. Longer drafts, samples, references, and combined passes increase processing volume.

Ordinary prose use needs no Python or Node.js installation. Maintainers need the relevant runtimes for the repository's offline structural checks. File access, document conversion, tracked changes, and persistence depend on client tools and permissions.

There is no separate “Human Writing upload service” required by this package. That does not remove the data processing performed by whichever AI service you use.

## 10. What the evidence does—and does not—show

The [evaluation record](../EVALUATION.md) is the authoritative account; its different stages must not be combined into one success rate.

- General rewriting: 8 source texts, 15 source/path combinations, 45 outputs, and 60 valid judge observations. Most comparisons were ties; some apparent wins have disputed fidelity judgments.
- Before the profile-specific fix: 11 of 12 synthetic workflow checks passed. The remaining issue concerned insufficient stylistic restraint.
- Targeted profile regression: Human Writing 2.12.1 passed 5/5, versus 4/5 for 2.12.0. This deliberately selected set includes the known failure and protective cases, not a broad random blind test.
- The evaluation record's 36 offline tests belong to the historical writing-evaluation harness, not 36 additional writing cases or the current repository's total test count. The root structural check also runs mocked maintenance-utility unit tests; those are counted separately from this historical figure and are not writing cases either.
- Heldout generalization, real private-profile calibration, actual persistent-state operations, user preference acceptance, personal style similarity, and detector evasion have not been established.

General rewriting used Human Writing 2.12.0 and Academic Clarity 1.1.1. Human Writing 2.12.1 leaves the ordinary editing entrypoint body unchanged; its profile-reference change was assessed separately. The model-based judgments are not independent user endorsement or a guarantee of factual fidelity.

For academic or course work, follow your institution's rules on AI assistance and authorship. You remain responsible for the argument, facts, and citations.

## 11. Licenses and attribution

Original repository-level integration documentation and validation code use the root [MIT license](../LICENSE). The skill packages retain their own original licenses and copyright notices.

Human Writing derives from the supplied `blader/humanizer` package; Academic Clarity derives from `Worigin0314/academic-defensive-writing-auditor`. These names and versions do not claim an upstream release or endorsement. Preserve the relevant licenses and notices when redistributing. See [third-party attribution](../THIRD_PARTY_NOTICES.md).

Start small: choose one skill, make the requested action explicit, and check that the revision still says what you intended.
