from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Optional
from app.services.scheduler import ai_planning_service
from datetime import date, timedelta
from app.core.middleware import get_current_user
# Assuming authentication middleware 'get_current_user'

router = APIRouter()

@router.post("/analyze_task", response_model=Dict)
async def analyze_task(task_description: str):
    # Analyze a task description using an LLM
    return await ai_planning_service.analyze_task_with_llm(task_description)

@router.post("/balance_workload", response_model=Dict[date, List[Dict]])
async def balance_workload(tasks: List[Dict], available_time: Dict[str, int], user = Depends(get_current_user)):
    # Balance workload across available time
    #  The 'available_time' should be a dictionary where keys are dates (YYYY-MM-DD string) and values are available time in seconds
    #  The 'tasks' should be a list of task dictionaries, each with at least a task_id
    # Convert date strings to date objects and time in seconds to timedelta
    converted_available_time: Dict[date, timedelta] = {}
    for date_str, time_seconds in available_time.items():
        try:
            date_obj = date.fromisoformat(date_str)
            converted_available_time[date_obj] = timedelta(seconds=time_seconds)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Use YYYY-MM-DD.")

    return await ai_planning_service.balance_workload(user["user_id"], tasks, converted_available_time)

@router.post("/recommend_adjustments", response_model=List[str])
async def recommend_schedule_adjustments(current_schedule: Dict[str, List[Dict]], user = Depends(get_current_user)):
    # Recommend adjustments to the current schedule
    #  The 'current_schedule' should be a dictionary where keys are dates (YYYY-MM-DD string) and values are lists of task dictionaries
     # Convert date strings to date objects
    converted_schedule: Dict[date, List[Dict]] = {}
    for date_str, tasks in current_schedule.items():
        try:
            date_obj = date.fromisoformat(date_str)
            converted_schedule[date_obj] = tasks
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}. Use YYYY-MM-DD.")
    return await ai_planning_service.recommend_schedule_adjustments(user["user_id"], converted_schedule)