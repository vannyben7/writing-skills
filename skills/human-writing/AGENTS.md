# Guide for agents

This file explains how to change Human Writing without breaking its package or prompt.

## What this repo contains

Human Writing is an independent local derivative of Humanizer, written in Markdown. Its skill name and package IDs are `human-writing`. `SKILL.md` is the prompt that agents read. The repo has no build step.

Keep the skill portable. Do not write instructions that limit it to one or two agent tools.

## Key files

- `SKILL.md` is the only skill entrypoint. It contains portable YAML metadata, mode routing, preservation rules, and the editing workflow.
- `references/patterns.md` holds 35 legacy pattern IDs as advisory diagnostics. Other references cover language/genre, optional profiles, composition, and research decisions.
- `README.md` explains local candidate status, use, the pattern index, and version history.
- `assets/TEST-profile.json` is a synthetic fixture, not a user profile or an automatic default.
- `.claude-plugin/plugin.json` describes the Claude plugin and points its skill loader at the root `SKILL.md`.
- `.claude-plugin/marketplace.json` is a local-only marketplace for this package directory. The intended public repository `vannyben7/writing-skills` places this package at `skills/human-writing`; its root owns publication and repository-wide marketplace configuration.
- `scripts/validate-package.py` checks package files and shared values.

## Rules for changes

Keep `SKILL.md` and `README.md` in sync.

- **Patterns:** The reference has 35 numbered legacy patterns. If you add, remove, or renumber one, update the README table, validator, and every pattern reference. Never make a pattern override semantic preservation.
- **Version:** Keep the same version in `SKILL.md` under `metadata.version`, the first README version entry, and `.claude-plugin/plugin.json`. Do not add a top-level `version` field to the skill.
- **Compatibility:** Keep install and use instructions neutral across agents. Names such as Claude Code, OpenCode, and Codex are examples, not limits.
- **History:** Add a short README version note for any behavior change or non-obvious fix.
- **Checks:** Run `python3 scripts/validate-package.py`. Run the skill-creator format validator when available. Before publishing, also run `npx skills add . --list` and `claude plugin validate .` when those tools are available; report unavailable checks honestly. Package validation does not establish writing quality.
- **Local derivative:** Version 2.12.1 is this candidate's version, not an upstream release. Preserve upstream attribution, historical names/source URLs, and the original LICENSE. Current identifiers are `human-writing`; do not present upstream install commands as this package's identity. Record influences and license status in `references/sources-and-decisions.md`.
- **Profiles:** Keep actual profiles and samples outside the shared package. Default to evidence paraphrases plus sample locators; retain exact snippets only with permission. Honor `enabled: false`; only an explicit temporary override or reenabling can activate it. Ignore-this-time means no load or saved mutation. Do not infer a real user profile from the synthetic TEST fixture or silently collect private samples.
- **Composition:** Keep the optional handoff fields and preservation contract consistent with academic-clarity, without requiring that skill to be installed or invoked.
- **Examples:** Every before/after pair must preserve numbers, relations, qualifiers, negation, attribution, and citation role. Do not fix style by inventing facts or opinions.

## Writing style

Use Plain Language in code comments, prompts, documentation, descriptions, validation messages, and progress reports.

- Lead with the main point.
- Use common words and active voice.
- Keep sentences and paragraphs short.
- Use one term for the same item.
- Use `must` for requirements.
- Use headings, lists, and tables when they help the reader.
- Remove repeated or unnecessary words.
- Limit acronyms and explain technical terms.
- Avoid double negatives.
- Keep exact identifiers, commands, paths, schema fields, quotations, watched phrases, and behavior-bearing examples.
- Keep the full technical meaning.

## Editing the skill

- Keep the YAML metadata valid.
- Treat the prompt below the metadata as the product.
- Prefer a short, clear instruction over another exception or repeated explanation.
