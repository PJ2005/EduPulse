from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class NoteVersion(BaseModel):
    """Model for representing a version of a note"""
    note_id: str
    version: int
    content: str
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Note(BaseModel):
    """Model for representing a generated note"""
    note_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content_id: str
    user_id: str
    title: str
    content: str
    version: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    format_options: Dict = {}
    learning_mode: Optional[str] = None
