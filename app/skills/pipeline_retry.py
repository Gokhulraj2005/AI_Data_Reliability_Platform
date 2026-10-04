"""Retry a pipeline operation with bounded exponential backoff."""

import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def retry_pipeline(
    operation: Callable[[], T], attempts: int = 3, base_delay: float = 0.25
) -> T:
    if attempts < 1:
        raise ValueError("attempts must be at least 1")
    for attempt in range(attempts):
        try:
            return operation()
        except Exception:
            if attempt == attempts - 1:
                raise
            time.sleep(base_delay * (2 ** attempt))
    raise RuntimeError("unreachable")
