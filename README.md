# fde-problem-framing · v0.2.2

独立的第二个 FDE Skill：针对一个具体业务问题，按需澄清、现场诊断、生成定义卡或审查。fde-ramp 负责行业入门与机会发现；本 Skill 接收其选定场景，不需要安装 ramp，也不修改其仓库。

## 安装与使用

将整个 `fde-problem-framing` 文件夹放入宿主的 skills 目录，保留目录名与 SKILL.md。Codex 常用 `${CODEX_HOME:-$HOME/.codex}/skills/`；本机安装状态见 tests/RESULTS-v02.md。也可不安装，直接让助手读取本目录 SKILL.md。

例如在解压目录运行（已有同名目录时先检查，不覆盖）：
```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R -n fde-problem-framing "${CODEX_HOME:-$HOME/.codex}/skills/"
```
如宿主未重新发现技能，开启新会话。DSH 用户可按其已有 fde-ramp 安装方式放到对应 skills 目录；未做该宿主实机测试。

可直接说：
- “用 $fde-problem-framing 澄清这个需求：我们要上AI客服。先问最影响下一步的问题。”
- “读取 ramp/ 的 activities.md、flow.md 和 process-metrics.md，只诊断材料核对这一环。”
- “把现有证据生成一页纸定义卡，缺证据保留 Investigate。”
- “审查这份定义，重点核对目标可达性、手写覆盖和200单抽样。”

## 工程内容
- SKILL.md：入口与四种模式路由。
- references/：衔接、证据、决策、指标、作图、留底规范。
- templates/：定义卡、底稿、验证计划、审查和修订记录。
- examples/：理赔完整产物与客服、问数案例，均非真实现场证据。
- scripts/check_math.py：条件算术审查，不是业务审批器。
- tests/：可重复单元测试、行为任务与实际结果。
- DEVELOPMENT.md：来源、方法修订与待办。

## FDE Skill 系列

各 Skill 独立运行，通过手动读取的产物衔接，不互相依赖安装。典型顺序：ramp → problem-framing → route-selection → knowledge-base（场景含文档检索时）→ demo → pilot，comms 贯穿各阶段。

| Skill | 管什么 | 结论词 |
|---|---|---|
| [fde-ramp](https://github.com/meiluosi/fde-ramp) | 见客户前搭起行业基本盘，拿图去被一线改 | 自检分数 |
| [fde-problem-framing](https://github.com/meiluosi/fde-problem-framing) | 把需求变成有证据的业务问题，比较 AI 与非 AI | Proceed / Investigate / Non-AI / Stop-Defer |
| [fde-route-selection](https://github.com/meiluosi/fde-route-selection) | 业务问题定义之后，先过滤合规与部署等硬约束，再选适配路线，最后用客户样本比选模型 | 见该仓库 |
| [fde-knowledge-base](https://github.com/meiluosi/fde-knowledge-base) | 路线含文档检索（RAG）时，判断知识够不够、怎么治、怎么评、质量卡在哪 | Proceed / Investigate / Pivot / Stop-Defer |
| [fde-comms](https://github.com/meiluosi/fde-comms) | 与人的关键沟通：访谈、向上汇报、坏消息 | 无（产出文稿） |
| [fde-demo](https://github.com/meiluosi/fde-demo) | 设计并复盘一次客户 Demo，换验证与信任 | Proceed / Iterate / Pivot / Stop-Defer |
| [fde-pilot](https://github.com/meiluosi/fde-pilot) | 把 Demo 通过的方案做成可检验的试点并判定成效 | Proceed / Iterate / Pivot / Stop-Defer |

跨 Skill 引用时加前缀保留原编号（`ramp:S01`、`framing:V2`、`kb:Q01`、`demo:L3`、`pilot:M2`）；同名结论词含义随阶段不同，引用时写 `framing:Proceed`、`demo:Proceed`。编号、结论词、边界与回写规则的完整约定见 [fde-demo 的 references/series.md](https://github.com/meiluosi/fde-demo/blob/main/references/series.md)。

## 运行验证
Python 3.9+，核心脚本与测试仅用标准库。
```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_math.py --stage 20 --share 0.5 --target 22 --unaffected-case-share 0.35
```
第二条的0.35是明确的**假设案件占比**，不能由原文的定损单占比直接代入。默认不提供该参数时不会计算覆盖下界。

实际结果与限制见 tests/RESULTS.md。静态规范检查和数学测试不能证明模型必然遵守流程，更不能证明客户方案有效。按 tests/behavioral-cases.md 可在目标宿主重跑行为测试。

## 书稿与分发
原始需求、来源指纹和修订记录已保留；案例数字来自用户教学情境或显式条件推导。没有公开授权推定，分发前按 references/provenance.md 检查来源元数据与匿名化。未复制私有仓库全文。原私有仓库保持不变。本工程独立托管为公开仓库（MIT），后续推进见 [ROADMAP.md](ROADMAP.md)，历史验证与待办见 [DEVELOPMENT.md](DEVELOPMENT.md)。

## 煤层气标准检索验证
新增 [煤层气案例](examples/cbm-standards/README.md)，重点为条款定位与工况适用性。公开材料与专家方向反馈分开留底；验证情况见 [v0.2结果](tests/RESULTS-v02.md)。

本轮修订将煤层气案例收回问题定义与诊断，见 [v0.2.2验证记录](tests/RESULTS-v021.md)。

以根路径安装后须检查 references/、templates/ 等子目录是否齐全；本机曾遇到仅安装入口文件的情况，已补齐。完整压缩包解压复制可避免这一缺失。

本版区分改善价值、干预选择与推进状态，见 [判断流程](references/decision-flow.md) 与 [本轮验证](tests/RESULTS-v022.md)。

## 参考与致谢

本系列各 Skill 在方法设计上不同程度参考了《FDE:AI落地实战指南》，以及作者本人的 FDE 实践经历。各 Skill 的流程、模板、规则与脚本是在此基础上改写和扩展的方法。示例中的人物、数字与场景均为虚构，不是客户事实。

## 许可
MIT，见 [LICENSE](LICENSE)。
