# 评审报告 004：Validation 因子与权重验证系统

评审日期：2026-02-14  
评审范围：`docs/design/core-algorithms/validation/*`，联动 `integration`

---

## 1. 结论摘要

- 结论：Validation 是系统实盘闸门层，核心作用是把“可计算信号”提升为“可执行信号”。
- 主要收益：因子失效拦截、权重过拟合抑制、降级回退可审计。
- 主要风险：全局固定阈值与固定 WFA 窗口在极端 regime 切换期可能偏保守。

---

## 2. 设计事实（文档证据）

1. Validation 双目标明确：验证因子预测力、验证候选权重优于 baseline。  
   证据：`docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md:11`、`docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md:14`
2. 输出契约固定为 `validation_gate_decision + validation_weight_plan`，供 CP-05/06/07 消费。  
   证据：`docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md:16`
3. 日级门禁发生在收盘后、Integration 前，且 CP-05 从 DuckDB 读取 gate/weight_plan。  
   证据：`docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md:24`、`docs/design/core-algorithms/validation/factor-weight-validation-information-flow.md:28`
4. 因子验证指标与 PASS/WARN/FAIL 阈值齐备（IC/RankIC/ICIR/正IC比例/衰减/覆盖率）。  
   证据：`docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md:58`、`docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md:72`
5. 权重验证采用 baseline vs candidate + WFA（252/63/63），候选需同时满足 OOS 收益、回撤、夏普条件才可替换。  
   证据：`docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md:89`、`docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md:91`、`docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md:115`、`docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md:118`
6. Gate 规则完整：FAIL 阻断、WARN 放行并标记风险、PASS 正常通过。  
   证据：`docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md:127`、`docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md:132`、`docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md:134`
7. Integration 已按 Gate 契约执行：FAIL 抛错阻断；IRS 质量异常或候选缺失时回退 baseline+WARN。  
   证据：`docs/design/core-algorithms/integration/integration-algorithm.md:113`、`docs/design/core-algorithms/integration/integration-algorithm.md:116`、`docs/design/core-algorithms/integration/integration-algorithm.md:118`、`docs/design/core-algorithms/integration/integration-algorithm.md:126`
8. Gate 数据模型包含治理关键字段：`selected_weight_plan/stale_days/fallback_plan/reason`。  
   证据：`docs/design/core-algorithms/validation/factor-weight-validation-data-models.md:95`、`docs/design/core-algorithms/validation/factor-weight-validation-data-models.md:96`、`docs/design/core-algorithms/validation/factor-weight-validation-data-models.md:97`、`docs/design/core-algorithms/validation/factor-weight-validation-data-models.md:98`
9. 运行时数据源约束明确：禁止直接从 `.reports` 读取门禁与权重。  
   证据：`docs/design/core-algorithms/validation/factor-weight-validation-api.md:163`

---

## 3. 实战正向收益来源（实战推断）

1. 失效因子被日级门禁拦截，可减少错误仓位暴露。
2. 候选权重需样本外优于 baseline，可抑制局部过拟合。
3. WARN/FAIL + baseline 回退让系统在缺口与漂移场景下“降级运行而非失控运行”。
4. `validation_*` 持久化链路可复盘“为何当日放行/阻断”。

---

## 4. A 股适配阶段与不适配阶段

### 4.1 更适配

1. 风格快速切换期（因子失效频发）。
2. 主题轮动期（候选权重短期拟合风险高）。
3. 波动放大期（门禁与回退价值更高）。

### 4.2 较难适配

1. 单边强趋势且跨期稳定阶段，严格门禁可能偏保守。
2. 极短窗口 regime shift，252/63/63 对超快切换响应可能不足。
3. 制度冲击日，历史统计阈值可能短时失真。

---

## 5. 实战沙盘演示（预期行为）

1. 场景 A（正常通过）  
   条件：因子 PASS、权重 PASS。  
   预期：`final_gate=PASS`，按 `selected_weight_plan` 进入 Integration。
2. 场景 B（谨慎放行）  
   条件：Gate=WARN 或候选 plan 缺失。  
   预期：继续运行但回退 baseline 并标记 WARN。  
   证据：`docs/design/core-algorithms/integration/integration-algorithm.md:125`、`docs/design/core-algorithms/integration/integration-algorithm.md:126`
3. 场景 C（硬阻断）  
   条件：核心输入缺失、因子 FAIL 或权重 FAIL。  
   预期：`final_gate=FAIL`，阻断 Integration。  
   证据：`docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md:127`、`docs/design/core-algorithms/validation/factor-weight-validation-algorithm.md:128`
4. 场景 D（数据陈旧）  
   条件：验证数据过期或 IRS 质量为 stale/cold_start。  
   预期：使用最近有效结果并标记 stale；Integration 回退 baseline+WARN。  
   证据：`docs/design/core-algorithms/validation/factor-weight-validation-information-flow.md:100`、`docs/design/core-algorithms/integration/integration-algorithm.md:116`、`docs/design/core-algorithms/integration/integration-algorithm.md:118`

---

## 6. 防御措施盘点

1. Gate 三态防线（PASS/WARN/FAIL）同时具备“可放行”和“可阻断”能力。
2. baseline 常备回退，候选不可用不致中断主链路。
3. `stale_days` 入模，避免在过期验证结论上继续激进执行。
4. DuckDB 为权威运行源，`.reports` 仅阅读用途。
5. `selected_weight_plan -> validation_weight_plan -> WeightPlan` 桥接契约清晰。

---

## 7. 需要进化的点（优先级）

1. P0：阈值分 regime 化（按市场温度/波动分层）。
2. P0：WFA 双窗口并行（如 252/63/63 + 126/42/42）并用稳健性投票决策。
3. P1：fallback 分层（因子失败/权重失败/数据失败对应不同回退方案）。
4. P1：`stale_days` 超阈值后联动执行层自动降仓，而非仅告警。
5. P2：候选搜索显式加入换手、冲击成本、涨跌停可成交性约束。

---

## 8. 下一步（执行建议）

1. 做 Validation 对照：固定阈值 vs regime 阈值（触发频率、误阻断率、收益回撤比）。
2. 做 WFA 对照：单窗口 vs 双窗口投票（替换稳定性与收益方差）。
3. 继续进入下一份：`review-005-integration-20260214.md`。
