from providers.errors import ProviderNotConfiguredError
from providers.interfaces import ScenePlannerProvider, StoryboardPlan


class LocalScenePlannerProvider(ScenePlannerProvider):
    def __init__(self) -> None:
        raise ProviderNotConfiguredError(
            "Local scene planner is not configured. Configure your LLM scene-planning backend and set "
            "SCENE_PLANNER_PROVIDER=local."
        )

    def plan_scenes(self, script: str, target_scene_count: int | None = None) -> StoryboardPlan:
        raise NotImplementedError
