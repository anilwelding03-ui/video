"""Prompt assembly utilities for shot generation."""

from __future__ import annotations

from dataclasses import dataclass

STYLE_PRESETS: dict[str, dict[str, str]] = {
    "cinematic_realism": {
        "style": "cinematic realism",
        "lens_feel": "35mm film texture",
        "lighting": "motivated practical lighting",
        "color_palette": "rich neutrals with warm highlights",
        "negative": "plastic skin, over-sharpening, video noise",
    },
    "neo_noir": {
        "style": "neo-noir",
        "lens_feel": "anamorphic flare",
        "lighting": "high-contrast chiaroscuro",
        "color_palette": "teal shadows, amber accents",
        "negative": "flat contrast, blown highlights",
    },
    "dreamy_anime": {
        "style": "dreamy anime illustration",
        "lens_feel": "soft depth compression",
        "lighting": "ethereal bloom",
        "color_palette": "pastel gradients",
        "negative": "muddy lines, grainy edges",
    },
    "documentary": {
        "style": "grounded documentary",
        "lens_feel": "handheld vérité",
        "lighting": "available light",
        "color_palette": "true-to-life muted tones",
        "negative": "over-stylized bokeh, beauty retouch",
    },
}


@dataclass(slots=True)
class PromptFields:
    subject: str
    action: str
    environment: str
    mood: str
    camera_angle: str
    lens_feel: str
    lighting: str
    color_palette: str
    style: str
    continuity_notes: str
    negative_prompt: str


@dataclass(slots=True)
class ShotPrompts:
    master_prompt: str
    short_prompt: str
    negative_prompt: str
    motion_prompt: str
    camera_prompt: str


def build_prompt_fields(
    *,
    subject: str,
    action: str,
    environment: str,
    mood: str = "balanced",
    camera_angle: str = "eye-level",
    lens_feel: str = "natural perspective",
    lighting: str = "soft directional",
    color_palette: str = "cinematic neutral",
    style: str = "cinematic_realism",
    continuity_notes: str = "",
    negative_prompt: str = "",
    custom_style_prompt: str = "",
) -> PromptFields:
    """Create normalized prompt fields merged with a style preset."""
    preset = STYLE_PRESETS.get(style, STYLE_PRESETS["cinematic_realism"])
    style_label = preset["style"] if style in STYLE_PRESETS else style

    merged_lens = lens_feel if lens_feel != "natural perspective" else preset["lens_feel"]
    merged_lighting = lighting if lighting != "soft directional" else preset["lighting"]
    merged_palette = color_palette if color_palette != "cinematic neutral" else preset["color_palette"]

    style_text = style_label
    if custom_style_prompt.strip():
        style_text = f"{style_text}; {custom_style_prompt.strip()}"

    negative_parts = [preset.get("negative", ""), negative_prompt.strip()]
    merged_negative = ", ".join(part for part in negative_parts if part)

    return PromptFields(
        subject=subject.strip(),
        action=action.strip(),
        environment=environment.strip(),
        mood=mood.strip(),
        camera_angle=camera_angle.strip(),
        lens_feel=merged_lens.strip(),
        lighting=merged_lighting.strip(),
        color_palette=merged_palette.strip(),
        style=style_text.strip(),
        continuity_notes=continuity_notes.strip(),
        negative_prompt=merged_negative.strip(),
    )


def build_shot_prompts(fields: PromptFields) -> ShotPrompts:
    """Generate prompt variants for a single shot."""
    master = (
        f"{fields.subject} {fields.action} in {fields.environment}. "
        f"Mood: {fields.mood}. Camera: {fields.camera_angle}, {fields.lens_feel}. "
        f"Lighting: {fields.lighting}. Palette: {fields.color_palette}. "
        f"Style: {fields.style}. Continuity: {fields.continuity_notes or 'maintain prior look and costume continuity'}."
    )

    short = f"{fields.subject}, {fields.action}, {fields.environment}, {fields.style}"
    motion = f"Motion beats: {fields.action}; emotional rhythm: {fields.mood}."
    camera = f"Camera direction: {fields.camera_angle}; lens feel: {fields.lens_feel}; lighting motivation: {fields.lighting}."

    return ShotPrompts(
        master_prompt=master,
        short_prompt=short,
        negative_prompt=fields.negative_prompt,
        motion_prompt=motion,
        camera_prompt=camera,
    )
