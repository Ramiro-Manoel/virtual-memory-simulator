"""RAM — the physical main memory, a list of frames indexed by frame number."""

from dataclasses import dataclass, field
from typing import Optional
from config import PAGE_SIZE, NUM_FRAMES


@dataclass
class Frame:
    """One slot of RAM: the data plus which process page is loaded in it."""
    data: bytearray = field(default_factory=lambda: bytearray(PAGE_SIZE))
    thread_id: Optional[int] = None
    page_number: Optional[int] = None

    @property
    def is_free(self) -> bool:
        return self.thread_id is None

    def __str__(self) -> str:
        if self.is_free:
            return "[FREE]"
        return f"[Thread {self.thread_id}, Page {self.page_number}]"


class Ram:
    """The physical memory: NUM_FRAMES frames accessed by their index."""

    def __init__(self):
        self._frames: list[Frame] = [Frame() for _ in range(NUM_FRAMES)]

    def get_frame(self, frame_number: int) -> Frame:
        return self._frames[frame_number]

    def load(self, frame_number: int, thread_id: int, page_number: int, data: bytearray) -> None:
        frame = self._frames[frame_number]
        frame.data = data
        frame.thread_id = thread_id
        frame.page_number = page_number

    def clear(self, frame_number: int) -> None:
        self._frames[frame_number] = Frame()

    @property
    def frames(self) -> list[Frame]:
        return self._frames
