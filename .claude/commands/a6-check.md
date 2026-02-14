# A6 完整检查（Spiral 圈收口）

执行 A6 阶段完整质量验证。Spiral 圈收口前的完整检查，包括测试、文档同步、技术债登记。

## 执行步骤

### 1. 测试验证（前置条件）

```bash
# 运行全量回归测试
pytest tests/ -v
```

检查项：

- [ ] 当前 Spiral 圈相关测试通过
- [ ] **全量回归测试通过**
- [ ] 测试覆盖率达标（建议 ≥80%）

### 2. Gate 完整检查

使用斜杠命令直接执行：

```text
/a6-check [spiral]
```

或者手动执行零容忍检查：

```bash
# 检查路径硬编码
grep -r "G:/EmotionQuant_data\|C:/\|D:/" --include="*.py" src/ tests/ 2>/dev/null

# 检查技术指标
grep -r "talib\|MA\|RSI\|MACD\|KDJ\|BOLL\|EMA\|SMA\|ATR\|DMI\|ADX" --include="*.py" src/ tests/ 2>/dev/null
```

如果用户没有提供 spiral 参数，请询问当前是哪个 Spiral 圈。

检查项：

- [ ] 路径硬编码检查通过（必须通过 `Config.from_env()` 读取）
- [ ] 技术指标检查通过（可用于对照/特征工程，但不得独立触发交易）
- [ ] 数据契约一致性
- [ ] S6 阶段无简化方案（TODO/FIXME/HACK/mock/fake）

### 3. 最小同步检查

根据 `CLAUDE.md` 第 7 节，每圈收口必须同步以下 5 项：

- [ ] `Governance/specs/spiral-s{N}/final.md`
- [ ] `Governance/record/development-status.md`
- [ ] `Governance/record/debts.md`
- [ ] `Governance/record/reusable-assets.md`
- [ ] `Governance/Capability/SPIRAL-CP-OVERVIEW.md`（只更新当圈状态）

### 4. 复用资产登记

- [ ] 识别可复用资产（数据模型、API、工具函数）
- [ ] 登记到 `Governance/record/reusable-assets.md`

### 5. 技术债处理

- [ ] 新增技术债已登记到 `Governance/record/debts.md`

### 6. 输出格式

```text
## A6 完整检查结果

**Spiral**: S{N} | **时间**: YYYY-MM-DD HH:MM

### 测试验证
- 单元测试: ✅ / ❌
- 回归测试: ✅ / ❌
- 覆盖率: XX%

### Gate 检查
- 全部通过: ✅ / ❌

### 最小同步（5 项）
- final.md: ✅ / ❌
- development-status.md: ✅ / ❌
- debts.md: ✅ / ❌
- reusable-assets.md: ✅ / ❌
- SPIRAL-CP-OVERVIEW.md: ✅ / ❌

### 复用资产
- 已登记 X 个资产

### 结论
[✅ 圈完成 / ❌ 需补充后重新检查]
```

### 7. 产物清单

完成 A6 后必须产出：

1. `Governance/specs/spiral-s{N}/final.md` - 圈总结文档
2. `Governance/specs/spiral-s{N}/review.md` - 评审记录文档

### 8. 权威文档

- `CLAUDE.md` - 第 7 节"每圈最小同步（5 项）"
- `Governance/Capability/SPIRAL-CP-OVERVIEW.md` - Spiral 路线
