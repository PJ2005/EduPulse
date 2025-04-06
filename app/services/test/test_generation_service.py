from typing import List, Dict, Optional
from app.models.questions import Question, Difficulty
import random
# Assuming question_service is available to fetch questions
from app.services.test import question_service
import uuid

async def generate_test(topic: str, num_questions: int = 10, difficulty_balance: Optional[Dict[Difficulty, int]] = None) -> Dict:
    # Basic test generation -  improve with adaptive algorithms
    if not difficulty_balance:
        # Default: Even distribution
        difficulty_balance = {Difficulty.EASY: num_questions // 3, Difficulty.MEDIUM: num_questions // 3, Difficulty.HARD: num_questions - (2 * (num_questions // 3))}
    else:
        # Ensure the difficulty counts sum up to the total number of questions
        if sum(difficulty_balance.values()) != num_questions:
            raise ValueError("Difficulty balance counts do not match the total number of questions.")

    test_questions: List[Question] = []
    for difficulty, count in difficulty_balance.items():
        available_questions = await question_service.list_questions(topic=topic, difficulty=difficulty)
        if len(available_questions) < count:
            raise ValueError(f"Not enough {difficulty.value} questions available for topic {topic}.")
        test_questions.extend(random.sample(available_questions, count))

    # Basic time estimation (improve)
    time_per_question = 60  # seconds
    estimated_time = num_questions * time_per_question

    test_id = str(uuid.uuid4())
    test_data = {
        "test_id": test_id,
        "topic": topic,
        "questions": [{"question_id": q.question_id, "text": q.text, "options": q.options if q.question_type == "multiple_choice" else None} for q in test_questions], # Send only necessary question data
        "estimated_time": estimated_time,
        "num_questions": num_questions
    }
    print(f"Simulating generating test: {test_data}")
    return test_data