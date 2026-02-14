# 评审报告 012：Naming Conventions / Contracts 一致性专项

评审日期：2026-02-14  
评审范围：`docs/naming-conventions.md` + `docs/design/core-algorithms/*` + `docs/design/core-infrastructure/*`（命名与跨层契约）

---

## 1. 结论摘要

- 结论：命名规范与跨模块契约整体一致性高，已形成“统一枚举 + 桥接解耦 + 异常降级”的稳定框架。
- 主要正向收益：降低跨模块语义错配，提升回测/交易执行同口径能力，增强异常输入可控性。
- 关键修正：此前 PAS 风险收益比门槛漂移已修复，当前口径已统一为 `risk_reward_ratio >= 1.0`（执行层对 `<1.0` 继续软过滤）。  
  证据：`docs/design/core-algorithms/pas/pas-algorithm.md:22`、`docs/design/core-algorithms/pas/pas-algorithm.md:345`、`docs/design/core-algorithms/pas/pas-data-models.md:286`、`docs/design/core-infrastructure/trading/trading-algorithm.md:52`、`docs/design/core-infrastructure/backtest/backtest-algorithm.md:103`

---

## 2. 设计事实（文档证据）

1. 命名规范已统一定义 MSS 周期、趋势、PAS 方向、IRS 轮动状态、推荐等级与字段边界。  
   证据：`docs/naming-conventions.md:45`、`docs/naming-conventions.md:67`、`docs/naming-conventions.md:96`、`docs/naming-conventions.md:118`、`docs/naming-conventions.md:135`
2. `unknown` 已形成规范到 MSS 的闭环降级语义。  
   证据：`docs/naming-conventions.md:27`、`docs/design/core-algorithms/mss/mss-data-models.md:144`、`docs/design/core-algorithms/mss/mss-api.md:71`、`docs/design/core-algorithms/mss/mss-api.md:113`
3. 趋势命名统一为 `up/down/sideways`，并显式禁用 `flat` 作为趋势枚举。  
   证据：`docs/naming-conventions.md:79`、`docs/design/core-algorithms/mss/mss-algorithm.md:252`
4. `STRONG_BUY >= 75` 在命名规范、Integration、Data Layer、GUI 口径一致。  
   证据：`docs/naming-conventions.md:135`、`docs/design/core-algorithms/integration/integration-algorithm.md:200`、`docs/design/core-infrastructure/data-layer/data-layer-data-models.md:454`、`docs/design/core-infrastructure/gui/gui-algorithm.md:57`
5. Validation 到 Integration 的桥接契约一致：`selected_weight_plan` 业务键经 `validation_weight_plan` 解析为 `WeightPlan`。  
   证据：`docs/design/core-algorithms/validation/factor-weight-validation-api.md:127`、`docs/design/core-algorithms/validation/factor-weight-validation-api.md:132`、`docs/design/core-algorithms/validation/factor-weight-validation-data-models.md:95`、`docs/design/core-algorithms/validation/factor-weight-validation-data-models.md:162`、`docs/design/core-algorithms/integration/integration-api.md:91`、`docs/design/core-algorithms/integration/integration-api.md:102`
6. Gate 语义一致：`FAIL` 阻断、`WARN` 继续但降级，且候选缺失时回退 baseline。  
   证据：`docs/design/core-algorithms/integration/integration-algorithm.md:113`、`docs/design/core-algorithms/integration/integration-algorithm.md:125`、`docs/design/core-algorithms/integration/integration-algorithm.md:126`、`docs/design/core-algorithms/integration/integration-algorithm.md:133`
7. 代码字段转换契约清晰：L1 保留 `ts_code`，L2+ 统一 `stock_code`，转换集中在 Data Layer。  
   证据：`docs/naming-conventions.md:280`、`docs/naming-conventions.md:281`、`docs/design/core-infrastructure/data-layer/data-layer-api.md:612`、`docs/design/core-infrastructure/data-layer/data-layer-api.md:614`、`docs/design/core-infrastructure/data-layer/data-layer-api.md:882`
8. 风险收益比字段命名统一为 `risk_reward_ratio`，`rr_ratio` 明确禁用。  
   证据：`docs/naming-conventions.md:277`
9. PAS 风险收益比门槛现已全链路一致：算法/模型为 `>=1.0`，交易/回测执行侧过滤 `<1.0`。  
   证据：`docs/design/core-algorithms/pas/pas-algorithm.md:345`、`docs/design/core-algorithms/pas/pas-data-models.md:286`、`docs/design/core-infrastructure/trading/trading-algorithm.md:52`、`docs/design/core-infrastructure/backtest/backtest-algorithm.md:103`

---

## 3. 实战正向收益来源（实战推断）

1. 语义一致性收益：统一枚举减少 MSS/IRS/PAS/Integration 链路中的翻译偏差。
2. 执行一致性收益：同一 `final_score/recommendation/risk_reward_ratio` 在回测与交易端行为更可预测。
3. 风控收益：`unknown` 与 Gate 的“阻断/降级”双机制降低异常数据导致的误交易概率。
4. 可解释性收益：`selected_weight_plan -> WeightPlan` 桥接可追溯，便于复盘当天推荐差异。

---

## 4. A 股适配阶段与不适配阶段

### 4.1 更适配

1. 高频轮动与波动放大阶段：统一枚举与推荐阈值可降低跨模块误触发。
2. 数据缺口或质量波动阶段：`unknown` 与 Gate 降级机制可在不停摆前提下降低风险。
3. 多模块并行迭代阶段：契约稳定可显著降低联调返工成本。

### 4.2 较难适配

1. 规则快速演化阶段：新增枚举或阈值时，文档与实现可能短时不同步。
2. 多源数据异构阶段：`ts_code/stock_code` 转换若被绕过，错配风险会放大。
3. 手工同步密集阶段：跨文档阈值更新若无自动检查，容易再次产生漂移。

---

## 5. 实战沙盘演示（命名/契约）

1. 场景 A（标准链路）  
   条件：字段与枚举全部符合命名规范。  
   预期：Validation 先解出 `WeightPlan`，Integration 正常产出，Trading/Backtest 同口径执行。
2. 场景 B（周期异常）  
   条件：MSS 历史窗口不足。  
   预期：返回 `unknown` 且不抛系统错误，进入保守降级流程。  
   证据：`docs/design/core-algorithms/mss/mss-api.md:113`
3. 场景 C（Gate=FAIL）  
   条件：Validation 最终门禁失败。  
   预期：Integration 立即阻断，不下发交易信号。  
   证据：`docs/design/core-algorithms/integration/integration-algorithm.md:113`
4. 场景 D（RR 边界）  
   条件：`risk_reward_ratio = 0.95`。  
   预期：即便上游有推荐，执行层也会过滤，不进入订单链路。  
   证据：`docs/design/core-infrastructure/trading/trading-algorithm.md:52`、`docs/design/core-infrastructure/backtest/backtest-algorithm.md:103`

---

## 6. 防御措施盘点

1. 命名规范 SoT 明确禁用项（`flat` 趋势、`rr_ratio` 字段）。
2. `unknown` 周期与 Gate 机制构成“可降级 + 可阻断”双层防线。
3. `selected_weight_plan` 业务键与 `WeightPlan` 数值对象职责分离，减少重复解析错误。
4. `ts_code -> stock_code` 转换集中管理，降低跨层 join 错配。
5. 交易/回测执行层保留 RR 软过滤，作为末端质量兜底。

---

## 7. 需要进化的点（优先级）

1. P0：增加命名/契约一致性自动检查。  
   对 `sideways/unknown/risk_reward_ratio/stock_code/ts_code/PASS-WARN-FAIL` 与关键阈值（`75/70/55/1.0`）做 CI 扫描，防止再次漂移。
2. P0：建立阈值与枚举的单一机器可读来源（Schema-first）。  
   由 schema 生成文档片段与类型定义，减少手工同步误差。
3. P1：在 Integration/Trading/Backtest 增加契约版本校验。  
   检测不兼容版本时拒绝执行并提示迁移。
4. P1：补齐边界回归用例。  
   覆盖 `unknown`、`sideways`、`risk_reward_ratio=1.0`、`Gate=WARN/FAIL` 等关键边界。
5. P2：沉淀跨模块术语字典与变更模板。  
   新增字段/枚举时自动给出受影响模块清单。

---

## 8. 下一步（执行建议）

1. 先落地最小 CI 一致性检查脚本（关键词 + 阈值矩阵）。
2. 再将脚本接入 pre-commit/CI 阻断规则，防止文档回归漂移。
3. 下一轮从“文档一致性”转到“实现一致性”，抽样核对 `src/` 与设计契约。

