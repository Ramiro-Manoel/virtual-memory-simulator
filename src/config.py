"""System-wide constants for the virtual memory simulator."""

# Memory sizes in bytes
MAIN_MEMORY_SIZE = 64 * 1024       # 64 KB
VIRTUAL_MEMORY_SIZE = 1 * 1024 * 1024  # 1 MB
PAGE_SIZE = 8 * 1024               # 8 KB

# Derived counts
NUM_FRAMES = MAIN_MEMORY_SIZE // PAGE_SIZE        # 8 frames
NUM_VIRTUAL_PAGES = VIRTUAL_MEMORY_SIZE // PAGE_SIZE  # 128 pages

# Simulation parameters
NUM_THREADS = 2
INSTRUCTIONS_PER_THREAD = 20
ADDRESS_QUEUE_MAX_SIZE = 10
