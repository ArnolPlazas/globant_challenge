from pydantic import BaseModel

class DepartmentBase(BaseModel):
    id: int
    department: str

class DepartmentCreate(DepartmentBase):
    pass