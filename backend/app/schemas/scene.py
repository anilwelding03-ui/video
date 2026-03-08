from pydantic import BaseModel


class SceneBase(BaseModel):
    project_id: int
    index: int
    title: str
    text: str
    duration_s: int = 0


class SceneCreate(SceneBase):
    pass


class SceneRead(SceneBase):
    id: int

    model_config = {"from_attributes": True}
