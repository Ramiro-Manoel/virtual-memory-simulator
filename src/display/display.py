"""Prints the simulation log, memory state, page tables and statistics."""

from models.models import AccessResult
from mmu.mmu import MMU


def _section(title: str) -> None:
    print(f"\n{'-' * 60}\n  {title}\n{'-' * 60}")


def print_results(results: list[AccessResult]) -> None:
    print("=" * 60)
    print("  MEMORY ACCESS LOG")
    print("=" * 60)
    for i, result in enumerate(results, 1):
        print(f"\n[#{i:03d}] {result}")

    _section("STATISTICS")
    total = len(results)
    faults = sum(1 for r in results if r.page_fault)
    print(f"  Total accesses : {total}")
    print(f"  Page hits      : {total - faults}")
    print(f"  Page faults    : {faults}")


def print_memory_state(mmu: MMU) -> None:
    _section("PHYSICAL MEMORY (frames)")
    for line in mmu.memory_snapshot():
        print(f"  {line}")


def print_page_tables(mmu: MMU) -> None:
    _section("PAGE TABLES")
    for table in mmu.page_tables():
        pages = table.pages()
        if pages:
            mapping = ", ".join(f"P{p}->F{table.get_frame(p)}" for p in pages)
            print(f"  Thread {table.thread_id}: {mapping}")
        else:
            print(f"  Thread {table.thread_id}: (empty)")
