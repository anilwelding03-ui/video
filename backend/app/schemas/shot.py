from pydantic import BaseModel


class ShotBase(BaseModel):
    scene_id: int
    index: int
    prompt_master: str
    prompt_negative: str = ""
    duration_s: int = 0
    seed: int | None = None


class ShotCreate(ShotBase):
    pass


class ShotRead(ShotBase):
    id: int

    model_config = {"from_attributes": True}
