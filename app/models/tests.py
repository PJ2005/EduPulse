from typing import Optional, Any
from pydantic import BaseModel, Field


class Tests(BaseModel):
    question_id: str
    topic_id: str
    question_format: str
    question_text: str
    answer: Any  # Structure will depend on question_format
    difficulty: int = Field(..., ge=1, le=5)  # Assuming difficulty is on a 1-5 scale
    past_year: bool = False
    # Add other question-related fields as needed