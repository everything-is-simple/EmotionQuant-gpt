#!/usr/bin/env python3
"""
Naming / contracts consistency checks for design docs.

Goal:
- Detect drift for critical enum names, thresholds, and bridge contracts.
- Provide a lightweight gate that can be used in local checks / CI.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Expectation:
    rule_id: str
    path: str
    pattern: str
    note: str


EXPECTATIONS: tuple[Expectation, ...] = (
    # Trend / naming base
    Expectation(
        "trend_sideways",
        "docs/naming-conventions.md",
        r"sideways",
        "Trend enum must include sideways",
    ),
    Expectation(
        "trend_sideways",
        "docs/naming-conventions.md",
        r"不使用\s*`?flat`?",
        "Naming spec must forbid flat as trend enum",
    ),
    Expectation(
        "trend_sideways",
        "docs/design/core-algorithms/mss/mss-algorithm.md",
        r'trend取值:\s*"up"\s*\|\s*"down"\s*\|\s*"sideways"',
        "MSS trend enum must be up/down/sideways",
    ),
    # unknown fallback
    Expectation(
        "unknown_fallback",
        "docs/naming-conventions.md",
        r"\bunknown\b",
        "Naming spec must define unknown fallback",
    ),
    Expectation(
        "unknown_fallback",
        "docs/design/core-algorithms/mss/mss-api.md",
        r"unknown",
        "MSS API must expose unknown",
    ),
    Expectation(
        "unknown_fallback",
        "docs/design/core-algorithms/mss/mss-api.md",
        r"合法降级",
        "MSS API must describe unknown as legal degradation",
    ),
    # risk_reward_ratio naming and threshold alignment
    Expectation(
        "rr_name",
        "docs/naming-conventions.md",
        r"risk_reward_ratio",
        "Canonical RR field name must exist",
    ),
    Expectation(
        "rr_name",
        "docs/naming-conventions.md",
        r"rr_ratio",
        "Non-canonical rr_ratio must be documented as forbidden alias",
    ),
    Expectation(
        "rr_threshold",
        "docs/design/core-algorithms/pas/pas-algorithm.md",
        r"risk_reward_ratio[^\n]*(?:>=|≥)\s*1\.0",
        "PAS algorithm must use RR >= 1.0",
    ),
    Expectation(
        "rr_threshold",
        "docs/design/core-algorithms/pas/pas-data-models.md",
        r"risk_reward_ratio[^\n]*(?:>=|≥)\s*1\.0",
        "PAS data model must use RR >= 1.0",
    ),
    Expectation(
        "rr_threshold",
        "docs/design/core-infrastructure/trading/trading-algorithm.md",
        r"risk_reward_ratio\s*<\s*1\.0",
        "Trading execution must filter RR < 1.0",
    ),
    Expectation(
        "rr_threshold",
        "docs/design/core-infrastructure/backtest/backtest-algorithm.md",
        r"risk_reward_ratio\s*<\s*1\.0",
        "Backtest execution must filter RR < 1.0",
    ),
    # STRONG_BUY threshold alignment
    Expectation(
        "strong_buy_75",
        "docs/naming-conventions.md",
        r"(?:STRONG_BUY[^\n]*75|75[^\n]*STRONG_BUY)",
        "Naming spec must align STRONG_BUY threshold with 75",
    ),
    Expectation(
        "strong_buy_75",
        "docs/design/core-algorithms/integration/integration-algorithm.md",
        r"(?:STRONG_BUY[^\n]*75|75[^\n]*STRONG_BUY)",
        "Integration must align STRONG_BUY threshold with 75",
    ),
    Expectation(
        "strong_buy_75",
        "docs/design/core-infrastructure/data-layer/data-layer-data-models.md",
        r"(?:STRONG_BUY[^\n]*75|75[^\n]*STRONG_BUY)",
        "Data layer models must align STRONG_BUY threshold with 75",
    ),
    Expectation(
        "strong_buy_75",
        "docs/design/core-infrastructure/gui/gui-algorithm.md",
        r"final_score\s*>=\s*75",
        "GUI display rules must align STRONG_BUY threshold with 75",
    ),
    # stock_code / ts_code boundary
    Expectation(
        "code_boundary",
        "docs/naming-conventions.md",
        r"stock_code",
        "Naming spec must define stock_code",
    ),
    Expectation(
        "code_boundary",
        "docs/naming-conventions.md",
        r"ts_code",
        "Naming spec must define ts_code",
    ),
    Expectation(
        "code_boundary",
        "docs/design/core-infrastructure/data-layer/data-layer-api.md",
        r"L1 数据落库",
        "Data layer API must document L1 code boundary",
    ),
    Expectation(
        "code_boundary",
        "docs/design/core-infrastructure/data-layer/data-layer-api.md",
        r"保持 `ts_code`",
        "L1 boundary must keep ts_code",
    ),
    Expectation(
        "code_boundary",
        "docs/design/core-infrastructure/data-layer/data-layer-api.md",
        r"L2\+ 内部使用",
        "L2+ boundary must be explicitly documented",
    ),
    Expectation(
        "code_boundary",
        "docs/design/core-infrastructure/data-layer/data-layer-api.md",
        r"stock_code",
        "L2+ boundary must use stock_code",
    ),
    # Gate PASS/WARN/FAIL
    Expectation(
        "gate_triplet",
        "docs/design/core-algorithms/validation/factor-weight-validation-data-models.md",
        r"final_gate",
        "Validation models must define final_gate",
    ),
    Expectation(
        "gate_triplet",
        "docs/design/core-algorithms/validation/factor-weight-validation-data-models.md",
        r"PASS/WARN/FAIL",
        "Validation models must preserve PASS/WARN/FAIL triplet",
    ),
    Expectation(
        "gate_triplet",
        "docs/design/core-algorithms/integration/integration-algorithm.md",
        r"final_gate",
        "Integration must consume final_gate",
    ),
    Expectation(
        "gate_triplet",
        "docs/design/core-algorithms/integration/integration-algorithm.md",
        r"PASS/WARN/FAIL",
        "Integration must preserve PASS/WARN/FAIL triplet",
    ),
)


def run_expectations(
    root: Path,
    expectations: tuple[Expectation, ...] = EXPECTATIONS,
) -> list[str]:
    violations: list[str] = []
    cache: dict[str, str] = {}

    for exp in expectations:
        text = cache.get(exp.path)
        if text is None:
            target = root / exp.path
            if not target.exists():
                violations.append(f"[{exp.rule_id}] missing file: {exp.path}")
                continue
            text = target.read_text(encoding="utf-8")
            cache[exp.path] = text

        if re.search(exp.pattern, text, flags=re.MULTILINE) is None:
            violations.append(
                f"[{exp.rule_id}] {exp.path}: missing pattern /{exp.pattern}/ ({exp.note})"
            )

    return violations


def check_naming_contracts(root: Path = PROJECT_ROOT) -> int:
    violations = run_expectations(root)
    if not violations:
        print(f"[contracts] pass ({len(EXPECTATIONS)} checks)")
        return 0

    print(f"[contracts] failed ({len(violations)} violations)")
    for item in violations:
        print(f"  - {item}")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check naming/contracts consistency in core design docs."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=PROJECT_ROOT,
        help="Project root to scan (default: repository root)",
    )
    args = parser.parse_args()
    return check_naming_contracts(args.root.resolve())


if __name__ == "__main__":
    sys.exit(main())
