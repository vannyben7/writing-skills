# Semantic examples: what changes and what survives

All passages below are illustrative, not empirical claims or verified citations. Each revision uses only facts in its own Before passage. Citation strings illustrate preserving attachment; do not reuse them as references. Dispositions depend on the stated context, and unchanged text is a valid result.

## 1. Remove a wrapper, retain the negative boundary — D1, D2

Before:

> We emphasize that these results should not be interpreted as evidence of universal robustness.

After (`TIGHTEN`):

> These results should not be interpreted as evidence of universal robustness.

Preserved: the exact excluded interpretation and its force. No shift count, section reference, test protocol, or new positive robustness claim is available to insert. Replacing “not evidence of” with merely “does not prove” could weaken this boundary.

## 2. Describe the supplied control — D6

Before:

> For a fair comparison, all methods are evaluated using the same encoder.

After (`TIGHTEN`):

> All methods are evaluated using the same encoder.

Preserved: the encoder control during evaluation. This edit removes the framing assertion, not a measured fairness result. It does not change “evaluated using” into a claim about training.

## 3. A modest result without apology — D4

Before:

> We apologize for the small gain: Macro-F1 increases from 71.4 to 72.1 on Dataset A.

After (`TIGHTEN`):

> Macro-F1 increases from 71.4 to 72.1 on Dataset A, a small gain.

Preserved: supplied metric, values, setting, and the author's magnitude assessment. Removed: apology framing, which adds no property of the result. The result does not establish reliability or safety.

## 4. Three independent restrictions remain — D3

Before:

> It should be noted that, in this convenience sample of 18 managers, self-reported autonomy was associated with retention intentions; the cross-sectional design does not establish that autonomy caused those intentions.

After (`TIGHTEN`):

> In this convenience sample of 18 managers, self-reported autonomy was associated with retention intentions; the cross-sectional design does not establish that autonomy caused those intentions.

Preserved: sample selection and size, source/measurement status, and causal limit. All three remain beside the inference. Neither “in this sample” nor “associated” fully substitutes for the other restrictions.

## 5. 中文：研究范围不能替代代表性限制 — D2, D12

改前：

> 需要强调的是，本文考察的是三家沿海制造企业，这三家企业并不代表全国制造业。

改后（`TIGHTEN`）：

> 本文考察三家沿海制造企业；这三家企业并不代表全国制造业。

保留：企业数量、地区、行业和不具全国代表性的判断。只写“本文考察三家企业”会丢失代表性边界，不能作为等义改写。

## 6. 中文：计划、报告与结果不能互换 — D1

改前：

> 为免误解，需要说明的是，2022 年的方案提出增设两个服务站，但现有材料未说明服务站是否建成（市级规划文本，2022，第 8 页）。

改后（`TIGHTEN`）：

> 2022 年的方案提出增设两个服务站，但现有材料未说明服务站是否建成（市级规划文本，2022，第 8 页）。

保留：年份、数量、计划状态、建成状态未知，以及引文支持的位置。不得改为“2022 年增设了两个服务站”。

## 7. A null finding and a rival are findings — D4 false positive

Before:

> We found no detectable association between workload and turnover in this sample. The confidence interval includes effects in both directions, and differences in management practice remain a plausible alternative explanation.

Decision: `KEEP`.

“No detectable association” is not proof of no association. The interval and rival restrict the interpretation; none is an apology to cut. Do not rewrite this as a successful confirmation of the study's hypothesis.

## 8. State the documented omission — D5

Before:

> We did not compare Method X because it requires labeled target-domain data, which our protocol does not provide; calling this an unfair comparison is therefore justified.

After (`TIGHTEN`):

> We did not compare Method X because it requires labeled target-domain data, which our protocol does not provide.

Preserved: the actual omission and its stated reason. A revision mentioning only the data difference could hide the fact that no comparison was run.

## 9. Missing support cannot be invented — D10

Before:

> Our method provides reliable and safe performance.

Decision: `QUERY` — What evidence or definitions support reliability and safety here?

Leave the sentence unchanged pending that information. Do not invent an accuracy gain or latency reduction; neither would establish safety. A request for routine editing does not require stopping work on other clear passages.

## 10. Preserve the uncertainty of an explanation — D4

Before:

> Although we cannot be certain, the lower response rate may reflect survey fatigue; we did not measure fatigue directly.

After (`TIGHTEN`):

> The lower response rate may reflect survey fatigue; we did not measure fatigue directly.

Preserved: the tentative explanation and lack of a direct measure. “The lower response rate reflects survey fatigue” would convert a hypothesis into a diagnosis.

## 11. Procedural detail affects reproducibility — D9 false positive

Before:

> After inspecting the residuals, we excluded observations above the preregistered threshold of 10 and reran the model. Both estimates are reported in Table 3.

Decision: `KEEP`.

The sequence, exclusion rule, threshold, and reporting of both estimates matter to interpreting the analysis. Do not delete them as a work log, reinterpret the threshold, or claim the rerun was itself preregistered.

## 12. 中文：有逻辑作用的学术衔接词应保留 — D11 false positive

原文：

> 企业引入了弹性排班。然而，访谈显示，员工仍需提前两周提出申请，因此制度上的灵活性未必转化为实际自主权。

处置：`KEEP`。

“然而”标明制度安排与访谈发现的反差；“因此”引出作者的解释；“未必”限定推论。“综上”等词也应按具体功能判断，不能仅因常见就删除。

## 13. Course-essay voice and counterexample — D2 false positive

Before:

> I find the participatory account more persuasive in this case, although the director's unilateral budget decision complicates that reading. The case does not justify treating participation as a general explanation of reform.

Decision: `KEEP`.

The passage states an owned, qualified interpretation, a counterexample, and a limit on generalization. Do not replace it with a neutral summary or invent stronger personal conviction. A first-person voice profile could support keeping this stance; it would not authorize adding it to a different author's text.

## 14. 中文：压缩重复的自我说明，保留立场 — D1, D2

改前：

> 为免误解，我在这里想要说明的是，我认为该理论能够解释规则为何被遵守，但不能充分解释员工为何主动提出改变。这也是本文所要表达的观点。

改后（`TIGHTEN`）：

> 我认为，该理论能够解释规则为何被遵守，但不能充分解释员工为何主动提出改变。

保留：第一人称判断、理论解释力的两项具体判断，以及“不能充分”而非“完全不能”的强度。删除的两处框架句不承担额外论证功能。

## 15. Local boundary versus relocation — D12

Supplied context: the Methods section already describes the same ten consenting schools and their recruitment; the abstract reads:

> The analysis covers ten consenting schools. It does not establish effects in schools that declined participation. The schools were recruited through the district network described in Methods.

Possible revision (`RELOCATE`/remove duplicate detail):

> The analysis covers ten consenting schools. It does not establish effects in schools that declined participation.

Destination: the supplied Methods recruitment description already contains the final sentence's information; retain it there. The selection boundary remains in the abstract. Without that destination or context, recommend a location rather than pretending a move has been completed.

## 16. Chinese classroom synthesis adds content — D11 false positive

原文：

> 综上，两个案例对正式规则的依赖程度不同。因此，本文更倾向于将规则视为协作的一项条件，而非协作的充分保证。

处置：`KEEP`。

保留：案例比较的综合、作者的解释倾向，以及“条件”与“充分保证”的逻辑区分。此处的总结句推进论点，不是可以机械删除的收尾句。

## 17. An exact guarantee should stay exact — D13 false positive

Before:

> Under assumptions A1–A3, Theorem 2 guarantees convergence to the unique minimizer.

Decision: `KEEP` when the supplied theorem states that result.

Do not change “guarantees” to “may support” merely to reduce apparent confidence. Preserve the assumptions and cross-reference; if the theorem was not supplied and a substantive check is needed, flag that limit instead of pretending to verify it.
