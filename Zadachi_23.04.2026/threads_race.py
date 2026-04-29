
"""
The Great Thread Race
=====================
A hands-on way to SEE parallelism happen.

Run it:
    python thread_race.py             # parallel (all horses race at once)
    python thread_race.py sequential  # boring mode (one at a time)

In parallel mode, every progress bar advances at the same time.
In sequential mode, each horse finishes fully before the next one starts.
Same total work, very different wall-clock time. That's the whole point.

Needs a terminal that understands ANSI escape codes (any macOS/Linux
terminal, Windows Terminal, VS Code terminal). Classic cmd.exe won't render it.
"""

import threading
import time
import random
import sys

TRACK_LENGTH = 40
HORSES = ["Alpha  ", "Bravo  ", "Charlie", "Delta  ", "Echo   "]

# Prevents threads from garbling each other's terminal output.
print_lock = threading.Lock()


def draw_row(row: int, name: str, pos: int) -> None:
    """Draw one horse on its own terminal row, safely."""
    with print_lock:
        bar = "─" * pos + "🐎" + "·" * (TRACK_LENGTH - pos)
        # ANSI: move cursor to (row, col 1), clear line, write text.
        sys.stdout.write(f"\033[{row};1H\033[2K  {name} {bar} {pos:2d}/{TRACK_LENGTH}")
        sys.stdout.flush()


def run_horse(row: int, name: str, finishers: list, lock: threading.Lock) -> None:
    """A horse trots from 0 to TRACK_LENGTH, sleeping random amounts per step."""
    for pos in range(TRACK_LENGTH + 1):
        time.sleep(random.uniform(0.02, 0.12))  # simulated I/O-bound step
        draw_row(row, name, pos)
    with lock:
        finishers.append(name.strip())


def race_parallel() -> None:
    sys.stdout.write("\033[2J\033[H")  # clear screen, home cursor
    print("PARALLEL: all horses racing at once\n")
    finishers: list[str] = []
    finish_lock = threading.Lock()
    start = time.time()

    threads = [
        threading.Thread(target=run_horse, args=(i + 3, name, finishers, finish_lock))
        for i, name in enumerate(HORSES)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    sys.stdout.write(f"\033[{len(HORSES) + 5};1H\n")
    print(f"Elapsed: {time.time() - start:.2f}s")
    print(f"Finish order: {' → '.join(finishers)}")


def race_sequential() -> None:
    sys.stdout.write("\033[2J\033[H")
    print("SEQUENTIAL: one horse at a time\n")
    finishers: list[str] = []
    start = time.time()
    for i, name in enumerate(HORSES):
        run_horse(i + 3, name, finishers, threading.Lock())
    sys.stdout.write(f"\033[{len(HORSES) + 5};1H\n")
    print(f"Elapsed: {time.time() - start:.2f}s")
    print(f"Finish order: {' → '.join(finishers)}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "parallel"
    (race_sequential if mode == "sequential" else race_parallel)()
