from typing import Any


class TuShareFetcher:
    """TuShare 数据采集器（占位实现）。"""

    def fetch_with_retry(self, api_name: str, params: dict[str, Any]) -> Any:
        raise NotImplementedError("TuShareFetcher is not implemented")
