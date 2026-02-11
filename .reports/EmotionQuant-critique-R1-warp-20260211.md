# EmotionQuant 全文档批判性审查 — 第 1 轮

**审查人**: Warp (Claude Opus)
**日期**: 2026-02-11
**轮次**: R1
**范围**: `Governance/steering/` 4 个活跃文件 × 与 WARP.md/CLAUDE.md/AGENTS.md/core-algorithms README 交叉一致性
**累计**: 本轮 6 项

---

## 审查方法

逐文件精读 `Governance/steering/` 下全部 4 个活跃文件（6A-WORKFLOW.md、CORE-PRINCIPLES.md、GOVERNANCE-STRUCTURE.md、系统铁律.md），与以下权威源交叉对比：

- WARP.md / CLAUDE.md / AGENTS.md（代理指令文件，刚同步为同一精度）
- `docs/design/core-algorithms/README.md`（冻结区定义）
- `docs/naming-conventions.md`（命名权威）

重点检查：铁律表述精度、SoT 完整性、冻结区范围一致性、路径引用有效性。

---

## 发现汇总

| ID | 优先级 | 文件 | 位置 | 问题 |
|---|---|---|---|---|
| P2-R1-01 | P2 | 系统铁律.md | §1 铁律5 (line 17) | 铁律5 A 股规则描述精度不足，缺少涨跌停具体比率与申万行业 |
| P2-R1-02 | P2 | CORE-PRINCIPLES.md | §2 原则4 (line 22) | 同上，A 股规则描述与铁律权威文件一样偏简 |
| P2-R1-03 | P2 | GOVERNANCE-STRUCTURE.md | §2 SoT (lines 24-34) | SoT 矩阵缺少 5 项：能力契约、核心原则、命名规范、系统总览、模块索引 |
| P2-R1-04 | P2 | 6A-WORKFLOW.md | §3 A3 (line 44) | 冻结区表述遗漏 Integration：只写"MSS/IRS/PAS+Validation"，实际 core-algorithms 冻结区含 5 模块 |
| P3-R1-05 | P3 | GOVERNANCE-STRUCTURE.md | §1 (line 14) | SpiralRoadmap 描述"新系统实现路线（按圈闭环）"，但目录实际仅含候选草稿 |
| P3-R1-06 | P3 | GOVERNANCE-STRUCTURE.md | §4 (lines 55-58) | .claude 资产迁移方向列表缩进层级错乱 |

---

## 问题详述

### P2-R1-01 — 系统铁律.md §1 铁律5 精度不足

**位置**: `Governance/steering/系统铁律.md` line 17

**当前**:
```
| 铁律5 A股规则刚性执行 | 必须遵守 T+1、涨跌停、交易时段 | 阻断 |
```

**问题**: WARP.md/CLAUDE.md/AGENTS.md 铁律5 描述为：`T+1、涨跌停（主板10%/创业板科创板20%/ST 5%）、交易时段、申万行业`。作为铁律权威源，`系统铁律.md` 反而是最简版，缺少：
1. 涨跌停具体比率（主板10%/创业板科创板20%/ST 5%）
2. 申万行业分类

**修复建议**: 将 line 17 的核心要求改为 `必须遵守 T+1、涨跌停（主板10%/创业板科创板20%/ST 5%）、交易时段、申万行业`。

---

### P2-R1-02 — CORE-PRINCIPLES.md §2 原则4 同样偏简

**位置**: `Governance/steering/CORE-PRINCIPLES.md` line 22

**当前**:
```
4. 严守 A 股规则（T+1、涨跌停、交易时段）。
```

**问题**: 与 P2-R1-01 同源问题。铁律权威文件精度提升后，CORE-PRINCIPLES 应同步。

**修复建议**: 改为 `4. 严守 A 股规则（T+1、涨跌停（主板10%/创业板科创板20%/ST 5%）、交易时段、申万行业）。`

---

### P2-R1-03 — GOVERNANCE-STRUCTURE.md §2 SoT 矩阵不完整

**位置**: `Governance/steering/GOVERNANCE-STRUCTURE.md` lines 24-34

**当前**: SoT 矩阵有 9 行。

**问题**: WARP.md/CLAUDE.md §8.2 的 SoT 矩阵含 9 行，其中 5 项在 GOVERNANCE-STRUCTURE.md 中缺失：

| 缺失 SoT | WARP.md 中的权威文件 |
|---|---|
| 能力契约 | `Governance/Capability/CP-*.md`（CP） |
| 核心原则 | `Governance/steering/CORE-PRINCIPLES.md` |
| 命名规范 | `docs/naming-conventions.md` |
| 系统总览 | `docs/system-overview.md` |
| 模块索引 | `docs/module-index.md` |

GOVERNANCE-STRUCTURE.md 作为治理结构权威文件，其 SoT 矩阵应是最完整的超集。

**修复建议**: 在 §2 表格末尾补充上述 5 行。

---

### P2-R1-04 — 6A-WORKFLOW.md §3 A3 冻结区遗漏 Integration

**位置**: `Governance/steering/6A-WORKFLOW.md` line 44

**当前**:
```
不改核心冻结区（情绪主逻辑、MSS/IRS/PAS+Validation 核心语义、Spiral+CP 主路线）。
```

**问题**: `docs/design/core-algorithms/README.md` §5.1 明确：本目录属于核心算法冻结区，覆盖 **5 个核心模块**（MSS/IRS/PAS/Validation/Integration）。6A-WORKFLOW 中遗漏了 Integration。

**修复建议**: 改为 `不改核心冻结区（情绪主逻辑、MSS/IRS/PAS/Validation/Integration 核心语义、Spiral+CP 主路线）。`

---

### P3-R1-05 — GOVERNANCE-STRUCTURE.md §1 SpiralRoadmap 描述过宽

**位置**: `Governance/steering/GOVERNANCE-STRUCTURE.md` line 14

**当前**:
```
- `Governance/SpiralRoadmap/`：新系统实现路线（按圈闭环）
```

**问题**: 该目录当前仅含 `draft/` 子目录（2 个候选草稿 + 1 个 README）。不存在正式的"实现路线"文件。§2 SoT 行 31 已正确标注为"候选草稿"，但 §1 描述仍为宽泛叙述。

**修复建议**: 改为 `- Governance/SpiralRoadmap/：实现路线候选草稿`（与 README.md 目录导航一致）。

---

### P3-R1-06 — GOVERNANCE-STRUCTURE.md §4 列表缩进错乱

**位置**: `Governance/steering/GOVERNANCE-STRUCTURE.md` lines 55-58

**当前**:
```markdown
- `.claude/` 保留为历史工具资产，不作为当前强制流程。
- 可复用内容迁移方向：
- 命令级检查逻辑 -> `Governance/steering/`
  - 规则类约束 -> `Governance/steering/系统铁律.md`
  - 经验模板 -> `Governance/Capability/SPIRAL-TASK-TEMPLATE.md`
```

**问题**: line 56 "- 命令级检查逻辑" 与 line 55 "- 可复用内容迁移方向" 在同一缩进层级，但语义上应该是子项。lines 57-58 是 line 56 的子项，缩进正确。

**修复建议**:
```markdown
- `.claude/` 保留为历史工具资产，不作为当前强制流程。
- 可复用内容迁移方向：
  - 命令级检查逻辑 → `Governance/steering/`
  - 规则类约束 → `Governance/steering/系统铁律.md`
  - 经验模板 → `Governance/Capability/SPIRAL-TASK-TEMPLATE.md`
```

---

## 无问题确认（Clean Pass）

- **6A 六步定义**: 6A-WORKFLOW.md ↔ WARP.md/CLAUDE.md/AGENTS.md §4.1 完全一致 ✅
- **执行约束 5 条**: 三文件一致 ✅
- **退出条件**: 6A-WORKFLOW.md §6 ↔ WARP.md §4.3 一致 ✅
- **分支策略**: 一致 ✅
- **每圈最小同步 5 项**: 4 个文件交叉一致（6A §A6、CORE-PRINCIPLES §5、GOVERNANCE-STRUCTURE §3、WARP §4.5） ✅
- **技术指标边界**: 系统铁律 §2 ↔ CORE-PRINCIPLES §2.1 ↔ WARP §3 注释 表述一致 ✅
- **归档策略**: GOVERNANCE-STRUCTURE §5 ↔ WARP §8.3 一致 ✅
- **路径引用有效性**: 所有文件中的路径引用均指向存在的文件/目录 ✅
- **workflow/archive-compat-v6-20260210/ README**: 内容准确，指向正确的权威入口 ✅

---

## 统计

| 优先级 | 数量 | 编号 |
|--------|------|------|
| P2 | 4 | R1-01, R1-02, R1-03, R1-04 |
| P3 | 2 | R1-05, R1-06 |
| **合计** | **6** | |

---

## 下一轮预告

R2 将检查 `Governance/Capability/`（SPIRAL-CP-OVERVIEW.md + SPIRAL-TASK-TEMPLATE.md + CP-01~CP-10，共 12 个文件）。
