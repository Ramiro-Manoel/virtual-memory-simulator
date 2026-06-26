"""Simple data carriers used across the simulator."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class MemoryAccess:
    """A request from a process: read one byte at (page, offset)."""
    thread_id: int
    page_number: int
    offset: int


@dataclass
class AccessResult:
    """What the MMU produced for one access — used for the output log."""
    access: MemoryAccess
    frame_number: int
    page_fault: bool
    removed_page: Optional[int]
    byte_value: int

    def __str__(self) -> str:
        lines = [f"Thread {self.access.thread_id} | Page {self.access.page_number}, Offset {self.access.offset}"]
        if self.page_fault:
            lines.append("  >> PAGE FAULT")
            if self.removed_page is not None:
                lines.append(f"  >> Removed Page {self.removed_page}")
            lines.append(f"  >> Loaded into Frame {self.frame_number}")
        else:
            lines.append(f"  >> Hit: Frame {self.frame_number}")
        lines.append(f"  >> Byte read: {self.byte_value}")
        return "\n".join(lines)
