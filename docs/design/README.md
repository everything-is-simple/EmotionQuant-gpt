# Design Overview

本目录是 EmotionQuant 设计文档的正式导航首页，采用三层结构：

1. 核心算法：`docs/design/core-algorithms/`
2. 核心基础设施：`docs/design/core-infrastructure/`
3. 外挂增强：`docs/design/enhancements/`

## 1. 阅读顺序

1. `docs/system-overview.md`
2. `docs/module-index.md`
3. `docs/design/core-algorithms/`
4. `docs/design/core-infrastructure/`
5. `docs/design/enhancements/`

## 2. 三层职责

### 2.1 核心算法

- 路径：`docs/design/core-algorithms/`
- 范围：MSS / IRS / PAS / Integration
- 约束：算法语义、评分口径、门禁逻辑属于冻结区，只能实现，不得改写语义

### 2.2 核心基础设施

- 路径：`docs/design/core-infrastructure/`
- 范围：Data Layer / Validation / Backtest / Trading / GUI / Analysis
- 原则：服务核心算法与核心功能；能在基础设施实现的，不上推到外挂层

### 2.3 外挂增强

- 路径：`docs/design/enhancements/`
- 范围：执行编排、契约守卫、可观测性、治理守卫等增强设计
- 原则：核心算法与核心基础设施未定义且不冲突的能力，才进入外挂层

## 3. 执行与权威口径

1. 执行主计划唯一入口：`docs/design/enhancements/eq-improvement-plan-core-frozen.md`
2. 外挂选型论证：`docs/design/enhancements/enhancement-selection-analysis_claude-opus-max_20260210.md`
3. 兼容指针：`docs/improvement-plans.md`（仅重定向说明，不是执行基线）

## 4. 边界规则

1. 核心算法优先：能在核心算法实现，就在核心算法实现。
2. 核心基础设施次级：能在基础设施实现，就在基础设施实现。
3. 外挂最后：核心算法与核心基础设施都未覆盖且不冲突时，才进入外挂。
4. 情绪优先与“单指标不得独立决策”铁律始终有效。
