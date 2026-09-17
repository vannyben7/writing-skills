# Sources and implementation decisions

Reviewed on 2026-09-17 for this local candidate. These are primary repository
sources, not independent evidence of writing improvement. Branch URLs can change;
commit hashes could not be resolved in this environment. The supplied local baseline
reports 2.11.2. The inspected `blader/humanizer` main branch reports 3.0.0, so the
candidate's **2.12.1 is explicitly a local version, not an upstream release**.
The user renamed this independent derivative to `human-writing`; historical project
names and source URLs retain their original spelling for attribution.

## blader/humanizer

Sources: [repository](https://github.com/blader/humanizer),
[main skill](https://github.com/blader/humanizer/blob/main/SKILL.md),
[license](https://github.com/blader/humanizer/blob/main/LICENSE).

Retained the supplied package's MIT license, original attribution, and 35 legacy
IDs. The local skill name is now `human-writing`. Kept attention to formulaic
framing and preservation of real voice.
Moved the catalog to a reference rather than adopting main's new numbering.

Rejected automatic rewriting based on individual constructions, blanket dash
removal, permission to add reactions, and the default draft/critique/final triplet.
Replaced examples that lost qualifiers or invented facts, including exact 3,000
square feet, culinary details, travel memories, and implementation details.
Unverified sources now prompt a separate issue instead of silent deletion.

License: supplied MIT LICENSE, Copyright (c) 2025 Siqi Chen, retained unchanged at
the package root. This package remains a derivative of that supplied baseline.

## msimchowitz/writing-skills

Sources: [academic-voice](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/academic-voice/SKILL.md),
[writing-cadence](https://github.com/msimchowitz/writing-skills/blob/main/for-agents/writing-cadence/SKILL.md),
[license](https://github.com/msimchowitz/writing-skills/blob/main/LICENSE).

Adapted the ideas that academic prose can express deliberate intellectual priorities,
that evidence and interpretation need separation, and that rhythm should follow
relationships and emphasis. The local workflow implements those ideas at paragraph,
sentence, then word scale, with Chinese and genre guidance.

Did not introduce a dependency on that repository's sibling skills, mandatory voice
uniformity, or numeric sentence-length targets. Neutral technical passages remain
eligible for no change. Adaptation is instructional; no executable code was imported.

License verified: MIT, Copyright (c) 2026 Max Simchowitz. For adapted instructional
ideas, retain this attribution together with the MIT permission and disclaimer in
[the license notice](third-party-notices.md).

## Aboudjem/humanizer-skill

Sources: [skill](https://github.com/Aboudjem/humanizer-skill/blob/main/skills/humanizer/SKILL.md),
[README](https://github.com/Aboudjem/humanizer-skill/blob/main/README.md),
[license](https://github.com/Aboudjem/humanizer-skill/blob/main/LICENSE).

Adopted the conceptual separation of audit, rewrite, and file editing, the need to
protect good prose, and checking concrete invariants. Mode routing here follows
natural-language intent, with no copied CLI or scoring implementation.

Rejected its numeric AI-tell score, lexical “evidence-grade” claims, burstiness and
perplexity targets, em-dash ban, forced strong positions, sensory-detail injection,
and automatic private context loading. The local skill does not equate low variance
or formal/non-native writing with machine authorship.

License verified: MIT, Copyright (c) 2026 Adam Boudjemaa. No source code or catalog
text was copied from this project; the above are independently expressed design
decisions, not an imported implementation.

## ymeiri/voice-layer

Sources: [repository](https://github.com/ymeiri/voice-layer),
[README](https://github.com/ymeiri/voice-layer/blob/main/README.md),
[profile specification](https://github.com/ymeiri/voice-layer/blob/main/VOICE_PROFILE_SPEC.md),
[license location](https://github.com/ymeiri/voice-layer/blob/main/LICENSE).

Adopted the concepts of an inspectable profile separate from shared instructions,
evidence and confidence records, user control, and distinguishing self-writing from
style references. Created an independent small format with common, language, genre,
and language×genre observations and an explicitly synthetic TEST fixture.

Did not import its schema, implementation, private-source discovery, installation
paths, channel inventory, or blanket approval gates. Existing authorization to read
supplied samples is sufficient. Profiles describe writing, not inferred psychology;
the source sample's private facts do not become article content.

License status: the repository page identifies MIT and lists LICENSE, but retrieval
of the raw license and notice failed. No text, schema, or code from that project is
redistributed here. Its exact copyright notice was not verified; do not invent one.

## Earlier source context

The supplied baseline credits [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
and [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup).
That provenance is retained. No new Wikipedia text was copied. This candidate does
not treat an encyclopedia cleanup guide as an authorship test or a universal account
of Chinese, academic, or personal writing.

## What validation can show

Package checks can show coherent metadata, reachable local references, stable legacy
IDs, and a labeled TEST fixture. They cannot show that the new instructions improve
real writing, preserve every claim in all generated edits, or match this user's
voice. Those claims require separate behavioral evaluation and actual sample-based
calibration; neither is asserted by this implementation record.
