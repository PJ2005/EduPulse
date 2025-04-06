from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StudyPlan(BaseModel):
    plan_id: str
    topic_id: str
    start_time: datetime
    end_time: datetime
    # Add other relevant fields as needed, e.g.:
    # goal: Optional[str] = None
    # notes: Optional[str] = None