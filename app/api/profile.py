from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Optional
from app.services.user import profile_service
from app.models.user import UserProfile, UserSettings, LearningPace, NotificationFrequency, AccountManagement
# Assuming authentication middleware 'get_current_user'

router = APIRouter()

@router.get("/", response_model=UserProfile)
async def get_user_profile(user = Depends(get_current_user)):
    profile = await profile_service.get_user_profile(user["user_id"])
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/", response_model=bool)
async def update_user_profile(profile_data: Dict, user = Depends(get_current_user)):
    return await profile_service.update_user_profile(user["user_id"], profile_data)

@router.get("/settings", response_model=UserSettings)
async def get_user_settings(user = Depends(get_current_user)):
    return await profile_service.get_user_settings(user["user_id"])

@router.put("/settings", response_model=bool)
async def update_user_settings(settings_data: Dict, user = Depends(get_current_user)):
    return await profile_service.update_user_settings(user["user_id"], settings_data)

@router.put("/preferences", response_model=bool)
async def update_learning_preferences(learning_pace: LearningPace, preferred_subjects: List[str], user = Depends(get_current_user)):
    return await profile_service.update_learning_preferences(user["user_id"], learning_pace, preferred_subjects)

@router.put("/privacy", response_model=bool)
async def update_privacy_settings(privacy_settings: Dict, user = Depends(get_current_user)):
    return await profile_service.update_privacy_settings(user["user_id"], privacy_settings)

@router.put("/notifications", response_model=bool)
async def update_notification_settings(notification_settings: Dict, user = Depends(get_current_user)):
    return await profile_service.update_notification_settings(user["user_id"], notification_settings)

@router.get("/account", response_model=AccountManagement)
async def get_account_management(user = Depends(get_current_user)):
    return await profile_service.get_account_management(user["user_id"])
