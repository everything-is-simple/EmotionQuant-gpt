# EmotionQuant S0-S2 真螺旋执行路线图（执行版 v0.2）

**状态**: Candidate  
**更新时间**: 2026-02-13  
**适用范围**: S0-S2（数据层到 MSS+IRS 最小推荐闭环）  
**文档角色**: 执行分解稿（不是上位 SoT 替代）

---

## 0. 文档定位（先对齐 SoT）

冲突处理原则（从高到低）：

1. `docs/design/enhancements/eq-improvement-plan-core-frozen.md`（执行基线）
2. `Governance/Capability/SPIRAL-CP-OVERVIEW.md`（能力路线）
3. `Governance/steering/6A-WORKFLOW.md` + `Governance/steering/系统铁律.md`
4. 本文件（S0-S2 执行分解）

本文件只做两件事：

- 把 S0-S2 拆成可收口微圈
- 把每圈 run/test/artifact/review/sync 写成可审计合同

---

## 1. 现实基线快照（As-Is）

截至 2026-02-13 仓库事实：

1. `eq` 命令入口尚未落地（`pyproject.toml` 未定义 `project.scripts.eq`）
2. 可稳定执行的测试主路径为 `tests/unit/*`
3. `.venv` 环境可用，`pytest -q` 可全绿

因此执行口径分为两层：

- `baseline command`：当前仓库立即可执行，用于圈前健康检查
- `target command`：该圈完成后必须可执行，用于收口

---

## 2. 收口定义（硬门禁）

每个微圈必须满足 5 件套，否则不能标记完成：

1. `run`: 核心命令成功
2. `test`: 自动化测试通过
3. `artifact`: 产物可定位
4. `review`: 复盘完成
5. `sync`: 最小 5 文件同步完成

附加强制项（执行增强）：

- `consumption`: 记录“谁消费/怎么消费/消费结论”
- `gate`: 门禁结论（PASS/WARN/FAIL）

证据目录统一：

`artifacts/spiral-{spiral_id}/{trade_date}/`

最小证据文件：

- `run.log`
- `test.log`
- `gate_report.md`
- `consumption.md`
- `review.md`
- `sync_checklist.md`

---

## 3. 执行参数与命令兼容规则

参数占位符：

- `{trade_date}`: 交易日 `YYYYMMDD`
- `{start}` / `{end}`: 回溯窗口（交易日口径）

兼容规则：

1. 在 S0a 完成前，允许使用 Python 模块命令作为临时入口
2. S0a 收口后，`eq` 必须成为统一入口
3. 若 `eq` 与模块命令结果不一致，以 `eq` 为修复目标并阻断收口

全圈 baseline command（圈前必须执行）：

```bash
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\pytest.exe -q
.\.venv\Scripts\python.exe scripts/quality/local_quality_check.py --scan
```

---

## 4. S0-S2 微圈总览（重排）

| Spiral | 主目标 | CP Slice（1-3） | 预算 | 前置 | 退出去向 |
|---|---|---|---:|---|---|
| S0a | 统一入口与配置注入可用 | CP-01 | 2d | 无 | S0b |
| S0b | L1 采集入库闭环 | CP-01 | 3d | S0a | S0c |
| S0c | L2 快照与失败链路闭环 | CP-01 | 3d | S0b | S1a |
| S1a | MSS 最小评分可跑 | CP-02 | 3d | S0c | S1b |
| S1b | MSS 消费验证闭环 | CP-02, CP-05 | 2d | S1a | S2a |
| S2a | IRS + Validation 最小闭环 | CP-03, CP-10 | 4d | S1b | S2b |
| S2b | MSS+IRS 集成推荐闭环 | CP-03, CP-05 | 3d | S2a | S3 或 S2r |
| S2r | 质量门失败修复子圈 | CP-03, CP-05, CP-10 | 1-2d | S2b FAIL | 回 S2b |

说明：默认 7 天 cadence 不变；上述微圈是 7 天内可组合的执行单元。

---

## 5. 各圈执行合同（v0.2）

### S0a

- 主目标：统一入口与配置注入可运行
- `baseline command`：`.\.venv\Scripts\pytest.exe tests/unit/config/test_config_defaults.py -q`
- `target command`：
  - `python -m src.pipeline.main --help`
  - `eq --help`
- `target test`：`.\.venv\Scripts\pytest.exe tests/unit/config/test_config_defaults.py tests/unit/config/test_env_docs_alignment.py -q`
- 门禁：
  - `eq` 命令可调用
  - 路径读取全部来自 `Config.from_env()`
- 产物：`cli_contract.md`, `config_effective_values.json`
- 消费：S0b 记录“通过统一入口触发采集”

### S0b

- 主目标：L1 原始数据采集与入库闭环
- `baseline command`：`.\.venv\Scripts\pytest.exe tests/unit/data/models/test_model_contract_alignment.py -q`
- `target command`：`eq run --date {trade_date} --source tushare --l1-only`
- `target test`：`.\.venv\Scripts\pytest.exe tests/unit/data/test_fetcher_contract.py tests/unit/data/test_l1_repository_contract.py -q`
- 门禁：
  - `raw_daily` 当日记录数 `> 0`
  - `raw_trade_cal` 含 `{trade_date}`
  - 失败输出 `error_manifest.json`
- 产物：`raw_counts.json`, `fetch_retry_report.md`, `error_manifest_sample.json`
- 消费：S0c 记录“L1 -> L2 读取链路”

### S0c

- 主目标：L2 快照与错误分级闭环
- `baseline command`：`.\.venv\Scripts\pytest.exe tests/unit/data/models/test_snapshots.py -q`
- `target command`：`eq run --date {trade_date} --source tushare --to-l2`
- `target test`：`.\.venv\Scripts\pytest.exe tests/unit/data/test_snapshot_contract.py tests/unit/data/test_s0_canary.py -q`
- 门禁：
  - `market_snapshot` 当日存在
  - 字段含 `data_quality/stale_days/source_trade_date`
  - 失败流程包含 `error_level`
- 产物：`market_snapshot_sample.parquet`, `industry_snapshot_sample.parquet`, `s0_canary_report.md`
- 消费：S1a 记录“L2 作为 MSS 输入”

### S1a

- 主目标：MSS 最小评分可跑
- `baseline command`：`.\.venv\Scripts\pytest.exe tests/unit/data/models/test_snapshots.py -q`
- `target command`：`eq mss --date {trade_date}`
- `target test`：`.\.venv\Scripts\pytest.exe tests/unit/algorithms/mss/test_mss_contract.py tests/unit/algorithms/mss/test_mss_engine.py -q`
- 门禁：
  - `mss_panorama` 当日记录数 `> 0`
  - 字段含 `mss_score/mss_temperature/mss_cycle`
- 产物：`mss_panorama_sample.parquet`, `mss_factor_trace.md`
- 消费：S1b 记录“MSS 输出被回溯探针消费”

### S1b

- 主目标：MSS 消费验证闭环（非只算分）
- `baseline command`：`.\.venv\Scripts\pytest.exe tests/unit/config/test_config_defaults.py -q`
- `target command`：`eq mss-probe --start {start} --end {end}`
- `target test`：`.\.venv\Scripts\pytest.exe tests/unit/algorithms/mss/test_mss_probe_contract.py tests/unit/integration/test_mss_integration_contract.py -q`
- 门禁：
  - 产出 `mss_only_probe_report`
  - 包含 `top_bottom_spread_5d` 与结论
- 产物：`mss_only_probe_report.md`, `mss_consumption_case.md`
- 消费：S2a 记录“IRS 叠加前使用 S1b 结论”

### S2a

- 主目标：IRS + Validation 最小闭环
- `baseline command`：`.\.venv\Scripts\pytest.exe tests/unit/config/test_dependency_manifest.py -q`
- `target command`：`eq recommend --date {trade_date} --mode mss_irs --with-validation`
- `target test`：`.\.venv\Scripts\pytest.exe tests/unit/algorithms/irs/test_irs_contract.py tests/unit/integration/test_validation_gate_contract.py -q`
- 门禁：
  - `irs_industry_daily` 当日记录数 `> 0`
  - `validation_gate_decision` 当日可追溯
  - FAIL 必须产出 `validation_prescription`
- 产物：`irs_industry_daily_sample.parquet`, `validation_gate_decision_sample.parquet`, `validation_prescription_sample.md`
- 消费：S2b 记录“使用 gate 决策驱动集成”

### S2b

- 主目标：MSS+IRS 集成推荐闭环
- `baseline command`：`.\.venv\Scripts\pytest.exe tests/unit/config/test_env_docs_alignment.py -q`
- `target command`：`eq recommend --date {trade_date} --mode integrated`
- `target test`：`.\.venv\Scripts\pytest.exe tests/unit/integration/test_integration_contract.py tests/unit/integration/test_quality_gate_contract.py -q`
- 门禁：
  - `integrated_recommendation` 当日记录数 `> 0`
  - `quality_gate_report.status in (PASS, WARN)`
  - FAIL 不得进入 S3，必须进入 S2r
- 产物：`integrated_recommendation_sample.parquet`, `quality_gate_report.md`, `s2_go_nogo_decision.md`
- 消费：S3 记录“回测消费推荐结果”

### S2r（条件触发）

- 触发：S2b `quality_gate_report.status = FAIL`
- 主目标：只修不扩，恢复可通过质量门
- `baseline command`：`.\.venv\Scripts\pytest.exe tests/unit/config/test_dependency_manifest.py -q`
- `target command`：`eq recommend --date {trade_date} --mode integrated --repair s2r`
- `target test`：`.\.venv\Scripts\pytest.exe tests/unit/integration/test_validation_gate_contract.py tests/unit/integration/test_quality_gate_contract.py -q`
- 门禁：
  - `quality_gate_report.status in (PASS, WARN)`
  - 必须产出 `s2r_patch_note` 与 `s2r_delta_report`
- 产物：`s2r_patch_note.md`, `s2r_delta_report.md`
- 消费：返回 S2b 重验并记录“修复前后差异结论”

---

## 6. 状态推进与降级规则

状态定义：

- `planned`：已排期未执行
- `in_progress`：执行中
- `blocked`：被门禁阻断
- `completed`：收口完成

推进规则：

1. 5 件套未齐，不得 `completed`
2. `consumption.md` 缺失，不得 `completed`
3. `blocked` 超过 1 天，必须提交降级策略到 `review.md`
4. S2b FAIL 仅允许进入 S2r，不允许跳过进入 S3

---

## 7. 首轮启动（立即可执行）

执行顺序：

1. 跑 baseline command（环境健康检查）
2. 启动 S0a（统一入口与配置）
3. S0a 完成后进入 S0b

启动命令：

```bash
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\pytest.exe -q
.\.venv\Scripts\python.exe scripts/quality/local_quality_check.py --scan
```

---

## 8. 最小同步（每圈固定）

每圈收口后必须同步：

1. `Governance/specs/spiral-{spiral_id}/final.md`
2. `Governance/record/development-status.md`
3. `Governance/record/debts.md`
4. `Governance/record/reusable-assets.md`
5. `Governance/Capability/SPIRAL-CP-OVERVIEW.md`

---

## 9. 变更记录

| 版本 | 日期 | 变更说明 |
|---|---|---|
| v0.2 | 2026-02-13 | 修复可执行性断点：补 SoT 定位、引入 baseline/target 双命令口径、补 CP Slice、统一参数占位符、重写微圈合同 |
| v0.1 | 2026-02-13 | 初稿 |
