"""MMU — the brain. Resolves accesses, handles page faults and page removal.

The memories are dumb byte stores; all the logic lives here.
"""

import threading
from typing import Optional
from models.models import MemoryAccess, AccessResult
from memory.ram import Ram
from memory.disk import Disk
from memory.page_table import PageTable
from replacement.base import ReplacementPolicy
from config import NUM_FRAMES


class MMU:
    def __init__(self, ram: Ram, policy: ReplacementPolicy):
        self._ram = ram
        self._policy = policy
        self._page_tables: dict[int, PageTable] = {}
        self._disks: dict[int, Disk] = {}
        self._free_frames: list[int] = list(range(NUM_FRAMES))
        self._lock = threading.Lock()

    def register_process(self, thread_id: int, disk: Disk) -> None:
        self._disks[thread_id] = disk
        self._page_tables[thread_id] = PageTable(thread_id)

    def access_memory(self, access: MemoryAccess) -> AccessResult:
        with self._lock:
            page_table = self._page_tables[access.thread_id]

            if page_table.has(access.page_number):
                frame = page_table.get_frame(access.page_number)
                self._policy.record_access(frame)
                return self._build_result(access, frame, page_fault=False, removed_page=None)

            return self._handle_page_fault(access, page_table)

    def _handle_page_fault(self, access: MemoryAccess, page_table: PageTable) -> AccessResult:
        frame_number, removed_page = self._claim_frame()

        data = self._disks[access.thread_id].read_page(access.page_number)
        self._ram.load(frame_number, access.thread_id, access.page_number, data)

        page_table.set_frame(access.page_number, frame_number)
        self._policy.record_load(frame_number)

        return self._build_result(access, frame_number, page_fault=True, removed_page=removed_page)

    def _claim_frame(self) -> tuple[int, Optional[int]]:
        """Return a usable frame and the page number removed to free it (or None)."""
        if self._free_frames:
            return self._free_frames.pop(0), None

        victim_frame = self._policy.choose_victim()
        frame = self._ram.get_frame(victim_frame)
        removed_page = frame.page_number
        self._page_tables[frame.thread_id].remove(frame.page_number)
        self._ram.clear(victim_frame)
        return victim_frame, removed_page

    def _build_result(self, access, frame_number, page_fault, removed_page) -> AccessResult:
        byte_value = self._ram.get_frame(frame_number).data[access.offset]
        return AccessResult(
            access=access,
            frame_number=frame_number,
            page_fault=page_fault,
            removed_page=removed_page,
            byte_value=byte_value,
        )

    def memory_snapshot(self) -> list[str]:
        return [f"Frame {i} {frame}" for i, frame in enumerate(self._ram.frames)]

    def page_tables(self) -> list[PageTable]:
        return list(self._page_tables.values())
