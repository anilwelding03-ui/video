from pathlib import Path

from providers.mock.narration import MockNarrationProvider
from providers.mock.scene_planner import MockScenePlannerProvider
from providers.mock.subtitle import MockSubtitleProvider
from providers.registry import load_active_providers


def test_scene_planner_is_deterministic() -> None:
    planner = MockScenePlannerProvider()
    script = "Line one\nLine two\nLine three"

    plan_a = planner.plan_scenes(script, target_scene_count=2)
    plan_b = planner.plan_scenes(script, target_scene_count=2)

    assert plan_a == plan_b
    assert len(plan_a.scenes) == 2
    assert len(plan_a.scenes[0].shots) == 2


def test_registry_falls_back_to_mock() -> None:
    providers = load_active_providers(config={"text_to_image": "local"})
    assert providers.text_to_image.__class__.__name__ == "MockTextToImageProvider"


def test_subtitle_and_narration_outputs(tmp_path: Path) -> None:
    lines = ["Hello world", "Second line"]
    durations = [1.2, 1.8]

    srt_path = tmp_path / "out.srt"
    wav_path = tmp_path / "voice.wav"

    subtitle_path = MockSubtitleProvider().build_srt(lines, durations, srt_path)
    narration = MockNarrationProvider().synthesize(lines, durations, wav_path)

    assert subtitle_path.exists()
    text = subtitle_path.read_text(encoding="utf-8")
    assert "00:00:00,000 --> 00:00:01,200" in text
    assert narration.path.exists()
    assert narration.duration_seconds > 3.0
