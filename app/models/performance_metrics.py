from pydantic import BaseModel
from typing import List, Optional

class TestResult(BaseModel):
    test_id: str
    score: float
    # Add other test result data as needed

class TimeTracking(BaseModel):
    activity: str  # e.g., "studying", "testing"
    topic_id: Optional[str] = None
    time_spent: int  # in seconds
    # Add other time tracking data as needed

class PerformanceMetrics(BaseModel):
    user_id: str
    test_results: List[TestResult] = []
    learning_progress: dict = {}  # Define structure for tracking progress as needed
    time_tracking: List[TimeTracking] = []
    difficulty_handling: dict = {}  # Define structure for difficulty analysis as needed
    # Add other metrics as needed