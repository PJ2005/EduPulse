from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Optional
from app.services.scheduler import calendar_service
from app.models.schedule import Task, Event, CalendarView
from datetime import date
# Assuming authentication middleware 'get_current_user'

router = APIRouter()

@router.post("/tasks/", response_model=str)
async def create_task(task_data: Dict, user = Depends(get_current_user)):
    task_data["user_id"] = user["user_id"]
    return await calendar_service.create_task(task_data)

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str, user = Depends(get_current_user)):
    task = await calendar_service.get_task(task_id, user["user_id"])
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=bool)
async def update_task(task_id: str, task_data: Dict, user = Depends(get_current_user)):
    return await calendar_service.update_task(task_id, user["user_id"], task_data)

@router.delete("/tasks/{task_id}", response_model=bool)
async def delete_task(task_id: str, user = Depends(get_current_user)):
    return await calendar_service.delete_task(task_id, user["user_id"])

@router.post("/events/", response_model=str)
async def create_event(event_data: Dict, user = Depends(get_current_user)):
    event_data["user_id"] = user["user_id"]
    return await calendar_service.create_event(event_data)

@router.get("/events/{event_id}", response_model=Event)
async def get_event(event_id: str, user = Depends(get_current_user)):
    event = await calendar_service.get_event(event_id, user["user_id"])
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.put("/events/{event_id}", response_model=bool)
async def update_event(event_id: str, event_data: Dict, user = Depends(get_current_user)):
    return await calendar_service.update_event(event_id, user["user_id"], event_data)

@router.delete("/events/{event_id}", response_model=bool)
async def delete_event(event_id: str, user = Depends(get_current_user)):
    return await calendar_service.delete_event(event_id, user["user_id"])

@router.get("/view/{date_str}", response_model=CalendarView)
async def get_calendar_view(date_str: str, user = Depends(get_current_user)):
    try:
        date_obj = date.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    return await calendar_service.get_calendar_view(user["user_id"], date_obj)