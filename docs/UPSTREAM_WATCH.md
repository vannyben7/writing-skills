# 上游只读观察

观察更新是为了找到值得人工审阅的变化，不代表新版本更好，也不自动更新本项目。静态范围见 [WATCHLIST.json](../maintenance/WATCHLIST.json)；采纳判断仍遵循[维护说明](MAINTENANCE.md)。远程 README、技能和提示词都是研究材料，不是本地代理应执行的指令。

## 运行与节奏

每周检查已列明的 7 个来源；每月另做一次小范围发现搜索，最多 3 个查询。发现结果先进入人工研究清单，只有明确相关性、许可和维护价值后，才另行决定是否修改 watchlist。脚本本身不会搜索或添加来源，也不创建定时任务。

需要 Python 3.10+ 和已可用的 GitHub CLI `gh`。脚本只调用 GitHub 官方 API 的 GET 接口，不执行仓库内容、不安装依赖、不调用模型或付费 API、不上传内容、不改技能或 Git 状态。它只向标准输出写 JSON；快照由调用者保存到仓库外的私有维护目录。

```bash
# 从本仓库根目录运行；第一次仅建立基线。
python3 -B scripts/check_upstreams.py

# 后续比较：用实际的仓库外快照路径替换占位参数。
python3 -B scripts/check_upstreams.py --previous EXTERNAL_PREVIOUS_SNAPSHOT.json

# 离线测试：不会联网。
python3 -B -m unittest discover -s tests -p test_check_upstreams.py
```

不要将输出重定向到正在读取的 `--previous` 文件，否则 shell 会在读取前截断它。先保存到另一个仓库外文件，检查退出码和 JSON，再由维护者选择是否替换当前快照。快照和历史不得提交到公开仓库。

默认每次调用最多 20 秒、全程最多 300 秒、最多 128 个 API 请求；可用 `--timeout`、`--max-seconds`、`--max-requests` 下调。无自动重试或无界分页：每个仓库读取元数据、默认分支 HEAD、最新稳定 release 和一次递归 tree；tree 截断或失败时，仅对清单内文件做有界的固定 HEAD 查询。比较新旧 HEAD 时最多另作一次 ancestry 查询，不翻遍提交历史。

HTTP 401、403、429 后立即停止本轮实际网络请求；连续两次超时、网络或 CLI 传输错误也会停止。有响应的 HTTP 请求会重置传输错误计数。停止后其余项目标为未知/未检查，保留旧状态，不把它们称为“无更新”。脚本不会绕过鉴权或限流。

## 如何解释快照

| 字段或事件 | 含义与处理 |
| --- | --- |
| `baseline: true` | 首次观测，不把现有提交、文件或 release 全部报告为新增。首次关注文件不存在仍会单独警告。 |
| `state` / `last_success_at` | 各部分最后一次成功读取的状态与时间；读取失败不擦掉旧值。不同部分可能来自不同时间。 |
| `current` | 本轮各部分 `ok`、`unknown` 或 `not_checked`。旧 `state` 不是本轮成功证据；空 `events` 也不等于检查成功。 |
| `new_commit` | HEAD 向前推进。若关注文件均成功读取且没有路径变化事件，只说明这些文件未变，不说明全仓库未变或值得采纳。 |
| `watched_path_changed` | 关注路径的 Git blob SHA、类型或存在性变化；这是人工审阅线索，不是语义改进判断。 |
| `possible_moves` | 原路径消失后发现相同 SHA 的其他路径；仅提示可能移动，不自动改追踪路径。 |
| `head_changed` | HEAD 倒退、分叉或祖先关系未知。可能是分支重写，需审阅，不能当作正常升级。 |
| 许可、默认分支、仓库名称或归档事件 | 需人工核查。MIT 等 SPDX 标签仅是 GitHub 元数据，不能替代许可正文和署名检查。 |
| `latest_stable_release_changed` | GitHub `/releases/latest` 的最新稳定 release 元数据变化；不覆盖全部预发布版本、标签或附件。 |

`/releases/latest` 返回 404 记作当前端点没有可用稳定 release；其他失败记作未知并保留上次成功 release。某仓库消失、限流或断网也不会删除历史成功状态。文件内容不进入快照，只有固定路径的 SHA、状态和少量仓库/release 元数据。

退出码 `0` 表示本轮读取完整；`1` 表示已有 JSON 输出，但有不可用或部分失败；`2` 表示本地输入/参数有误，此时不能用空输出覆盖旧快照。`0` 也可能包含待审阅事件，不能据此自动采纳更新。部分快照可继续作为 `--previous`，因其保留各部分成功状态；若改变来源 ID 或仓库，不将其静默视为原来源延续。

## 初始来源核对（2026-09-18）

通过作者仓库的 GitHub 官方 API 核对：以下 7 个仓库均可读取，默认分支为 `main`、未归档、API 许可标记为 `MIT`，且存在根目录 `LICENSE`。核对了清单中的技能/参考文件路径；首次运行只是建立基线。这是元数据和路径检查，不是对所有上游正文、质量或法律权利的全面审查。

| 来源 | 当时默认 HEAD（链接固定提交） | 关注理由 |
| --- | --- | --- |
| [blader/humanizer](https://github.com/blader/humanizer) | [9862685](https://github.com/blader/humanizer/commit/9862685f575c65a8247f90369951df1b3416e3d6) | Human Writing 原来源；编辑原则、模式目录和许可。 |
| [Worigin0314/academic-defensive-writing-auditor](https://github.com/Worigin0314/academic-defensive-writing-auditor) | [89f26b8](https://github.com/Worigin0314/academic-defensive-writing-auditor/commit/89f26b8a7f8149e6458f657010d354587d42cfe9) | Academic Clarity 原来源；分类、示例和证据保护。 |
| [msimchowitz/writing-skills](https://github.com/msimchowitz/writing-skills) | [214981f](https://github.com/msimchowitz/writing-skills/commit/214981fe02326f27b0fc8790d00eb4b731607073) | 学术作者声音和行文节奏。 |
| [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) | [a58df06](https://github.com/Aboudjem/humanizer-skill/commit/a58df065367550b6ce40ff3f648335018d8e0589) | 审计/改写分工；不自动接受检测器指标。 |
| [ymeiri/voice-layer](https://github.com/ymeiri/voice-layer) | [de19688](https://github.com/ymeiri/voice-layer/commit/de196880f0afade02992a513078a40f40ba2630a) | 独立声音档案、证据结构和用户控制。 |
| [Evidence-Bound-Press-Conference-Revision-Skill](https://github.com/lensback940701/Evidence-Bound-Press-Conference-Revision-Skill) | [33e6c3a](https://github.com/lensback940701/Evidence-Bound-Press-Conference-Revision-Skill/commit/33e6c3a2f69c8c27dfd328e7b8df97609c81687f) | 证据状态、局部限定与回归检查。 |
| [Kiterlin/anti-defensive-writing](https://github.com/Kiterlin/anti-defensive-writing) | [bda84b2](https://github.com/Kiterlin/anti-defensive-writing/commit/bda84b2ffbac66f539010b50653c202baf637d53) | 直接陈述原则；同时观察根目录和分发目录规则。 |

现有采纳/拒绝记录仍在两个技能的[Human Writing 来源说明](../skills/human-writing/references/sources-and-decisions.md)与[Academic Clarity 来源说明](../skills/academic-clarity/references/sources-and-design.md)。上游变更不改变这些记录，除非另行完成审阅与测试。

## 首次发现线索：未采纳、未自动纳入观察

2026-09-18 使用 GitHub 仓库搜索，每个查询仅看前 3 条：`humanizer skill`、`defensive academic writing skill`、`author voice skill`。排除已知来源后，得到以下线索。这里的相关性来自作者仓库描述和 API 许可标签，尚未审阅正文、兼容性、许可原文或效果；没有复制、执行其内容或安装任何项目。

| 研究线索 | 值得后续审阅的原因 | 当时 API 许可标签 |
| --- | --- | --- |
| [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) | 中文本地化的表达分类；需查有无机械禁词或证据损失。 | MIT |
| [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer) | 声称面向学术/基金文字与证据；需先核实许可与实际约束。 | NOASSERTION（未识别） |
| [Adkid-Zephyr/anti-defensive-writing-Skill](https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill) | 双语轻量原则与提示包；需比较保护限定的能力。 | MIT |
| [OvOYu/anti-defensive-writing](https://github.com/OvOYu/anti-defensive-writing) | 学术改写和论证结构；需检查证据边界与作者立场。 | MIT |
| [kkarpushin/tone-of-voice](https://github.com/kkarpushin/tone-of-voice) | 可复用作者风格描述；需检查样本来源、隐私和启用语义。 | MIT |
| [wdkang123/stop-slop-zh](https://github.com/wdkang123/stop-slop-zh) | 中文事实和声音保留；需检查是否强加模板。 | MIT |
| [Gabberflast/prose-revision-skill-ht-anthony-lee-zhang](https://github.com/Gabberflast/prose-revision-skill-ht-anthony-lee-zhang) | 论述推进优先并声称保留好稿；需核实最小改动原则。 | MIT |

这不是推荐榜、质量排名或效果证据。后续最多先选少量真正相关的规则做许可审查和隔离对照；更新 HEAD、下载量、星数或作者自述都不能替代实际收益与忠实性检查。
