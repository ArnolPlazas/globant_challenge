from pydantic import BaseModel

class JobBase(BaseModel):
    id: int
    job: str

class JobCreate(JobBase):
    pass