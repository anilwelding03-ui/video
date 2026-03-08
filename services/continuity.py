"""Persistence helpers for continuity memory and project bibles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def seed_continuity_memory(project_dir: str | Path) -> dict[str, Any]:
    """Ensure continuity files exist and return current memory payload."""
    root = Path(project_dir)
    bibles_dir = root / "bibles"
    bibles_dir.mkdir(parents=True, exist_ok=True)

    character_path = bibles_dir / "character.json"
    location_path = bibles_dir / "location.json"
    continuity_path = root / "continuity.json"

    character_data = _read_or_initialize(
        character_path,
        {
            "version": 1,
            "characters": [],
            "notes": "Character bible entries appended from parsed scenes.",
        },
    )
    location_data = _read_or_initialize(
        location_path,
        {
            "version": 1,
            "locations": [],
            "notes": "Location bible entries appended from parsed scenes.",
        },
    )
    continuity_data = _read_or_initialize(
        continuity_path,
        {
            "version": 1,
            "active_characters": [],
            "active_locations": [],
            "timeline_notes": [],
            "style_memory": {},
        },
    )

    return {
        "character_bible": character_data,
        "location_bible": location_data,
        "continuity": continuity_data,
        "paths": {
            "character": str(character_path),
            "location": str(location_path),
            "continuity": str(continuity_path),
        },
    }


def persist_bibles(
    project_dir: str | Path,
    *,
    characters: list[dict[str, Any]] | None = None,
    locations: list[dict[str, Any]] | None = None,
    continuity_patch: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Merge and write bible/continuity updates in-place."""
    state = seed_continuity_memory(project_dir)

    character_path = Path(state["paths"]["character"])
    location_path = Path(state["paths"]["location"])
    continuity_path = Path(state["paths"]["continuity"])

    if characters:
        merged_characters = _dedupe_named_entries(state["character_bible"]["characters"] + characters)
        state["character_bible"]["characters"] = merged_characters
        _write_json(character_path, state["character_bible"])

    if locations:
        merged_locations = _dedupe_named_entries(state["location_bible"]["locations"] + locations)
        state["location_bible"]["locations"] = merged_locations
        _write_json(location_path, state["location_bible"])

    if continuity_patch:
        state["continuity"].update(continuity_patch)
        _write_json(continuity_path, state["continuity"])

    return state


def _read_or_initialize(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        _write_json(path, default)
        return default

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def _dedupe_named_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    merged: list[dict[str, Any]] = []
    for entry in entries:
        name = str(entry.get("name", "")).strip().lower()
        if not name or name in seen:
            continue
        seen.add(name)
        merged.append(entry)
    return merged
