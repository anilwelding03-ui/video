from __future__ import annotations

import json
from pathlib import Path

from providers.interfaces import GeneratedVideo, ImageToVideoProvider


class MockImageToVideoProvider(ImageToVideoProvider):
    def animate_image(
        self,
        image_path: Path,
        output_dir: Path,
        duration_seconds: float,
        frame_rate: int = 24,
    ) -> GeneratedVideo:
        output_dir.mkdir(parents=True, exist_ok=True)
        frame_count = max(1, int(round(duration_seconds * frame_rate)))
        clip_path = output_dir / f"clip_from_{image_path.stem}.mockclip.json"
        payload = {
            "source_image": str(image_path),
            "frame_count": frame_count,
            "frame_rate": frame_rate,
            "duration_seconds": duration_seconds,
            "kind": "image_to_video_placeholder",
        }
        clip_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return GeneratedVideo(
            path=clip_path,
            duration_seconds=duration_seconds,
            frame_rate=frame_rate,
            width=1280,
            height=720,
        )
