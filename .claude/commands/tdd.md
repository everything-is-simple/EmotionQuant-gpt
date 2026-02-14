# TDD 提醒（A3 实现阶段）

在 A3 实现阶段，提醒 TDD（测试驱动开发）原则和零容忍规则。

## TDD 核心流程

```text
1. RED（红灯）: 先写失败的测试
   pytest tests/unit/xxx_test.py -v  # 应该 FAIL

2. GREEN（绿灯）: 写最小代码让测试通过
   pytest tests/unit/xxx_test.py -v  # 应该 PASS

3. REFACTOR（重构）: 改进代码质量
   black src/ && flake8 src/
   pytest tests/ -v  # 所有测试仍然 PASS
```

## 零容忍规则

### 1. 路径硬编码（最严重）

```python
# ❌ 绝对禁止
db_path = "G:/EmotionQuant_data/database/emotionquant.db"
cache_dir = "data/cache/"

# ✅ 必须这样
from utils.config import Config
config = Config.from_env()
db_path = config.database_path
cache_dir = config.cache_dir
```

### 2. 字段命名违规

```python
# ❌ 禁止自创字段名
@dataclass
class Bar:
    date: str  # 错误！应该是 trade_date
    symbol: str  # 错误！应该是 ts_code

# ✅ 必须符合 docs/naming-conventions.md
@dataclass
class Bar:
    ts_code: str       # TuShare 格式，如 000001.SZ
    trade_date: str    # 交易日，YYYYMMDD 格式
    open: float
    high: float
    low: float
    close: float
    volume: float
    amount: float
```

### 3. TDD 违规

```text
❌ 先实现后测试
❌ 批量实现后补测试
✅ 每个 Step：红灯 → 绿灯 → 重构
```

### 4. 技术指标使用

根据系统铁律第 2 条"单指标不得独立决策"：

```python
# ❌ 禁止作为独立交易触发
import talib
rsi_signal = talib.RSI(close, timeperiod=14) > 70
if rsi_signal:
    place_order()  # 错误：单指标独立触发

# ✅ 可用于对照/特征工程，但必须联合情绪因子并通过 Validation Gate
rsi = talib.RSI(close, timeperiod=14)
features['rsi_14'] = rsi
can_trade = (mss_score >= 70) and (final_gate in {"PASS", "WARN"})
if can_trade:
    place_order()
```

## 权威文档参考

- `CLAUDE.md` - 系统铁律与架构约束
- `docs/naming-conventions.md` - 字段命名规范
- `Governance/steering/系统铁律.md` - 零容忍规则

## 遇到问题时

1. **不确定字段命名**：立即查阅 `docs/naming-conventions.md`

2. **Gate 检查失败**：立即停止，修复后重跑

3. **测试无法通过**：先分析根因，必要时调整测试数据

## 成功标准

- [ ] 所有测试用例通过（绿灯）
- [ ] Gate 检查全部通过
- [ ] 代码符合 Black + Flake8 规范
- [ ] 无路径硬编码
- [ ] 字段命名符合规范
