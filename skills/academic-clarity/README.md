# Academic Clarity

[简体中文](README.zh-CN.md)

Version **1.1.1 — functional experimental edition**. Academic Clarity is the renamed independent derivative of Academic Defensive Writing Auditor 1.0.0. This GitHub-only distribution is maintained in [vannyben7/writing-skills](https://github.com/vannyben7/writing-skills), under `skills/academic-clarity`. Overall style superiority has not been demonstrated. It does not replace an installed skill until explicitly copied or installed. `package.json` remains private, and the inherited npm publication workflow has been removed.

Audit or revise defensive framing in English and Chinese academic papers and course essays: unnecessary disclaimers, repeated caveats, prebuttals, and result excuses. Preserve evidence boundaries, argument, uncertainty, and author's voice. D1–D14 remain available, with contextual `KEEP`, `TIGHTEN`, `REFRAME`, `RELOCATE`, `CUT`, and `QUERY` decisions. This is not a general writing or fact-checking service; personal articles normally use `human-writing` alone.

## Use

Give an LLM the [SKILL.md](SKILL.md) and the text to review:

> Use $academic-clarity to audit this passage for defensive wording only. Do not rewrite it. Explain which qualifications should stay.

Or authorize editing:

> Use $academic-clarity to revise this essay's defensive wording. Preserve my argument, English academic register, citations, and all distinct evidence limits. Return the revised passage first.

Ordinary use needs no profile or private samples. An explicitly selected portable profile shared with `human-writing` can guide either mode. `enabled: false` stays disabled unless the user explicitly requests temporary use or reenabling; naming alone does not activate it. “Ignore this time” means no profile load and no saved mutation. Store evidence paraphrases plus sample locators by default, not private verbatim excerpts without permission.

When both skills are requested, use original → `academic-clarity` → `human-writing` → semantic comparison with the original. The shared handoff is optional; neither skill automatically invokes the other. See [voice and composition](references/voice-and-composition.md).

## What changed in this candidate

- Version 1.1.1 adds a local-flow check after wrapper removal: preserving propositions need not preserve disconnected sentence divisions. This responds to preliminary reading feedback and remains a hypothesis to test.
- No quota for caveats: sample, causal, source, and other independent restrictions all survive.
- Local qualifications remain beside the inference where needed, including abstracts and captions.
- Audit-only requests leave the manuscript unchanged; ordinary rewrite requests do not require an additional approval ceremony.
- Negative findings, rivals, counterexamples, procedural detail, evidence status, citation roles, and author stance are protected.
- Chinese academic transitions and cautious English language are judged by function, not a ban list.
- Brief requests receive brief outputs; any requested score is explicitly an editorial heuristic, never an AI probability.
- Examples no longer insert missing measurements, experiment settings, or section references.

These are design changes, not a claim that the candidate has passed independent behavioral evaluation. Validation results should be reported separately.

## Package and installer

The JavaScript CLI **copies skill instructions**. It does not audit a manuscript or call a model. Node.js 18 or later is required only for this optional installer, not for reading the skill.

From this candidate's directory:

```bash
node bin/cli.js --help
node bin/cli.js --version
node bin/cli.js --dir /path/to/test-skills
```

`--dir` selects the parent directory; default is `./skills`. The installed folder is named `academic-clarity`. `--force` replaces that named skill folder at the destination, so use it only for an intended replacement. The CLI refuses to replace its own source directory. Prefer a separate test destination during evaluation. No npm installation or publication is part of this workflow.

The installer includes `SKILL.md`, both READMEs, license notices, `prompts/`, `examples/`, `references/`, and `agents/`. A local `npm pack --dry-run` only inspects file inclusion; it does not publish. Reading the Markdown instructions requires no installation.

## Resources

- [Taxonomy](references/taxonomy.md): D1–D14 and false-positive checks.
- [Before/after examples](examples/before-after.md): English and Chinese mappings, including deliberate non-edits.
- [Audit-only prompt](prompts/audit-only.md) and [cleanup prompt](prompts/full-paper-cleanup.md).
- [Sources and design decisions](references/sources-and-design.md): adopted ideas and rejected rules.
- [License](LICENSE) and [third-party notices](THIRD_PARTY_NOTICES.md).
