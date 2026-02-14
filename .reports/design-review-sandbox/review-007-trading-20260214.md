# 评审报告 007：Trading 交易执行与风控系统

评审日期：2026-02-14  
评审范围：`docs/design/core-infrastructure/trading/*`，联动 `integration`、`validation`

---

## 1. 结论摘要

- 结论：Trading 的核心价值是把 Integration 信号转成可执行、可风控、可追溯的订单链路。
- 主要收益：Gate 前置阻断、订单前多段风控、T+1 冻结机制、业务表状态审计。
- 主要风险：设计完整但实现未落地，实战收益取决于 CP-07 工程质量。

---

## 2. 设计事实（文档证据）

1. Trading 职责明确：信号转化、风险管理、交易执行、持仓/T+1 管理。  
   证据：`docs/design/core-infrastructure/trading/trading-algorithm.md:20`、`docs/design/core-infrastructure/trading/trading-algorithm.md:21`、`docs/design/core-infrastructure/trading/trading-algorithm.md:22`、`docs/design/core-infrastructure/trading/trading-algorithm.md:23`
2. Validation Gate 在交易入口前置：`final_gate=FAIL` 直接跳过当日信号。  
   证据：`docs/design/core-infrastructure/trading/trading-algorithm.md:37`、`docs/design/core-infrastructure/trading/trading-algorithm.md:39`
3. 信号过滤规则明确：低分、`AVOID/SELL`、`opportunity_grade=D`、`risk_reward_ratio < 1.0` 均过滤。  
   证据：`docs/design/core-infrastructure/trading/trading-algorithm.md:46`、`docs/design/core-infrastructure/trading/trading-algorithm.md:52`、`docs/design/core-infrastructure/trading/trading-algorithm.md:53`
4. Integration->Trading 桥接清晰：`bullish/bearish/neutral -> buy/sell/hold`，`hold` 不下单，`integration_mode` 透传。  
   证据：`docs/design/core-infrastructure/trading/trading-algorithm.md:101`、`docs/design/core-infrastructure/trading/trading-algorithm.md:108`
5. 订单前风控为多段检查：资金、单股、行业、总仓位、T+1、涨跌停。  
   证据：`docs/design/core-infrastructure/trading/trading-algorithm.md:130`、`docs/design/core-infrastructure/trading/trading-algorithm.md:136`、`docs/design/core-infrastructure/trading/trading-algorithm.md:144`、`docs/design/core-infrastructure/trading/trading-algorithm.md:154`、`docs/design/core-infrastructure/trading/trading-algorithm.md:161`、`docs/design/core-infrastructure/trading/trading-algorithm.md:166`
6. 风控阈值默认值明确：单股 20%、行业 30%、总仓位 80%。  
   证据：`docs/design/core-infrastructure/trading/trading-algorithm.md:179`、`docs/design/core-infrastructure/trading/trading-algorithm.md:180`、`docs/design/core-infrastructure/trading/trading-algorithm.md:181`
7. 执行口径以集合竞价为主，成交后更新状态与 T+1 冻结。  
   证据：`docs/design/core-infrastructure/trading/trading-algorithm.md:272`、`docs/design/core-infrastructure/trading/trading-algorithm.md:301`、`docs/design/core-infrastructure/trading/trading-algorithm.md:303`、`docs/design/core-infrastructure/trading/trading-algorithm.md:305`
8. 持仓与业务表已包含 T+1 执行字段：`can_sell_date/is_frozen/t1_frozen`。  
   证据：`docs/design/core-infrastructure/trading/trading-data-models.md:97`、`docs/design/core-infrastructure/trading/trading-data-models.md:98`、`docs/design/core-infrastructure/trading/trading-data-models.md:293`、`docs/design/core-infrastructure/trading/trading-data-models.md:299`
9. 信息流定义了失败与拒绝路径：订单状态机与 reason 码。  
   证据：`docs/design/core-infrastructure/trading/trading-information-flow.md:479`、`docs/design/core-infrastructure/trading/trading-information-flow.md:557`、`docs/design/core-infrastructure/trading/trading-information-flow.md:559`
10. 当前实现状态明确为“代码未落地”。  
    证据：`docs/design/core-infrastructure/trading/trading-algorithm.md:11`、`docs/design/core-infrastructure/trading/trading-api.md:11`

---

## 3. 实战正向收益来源（实战推断）

1. 风险拦截收益：下单前拒绝超仓、T+1 违规、涨跌停不可成交订单，可直接压低执行型回撤。
2. 一致性收益：集成字段透传减少研究信号与执行信号语义漂移。
3. 合规收益：A 股约束内生化，减少回测-实盘偏差。
4. 复盘收益：订单/持仓/T+1 三表可追溯拒单与成交原因。

---

## 4. A 股适配阶段与不适配阶段

### 4.1 更适配

1. 波动上升、风控压力高阶段。
2. 涨跌停频发阶段（可成交性检查价值高）。
3. 轮动频繁阶段（先过风控可抑制拥挤追涨）。

### 4.2 较难适配

1. 极端流动性冲击阶段（全额成交假设可能乐观）。
2. 高频盘口变化阶段（开盘口径对盘中微结构刻画有限）。
3. 信号突变阶段（固定阈值需 regime 化调整）。

---

## 5. 实战沙盘演示（预期行为）

1. 场景 A（Gate FAIL）  
   条件：`validation_gate_decision.final_gate=FAIL`。  
   预期：返回空信号并记录 `blocked_by_gate`。  
   证据：`docs/design/core-infrastructure/trading/trading-algorithm.md:37`、`docs/design/core-infrastructure/trading/trading-algorithm.md:39`、`docs/design/core-infrastructure/trading/trading-information-flow.md:547`
2. 场景 B（RR 不足）  
   条件：`risk_reward_ratio < 1.0`。  
   预期：执行层过滤，不下单。  
   证据：`docs/design/core-infrastructure/trading/trading-algorithm.md:52`、`docs/design/core-infrastructure/trading/trading-algorithm.md:53`
3. 场景 C（仓位超限）  
   条件：单股/行业/总仓位超阈值。  
   预期：风控拒单并返回原因。  
   证据：`docs/design/core-infrastructure/trading/trading-algorithm.md:141`、`docs/design/core-infrastructure/trading/trading-algorithm.md:151`、`docs/design/core-infrastructure/trading/trading-algorithm.md:158`
4. 场景 D（T+1 与涨跌停）  
   条件：当日买入当日卖出；涨停买入或跌停卖出。  
   预期：分别以 `t1_frozen` 与涨跌停不可成交拒单。  
   证据：`docs/design/core-infrastructure/trading/trading-algorithm.md:164`、`docs/design/core-infrastructure/trading/trading-algorithm.md:167`、`docs/design/core-infrastructure/trading/trading-algorithm.md:169`

---

## 6. 防御措施盘点

1. Gate 前置阻断，坏状态不进入执行链。
2. 风控组件化（`OrderManager/RiskManager/T1Tracker`）便于替换与测试。  
   证据：`docs/design/core-infrastructure/trading/trading-api.md:24`、`docs/design/core-infrastructure/trading/trading-api.md:410`
3. T+1 冻结与可卖判断双机制，避免当日回转与卖空风险。
4. 订单状态机区分 `submitted/rejected/filled`，异常路径可审计。
5. 数据缺失降级策略明确（Gate FAIL 跳过、开盘价缺失用前收）。  
   证据：`docs/design/core-infrastructure/trading/trading-information-flow.md:547`、`docs/design/core-infrastructure/trading/trading-information-flow.md:551`

---

## 7. 需要进化的点（优先级）

1. P0：先完成最小可运行实现（`signal -> order -> execution -> positions/t1_frozen`）。
2. P0：成交模型从“全额成交默认”升级为“可成交比例 + 流动性约束”。
3. P1：风险阈值 regime 化（20/30/80 分市场状态动态化）。
4. P1：拒单原因枚举标准化，便于跨期统计与调参。
5. P2：扩展分批与时段化执行实验，在 A 股约束下评估增益。

---

## 8. 下一步（执行建议）

1. 做 Trading 最小沙盘：Gate FAIL、T+1、涨跌停、超仓位四组回放。
2. 做执行偏差对照：全额成交假设 vs 可成交比例模型。
3. 继续进入下一份：`review-008-analysis-20260214.md`。
