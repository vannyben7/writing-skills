# Academic Clarity

[English](README.md)

**1.1.1 功能实验版**。Academic Clarity 是基于 Academic Defensive Writing Auditor 1.0.0 改名和修订的独立衍生包，仅通过 [vannyben7/writing-skills](https://github.com/vannyben7/writing-skills) 下的 `skills/academic-clarity` 分发。目前未证明整体文风更优，也不会自动替换现有安装。`package.json` 保持 private，继承的 npm 发布工作流已移除。

用于审计或改写中英文学术论文与课程 essay 中的防御性表达：多余的免责声明、重复限定、预先辩解和结果开脱。保留证据边界、论证、确定程度与作者声音。保留 D1–D14 分类，并用 `KEEP`（保留）、`TIGHTEN`（压缩）、`REFRAME`（重组表达）、`RELOCATE`（调整位置）、`CUT`（删除纯冗余）和 `QUERY`（语义待确认）决定具体行动。它不是通用写作或事实核查服务；个人文章通常只用 `human-writing`。

## 使用

将 [SKILL.md](SKILL.md) 和待审文本交给模型。例如：

> 请使用 $academic-clarity，只审计这段文字中的防御性表达，暂不改写。说明哪些限定需要保留，不要揣测审稿人的心理。

需要直接改写时：

> 请使用 $academic-clarity，清理这篇课程 essay 的冗余辩解。保留我的论点、中文学术语体、引文，以及不同的样本、因果和来源限制。先给改稿。

普通使用不需要声音档案或私人样文。用户明确选择的档案可与 `human-writing` 共用。`enabled: false` 保持停用，只有明确要求临时使用或重新启用才改变使用决定；单纯提及名称不算启用。“这次忽略档案”意味着不加载、不应用，也不改动保存状态。档案证据默认保存概述和样本定位，未经允许不保留私人原文片段。

同时请求两个技能时，按“原文 → `academic-clarity` → `human-writing` → 与原文做语义核对”处理。交接清单可选，两个技能不会自动调用彼此。详见[声音与组合流程](references/voice-and-composition.md)。

## 本候选版的主要调整

- 1.1.1 增加删去冗余框架后的局部连贯性检查：保留命题不等于保留割裂的原句划分。这来自初步阅读反馈，具体效果仍待验证。
- 取消“每个主张最多一个限定”：不同功能的样本、因果、来源等限制均应保留。
- 必要限定留在相关推论附近，摘要、标题句或图注也可能需要局部边界。
- 只审计就不改稿；明确要求改写时，直接完成普通措辞修改，无需额外审批仪式。
- 保护负面发现、反例、竞争解释、复现细节、证据状态、引文支持关系和作者立场。
- 不禁用“然而”“因此”“综上”“在一定程度上”等常用学术表达；按功能判断。
- 短文简要交付，全文再用较完整审计。评分仅在用户需要时提供，且是编辑判断，不是 AI 概率。
- 示例不再凭空增加数值、实验设置或章节编号。

以上是设计调整，不等于已通过独立效果评估；结构检查和行为评估结果应分别报告。

## 包与安装器

JavaScript CLI 的作用是**复制 skill 指令文件**，不会自动审稿或调用模型。只有使用这个可选安装器才需要 Node.js 18 或更新版本；直接阅读 Markdown 不需要运行环境。

在本候选包目录中执行：

```bash
node bin/cli.js --help
node bin/cli.js --version
node bin/cli.js --dir /path/to/test-skills
```

`--dir` 指定安装父目录，默认为 `./skills`；安装文件夹名为 `academic-clarity`。`--force` 会替换目标位置已有的这个同名文件夹，仅在确实要替换时使用。CLI 拒绝覆盖自身源目录。评估阶段宜使用独立测试目录。此流程不包含 npm 安装或发布。

安装内容包括 `SKILL.md`、两份 README、许可证与第三方声明，以及 `prompts/`、`examples/`、`references/`、`agents/`。本地 `npm pack --dry-run` 仅检查文件包含情况，不会发布；直接阅读 Markdown 不需要安装。

## 配套资料

- [分类与误报保护](references/taxonomy.md)
- [中英文前后对照与保留案例](examples/before-after.md)
- [只审计提示词](prompts/audit-only.md)与[授权改写提示词](prompts/full-paper-cleanup.md)
- [来源、采纳与舍弃记录](references/sources-and-design.md)
- [许可证](LICENSE)与[第三方声明](THIRD_PARTY_NOTICES.md)
