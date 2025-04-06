from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict
from app.services.test import adaptive_learning_service
# Assuming authentication middleware 'get_current_user'

router = APIRouter()

@router.get("/difficulty/{topic}", response_model=str)
async def get_suggested_difficulty(topic: str, user = Depends(get_current_user)):
    #  Get the suggested difficulty level for the user in a given topic
    return await adaptive_learning_service.adjust_difficulty(user["user_id"], topic)

@router.post("/repetition", response_model=List[Dict])
async def get_spaced_repetition_questions(incorrect_questions: List[Dict], user = Depends(get_current_user)):
    #  Get a list of questions for spaced repetition review
    return await adaptive_learning_service.spaced_repetition(user["user_id"], incorrect_questions)

@router.get("/explanation/{question_id}", response_model=str)
async def get_personalized_explanation(question_id: str, incorrect_answer: str = Query(...)):
    #  Get a personalized explanation for an incorrectly answered question
    return await adaptive_learning_service.generate_personalized_explanations(question_id, incorrect_answer)

@router.get("/recommendations", response_model=List[str])
async def get_study_recommendations(user = Depends(get_current_user)):
    #  Get personalized study focus recommendations
    return await adaptive_learning_service.recommend_study_focus(user["user_id"])