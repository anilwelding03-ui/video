from __future__ import annotations

from pathlib import Path


def write_placeholder_ppm(path: Path, width: int, height: int, seed: int) -> None:
    """Write a deterministic RGB PPM image with a simple gradient pattern."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii") as handle:
        handle.write(f"P3\n{width} {height}\n255\n")
        for y in range(height):
            for x in range(width):
                r = (x + seed * 17) % 256
                g = (y * 2 + seed * 29) % 256
                b = (x + y + seed * 7) % 256
                handle.write(f"{r} {g} {b} ")
            handle.write("\n")
