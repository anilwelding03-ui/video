from pathlib import Path

from providers.errors import ProviderNotConfiguredError
from providers.interfaces import GeneratedVideo, TextToVideoProvider


class ComfyUITextToVideoProvider(TextToVideoProvider):
    def __init__(self) -> None:
        raise ProviderNotConfiguredError(
            "ComfyUI text-to-video adapter is not configured. Run ComfyUI server with text-to-video workflow, "
            "set API URL, then set TEXT_TO_VIDEO_PROVIDER=local."
        )

    def generate_video(
        self,
        prompt: str,
        output_dir: Path,
        duration_seconds: float,
        frame_rate: int = 24,
        seed: int = 0,
    ) -> GeneratedVideo:
        raise NotImplementedError
