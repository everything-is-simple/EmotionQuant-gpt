# EmotionQuant 模块索引（Spiral 实现版）

**版本**: v4.2.0
**最后更新**: 2026-02-11
**状态**: 实现前最终模块清单

---

## 1. 模块结构

```
docs/
├── system-overview.md
├── module-index.md
├── naming-conventions.md
├── design/
│   ├── core-algorithms/
│   │   ├── mss/
│   │   ├── irs/
│   │   ├── pas/
│   │   └── integration/
│   ├── core-infrastructure/
│   │   ├── validation/
│   │   ├── data-layer/
│   │   ├── backtest/
│   │   │   └── backtest-engine-selection.md
│   │   ├── trading/
│   │   ├── gui/
│   │   └── analysis/
│   └── enhancements/
│       ├── eq-improvement-plan-core-frozen.md
│       ├── enhancement-selection-analysis_claude-opus-max_20260210.md
│       └── drafts/
```

---

## 2. 核心算法模块

### 2.1 MSS

- 路径：`docs/design/core-algorithms/mss/`
- 输出：温度、周期、趋势、仓位建议

### 2.2 IRS

- 路径：`docs/design/core-algorithms/irs/`
- 输出：行业评分、轮动状态、行业排名

### 2.3 PAS

- 路径：`docs/design/core-algorithms/pas/`
- 输出：机会评分、等级、方向、风险收益比

### 2.4 Integration

- 路径：`docs/design/core-algorithms/integration/`
- 输出：统一推荐信号与解释字段

---

## 3. 验证模块（新增，必须）

### 3.1 Factor & Weight Validation

- 路径：`docs/design/core-infrastructure/validation/`
- 作用：
  - 因子有效性验证（IC/RankIC/稳定性/衰减）
  - 权重方案验证（baseline 对照、OOS 评估、风险约束）
  - 输出 Gate 决策（PASS/WARN/FAIL）

> 该模块是实现前必须补齐的“证据层”，避免因子和权重长期拍脑袋。

---

## 4. 基础设施模块

### 4.1 Data Layer

- 路径：`docs/design/core-infrastructure/data-layer/`
- 存储口径：Parquet + DuckDB 单库优先

### 4.2 Backtest

- 路径：`docs/design/core-infrastructure/backtest/`
- 选型口径：接口优先，可替换引擎

### 4.3 Trading

- 路径：`docs/design/core-infrastructure/trading/`
- 重点：纸上交易先行，风险规则可审计

### 4.4 GUI

- 路径：`docs/design/core-infrastructure/gui/`
- 主线技术：Streamlit + Plotly

### 4.5 Analysis

- 路径：`docs/design/core-infrastructure/analysis/`
- 重点：绩效归因与日报

---

## 5. 外挂增强设计

- 路径：`docs/design/enhancements/`
- 定位：在不改核心算法与核心基础设施语义前提下，承载可审计的增强方案
- 执行基线：`docs/design/enhancements/eq-improvement-plan-core-frozen.md`
- 选型论证：`docs/design/enhancements/enhancement-selection-analysis_claude-opus-max_20260210.md`

---

## 6. 与 ROADMAP 的关系

- ROADMAP 文件采用 Capability Pack（CP）语义，不是线性闸门。
- 文件名采用 `CP-*.md`，执行时按 CP 理解。
- Validation 模块在路线图中对应 `CP-10`（`Governance/Capability/CP-10-validation.md`）。
- 每圈 Spiral 从能力包中取切片实现，收口时必须同步更新文档与 record。

---

## 变更记录

| 版本 | 日期 | 变更 |
|---|---|---|
| v4.2.0 | 2026-02-11 | 对齐目录重构：设计体系统一为 `core-algorithms + core-infrastructure + enhancements`，并新增外挂增强入口说明 |
| v4.1.0 | 2026-02-07 | 增补 Validation 对应 CP-10 的路线映射 |
| v4.0.0 | 2026-02-07 | 新增 Validation 模块与回测选型文档；统一 Spiral 口径 |
| v3.1.0 | 2026-02-05 | 线性重构版 |

---

## 7. 设计迁移说明

- 过渡期冲突处理：`docs/design/README-spiral-transition.md`



