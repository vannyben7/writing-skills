# Human Writing — functional experimental edition

Version **2.12.1** is an independent local derivative of the supplied
[blader/humanizer](https://github.com/blader/humanizer) 2.11.2 package. It is not an
upstream release or an automatic update to the installed skill. The current skill,
plugin, and marketplace IDs are `human-writing`; the original MIT license and Siqi
Chen copyright are retained. Old project names and URLs below identify sources only.

This experimental distribution is maintained in
[vannyben7/writing-skills](https://github.com/vannyben7/writing-skills), under
`skills/human-writing`. Overall style superiority has not been demonstrated.
Repository-level installation and marketplace configuration belong to that repository's
root; the `.claude-plugin/marketplace.json` in this package is local-only and its
`./` source refers to this package directory.

Human Writing audits or revises Chinese and English academic papers, course essays, and
personal articles. It makes the author's emphasis and reasoning more apparent while
preserving claims, source roles, qualifications, terminology, and good existing prose.
It edits paragraphs before sentences and words. It does not infer AI authorship,
assign detector scores, or manufacture personal experiences to create a voice.

## Use

Natural-language requests work without options or sample files:

```text
用 human-writing 检查这段学术文字，只指出问题，不改文件。
Use $human-writing to revise this course essay without changing its evidence or argument.
请直接修改 article.md，保留我的语气和所有引文。
```

Audit requests return findings. Rewrite requests return one finished revision.
Editing an actual file follows the user's request to update/save it; naming a path
as the source does not alone authorize overwriting it. File edits protect code,
frontmatter, data, identifiers, formulas, citations, and link targets.

The default works with no samples. A supplied sample can guide one rewrite without
being saved. For a reusable profile:

```text
学习我的风格：这些是我自己写的中文课程论文。把暂定档案保存到 writing-profiles/course.md。
这是我欣赏的文章，不是我的作品。只学习它的论证方式，单独建立目标风格档案。
按 writing-profiles/course.md 改写这段；这次不要增加任何个人经历或观点。
这次不用档案，按原文语境改写。
查看 / 纠正 / 补充 / 切换 / 停用 / 删除指定档案。
```

Profiles are editable Markdown or JSON outside the shared skill. They keep sample
evidence and common, language, genre, and language×genre observations separately.
A few samples produce provisional observations followed by a small calibration
example. Chinese samples do not establish English syntax. The included
[TEST profile](assets/TEST-profile.json) is synthetic and disabled by default; it is
not a learned profile of this user. Merely naming a disabled profile does not enable
it. An explicit instruction to use it for one turn can override the disabled flag
for that turn without saving changes. Ignore-this-time reads no profile and changes
no saved state. Persistent default selection needs an explicit request.

Profile evidence defaults to paraphrases and sample locators; exact snippets require
user permission. See [profile controls](references/style-profiles.md).

## Package layout

- [SKILL.md](SKILL.md): entrypoint, modes, preservation rules, and editing workflow.
- [Language and genre](references/language-and-genre.md): Chinese/English and academic/course/personal guidance.
- [Pattern reference](references/patterns.md): 35 advisory legacy IDs with corrected examples.
- [Style profiles](references/style-profiles.md): extraction, calibration, and user control.
- [Composition contract](references/composition-contract.md): accepts academic-clarity's protected claims without requiring that skill.
- [Sources and decisions](references/sources-and-decisions.md): research, adoption choices, and license status.

Only load the references relevant to the task. There is one skill entrypoint and no
required network service, profile database, or companion skill. A model provider may
still process the text supplied to the agent; this package does not promise that all
writing stays on the device merely because profile files are local.

## The 35 legacy patterns

Each ID points to a possible reading problem. A word or construction is not banned.
The preservation rules take priority over every pattern.

| # | Pattern | Editing decision |
| --- | --- | --- |
| 1 | Inflated significance | Separate ceremony from an actual evaluation |
| 2 | Name-dropping | Keep names and quantities unless summarizing is requested |
| 3 | Participial analysis | Preserve interpretation and attribution |
| 4 | Sales language | Match genre while retaining stated opinions |
| 5 | Vague sources | Flag unverified attribution; do not silently delete |
| 6 | Formulaic outlook | Rebuild progression without losing concrete claims |
| 7 | Stock vocabulary | Diagnose a cluster in context, not a word alone |
| 8 | Copula avoidance | Simplify only when the relation remains the same |
| 9 | Formulaic contrast | Keep meaningful exclusions and negative results |
| 10 | Forced triads | Preserve real categories and simultaneity |
| 11 | Naming/opening repetition | Preserve referents and deliberate repetition |
| 12 | False ranges | Clarify lists; preserve real ranges |
| 13 | Passive voice | Keep useful passive and natural Chinese omission |
| 14 | Dashes | Distinguish interruptions, ranges, and protected syntax |
| 15 | Bold text | Preserve semantic formatting |
| 16 | Labeled lists | Choose a list or prose by logical relation |
| 17 | Title case | Follow the target convention |
| 18 | Emojis | Preserve intentional personal signals |
| 19 | Quote typography | Match format; protect exact quotations |
| 20 | Chat residue | Remove wrappers without inventing content |
| 21 | Knowledge disclaimers | Keep evidence limits and time scope |
| 22 | Reflexive agreement | Separate empty praise from actual agreement |
| 23 | Filler | Shorten without changing relations |
| 24 | Qualifiers | Remove duplication, retain independent limits |
| 25 | Generic endings | End at the existing argument's destination |
| 26 | Hyphenation | Follow lexical meaning and convention |
| 27 | Deeper-truth staging | Retain conceptual distinctions |
| 28 | Announcements | Trim only redundant signposting |
| 29 | Repeated headings | Keep definitions and scope |
| 30 | Previous-version narration | Keep relevant history; invent no implementation |
| 31 | Punchlines/fragments | Let meaning govern pauses |
| 32 | Aphorisms | Do not invent a concrete claim to explain a vague one |
| 33 | Staged candor | Keep a real change of stance |
| 34 | Unraised objections | Preserve scientific boundaries and real counterarguments |
| 35 | Rejected alternatives | Retain substantive constraints and consequences |

## Validation and candidate use

Run `python3 scripts/validate-package.py` from this folder. It checks package
versions, reference links, legacy IDs, plugin metadata, and the synthetic fixture.
The skill-creator format validator can check skill frontmatter separately. For
distribution, also run `npx skills add . --list` and `claude plugin validate .` in an
environment where those tools are available. These checks do not measure prose
quality, citation fidelity in a generated revision, or personal style matching.

To use this candidate in an isolated evaluation, point the agent to this entire
folder. If an installation is later requested, copy the whole folder, including
references and assets, into the selected agent's skill location. Do not copy only
`SKILL.md`; its references are part of this version. Do not install over an existing
skill merely to evaluate this candidate.

## Version history

- **2.12.1** — Profile-specific correction motivated by an observed synthetic
  profile-use workflow failure and independent adjudication: allow explicitly requested,
  detail-grounded restraint without equally grand synonym substitutions, while
  preserving substantive author interpretation. The ordinary-editing skill body
  is unchanged. A five-case synthetic response-only regression passed for this
  version, versus four cases for the previous version; broader benefit remains
  unverified.
- **2.12.0** — Local candidate only, renamed from `humanizer` to `human-writing`.
  Introduces bilingual paragraph-first editing,
  intent-based audit/rewrite/edit modes, evidence-preserving authorial voice, separate
  optional profiles, and a standalone composition contract. Moves the 35 legacy IDs
  to a reference, repairs examples that added/dropped meaning, and removes blanket
  dash/passive rules. Profiles honor disabled state and explicit single-turn overrides.
  No writing-effect or real-profile validation is claimed.
- **2.11.2** — Supplied upstream baseline. Root skill loading replaced the plugin
  symlink and separate Claude Desktop package. Earlier upstream release history is
  documented in [the upstream repository](https://github.com/blader/humanizer).

## License

[MIT](LICENSE). Upstream attribution and additional source/license observations are
in [Sources and decisions](references/sources-and-decisions.md). This fork does not
represent an upstream release or imply endorsement by the researched projects.
