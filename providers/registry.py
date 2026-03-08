from __future__ import annotations

import logging
import os
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from providers.errors import ProviderNotConfiguredError
from providers.interfaces import (
    ImageToVideoProvider,
    NarrationProvider,
    ScenePlannerProvider,
    SubtitleProvider,
    TextToImageProvider,
    TextToVideoProvider,
)
from providers.local.image_to_video import ComfyUIImageToVideoProvider
from providers.local.narration import CoquiNarrationProvider
from providers.local.scene_planner import LocalScenePlannerProvider
from providers.local.subtitle import LocalSubtitleProvider
from providers.local.text_to_image import DiffusersTextToImageProvider
from providers.local.text_to_video import ComfyUITextToVideoProvider
from providers.mock.image_to_video import MockImageToVideoProvider
from providers.mock.narration import MockNarrationProvider
from providers.mock.scene_planner import MockScenePlannerProvider
from providers.mock.subtitle import MockSubtitleProvider
from providers.mock.text_to_image import MockTextToImageProvider
from providers.mock.text_to_video import MockTextToVideoProvider

logger = logging.getLogger(__name__)

ProviderFactory = Callable[[], Any]


@dataclass(frozen=True)
class ProviderSpec:
    env_var: str
    default_name: str
    factories: dict[str, ProviderFactory]


_PROVIDER_SPECS: dict[str, ProviderSpec] = {
    "scene_planner": ProviderSpec(
        env_var="SCENE_PLANNER_PROVIDER",
        default_name="mock",
        factories={"mock": MockScenePlannerProvider, "local": LocalScenePlannerProvider},
    ),
    "text_to_image": ProviderSpec(
        env_var="TEXT_TO_IMAGE_PROVIDER",
        default_name="mock",
        factories={"mock": MockTextToImageProvider, "local": DiffusersTextToImageProvider},
    ),
    "image_to_video": ProviderSpec(
        env_var="IMAGE_TO_VIDEO_PROVIDER",
        default_name="mock",
        factories={"mock": MockImageToVideoProvider, "local": ComfyUIImageToVideoProvider},
    ),
    "text_to_video": ProviderSpec(
        env_var="TEXT_TO_VIDEO_PROVIDER",
        default_name="mock",
        factories={"mock": MockTextToVideoProvider, "local": ComfyUITextToVideoProvider},
    ),
    "narration": ProviderSpec(
        env_var="NARRATION_PROVIDER",
        default_name="mock",
        factories={"mock": MockNarrationProvider, "local": CoquiNarrationProvider},
    ),
    "subtitle": ProviderSpec(
        env_var="SUBTITLE_PROVIDER",
        default_name="mock",
        factories={"mock": MockSubtitleProvider, "local": LocalSubtitleProvider},
    ),
}


@dataclass(frozen=True)
class ActiveProviders:
    scene_planner: ScenePlannerProvider
    text_to_image: TextToImageProvider
    image_to_video: ImageToVideoProvider
    text_to_video: TextToVideoProvider
    narration: NarrationProvider
    subtitle: SubtitleProvider


def _resolve_provider_name(
    provider_key: str,
    config: Mapping[str, str] | None,
    env: Mapping[str, str],
) -> str:
    spec = _PROVIDER_SPECS[provider_key]
    config_name = (config or {}).get(provider_key)
    if config_name:
        return config_name.lower()
    return env.get(spec.env_var, spec.default_name).lower()


def _build_provider(provider_key: str, provider_name: str) -> Any:
    spec = _PROVIDER_SPECS[provider_key]
    if provider_name not in spec.factories:
        supported = ", ".join(sorted(spec.factories))
        raise ValueError(f"Unsupported {provider_key} provider '{provider_name}'. Supported: {supported}")

    factory = spec.factories[provider_name]
    try:
        return factory()
    except ProviderNotConfiguredError as exc:
        if provider_name == "mock":
            raise
        logger.warning(
            "%s provider '%s' unavailable (%s). Falling back to mock provider.",
            provider_key,
            provider_name,
            exc,
        )
        return spec.factories["mock"]()


def load_provider(provider_key: str, config: Mapping[str, str] | None = None, env: Mapping[str, str] | None = None) -> Any:
    resolved_env = env or os.environ
    provider_name = _resolve_provider_name(provider_key, config=config, env=resolved_env)
    return _build_provider(provider_key, provider_name)


def load_active_providers(
    config: Mapping[str, str] | None = None,
    env: Mapping[str, str] | None = None,
) -> ActiveProviders:
    return ActiveProviders(
        scene_planner=load_provider("scene_planner", config=config, env=env),
        text_to_image=load_provider("text_to_image", config=config, env=env),
        image_to_video=load_provider("image_to_video", config=config, env=env),
        text_to_video=load_provider("text_to_video", config=config, env=env),
        narration=load_provider("narration", config=config, env=env),
        subtitle=load_provider("subtitle", config=config, env=env),
    )
