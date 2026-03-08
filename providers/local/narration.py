from pathlib import Path

from providers.errors import ProviderNotConfiguredError
from providers.interfaces import NarrationProvider, NarrationTrack


class CoquiNarrationProvider(NarrationProvider):
    def __init__(self) -> None:
        raise ProviderNotConfiguredError(
            "Coqui TTS narration adapter is not configured. Install coqui-tts, download a model, configure voice, "
            "then set NARRATION_PROVIDER=local."
        )

    def synthesize(
        self,
        lines: list[str],
        durations_seconds: list[float],
        output_path: Path,
        sample_rate: int = 22050,
    ) -> NarrationTrack:
        raise NotImplementedError
