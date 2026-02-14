# 评审报告 011：System Overview / Governance 交叉一致性

评审日期：2026-02-14  
评审范围：`docs/system-overview.md` + `Governance/steering/*` + `Governance/Capability/SPIRAL-CP-OVERVIEW.md` + `docs/naming-conventions.md`

---

## 1. 结论摘要

- 结论：总体一致性较高，总览与治理主控在铁律、Spiral 闭环、CP 术语、八层架构、本地优先上已形成同口径。
- 主要收益：治理与设计同口径可显著降低实现漂移与跨模块误读。
- 主要风险：仍有少量术语粒度差异，需要继续做消歧与导航补强。

---

## 2. 设计事实（文档证据）

1. 系统定位一致：面向 A 股、情绪驱动、Spiral 闭环。  
   证据：`docs/system-overview.md:11`、`Governance/steering/系统铁律.md:1`
2. 核心原则一致：情绪优先、单指标边界、本地优先、A 股规则刚性、闭环五件套。  
   证据：`docs/system-overview.md:21`、`docs/system-overview.md:25`、`docs/system-overview.md:26`、`Governance/steering/系统铁律.md:13`、`Governance/steering/系统铁律.md:15`、`Governance/steering/系统铁律.md:17`、`Governance/steering/CORE-PRINCIPLES.md:19`、`Governance/steering/CORE-PRINCIPLES.md:22`、`Governance/steering/CORE-PRINCIPLES.md:23`
3. 6A 执行约束与总览可行性说明一致：每圈 1 主目标、1-3 切片、无闭环不得收口。  
   证据：`docs/system-overview.md:89`、`docs/system-overview.md:91`、`Governance/steering/6A-WORKFLOW.md:18`、`Governance/steering/6A-WORKFLOW.md:21`
4. 闭环证据口径一致：`run/test/artifact/review/sync`。  
   证据：`Governance/Capability/SPIRAL-CP-OVERVIEW.md:27`、`Governance/steering/6A-WORKFLOW.md:21`
5. SoT 导航链基本闭合：System Overview 指向 Capability 总览；治理结构列出 TRD 与系统总览入口。  
   证据：`docs/system-overview.md:105`、`docs/system-overview.md:107`、`Governance/steering/GOVERNANCE-STRUCTURE.md:29`、`Governance/steering/GOVERNANCE-STRUCTURE.md:35`、`Governance/steering/GOVERNANCE-STRUCTURE.md:40`
6. 架构与命名口径一致：八层架构含 Integration；`unknown` 与推荐等级在命名规范中有权威定义。  
   证据：`docs/system-overview.md:32`、`docs/system-overview.md:37`、`docs/naming-conventions.md:27`、`docs/naming-conventions.md:135`、`docs/naming-conventions.md:137`

---

## 3. 实战正向收益来源（实战推断）

1. 收口效率收益：研发/回测/交易/分析按同一治理口径推进，减少反复解释成本。
2. 风险控制收益：铁律与 6A 同步约束让高风险改动更难带病上线。
3. 协作收益：CP/SoT 清晰后，跨模块负责人能快速定位权威文档执行同一契约。
4. 审计收益：统一闭环证据链利于复盘与问责，降低口头完成风险。

---

## 4. 一致性评估（重点）

### 4.1 已对齐项（强一致）

1. 铁律与总览原则同向，无硬冲突。
2. Spiral 与 6A 的“1 主目标 + 1-3 Slice + 五件套”同口径。
3. CP 术语与 `CP-*.md` 命名兼容策略一致。
4. 本地数据优先与 A 股刚性规则贯穿总览与治理。

### 4.2 仍需消歧项（弱不一致/表述差）

1. 回测“主选/主线”术语易混淆：总览强调 `Qlib` 主选研究，TRD 强调本地向量化收口基线。  
   证据：`docs/system-overview.md:69`、`docs/system-overview.md:72`、`Governance/steering/TRD.md:69`
2. A 股规则在总览为简写，在铁律/原则中为细写（含板块涨跌停比例与申万行业）。  
   证据：`docs/system-overview.md:25`、`Governance/steering/系统铁律.md:17`、`Governance/steering/CORE-PRINCIPLES.md:22`
3. SoT 可发现性可继续增强：总览列路线入口，但治理入口分散于 Capability/SpiralRoadmap/TRD 多处。  
   证据：`docs/system-overview.md:105`、`docs/system-overview.md:107`、`Governance/steering/GOVERNANCE-STRUCTURE.md:35`

---

## 5. 实战沙盘演示（治理层）

1. 场景 A（标准收口）  
   条件：具备 `run/test/artifact/review/sync`。  
   预期：允许收口并更新 Spiral 主控。
2. 场景 B（缺自动化测试）  
   条件：无 test 证据。  
   预期：按 6A 退出条件不得收口。  
   证据：`Governance/steering/6A-WORKFLOW.md:95`、`Governance/steering/6A-WORKFLOW.md:99`
3. 场景 C（契约变更未同步 CP）  
   条件：字段/语义变化但未更新 CP。  
   预期：视为治理违规，需先完成契约同步。  
   证据：`Governance/Capability/SPIRAL-CP-OVERVIEW.md:120`、`Governance/Capability/SPIRAL-CP-OVERVIEW.md:122`
4. 场景 D（本地数据绕过）  
   条件：主流程直连远端。  
   预期：触发铁律阻断。  
   证据：`Governance/steering/系统铁律.md:15`

---

## 6. 防御措施盘点

1. 铁律清单化，违规后果明确（阻断/不得收口）。
2. 6A 退出条件可执行，防止伪闭环。
3. SoT 路由明确，降低多版本真相风险。
4. CP 主控 + 最小同步 5 项，兼顾治理强度与单人开发负担。
5. 命名规范权威化，减少跨模块语义漂移。

---

## 7. 需要进化的点（优先级）

1. P0：术语消歧补丁：在总览/TRD 增加“研究主选 vs 收口主线”双轨注释。
2. P0：总览导航补强：在总览显式补 `Governance/steering/TRD.md` 入口。
3. P1：治理一致性自动检查：扫描铁律词条、6A 五件套、CP 同步项并提示偏差。
4. P1：A 股规则精度注释：总览简写条款链接到铁律精度定义。
5. P2：跨文档变更联动模板：契约/风控/数据边界变更给出同步清单。

---

## 8. 下一步（执行建议）

1. 先做 SoT 链接修订（system-overview 增补 TRD，补回测双轨术语注释）。
2. 再做治理一致性脚本草案（静态扫描关键条款）。
3. 继续进入下一份：`review-012-naming-contracts-20260214.md`。
