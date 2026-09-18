# Writing Skills

让文字更清楚，也让作者原本的意思留下来。

本仓库提供两个中英文写作技能：`human-writing` 处理段落推进、句子表达和作者声音；`academic-clarity` 处理学术文字中的重复辩解，同时保护必要的证据边界。它们是交给 AI 助手阅读的编辑说明，不是新模型、独立写作软件或 AI 检测器。

[中文使用指南](docs/USER_GUIDE.zh-CN.md) · [English user guide](docs/USER_GUIDE.en.md) · [评估结果](EVALUATION.md) · [维护与更新](docs/MAINTENANCE.md)

**当前为功能实验版，尚未证明整体文风优于旧版技能或直接提示。** 当前独立衍生版本：Human Writing **2.12.1**、Academic Clarity **1.1.1**。不保证检测器分数、论文录用、个人风格相似度，也不会自动替换你已安装的技能。

## 我应该选哪个？

| 你现在遇到的问题 | 先用哪个 | 它不应做什么 |
| --- | --- | --- |
| 文章读起来像几个互不相干的要点；句子重复；自己的重点不明显 | `human-writing` | 为了“有人味”编造观点、情绪、经历或事实 |
| 论文或课程 essay 不断解释“并非声称……”，有些限定反复出现 | `academic-clarity` | 为了更有底气而删除样本、因果、来源或适用范围限制 |
| 个人文章、随笔，希望保留自己的口吻 | 通常只用 `human-writing` | 把随笔强行改成学术论文 |
| 只想知道问题在哪里，还不想改 | 选对应技能，明确说“只审计，不改写” | 擅自改正文或文件 |
| 学术内容既有重复辩解，又有行文问题 | 明确要求两个技能各做一遍 | 自动循环修改，或让第二遍丢掉第一遍保护的信息 |

两个技能都能单独使用。无需先提供样文、创建风格档案或安装另一个技能。好文字可以保持不变。

## 三分钟开始

“三分钟”是简短上手路线，不是下载或生成耗时保证。你需要已有一个能使用技能或读取本地文件的 AI 客户端，以及可用的模型访问权限。

### 1. 安装一个或两个技能

在支持 `skill-installer` 的 Codex 中，发送以下自然语言请求；这是发给助手的消息，不是终端命令：

```text
请用 skill-installer 从 GitHub 仓库 vannyben7/writing-skills 安装：
- skills/human-writing
- skills/academic-clarity
先检查同名技能。已存在时不要覆盖，报告现有版本、目标路径和可选处理方式。
安装完成后告诉我实际路径和版本。
```

只需要一个时，删掉另一行。Codex CLI / IDE 支持时也可用 `$skill-installer` 选择安装技能。当前官方文档说明安装器可读取其他仓库、Codex 会自动发现新技能；未出现时可重启客户端。安装目录和交互方式随客户端而异。依据：[OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)（核对于 2026-09-18）。

不用安装器？可将下载仓库中的完整技能文件夹复制到写作项目的 `.agents/skills/`，先确认没有同名目录。必须保留 `references/` 等配套文件，不能只复制 `SKILL.md`。详细步骤和不覆盖已有目录的示例见[中文安装说明](docs/USER_GUIDE.zh-CN.md#install)或[English setup](docs/USER_GUIDE.en.md#install)。本项目不要求安装付费工具或额外服务。

### 2. 先试一小段

在聊天中选择技能或直接写出名称，再贴上你自己的文字：

```text
用 human-writing 改写下面这段课程 essay。
保留论点、数字、引用和我原来的立场；只返回改写后的文字，不修改文件。

[在这里粘贴原文]
```

Codex CLI / IDE 中可以写成 `$human-writing`。其他客户端使用其技能选择器；没有技能发现功能但能读文件时，可以让它先读完整技能目录中的 `SKILL.md` 及相关参考。不能读取这些文件的普通聊天窗口，不会仅凭技能名称获得本仓库的规则。

### 3. 对照原文再决定采用

检查数字、否定、因果关系、结论强度、引用支持的内容和自己的立场有没有变化。不要只看“更顺”或“更短”。有问题就指出具体丢失的信息，让助手恢复；也可以保留原文。

## 一个小例子

以下为专门编写的合成示例，不是实测输出或效果证明。假设两处引导语只起重复铺垫作用：

**原文**

> 需要强调的是，本研究仅纳入两所城市学校的48名学生，因此结果不能代表其他学校。值得注意的是，参与次数与结课成绩存在相关关系，但这一相关关系并不证明因果关系。

**一种 Academic Clarity 改法**

> 本研究仅纳入两所城市学校的48名学生，因此结果不能代表其他学校。参与次数与结课成绩相关，但这不证明因果关系。

删的是重复铺垫，不是“两所城市学校”“48名”“不能代表其他学校”或“不证明因果”。不是所有“值得注意的是”都应删除。更多段落、英文和保留原文的例子见两份使用指南。

## 三种常用请求

```text
用 academic-clarity 只审计这段论文，说明哪些限定应保留。不要改写或修改文件。

用 human-writing 改写这段个人文章，只在回复中给出文本，不增加经历或感受。

用 human-writing 读取 draft.md，把修订稿另存为 draft.revised.md；
若目标文件已存在先停下，不覆盖原稿。保留引用、代码和 YAML。
```

文件读写、Word/PDF 支持和修订痕迹由客户端能力决定；这些技能本身不提供文档转换器。请明确授权修改哪个文件，仅给出路径不等于要求覆盖它。

## 可选：风格档案与组合使用

风格档案是共享技能目录之外的可编辑 Markdown 或 JSON 文件，用来记录从授权样文中观察到的表达偏好。它不是训练好的个人模型。少量样文只能支持暂定观察；自己的作品、欣赏的第三方风格、合成示例必须分开。

- 默认只保留证据概述和样本定位；保存原文片段需要许可。
- `enabled: false` 表示停用；仅提到名称不会启用。明确要求临时使用只影响本次。
- “这次不用档案”表示本次不读取、不应用，也不改保存状态。
- 查看、纠正、切换、停用、删除和设为默认，都应明确说明具体档案和动作。
- 公开的 [TEST-profile.json](skills/human-writing/assets/TEST-profile.json) 是默认停用的合成示例，不是你的个人档案。

详见[中文档案说明](docs/USER_GUIDE.zh-CN.md#profiles)、[English profiles](docs/USER_GUIDE.en.md#profiles)和[完整档案规则](skills/human-writing/references/style-profiles.md)。本地保存不等于本地推理：模型服务仍可能处理发送给它的文字。

只有明确要求组合时，采用一次有边界的流程：

`原文 → academic-clarity → human-writing → 与原文做语义核对`

保留原文和未解决问题，不必另建交接文件，也不自动反复调用。个人文章通常只用 Human Writing。见[组合指南](docs/USER_GUIDE.zh-CN.md#combine)。

## 我们测试了什么？

[评估记录](EVALUATION.md)是数字与限制的完整来源，不同阶段不能合并成一个“成功率”。

| 检查 | 已公开结果 | 不能据此得出 |
| --- | --- | --- |
| 一般改写开发集 | 8份来源文本、15个文本与路径组合、45份输出、60条裁判观察；以平局为主，部分胜出有判定争议 | 整体优于旧版、直接提示或所有模型 |
| 修复前合成工作流 | 11/12通过；剩余问题是克制文风没有充分落实 | 已验证真实磁盘上的档案状态 |
| 档案专属定向回归 | 2.12.1为5/5；2.12.0对照为4/5 | 广泛盲测优势、个人风格匹配或检测器效果 |
| 历史写作评估工具链（见评估记录） | 36项离线检查通过 | 多了36个写作案例，或这是当前仓库测试总数 |

一般改写阶段使用 Human Writing 2.12.0 与 Academic Clarity 1.1.1；Human Writing 2.12.1 只改了档案参考中的行为规则，普通编辑入口正文未变。尚无保留集泛化结果、真实私人档案验证或用户偏好认可。

## 费用、更新与许可证

技能内容按 MIT 许可证提供，不自带模型或付费订阅。模型调用仍受你所用客户端、账号和服务商的计费、限额、网络与隐私规则约束；组合处理通常需要更多上下文或调用。普通使用不要求 Python 或 Node.js。

从仓库更新文件，不会自动更新一份已经复制安装的技能。升级前记录来源版本并备份整个旧目录；私人档案单独保存。如何避免同名冲突、迁移与回退，见[维护说明](docs/MAINTENANCE.md)及[使用指南](docs/USER_GUIDE.zh-CN.md#versions)。

维护者可在仓库根运行以下离线结构检查（Python 3.10+、Node.js 18+）：

```bash
python3 scripts/check_release.py
```

它检查公开文件清单、版本、链接和包结构，也运行使用模拟数据的维护工具单元测试；不调用模型，也不证明写作质量。新增的维护工具测试与评估记录中的历史36项分开计算，更不是新增写作案例。新增公开文件需同步 [RELEASE_FILES.txt](RELEASE_FILES.txt)。普通用户不必运行它才能编辑文章。

根集成文档和检查代码使用 [MIT](LICENSE)。两包保留各自的上游许可证、版权与来源记录；不是上游官方新版本，也不暗示上游认可。见[第三方声明](THIRD_PARTY_NOTICES.md)、[Human Writing 来源](skills/human-writing/references/sources-and-decisions.md)和[Academic Clarity 来源](skills/academic-clarity/references/sources-and-design.md)。

## English at a glance

These are two portable instruction packages for an AI assistant, not a model or detector. Use **Human Writing** for prose structure and authorial voice; use **Academic Clarity** for defensive academic framing without losing evidence limits. Both work without samples or profiles.

Start with the [English user guide](docs/USER_GUIDE.en.md), including safe installation, copyable requests, examples, privacy controls and rollback. This is a functional experimental release: overall writing superiority has not been demonstrated. Read the [evaluation record](EVALUATION.md) for the small-sample results and disputed judgments.
