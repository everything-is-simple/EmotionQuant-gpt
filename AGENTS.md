# AGENTS.md

This file is the concise entrypoint for automated agents in this repository.
Canonical policy is now **Spiral-first** and aligned with `README.md` + `CLAUDE.md`.

---

## Document positioning

- Purpose: provide minimal, executable repository work rules for automated agents.
- Single execution baseline: `docs/design/enhancements/eq-improvement-plan-core-frozen.md` (`enhancement-selection-analysis_claude-opus-max_20260210.md` serves only as selection rationale input).
- Authoritative architecture entry: `docs/system-overview.md`
- Authoritative roadmap entry: `Governance/Capability/SPIRAL-CP-OVERVIEW.md`
- Authoritative governance entry: `Governance/steering/`

---

## Mandatory reading order

1. `README.md`
2. `CLAUDE.md` (system entry + workflow)
3. `docs/system-overview.md`, `docs/module-index.md`, `docs/naming-conventions.md`
4. `Governance/steering/系统铁律.md` and `Governance/steering/CORE-PRINCIPLES.md`
5. `Governance/steering/6A-WORKFLOW.md`

---

## Execution model

- Model: Spiral (closed-loop), not linear stage pipeline.
- Default cadence: 7 days per spiral.
- Roadmap terminology: Capability Pack (CP), using `CP-*.md` filenames.
- Each spiral closure: `run + test + artifact + review + sync`.
- Do not interpret CP indices as linear stage gates.

---

## Non-negotiables (7 iron rules)

1. **Sentiment-first**: signal logic must center on sentiment factors.
2. **No single-indicator decisions**: technical indicators may serve as contrast/auxiliary features, but must not independently trigger trades.
3. **Local-data first**: main pipeline reads local data; remote is for supplementation only.
4. **No hardcoded paths/secrets**: must use `Config.from_env()` or env vars.
5. **A-share rules enforced**: T+1, price limits, trading sessions.
6. **Spiral closure mandatory**: each spiral must close with run/test/artifact/review/sync; no closure without all five.
7. **Docs serve implementation**: no doc bloat blocking development; minimal sync first.

Authoritative detail: `Governance/steering/系统铁律.md`

---

## Workflow (graded governance)

- Default: `Scope -> Build -> Verify -> Sync`
- Escalate to strict 6A only for: trading path changes, risk control changes, data contract breaking changes, critical new external dependencies.
- Each spiral minimal sync (5 items):
  1. `Governance/specs/spiral-s{N}/final.md`
  2. `Governance/record/development-status.md`
  3. `Governance/record/debts.md`
  4. `Governance/record/reusable-assets.md`
  5. `Governance/Capability/SPIRAL-CP-OVERVIEW.md`
- CP docs updated only on contract changes.

Authoritative workflow: `Governance/steering/6A-WORKFLOW.md`

---

## Tech stack

- Python `>=3.10`
- Data: Parquet + DuckDB (single-DB preferred)
- GUI: Streamlit + Plotly
- Backtest primary: Qlib (research & experiments); execution baseline: local vectorized backtester; compatibility adapter: backtrader (optional, not mainline)

Details: `pyproject.toml`, `docs/design/core-infrastructure/backtest/backtest-engine-selection.md`

---

## Quick references

- Single execution baseline: `docs/design/enhancements/eq-improvement-plan-core-frozen.md`
- Project status: `Governance/record/development-status.md`
- Debts: `Governance/record/debts.md`
- Reusable assets: `Governance/record/reusable-assets.md`
- Tests & tooling: `pyproject.toml`, `requirements.txt`

---

## Repository remote

- `origin`: `https://github.com/everything-is-simple/EmotionQuant_beta.git`

---

## Local directory anchors (this deployment)

- Local repo root (docs + code): `G:\EmotionQuant-gpt`
- Local database/data root: `G:\EmotionQuant_data`
- Keep code path handling via Config/env (no hardcoded paths in implementation).

---

## Tooling note (.claude)

- `.claude/` is retained as historical tooling assets.
- Reusable governance rules have been migrated to `Governance/steering/` and `Governance/Capability/`.
- Do not treat `.claude` commands as canonical workflow requirements.
