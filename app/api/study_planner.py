from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Optional
from app.services.scheduler import study_planner_service
from datetime import date
# Assuming authentication middleware 'get_current_user'

router = APIRouter()

@router.post("/generate", response_model=Dict)
async def generate_study_plan(exam_date_str: str, syllabus: List[str], title: str, description: Optional[str] = None, user = Depends(get_current_user)):
    try:
        exam_date = date.fromisoformat(exam_date_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format for exam_date. Use YYYY-MM-DD.")
    return await study_planner_service.generate_study_plan(user["user_id"], exam_date, syllabus, title, description)

@router.put("/{plan_id}", response_model=Dict)
async def adjust_study_plan(plan_id: str, adjustments: Dict, user = Depends(get_current_user)):
    try:
        return await study_planner_service.adjust_study_plan(plan_id, user["user_id"], adjustments)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) # Not Found for missing plan

@router.get("/{plan_id}/progress", response_model=Dict)
async def get_study_plan_progress(plan_id: str, user = Depends(get_current_user)):
    return await study_planner_service.get_study_plan_progress(plan_id, user["user_id"])

@router.get("/{plan_id}/visualization", response_model=Dict)
async def get_study_plan_visualization(plan_id: str, user = Depends(get_current_user)):
    try:
        study_plan = await study_planner_service.adjust_study_plan(plan_id, user["user_id"], {})
        progress = await study_planner_service.get_study_plan_progress(plan_id, user["user_id"])
        return await study_planner_service.prepare_plan_visualization(study_plan, progress)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) # Not Found for missing plan