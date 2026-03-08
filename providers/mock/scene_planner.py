from __future__ import annotations

from providers.interfaces import ScenePlan, ScenePlannerProvider, ShotPlan, StoryboardPlan


class MockScenePlannerProvider(ScenePlannerProvider):
    """Deterministic planner for local/dev pipelines."""

    def plan_scenes(self, script: str, target_scene_count: int | None = None) -> StoryboardPlan:
        lines = [line.strip() for line in script.splitlines() if line.strip()]
        if not lines:
            lines = ["Untitled sequence."]

        scene_count = max(1, target_scene_count or min(3, len(lines)))
        scenes: list[ScenePlan] = []

        for scene_index in range(scene_count):
            shots: list[ShotPlan] = []
            for shot_index in range(2):
                line = lines[(scene_index * 2 + shot_index) % len(lines)]
                shots.append(
                    ShotPlan(
                        shot_id=f"scene-{scene_index + 1:02d}-shot-{shot_index + 1:02d}",
                        prompt=f"{line} | cinematic storyboard frame {shot_index + 1}",
                        duration_seconds=3.0 + shot_index,
                        narration_line=line,
                    )
                )

            scenes.append(
                ScenePlan(
                    scene_id=f"scene-{scene_index + 1:02d}",
                    title=f"Scene {scene_index + 1}",
                    shots=shots,
                )
            )

        return StoryboardPlan(scenes=scenes)
