from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class StudyPlan(BaseModel):
    plan_id: str
    topic_id: str
    start_time: datetime
    end_time: datetime
    goal: Optional[str] = None
    notes: Optional[str] = None

class DailyTask(BaseModel):
    task_id: str
    description: str
    priority: int = Field(..., gt=0, le=5)  # Priority from 1 to 5
    status: str = Field(..., pattern="^(pending|in_progress|completed)$")  # Status can be pending, in_progress, or completed
    due_date: Optional[datetime] = None
    notes: Optional[str] = None

class Break(BaseModel):
    start_time: datetime
    end_time: datetime
    activity: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None

class Scheduler(BaseModel):
    schedule_id: str
    user_id: str
    study_plans: List[StudyPlan] = []
    daily_tasks: List[DailyTask] = []
    breaks: List[Break] = []
    # Add other relevant fields as needed, e.g.:
    # notes: Optional[str] = None