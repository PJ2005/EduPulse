from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Optional
from app.services.test import test_generation_service, test_taking_service
from app.models.questions import Difficulty
from app.core.middleware import get_current_user

router = APIRouter()

@router.post("/generate", response_model=Dict)
async def generate_test(topic: str, num_questions: int = Query(10, gt=0), 
                        easy: Optional[int] = Query(None, ge=0),
                        medium: Optional[int] = Query(None, ge=0),
                        hard: Optional[int] = Query(None, ge=0),
                        user = Depends(get_current_user)):
    difficulty_balance: Optional[Dict[Difficulty, int]] = None
    if easy is not None or medium is not None or hard is not None:
        difficulty_balance = {}
        if easy is not None: difficulty_balance[Difficulty.EASY] = easy
        if medium is not None: difficulty_balance[Difficulty.MEDIUM] = medium
        if hard is not None: difficulty_balance[Difficulty.HARD] = hard

    try:
        return await test_generation_service.generate_test(topic, num_questions, difficulty_balance)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{topic}/start")
async def start_test(
    topic: str,
    num_questions: int = Query(10, description="Number of questions in the test"),
    difficulty: str = Query("MIXED", description="Difficulty level: EASY, MEDIUM, HARD, or MIXED"),
    user = Depends(get_current_user)):
    pass