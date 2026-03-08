from __future__ import annotations

import hashlib
from pathlib import Path

from providers.interfaces import GeneratedImage, TextToImageProvider
from providers.mock.utils import write_placeholder_ppm


class MockTextToImageProvider(TextToImageProvider):
    def generate_image(
        self,
        prompt: str,
        output_dir: Path,
        width: int = 1280,
        height: int = 720,
        seed: int = 0,
    ) -> GeneratedImage:
        output_dir.mkdir(parents=True, exist_ok=True)
        key = hashlib.sha1(f"{prompt}:{seed}".encode("utf-8")).hexdigest()[:10]
        path = output_dir / f"image_{key}.ppm"
        write_placeholder_ppm(path, width=width, height=height, seed=seed)
        return GeneratedImage(path=path, prompt=prompt, width=width, height=height)
