"""Producer thread — generates random memory accesses for one process."""

import random
import threading
import time
from queue import Queue
from models.models import MemoryAccess
from config import INSTRUCTIONS_PER_THREAD, PAGE_SIZE


class Producer(threading.Thread):
    """Simulates a CPU generating random page accesses and queueing them."""

    def __init__(self, thread_id: int, num_pages: int, queue: Queue,
                 done_event: threading.Event, seed: int):
        super().__init__(name=f"Producer-{thread_id}", daemon=True)
        self._thread_id = thread_id
        self._num_pages = num_pages
        self._queue = queue
        self._done_event = done_event
        self._rng = random.Random(seed)

    def run(self) -> None:
        for _ in range(INSTRUCTIONS_PER_THREAD):
            page = self._rng.randint(0, self._num_pages - 1)
            offset = self._rng.randint(0, PAGE_SIZE - 1)
            self._queue.put(MemoryAccess(self._thread_id, page, offset))
            # Small random pause so the threads interleave instead of running
            # one fully before the other (simulates real CPU timing).
            time.sleep(self._rng.uniform(0.001, 0.01))
        self._done_event.set()
