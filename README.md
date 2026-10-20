# fde-problem-framing · v0.3.0 验证版

FDE业务问题定义与诊断助手。把客户诉求整理成有证据边界的问题、竞争解释和可执行下一步，比较流程、知识整理、规则、传统软件与AI。

`fde-ramp`负责行业入门与机会扫描；本Skill只承接选定场景，也可独立使用。它不代替一线证据、客户决定或系统实施。

## 三分钟开始

1. 下载 [v0.3.0版本包](https://github.com/meiluosi/fde-problem-framing/releases/tag/v0.3.0)，解压后进入 `fde-problem-framing` 文件夹。也可完整克隆本公开仓库，勿只复制SKILL.md。
2. Python 3.9+，无第三方Python依赖：

```sh
python3 scripts/package.py verify
python3 scripts/package.py install --dest "${CODEX_HOME:-$HOME/.codex}/skills/fde-problem-framing"
```

已有安装时加 `--update --backup-dir "${CODEX_HOME:-$HOME/.codex}/skill-backups"`（备份必须在skills目录之外，避免被重复发现）：先核对旧文件未修改，完整安装成功后保留旧目录备份；有本地修改或旧安装不完整则停止，不覆盖。先保存自己的修改，再选择新的安装目录或人工合并。散列只能检测文件一致性，不能证明发布者身份。

安装后在下一轮使用 `$fde-problem-framing`；如宿主没有发现，开启新会话。其他宿主使用其技能目录，尚未逐一实机验证。也可直接让助手读取本目录SKILL.md。

3. 任选一种请求：

| 模式 | 可以直接说 |
|---|---|
| 澄清 | 用此Skill澄清“客服太慢，想上AI”，先问最影响决定的问题 |
| 诊断 | 已知主要等待发生在工单转派，请提出竞争解释与最小验证 |
| 生成 | 根据已有信息先出一页纸，缺证据写清楚，不继续访谈 |
| 审查 | 审查这份定义，检查口径、覆盖、根因假设和非AI备选 |

## 输出是什么

一页问题卡、按需诊断底稿、验证计划、审查报告及辅助Mermaid图。决定拆成三列：

| 价值判断 | 干预方向 | 推进状态 |
|---|---|---|
| Supported / Unknown / Unsupported | 现状、流程、知识整理、规则搜索、传统软件、AI辅助、组合或未定 | Proceed / Investigate / Stop-Defer |

每列注明环节、证据与范围。Non-AI仅是方向标签；不用AI仍可推进，有效专家协作也不排除前置查阅改善。证据不足先交付带缺口草稿与最小验证，不无限追问。

## 看一个完整例子

[煤层气当前问题卡](examples/cbm-standards/problem-card.md)与[当前诊断](examples/cbm-standards/diagnosis.md)：用户逐段查PDF，未定位后请教专家；专家协作有效。当前核验前置查阅的非AI改善机会，尚无现场收益数据。旧误判保留在[修订记录](examples/cbm-standards/revisions.md)，不混进当前状态。

另有[理赔](examples/claims/problem-card.md)、[客服](examples/support.md)、[问数](examples/analytics.md)。数字来源和合成前提各自标注；示例不是当前客户事实。

## 验证与贡献

```sh
python3 -m unittest discover -s tests -v
python3 tests/installation-smoke.py
python3 scripts/package.py build --output ../fde-problem-framing-v0.3.0.zip
```

已知限制：完整多轮复测仍出现重复确认；本版未宣称所有行为测试通过。

[本版验证记录](tests/RESULTS-v03.md)区分工程检查、多轮行为回放和未完成的现场验证。行为评审关注实际输出，不靠关键词命中证明诊断可靠。测试输入、评分和执行输出分开，见 [回放协议](tests/multiturn/README.md)。

提交问题时提供脱敏原话、期望行为、实际行为及版本，不上传客户原件或凭据。讨论后再增加通用规则，避免把某个案例硬编码进Skill。当前路线见[ROADMAP](ROADMAP.md)。

## 来源与书稿

公开仓库：[meiluosi/fde-problem-framing](https://github.com/meiluosi/fde-problem-framing)。上游ramp仅保存接口来源与指纹，未复制私有全文；公开用户无法访问私有来源时仍可独立使用本Skill。原话、证据与修订分别留底；书稿使用前按 [来源与匿名化规则](references/provenance.md)处理。沿用远端已添加的MIT许可，见 [LICENSE](LICENSE)。

## FDE Skill 系列

各 Skill 独立运行，通过手动读取的产物衔接，不互相依赖安装。典型顺序：ramp → problem-framing → route-selection → knowledge-base（场景含文档检索时）→ demo → pilot，comms 贯穿各阶段。

| Skill | 管什么 | 结论词 |
|---|---|---|
| [fde-ramp](https://github.com/meiluosi/fde-ramp) | 见客户前搭起行业基本盘，拿图去被一线改 | 自检分数 |
| [fde-problem-framing](https://github.com/meiluosi/fde-problem-framing) | 把需求变成有证据的业务问题，比较 AI 与非 AI | 价值 / 方向 / 推进状态（三字段，Non-AI仅为方向标签） |
| [fde-route-selection](https://github.com/meiluosi/fde-route-selection) | 业务问题定义之后，先过滤合规与部署等硬约束，再选适配路线，最后用客户样本比选模型 | 见该仓库 |
| [fde-knowledge-base](https://github.com/meiluosi/fde-knowledge-base) | 路线含文档检索（RAG）时，判断知识够不够、怎么治、怎么评、质量卡在哪 | Proceed / Investigate / Pivot / Stop-Defer |
| [fde-comms](https://github.com/meiluosi/fde-comms) | 与人的关键沟通：访谈、向上汇报、坏消息 | 无（产出文稿） |
| [fde-demo](https://github.com/meiluosi/fde-demo) | 设计并复盘一次客户 Demo，换验证与信任 | Proceed / Iterate / Pivot / Stop-Defer |
| [fde-pilot](https://github.com/meiluosi/fde-pilot) | 把 Demo 通过的方案做成可检验的试点并判定成效 | Proceed / Iterate / Pivot / Stop-Defer |

跨 Skill 引用时加前缀保留原编号（`ramp:S01`、`framing:V2`、`kb:Q01`、`demo:L3`、`pilot:M2`）；同名结论词含义随阶段不同，引用时写 `framing:Proceed`、`demo:Proceed`。编号、结论词、边界与回写规则的完整约定见 [fde-demo 的 references/series.md](https://github.com/meiluosi/fde-demo/blob/main/references/series.md)。


## 参考与致谢

本系列各 Skill 在方法设计上不同程度参考了《FDE:AI落地实战指南》，以及作者本人的 FDE 实践经历。各 Skill 的流程、模板、规则与脚本是在此基础上改写和扩展的方法。示例的合成、教学或用户经验来源以各案例标注为准，不能将经验陈述冒充客户实测。


## 许可
MIT，见 [LICENSE](LICENSE)。
