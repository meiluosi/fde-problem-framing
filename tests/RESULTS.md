# v0.1.0 实际验证结果
日期：2026-10-19。全部在独立工作目录运行，未修改 fde-ramp 或真实技能安装目录。

| 检查 | 实际结果 | 能证明什么 |
|---|---|---|
| Python单元/交付检查 | 17/17通过，原始输出 unit-test-output.txt | 算术、边界、非法参数、命令行、引用路径及来源指纹完整性 |
| skill-creator quick_validate.py | Skill is valid!，原始输出 skill-validation-output.txt | frontmatter、命名及脚手架规范，不证明判断质量 |
| 临时安装烟测 | 通过，原始输出 installation-output.txt | 完整复制后可从其他目录运行；非宿主自动发现验证 |
| Mermaid | 源码人工检查；未运行渲染器 | 不声称已验证渲染或布局 |

数学覆盖：40分钟条件基线、核对2分钟与90%降幅、总体45%降幅；可选案件假设下27分钟下界与28.3分钟加权值；不传案件占比时不自动推覆盖；0/1覆盖边界、负数/NaN/Infinity拒绝、目标不可达与无需提效场景。

规范检查器最初因缺PyYAML失败。随后从PyPI取得PyYAML 6.0.3源码，核验其SHA256后仅在工作目录加载，原检查器成功；未替换检查器或自行模拟通过。该依赖只用于开发验证，核心脚本/单元测试不依赖第三方包。

## 独立行为验证
执行者为独立新上下文子代理，只提供 Skill 路径、按需引用和原始场景；未提供examples、tests及父任务判定。初轮Skill的指标参考本身包含理赔推导，因此初轮理赔测试属于指令应用回归。评审后已将具体数字移出通用规则，追加异值与并行边界迁移测试；该测试仍不构成跨场景统计保证。实际输出归档在 behavioral-output/。

最终逐项评审与复测记录见 behavioral-review.md。

## 可复跑命令
在工程目录运行：
```sh
python3 -m unittest discover -s tests -v
python3 tests/installation-smoke.py
python3 scripts/check_math.py --stage 20 --share 0.5 --target 22 --unaffected-case-share 0.35
```
官方规范检查另需 skill-creator 的 quick_validate.py 和 PyYAML；该校验器不随本包复制。

限制：不是现场试点；没有真实日志、客户访谈、费用或模型性能验证；没有跨模型统计评估；未在Codex/DSH真实安装目录安装。待办见 ../DEVELOPMENT.md。行为协议中的未执行项不得算作通过。
