from pydantic import BaseModel

class EmployeeBase(BaseModel):
    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int

class EmployeeCreate(EmployeeBase):
    pass
