from __future__ import annotations

from pathlib import Path

from providers.interfaces import SubtitleProvider


def _to_srt_timestamp(total_seconds: float) -> str:
    millis = int(round(total_seconds * 1000))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    seconds, millis = divmod(millis, 1_000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"


class MockSubtitleProvider(SubtitleProvider):
    def build_srt(
        self,
        lines: list[str],
        durations_seconds: list[float],
        output_path: Path,
    ) -> Path:
        if len(lines) != len(durations_seconds):
            raise ValueError("lines and durations_seconds must have same length")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        cursor = 0.0
        rows: list[str] = []

        for idx, (line, duration) in enumerate(zip(lines, durations_seconds), start=1):
            start = cursor
            end = start + duration
            rows.append(str(idx))
            rows.append(f"{_to_srt_timestamp(start)} --> {_to_srt_timestamp(end)}")
            rows.append(line or "...")
            rows.append("")
            cursor = end

        output_path.write_text("\n".join(rows), encoding="utf-8")
        return output_path
