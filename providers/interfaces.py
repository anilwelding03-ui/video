from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ShotPlan:
    """A single shot blueprint for an upcoming generated clip."""

    shot_id: str
    prompt: str
    duration_seconds: float
    narration_line: str


@dataclass(frozen=True)
class ScenePlan:
    """A sequence of shots grouped as one coherent scene."""

    scene_id: str
    title: str
    shots: list[ShotPlan]


@dataclass(frozen=True)
class StoryboardPlan:
    """A full plan with all scenes needed to render a final video."""

    scenes: list[ScenePlan]


@dataclass(frozen=True)
class GeneratedImage:
    """An image artifact produced by a provider."""

    path: Path
    prompt: str
    width: int
    height: int


@dataclass(frozen=True)
class GeneratedVideo:
    """A video/clip artifact produced by a provider."""

    path: Path
    duration_seconds: float
    frame_rate: int
    width: int
    height: int


@dataclass(frozen=True)
class NarrationSegment:
    """One timed narration phrase."""

    text: str
    start_seconds: float
    end_seconds: float


@dataclass(frozen=True)
class NarrationTrack:
    """Narration audio and timing metadata."""

    path: Path
    segments: list[NarrationSegment]
    duration_seconds: float


@dataclass(frozen=True)
class SubtitleCue:
    """One subtitle cue row for SRT."""

    index: int
    start_seconds: float
    end_seconds: float
    text: str


class ScenePlannerProvider(ABC):
    @abstractmethod
    def plan_scenes(self, script: str, target_scene_count: int | None = None) -> StoryboardPlan:
        """Generate scene and shot structure from a script."""


class TextToImageProvider(ABC):
    @abstractmethod
    def generate_image(
        self,
        prompt: str,
        output_dir: Path,
        width: int = 1280,
        height: int = 720,
        seed: int = 0,
    ) -> GeneratedImage:
        """Create an image based on text prompt."""


class ImageToVideoProvider(ABC):
    @abstractmethod
    def animate_image(
        self,
        image_path: Path,
        output_dir: Path,
        duration_seconds: float,
        frame_rate: int = 24,
    ) -> GeneratedVideo:
        """Create a clip from a source image."""


class TextToVideoProvider(ABC):
    @abstractmethod
    def generate_video(
        self,
        prompt: str,
        output_dir: Path,
        duration_seconds: float,
        frame_rate: int = 24,
        seed: int = 0,
    ) -> GeneratedVideo:
        """Create a clip directly from text prompt."""


class NarrationProvider(ABC):
    @abstractmethod
    def synthesize(
        self,
        lines: list[str],
        durations_seconds: list[float],
        output_path: Path,
        sample_rate: int = 22050,
    ) -> NarrationTrack:
        """Generate narration and segment timing metadata."""


class SubtitleProvider(ABC):
    @abstractmethod
    def build_srt(
        self,
        lines: list[str],
        durations_seconds: list[float],
        output_path: Path,
    ) -> Path:
        """Build subtitle file aligned to line durations."""
