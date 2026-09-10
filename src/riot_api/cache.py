from __future__ import annotations

from collections.abc import Callable, Hashable
from typing import Any


class MemoryCache:
    """한 번의 수집 실행 동안 동일 API 응답을 재사용하는 단순 메모리 캐시."""

    def __init__(self) -> None:
        self._values: dict[Hashable, Any] = {}

    def get_or_set(self, key: Hashable, loader: Callable[[], Any]) -> Any:
        if key not in self._values:
            self._values[key] = loader()
        return self._values[key]

    def clear(self) -> None:
        self._values.clear()
