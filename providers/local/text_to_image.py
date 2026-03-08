from pathlib import Path

from providers.errors import ProviderNotConfiguredError
from providers.interfaces import GeneratedImage, TextToImageProvider


class DiffusersTextToImageProvider(TextToImageProvider):
    def __init__(self) -> None:
        raise ProviderNotConfiguredError(
            "Diffusers text-to-image adapter is not configured. Install diffusers + torch, set your model path, "
            "then set TEXT_TO_IMAGE_PROVIDER=local."
        )

    def generate_image(
        self,
        prompt: str,
        output_dir: Path,
        width: int = 1280,
        height: int = 720,
        seed: int = 0,
    ) -> GeneratedImage:
        raise NotImplementedError
