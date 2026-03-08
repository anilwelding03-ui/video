from datetime import datetime

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    script_text: str = ""
    style_preset: str = "default"
    status: str = "draft"


class ProjectCreate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
