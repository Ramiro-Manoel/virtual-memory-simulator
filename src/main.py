"""Entry point for the Virtual Memory Simulator."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import NUM_THREADS, NUM_FRAMES, NUM_VIRTUAL_PAGES
from replacement.lru import LRUPolicy
from replacement.fifo import FIFOPolicy
from simulator import Simulator

ALGORITHMS = {"lru": LRUPolicy, "fifo": FIFOPolicy}


def choose_policy():
    name = "lru"
    if "--algorithm" in sys.argv:
        idx = sys.argv.index("--algorithm")
        if idx + 1 < len(sys.argv):
            name = sys.argv[idx + 1].lower()
    if name not in ALGORITHMS:
        print(f"Unknown algorithm '{name}'. Choose from: {', '.join(ALGORITHMS)}")
        sys.exit(1)
    return ALGORITHMS[name]()


def main() -> None:
    policy = choose_policy()
    print("=" * 60)
    print("  VIRTUAL MEMORY SIMULATOR")
    print(f"  Frames: {NUM_FRAMES} | Virtual pages: {NUM_VIRTUAL_PAGES} | "
          f"Threads: {NUM_THREADS} | Algorithm: {policy.name}")
    print("=" * 60)

    Simulator(policy).run()

    print("\n" + "=" * 60)
    print("  Done.")
    print("=" * 60)


if __name__ == "__main__":
    main()
