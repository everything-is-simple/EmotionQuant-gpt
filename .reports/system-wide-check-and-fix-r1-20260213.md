# 系统全量检查与修复报告（R1）

**检查时间**: 2026-02-13  
**检查范围**: `src/` `scripts/` `tests/` `Governance/` `docs/`  
**目标**: 对照历史批判式检查口径，做一轮“发现即修复”的全仓治理

---

## 1. 结论摘要

- 门禁状态：通过
- 本轮修复完成：是
- 当前阻断项：无

---

## 2. 发现与修复

### F1（工程卫生，P1）：仓库跟踪了 `__pycache__/*.pyc`

- 现象：
  - `git ls-files` 中存在以下跟踪文件：
    - `src/data/__pycache__/__init__.cpython-310.pyc`
    - `src/data/models/__pycache__/__init__.cpython-310.pyc`
    - `src/data/models/__pycache__/entities.cpython-310.pyc`
    - `src/data/models/__pycache__/snapshots.cpython-310.pyc`
- 风险：
  - 提交噪声高、跨环境二进制差异引发无效冲突
- 修复：
  - 已从版本库删除上述 `.pyc` 跟踪文件（`git rm`）
  - `.gitignore` 已覆盖 `__pycache__/` 与 `*.py[cod]`（无需新增）

### F2（执行稳定性，P2）：本机未注入全局 `python/ruff` 到 PATH

- 现象：
  - 直接执行 `ruff` / `python` 在当前 shell 不可用
  - `.venv` 与 `uv` 可用
- 修复策略：
  - 本轮门禁统一改为 `uv run --no-sync ...` 执行，确保命令可复现且无依赖同步噪声

### F3（Git 环境，P2）：凭据 helper 配置确认

- 检查：
  - `git config --show-origin --get-all credential.helper`
- 结果：
  - 当前为 `manager`（不存在 `manager-core` 误配置）
  - 本轮无需进一步修复

---

## 3. 验证证据（可复跑）

```powershell
uv run --no-sync ruff check src tests scripts
uv run --no-sync pytest -q
uv run --no-sync python scripts/quality/local_quality_check.py --scan
```

验证结果：

- `ruff`: All checks passed
- `pytest`: 14 passed
- `local_quality_check --scan`: hardcoded path check passed

---

## 4. 后续执行建议（下一圈可直接复用）

1. 统一将质量门禁命令固定为 `uv run --no-sync` 形态，减少环境差异。
2. 合并前保留本报告模板，继续执行“先检查、再修复、再验收”的闭环。
