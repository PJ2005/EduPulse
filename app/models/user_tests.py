from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

class Response(BaseModel):
    question_id: str
    answer: Any  # Flexible type to accommodate different question formats
    correct: bool

class UserTests(BaseModel):
    user_id: str
    test_id: str
    responses: List[Response]
    score: float
    time_taken: int
    completed_at: datetime
    # Add other test attempt data fields as needed
    # For example:
    # feedback: Dict[str, str] = Field(default_factory=dict)