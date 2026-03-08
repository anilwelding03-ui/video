from __future__ import annotations

import array
import math
import wave
from pathlib import Path

from providers.interfaces import NarrationProvider, NarrationSegment, NarrationTrack


class MockNarrationProvider(NarrationProvider):
    def synthesize(
        self,
        lines: list[str],
        durations_seconds: list[float],
        output_path: Path,
        sample_rate: int = 22050,
    ) -> NarrationTrack:
        if len(lines) != len(durations_seconds):
            raise ValueError("lines and durations_seconds must have same length")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        samples = array.array("h")
        segments: list[NarrationSegment] = []
        cursor = 0.0

        for idx, (line, duration) in enumerate(zip(lines, durations_seconds, strict=True)):
            freq = 220.0 + idx * 40.0
            segment_samples = max(1, int(duration * sample_rate))
            for i in range(segment_samples):
                t = i / sample_rate
                amplitude = 0.22 if line.strip() else 0.0
                value = int(32767.0 * amplitude * math.sin(2.0 * math.pi * freq * t))
                samples.append(value)

            start = cursor
            cursor += duration
            segments.append(NarrationSegment(text=line, start_seconds=start, end_seconds=cursor))

            silence_len = int(0.05 * sample_rate)
            samples.extend([0] * silence_len)
            cursor += silence_len / sample_rate

        with wave.open(str(output_path), "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(samples.tobytes())

        return NarrationTrack(path=output_path, segments=segments, duration_seconds=cursor)
