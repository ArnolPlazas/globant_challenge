from pydantic import BaseModel

class HireQuarterStats(BaseModel):
    department: str
    job: str
    Q1: int
    Q2: int
    Q3: int
    Q4: int