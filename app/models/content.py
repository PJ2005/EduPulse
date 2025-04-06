from typing import Dict, List, Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime

class FileUpload(BaseModel):
    """Model for uploaded file information"""
    file_name: str
    file_type: str
    file_size: int
    gcs_path: Optional[str] = None  # Path in cloud storage
    
class ProcessedNote(BaseModel):
    """Model for processed notes extracted from content"""
    note_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    text: str
    topic_id: Optional[str] = None
    version: int = 1
    
class Content(BaseModel):
    """Model for content uploaded by users"""
    content_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    original_upload: FileUpload
    processed_notes: List[ProcessedNote] = []
    yet_to_read: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    metadata: Dict = {}