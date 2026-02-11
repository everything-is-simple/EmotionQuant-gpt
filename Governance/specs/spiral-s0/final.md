# Spiral S0 Final

## 1. 本圈目标达成情况

- 目标：完成设计目录重构与入口文档对齐，收敛为单一执行口径。
- 结果：已完成，设计体系统一为“核心算法 + 核心基础设施 + 外挂增强”三层结构。

## 2. 闭环证据

- run: 完成目录重构落地（`analysis/backtest/data-layer/gui/trading/validation` 迁入 `docs/design/core-infrastructure/`；`docs/improvement-plans/` 迁入 `docs/design/enhancements/`）。
- test: 执行全仓路径扫描，确认入口文档已切换到新路径口径（归档目录除外）。
- artifact:
  - `docs/design/README.md`（新增三层设计导航首页）
  - `docs/improvement-plans.md`（兼容指针）
  - `docs/module-index.md` / `docs/system-overview.md` / `Governance/steering/GOVERNANCE-STRUCTURE.md` 等入口文档对齐更新
- review: `Governance/specs/spiral-s0/review.md`

## 3. 目录重构影响清单

1. 目录结构变更：
   - 新增 `docs/design/core-infrastructure/`
   - 新增 `docs/design/enhancements/`
   - 新增 `docs/design/README.md`
2. 迁移模块：
   - `docs/design/analysis/` -> `docs/design/core-infrastructure/analysis/`
   - `docs/design/backtest/` -> `docs/design/core-infrastructure/backtest/`
   - `docs/design/data-layer/` -> `docs/design/core-infrastructure/data-layer/`
   - `docs/design/gui/` -> `docs/design/core-infrastructure/gui/`
   - `docs/design/trading/` -> `docs/design/core-infrastructure/trading/`
   - `docs/design/validation/` -> `docs/design/core-infrastructure/validation/`
   - `docs/improvement-plans/` -> `docs/design/enhancements/`
3. 入口文档对齐：
   - `README.md`
   - `README.en.md`
   - `AGENTS.md`
   - `CLAUDE.md`
   - `WARP.md`
   - `docs/module-index.md`
   - `docs/system-overview.md`
   - `Governance/steering/GOVERNANCE-STRUCTURE.md`
4. 兼容策略：
   - 保留 `docs/improvement-plans.md` 作为迁移指针，避免旧入口立即断链
5. 风险与边界：
   - 核心算法语义未改，仅目录与引用治理重构
   - 历史归档目录保留旧路径表述，不作为现行执行口径

## 4. 同步记录

- [ ] `Governance/record/development-status.md`
- [ ] `Governance/record/debts.md`
- [ ] `Governance/record/reusable-assets.md`
- [ ] `Governance/Capability/SPIRAL-CP-OVERVIEW.md`

## 5. 下一圈建议

- 主目标：
- CP 组合：
- 预估风险：


