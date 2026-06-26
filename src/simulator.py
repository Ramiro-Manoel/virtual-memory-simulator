"""Wires everything together and runs the producer/consumer simulation."""

import random
import threading
from queue import Queue

from config import NUM_THREADS, ADDRESS_QUEUE_MAX_SIZE, NUM_VIRTUAL_PAGES
from replacement.base import ReplacementPolicy
from memory.ram import Ram
from memory.disk import Disk
from mmu.mmu import MMU
from threads.producer import Producer
from threads.consumer import Consumer
from display.display import print_results, print_memory_state, print_page_tables


class Simulator:
    """Builds the system with the chosen replacement policy and runs it."""

    def __init__(self, policy: ReplacementPolicy, seed: int = 42):
        self._rng = random.Random(seed)
        self._mmu = MMU(Ram(), policy)
        self._page_counts: dict[int, int] = {}

    def _create_processes(self) -> None:
        for thread_id in range(NUM_THREADS):
            num_pages = self._rng.randint(1, NUM_VIRTUAL_PAGES)
            self._mmu.register_process(thread_id, Disk(num_pages, seed=thread_id))
            self._page_counts[thread_id] = num_pages
            print(f"  Thread {thread_id}: {num_pages} pages")

    def run(self) -> None:
        print(f"\n  Creating {NUM_THREADS} processes...")
        self._create_processes()

        queue: Queue = Queue(maxsize=ADDRESS_QUEUE_MAX_SIZE)
        done_events = [threading.Event() for _ in range(NUM_THREADS)]

        producers = [
            Producer(tid, self._page_counts[tid], queue, done_events[tid],
                     seed=self._rng.randint(0, 2**32))
            for tid in range(NUM_THREADS)
        ]
        consumer = Consumer(self._mmu, queue, done_events)

        print("\n  Running...\n")
        consumer.start()
        for p in producers:
            p.start()
        for p in producers:
            p.join()
        consumer.join()

        print_results(consumer.results)
        print_memory_state(self._mmu)
        print_page_tables(self._mmu)
