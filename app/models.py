from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Task(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = None
    due_date: datetime
    priority: str = Field(..., regex="^(Low|Medium|High)$")
    status: str = Field(default="Pending", regex="^(Pending|Completed)$")
