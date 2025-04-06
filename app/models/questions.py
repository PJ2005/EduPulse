from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union
import uuid
from enum import Enum

class QuestionType(str, Enum):
    THEORETICAL = "theoretical"
    NUMERICAL = "numerical"
    MULTIPLE_CHOICE = "multiple_choice"
    DESCRIPTIVE = "descriptive"

class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class MultipleChoiceOption(BaseModel):
    text: str
    is_correct: bool

class Question(BaseModel):
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question_type: QuestionType
    topic: str  #  e.g., "Physics", "Calculus"
    subtopic: Optional[str] = None
    difficulty: Difficulty
    text: str  # The question itself
    solution: Optional[str] = None  # For numerical and theoretical
    options: Optional[List[MultipleChoiceOption]] = None  # For multiple choice
    answer: Optional[str] = None # For descriptive questions
    past_years: Optional[List[int]] = []  # List of years this question appeared
    metadata: Optional[Dict] = {}  # Tags, source, etc.

    class Config:
        use_enum_values = True