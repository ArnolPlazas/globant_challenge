from pydantic import BaseModel

class HireStats(BaseModel):
    id: int
    department: str
    hired: int