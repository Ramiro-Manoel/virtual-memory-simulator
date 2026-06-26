"""Disk — one process's pages as they live on disk (its backing store).

A dumb store: a list of pages, indexed by page number. Each process has its own.
"""

import random
from config import PAGE_SIZE


class Disk:
    """Holds the on-disk pages of one process. It only stores and returns bytes."""

    def __init__(self, num_pages: int, seed: int = 0):
        rng = random.Random(seed)
        self._pages: list[bytearray] = [
            bytearray(rng.randbytes(PAGE_SIZE)) for _ in range(num_pages)
        ]

    def read_page(self, page_number: int) -> bytearray:
        return self._pages[page_number]

    def write_page(self, page_number: int, data: bytearray) -> None:
        self._pages[page_number] = data

    @property
    def num_pages(self) -> int:
        return len(self._pages)
