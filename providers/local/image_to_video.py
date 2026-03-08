from pathlib import Path

from providers.errors import ProviderNotConfiguredError
from providers.interfaces import GeneratedVideo, ImageToVideoProvider


class ComfyUIImageToVideoProvider(ImageToVideoProvider):
    def __init__(self) -> None:
        raise ProviderNotConfiguredError(
            "ComfyUI image-to-video adapter is not configured. Run ComfyUI server, configure workflow/API URL, "
            "then set IMAGE_TO_VIDEO_PROVIDER=local."
        )

    def animate_image(
        self,
        image_path: Path,
        output_dir: Path,
        duration_seconds: float,
        frame_rate: int = 24,
    ) -> GeneratedVideo:
        raise NotImplementedError
