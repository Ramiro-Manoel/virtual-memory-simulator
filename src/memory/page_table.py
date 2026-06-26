"""Page table — maps virtual pages to physical frames for one process."""

from typing import Optional


class PageTable:
    """A simple page -> frame map. Knows nothing about memory contents."""

    def __init__(self, thread_id: int):
        self.thread_id = thread_id
        self._map: dict[int, int] = {}

    def has(self, page_number: int) -> bool:
        return page_number in self._map

    def get_frame(self, page_number: int) -> int:
        return self._map[page_number]

    def set_frame(self, page_number: int, frame_number: int) -> None:
        self._map[page_number] = frame_number

    def remove(self, page_number: int) -> None:
        self._map.pop(page_number, None)

    def pages(self) -> list[int]:
        return sorted(self._map)
