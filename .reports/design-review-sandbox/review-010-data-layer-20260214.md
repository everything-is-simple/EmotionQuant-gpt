# 评审报告 010：Data Layer 数据层系统

评审日期：2026-02-14  
评审范围：`docs/design/core-infrastructure/data-layer/*`，联动 `validation`、`integration`、`trading`

---

## 1. 结论摘要

- 结论：Data Layer 是系统实战稳定性的地基层，核心价值在数据质量与契约一致性，而非直接提供策略收益。
- 主要收益：本地优先链路、分层边界清晰、降级可追溯、Validation/Integration 调度闭环。
- 主要风险：设计口径完整，但仓库实现仍偏骨架，权威模型与实现可能存在偏差。

---

## 2. 设计事实（文档证据）

1. Data Layer 已定义 L1-L4 分层 + Ops/Business Tables，且 L1 Parquet、L2+ DuckDB 单库优先。  
   证据：`docs/design/core-infrastructure/data-layer/data-layer-information-flow.md:31`、`docs/design/core-infrastructure/data-layer/data-layer-information-flow.md:45`、`docs/design/core-infrastructure/data-layer/data-layer-data-models.md:35`
2. 主流程遵循“本地数据优先”，禁止把远端实时查询作为常态依赖。  
   证据：`docs/design/core-infrastructure/data-layer/data-layer-information-flow.md:86`、`docs/design/core-infrastructure/data-layer/data-layer-information-flow.md:88`
3. 降级字段契约明确：`data_quality/stale_days/source_trade_date`。  
   证据：`docs/design/core-infrastructure/data-layer/data-layer-information-flow.md:90`、`docs/design/core-infrastructure/data-layer/data-layer-data-models.md:229`、`docs/design/core-infrastructure/data-layer/data-layer-data-models.md:230`、`docs/design/core-infrastructure/data-layer/data-layer-data-models.md:231`
4. 降级上限明确：`stale_days > 3` 必须阻断主流程并告警。  
   证据：`docs/design/core-infrastructure/data-layer/data-layer-information-flow.md:91`、`docs/design/core-infrastructure/data-layer/data-layer-information-flow.md:518`
5. 日调度中已纳入 Validation Gate 与 Integration 质量检查时段。  
   证据：`docs/design/core-infrastructure/data-layer/data-layer-algorithm.md:554`、`docs/design/core-infrastructure/data-layer/data-layer-algorithm.md:555`
6. A 股关键 L1 原始契约明确：`raw_limit_list`、`raw_trade_cal`。  
   证据：`docs/design/core-infrastructure/data-layer/data-layer-data-models.md:108`、`docs/design/core-infrastructure/data-layer/data-layer-data-models.md:191`
7. L3 的 `integrated_recommendation` 字段已覆盖权重、门禁、推荐、仓位、RR 等执行关键信息。  
   证据：`docs/design/core-infrastructure/data-layer/data-layer-data-models.md:420`、`docs/design/core-infrastructure/data-layer/data-layer-data-models.md:441`、`docs/design/core-infrastructure/data-layer/data-layer-data-models.md:443`、`docs/design/core-infrastructure/data-layer/data-layer-data-models.md:450`
8. 股票代码转换口径统一：L1 保留 `ts_code`，L2+ 统一 `stock_code`。  
   证据：`docs/design/core-infrastructure/data-layer/data-layer-api.md:612`、`docs/design/core-infrastructure/data-layer/data-layer-api.md:614`
9. 存储边界明确：主库 `emotionquant.duckdb` + 运维库 `ops.duckdb`。  
   证据：`docs/design/core-infrastructure/data-layer/data-layer-api.md:682`、`docs/design/core-infrastructure/data-layer/data-layer-api.md:683`
10. 当前实现状态明确为“骨架/占位实现”。  
    证据：`docs/design/core-infrastructure/data-layer/data-layer-data-models.md:11`、`docs/design/core-infrastructure/data-layer/data-layer-information-flow.md:11`

---

## 3. 实战正向收益来源（实战推断）

1. 稳定性收益：本地优先 + 降级上限，降低外部数据波动冲击。
2. 一致性收益：分层与字段契约固定后，MSS/IRS/PAS/Integration 输入输出更可控。
3. 风险收益：`stale_days` 与质量标记可在数据不新鲜时自动减速或阻断。
4. 复盘收益：`source_trade_date` + `validation/integration` 链路可追溯问题来源。

---

## 4. A 股适配阶段与不适配阶段

### 4.1 更适配

1. 盘后批处理主导阶段（EOD 调度稳定）。
2. 质量优先阶段（对一致性要求高的实盘准备场景）。
3. 轮动行情阶段（L2 快照 + L3 输出便于跨层回放）。

### 4.2 较难适配

1. 盘中高频场景（日更流水线对秒级决策支持弱）。
2. 长时外部异常阶段（连续降级后可用性下降）。
3. 结构突变阶段（仅靠 stale 阈值难覆盖“新但失真”的语义问题）。

---

## 5. 实战沙盘演示（预期行为）

1. 场景 A（正常日）  
   条件：L1 核心文件齐全、质量正常。  
   预期：L2/L3/L4 顺序推进，17:15 Gate，17:20 集成+质量检查后产出推荐。
2. 场景 B（轻度降级）  
   条件：单项缺失但 `stale_days<=3`。  
   预期：允许继续并向下游透传质量标记。  
   证据：`docs/design/core-infrastructure/data-layer/data-layer-information-flow.md:519`
3. 场景 C（重度降级）  
   条件：`stale_days>3`。  
   预期：`is_ready=false`，阻断 MSS/IRS/PAS 并告警。  
   证据：`docs/design/core-infrastructure/data-layer/data-layer-information-flow.md:518`
4. 场景 D（关键数据缺失链）  
   条件：L1/L2 关键输入缺失。  
   预期：degraded mode，记录 `stale_days/source_trade_date`。  
   证据：`docs/design/core-infrastructure/data-layer/data-layer-information-flow.md:585`

---

## 6. 防御措施盘点

1. Step0 门禁 + stale 阈值阻断，防止坏数据进入算法层。
2. 质量字段三件套保障降级可追溯。
3. 主库/ops 库分离，降低运维与审计耦合。  
   证据：`docs/design/core-infrastructure/data-layer/data-layer-api.md:682`、`docs/design/core-infrastructure/data-layer/data-layer-api.md:683`
4. `ts_code -> stock_code` 统一转换，降低跨层 join 错配。
5. `validation_*` 与 `integrated_recommendation` 入模，保障下游读取契约稳定。

---

## 7. 需要进化的点（优先级）

1. P0：先完成契约落地（`src/data/models` 对齐权威模型并补测试）。
2. P0：质量门禁自动化（`stale_days`、覆盖率、跨日一致性前置检查）。
3. P1：降级策略细化为“数据类型分级阈值 + 影响面分级”。
4. P1：在不破坏主流程前提下增加可选盘中增量层。
5. P2：建立跨年分库触发与回迁策略，降低人工维护成本。

---

## 8. 下一步（执行建议）

1. 做 Data Layer 最小沙盘：正常日、`stale<=3`、`stale>3` 三组回放。
2. 做契约一致性测试：权威 DDL vs `src/data/models` 字段扫描。
3. 继续进入下一份：`review-011-system-overview-governance-20260214.md`。
