from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union
import uuid
from datetime import datetime, date, timedelta
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: Optional[str] = None
    subject: Optional[str] = None  # e.g., "Math", "Physics"
    topic: Optional[str] = None  # More specific
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 0  #  Higher value = higher priority (calculated)
    deadline: Optional[date] = None
    estimated_time: Optional[timedelta] = None  # How long the task should take
    recurring: bool = False
    recurrence_rule: Optional[str] = None  #  e.g., "RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR" (iCalendar format)
    user_id: str #  Associate task with a user

    class Config:
        use_enum_values = True

class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    user_id: str

class CalendarView(BaseModel):
    date: date
    events: List[Event] = []
    tasks: List[Task] = []  # Tasks scheduled for this date

class StudyPlan(BaseModel):
    plan_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    start_date: date
    end_date: date
    title: str
    description: Optional[str] = None
    daily_allocations: Dict[date, List[Union[Task, Event]]] = {}  # Tasks/Events for each day