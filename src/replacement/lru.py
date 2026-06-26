"""Least-Recently-Used replacement policy."""

from collections import OrderedDict
from replacement.base import ReplacementPolicy


class LRUPolicy(ReplacementPolicy):
    """Evicts the frame whose page was accessed longest ago."""

    def __init__(self):
        self._frames: OrderedDict[int, None] = OrderedDict()

    @property
    def name(self) -> str:
        return "LRU"

    def record_load(self, frame_number: int) -> None:
        self._frames[frame_number] = None
        self._frames.move_to_end(frame_number)

    def record_access(self, frame_number: int) -> None:
        self._frames.move_to_end(frame_number)

    def choose_victim(self) -> int:
        frame_number, _ = self._frames.popitem(last=False)
        return frame_number
