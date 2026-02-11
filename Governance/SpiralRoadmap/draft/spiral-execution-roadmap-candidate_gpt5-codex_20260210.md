# EmotionQuant 螺旋实施路线图执行候选稿（GPT-5 Codex）

## 0. 文档元信息

- 文档用途: 作为 `Governance/SpiralRoadmap/draft/spiral-full-roadmap-detailed_claude-opus-max_20260210.md` 的校正后执行稿，供你审批后落为主路线。
- 生成模型: GPT-5 Codex
- 生成时间: 2026-02-10
- 状态: Candidate（评审中）
- 适用范围: S0-S6 Spiral 实施
- 上位约束:
  - `docs/design/enhancements/eq-improvement-plan-core-frozen.md`
  - `Governance/steering/系统铁律.md`
  - `Governance/steering/CORE-PRINCIPLES.md`
  - `Governance/steering/6A-WORKFLOW.md`
  - `Governance/Capability/CP-*.md`

> 说明: 本文件是“新路线图候选稿”，不是并行长期主计划。你确认后建议回写到 `eq-improvement-plan-core-frozen.md`，保持目录单主文件原则。

---

## 1. 评估结论

## 1.1 是否可成为新路线图

结论: 可以，但不能原样直接升主计划。详细版明显优于旧版，已经具备任务可执行骨架；需要修正以下关键项后再作为主路线。

1. 修正 Slice 预算冲突: 多处超过“每圈 1-3 Slice”铁则。
2. 补齐 S4-S6 缺失项: 验收标准与五件套退出条件不完整。
3. 统一编号口径: 当前仓库同时存在 `S0-S6` 与 `S00-S07` 两套编号。
4. 修正文档同步边界: 不应把入口文档全量更新设为每圈刚性动作。
5. 结合仓库现状重估工时: 当前仓库并非纯空白，已有 config/模型/测试骨架，应按“骨架已在、能力未成”估算。

## 1.2 本稿新增价值

1. 每个 S 都给出: 核心/基础设施/外挂占比、任务数量、进出边界、错误处理、验收标准、遗产。
2. 每个任务都写明“存在理由”，避免形式化任务堆砌。
3. 明确降级策略: 任何一圈失败时如何缩圈，不破坏闭环。
4. 显式标注 Strict 6A 圈: S4 必升，S3/S6 条件触发升。

---

## 2. 关键依据清单（已对读）

- 入口与治理:
  - `README.md`
  - `CLAUDE.md`
  - `docs/system-overview.md`
  - `docs/module-index.md`
  - `docs/naming-conventions.md`
  - `Governance/steering/系统铁律.md`
  - `Governance/steering/CORE-PRINCIPLES.md`
  - `Governance/steering/6A-WORKFLOW.md`
- 路线与能力包:
  - `docs/design/enhancements/eq-improvement-plan-core-frozen.md`
  - `Governance/SpiralRoadmap/draft/spiral-full-roadmap-detailed_claude-opus-max_20260210.md`
  - `Governance/Capability/SPIRAL-CP-OVERVIEW.md`
  - `Governance/Capability/CP-01-data-layer.md` 到 `Governance/Capability/CP-10-validation.md`
- 设计契约:
  - `docs/design/core-infrastructure/data-layer/data-layer-data-models.md`
  - `docs/design/core-algorithms/mss/mss-algorithm.md`
  - `docs/design/core-algorithms/irs/irs-algorithm.md`
  - `docs/design/core-algorithms/pas/pas-algorithm.md`
  - `docs/design/core-algorithms/integration/integration-algorithm.md`
  - `docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md`
  - `docs/design/core-algorithms/validation/factor-weight-validation-data-models.md`
  - `docs/design/core-infrastructure/backtest/backtest-algorithm.md`
  - `docs/design/core-infrastructure/backtest/backtest-engine-selection.md`
  - `docs/design/core-infrastructure/trading/trading-algorithm.md`
  - `docs/design/core-infrastructure/trading/trading-data-models.md`
  - `docs/design/core-infrastructure/analysis/analysis-algorithm.md`
  - `docs/design/core-infrastructure/gui/gui-algorithm.md`
- 实现现状:
  - `src/config/config.py`
  - `src/data/fetcher.py`
  - `src/data/models/snapshots.py`
  - `src/pipeline/main.py`
  - `src/gui/app.py`
  - `tests/unit/**`

---

## 3. 全局执行契约（所有 Spiral 生效）

## 3.1 冻结边界

只允许实现，不允许改语义:

1. 情绪优先与“单指标不得独立决策”。
2. MSS/IRS/PAS/Validation/Integration 核心公式与命名口径。
3. L1-L4 数据契约与关键业务表字段。
4. A 股规则: T+1、涨跌停、交易时段、整手、费用模型。

## 3.2 切片预算与拆圈规则

1. 一圈仅 1 主目标。
2. 一圈仅 1-3 CP Slice。
3. 若超过 3 Slice，必须拆为下一圈或圈内“前后闭环子圈”并分别留五件套证据。
4. 单任务预计超过 1 天必须拆分。

## 3.3 分类定义（用于工时分配）

- 核心实现: 直接产出 CP 业务能力。
- 主要基础设施: 编排、配置、适配、可观测、可运行入口。
- 外挂增强: 不改变核心语义的守卫、对照、可视化、回归资产。

## 3.4 错误分级

- P0: 阻断（输入缺失、契约破坏、合规违规）。
- P1: 降级+标注（局部缺失、局部失败）。
- P2: 重试+记录（非关键异常）。

## 3.5 五件套退出条件（每圈必须）

1. run: 至少 1 条可复制命令。
2. test: 至少 1 组自动化测试。
3. artifact: 至少 1 个结构化产物。
4. review: `Governance/specs/spiral-s{N}/review.md`。
5. sync: 最小同步 5 文件（`final.md` + `development-status.md` + `debts.md` + `reusable-assets.md` + `SPIRAL-CP-OVERVIEW.md`）。

## 3.6 Strict 6A 升级规则

- S4 默认 Strict 6A（交易执行主链改动）。
- S3/S6 在以下条件触发 Strict 6A:
  - 数据契约破坏性变化。
  - Validation Gate 规则变更。
  - 新关键外部依赖进入主路径。

## 3.7 编号统一

本稿执行采用 `S0-S6`。与 `S00-S07` 的映射:

- S00 -> S0 准备态（并入 S0）
- S01 -> S0
- S02 -> S1/S2
- S03 -> S2/S3
- S04 -> S3
- S05 -> S4
- S06 -> S5
- S07 -> S6

---

## 4. 总体路线与工作量

| Spiral | 主目标 | CP Slice（<=3） | 任务数 | 预估工时 | 核心 | 基础设施 | 外挂 |
|---|---|---|---:|---:|---:|---:|---:|
| S0 | 数据最小闭环 | CP01-S1, CP01-S2 | 5 | 4.5d | 45% | 30% | 25% |
| S1 | MSS 闭环 | CP02-S1, CP02-S2(最小) | 4 | 3.5d | 75% | 10% | 15% |
| S2 | IRS/PAS/Validation 闭环 | CP03-S1, CP04-S1, CP10-S1 | 5 | 5.5d | 70% | 15% | 15% |
| S3 | Integration+Backtest+Analysis 闭环 | CP05-S1, CP06-S1, CP09-S1 | 5 | 5.0d | 55% | 25% | 20% |
| S4 | 纸上交易闭环（Strict 6A） | CP07-S1, CP07-S2, CP09-S1(复用) | 4 | 4.5d | 60% | 15% | 25% |
| S5 | GUI+日报闭环 | CP08-S1, CP09-S2 | 3 | 3.0d | 55% | 25% | 20% |
| S6 | 稳定化收敛闭环 | CP10-S2, CP07-S3, CP09-S3 | 4 | 4.0d | 50% | 25% | 25% |
| 合计 | - | - | 30 | 30.0d | ~59% | ~20% | ~21% |

> 说明: 估算已考虑仓库已有 `Config`、`snapshot dataclass`、基础测试骨架，不按“零起步”估算。

---

## 5. S0 数据最小闭环

## 5.1 存在意义

无稳定 L1/L2 输入，后续所有算法无法形成可验证结果。S0 的目标是“可复现链路”，不是“一次性拉全”。

## 5.2 组成与边界

- 核心: TuShare 拉取、Parquet 落盘、DuckDB 入库、L2 快照。
- 基础设施: `eq run` 命令、环境配置、数据路径注入。
- 外挂: error_manifest、canary 数据包、freeze_check。

In Scope:

- `raw_daily/raw_daily_basic/raw_limit_list/raw_index_daily/raw_trade_cal` 最小可用。
- `market_snapshot` 完整字段（含 `data_quality/stale_days/source_trade_date`）。
- `industry_snapshot` 骨架字段。

Out Scope:

- IRS/PAS/MSS 评分。
- Validation Gate。
- Backtest/Trading/GUI。

## 5.3 子任务分解（5个）

| 任务 | 分类 | 主要产出 | 存在理由 | 工时 |
|---|---|---|---|---:|
| S0-T1 CLI 与配置落地 | 基础设施 | `eq run`、`.env.example`、Config 接线 | 没有统一入口无法闭环复现 | 0.8d |
| S0-T2 TuShare 采集实现 | 核心 | `TuShareFetcher` 可用拉取 | 数据源入口必须先通 | 1.0d |
| S0-T3 Parquet->DuckDB 入库 | 核心 | Repository 入库链路 | 后续算法统一读本地 | 1.0d |
| S0-T4 L2 快照计算 | 核心 | `market_snapshot/industry_snapshot` | MSS/IRS 输入前置依赖 | 1.0d |
| S0-T5 守卫与回归资产 | 外挂 | `error_manifest`、canary、freeze_check | 保证失败可追踪、离线可回归 | 0.7d |

## 5.4 错误处理

| 场景 | 级别 | 处理 |
|---|---|---|
| `TUSHARE_TOKEN` 缺失/无效 | P0 | 立即阻断 |
| API 限流或网络抖动 | P2 | 重试3次+指数退避 |
| 非交易日无数据 | P1 | 回退最近交易日并标注 stale |
| parquet/duckdb 写入失败 | P0 | 阻断并写 error_manifest |
| 局部标的缺失 | P1 | 跳过并标注质量 |

## 5.5 验收标准

1. `eq run --date 20260207 --source mock` 返回 0。
2. `pytest tests/canary tests/contracts/test_data_* -q` 全通过。
3. DuckDB 存在 `market_snapshot` 且字段契约完整。
4. 失败流程能输出 `error_manifest.json`（含 `error_level`）。
5. `freeze_check` 可执行并对关键文档给出锚点结果。

## 5.6 退出五件套

- run: `eq run --date {trade_date} --source mock`
- test: `pytest tests/canary tests/contracts/test_data_* -q`
- artifact: parquet + duckdb 表 + error_manifest
- review: `Governance/specs/spiral-s0/review.md`
- sync: 最小同步 5 文件

## 5.7 产生遗产

- 统一数据采集入口（TuShareFetcher）。
- 统一运行入口（CLI）。
- canary 数据夹（离线回归）。
- 设计冻结锚点（防漂移）。
- L2 快照表（S1/S2 直接消费）。

---

## 6. S1 MSS 闭环

## 6.1 存在意义

MSS 给出市场层主信号（温度/周期/趋势），是后续 Integration 的必需输入。

## 6.2 组成与边界

In Scope:

- 六因子实现与温度合成（`0.17/0.34/0.34/0.05/0.05/0.05`）。
- 周期判定（含 `unknown` 兜底）与趋势判定。
- `mss_panorama` 落库与契约测试。

Out Scope:

- IRS/PAS/Validation。
- 交易触发逻辑。

## 6.3 子任务分解（4个）

| 任务 | 分类 | 主要产出 | 存在理由 | 工时 |
|---|---|---|---|---:|
| S1-T1 六因子引擎 | 核心 | `src/algorithms/mss/factors.py` | 没有因子就没有温度来源 | 1.0d |
| S1-T2 温度/周期/趋势 | 核心 | `src/algorithms/mss/engine.py` | 周期直接影响推荐等级规则 | 1.0d |
| S1-T3 Writer + CLI | 核心/基础设施 | `mss_panorama` 与 `eq mss` | 没有落库无法被下游消费 | 0.8d |
| S1-T4 契约测试与可视化基础 | 外挂 | mss contract tests + L4温度序列 | 防回归并为 S5 提前准备 | 0.7d |

## 6.4 错误处理

| 场景 | 级别 | 处理 |
|---|---|---|
| `market_snapshot` 关键字段缺失 | P0 | 阻断并提示回到 S0 |
| 历史样本不足 | P1 | 分数置 50 并标记 cold_start |
| 温度越界 | P1 | 裁剪到 [0,100] 并告警 |
| 非交易日输入 | P0 | 阻断 |

## 6.5 验收标准

1. `eq mss --date {trade_date}` 成功产出 `mss_panorama`。
2. `pytest tests/contracts/test_mss_* -q` 通过。
3. `temperature in [0,100]`、`neutrality in [0,1]`。
4. 相同输入重复运行结果一致。
5. 无交易触发字段（保持信号层边界）。

## 6.6 退出五件套

- run: `eq mss --date {trade_date}`
- test: `pytest tests/contracts/test_mss_* -q`
- artifact: `mss_panorama`
- review: `Governance/specs/spiral-s1/review.md`
- sync: 最小同步 5 文件

## 6.7 产生遗产

- `normalize_zscore` 统一实现。
- MSS 输出标准表。
- 周期与趋势判定实现模板（IRS/PAS 可参考）。

---

## 7. S2 IRS/PAS/Validation 闭环

## 7.1 存在意义

完成行业层与个股层信号，并给出可执行 Gate。S2 结束后，系统具备“可被集成”的完整输入，但不强行在同圈叠加 Integration，避免超 Slice。

## 7.2 组成与边界

In Scope:

- IRS 六因子最小版（31 行业覆盖）。
- PAS 三因子最小版（等级/方向/RR）。
- Validation 因子门禁（IC/RankIC/ICIR/positive_ratio，输出 PASS/WARN/FAIL）。

Out Scope:

- Integration 融合输出（放 S3）。
- 权重 WFA（放 S6 的 CP10-S2）。

## 7.3 子任务分解（5个）

| 任务 | 分类 | 主要产出 | 存在理由 | 工时 |
|---|---|---|---|---:|
| S2-T1 `industry_snapshot` 补齐 + IRS 引擎 | 核心 | `irs_industry_daily` | 三三制行业层输入 | 1.3d |
| S2-T2 `stock_gene_cache` + PAS 引擎 | 核心 | `stock_pas_daily` | 三三制个股层输入 | 1.3d |
| S2-T3 Validation 因子门禁 | 核心 | `validation_gate_decision` | Integration 前置门禁 | 1.2d |
| S2-T4 `validation_weight_plan` 桥接最小版 | 基础设施 | baseline plan 记录 | 对齐 CP10/CP05 接口 | 0.8d |
| S2-T5 契约测试与编排骨架 | 外挂/基础设施 | `eq signal` 或 `eq recommend --phase signal` | 为 S3 集成提供稳定输入 | 0.9d |

## 7.4 错误处理

| 场景 | 级别 | 处理 |
|---|---|---|
| 行业覆盖不足 31 | P1 | 标记 stale，允许继续 |
| 估值样本不足 8 只 | P1 | 沿用前值，标记 cold_start |
| 个股停牌或缺行情 | P1 | 跳过该股 |
| Validation 输入缺失 | P0 | Gate=FAIL，阻断后续集成 |
| baseline plan 缺失 | P0 | 阻断（契约不完整） |

## 7.5 验收标准

1. `irs_industry_daily` 覆盖 31 行业。
2. `stock_pas_daily` 评分范围合法、等级合法、方向合法。
3. `validation_gate_decision` 具备 PASS/WARN/FAIL + reason。
4. `validation_weight_plan` 可按 `(trade_date, plan_id)` 查询。
5. 四组契约测试（IRS/PAS/Validation/Bridge）通过。

## 7.6 退出五件套

- run: `eq recommend --date {trade_date} --phase signal`
- test: `pytest tests/contracts/test_irs_* tests/contracts/test_pas_* tests/contracts/test_validation_* -q`
- artifact: `irs_industry_daily` + `stock_pas_daily` + `validation_gate_decision` + `validation_weight_plan`
- review: `Governance/specs/spiral-s2/review.md`
- sync: 最小同步 5 文件

## 7.7 产生遗产

- 行业与个股信号标准表。
- Validation Gate 决策表与桥接表。
- S3 集成可直接消费的稳定输入层。

---

## 8. S3 Integration + Backtest + Analysis 闭环

## 8.1 存在意义

将 S1/S2 产出的信号融合成统一推荐，再用回测验证是否有效，并产出最小绩效摘要，形成“信号到证据”的第一个完整闭环。

## 8.2 组成与边界

In Scope:

- CP05-S1: baseline 集成输出。
- CP06-S1: 本地向量化回测器。
- CP09-S1: 最小绩效指标摘要。
- Qlib 适配层可选接入（非阻断）。

Out Scope:

- 权重 WFA（S6 CP10-S2）。
- 交易执行（S4）。

## 8.3 子任务分解（5个）

| 任务 | 分类 | 主要产出 | 存在理由 | 工时 |
|---|---|---|---|---:|
| S3-T1 Integration 引擎 | 核心 | `integrated_recommendation` | 下游唯一信号上游 | 1.1d |
| S3-T2 向量化回测器 | 核心 | `backtest_results/trade_records` | 验证信号有效性 | 1.2d |
| S3-T3 分析指标实现 | 核心 | `performance_metrics` | 形成可对比证据 | 0.9d |
| S3-T4 Qlib 适配器 | 基础设施 | `qlib_adapter` | 保持研究主选兼容 | 0.8d |
| S3-T5 A/B/C 对照 | 外挂 | 对照报表 | 证明情绪主线价值 | 1.0d |

## 8.4 错误处理

| 场景 | 级别 | 处理 |
|---|---|---|
| Validation Gate=FAIL | P0 | 阻断 Integration |
| 候选权重缺失且 Gate=WARN | P1 | 回退 baseline |
| 信号与行情日期错位 | P0 | 阻断 |
| 个别标的无行情 | P1 | 跳过并记录 |
| Qlib 不可用 | P2 | 仅执行向量化基线 |

## 8.5 验收标准

1. `integrated_recommendation.final_score` 可追溯到 MSS/IRS/PAS + 权重。
2. `eq backtest --engine vectorized` 可复现。
3. T+1 与涨跌停规则测试通过。
4. 产出 `performance_metrics`。
5. A/B/C 对照表可生成且归档。

## 8.6 退出五件套

- run: `eq recommend --date {trade_date}` + `eq backtest --engine vectorized --start {start} --end {end}`
- test: `pytest tests/contracts/test_integration_* tests/contracts/test_backtest_* tests/contracts/test_analysis_* -q`
- artifact: `integrated_recommendation` + `backtest_results` + `performance_metrics` + A/B/C 报表
- review: `Governance/specs/spiral-s3/review.md`
- sync: 最小同步 5 文件

## 8.7 产生遗产

- 统一推荐输出表。
- 可复用回测引擎与指标模块。
- 对照基线数据资产。

---

## 9. S4 纸上交易闭环（Strict 6A）

## 9.1 存在意义

验证“信号 -> 订单 -> 持仓 -> 风控”的真实执行链路，并与 S3 回测口径对齐，防止回测与交易语义分叉。

## 9.2 组成与边界

In Scope:

- 订单状态机。
- 持仓与 T+1 冻结。
- 风控规则（20/30/80、止损8%、止盈15%）。
- 回测-交易一致性验证。

Out Scope:

- 实盘接入。
- 异常恢复演练（S6 CP07-S3）。

## 9.3 子任务分解（4个）

| 任务 | 分类 | 主要产出 | 存在理由 | 工时 |
|---|---|---|---|---:|
| S4-T1 订单管理 | 核心 | `trade_records` | 交易链路最小单元 | 1.0d |
| S4-T2 持仓/T+1 管理 | 核心 | `positions` + `t1_frozen` | A 股规则刚性要求 | 1.1d |
| S4-T3 风控引擎 | 核心 | `risk_events` | 防止执行失控 | 1.2d |
| S4-T4 口径对齐测试 | 外挂/基础设施 | parity tests | 确保回测与交易一致 | 1.2d |

## 9.4 错误处理

| 场景 | 级别 | 处理 |
|---|---|---|
| 非交易日下单 | P0 | 阻断 |
| 涨停买入/跌停卖出 | P0 | 阻断并记录 risk_event |
| T+1 违规卖出 | P0 | 阻断 |
| 风控规则冲突 | P0 | 执行更严格规则 |
| 资金不足 | P1 | 降仓或跳过 |

## 9.5 验收标准

1. `eq trade --mode paper --date {trade_date}` 可运行。
2. `trade_records/positions/risk_events` 三表可追溯。
3. 订单状态机可重放。
4. 回测-交易同信号一致性测试通过。
5. Strict 6A 文档证据齐全。

## 9.6 退出五件套

- run: `eq trade --mode paper --date {trade_date}`
- test: `pytest tests/contracts/test_trading_* tests/contracts/test_backtest_trading_signal_parity.py -q`
- artifact: `trade_records` + `positions` + `t1_frozen` + `risk_events`
- review: `Governance/specs/spiral-s4/review.md`
- sync: 最小同步 5 文件

## 9.7 产生遗产

- 纸上交易主链实现。
- 风控事件标准日志。
- 回测-交易一致性基线测试。

---

## 10. S5 GUI + 日报闭环

## 10.1 存在意义

将 L3/L4 数据转为可见、可导出、可归档的产物，支撑日常使用与复盘。

## 10.2 组成与边界

In Scope:

- Streamlit 单页 Dashboard（温度、行业、TopN、持仓）。
- 日报自动生成。
- CSV/Markdown 导出与归档。

Out Scope:

- 高级筛选（CP08-S2，留 S6 或后续）。
- 深度归因漂移（S6）。

## 10.3 子任务分解（3个）

| 任务 | 分类 | 主要产出 | 存在理由 | 工时 |
|---|---|---|---|---:|
| S5-T1 Dashboard 最小版 | 核心 | `src/gui/app.py` 可运行 | 形成用户可视入口 | 1.2d |
| S5-T2 日报生成 | 核心 | `daily_report` + markdown 文件 | 固化每日证据 | 1.0d |
| S5-T3 导出归档 | 基础设施/外挂 | CSV/MD 导出规范 | 运营可复查、可流转 | 0.8d |

## 10.4 错误处理

| 场景 | 级别 | 处理 |
|---|---|---|
| 上游表缺失 | P1 | 空态展示 + 告警 |
| 导出失败 | P2 | 重试并提示 |
| 数据刷新超时 | P2 | 回退最近快照 |

## 10.5 验收标准

1. `eq gui --date {trade_date}` 可启动。
2. 页面符合 A 股红涨绿跌。
3. `daily_report` 可生成并归档。
4. 导出文件与页面关键指标一致。

## 10.6 退出五件套

- run: `eq gui --date {trade_date}`
- test: `pytest tests/contracts/test_gui_* tests/contracts/test_analysis_* -q`
- artifact: 页面截图 + `daily_report` + 导出文件
- review: `Governance/specs/spiral-s5/review.md`
- sync: 最小同步 5 文件

## 10.7 产生遗产

- GUI 基线模板。
- 日报模板与归档命名规范。
- 面向运营的可见化入口。

---

## 11. S6 稳定化收敛闭环

## 11.1 存在意义

清债、稳态、校准。S6 目标是让系统从“能跑”转到“可持续运行”。

## 11.2 组成与边界

In Scope:

- 全链路重跑一致性。
- P0/P1 债务清偿。
- Validation 权重对照最小版（CP10-S2）。
- 归因与漂移报告（CP09-S3）。

Out Scope:

- 新功能扩张。
- 实盘接入。

## 11.3 子任务分解（4个）

| 任务 | 分类 | 主要产出 | 存在理由 | 工时 |
|---|---|---|---|---:|
| S6-T1 全链路重跑与一致性报告 | 核心 | run-all diff 报告 | 验证系统确定性 | 1.0d |
| S6-T2 债务清偿 | 核心 | debts P0/P1 清零记录 | 防技术债滚雪球 | 1.0d |
| S6-T3 CP10-S2 最小权重对照 | 核心/外挂 | baseline vs candidate 结论 | 让权重变更有证据 | 1.0d |
| S6-T4 归档与冻结全检 | 基础设施/外挂 | freeze 报告 + 里程碑归档 | 防文档/实现漂移 | 1.0d |

## 11.4 错误处理

| 场景 | 级别 | 处理 |
|---|---|---|
| run-all 前后结果不可解释漂移 | P0 | 阻断收口，回溯变更 |
| 债务项无法关闭 | P1 | 明确延期圈号与阻断影响 |
| candidate 权重不优于 baseline | P1 | 回退 baseline |
| freeze_check 失败 | P0 | 阻断并定位变更来源 |

## 11.5 验收标准

1. `eq run-all --start {start} --end {end}` 两次结果一致（允许时间戳差异）。
2. `Governance/record/debts.md` 中 P0/P1 均有处置结论。
3. `validation_weight_report` 与 `validation_weight_plan` 可追溯。
4. 归因报告可生成且输入链可追溯。
5. 冻结检查通过。

## 11.6 退出五件套

- run: `eq run-all --start {start} --end {end}`
- test: `pytest -q`（含 contracts/canary/parity）
- artifact: 一致性报告 + 债务清偿记录 + validation weight 报告 + freeze 报告
- review: `Governance/specs/spiral-s6/review.md`
- sync: 最小同步 5 文件

## 11.7 产生遗产

- 重跑一致性基线。
- 权重更新证据链。
- 可持续运营的收敛里程碑。

---

## 12. 残留风险与降级策略

1. S2 复杂度高，超时风险最大。
- 降级: 优先保 IRS/PAS + Gate；Integration 延后到 S3 不破圈。
2. Qlib 环境与本地向量化口径可能短期不一致。
- 降级: 以向量化引擎为收口基线，Qlib 作为研究旁路。
3. 交易环节最可能触发 Strict 6A 文档负担。
- 降级: 仅保最小 6A 证据，不做额外文档扩张。

---

## 13. 执行与回写建议

若你认可本稿，建议按以下顺序落地:

1. 先将本稿标记为“Approved”。
2. 将核心内容回写至 `docs/design/enhancements/eq-improvement-plan-core-frozen.md`，保持单主计划。
3. 在 `Governance/record/development-status.md` 更新当前圈为 S0 开始执行。
4. 从 S0-T1 立即开工，先拿到第一圈五件套证据。

---

## 14. 变更记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-02-10 | v1.0.0-candidate | 基于详细版路线图与仓库现状交叉校正，补齐每圈边界/错误处理/验收/遗产/工时与 Slice 预算合规约束 |
