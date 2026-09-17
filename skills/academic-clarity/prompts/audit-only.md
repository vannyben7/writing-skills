# Audit-only prompt / 只审计

Use `$academic-clarity` and `SKILL.md` to audit the supplied English or Chinese academic paper or course essay for defensive wording. Do not revise the text or provide replacement prose unless I request it.

Use D1–D14 as contextual cues, then choose `KEEP`, `TIGHTEN`, `REFRAME`, `RELOCATE`, `CUT`, or `QUERY`. Explain the actual reading problem and the information that must survive; do not speculate about reviewer reactions. Keep independent sample, causal, source, and other limits; preserve negative findings, rivals, counterexamples, citations, numbers, and author stance.

For a short passage, return a concise diagnosis. For a full paper, return a prioritized audit table plus important retained cautions and unresolved queries. Do not assign a score unless requested. Any requested score is an editorial heuristic, not an AI-authorship probability or publication forecast.

Optional context: assignment/journal requirements, section purpose, terminology constraints, or an explicitly selected voice profile. No profile or private samples are required. A disabled profile stays disabled unless I explicitly request temporary use or reenabling; “ignore this time” means no load and no saved change. Profile evidence defaults to a paraphrase plus sample locator, not retained private quotations.

中文调用：

> 请使用 $academic-clarity，依据 SKILL.md，只审计这段中文学术文字中的防御性表达，暂不改写。区分冗余辩解与必要的证据边界，保留作者立场、反例、引文和数值；说明具体阅读问题及建议处置。不要因“然而”“综上”“在一定程度上”等词出现就判定有问题。短文简要反馈，全文再给分级审计表。
