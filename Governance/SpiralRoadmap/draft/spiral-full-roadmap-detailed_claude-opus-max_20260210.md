# EmotionQuant 螺旋全流程实施路线图（详细版）

**生成模型**: Claude 4.6 Opus (Max)
**生成时间**: 2026-02-10T10:30:00Z
**版本**: v1.0.0
**状态**: 待审批
**性质**: 实施路线图（基于 `eq-improvement-plan-core-frozen.md` v2.0.0 细化）

---

## 0. 本文档用途

本文档是 `eq-improvement-plan-core-frozen.md` 的**执行细化版**。主计划定义了冻结边界、技术基线、外挂白名单和 S0-S6 粗粒度路线；本文档在此基础上，为每个 Spiral 补充：

1. **组成分类**——哪些是核心实现、哪些是基础设施、哪些是外挂增强
2. **存在意义**——为什么需要这一圈，不做会怎样
3. **进入条件**——什么就绪了才能开始
4. **范围边界**——In Scope / Out Scope
5. **子任务分解**——每个任务的合理性说明
6. **错误处理策略**——本圈特有的 P0/P1/P2 场景
7. **验收标准**——怎么判定闭环
8. **退出条件**——五件套要求
9. **遗产产出**——本圈为后续圈留下什么可复用资产
10. **工时估算**——含核心/基础设施/外挂的分配比

**权威源不变**：核心设计仍以 `docs/design/**` 为准，能力包以 `Governance/Capability/CP-*.md` 为准，工作流以 `Governance/steering/6A-WORKFLOW.md` 为准。本文档不替代它们，只做实施编排。

---

## 1. 全局约束（所有 Spiral 生效）

### 1.1 冻结边界

原文见主计划 §1，此处不重复。核心一句话：**`docs/design/**` 里的公式、字段、枚举、信息流，只能照搬实现，不得改语义**。

### 1.2 螺旋闭环铁则

- 一圈 1 个主目标，1-3 个 Slice，每 Slice ≤1 天
- 五件套：`run + test + artifact + review + sync`
- 遇阻塞优先缩圈，不跨圈并行扩张
- 默认流程 `Scope → Build → Verify → Sync`；命中 Strict 6A 条件时升级

### 1.3 错误分级（全局）

- **P0**（阻断）：核心输入缺失、规则冲突、合规违规
- **P1**（降级+标记）：局部数据缺失、局部计算失败
- **P2**（重试+记录）：非关键异常

### 1.4 分支策略

- 开发分支：`feature/spiral-s{N}-{topic}`
- 合并目标：`main`（当前口径）
- 每圈收口后合并

---

## 2. S0 —— 数据最小闭环

### 2.1 存在意义

S0 是**整个系统的地基**。没有可复现的本地数据链路，后续所有算法（MSS/IRS/PAS）都无法运行。S0 的目标不是"拉全量数据"，而是证明**一条最小链路可以跑通并且输出可复现**。

如果跳过 S0 直接做算法，会导致：算法无法验证，因为没有真实格式的输入数据。

### 2.2 组成分类与工时估算

**总工时**：5 个子任务，预计 5 天

| 类别 | 内容 | 占比 | 工时 |
|------|------|------|------|
| **核心实现** | TuShareFetcher 采集链路 + DuckDB 写入 + L2 快照生成 | 50% | 2.5d |
| **基础设施** | CLI 骨架 + .env + pyproject scripts 入口 | 20% | 1d |
| **外挂增强** | ENH-01/02/03/05/08（CLI、预检、失败产物、金丝雀、冻结检查） | 30% | 1.5d |

**合理性**：基础设施和外挂占比 50% 看似偏高，但 S0 是首圈，必须搭建后续所有圈都会复用的脚手架（CLI、Config 注入、测试 fixtures、冻结检查）。后续圈的基础设施占比会大幅下降。

### 2.3 进入条件

- `pyproject.toml` 存在且 `pip install -e .` 可成功
- `Config.from_env()` 可加载（`.env` 中有 `TUSHARE_TOKEN`、`DATA_PATH`）
- Python ≥ 3.10 环境就绪

### 2.4 范围边界

**In Scope**：
- L1 原始数据采集（8 张表：raw_daily, raw_daily_basic, raw_limit_list, raw_index_daily, raw_index_member, raw_index_classify, raw_stock_basic, raw_trade_cal）
- L2 快照生成（market_snapshot, industry_snapshot 骨架）
- CLI 骨架（`eq run` 子命令）
- 金丝雀 10 日 mock 数据包
- 冻结锚点 hash 基线

**Out Scope**：
- L3 算法输出（MSS/IRS/PAS）—— 属于 S1/S2
- L4 分析报告 —— 属于 S3/S5
- 数据回填与缺口补采 —— 属于 S1+ 的 CP01-S3
- stock_gene_cache 计算 —— 属于 S2（PAS 依赖）

### 2.5 子任务分解

#### S0-T1：项目基础设施（≤1d）【基础设施】

**合理性**：后续所有圈的 `eq xxx` 命令都依赖此骨架，不做则每圈都要手动拼命令。

- 补齐 `pyproject.toml` 中 `[project.scripts]`：`eq = "src.pipeline.cli:app"`
- 创建 `src/pipeline/cli.py`：Click 或 Typer 骨架
  - 子命令占位：`eq run / eq mss / eq recommend / eq backtest / eq trade / eq gui / eq run-all`
  - 每个子命令接受 `--date`、`--source` 等基础参数
- 创建 `.env.example`：文档化 TUSHARE_TOKEN、DATA_PATH、DUCKDB_DIR 等
- ENH-08：创建 `scripts/quality/freeze_check.py`
  - 对 `docs/design/**` 核心文件生成 SHA256 锚点
  - 输出 `scripts/quality/freeze_anchors.json`
  - 后续每圈可运行此脚本验证核心设计未被篡改
- **产物**：`eq --help` 可运行；`freeze_anchors.json` 存在

#### S0-T2：交易日历与基础信息采集（≤1d）【核心实现】

**合理性**：交易日历是判断"哪天能跑"的前提；stock_basic 和 index_classify 是行业映射的前提。没有它们，后续 IRS 无法做行业聚合。

- 实现 `src/data/fetcher.py` 中 `TuShareFetcher`（或重构现有骨架）：
  - `fetch_trade_cal(start, end)` → `${PARQUET_PATH}/trade_cal/trade_cal.parquet`
  - `fetch_stock_basic()` → `${PARQUET_PATH}/stock_basic/stock_basic.parquet`
  - `fetch_index_classify()` → `${PARQUET_PATH}/index_classify/index_classify.parquet`
  - `fetch_index_member()` → `${PARQUET_PATH}/index_member/index_member.parquet`
- ENH-02：token 预检（调 TuShare 前先验证 token 有效）、频率限流（tenacity 重试 + rate limit）
- 字段严格对齐 `data-layer-data-models.md` §2.8（raw_trade_cal: cal_date, is_open, pretrade_date）、§2.7（raw_stock_basic: ts_code, name, industry, list_date）、§2.6（raw_index_classify: index_code, index_name, level, src）
- **测试**：至少 1 条 pytest（mock TuShare 返回 → 验证 parquet 存在且 schema 正确）

#### S0-T3：单日行情采集链路（≤1d）【核心实现】

**合理性**：日线行情是 MSS/IRS/PAS 全部因子的数据源头。这是系统的"血液"。

- `fetch_daily(trade_date)` → `${PARQUET_PATH}/daily/{trade_date}.parquet`
  - 字段对齐 §2.1：ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount
- `fetch_daily_basic(trade_date)` → `${PARQUET_PATH}/daily_basic/{trade_date}.parquet`
  - 字段对齐 §2.2：turnover_rate, volume_ratio, pe_ttm, pb, total_mv, circ_mv 等
- `fetch_limit_list(trade_date)` → `${PARQUET_PATH}/limit_list/{trade_date}.parquet`
  - 字段对齐 §2.3：limit 类型 U/D/Z、fc_ratio、fd_amount 等
- `fetch_index_daily(trade_date)` → `${PARQUET_PATH}/index_daily/{trade_date}.parquet`
  - 字段对齐 §2.4：指数日线
- ENH-03：任何采集失败时写 `error_manifest.json`（含 error_level P0/P1/P2、failed_api、trade_date、timestamp）
- **测试**：mock 场景 + parquet schema 校验（列名、类型）

#### S0-T4：DuckDB 写入与 L2 快照生成（≤1d）【核心实现】

**合理性**：L2 快照是 MSS 六因子的直接输入（market_snapshot 提供 rise_count、limit_up_count 等），不生成快照则 S1 无法启动。

- 实现 `src/data/repositories/` 中 Repository 类：
  - `DailyRepository.ingest(trade_date)` → 从 parquet 读取，写入 DuckDB
  - `MarketSnapshotRepository.compute_and_write(trade_date)` → 聚合生成 market_snapshot
- `market_snapshot` 字段对齐 `data-layer-data-models.md` §3.1：
  - 计数字段（23 个）：total_stocks, rise_count, fall_count, flat_count, strong_up_count, strong_down_count, limit_up_count, limit_down_count, touched_limit_up, new_100d_high_count, new_100d_low_count, continuous_limit_up_2d, continuous_limit_up_3d_plus, continuous_new_high_2d_plus, high_open_low_close_count, low_open_high_close_count
  - 统计字段：pct_chg_std, amount_volatility, yesterday_limit_up_today_avg_pct
  - 质量字段：data_quality, stale_days, source_trade_date
- `industry_snapshot` 骨架（§3.2）：至少能按行业聚合 stock_count、rise_count、industry_pct_chg（完整字段在 S2 补齐）
- DuckDB 路径：`Config.from_env().duckdb_dir`，零硬编码
- **测试**：内存 DuckDB + 字段完整性断言

#### S0-T5：端到端验证与金丝雀数据包（≤1d）【外挂增强】

**合理性**：金丝雀数据包让后续所有圈都能离线回归测试，不依赖 TuShare 网络。冻结检查确保核心设计不被意外修改。

- `eq run --date {trade_date} --source tushare` 端到端跑通
- `eq run --date {trade_date} --source mock` 使用 mock 数据跑通（离线验证）
- ENH-05：生成 `tests/fixtures/canary_10d/`
  - 包含 10 个交易日的 parquet mock 数据（daily, daily_basic, limit_list, index_daily, trade_cal, stock_basic）
  - 数据量精简但字段完整，满足后续 MSS/IRS/PAS 最小计算需求
- `tests/canary/test_data_canary.py`：使用金丝雀包做离线回归
- `tests/contracts/test_data_layer_contract.py`：验证 L1→L2 字段契约（parquet schema → DuckDB schema）
- **产物**：run 命令日志 + pytest 报告 + parquet/DuckDB 文件

### 2.6 错误处理（S0 特有场景）

| 场景 | 级别 | 处理 |
|------|------|------|
| TUSHARE_TOKEN 缺失或无效 | P0 | 阻断，提示配置 .env |
| TuShare API 超频 | P2 | tenacity 重试（最多 3 次，间隔递增） |
| 非交易日拉取无数据 | P1 | 标记 data_quality=stale，使用最近交易日 |
| parquet 写盘失败 | P0 | 阻断并记录 error_manifest.json |
| DuckDB 连接失败 | P0 | 阻断 |
| 个别股票缺失 | P1 | 跳过该股，total_stocks 不含缺失 |

### 2.7 验收标准

1. `eq run --date 20260207 --source mock` 退出码 0
2. `pytest tests/canary/ tests/contracts/test_data_* -q` 全 PASSED
3. DuckDB 中 `market_snapshot` 表存在且 `total_stocks > 0`
4. 失败场景下 `error_manifest.json` 可生成且含 error_level 字段
5. `scripts/quality/freeze_check.py` 退出码 0（锚点未变化）

### 2.8 退出条件（五件套）

1. **run**：`eq run --date {date} --source mock`
2. **test**：`pytest tests/canary/ tests/contracts/test_data_* -q`
3. **artifact**：`raw_daily parquet` + `market_snapshot DuckDB 表` + `error_manifest.json`
4. **review**：`Governance/specs/spiral-s0/review.md`
5. **sync**：development-status + debts + reusable-assets + SPIRAL-CP-OVERVIEW 状态更新

### 2.9 遗产产出（可复用资产）

| 遗产 | 消费方 | 说明 |
|------|--------|------|
| `TuShareFetcher` 类 | S1-S6 所有需要数据的圈 | 统一采集入口 |
| CLI 骨架 (`eq` 命令) | S1-S6 所有圈 | 统一运行入口 |
| `tests/fixtures/canary_10d/` | S1-S6 所有圈的离线测试 | 金丝雀数据包 |
| `freeze_anchors.json` | S6 全量冻结检查 | 设计文档锚点基线 |
| `error_manifest.json` 协议 | S4 交易失败产物 | 统一错误输出格式 |
| `market_snapshot` L2 表 | S1 MSS 六因子计算 | 直接输入 |
| `industry_snapshot` L2 骨架 | S2 IRS 行业评分 | 待 S2 补齐完整字段 |
| Repository 基类模式 | S1-S5 所有 DuckDB 写入 | 统一存储模式 |

---

## 3. S1 —— MSS 闭环

### 3.1 存在意义

MSS 是系统的**市场情绪基准**。它回答"当前市场整体情绪如何"，为 Integration 提供温度、周期、趋势、仓位建议。S1 的目标是证明**六因子 → 温度 → 周期映射这条链路可以跑通并且输出确定性可复现**。

如果跳过 S1 直接做 S2（IRS/PAS/Integration），则 Integration 三三制缺少 MSS 输入，无法生成 final_score。

### 3.2 组成分类与工时估算

**总工时**：4 个子任务，预计 4 天

| 类别 | 内容 | 占比 | 工时 |
|------|------|------|------|
| **核心实现** | 六因子引擎 + 温度/周期/趋势判定 + mss_panorama 写入 | 75% | 3d |
| **基础设施** | CLI `eq mss` 集成 + DuckDB writer | 10% | 0.5d |
| **外挂增强** | ENH-04（MSS 契约测试）+ ENH-07（L4 温度视图骨架） | 15% | 0.5d |

**合理性**：核心实现占 75% 是合理的——MSS 六因子体系有明确公式（`mss-algorithm.md` §3.1-§3.6），实现量集中在因子计算和状态判定。

### 3.3 进入条件

- **S0 已收口**：五件套齐全
- `market_snapshot` DuckDB 表可读且字段完整（rise_count, limit_up_count, pct_chg_std 等 23 个字段）
- `raw_daily` parquet 可用（MSS 波动因子需要个股 pct_chg 截面数据）
- 金丝雀数据包 `canary_10d` 可用（离线测试用）

### 3.4 范围边界

**In Scope**：
- MSS 六因子计算（大盘系数、赚钱效应、亏钱效应、连续性、极端、波动）
- 温度合成（六因子加权 → 0-100）
- 七大周期判定（emergence/fermentation/acceleration/divergence/climax/diffusion/recession）
- 趋势方向判定（up/down/sideways）
- 仓位建议映射
- 中性度计算：`neutrality = 1 - |temperature - 50| / 50`
- `mss_panorama` DuckDB 写入（字段对齐 `data-layer-data-models.md` §4.1）

**Out Scope**：
- Z-Score 基线参数的离线计算（首版使用硬编码 baseline 或全量历史统计）—— 完善版属于 S6
- IRS/PAS 因子计算 —— 属于 S2
- MSS 趋势的 WFA 滚动验证 —— 属于 S3/S6

### 3.5 子任务分解

#### S1-T1：MSS 六因子计算引擎（≤1d）【核心实现】

**合理性**：六因子是 MSS 的全部评分来源，公式已在 `mss-algorithm.md` §3.1-§3.6 明确定义，逐个实现即可。

- 创建 `src/algorithms/mss/factors.py`
- 实现 `normalize_zscore(value, mean, std) → 0-100`（统一归一化函数，MSS/IRS/PAS 共用）
- 六因子实现（每个因子：raw 计算 → Z-Score → 0-100 得分）：
  - 大盘系数（§3.1）：`rise_count / total_stocks → zscore`，权重 17%
  - 赚钱效应（§3.2）：`0.4×limit_up_ratio + 0.3×new_high_ratio + 0.3×strong_up_ratio → zscore`，权重 34%
  - 亏钱效应（§3.3）：`0.3×broken_rate + 0.2×limit_down_ratio + 0.3×strong_down_ratio + 0.2×new_low_ratio → zscore`，权重 34%
  - 连续性因子（§3.4）：`0.5×continuous_limit_up_ratio + 0.5×continuous_new_high_ratio → zscore`，权重 5%
  - 极端因子（§3.5）：`high_open_low_close_ratio + low_open_high_close_ratio → zscore`，权重 5%
  - 波动因子（§3.6）：`0.5×pct_chg_std + 0.5×amount_volatility → zscore`，权重 5%
- Z-Score 冷启动：首版使用全量金丝雀数据的 mean/std；后续由 Validation 滚动更新
- **测试**：固定 market_snapshot 输入 → 确定性六因子得分断言

#### S1-T2：温度/周期/趋势判定（≤1d）【核心实现】

**合理性**：温度是 MSS 的核心输出，周期映射决定了 Integration 中 STRONG_BUY 的附加条件。

- 创建 `src/algorithms/mss/engine.py`
- `compute_temperature(snapshot)` → 六因子加权求和（温度公式对齐 §4）：
  - `temperature = market_coefficient×0.17 + profit_effect×0.34 + (100-loss_effect)×0.34 + continuity×0.05 + extreme×0.05 + (100-volatility)×0.05`
  - 注意：loss_effect 和 volatility 取反义（越高越差，温度中用 100-score）
- `determine_cycle(temperature, trend)` → 七大周期（对齐 `data-layer-data-models.md` §4.1 的 cycle 取值说明）：
  - emergence: <30°C + up
  - fermentation: 30-45°C + up
  - acceleration: 45-60°C + up
  - divergence: 60-75°C + up/sideways
  - climax: ≥75°C
  - diffusion: 60-75°C + down
  - recession: <60°C + down/sideways
- `determine_trend(temperature_series)` → up/down/sideways（连续 N 日方向判定）
- `suggest_position(cycle)` → 仓位范围字符串
- **测试**：边界温度值（0/29/30/44/45/59/60/74/75/100）→ 期望周期映射

#### S1-T3：mss_panorama 写入与 CLI 集成（≤1d）【核心实现 + 基础设施】

**合理性**：写入 DuckDB 是闭环证据的"artifact"部分；CLI 集成让 `eq mss` 成为可复现命令。

- 创建 `src/algorithms/mss/writer.py`：写 `mss_panorama` 到 DuckDB
- 字段完整对齐 `data-layer-data-models.md` §4.1（17 个字段）：
  - id, trade_date, temperature, cycle, trend, position_advice
  - 六因子分项得分：market_coefficient, profit_effect, loss_effect, continuity_factor, extreme_factor, volatility_factor
  - neutrality, rank, percentile, created_at
- 集成到 CLI：`eq mss --date {trade_date}` → 读 market_snapshot → 计算 → 写 mss_panorama
- **测试**：DuckDB 读回 → 字段完整性 + 温度范围 [0, 100] + cycle 枚举合法

#### S1-T4：MSS 契约测试与 L4 基础视图（≤1d）【外挂增强】

**合理性**：契约测试确保 mss_panorama 输出格式稳定，不会因为后续修改而破坏 CP-05 的消费。L4 温度视图为 S5 GUI 预留数据。

- ENH-04：`tests/contracts/test_mss_contract.py`
  - 验证 mss_panorama 输出字段可被 CP-05 Integration 直接消费
  - 验证 temperature ∈ [0, 100]、cycle ∈ 七大周期、neutrality ∈ [0, 1]
- ENH-07：最小 L4 温度曲线数据
  - 将多日 mss_panorama 的 temperature 序列导出为可视化友好格式
  - 为 S5 的 Streamlit 温度仪表盘预留数据接口

### 3.6 错误处理（S1 特有场景）

| 场景 | 级别 | 处理 |
|------|------|------|
| market_snapshot 缺关键字段（rise_count 等） | P0 | 阻断，提示先完成 S0 |
| 历史窗口不足（Z-Score 统计量无法计算） | P1 | 因子得分返回 50（中性），标记 quality=cold_start |
| 单日快照为空（非交易日） | P0 | 阻断，提示检查交易日历 |
| 温度计算溢出（>100 或 <0） | P1 | 裁剪到 [0, 100] 并记录 WARN |

### 3.7 验收标准

1. `eq mss --date {date}` 退出码 0，输出 mss_panorama
2. `pytest tests/contracts/test_mss_* -q` 全 PASSED
3. DuckDB 中 mss_panorama 表 temperature ∈ [0, 100]
4. 同一输入两次运行，输出完全一致（确定性）
5. 单指标不触发交易决策——mss_panorama 仅含温度/周期/趋势/仓位建议，无买卖信号

### 3.8 退出条件（五件套）

1. **run**：`eq mss --date {date}`
2. **test**：`pytest tests/contracts/test_mss_* -q`
3. **artifact**：`mss_panorama` DuckDB 表
4. **review**：`Governance/specs/spiral-s1/review.md`
5. **sync**：更新 5 处治理文档

### 3.9 遗产产出

| 遗产 | 消费方 | 说明 |
|------|--------|------|
| `normalize_zscore()` 函数 | S2 IRS/PAS 因子归一化 | 三系统共用 |
| `mss_panorama` L3 表 | S2 Integration 输入 | MSS → CP-05 |
| MSS 因子计算模式 | S2 IRS/PAS 参考 | 相似的 factors.py + engine.py 结构 |
| 冷启动中性值策略 | S2 IRS/PAS 冷启动 | 因子缺 baseline 时返回 50 |

---

## 4. S2 —— 信号生成闭环

### 4.1 存在意义

S2 是系统**核心信号链**的完成。它将 MSS（市场层）+ IRS（行业层）+ PAS（个股层）通过 Validation Gate 和 Integration 三三制融合为最终推荐。S2 完成后，系统才具备"给出买什么"的能力。

这是所有圈中**任务最重、复杂度最高**的一圈，因为同时涉及 4 个 CP（IRS/PAS/Validation/Integration），但每个只取最小 Slice。

### 4.2 组成分类与工时估算

**总工时**：5 个子任务，预计 5-6 天

| 类别 | 内容 | 占比 | 工时 |
|------|------|------|------|
| **核心实现** | IRS 六因子 + PAS 三因子 + Validation Gate + Integration 三三制 | 80% | 4d |
| **基础设施** | CLI `eq recommend` + industry_snapshot 补齐 + stock_gene_cache | 10% | 0.5d |
| **外挂增强** | ENH-04（4 组契约测试）+ ENH-06（A/B/C 对照骨架） | 10% | 0.5-1d |

**合理性**：核心占 80% 是因为 IRS 有 6 个因子（相对强度/连续性/资金流向/估值/龙头/基因库，权重 25/20/20/15/12/8），PAS 有 3 个因子（牛股基因/结构位置/行为确认，权重 20/50/30），Validation 有 IC/ICIR 计算，Integration 有 Gate+加权+方向一致性。每个都有明确公式但实现量不小。

**风险**：S2 可能超 7 天。应对策略：如果 IRS+PAS 超时，优先保证 IRS 最小版 + PAS 最小版 + Integration baseline 等权，Validation 降级为"始终返回 PASS + baseline 权重"的 stub。

### 4.3 进入条件

- **S1 已收口**：mss_panorama 可用
- `market_snapshot` 完整（S0 产出）
- `industry_snapshot` 骨架可用（S0 产出，S2 内补齐完整字段）
- `raw_daily`, `raw_daily_basic`, `raw_limit_list`, `raw_index_daily` 可用
- `raw_stock_basic`, `raw_index_classify`, `raw_index_member` 可用

### 4.4 范围边界

**In Scope**：
- IRS 六因子最小版（CP03-S1）：31 行业评分 + 排名 + 轮动状态 + 配置建议
- PAS 三因子最小版（CP04-S1）：个股评分 + 等级 + 方向 + 风险收益比
- Validation 因子最小门禁（CP10-S1）：IC/RankIC/ICIR + Gate 决策
- Integration 三三制（CP05-S1）：baseline 等权融合 + 方向一致性 + 推荐等级
- `industry_snapshot` 完整字段补齐
- `stock_gene_cache` 计算（PAS 牛股基因因子的数据源）

**Out Scope**：
- IRS 稳定性增强（CP03-S2）—— 属于 S3/S6
- PAS 等级/方向/执行字段增强（CP04-S2）—— 属于 S3/S6
- Validation 权重 Walk-Forward（CP10-S2）—— 属于 S3
- Integration 风险约束接入（CP05-S2）—— 属于 S3
- 回测 —— 属于 S3

### 4.5 子任务分解

#### S2-T1：IRS 行业评分最小版（≤1d）【核心实现】

**合理性**：IRS 提供行业层信号，是三三制的 1/3。31 行业必须全覆盖。

- 创建 `src/algorithms/irs/engine.py`
- 补齐 `industry_snapshot` 完整字段（对齐 §3.2：stock_count, rise_count, fall_count, industry_pct_chg, industry_amount, industry_turnover, industry_pe_ttm, industry_pb, limit_up_count, new_100d_high_count, new_100d_low_count, top5_codes, top5_pct_chg, top5_limit_up）
- 六因子实现（对齐 `irs-algorithm.md` §3.1-§3.6）：
  - 相对强度（25%）：`industry_pct_chg - benchmark_pct_chg → zscore`
  - 连续性（20%）：`0.6×Σ(net_breadth,5d) + 0.4×Σ(net_new_high,5d) → zscore`
  - 资金流向（20%）：`Σ(industry_amount_delta, 10d) → zscore`
  - 估值（15%）：`-industry_pe_ttm → zscore`（PE 越低越优）
  - 龙头（12%）：`0.6×top5_avg_pct + 0.4×top5_limit_up_ratio → zscore`
  - 基因库（8%）：`time_decay(history_limit_up_ratio) → zscore`
- 综合评分 → 排名 → rotation_status（IN/OUT/HOLD）→ allocation_advice（超配/标配/减配/回避）
- 输出写入 `irs_industry_daily` DuckDB 表（对齐 §4.2：19 个字段）
- quality_flag + sample_days 输出（冷启动/陈旧识别）
- **测试**：固定 industry_snapshot → 确定性排名

#### S2-T2：PAS 个股评分最小版（≤1d）【核心实现】

**合理性**：PAS 提供个股层信号，是三三制的 1/3。

- 创建 `src/algorithms/pas/engine.py`
- 先完成 `stock_gene_cache` 计算（对齐 §3.3：limit_up_count_120d, new_high_count_60d, max_pct_chg_history）
- 三因子实现（对齐 `pas-algorithm.md` §3.1-§3.3）：
  - 牛股基因（20%）：`0.4×limit_up_120d_ratio + 0.3×new_high_60d_ratio + 0.3×max_pct_chg_ratio → zscore`
  - 结构位置（50%）：`0.4×price_position + 0.3×trend_continuity_ratio + 0.3×breakout_strength → zscore`
  - 行为确认（30%）：`0.4×volume_ratio_norm + 0.3×pct_chg_norm + 0.3×limit_up_flag → zscore`
- 机会等级映射（§5.1）：S(≥85)/A([70,85))/B([55,70))/C([40,55))/D(<40)
- 方向判断（§5.2）：`close > high_20d_prev && consecutive_up_days ≥ 3` → bullish
- 风险收益比（§6）：entry/stop/target 计算
- 输出写入 `stock_pas_daily` DuckDB 表（对齐 §4.3）
- **测试**：固定个股数据 → 确定性评分 + 等级

#### S2-T3：Validation 因子最小门禁（≤1d）【核心实现】

**合理性**：Validation Gate 是 Integration 的前置必需。没有 Gate，Integration 不知道该用 baseline 还是 candidate 权重。最小版先做"因子门禁"，权重 Walk-Forward 在 S3。

- 创建 `src/validation/engine.py`
- 因子验证最小版（对齐 `factor-weight-validation-algorithm.md` §3）：
  - IC（Pearson 相关系数均值）
  - RankIC（Spearman 秩相关均值）
  - ICIR（mean_ic / std(ic)）
  - positive_ic_ratio
- Gate 决策（对齐 §5）：
  - 任一核心输入缺失 → FAIL
  - 因子 FAIL → FAIL
  - 因子 WARN → WARN
  - 因子 PASS → PASS（最小版暂不做权重验证，权重始终 baseline）
- 输出 `validation_gate_decision` + `validation_weight_plan`（最小版：selected_weight_plan 始终为 "baseline"）
- **测试**：构造 PASS/WARN/FAIL 三种场景的因子数据

#### S2-T4：Integration 三三制集成（≤1d）【核心实现】

**合理性**：Integration 是系统的汇聚点，将三子系统融合为最终信号。

- 创建 `src/integration/engine.py`
- `resolve_gate_and_weights()`（对齐 `integration-algorithm.md` §3.1）：
  - FAIL → 抛 ValidationGateError
  - irs_quality_flag ∈ {cold_start, stale} → 强制 baseline + WARN
  - PASS/WARN → 根据 selected_weight_plan 选权重
- 三三制加权（§3.2）：`final_score = mss×w_mss + irs×w_irs + pas×w_pas`
- 方向一致性（§4）：三者方向编码 → consistency_factor
- 推荐等级（§5）：STRONG_BUY(≥75 + emergence/fermentation) / BUY(≥70) / HOLD(50-69) / SELL(30-49) / AVOID(<30)
- 仓位建议计算
- 输出写入 `integrated_recommendation` DuckDB 表（对齐 §4.4：28 个字段）
- **测试**：固定三系统输入 → 确定性 final_score + recommendation

#### S2-T5：端到端信号链路与契约测试（≤1d）【基础设施 + 外挂增强】

**合理性**：端到端验证确保 MSS→IRS→PAS→Validation→Integration 全链路可跑通。

- `eq recommend --date {date}` 编排：读数据 → MSS → IRS → PAS → Validation → Integration → 输出 TopN
- ENH-04（4 组契约测试）：
  - `test_irs_contract.py`：irs_industry_daily 输出可被 CP-05 消费
  - `test_pas_contract.py`：stock_pas_daily 输出可被 CP-05 消费
  - `test_validation_contract.py`：validation_gate_decision 格式正确
  - `test_integration_contract.py`：integrated_recommendation 字段完整
- ENH-06 骨架：记录 A 组（情绪主线）TopN 产出的 stock_code + final_score

### 4.6 错误处理（S2 特有场景）

| 场景 | 级别 | 处理 |
|------|------|------|
| mss_panorama 不存在 | P0 | 阻断，提示先完成 S1 |
| industry_snapshot 行业覆盖 < 31 | P1 | 缺失行业标记 quality_flag=stale |
| IRS 估值因子样本不足 8 只 | P1 | 沿用前值，标记 quality_flag=cold_start |
| PAS 个股停牌/无行情 | P1 | 跳过，不纳入评分 |
| Validation Gate = FAIL | P0 | 不进入 Integration，当日无推荐 |
| Integration 权重方案缺失 | P1 | 回退 baseline 等权 |

### 4.7 验收标准

1. `eq recommend --date {date}` 输出 TopN 推荐列表
2. `irs_industry_daily` 覆盖 31 行业
3. `stock_pas_daily` 评分 ∈ [0, 100]、等级 ∈ {S,A,B,C,D}
4. `validation_gate_decision` 可输出 PASS/WARN/FAIL
5. `integrated_recommendation` 的 final_score 可追溯到 mss_score + irs_score + pas_score
6. 4 组契约测试全 PASSED

### 4.8 退出条件（五件套）

1. **run**：`eq recommend --date {date}`
2. **test**：`pytest tests/contracts/test_irs_* test_pas_* test_validation_* test_integration_* -q`
3. **artifact**：`irs_industry_daily` + `stock_pas_daily` + `validation_gate_decision` + `integrated_recommendation`
4. **review**：`Governance/specs/spiral-s2/review.md`
5. **sync**：更新 5 处治理文档

### 4.9 遗产产出

| 遗产 | 消费方 | 说明 |
|------|--------|------|
| `integrated_recommendation` L3 表 | S3 回测 / S4 交易 / S5 GUI | 系统核心输出 |
| `irs_industry_daily` L3 表 | S5 GUI 行业热力图 | 行业层信号 |
| `stock_pas_daily` L3 表 | S5 GUI 个股列表 | 个股层信号 |
| `validation_gate_decision` L3 表 | S3 权重 WFA / S4 交易门禁 | Gate 决策 |
| `stock_gene_cache` L2 表 | PAS 每日更新 | 牛股基因缓存 |
| A 组 TopN 基线记录 | S3 A/B/C 对照 | ENH-06 骨架 |

---

## 5. S3 —— 回测闭环

### 5.1 存在意义

S3 证明系统的信号**在历史数据上是否有效**。没有回测，所有评分都只是"看上去合理"。S3 还引入 A/B/C 对照，用数据证明情绪主线优于随机和等权。

### 5.2 组成分类与工时估算

**总工时**：4 个子任务，预计 4 天

| 类别 | 内容 | 占比 | 工时 |
|------|------|------|------|
| **核心实现** | 向量化回测器 + 绩效指标 | 50% | 2d |
| **基础设施** | Qlib 适配层 + CLI `eq backtest` | 25% | 1d |
| **外挂增强** | ENH-06（A/B/C 对照）+ ENH-07（报告模板） | 25% | 1d |

### 5.3 进入条件

- **S2 已收口**：integrated_recommendation 可用
- `raw_daily` + `raw_trade_cal` 可用（回测需要行情和交易日历）
- Config 中回测参数可读（backtest_initial_cash, commission_rate, stamp_duty_rate 等）

### 5.4 范围边界

**In Scope**：
- 本地向量化回测器（主执行基线）：T+1、涨跌停、佣金/印花税/过户费
- Qlib 适配层（信号格式转换）
- 绩效指标最小版（年化收益、最大回撤、Sharpe、Calmar、胜率、盈亏比）
- Validation 权重 Walk-Forward 骨架（CP10-S2）
- A/B/C 三组对照

**Out Scope**：
- backtrader 兼容适配 —— 属于 S6 可选
- 回测-交易偏差对齐 —— 属于 S4
- 深度归因分析 —— 属于 S5/S6

### 5.5 子任务分解

#### S3-T1：本地向量化回测器（≤1d）【核心实现】

**合理性**：这是系统的"执行基线"回测器，对齐 A 股真实规则。

- 创建 `src/backtest/vectorized_engine.py`
- 输入：`integrated_recommendation` + `raw_daily` + `raw_trade_cal`
- A 股规则对齐：
  - T+1 交割（今日买入明日才能卖出）
  - 涨跌停限制（主板±10%、创业板±20%、ST±5%）
  - 整手限制（100 股为 1 手）
- 费用对齐 Config：佣金(0.03%)、印花税(0.1% 卖方)、过户费(0.002%)、最低佣金(5 元)
- 输出 `backtest_results` + `backtest_trade_records` 写入 DuckDB
- **测试**：固定信号 + 固定行情 → 确定性净值曲线

#### S3-T2：Qlib 适配层（≤1d）【基础设施】

**合理性**：Qlib 是回测主选平台（研究用途），但其信号格式与本系统不同，需要薄适配层。

- 创建 `src/adapters/qlib_adapter.py`
- `to_qlib_signal(integrated_recommendation) → Qlib 格式`
- `from_qlib_result(qlib_output) → backtest_results 标准格式`
- **测试**：格式转换正确性

#### S3-T3：绩效指标最小版（≤1d）【核心实现】

**合理性**：没有指标就无法评估策略好坏。公式对齐 `analysis-algorithm.md` §2。

- 创建 `src/analysis/metrics.py`
- 收益指标：total_return, annual_return
- 风险指标：max_drawdown, volatility
- 风险调整：sharpe_ratio, sortino_ratio, calmar_ratio
- 交易统计：win_rate, profit_factor, avg_holding_days
- 输出 `performance_metrics` 写入 DuckDB
- ENH-07：Markdown 报告模板
- **测试**：已知净值序列 → 确定性指标值

#### S3-T4：A/B/C 对照与端到端验证（≤1d）【外挂增强】

**合理性**：A/B/C 对照是"情绪主线有效性"的核心证据。

- ENH-06：
  - A 组：情绪主线（integrated_recommendation → 向量化回测）
  - B 组：纯随机 baseline（等概率随机选股，仓位等权）
  - C 组：等权 benchmark（沪深 300 等权买入持有）
  - 输出对照表：三组的年化收益、最大回撤、Sharpe
  - **铁律**：技术指标仅对照，不入交易链
- `eq backtest --engine vectorized --start {start} --end {end}` 可运行

### 5.6 错误处理（S3 特有场景）

| 场景 | 级别 | 处理 |
|------|------|------|
| 信号与行情日期错位 | P0 | 阻断 |
| 个别标的无行情数据 | P1 | 跳过并记录 |
| 净值为 0 或负值 | P0 | 阻断，检查费用/止损逻辑 |
| Qlib 未安装 | P2 | 跳过 Qlib 回测，仅用向量化引擎 |

### 5.7 验收标准

1. `eq backtest` 输出 `backtest_results` 且指标完整
2. T+1 和涨跌停规则有自动化测试
3. A/B/C 对照表可生成
4. `performance_metrics` 可追溯到 `backtest_trade_records`

### 5.8 退出条件（五件套）

1. **run**：`eq backtest --engine vectorized --start {start} --end {end}`
2. **test**：`pytest tests/backtest/ tests/analysis/ -q`
3. **artifact**：`backtest_results` + `performance_metrics` + A/B/C 对照表
4. **review**：`Governance/specs/spiral-s3/review.md`
5. **sync**：更新 5 处治理文档

### 5.9 遗产产出

| 遗产 | 消费方 | 说明 |
|------|--------|------|
| `vectorized_engine` | S4 回测-交易口径对齐 | 执行基线 |
| `qlib_adapter` | 后续 Qlib 研究实验 | 薄适配层 |
| `metrics.py` | S4 交易绩效 / S5 日报 | 共用指标计算 |
| `performance_metrics` L4 表 | S5 GUI / 日报 | 绩效数据 |
| A/B/C 对照结果 | S5 GUI 对照看板 | 情绪主线证据 |

---

## 6. S4 —— 纸上交易闭环

### 6.1 存在意义

S4 将信号从"历史回测"推进到"模拟实盘"。它验证的是**信号→订单→持仓→风控**的完整交易流程，并与 S3 回测口径对齐，确保"回测怎么算，交易就怎么执行"。

**注意**：S4 触发 Strict 6A 条件（交易执行路径重大改动），需要更严格的审查。

### 6.2 组成分类与工时估算

**总工时**：4 个子任务，预计 4 天

| 类别 | 内容 | 占比 | 工时 |
|------|------|------|------|
| **核心实现** | 订单管理 + 持仓管理 + 风控引擎 | 60% | 2.5d |
| **基础设施** | CLI `eq trade` + 交易日志 | 15% | 0.5d |
| **外挂增强** | ENH-03（失败产物）+ ENH-04（交易契约）+ 口径对齐测试 | 25% | 1d |

### 6.3 进入条件

- **S3 已收口**：回测可复现
- `integrated_recommendation` 可用
- Config 中交易参数可读（max_position_pct, stop_loss_pct 等）

### 6.4 范围边界

**In Scope**：
- 信号转化（integrated_recommendation → TradeSignal）
- 订单状态机（pending → filled → closed）
- T+1 冻结管理
- 风控规则（单股仓位20%、行业30%、总仓位80%、止损8%、止盈15%）
- 回测-交易口径一致性验证

**Out Scope**：
- 实盘接入 —— 不在 S0-S6 范围内
- 异常恢复与稳定性（CP07-S3）—— 属于 S6

### 6.5 子任务分解

#### S4-T1：订单与持仓管理（≤1d）【核心实现】

- `src/trading/order_manager.py`：信号转订单（对齐 `trading-algorithm.md` §2）+ 状态机
- `src/trading/position_manager.py`：T+1 冻结 + 持仓更新
- 输出：`trade_records` + `positions` + `t1_frozen`

#### S4-T2：风控规则引擎（≤1d）【核心实现】

- `src/trading/risk_manager.py`：全部 5 项风控（对齐 `trading-algorithm.md` §3.1）
- 所有阈值从 Config 注入
- 输出：`risk_events`

#### S4-T3：纸上交易编排与日志（≤1d）【核心实现 + 基础设施】

- `eq trade --mode paper --date {date}` 全流程编排
- ENH-03：交易失败时 error_manifest.json

#### S4-T4：回测-交易口径对齐验证（≤1d）【外挂增强】

- `test_backtest_trading_signal_parity.py`：同一信号，向量化回测器和纸上交易的成交逻辑一致

### 6.6 错误处理（S4 特有场景）

| 场景 | 级别 | 处理 |
|------|------|------|
| 非交易日下单 | P0 | 阻断 |
| 涨停买入/跌停卖出 | P0 | 阻断，记录 risk_event |
| T+1 违规（当日买入当日卖出） | P0 | 阻断 |
| 风控规则冲突（多条同时触发） | P1 | 采用更严格规则 |
| 资金不足 | P1 | 降低仓位或跳过 |

### 6.7 验收标准

1. `eq trade --mode paper --date {date}` 退出码 0
2. T+1 冻结规则有自动化测试（当日买入当日卖出 → 阻断）
3. 5 项风控规则各有至少 1 条触发测试
4. 同一信号经回测器和纸上交易，成交价/数量一致（口径对齐）
5. `error_manifest.json` 在交易失败时可正确生成

### 6.8 退出条件（五件套）

1. **run**：`eq trade --mode paper --date {date}`
2. **test**：`pytest tests/trading/ tests/contracts/test_backtest_trading_* -q`
3. **artifact**：`trade_records` + `positions` + `risk_events` + `error_manifest.json`
4. **review**：`Governance/specs/spiral-s4/review.md`（Strict 6A 级别）
5. **sync**：更新 5 处治理文档

### 6.9 遗产产出

| 遗产 | 消费方 | 说明 |
|------|--------|------|
| `trade_records` / `positions` | S5 GUI 持仓展示 | 交易数据 |
| `risk_events` | S5 GUI 风控概览 | 风控日志 |
| 口径对齐测试 | S6 稳定化验证 | 回测-交易一致性基线 |

---

## 7. S5 —— 展示闭环

### 7.1 存在意义

S5 是系统的**用户界面层**。前 4 圈产出了数据、信号、回测、交易，但都是 DuckDB 里的表。S5 将它们转化为可视化 dashboard 和可导出的日报，让人能"看得见"。

### 7.2 组成分类与工时估算

**总工时**：3 个子任务，预计 3 天

| 类别 | 内容 | 占比 | 工时 |
|------|------|------|------|
| **核心实现** | Streamlit Dashboard + 日报生成 | 60% | 2d |
| **基础设施** | CLI `eq gui` + 导出/归档 | 20% | 0.5d |
| **外挂增强** | ENH-01（GUI 命令）+ ENH-07（报告标准化） | 20% | 0.5d |

### 7.3 进入条件

- **S4 已收口**（或至少 S3 已收口——GUI 可先展示回测结果，不强制依赖 S4 交易）
- `mss_panorama` + `irs_industry_daily` + `integrated_recommendation` 可用
- Streamlit + Plotly 已安装

### 7.4 范围边界

**In Scope**：
- 单页 Dashboard（温度仪表盘 + 行业热力图 + TopN 推荐 + 持仓概览）
- 自动日报生成（Markdown）
- 导出（CSV）与归档

**Out Scope**：
- 高级筛选（CP08-S2）—— 属于 S6
- 归因与漂移报告（CP09-S3）—— 属于 S6

### 7.5 子任务分解

#### S5-T1：Streamlit Dashboard 最小版（≤1d）【核心实现】

- `src/gui/app.py`：温度仪表盘（对齐 `gui-algorithm.md` §2.1 色彩分级）+ 行业热力图 + TopN 列表
- GUI 只读展示，数据全部从 DuckDB 读取
- A 股色彩：红涨绿跌

#### S5-T2：自动日报生成（≤1d）【核心实现】

- `src/analysis/report.py`：日报模板对齐 ENH-07
- 数据来源：mss_panorama + irs_industry_daily + integrated_recommendation + performance_metrics
- 输出：`daily_report` DuckDB 表 + `.reports/analysis/` Markdown 文件

#### S5-T3：导出与归档（≤1d）【基础设施 + 外挂增强】

- Dashboard CSV 导出
- 报告归档命名：`{report_name}_{YYYYMMDD}_{HHMMSS}.md`
- `eq gui --date {date}` 可启动

### 7.6 错误处理（S5 特有场景）

| 场景 | 级别 | 处理 |
|------|------|------|
| DuckDB 表不存在（前置圈未完成） | P0 | 阻断，提示先完成对应 Spiral |
| mss_panorama 为空（无数据日） | P1 | Dashboard 显示"暂无数据"占位 |
| Streamlit 启动端口被占用 | P2 | 自动尝试下一端口 |
| Plotly 渲染超时（数据量过大） | P2 | 限制展示最近 60 个交易日 |
| 日报模板字段缺失 | P1 | 缺失字段显示 N/A，不阻断生成 |

### 7.7 验收标准

1. `eq gui --date {date}` 可启动 Streamlit 服务
2. Dashboard 包含 4 个区域：温度仪表盘、行业热力图、TopN 推荐、持仓概览
3. 日报 Markdown 可生成且包含 MSS 温度 + 行业 Top3 + TopN 推荐
4. CSV 导出功能可用
5. 红涨绿跌色彩规范正确

### 7.8 退出条件（五件套）

1. **run**：`eq gui --date {date}`
2. **test**：`pytest tests/gui/ tests/analysis/test_report_* -q`
3. **artifact**：Dashboard 截图 + `daily_report` DuckDB 表 + `.reports/analysis/` Markdown
4. **review**：`Governance/specs/spiral-s5/review.md`
5. **sync**：更新 5 处治理文档

### 7.9 遗产产出

| 遗产 | 消费方 | 说明 |
|------|--------|------|
| `daily_report` L4 表 | 用户 / 治理 | 日度分析 |
| Dashboard 模板 | S6 稳定化 | GUI 基线 |
| 报告归档规范 | 长期运营 | `.reports/` 归档结构 |

---

## 8. S6 —— 稳定化闭环

### 8.1 存在意义

S6 是**收敛圈**。前 5 圈快速迭代可能留下技术债、边界 case、覆盖率缺口。S6 的目标是全链路重跑一致、债务清零、覆盖率达标、冻结检查通过。S6 完成后系统进入"可运营"状态。

### 8.2 组成分类与工时估算

**总工时**：4 个子任务，预计 4 天

| 类别 | 内容 | 占比 | 工时 |
|------|------|------|------|
| **核心实现** | 全链路重跑 + 覆盖率补齐 | 50% | 2d |
| **基础设施** | 文档同步 + 里程碑 tag | 25% | 1d |
| **外挂增强** | ENH-08（全量冻结检查） | 25% | 1d |

### 8.3 进入条件

- **S5 已收口**：GUI + 日报可用
- S0-S5 所有五件套齐全

### 8.4 范围边界

**In Scope**：
- 全链路重跑一致性（`eq run-all`）
- P0/P1 技术债清偿
- 测试覆盖率补齐（核心≥80%、基础设施≥70%、GUI≥50%）
- 全量冻结检查
- 全部治理文档同步

**Out Scope**：
- 新功能开发 —— S6 只修不加
- 实盘接入

### 8.5 子任务分解

#### S6-T1：全链路重跑一致性（≤1d）【核心实现】

- `eq run-all --start {start} --end {end}` 跑通
- 两次运行输出 diff → 一致性报告（所有表的行数、关键字段 hash）

#### S6-T2：债务清偿与 TODO 清理（≤1d）【核心实现】

- 扫描 TODO/HACK/FIXME
- 清偿 `Governance/record/debts.md` 中所有 P0/P1 项

#### S6-T3：覆盖率补齐与门禁全检（≤1d）【外挂增强】

- pytest --cov 达到分级目标
- ENH-08：`scripts/quality/freeze_check.py` 全量执行

#### S6-T4：文档同步与里程碑（≤1d）【基础设施】

- 更新全部 `Governance/record/*`
- 更新 SPIRAL-CP-OVERVIEW 所有状态
- 更新入口文档（AGENTS.md, CLAUDE.md, WARP.md, README.md）
- 打 tag：`v0.1.0-spiral-s6`

### 8.6 错误处理（S6 特有场景）

| 场景 | 级别 | 处理 |
|------|------|------|
| 全链路两次运行输出不一致 | P0 | 阻断，定位非确定性源（随机种子/时间戳/浮点精度） |
| 冻结检查发现设计文档被修改 | P0 | 阻断，恢复到锚点版本或走 6A 变更流程 |
| 覆盖率未达分级目标 | P1 | 补写测试，标记为 S6 债务 |
| TODO/HACK/FIXME 残留 | P1 | 清偿或升级为正式 issue |
| 治理文档状态与实际不一致 | P1 | 修正文档，不修改代码 |

### 8.7 验收标准

1. `eq run-all --start {start} --end {end}` 两次运行输出完全一致
2. `Governance/record/debts.md` 中 P0/P1 项全部清零
3. pytest --cov 核心模块 ≥80%、基础设施 ≥70%、GUI ≥50%
4. `scripts/quality/freeze_check.py` 全量通过
5. SPIRAL-CP-OVERVIEW 所有 CP 状态与实际代码一致
6. `v0.1.0-spiral-s6` tag 已打

### 8.8 退出条件（五件套）

1. **run**：`eq run-all --start {start} --end {end}`
2. **test**：`pytest --cov -q`（全量）
3. **artifact**：一致性报告 + 覆盖率报告 + 冻结检查报告
4. **review**：`Governance/specs/spiral-s6/review.md`
5. **sync**：全部 `Governance/record/*` + 入口文档 + tag

### 8.9 遗产产出

| 遗产 | 消费方 | 说明 |
|------|--------|------|
| 一致性报告 | 长期运营 | 重跑基线 |
| 覆盖率报告 | 长期运营 | 质量基线 |
| v0.1.0 tag | 后续迭代 | 里程碑 |

---

## 9. 全局工时汇总与合理性评估

| Spiral | 子任务数 | 预计工时 | 核心 | 基础设施 | 外挂 |
|--------|----------|----------|------|----------|------|
| S0 数据 | 5 | 5d | 50% | 20% | 30% |
| S1 MSS | 4 | 4d | 75% | 10% | 15% |
| S2 信号 | 5 | 5-6d | 80% | 10% | 10% |
| S3 回测 | 4 | 4d | 50% | 25% | 25% |
| S4 交易 | 4 | 4d | 60% | 15% | 25% |
| S5 展示 | 3 | 3d | 60% | 20% | 20% |
| S6 稳定 | 4 | 4d | 50% | 25% | 25% |
| **合计** | **29** | **29-30d** | **~61%** | **~18%** | **~21%** |

**合理性评估**：

- **总量 29-30 天**：按 7 天/圈计算约 4-5 周，个人开发节奏合理
- **核心占 61%**：超过一半精力用于实现冻结设计，符合"核心不动只落地"原则
- **S0 外挂占 30%**：首圈搭建脚手架偏高但必要，后续圈外挂占比降至 10-25%
- **S2 最重（5-6d）**：同时涉及 4 个 CP，是风险最高的一圈；应对策略是 Validation 可先用 stub
- **S5 最轻（3d）**：GUI 只读展示，复杂度低
- **每个 Task ≤ 1 天**：符合铁则要求

---

## 10. 设计权威文档索引

每个 Spiral 实现时，必须对照以下权威源：

| 模块 | 权威文档路径 | 关键章节 |
|------|-------------|----------|
| Data Layer | `docs/design/core-infrastructure/data-layer/data-layer-data-models.md` | §2 L1 字段、§3 L2 快照字段 |
| Data Layer API | `docs/design/core-infrastructure/data-layer/data-layer-api.md` | §2 TuShareClient、§3 DataFetcher |
| MSS | `docs/design/core-algorithms/mss/mss-algorithm.md` | §2 六因子、§3 公式、§4 温度 |
| IRS | `docs/design/core-algorithms/irs/irs-algorithm.md` | §2 六因子、§3 公式、§5 轮动 |
| PAS | `docs/design/core-algorithms/pas/pas-algorithm.md` | §2 三因子、§3 公式、§5 等级 |
| Validation | `docs/design/core-infrastructure/validation/factor-weight-validation-algorithm.md` | §3 因子验证、§5 Gate |
| Integration | `docs/design/core-algorithms/integration/integration-algorithm.md` | §3 三三制、§4 一致性、§5 推荐 |
| Backtest | `docs/design/core-infrastructure/backtest/backtest-engine-selection.md` | §1 决策、§3 边界 |
| Trading | `docs/design/core-infrastructure/trading/trading-algorithm.md` | §2 信号、§3 风控 |
| Analysis | `docs/design/core-infrastructure/analysis/analysis-algorithm.md` | §2 绩效、§4 归因 |
| GUI | `docs/design/core-infrastructure/gui/gui-algorithm.md` | §2 分级、§3 排序、§4 过滤 |
| 命名规范 | `docs/naming-conventions.md` | §1-5 周期/趋势/推荐/等级/方向 |

---

## 变更记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-02-10 | v1.0.0 | 基于 `eq-improvement-plan-core-frozen.md` v2.0.0 细化为详细版实施路线图；补充每个 Spiral 的分类/进出条件/边界/错误处理/验收/遗产/工时 |
