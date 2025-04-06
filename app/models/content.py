from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class OriginalUpload(BaseModel):
    file_name: str
    file_type: str
    gcs_path: str
    metadata: Optional[Dict] = None  # For other metadata


class Note(BaseModel):
    note_id: str
    text: str
    topic_id: str
    version: int
    other_fields: Optional[Dict] = None  # For other note fields


class Content(BaseModel):
    content_id: str
    user_id: str
    original_upload: OriginalUpload
    processed_notes: List[Note] = Field(default_factory=list)
    yet_to_read: bool = True
    created_at: datetime
    updated_at: datetime