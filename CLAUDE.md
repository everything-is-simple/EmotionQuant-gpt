# CLAUDE.md

本文件保留为代理兼容入口，但已与当前 Spiral 开发基线同步。

## 文档定位

- 作用：给自动化代理提供最小、可执行的仓库工作规则。
- 执行主计划唯一入口：`docs/design/enhancements/eq-improvement-plan-core-frozen.md`（`enhancement-selection-analysis_claude-opus-max_20260210.md` 仅作选型论证输入）。
- 权威架构入口：`docs/system-overview.md`
- 权威路线入口：`Governance/Capability/SPIRAL-CP-OVERVIEW.md`
- 权威治理入口：`Governance/steering/`

## 当前执行模型

- 执行模型：Spiral（螺旋闭环），非线性 Stage 流水线。
- 默认节奏：7 天一圈。
- 路线术语：Capability Pack（CP），使用 `CP-*` 文件名。
- 每圈闭环：`run + test + artifact + review + sync`。

## 核心约束（七铁律）

1. 情绪优先：信号主逻辑必须以情绪因子为核心。
2. 单指标不得独立决策：技术指标可对照/辅助特征，但不得单独触发交易。
3. 本地数据优先：主流程读取本地数据，远端仅补采。
4. 路径密钥禁止硬编码：路径/密钥必须通过 `Config.from_env()` 或环境变量注入。
5. A 股规则刚性执行：T+1、涨跌停、交易时段。
6. 螺旋闭环强制：每圈必须有 run/test/artifact/review/sync，缺一不得收口。
7. 文档服务实现：禁止文档膨胀阻塞开发，最小同步优先。

详见：`Governance/steering/系统铁律.md`

## 工作流（分级治理）

### 默认模式（个人开发）

`Scope -> Build -> Verify -> Sync`

适用绝大多数任务。

### 升级模式（Strict 6A）

仅在以下场景启用完整 6A：

- 交易执行路径重大改动
- 风控规则重大改动
- 数据契约破坏性变更
- 引入影响主流程的新外部依赖

详见：

- `Governance/steering/6A-WORKFLOW.md`

## 文档同步要求（最小集）

每圈收口强制同步：

1. `Governance/specs/spiral-s{N}/final.md`
2. `Governance/record/development-status.md`
3. `Governance/record/debts.md`
4. `Governance/record/reusable-assets.md`
5. `Governance/Capability/SPIRAL-CP-OVERVIEW.md`

`CP-*.md` 仅在契约变化时更新。

## 技术栈口径（当前）

- Python `>=3.10`
- 数据：Parquet + DuckDB（单库优先）
- GUI 主线：Streamlit + Plotly
- 回测主选：Qlib（研究与实验）；执行基线：本地向量化回测器；兼容适配：backtrader（可选，不是主线）

详见：

- `pyproject.toml`
- `requirements.txt`
- `docs/design/core-infrastructure/backtest/backtest-engine-selection.md`

## 仓库远端

- `origin`: `https://github.com/everything-is-simple/EmotionQuant_beta.git`

## 历史说明

- 旧版线性文档已归档至：
  - `Governance/Capability/archive-legacy-linear-v4-20260207/`
- 本文件不再维护线性 Stage 叙述。



