# fde-problem-framing · v0.2.0

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

## 运行验证
Python 3.9+，核心脚本与测试仅用标准库。
```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_math.py --stage 20 --share 0.5 --target 22 --unaffected-case-share 0.35
```
第二条的0.35是明确的**假设案件占比**，不能由原文的定损单占比直接代入。默认不提供该参数时不会计算覆盖下界。

实际结果与限制见 tests/RESULTS.md。静态规范检查和数学测试不能证明模型必然遵守流程，更不能证明客户方案有效。按 tests/behavioral-cases.md 可在目标宿主重跑行为测试。

## 书稿与分发
原始需求、来源指纹和修订记录已保留；案例数字来自用户教学情境或显式条件推导。没有公开授权推定，分发前按 references/provenance.md 检查来源元数据与匿名化。未复制私有仓库全文。原私有仓库保持不变。本工程按用户要求独立托管为私有仓库，后续推进见 [ROADMAP.md](ROADMAP.md)，历史验证与待办见 [DEVELOPMENT.md](DEVELOPMENT.md)。

## 煤层气标准检索验证
新增 [煤层气案例](examples/cbm-standards/README.md)，重点为条款定位与工况适用性。公开材料与专家方向反馈分开留底；验证情况见 [v0.2结果](tests/RESULTS-v02.md)。
