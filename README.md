# Virtual Memory Simulator

Practical assignment for Operating Systems Analysis and Application.

Simulates virtual memory management with paging: address translation by the MMU, page
fault handling and page replacement. Uses threads (lightweight processes) in the
producer/consumer pattern.

## Video

[![Watch the video](https://img.youtube.com/vi/KejD4vCSbXg/maxresdefault.jpg)](https://www.youtube.com/watch?v=KejD4vCSbXg)

## Specification

- Main memory (RAM): 64 KB
- Virtual memory: 1 MB
- Page/frame: 8 KB
- Physical frames: 8
- Virtual pages: 128
- Threads: 2
- Replacement algorithm: LRU (default) or FIFO

## How to run

Requires only Python 3.10+ (no external libraries).

```bash
cd src
python main.py                  # LRU (default)
python main.py --algorithm fifo # FIFO
```

## How it works

Each process generates memory accesses (page + offset). The MMU translates this virtual
address into a physical address (frame + offset):

- If the page is already in RAM, it reads the byte directly (hit).
- If not, a page fault occurs: the page is loaded from disk into RAM. If there is no free
  frame, the replacement algorithm (LRU or FIFO) chooses a page to remove and free space.

The producer threads generate the accesses and put them in a queue. The consumer thread
takes them from the queue and calls the MMU. The MMU uses a lock to handle one access at
a time safely.

## Structure

```
src/
├── main.py            # entry point and algorithm selection
├── config.py          # system constants
├── simulator.py       # builds and runs the simulation
├── models/            # data structures (access and result)
├── memory/            # disk.py, ram.py, page_table.py
├── replacement/       # base.py, lru.py, fifo.py
├── mmu/               # mmu.py (translation and page fault logic)
└── threads/           # producer.py and consumer.py
```

The memories (disk and ram) only store bytes. All the logic lives in the MMU. The
replacement algorithm can be swapped without changing the rest of the code.

## Sample output

```
[#001] Thread 0 | Page 8, Offset 2306
  >> PAGE FAULT
  >> Loaded into Frame 0
  >> Byte read: 205

[#009] Thread 0 | Page 22, Offset 1568
  >> PAGE FAULT
  >> Removed Page 8
  >> Loaded into Frame 0
  >> Byte read: 42

------------------------------------------------------------
  STATISTICS
------------------------------------------------------------
  Total accesses : 40
  Page hits      : 16
  Page faults    : 24
```
