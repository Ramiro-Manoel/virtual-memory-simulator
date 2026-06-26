"""Consumer thread — takes accesses from the queue and asks the MMU to resolve them."""

import threading
from queue import Queue, Empty
from mmu.mmu import MMU
from models.models import AccessResult


class Consumer(threading.Thread):
    """Pulls accesses from the queue, runs them through the MMU, stores results."""

    def __init__(self, mmu: MMU, queue: Queue, producers_done: list[threading.Event]):
        super().__init__(name="Consumer", daemon=True)
        self._mmu = mmu
        self._queue = queue
        self._producers_done = producers_done
        self.results: list[AccessResult] = []

    def run(self) -> None:
        while True:
            try:
                access = self._queue.get(timeout=0.1)
                self.results.append(self._mmu.access_memory(access))
            except Empty:
                if all(e.is_set() for e in self._producers_done) and self._queue.empty():
                    break
