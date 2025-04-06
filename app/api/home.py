from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict
from app.services.home import reminder_service, todo_service, subject_service, spotify_service
from app.core.middleware import get_current_user
# Assuming authentication middleware 'get_current_user' provides user info

router = APIRouter()

# Reminder Endpoints
reminder_router = APIRouter()

@reminder_router.get("/", response_model=List[Dict])  # Using Dict as model is not yet defined
async def get_reminders(user = Depends(get_current_user)):
    reminders = await reminder_service.get_topics_to_read(user["user_id"])
    return reminders

@reminder_router.put("/{reminder_id}/status")
async def update_reminder(reminder_id: str, status: str, user = Depends(get_current_user)):
    await reminder_service.update_reminder_status(reminder_id, status)
    return {"message": "Reminder status updated"}

@reminder_router.get("/notifications/preferences")
async def get_notification_prefs(user = Depends(get_current_user)):
    prefs = await reminder_service.get_notification_preferences(user["user_id"])
    return prefs

@reminder_router.put("/notifications/preferences")
async def update_notification_prefs(preferences: dict, user = Depends(get_current_user)):
    await reminder_service.update_notification_preferences(user["user_id"], preferences)
    return {"message": "Notification preferences updated"}

router.include_router(reminder_router, prefix="/reminders", tags=["reminders"])

# To-Do Endpoints
todo_router = APIRouter()

@todo_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(task: str, due_date: str, priority: int, user = Depends(get_current_user)):  # Using str for due_date initially
    item_id = await todo_service.create_todo_item(user["user_id"], task, due_date, priority)
    return {"item_id": item_id, "message": "To-do item created"}

@todo_router.get("/", response_model=List[Dict])  # Using Dict as model is not yet defined
async def get_todos(for_date: str = Query(None), user = Depends(get_current_user)):  # Using str for for_date initially
    items = await todo_service.get_todo_items(user["user_id"], for_date)
    return items

@todo_router.put("/{item_id}")
async def update_todo(item_id: str, updates: dict, user = Depends(get_current_user)):
    await todo_service.update_todo_item(item_id, **updates)
    return {"message": "To-do item updated"}

@todo_router.delete("/{item_id}")
async def delete_todo(item_id: str, user = Depends(get_current_user)):
    await todo_service.delete_todo_item(item_id)
    return {"message": "To-do item deleted"}

router.include_router(todo_router, prefix="/todos", tags=["todos"])

# Subject Endpoints
subject_router = APIRouter()

@subject_router.get("/hierarchy", response_model=Dict)
async def get_subjects(user = Depends(get_current_user)):
    hierarchy = await subject_service.get_subject_hierarchy(user["user_id"])
    return hierarchy

@subject_router.get("/{subject_id}/progress", response_model=Dict)
async def get_progress(subject_id: str, user = Depends(get_current_user)):
    progress = await subject_service.get_subject_progress(user["user_id"], subject_id)
    return progress

@subject_router.get("/activity/recent", response_model=List[Dict])  # Using Dict as model is not yet defined
async def get_activity(limit: int = 5, user = Depends(get_current_user)):
    activities = await subject_service.get_recent_activity(user["user_id"], limit)
    return activities

router.include_router(subject_router, prefix="/subjects", tags=["subjects"])

# Spotify Endpoints
spotify_router = APIRouter()

@spotify_router.get("/auth-url")
def get_auth_url():
    auth_url = spotify_service.get_auth_url()
    return {"auth_url": auth_url}

@spotify_router.get("/callback")
async def spotify_callback(code: str = Query(...), user = Depends(get_current_user)):
    # Assuming spotify_service.spotify_callback handles token storage
    return {"message": "Spotify connected"}

@spotify_router.get("/preferences", response_model=Dict)
async def get_spotify_prefs(user = Depends(get_current_user)):
    prefs = await spotify_service.get_music_preferences(user["user_id"])
    return prefs

@spotify_router.put("/preferences")
async def update_spotify_prefs(preferences: Dict, user = Depends(get_current_user)):
    await spotify_service.update_music_preferences(user["user_id"], preferences)
    return {"message": "Spotify preferences updated"}

@spotify_router.get("/playlist", response_model=List[Dict])  # Using Dict as model is not yet defined
async def get_playlist(activity: str, user = Depends(get_current_user)):
    playlist = await spotify_service.get_study_playlist(user["user_id"], activity)  # Passing user_id for token retrieval
    return playlist

@spotify_router.post("/playback")
async def control_spotify(action: str, user = Depends(get_current_user)):
    await spotify_service.control_playback(user["user_id"], action)  # Passing user_id for token retrieval
    return {"message": f"Spotify playback {action}"}

router.include_router(spotify_router, prefix="/spotify", tags=["spotify"])
