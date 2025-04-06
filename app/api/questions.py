from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Optional
from app.services.test import question_service
from app.models.questions import Question, QuestionType, Difficulty
from app.core.middleware import get_current_admin_user  # Add this import

router = APIRouter()

@router.post("/", response_model=str, dependencies=[Depends(get_current_admin_user)])
async def create_question(question_data: Dict):
    return await question_service.create_question(question_data)

@router.get("/{question_id}", response_model=Question)
async def get_question(question_id: str):
    question = await question_service.get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.put("/{question_id}", response_model=bool, dependencies=[Depends(get_current_admin_user)])
async def update_question(question_id: str, question_data: Dict):
    return await question_service.update_question(question_id, question_data)

@router.delete("/{question_id}", response_model=bool, dependencies=[Depends(get_current_admin_user)])
async def delete_question(question_id: str):
    return await question_service.delete_question(question_id)

@router.get("/", response_model=List[Question])
async def list_questions(topic: Optional[str] = Query(None), subtopic: Optional[str] = Query(None), difficulty: Optional[Difficulty] = Query(None)):
    return await question_service.list_questions(topic, subtopic, difficulty)