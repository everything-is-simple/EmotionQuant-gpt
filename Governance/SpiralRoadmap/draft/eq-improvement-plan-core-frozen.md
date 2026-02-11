# EmotionQuant 改进行动主计划（核心设计冻结 + 外挂增强）

## 0. 文档信息

- 状态: 当前唯一有效主计划（覆盖 R1-R31 收敛后实施阶段）
- 最后更新: 2026-02-10
- 适用: Spiral S0-S6（与 `Governance/Capability/SPIRAL-CP-OVERVIEW.md` 严格对齐）
- 输入来源:
  - `.reports/archive-critique-r1-r31-20260210/`
  - `.reports/对标开源A股量化系统批判_20260209_150147.md`
  - `.reports/对标开源A股量化系统批判_修订版_20260209.md`
  - `.reports/对标批判响应行动计划_20260209_233929.md`
  - `.reports/EmotionQuant_行动计划_采纳批判建议_20260209_2341.md`

---

## 1. 冻结边界（大动脉不可动）

以下内容为冻结区，只能实现，不得改写语义：

1. `情绪优先` 主逻辑与“单指标不得独立决策”铁律。
2. `MSS/IRS/PAS + Validation` 核心算法语义、评分口径、门禁逻辑。
3. `Spiral + CP-01~CP-10` 主路线与五件套闭环定义。
4. 已在 R1-R31 收口的核心设计结论（字段、枚举、数据模型、信息流）。

冻结区权威源：

- `docs/design/**`
- `docs/module-index.md`
- `docs/naming-conventions.md`
- `docs/system-overview.md`
- `Governance/Capability/CP-*.md`
- `Governance/Capability/SPIRAL-CP-OVERVIEW.md`
- `Governance/steering/系统铁律.md`

---

## 2. 既定技术基线（必须遵守）

### 2.1 数据采集与配置

1. 主采集源: TuShare（5000 积分官方口径优先）。
2. 配置权威: `docs/reference/tushare/tushare-config-5000-官方.md`。
3. 密钥与路径: 仅 `Config.from_env()` 注入，禁止硬编码。
4. 数据路径原则: 远端补采 -> 本地落库 -> 主流程读取。

### 2.2 数据存储与分层

1. 存储口径: `Parquet + DuckDB`。
2. 分层口径: L1/L2/L3/L4 不反向依赖。
3. Validation 运行时结果以 DuckDB 契约为准（parquet 仅调试导出）。

### 2.3 回测与交易

1. 回测主选: `Qlib`（研究与实验）。
2. 执行基线: 本地向量化回测器（A 股规则对齐）。
3. 兼容实现: `backtrader_compat`（可选，不是主线）。
4. 交易口径: 先纸上交易，严格执行 T+1/涨跌停/交易时段。

### 2.4 GUI 与分析

1. GUI 主线: `Streamlit + Plotly`。
2. GUI 只读展示，不执行算法计算。
3. L4 产物必须可追溯到 L1-L3 输入和参数。

---

## 3. 允许变更范围（外挂白名单）

在不改核心设计文档语义的前提下，允许新增/增强：

- `src/pipeline/`（编排、参数、失败产物，不改算法公式）
- `src/adapters/`（数据/回测/交易/展示薄适配层）
- `src/data/` `src/backtest/` `src/trading/` `src/gui/`（仅按现有设计稿落地实现）
- `tests/contracts/` `tests/canary/`（契约与金丝雀）
- `scripts/quality/`（冻结检查、回归脚本）
- `docs/design/enhancements/eq-improvement-plan-core-frozen.md`（唯一执行主计划）
- `Governance/specs/spiral-s*/`、`Governance/record/*`（闭环同步）

禁止事项：

1. 修改 `docs/design/**` 核心契约含义。
2. 引入与既定技术基线冲突的替代主线（例如以其他回测引擎替代 Qlib 主选）。
3. 将技术指标对照实验结果直接接入交易触发链。

---

## 4. 外挂增强包（来自批判文件的可采纳项）

| ENH | 名称 | 目标 | 约束 |
|---|---|---|---|
| ENH-01 | 统一运行入口 | 提供一键闭环命令（按 Spiral 阶段） | 只做编排，不改评分逻辑 |
| ENH-02 | 数据预检与限流守卫 | TuShare token/频率/交易日历预检 | 必须走 Config/env |
| ENH-03 | 失败产物协议 | 统一输出 `error_manifest.json` + 输入快照 | 错误分级遵循 P0/P1/P2 |
| ENH-04 | 适配层契约测试 | data/backtest/trading/gui 接口稳定 | 不修改 CP 输入输出定义 |
| ENH-05 | 小样本金丝雀 | 10 日可复现数据包与回归测试 | 仅用于回归，不替代正式数据 |
| ENH-06 | A/B/C 对照看板 | 证明情绪主线优于技术单指标对照 | 技术指标仅对照，不入交易链 |
| ENH-07 | L4 产物标准化 | 固定报告模板、导出结构、归档规则 | 与 CP-09 指标口径一致 |
| ENH-08 | 设计冻结检查 | 关键锚点变化自动告警/失败 | 只做守卫，不改设计文档 |

---

## 5. Spiral 全流程实施路线（S0-S6）

每个 Spiral 统一闭环: `run + test + artifact + review + sync`

### S0 数据最小闭环（CP-01）

- 主目标: TuShare -> 本地 Parquet/DuckDB -> 快照可复现。
- CP 切片: `CP01-S1` `CP01-S2`。
- 外挂增强: `ENH-01` `ENH-02` `ENH-03` `ENH-05` `ENH-08`。
- 建议命令:
  - run: `eq run --date {trade_date} --source tushare`
  - test: `pytest tests/canary tests/contracts/test_data_* -q`
- 必要产物:
  - `raw_* parquet`
  - `market_snapshot`
  - `error_manifest.json`（失败场景）

### S1 MSS 闭环（CP-02 + CP-01）

- 主目标: 输出可复现 `mss_panorama`。
- CP 切片: `CP02-S1`（必要） + `CP02-S2`（可选）。
- 外挂增强: `ENH-04` `ENH-07`。
- 建议命令:
  - run: `eq mss --date {trade_date}`
  - test: `pytest tests/contracts/test_mss_* -q`
- 必要产物:
  - `mss_panorama`
  - 温度曲线基础视图（L4）

### S2 信号生成闭环（CP-03/04/10/05）

- 主目标: 形成可追溯 TopN 推荐。
- CP 切片: `CP03-S1` `CP04-S1` `CP10-S1` `CP05-S1`。
- 外挂增强: `ENH-04` `ENH-06` `ENH-07`。
- 建议命令:
  - run: `eq recommend --date {trade_date}`
  - test: `pytest tests/contracts/test_irs_* tests/contracts/test_pas_* tests/contracts/test_validation_* tests/contracts/test_integration_* -q`
- 必要产物:
  - `irs_industry_daily`
  - `stock_pas_daily`
  - `validation_gate_decision`
  - `integrated_recommendation`

### S3 回测闭环（CP-10/06/09）

- 主目标: Qlib 主线回测可复现并可对照 baseline。
- CP 切片: `CP10-S2` `CP06-S1` `CP09-S1`。
- 外挂增强: `ENH-04` `ENH-06` `ENH-07`。
- 建议命令:
  - run: `eq backtest --engine qlib --start {start} --end {end}`
  - test: `pytest tests/contracts/test_backtest_* tests/contracts/test_validation_integration_bridge.py -q`
- 必要产物:
  - `backtest_results`
  - `backtest_trade_records`
  - A/B/C 对照指标表（对照用途）

### S4 纸上交易闭环（CP-07/09）

- 主目标: 信号 -> 订单 -> 持仓 -> 风控日志可重放。
- CP 切片: `CP07-S1` `CP07-S2` `CP09-S1`。
- 外挂增强: `ENH-04` `ENH-03` `ENH-07`。
- 建议命令:
  - run: `eq trade --mode paper --date {trade_date}`
  - test: `pytest tests/contracts/test_trading_* tests/contracts/test_backtest_trading_signal_parity.py -q`
- 必要产物:
  - `trade_records`
  - `positions`
  - `risk_events`

### S5 展示闭环（CP-08/09）

- 主目标: GUI 可启动、报告可导出。
- CP 切片: `CP08-S1` `CP09-S2`。
- 外挂增强: `ENH-01` `ENH-07`。
- 建议命令:
  - run: `eq gui --date {trade_date}`
  - test: `pytest tests/contracts/test_gui_* tests/contracts/test_analysis_* -q`
- 必要产物:
  - GUI 页面截图
  - `daily_report`

### S6 稳定化闭环（全 CP）

- 主目标: 全链路重跑一致、债务与复盘闭环。
- CP 切片: 根据债务清单抽取，不改核心语义。
- 外挂增强: `ENH-08` 全量执行。
- 建议命令:
  - run: `eq run-all --start {start} --end {end}`
  - test: `pytest -q`
- 必要产物:
  - 一致性报告（重跑 diff）
  - 技术债清偿记录

---

## 6. 每圈固定闭环模板（必须执行）

1. run: 至少 1 条可复现命令。
2. test: 至少 1 条自动化测试（建议契约测试优先）。
3. artifact: 至少 1 个结构化产物（数据/报告/日志）。
4. review: `Governance/specs/spiral-s{N}/review.md`。
5. sync: 更新以下最小同步集：
   - `Governance/specs/spiral-s{N}/final.md`
   - `Governance/record/development-status.md`
   - `Governance/record/debts.md`
   - `Governance/record/reusable-assets.md`
   - `Governance/Capability/SPIRAL-CP-OVERVIEW.md`（仅状态）

---

## 7. 升级 Strict 6A 条件

命中任一条件，当前 Spiral 升级 Strict 6A：

1. 交易执行路径重大改动（CP-07）。
2. 风控规则重大改动（CP-07/09）。
3. 数据契约破坏性变更（任何 CP 输入输出字段）。
4. 新外部依赖进入主路径（如回测/交易适配器转正式）。

默认仍执行 `Scope -> Build -> Verify -> Sync`。

---

## 8. 入口文档同步规则（防漂移）

当以下事项发生时，才更新入口文档：

- 路径变更、流程变更、主计划状态变更。
- 需同步文件：`AGENTS.md`、`CLAUDE.md`、`README.md`、`README.en.md`、`WARP.md`。

不发生上述变化时，不做无效改写。

---

## 9. DoD（本计划完成标准）

1. S0-S6 每圈都有五件套证据。
2. 核心冻结检查长期通过（ENH-08）。
3. 至少 6 组契约测试稳定运行（Data/MSS/IRS/PAS/Integration/Validation/Backtest/Trading/GUI 中任取）。
4. A/B/C 对照报告持续产出，且技术指标仅作为对照证据。
5. 所有新增增强均为外挂层，不改核心设计稿语义。

---

## 10. 变更记录

| 日期 | 版本 | 变更 |
|---|---|---|
| 2026-02-10 | v2.0.0 | 基于现有 CP 与设计稿重构为“核心冻结 + 外挂增强”全流程 Spiral 路线；吸收 4 份批判/行动报告建议并收敛到唯一主计划 |
| 2026-02-10 | v1.0.0 | 首版主计划；建立 docs 统一入口，收敛分散计划 |
