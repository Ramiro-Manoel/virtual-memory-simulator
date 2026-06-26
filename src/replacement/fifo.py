"""First-In First-Out replacement policy."""

from collections import deque
from replacement.base import ReplacementPolicy


class FIFOPolicy(ReplacementPolicy):
    """Evicts the frame that was loaded first (oldest)."""

    def __init__(self):
        self._frames: deque[int] = deque()

    @property
    def name(self) -> str:
        return "FIFO"

    def record_load(self, frame_number: int) -> None:
        self._frames.append(frame_number)

    def record_access(self, frame_number: int) -> None:
        pass  # FIFO ignores accesses

    def choose_victim(self) -> int:
        return self._frames.popleft()
