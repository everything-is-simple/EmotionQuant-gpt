# .claude Integration Notes

**Status**: Runtime configuration for Claude Code
**Last updated**: 2026-02-14

---

## Scope

This file documents the `.claude` tooling configuration.
Canonical policy lives in:

- `CLAUDE.md`
- `Governance/steering/`
- `Governance/Capability/`

---

## Runtime Configuration

- **Hook wiring**: `.claude/settings.json`
- **Hook scripts**: `.claude/hooks/*.py`
- **Spiral state**: `Governance/record/development-status.md`

If any `.claude` markdown conflicts with governance docs, governance docs win.

---

## Active Commands

| Command | File | Purpose |
|---------|------|---------|
| `/6a-status` | `commands/6a-status.md` | Spiral 工作流状态查询 |
| `/a4-check` | `commands/a4-check.md` | A4 Gate 检查 |
| `/a6-check` | `commands/a6-check.md` | A6 完整检查 |
| `/tdd` | `commands/tdd.md` | TDD 提醒 |

---

## Active Hooks

| Hook | Script | Purpose |
|------|--------|---------|
| SessionStart | `hooks/session_start.py` | 会话启动检查 |
| UserPromptSubmit | `hooks/user_prompt_submit.py` | 提示词提交检查 |
| PreToolUse (Edit/Write) | `hooks/pre_edit_check.py` | 编辑前检查 |
| PostToolUse (Edit/Write) | `hooks/post_edit_check.py` | 编辑后检查 |

---

## Principles

- **Spiral-first**: Use `S0-S6` terminology, not "Phase"
- **CP naming**: Use `CP-*` for capability packs
- **Minimal sync**: 5 required files per Spiral (per `CLAUDE.md` §7)
- **No duplication**: Keep `.claude/` lightweight
