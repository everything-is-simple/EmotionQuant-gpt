# 系统设计再评审（实战沙盘）

开始日期：2026-02-14  
目录用途：逐项评审 `docs/design` 核心设计，按模块输出独立评审报告。

## 评审规则

1. 每次只评审一个模块（先核心算法，再基础设施）。
2. 每份报告必须包含：设计事实、实战收益来源、适配阶段、失效阶段、防御措施、进化建议。
3. 每份报告必须给出“可执行下一步”，避免只做抽象讨论。
4. 评审结论区分两类：
   - 文档证据（来自现有设计）
   - 实战推断（基于 A 股微观结构的推演）

## 报告清单

1. `review-001-mss-20260214.md`：MSS 市场情绪系统（首轮）
2. `review-002-irs-20260214.md`：IRS 行业轮动系统（首轮）
3. `review-003-pas-20260214.md`：PAS 个股机会系统（首轮）
4. `review-004-validation-20260214.md`：Validation 因子与权重验证系统（首轮）
5. `review-005-integration-20260214.md`：Integration 三三制集成系统（首轮）
6. `review-006-backtest-20260214.md`：Backtest 回测系统（首轮）
7. `review-007-trading-20260214.md`：Trading 交易执行与风控系统（首轮）
8. `review-008-analysis-20260214.md`：Analysis 绩效归因与报告系统（首轮）
9. `review-009-gui-20260214.md`：GUI 可视化与交互系统（首轮）
10. `review-010-data-layer-20260214.md`：Data Layer 数据层系统（首轮）
11. `review-011-system-overview-governance-20260214.md`：System Overview / Governance 交叉一致性（首轮）
12. `review-012-naming-contracts-20260214.md`：Naming Conventions / Contracts 一致性专项（首轮）

## 维护记录

1. `repair-log-20260214.md`：首轮结构与一致性修复记录（含文档打包备份信息）
