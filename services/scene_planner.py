"""Scene planning heuristics for splitting scenes into timed shot groups."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Any

PACE_KEYWORDS = {
    "fast": {"run", "chase", "fight", "panic", "urgent", "explode", "escape"},
    "slow": {"quiet", "linger", "observe", "stare", "memory", "silence", "breathe"},
}


@dataclass(slots=True)
class PlannedSubScene:
    index: int
    text: str
    word_count: int
    token_estimate: int
    pace: str
    duration_seconds: float
    shot_count: int
    notes: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ScenePlan:
    scene_index: int
    total_duration_seconds: float
    total_shots: int
    sub_scenes: list[PlannedSubScene]


def plan_scene(
    scene_text: str,
    scene_index: int,
    token_threshold: int = 120,
    word_threshold: int = 90,
) -> ScenePlan:
    """Split a scene into sub-scenes using token/word and pacing heuristics."""
    units = _segment_units(scene_text)

    sub_scenes: list[PlannedSubScene] = []
    bucket: list[str] = []
    words_in_bucket = 0

    for unit in units:
        unit_words = len(unit.split())
        predicted_tokens = int(unit_words * 1.35)
        if bucket and (words_in_bucket + unit_words > word_threshold or predicted_tokens > token_threshold):
            sub_scenes.append(_build_subscene(sub_scenes, bucket))
            bucket = []
            words_in_bucket = 0

        bucket.append(unit)
        words_in_bucket += unit_words

    if bucket:
        sub_scenes.append(_build_subscene(sub_scenes, bucket))

    total_duration = round(sum(sub.duration_seconds for sub in sub_scenes), 2)
    total_shots = sum(sub.shot_count for sub in sub_scenes)

    return ScenePlan(
        scene_index=scene_index,
        total_duration_seconds=total_duration,
        total_shots=total_shots,
        sub_scenes=sub_scenes,
    )


def _segment_units(text: str) -> list[str]:
    normalized = re.sub(r"\n{2,}", "\n", text.strip())
    if not normalized:
        return [""]

    sentence_units = [piece.strip() for piece in re.split(r"(?<=[.!?])\s+", normalized) if piece.strip()]
    if len(sentence_units) == 1:
        return [line.strip() for line in normalized.split("\n") if line.strip()] or [normalized]
    return sentence_units


def _build_subscene(existing: list[PlannedSubScene], bucket: list[str]) -> PlannedSubScene:
    text = " ".join(bucket).strip()
    word_count = len(text.split())
    token_estimate = int(word_count * 1.35)
    pace = _infer_pace(text)

    seconds_per_word = 0.33
    pace_mult = 0.8 if pace == "fast" else 1.2 if pace == "slow" else 1.0
    duration = max(2.5, word_count * seconds_per_word * pace_mult)

    base_shots = max(1, math.ceil(word_count / 28))
    if pace == "fast":
        base_shots += 1
    elif pace == "slow" and base_shots > 1:
        base_shots -= 1

    return PlannedSubScene(
        index=len(existing) + 1,
        text=text,
        word_count=word_count,
        token_estimate=token_estimate,
        pace=pace,
        duration_seconds=round(duration, 2),
        shot_count=base_shots,
        notes={
            "pacing_multiplier": pace_mult,
            "estimated_words_per_shot": round(word_count / base_shots, 1),
        },
    )


def _infer_pace(text: str) -> str:
    tokens = {token.lower() for token in re.findall(r"\b[a-z']+\b", text)}

    fast_score = len(tokens.intersection(PACE_KEYWORDS["fast"]))
    slow_score = len(tokens.intersection(PACE_KEYWORDS["slow"]))

    if "!" in text:
        fast_score += 1
    if "..." in text:
        slow_score += 1

    if fast_score > slow_score:
        return "fast"
    if slow_score > fast_score:
        return "slow"
    return "balanced"
