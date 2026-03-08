from pydantic import BaseModel


class JobBase(BaseModel):
    project_id: int
    type: str
    status: str = "queued"
    payload_json: str = "{}"
    result_json: str = "{}"


class JobCreate(JobBase):
    pass


class JobRead(JobBase):
    id: int

    model_config = {"from_attributes": True}
