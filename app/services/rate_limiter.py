import time
from collections import defaultdict, deque
from threading import Lock


class SlidingWindowRateLimiter:
    """Counts the failures of each key (here: an IP) over a time window."""

    def __init__(self, max_attempts: int, window_seconds: int):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._failures = defaultdict(deque)
        self._lock = Lock()

    def record_failure(self, key: str) -> int:
        """Records one failure and returns the number of recent failures."""
        now = time.time()
        with self._lock:
            attempts = self._failures[key]
            attempts.append(now)
            while attempts and now - attempts[0] > self.window_seconds:
                attempts.popleft()
            return len(attempts)

    def is_exceeded(self, count: int) -> bool:
        return count > self.max_attempts