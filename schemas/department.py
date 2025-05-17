from pydantic import BaseModel

class DepartmentBase(BaseModel):
    id: int
    department: str

class DepartmentCreate(DepartmentBase):
    pass

class Department(DepartmentBase):
    class Config:
        from_attributes = True