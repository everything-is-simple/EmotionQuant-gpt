# 评审报告 008：Analysis 绩效归因与报告系统

评审日期：2026-02-14  
评审范围：`docs/design/core-infrastructure/analysis/*`，联动 `integration`、`trading`、`backtest`

---

## 1. 结论摘要

- 结论：Analysis 的价值在“可解释、可复盘、可迭代”，主要提升治理反馈，不直接生成交易信号。
- 主要收益：统一绩效口径、三路归因拆解、风险摘要结构化、日报闭环输出。
- 主要风险：设计完成但代码未落地，短期收益取决于 L4 实现与数据质量。

---

## 2. 设计事实（文档证据）

1. Analysis 仅消费 L3 与执行结果，产出 L4 分析指标/报告，不替代算法层。  
   证据：`docs/design/core-infrastructure/analysis/analysis-algorithm.md:17`、`docs/design/core-infrastructure/analysis/analysis-api.md:11`
2. 输入依赖覆盖实盘与回测双场景。  
   证据：`docs/design/core-infrastructure/analysis/analysis-algorithm.md:26`、`docs/design/core-infrastructure/analysis/analysis-information-flow.md:79`
3. 输出落盘规范统一到 `.reports/analysis/` 且命名模板固定。  
   证据：`docs/design/core-infrastructure/analysis/analysis-algorithm.md:21`、`docs/design/core-infrastructure/analysis/analysis-api.md:519`、`docs/design/core-infrastructure/analysis/analysis-api.md:523`
4. 绩效口径包含无风险利率日化，与 Backtest 口径对齐（`risk_free_rate=0.015`）。  
   证据：`docs/design/core-infrastructure/analysis/analysis-algorithm.md:68`、`docs/design/core-infrastructure/analysis/analysis-algorithm.md:72`、`docs/design/core-infrastructure/analysis/analysis-algorithm.md:398`
5. 归因支持实盘/回测上下文切换，并输出 MSS/IRS/PAS 三路贡献。  
   证据：`docs/design/core-infrastructure/analysis/analysis-algorithm.md:170`、`docs/design/core-infrastructure/analysis/analysis-algorithm.md:172`、`docs/design/core-infrastructure/analysis/analysis-algorithm.md:174`、`docs/design/core-infrastructure/analysis/analysis-algorithm.md:199`、`docs/design/core-infrastructure/analysis/analysis-algorithm.md:201`
6. 风险摘要模型结构化定义了低/中/高风险计数与占比及风险提示文案。  
   证据：`docs/design/core-infrastructure/analysis/analysis-data-models.md:199`、`docs/design/core-infrastructure/analysis/analysis-data-models.md:200`、`docs/design/core-infrastructure/analysis/analysis-data-models.md:201`、`docs/design/core-infrastructure/analysis/analysis-data-models.md:202`、`docs/design/core-infrastructure/analysis/analysis-data-models.md:203`、`docs/design/core-infrastructure/analysis/analysis-data-models.md:204`、`docs/design/core-infrastructure/analysis/analysis-data-models.md:205`
7. L4 持久化表已定义：`daily_report`、`performance_metrics`、`signal_attribution`。  
   证据：`docs/design/core-infrastructure/analysis/analysis-data-models.md:215`、`docs/design/core-infrastructure/analysis/analysis-data-models.md:243`、`docs/design/core-infrastructure/analysis/analysis-data-models.md:263`
8. 缺失输入按降级/跳过处理并标记 `degraded`，不做跨层回填。  
   证据：`docs/design/core-infrastructure/analysis/analysis-algorithm.md:444`、`docs/design/core-infrastructure/analysis/analysis-information-flow.md:429`、`docs/design/core-infrastructure/analysis/analysis-information-flow.md:431`
9. 当前实现状态明确为“设计完成、代码未落地”。  
   证据：`docs/design/core-infrastructure/analysis/analysis-algorithm.md:5`

---

## 3. 实战正向收益来源（实战推断）

1. 复盘效率收益：能区分“信号问题”与“执行问题”，减少盲目调参。
2. 归因收益：可定位 MSS/IRS/PAS 哪一层在当前市场有效或失效。
3. 风控收益：风险分布和集中度统计可提前显性化潜在回撤。
4. 决策收益：固定日报节奏（15:35-15:45）形成稳定反馈回路。  
   证据：`docs/design/core-infrastructure/analysis/analysis-information-flow.md:389`、`docs/design/core-infrastructure/analysis/analysis-information-flow.md:391`

---

## 4. A 股适配阶段与不适配阶段

### 4.1 更适配

1. 轮动与分化阶段（三层归因可清晰定位收益驱动）。
2. 波动放大阶段（风险调整指标指导性更强）。
3. 迭代密集阶段（日报闭环有利于快速修正）。

### 4.2 较难适配

1. 成交数据质量弱阶段（归因容易被成交噪声污染）。
2. 极端事件日（单日指标易被异常样本主导）。
3. 长牛单边期（风险指标可能“表面健康”而掩盖拥挤累积）。

---

## 5. 实战沙盘演示（预期行为）

1. 场景 A（实盘日常）  
   条件：`trade_records` 可用。  
   预期：走实盘分支，输出绩效/归因/风险日报。
2. 场景 B（回测复盘）  
   条件：`is_backtest_context=True`。  
   预期：成交统计使用 `backtest_trade_records`，绩效使用 `backtest_results.equity_curve`。  
   证据：`docs/design/core-infrastructure/analysis/analysis-information-flow.md:165`、`docs/design/core-infrastructure/analysis/analysis-information-flow.md:166`
3. 场景 C（归因输入缺失）  
   条件：`integrated_recommendation` 缺失。  
   预期：跳过归因计算，不影响其他可算项。  
   证据：`docs/design/core-infrastructure/analysis/analysis-information-flow.md:431`
4. 场景 D（回测绩效输入缺失）  
   条件：`backtest_results/equity_curve` 缺失。  
   预期：跳过绩效计算并标记降级。  
   证据：`docs/design/core-infrastructure/analysis/analysis-information-flow.md:429`、`docs/design/core-infrastructure/analysis/analysis-information-flow.md:430`

---

## 6. 防御措施盘点

1. 口径边界防御：禁止用第三方库替代模块输出口径。  
   证据：`docs/design/core-infrastructure/analysis/analysis-api.md:13`
2. 场景分支防御：实盘/回测数据源显式分支，避免混用成交记录。  
   证据：`docs/design/core-infrastructure/analysis/analysis-information-flow.md:165`、`docs/design/core-infrastructure/analysis/analysis-information-flow.md:166`
3. 缺失降级防御：缺什么跳什么，不跨层回填。  
   证据：`docs/design/core-infrastructure/analysis/analysis-algorithm.md:444`
4. 输出标准化防御：固定落盘目录与命名模板，保证证据链可追溯。  
   证据：`docs/design/core-infrastructure/analysis/analysis-api.md:519`、`docs/design/core-infrastructure/analysis/analysis-api.md:523`
5. L4 分表沉淀防御：日报/绩效/归因分表，支持审计和横向对比。  
   证据：`docs/design/core-infrastructure/analysis/analysis-data-models.md:215`、`docs/design/core-infrastructure/analysis/analysis-data-models.md:243`、`docs/design/core-infrastructure/analysis/analysis-data-models.md:263`

---

## 7. 需要进化的点（优先级）

1. P0：优先完成 L4 最小实现闭环（`compute_metrics + attribute_signals + generate_daily_report + 落盘`）。
2. P0：增强归因稳健性（去极值/分位过滤）以降低异常日失真。
3. P1：风险摘要前瞻化（变化率/拐点检测）提升预警能力。
4. P1：增加实盘-回测偏差归因（信号偏差/成交偏差/成本偏差）。
5. P2：标准化对接 GUI/治理看板，降低手工读报成本。

---

## 8. 下一步（执行建议）

1. 做 Analysis 最小沙盘：正常日、回测日、缺失日三组回放。
2. 做归因稳定性对照：原始均值归因 vs 稳健归因。
3. 继续进入下一份：`review-009-gui-20260214.md`。
