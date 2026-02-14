# 评审报告 005：Integration 三三制集成系统

评审日期：2026-02-14  
评审范围：`docs/design/core-algorithms/integration/*`，联动 `validation`、`trading`

---

## 1. 结论摘要

- 结论：Integration 的核心价值是把 MSS/IRS/PAS 统一为可执行输出，并把风险控制前置到集成层。
- 主要收益：门禁前置、权重回退、软约束协同、输出可追溯。
- 主要风险：设计口径完整但实现仍偏骨架，短期效果取决于 CP-05 工程落地。

---

## 2. 设计事实（文档证据）

1. 三三制基线明确：默认等权 1/3，Validation 通过后可切 candidate。  
   证据：`docs/design/core-algorithms/integration/integration-algorithm.md:17`、`docs/design/core-algorithms/integration/integration-algorithm.md:21`
2. Validation Gate 是前置必需输入，包含 `final_gate/selected_weight_plan/fallback_plan`。  
   证据：`docs/design/core-algorithms/integration/integration-algorithm.md:75`、`docs/design/core-algorithms/integration/integration-algorithm.md:79`、`docs/design/core-algorithms/integration/integration-algorithm.md:80`、`docs/design/core-algorithms/integration/integration-algorithm.md:81`
3. Gate 处理规则明确：FAIL 阻断；IRS 质量异常或候选缺失时回退 baseline+WARN。  
   证据：`docs/design/core-algorithms/integration/integration-algorithm.md:113`、`docs/design/core-algorithms/integration/integration-algorithm.md:116`、`docs/design/core-algorithms/integration/integration-algorithm.md:118`、`docs/design/core-algorithms/integration/integration-algorithm.md:126`
4. 综合评分采用权重线性融合，权重来自 gate 解析结果。  
   证据：`docs/design/core-algorithms/integration/integration-algorithm.md:141`、`docs/design/core-algorithms/integration/integration-algorithm.md:147`
5. 推荐等级与降级规则固定：`mss_cycle=unknown` 强制降到 `HOLD`。  
   证据：`docs/design/core-algorithms/integration/integration-algorithm.md:200`、`docs/design/core-algorithms/integration/integration-algorithm.md:207`
6. 协同约束是软约束：IRS 仅对 PAS 做轻度折扣/上浮并重算分数。  
   证据：`docs/design/core-algorithms/integration/integration-algorithm.md:225`、`docs/design/core-algorithms/integration/integration-algorithm.md:228`、`docs/design/core-algorithms/integration/integration-algorithm.md:229`、`docs/design/core-algorithms/integration/integration-algorithm.md:234`
7. 推荐列表排序以 `final_score` 为主，PAS/IRS 仅软排序不硬过滤。  
   证据：`docs/design/core-algorithms/integration/integration-algorithm.md:363`、`docs/design/core-algorithms/integration/integration-algorithm.md:364`、`docs/design/core-algorithms/integration/integration-algorithm.md:365`
8. TD/BU 双模式边界明确：BU 受 TD 风险上限约束，冲突以 TD 为准。  
   证据：`docs/design/core-algorithms/integration/integration-algorithm.md:382`、`docs/design/core-algorithms/integration/integration-algorithm.md:509`、`docs/design/core-algorithms/integration/integration-algorithm.md:510`
9. 输出模型保留模式、权重快照、Gate 状态和三系统分数，支持审计追溯。  
   证据：`docs/design/core-algorithms/integration/integration-data-models.md:153`、`docs/design/core-algorithms/integration/integration-data-models.md:155`、`docs/design/core-algorithms/integration/integration-data-models.md:158`、`docs/design/core-algorithms/integration/integration-data-models.md:161`、`docs/design/core-algorithms/integration/integration-data-models.md:164`
10. API 契约明确 Gate=FAIL 阻断，且权重违规抛异常。  
    证据：`docs/design/core-algorithms/integration/integration-api.md:53`、`docs/design/core-algorithms/integration/integration-api.md:133`
11. 当前实现状态为“设计完成、代码未落地”。  
    证据：`docs/design/core-algorithms/integration/integration-information-flow.md:5`、`docs/design/core-algorithms/integration/integration-information-flow.md:11`

---

## 3. 实战正向收益来源（实战推断）

1. 决策一致性收益：统一输出 `final_score/recommendation/position_size/neutrality`，减少执行分歧。
2. 回撤控制收益：Gate + baseline 回退可抑制异常权重扩损。
3. 风险预算收益：MSS/IRS/PAS 协同约束把风险管理前置到集成层。
4. 复盘治理收益：权重与 Gate 快照可直接解释“为何放行/降级/降仓”。

---

## 4. A 股适配阶段与不适配阶段

### 4.1 更适配

1. 轮动与分化并存阶段（三系统互补价值高）。
2. 高噪声阶段（软约束与降级链可抑制单模块误判）。
3. 结构性行情阶段（BU 可补充强股扩散，但受 TD 风险上限约束）。

### 4.2 较难适配

1. 单边逼空且持续高温阶段（风控约束可能偏保守）。
2. 超短 V 反阶段（固定倍率和阈值响应偏慢）。
3. 上游大面积缺失阶段（虽可降级，但可交易机会密度下降）。

---

## 5. 实战沙盘演示（预期行为）

1. 场景 A（PASS + candidate 有效）  
   预期：按 candidate 权重融合，输出正常推荐与仓位。
2. 场景 B（WARN + candidate 缺失）  
   预期：自动回退 baseline，带 WARN 标记继续运行。  
   证据：`docs/design/core-algorithms/integration/integration-algorithm.md:125`、`docs/design/core-algorithms/integration/integration-algorithm.md:126`
3. 场景 C（FAIL）  
   预期：抛 `ValidationGateError`，阻断输出。  
   证据：`docs/design/core-algorithms/integration/integration-algorithm.md:113`、`docs/design/core-algorithms/integration/integration-algorithm.md:114`
4. 场景 D（`mss_cycle=unknown`）  
   预期：高分也降级为 `HOLD`，进入观察模式。  
   证据：`docs/design/core-algorithms/integration/integration-information-flow.md:270`、`docs/design/core-algorithms/integration/integration-information-flow.md:271`
5. 场景 E（BU 激进、TD 保守）  
   预期：BU 仓位受 TD 上限约束，方向冲突以 TD 为准。  
   证据：`docs/design/core-algorithms/integration/integration-algorithm.md:509`、`docs/design/core-algorithms/integration/integration-algorithm.md:510`

---

## 6. 防御措施盘点

1. Gate 失败硬阻断，阻止坏信号入执行链。
2. baseline 常备回退，候选异常时不中断主流程。
3. `unknown -> HOLD` 保护，降低异常输入误开仓。
4. 输出边界校验，避免越界污染下游。
5. Trading 二次风控继续兜底（Gate/ RR / T+1 / 涨跌停）。  
   证据：`docs/design/core-infrastructure/trading/trading-algorithm.md:37`、`docs/design/core-infrastructure/trading/trading-algorithm.md:52`、`docs/design/core-infrastructure/trading/trading-algorithm.md:161`、`docs/design/core-infrastructure/trading/trading-algorithm.md:166`

---

## 7. 需要进化的点（优先级）

1. P0：先补实现闭环（`IntegrationEngine + Repository + 契约测试`）。
2. P0：参数 regime 化（阈值、协同倍率、仓位乘子分状态配置）。
3. P1：候选评估加入可成交性与冲击成本约束。
4. P1：BU/TD 冲突从“TD 全覆盖”升级为“风险预算分层覆盖”。
5. P2：统一 `degraded/WARN/stale/cold_start` 语义为单一状态机。

---

## 8. 下一步（执行建议）

1. 做最小实现沙盘：PASS/WARN/FAIL + baseline/candidate 切换回放。
2. 做参数敏感性对照：固定参数 vs regime 参数（胜率、回撤、换手、降级频率）。
3. 继续进入下一份：`review-006-backtest-20260214.md`。
