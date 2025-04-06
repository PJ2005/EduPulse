from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from app.services.scheduler import break_service
from app.core.middleware import get_current_user
# Assuming authentication middleware 'get_current_user'

router = APIRouter()

@router.post("/pomodoro/start", response_model=Dict)
async def start_pomodoro(user = Depends(get_current_user)):
    try:
        return await break_service.start_pomodoro(user["user_id"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status", response_model=Dict)
async def check_break_status(user = Depends(get_current_user)):
    return await break_service.check_break_status(user["user_id"])

@router.post("/pomodoro/stop", response_model=Dict)
async def stop_pomodoro(user = Depends(get_current_user)):
    try:
        return await break_service.stop_pomodoro(user["user_id"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))