# 评审报告 006：Backtest 回测系统

评审日期：2026-02-14  
评审范围：`docs/design/core-infrastructure/backtest/*`，联动 `integration`、`validation`

---

## 1. 结论摘要

- 结论：Backtest 的核心价值是执行口径一致性与可复现验证，不是重做信号层。
- 主要收益：无未来函数约束、A 股规则复刻、Gate 前置门控、TD/BU 可对照。
- 主要风险：设计完整但实现未落地，短期收益取决于 CP-06 工程质量。

---

## 2. 设计事实（文档证据）

1. Backtest 明确只消费 L3 集成信号，不重算 MSS/IRS/PAS。  
   证据：`docs/design/core-infrastructure/backtest/backtest-algorithm.md:20`、`docs/design/core-infrastructure/backtest/backtest-algorithm.md:50`
2. 执行规则按 A 股口径建模：T+1、涨跌停、整手、费用、滑点。  
   证据：`docs/design/core-infrastructure/backtest/backtest-algorithm.md:21`、`docs/design/core-infrastructure/backtest/backtest-algorithm.md:195`、`docs/design/core-infrastructure/backtest/backtest-algorithm.md:199`
3. 时间轴拆分明确：`signal_date=T`，`execute_date=T+1`，防未来函数。  
   证据：`docs/design/core-infrastructure/backtest/backtest-algorithm.md:31`、`docs/design/core-infrastructure/backtest/backtest-algorithm.md:64`、`docs/design/core-infrastructure/backtest/backtest-api.md:40`、`docs/design/core-infrastructure/backtest/backtest-api.md:41`
4. 引擎架构为“Qlib 主选 + 本地向量化基线 + backtrader 兼容”。  
   证据：`docs/design/core-infrastructure/backtest/backtest-engine-selection.md:11`、`docs/design/core-infrastructure/backtest/backtest-engine-selection.md:13`、`docs/design/core-infrastructure/backtest/backtest-engine-selection.md:14`、`docs/design/core-infrastructure/backtest/backtest-engine-selection.md:15`
5. Gate 是 Step0 前置门控：`final_gate=FAIL` 跳过当日信号并记录阻断。  
   证据：`docs/design/core-infrastructure/backtest/backtest-algorithm.md:75`、`docs/design/core-infrastructure/backtest/backtest-algorithm.md:77`、`docs/design/core-infrastructure/backtest/backtest-information-flow.md:118`
6. 信号筛选统一为推荐等级门槛 + RR 过滤（`risk_reward_ratio < 1.0` 过滤）。  
   证据：`docs/design/core-infrastructure/backtest/backtest-algorithm.md:92`、`docs/design/core-infrastructure/backtest/backtest-algorithm.md:93`、`docs/design/core-infrastructure/backtest/backtest-algorithm.md:103`、`docs/design/core-infrastructure/backtest/backtest-algorithm.md:104`
7. 降级策略明确：L3 缺失可回退上一可用日，BU 缺失回退 TD，且禁止直连远端。  
   证据：`docs/design/core-infrastructure/backtest/backtest-algorithm.md:353`、`docs/design/core-infrastructure/backtest/backtest-algorithm.md:354`、`docs/design/core-infrastructure/backtest/backtest-algorithm.md:356`
8. 持久化边界清晰：业务输出表与运行态持仓表分离，避免与 Trading 冲突。  
   证据：`docs/design/core-infrastructure/backtest/backtest-data-models.md:244`、`docs/design/core-infrastructure/backtest/backtest-data-models.md:246`
9. 当前实现状态明确为“设计完成、代码未落地”。  
   证据：`docs/design/core-infrastructure/backtest/backtest-algorithm.md:13`、`docs/design/core-infrastructure/backtest/backtest-api.md:11`

---

## 3. 实战正向收益来源（实战推断）

1. 可实现性收益：将 A 股执行限制前置到回测，减少“回测可赚、实盘难做”偏差。
2. 风险控制收益：Gate 阻断与 RR 过滤可降低低质量信号入场频率。
3. 策略迭代收益：TD/BU 可对照回放，便于验证不同市况下模式有效性。
4. 治理收益：引擎、模式、信号来源与成交记录可追溯。

---

## 4. A 股适配阶段与不适配阶段

### 4.1 更适配

1. 高波动与快切换阶段（执行约束建模价值更高）。
2. 结构性行情阶段（TD/BU 对照可重复验证）。
3. 风险事件密集阶段（Gate 与降级可防批量误入场）。

### 4.2 较难适配

1. 极端流动性扭曲阶段（简化撮合/滑点可能低估冲击成本）。
2. 长期单边趋势阶段（过严过滤可能压缩后段收益）。
3. 微观结构快速变化阶段（若成交模型不更新，偏差会累积）。

---

## 5. 实战沙盘演示（预期行为）

1. 场景 A（标准日）  
   条件：Gate=PASS，L1/L3 齐全。  
   预期：T 日出信号，T+1 开盘执行并计入费用与滑点。
2. 场景 B（Gate 阻断）  
   条件：`final_gate=FAIL`。  
   预期：跳过当日信号并记录 `blocked_by_gate`。  
   证据：`docs/design/core-infrastructure/backtest/backtest-algorithm.md:351`
3. 场景 C（BU 数据缺失）  
   条件：`pas_breadth_daily` 缺失。  
   预期：禁用 BU，回退 TD。  
   证据：`docs/design/core-infrastructure/backtest/backtest-algorithm.md:354`
4. 场景 D（执行约束触发）  
   条件：T 日买入后当日卖出，或 execute_date 开盘即涨停。  
   预期：前者被 T+1 拒绝，后者买单拒绝/成交概率 0。  
   证据：`docs/design/core-infrastructure/backtest/backtest-test-cases.md:12`、`docs/design/core-infrastructure/backtest/backtest-test-cases.md:13`、`docs/design/core-infrastructure/backtest/backtest-test-cases.md:31`、`docs/design/core-infrastructure/backtest/backtest-test-cases.md:33`

---

## 6. 防御措施盘点

1. 无未来函数铁律：信号日与执行日严格拆分。
2. Gate 前置门控：Validation 风险直接传导到回测入口。
3. 执行策略组件化：`ExecutionPolicy/FeeModel/OrderSequencer` 可替换但口径统一。  
   证据：`docs/design/core-infrastructure/backtest/backtest-api.md:91`、`docs/design/core-infrastructure/backtest/backtest-api.md:110`、`docs/design/core-infrastructure/backtest/backtest-api.md:123`
4. 降级路径清晰：缺失场景按“跳过/回退/降级”处理，不补未来数据。
5. 质量门禁清单完整：未来函数、T+1、涨跌停均有验收条目。  
   证据：`docs/design/core-infrastructure/backtest/backtest-test-cases.md:161`、`docs/design/core-infrastructure/backtest/backtest-test-cases.md:163`、`docs/design/core-infrastructure/backtest/backtest-test-cases.md:167`、`docs/design/core-infrastructure/backtest/backtest-test-cases.md:171`

---

## 7. 需要进化的点（优先级）

1. P0：先落地最小可运行引擎与回测命令（`local_vectorized + top_down`）。
2. P0：增强成交可行性模型（排队、量能、成交概率）。
3. P1：成本模型细化为与流动性分层挂钩。
4. P1：`blocked_by_gate/degraded/fallback` 统一为标准状态机。
5. P2：模式切换从配置化升级为状态驱动或混合权重。

---

## 8. 下一步（执行建议）

1. 做 CP-06 最小实现：跑通 1 条回测命令并落库。
2. 做四组回放：Gate FAIL、T+1、涨跌停、RR<1。
3. 继续进入下一份：`review-007-trading-20260214.md`。
