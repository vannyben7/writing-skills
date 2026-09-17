# Writing Skills

面向中英文写作的两个独立技能：`human-writing` 处理行文、论证展开与作者声音，`academic-clarity` 处理学术文字中的冗余辩解和证据边界。

**功能实验版：尚未证明整体文风优于旧版或直接提示。** 本项目通过 [vannyben7/writing-skills](https://github.com/vannyben7/writing-skills) 分发：`human-writing` 为独立衍生版本 2.12.1，`academic-clarity` 为独立衍生版本 1.1.1，均不冒充上游版本，也不自动替换已安装技能。

一般改写试验以平局为主，少量胜出包含有争议的忠实度判定。档案专属修复的 5 案例定向回归中，新版本 5/5 通过，对照 4/5 通过；这不能外推为通用写作优势、个人风格匹配效果或检测器表现。具体数据与限制见 [EVALUATION.md](EVALUATION.md)。本实验版开放功能试用，不以继续调优到某个胜率门槛为发布前提。

## 选择技能

| 技能 | 适用任务 | 边界 |
|---|---|---|
| [Human Writing](skills/human-writing/README.md) | 中英文学术论文、课程 essay、个人文章的审计或改写；先处理段落，再处理句子和词语 | 保留原有论点、事实、引文作用、语气和有用的表达，不推断 AI 作者身份 |
| [Academic Clarity](skills/academic-clarity/README.zh-CN.md) | 学术论文与课程 essay 中的免责声明、重复限定、预先辩解和结果开脱 | 保留独立的样本、因果、来源等限制；不是通用写作或事实核查服务 |

个人文章通常只用 `human-writing`。两个技能都能独立使用；普通使用不需要样文、声音档案、网络服务或另一个技能。

```text
用 $human-writing 改写这段课程 essay，保留论点、引文、事实和我的语气。
用 $academic-clarity 只审计这段论文中的防御性表达，说明哪些限定必须保留，暂不改写。
```

明确要求组合使用时，按一次有边界的流程处理：

```text
原文 → academic-clarity → human-writing → 与原文做语义核对
```

最后比较确定程度、因果关系、否定、适用范围、证据状态、数值、引文作用和作者立场。交接可以是一条简短说明，不要求额外文件，也不会自动循环调用。详见 [Human Writing 交接契约](skills/human-writing/references/composition-contract.md)与 [Academic Clarity 组合说明](skills/academic-clarity/references/voice-and-composition.md)。

## 可选声音档案

两个技能接受同一套可编辑 Markdown 或 JSON 档案；只在用户明确选择后使用。档案与私人样文应保存在共享技能目录之外，普通改写不要求收集或保存这些资料。

证据默认保存概述和样本定位；保留私人原文片段需要许可。区分自己的作品、欣赏的第三方风格和合成示例，并分别记录语言、文体和置信程度。中文样文不能直接确立英文句法偏好，也不能据此编造作者经历或观点。

`enabled: false` 保持停用；单纯提及名称不算启用。明确要求临时使用只影响本次，不修改保存状态。“这次不用档案”意味着不加载、不应用、不查询选择器，也不修改保存内容。公开包中的 [TEST-profile.json](skills/human-writing/assets/TEST-profile.json) 是明确标记且默认停用的合成测试样例，不是真实用户档案。详情见[声音档案规则](skills/human-writing/references/style-profiles.md)。

本包没有样文上传服务；所用模型或客户端仍可能处理你提供的文本，不能因为档案保存在本地就推断所有文字只在设备内处理。

## 本地使用与安装

不安装也可以把某个完整技能目录交给支持读取文件的客户端，并要求它从 `SKILL.md` 开始。保留 `references/`、`assets/` 和其他配套文件；只复制入口文件会丢失规则。

Codex 可从项目内的 `.agents/skills` 发现技能。下面以已下载的本仓库为来源，在你的写作项目中执行；将示例来源路径替换为实际位置，按需只安装其中一个。已有同名目录时，相应命令停止复制，应先自行比较版本。安装说明依据 [OpenAI 官方 Build skills 文档](https://learn.chatgpt.com/docs/build-skills)。

```bash
writing_skills_source="/path/to/writing-skills"
mkdir -p .agents/skills
test ! -e .agents/skills/human-writing && cp -R "$writing_skills_source/skills/human-writing" .agents/skills/
test ! -e .agents/skills/academic-clarity && cp -R "$writing_skills_source/skills/academic-clarity" .agents/skills/
```

其他技能客户端：把选定的完整目录复制到该客户端配置的技能目录，并使用其发现或调用机制；支持直接读取 `SKILL.md` 的客户端也可直接使用。不要假设不同客户端共用相同安装路径。仓库根未提供 Claude marketplace；`skills/human-writing/.claude-plugin/marketplace.json` 仅供该子包目录的本地使用。

Academic Clarity 的可选 Node 安装器只复制指令文件，不调用模型。它保持 `private: true`，本项目不采用 npm 发布流程。

## 本地结构检查

要求 Python 3.10+ 和 Node.js 18+。在仓库根运行：

```bash
python3 scripts/check_release.py
```

检查公开文件白名单、技能名称和版本、相对链接、客户端元数据、合成 TEST 样例、禁止发布的私人目录或文件、个人绝对路径和常见凭据模式。它还会在 `skills/human-writing` 中运行已有包验证器，并检查 Academic Clarity 的 CLI。所有检查均为确定性的本地检查，不调用模型、不安装依赖、不发布 npm 包。

根目录 CI 运行同一命令。子包内保留的 workflow 不会作为仓库根工作流自动执行。预期发布文件见 [RELEASE_FILES.txt](RELEASE_FILES.txt)；白名单是审核边界，新增公开文件时需要同步维护。此检查不能替代人工核对未知形式的敏感信息。

## English quick use

Use `$human-writing` to audit or revise prose while preserving the author's meaning and voice. Use `$academic-clarity` for defensive academic framing and evidence boundaries. Both work without writing samples or a profile.

For an explicitly requested combined pass: original → Academic Clarity → Human Writing → compare with the original. Copy a complete skill directory into your client's configured skill location, or have the client read its `SKILL.md` directly. This is a functional experimental distribution; overall style superiority has not been demonstrated. See [evaluation scope and results](EVALUATION.md), including disputed judgments and the limited targeted regression.

## 许可证与来源

根目录集成文档和检查代码使用 [MIT 许可证](LICENSE)。两个技能保留各自未改写的上游许可证、版权声明和来源记录；根许可证不重新归属上游内容。见[第三方归属说明](THIRD_PARTY_NOTICES.md)。
