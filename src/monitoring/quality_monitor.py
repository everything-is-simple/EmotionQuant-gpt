from __future__ import annotations

from typing import Any


class QualityMonitor:
    """质量监控占位实现。"""

    def check(self) -> dict[str, Any]:
        raise NotImplementedError("QualityMonitor.check is not implemented")
