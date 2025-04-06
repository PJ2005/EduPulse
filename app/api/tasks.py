from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from app.services.scheduler import task_service
from app.models.schedule import TaskStatus
from datetime import date
from app.core.middleware import get_current_user
# Assuming authentication middleware 'get_current_user'

router = APIRouter()

@router.put("/{task_id}/status/{status}", response_model=bool)
async def update_task_status(task_id: str, status: TaskStatus, user = Depends(get_current_user)):
    return await task_service.update_task_status(task_id, user["user_id"], status)

@router.put("/{task_id}/postpone/{new_deadline_str}", response_model=bool)
async def postpone_task(task_id: str, new_deadline_str: str, user = Depends(get_current_user)):
    try:
        new_deadline = date.fromisoformat(new_deadline_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    return await task_service.postpone_task(task_id, user["user_id"], new_deadline)

@router.post("/redistribute/{day_str}", response_model=List[Dict])  #  Returning List[Dict] for now, adjust as needed
async def redistribute_tasks(day_str: str, user = Depends(get_current_user)):
    try:
        day = date.fromisoformat(day_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    return await task_service.redistribute_tasks(user["user_id"], day)