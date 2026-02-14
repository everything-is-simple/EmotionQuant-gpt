# design-review-sandbox 修复记录（2026-02-14）

## 0. 备份

- 已完成系统文档打包：`.reports/system-docs-backup-20260214-131149.zip`
- 打包范围：`docs/`、`Governance/`、`AGENTS.md`

## 1. 统一结构修复（12 份报告）

- 文件范围：`review-001` 到 `review-012`
- 修复项：
1. 将 `4.1/4.2` 子段标题统一由二级标题改为三级标题（`##` -> `###`）。
2. 统一校验为 8 段模板：`1..8` 主段完整且顺序一致。
3. 校验“实战沙盘演示”章节在 12 份报告中全部存在。

## 2. 单文件专项修复

1. `review-001-mss-20260214.md`
- 新增 `## 5. 实战沙盘演示（预期行为）`（4 个场景）
- 原章节重排：
  - `防御措施盘点`：`5 -> 6`
  - `需要进化的点`：`6 -> 7`
  - `下一步`：`7 -> 8`

2. `review-011-system-overview-governance-20260214.md`
- 修复证据行英文连接词：`to` -> `到`

3. `review-001/002/003`
- 章节标题统一：`## 4. A 股适配阶段与不适配阶段`

## 3. 校验结果

1. 子段层级问题：已清零（无 `^## 4.1` / `^## 4.2` 残留）。
2. 英文连接词笔误：已清零（无 `to` 残留）。
3. 模板完整性：12/12 通过（均为 8 段结构）。

## 4. 备注

- 本轮为结构与一致性修复，未改变各报告核心结论立场。
- 若继续下一轮，建议按 `review-001 -> review-012` 逐份做“证据行号复核 + 表述压缩 + 风险优先级复评”内容级精修。

## 5. 第二轮进度（内容级精修）

1. 已完成：`review-001-mss-20260214.md`
- 逐条复核证据行号并纠偏：
  - 核心输出证据由 `mss-algorithm.md:14` 校正为 `mss-algorithm.md:16`
  - Integration 角色证据由 `integration-algorithm.md:226` 优化为 `integration-algorithm.md:92`
- 全文完成表述压缩（不改变原结论立场）
- 结构完整性复核通过（8 段模板齐全）

2. 已完成：`review-002-irs-20260214.md`
- 逐条复核证据行号并纠偏：
  - 输出契约证据补齐 `rotation_status` 与 `neutrality` 行位点（`irs-algorithm.md:20/:23`）
  - “尺度约束”证据补齐 `count->ratio->zscore` 直接位点（`irs-algorithm.md:411`）
  - Integration 软约束证据补齐规则总述位点（`integration-algorithm.md:225`）
- 删除证据不足表述并压缩全文（结论方向不变）
- 结构完整性复核通过（8 段模板齐全）

3. 已完成：`review-003-pas-20260214.md`
- 逐条复核证据行号并纠偏：
  - 输出契约证据补齐 `opportunity_grade/direction` 行位点（`pas-algorithm.md:20/:21`）
  - 行为因子 ±20% 映射证据由变更记录位点改为规则位点（`pas-algorithm.md:161`）
  - RR 口径冲突条目移除，改为“算法与数据模型已对齐”并双证据确认（`pas-algorithm.md:345` + `pas-data-models.md:286`）
- 全文完成表述压缩（结论方向不变）
- 结构完整性复核通过（8 段模板齐全）

4. 已完成：`review-004-validation-20260214.md`
- 逐条复核证据行号并纠偏：
  - 补齐 Validation 双目标证据（`factor-weight-validation-algorithm.md:11/:14`）
  - 权重验证条件证据改为规则位点（`...:89/:91/:115/:118`）
  - Gate 关键治理字段改为精确字段位点（`data-models.md:95-98`）
- 全文完成表述压缩（结论方向不变）
- 结构完整性复核通过（8 段模板齐全）

5. 已完成：`review-005-integration-20260214.md`
- 逐条复核证据行号并纠偏：
  - Gate 输入字段证据细化到字段位点（`integration-algorithm.md:79/:80/:81`）
  - 软约束与排序证据改为规则位点（`...:225/:228/:229/:234`，`...:363/:364/:365`）
  - 输出可追溯证据改为模型字段位点（`integration-data-models.md:153/:155/:158/:161/:164`）
- 全文完成表述压缩（结论方向不变）
- 结构完整性复核通过（8 段模板齐全）

6. 已完成：`review-006-backtest-20260214.md`
- 逐条复核证据行号并纠偏：
  - 引擎选型证据细化到三轨位点（`backtest-engine-selection.md:13/:14/:15`）
  - 执行约束沙盘证据补齐测试用例期望位点（`backtest-test-cases.md:13/:33`）
  - 质量门禁证据改为条目位点（`backtest-test-cases.md:163/:167/:171`）
- 全文完成表述压缩（结论方向不变）
- 结构完整性复核通过（8 段模板齐全）

7. 已完成：`review-007-trading-20260214.md`
- 逐条复核证据行号并纠偏：
  - 风控检查描述修正为“多段检查”（文档实际为 1/2/2.5/3/4/5 共六类）
  - 风控阈值证据补齐行业位点（`trading-algorithm.md:180`）
  - 沙盘拒单证据细化到具体条件位点（`...:164/:167/:169`）
- 全文完成表述压缩（结论方向不变）
- 结构完整性复核通过（8 段模板齐全）

8. 已完成：`review-008-analysis-20260214.md`
- 逐条复核证据行号并纠偏：
  - 归因切换证据细化到上下文分支与三路贡献位点（`analysis-algorithm.md:170/:172/:174/:199/:201`）
  - 风险摘要证据细化到字段位点（`analysis-data-models.md:199-205`）
  - 防御“外部库边界”补充直接证据（`analysis-api.md:13`）
- 全文完成表述压缩（结论方向不变）
- 结构完整性复核通过（8 段模板齐全）

9. 已完成：`review-009-gui-20260214.md`
- 逐条复核证据行号并纠偏：
  - GUI 定位证据补齐“信号展示/只读展示”位点（`gui-algorithm.md:14/:16`）
  - 缓存策略证据补齐“交易执行数据 1 分钟”位点（`gui-algorithm.md:260`）
  - 异常反馈证据聚焦用户态三条消息位点（`gui-information-flow.md:468/:469/:470`）
- 全文完成表述压缩（结论方向不变）
- 结构完整性复核通过（8 段模板齐全）

10. 已完成：`review-010-data-layer-20260214.md`
- 逐条复核证据行号并纠偏：
  - 降级字段证据细化到三字段位点（`data-layer-data-models.md:229/:230/:231`）
  - L3 执行关键字段证据改为关键列位点（`...:441/:443/:450`）
  - 存储边界证据聚焦主库/ops 库位点（`data-layer-api.md:682/:683`）
- 全文完成表述压缩（结论方向不变）
- 结构完整性复核通过（8 段模板齐全）

11. 已完成：`review-011-system-overview-governance-20260214.md`
- 逐条复核证据行号并纠偏：
  - 原区间证据改为关键规则位点（`system-overview.md:21/:25/:26`，`6A-WORKFLOW.md:18/:21`）
  - SoT 导航证据聚焦入口位点（`system-overview.md:105/:107`，`GOVERNANCE-STRUCTURE.md:29/:35/:40`）
  - 6A 收口失败沙盘证据细化到退出条件条目位点（`6A-WORKFLOW.md:95/:99`）
- 全文完成表述压缩（结论方向不变）
- 结构完整性复核通过（8 段模板齐全）

12. 已完成：`review-012-naming-contracts-20260214.md`
- 逐条复核证据行号并纠偏：
  - 移除过期 P0 冲突叙述（`pas-data-models >= 0`），改为“RR 口径已对齐”并补四端证据（`pas-algorithm.md:22/:345`、`pas-data-models.md:286`、`trading-algorithm.md:52`、`backtest-algorithm.md:103`）
  - Validation->Integration 桥接证据细化到“业务键 -> 数值对象”位点（`factor-weight-validation-api.md:127/:132`、`factor-weight-validation-data-models.md:95/:162`、`integration-api.md:91/:102`）
  - 代码字段契约证据补齐“命名规范 + Data Layer 转换边界”双位点（`naming-conventions.md:280/:281`、`data-layer-api.md:612/:614/:882`）
- 全文完成表述压缩（结论方向不变）
- 结构完整性与引用解析复核通过（`sections=8; seq=1..8`，`ALL_REFERENCES_RESOLVED`）

13. 已完成：命名/契约一致性 P0 自动检查落地
- 新增脚本：`scripts/quality/naming_contracts_check.py`
  - 覆盖 6 类关键契约：`sideways/flat`、`unknown`、`risk_reward_ratio` 命名与 `>=1.0` 门槛、`STRONG_BUY=75`、`stock_code/ts_code` 分层边界、`PASS/WARN/FAIL` Gate 语义
  - 当前基线检查通过：`[contracts] pass (26 checks)`
- 集成入口：`scripts/quality/local_quality_check.py`
  - 新增 `--contracts` 参数，支持与现有 `--session/--scan` 统一执行
- 单测补齐：
  - 新增 `tests/unit/scripts/test_naming_contracts_check.py`
  - 更新 `tests/unit/scripts/test_local_quality_check.py`
  - 新增 `tests/conftest.py`（确保 `scripts.*` 可导入）
  - 针对当前环境权限限制，测试临时目录改用仓库内 `.reports/.tmp-test-artifacts`
- 验证结果：
  - `pytest tests/unit/scripts/test_local_quality_check.py tests/unit/scripts/test_naming_contracts_check.py` -> 7 passed
  - `C:\\miniconda3\\python.exe -m scripts.quality.local_quality_check --contracts` -> pass
