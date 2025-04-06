from typing import Optional

from pydantic import BaseModel


class Topics(BaseModel):
    topic_id: str
    name: str
    parent_topic_id: Optional[str] = None
    subject: str
    difficulty: int
    priority: int
    time_estimate: int
    # Add other topic-related fields here as needed
    # Example:
    # description: Optional[str] = None