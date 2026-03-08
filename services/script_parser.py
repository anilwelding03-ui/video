"""Utilities for parsing source scripts into structured scene data."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

SCENE_HEADING_RE = re.compile(
    r"^\s*(?P<prefix>INT\.?|EXT\.?|INT/EXT\.?|EST\.?)(?:\s*[-.])?\s*(?P<rest>.+)$",
    re.IGNORECASE,
)
OUTLINE_MARKER_RE = re.compile(
    r"^\s*(?:SCENE\s*\d+|S\d+|\d+[\).]|[-*+]\s*SCENE\s*\d+|BEAT\s*\d+)\s*[:.-]?\s*(?P<title>.+)?$",
    re.IGNORECASE,
)
DIALOGUE_NAME_RE = re.compile(r"^\s*(?P<name>[A-Z][A-Z0-9\s\-']{1,40})\s*$")
PARENTHETICAL_RE = re.compile(r"^\s*\((?P<text>[^)]+)\)\s*$")
CHARACTER_RE = re.compile(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b")
LOCATION_RE = re.compile(
    r"\b(?:in|at|inside|outside|near|toward|towards|into|from)\s+([A-Z][\w\-]*(?:\s+[A-Z][\w\-]*){0,3})\b"
)
EMOTION_TERMS = {
    "angry",
    "anxious",
    "afraid",
    "calm",
    "confident",
    "confused",
    "curious",
    "desperate",
    "excited",
    "frustrated",
    "furious",
    "happy",
    "hopeful",
    "nervous",
    "sad",
    "scared",
    "shocked",
    "tense",
    "tired",
    "worried",
}
ACTION_RE = re.compile(
    r"\b(run(?:s|ning)?|walk(?:s|ing)?|look(?:s|ing)?|grab(?:s|bing)?|open(?:s|ing)?|close(?:s|ing)?|turn(?:s|ing)?|enter(?:s|ing)?|exit(?:s|ing)?|fight(?:s|ing)?|cry(?:s|ing)?|smile(?:s|ing)?|laugh(?:s|ing)?|whisper(?:s|ing)?|shout(?:s|ing)?)\b",
    re.IGNORECASE,
)


@dataclass(slots=True)
class ParsedScene:
    """Single parsed scene with heuristically extracted metadata."""

    index: int
    kind: str
    heading: str
    text: str
    dialogue_ratio: float
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ParseResult:
    """Top-level parser output."""

    parser_mode: str
    scenes: list[ParsedScene]


def parse_script(text: str) -> ParseResult:
    """Parse arbitrary script text into scenes using lightweight heuristics.

    Supported modes:
    * screenplay headings (INT/EXT)
    * scene-by-scene outlines
    * dialogue-heavy scripts
    * raw paragraphs
    """
    normalized = (text or "").replace("\r\n", "\n").strip()
    if not normalized:
        return ParseResult(parser_mode="empty", scenes=[])

    lines = [line.rstrip() for line in normalized.split("\n")]
    mode = _detect_mode(lines)

    if mode == "screenplay":
        chunks = _split_by_screenplay_headings(lines)
    elif mode == "outline":
        chunks = _split_by_outline_markers(lines)
    elif mode == "dialogue":
        chunks = _split_dialogue_blocks(lines)
    else:
        chunks = _split_raw_paragraphs(normalized)

    scenes: list[ParsedScene] = []
    for idx, chunk in enumerate(chunks, start=1):
        heading = chunk["heading"]
        scene_text = chunk["text"].strip()
        dialogue_ratio = _dialogue_ratio(scene_text)
        metadata = _extract_entities(scene_text, heading)
        scenes.append(
            ParsedScene(
                index=idx,
                kind=mode,
                heading=heading,
                text=scene_text,
                dialogue_ratio=dialogue_ratio,
                metadata=metadata,
            )
        )

    return ParseResult(parser_mode=mode, scenes=scenes)


def _detect_mode(lines: list[str]) -> str:
    non_empty = [line for line in lines if line.strip()]
    if not non_empty:
        return "raw"

    heading_hits = sum(1 for line in non_empty if SCENE_HEADING_RE.match(line))
    outline_hits = sum(1 for line in non_empty if OUTLINE_MARKER_RE.match(line))
    dialogue_hits = sum(1 for line in non_empty if DIALOGUE_NAME_RE.match(line))

    if heading_hits >= 2:
        return "screenplay"
    if outline_hits >= 2:
        return "outline"
    if dialogue_hits / len(non_empty) >= 0.25:
        return "dialogue"
    return "raw"


def _split_by_screenplay_headings(lines: list[str]) -> list[dict[str, str]]:
    scenes: list[dict[str, str]] = []
    heading = "SCENE 1"
    bucket: list[str] = []

    for line in lines:
        if SCENE_HEADING_RE.match(line):
            if bucket:
                scenes.append({"heading": heading, "text": "\n".join(bucket).strip()})
                bucket = []
            heading = line.strip()
        else:
            bucket.append(line)

    if bucket or not scenes:
        scenes.append({"heading": heading, "text": "\n".join(bucket).strip()})

    return scenes


def _split_by_outline_markers(lines: list[str]) -> list[dict[str, str]]:
    scenes: list[dict[str, str]] = []
    heading = "Outline Scene 1"
    bucket: list[str] = []

    for line in lines:
        marker = OUTLINE_MARKER_RE.match(line)
        if marker:
            if bucket:
                scenes.append({"heading": heading, "text": "\n".join(bucket).strip()})
                bucket = []
            heading = marker.group("title") or line.strip()
            continue
        bucket.append(line)

    if bucket or not scenes:
        scenes.append({"heading": heading, "text": "\n".join(bucket).strip()})

    return scenes


def _split_dialogue_blocks(lines: list[str]) -> list[dict[str, str]]:
    blocks: list[dict[str, str]] = []
    bucket: list[str] = []
    speaker = "Dialogue Scene 1"

    for line in lines:
        if DIALOGUE_NAME_RE.match(line):
            if bucket:
                blocks.append({"heading": speaker, "text": "\n".join(bucket).strip()})
                bucket = []
            speaker = line.strip().title()
            continue
        bucket.append(line)

    if bucket:
        blocks.append({"heading": speaker, "text": "\n".join(bucket).strip()})
    if not blocks:
        blocks.append({"heading": speaker, "text": "\n".join(lines).strip()})

    return blocks


def _split_raw_paragraphs(text: str) -> list[dict[str, str]]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paragraphs:
        return [{"heading": "Paragraph 1", "text": text}]
    return [
        {"heading": f"Paragraph {idx}", "text": paragraph}
        for idx, paragraph in enumerate(paragraphs, start=1)
    ]


def _dialogue_ratio(text: str) -> float:
    lines = [line for line in text.split("\n") if line.strip()]
    if not lines:
        return 0.0
    dialogue_like = sum(1 for line in lines if DIALOGUE_NAME_RE.match(line) or PARENTHETICAL_RE.match(line))
    return round(dialogue_like / len(lines), 3)


def _extract_entities(scene_text: str, heading: str) -> dict[str, Any]:
    lower_tokens = re.findall(r"\b[a-z']+\b", scene_text.lower())

    characters = sorted({name for name in CHARACTER_RE.findall(scene_text) if len(name) > 2})
    locations = sorted({loc for loc in LOCATION_RE.findall(scene_text)})

    heading_loc = SCENE_HEADING_RE.match(heading)
    if heading_loc:
        rest = heading_loc.group("rest")
        locations.append(rest.split("-")[0].strip())

    emotions = sorted({token for token in lower_tokens if token in EMOTION_TERMS})
    actions = sorted({match.group(0).lower() for match in ACTION_RE.finditer(scene_text)})

    return {
        "characters": characters[:12],
        "locations": sorted(set(locations))[:8],
        "emotions": emotions[:8],
        "actions": actions[:12],
    }
