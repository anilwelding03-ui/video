from pathlib import Path

from providers.errors import ProviderNotConfiguredError
from providers.interfaces import SubtitleProvider


class LocalSubtitleProvider(SubtitleProvider):
    def __init__(self) -> None:
        raise ProviderNotConfiguredError(
            "Local subtitle adapter is not configured. Provide your custom subtitle backend and set "
            "SUBTITLE_PROVIDER=local."
        )

    def build_srt(
        self,
        lines: list[str],
        durations_seconds: list[float],
        output_path: Path,
    ) -> Path:
        raise NotImplementedError
