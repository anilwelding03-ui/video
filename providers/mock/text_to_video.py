from __future__ import annotations

import hashlib
import json
from pathlib import Path

from providers.interfaces import GeneratedVideo, TextToVideoProvider


class MockTextToVideoProvider(TextToVideoProvider):
    def generate_video(
        self,
        prompt: str,
        output_dir: Path,
        duration_seconds: float,
        frame_rate: int = 24,
        seed: int = 0,
    ) -> GeneratedVideo:
        output_dir.mkdir(parents=True, exist_ok=True)
        key = hashlib.sha1(f"{prompt}:{seed}".encode("utf-8")).hexdigest()[:10]
        clip_path = output_dir / f"text_clip_{key}.mockclip.json"
        payload = {
            "prompt": prompt,
            "seed": seed,
            "duration_seconds": duration_seconds,
            "frame_rate": frame_rate,
            "kind": "text_to_video_placeholder",
        }
        clip_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return GeneratedVideo(
            path=clip_path,
            duration_seconds=duration_seconds,
            frame_rate=frame_rate,
            width=1280,
            height=720,
        )
