# EmotionQuant 全文档批判性审查 — 第 3 轮

**审查人**: Warp (Claude Opus)
**日期**: 2026-02-11
**轮次**: R3
**范围**: `Governance/record/`（3）+ `Governance/specs/spiral-s0/`（3）+ `Governance/SpiralRoadmap/draft/`（3）= 9 个活跃文件
**累计**: R1 6 + R2 6（已修复）+ 本轮 6 = **18 项**

---

## 审查方法

逐文件精读 9 个文件，与以下权威源交叉对比：

- GitHub 远程仓库实际 URL
- `Governance/Capability/` CP 文件清单（R2 已验证）
- `docs/design/` 目录结构（Validation 归属 core-algorithms，R1 已确认）
- `Governance/steering/6A-WORKFLOW.md`（同步清单权威）
- `Governance/specs/spiral-s0/review.md`（S0 完成状态）

---

## 发现汇总

| ID | 优先级 | 文件 | 位置 | 问题 |
|---|---|---|---|---|
| P2-R3-01 | P2 | development-status.md | L5 | 仓库地址 `EmotionQuant_beta` 已过时，当前仓库为 `EmotionQuant-gpt` |
| P2-R3-02 | P2 | development-status.md | L22 | "9 个能力包" 应为 "10 个能力包"（CP-01 ~ CP-10） |
| P2-R3-03 | P2 | 两份草稿路线图 | GPT5 L64-65 / Claude L960 | Validation 路径仍用 `core-infrastructure/validation/`，应为 `core-algorithms/validation/` |
| P2-R3-04 | P2 | GPT5 Codex draft | L5, L55 | 对 Claude 详细稿的引用路径错误：指向 `docs/design/enhancements/` 而非 `Governance/SpiralRoadmap/draft/` |
| P3-R3-05 | P3 | final.md | §4 (L49-52) | 同步清单 4 项全部未勾选，但 review.md §4 已标"通过" |
| P3-R3-06 | P3 | final.md | §5 (L56-58) | "下一圈建议"三项全空（主目标/CP 组合/预估风险） |

---

## 问题详述

### P2-R3-01 — development-status.md 仓库地址过时

**位置**: `Governance/record/development-status.md` line 5

**当前**: `https://github.com/everything-is-simple/EmotionQuant_beta`

**问题**: 当前仓库 remote 为 `https://github.com/everything-is-simple/EmotionQuant-gpt`（`EmotionQuant_beta` 是旧仓库名）。作为活跃治理文档，地址错误会误导协作者或外部读者。

**修复建议**: 改为 `https://github.com/everything-is-simple/EmotionQuant-gpt`。

---

### P2-R3-02 — development-status.md CP 数量不一致

**位置**: `Governance/record/development-status.md` line 22

**当前**: "9 个能力包文档统一为 CP 模板"

**问题**: 当前 `Governance/Capability/` 包含 CP-01 ~ CP-10 共 10 个能力包。"9 个" 与实际不符。

**修复建议**: 改为 "10 个能力包文档统一为 CP 模板"。

---

### P2-R3-03 — 两份草稿路线图 Validation 路径过时

**位置**:
- `spiral-execution-roadmap-candidate_gpt5-codex_20260210.md` lines 64-65
- `spiral-full-roadmap-detailed_claude-opus-max_20260210.md` line 960

**当前**: 引用 `docs/design/core-infrastructure/validation/factor-weight-validation-*.md`

**问题**: Validation 已迁入 `docs/design/core-algorithms/validation/`（R1 确认，GOVERNANCE-STRUCTURE.md SoT 已更新）。虽然草稿标记为"仅供参考"，路径错误仍会误导读者定位设计文档。

**修复建议**:
- GPT5 L64-65: `core-infrastructure` → `core-algorithms`
- Claude L960: `core-infrastructure` → `core-algorithms`

---

### P2-R3-04 — GPT5 Codex 对 Claude 详细稿引用路径错误

**位置**: `spiral-execution-roadmap-candidate_gpt5-codex_20260210.md` lines 5, 55

**当前**:
```
作为 `docs/design/enhancements/spiral-full-roadmap-detailed_claude-opus-max_20260210.md` 的校正后执行稿
```

**问题**: Claude 详细稿实际位于 `Governance/SpiralRoadmap/draft/`，非 `docs/design/enhancements/`。路径断链。

**修复建议**: 两处均改为 `Governance/SpiralRoadmap/draft/spiral-full-roadmap-detailed_claude-opus-max_20260210.md`。

---

### P3-R3-05 — final.md 同步清单未勾选

**位置**: `Governance/specs/spiral-s0/final.md` §4 lines 49-52

**当前**:
```
- [ ] `Governance/record/development-status.md`
- [ ] `Governance/record/debts.md`
- [ ] `Governance/record/reusable-assets.md`
- [ ] `Governance/Capability/SPIRAL-CP-OVERVIEW.md`
```

**问题**: review.md §4 已标"通过"（`[x] 通过`），表示本圈审查已完成。但 final.md 同步清单 4 项仍全部未勾选，说明要么同步未执行，要么执行后未更新勾选状态。

**修复建议**: 若同步已执行则勾选；若未执行，应在下一次 S0 收口时补充同步。

---

### P3-R3-06 — final.md 下一圈建议为空

**位置**: `Governance/specs/spiral-s0/final.md` §5 lines 56-58

**当前**:
```
- 主目标：
- CP 组合：
- 预估风险：
```

**问题**: S0 治理工作已标"通过"，但未给出下一圈（S0 数据闭环或 S1）的建议。空白的"下一圈建议"降低了 final.md 作为圈间桥梁的价值。

**修复建议**: 补充 S0 数据闭环（或 S1）的主目标、CP 组合、预估风险。例如：
```
- 主目标：S0 数据最小闭环（CP-01 单日采集→落盘→快照→测试）
- CP 组合：CP01-S1, CP01-S2
- 预估风险：TuShare token 可用性、首圈脚手架搭建工时
```

---

## 无问题确认（Clean Pass）

- **debts.md 分级标准 / 处理时限**: P0-P3 定义清晰，与 6A-WORKFLOW 错误分级一致 ✅
- **debts.md 已清偿记录**: TD-GOV-001~005 描述与治理改革实际一致 ✅
- **debts.md 备注规则**: "技术债必须在每圈 final.md 中复核" 与 6A-WORKFLOW Sync 阶段对齐 ✅
- **reusable-assets.md 路径正确性**: S-GOV-001~004、S-DES-001~004、A-CFG-001~002、B-CODE-003 路径全部正确 ✅
- **reusable-assets.md A-DES-004 Validation 路径**: `docs/design/core-algorithms/validation/*` 已指向正确位置 ✅
- **requirements.md S0 In/Out Scope**: 与 CP-01 契约和 development-status S0 目标一致 ✅
- **requirements.md 闭环证据三件套**: run/test/artifact 具体且可复现 ✅
- **review.md 偏差与风险处理**: 记录清晰，处理决策可追溯 ✅
- **SpiralRoadmap/draft/README.md**: 主计划权威引用路径正确，文件清单完整 ✅
- **GPT5 Codex 全局执行契约**: 冻结边界/切片预算/五件套/错误分级/Strict 6A 规则与治理体系一致 ✅
- **Claude Opus 详细稿整体结构**: S0-S6 各圈存在意义/进入条件/边界/错误处理/验收/遗产结构完整 ✅

---

## 统计

| 优先级 | 数量 | 编号 |
|--------|------|------|
| P2 | 4 | R3-01, R3-02, R3-03, R3-04 |
| P3 | 2 | R3-05, R3-06 |
| **合计** | **6** | |

**累计（R1-R3）**: 6 + 6 + 6 = **18 项**（R1-R2 全部已修复）

---

## 下一轮预告

R4 将检查 `docs/` 根文档（system-overview.md + module-index.md + naming-conventions.md + improvement-plans.md）+ `docs/design/` READMEs，约 5-7 个文件。
