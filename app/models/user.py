from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict
import uuid
from datetime import date, datetime
from enum import Enum

class Profile(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    # Add other profile fields as needed


class Preferences(BaseModel):
    note_formatting: Optional[Dict] = None
    learning_styles: Optional[List[str]] = None
    # Add other preference fields as needed


class Education(BaseModel):
    level: Optional[str] = None
    subject_interests: Optional[List[str]] = None


class LearningPace(str, Enum):
    SLOW = "slow"
    MODERATE = "moderate"
    FAST = "fast"

class NotificationFrequency(str, Enum):
    IMMEDIATE = "immediate"
    DAILY = "daily"
    WEEKLY = "weekly"
    OFF = "off"

class UserProfile(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    bio: Optional[str] = None
    profile_picture_url: Optional[str] = None
    learning_pace: LearningPace = LearningPace.MODERATE
    preferred_subjects: List[str] = []  # e.g., ["Math", "Physics"]
    notification_settings: Dict = {
        "study_reminders": True,
        "progress_updates": NotificationFrequency.DAILY,
        "new_content_alerts": True,
    }
    privacy_settings: Dict = {
        "profile_visibility": "public",  #  Options: public, private, friends
        "activity_sharing": True,
    }

class UserSettings(BaseModel):
    user_id: str
    theme: str = "light"  #  Options: light, dark, system
    preferred_language: str = "en"  #  e.g., en, es, fr
    audio_volume: int = 100  #  Percentage
    playback_speed: float = 1.0


class AccountManagement(BaseModel):
    user_id: str
    is_active: bool = True
    last_login: Optional[datetime] = None
    # Add other fields as needed (e.g., roles, permissions)