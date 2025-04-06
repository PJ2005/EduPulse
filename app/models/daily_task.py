from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DailyTask(BaseModel):
    task_id: str
    description: str
    priority: int = Field(..., gt=0, le=5)  # Priority from 1 to 5
    status: str = Field(..., pattern="^(pending|in_progress|completed)$")  # Status can be pending, in_progress, or completed
    due_date: Optional[datetime] = None
    notes: Optional[str] = None
    # Add other relevant fields as needed, e.g.:
    # category: Optional[str] = None
    # estimated_time: Optional[int] = None  # in minutes