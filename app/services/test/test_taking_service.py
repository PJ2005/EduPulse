from typing import List, Dict, Optional
from app.models.questions import Question, QuestionType
# Assuming database client 'db' and test_generation_service is available
# Also assuming a model for TestSession to track test progress
import uuid
import time

class TestSession:
    def __init__(self, test_id: str, user_id: str, questions: List[Dict], start_time: float, end_time: Optional[float] = None, answers: Optional[Dict[str, str]] = None):
        self.test_id = test_id
        self.user_id = user_id
        self.questions = questions  # List of question dictionaries (id, text, options)
        self.start_time = start_time
        self.end_time = end_time
        self.answers = answers if answers is not None else {}
        self.progress = 0  # Percentage of questions answered

    def update_answer(self, question_id: str, answer: str):
        self.answers[question_id] = answer
        self.progress = int(len(self.answers) / len(self.questions) * 100)

    def finish_test(self):
        self.end_time = time.time()

# In-memory storage for active test sessions (replace with database in real app)
test_sessions: Dict[str, TestSession] = {}

async def start_test(topic: str, user_id: str, num_questions: int = 10, difficulty_balance: Optional[Dict] = None) -> Dict:
    # Generate a test and create a test session
    from app.services.test import test_generation_service  # Import here to avoid circular import
    test_data = await test_generation_service.generate_test(topic, num_questions, difficulty_balance)
    test_id = test_data["test_id"]
    questions = test_data["questions"]

    session = TestSession(test_id=test_id, user_id=user_id, questions=questions, start_time=time.time())
    test_sessions[test_id] = session

    return {"test_id": test_id, "questions": questions, "estimated_time": test_data["estimated_time"], "message": "Test started"}

async def submit_answer(test_id: str, question_id: str, answer: str, user_id: str) -> Dict:
    session = test_sessions.get(test_id)
    if not session or session.user_id != user_id:
        raise ValueError("Invalid test session")

    session.update_answer(question_id, answer)
    print(f"Simulating submitting answer for test {test_id}, question {question_id}: {answer}")
    return {"message": "Answer submitted", "progress": session.progress}

async def finish_test(test_id: str, user_id: str) -> Dict:
    session = test_sessions.get(test_id)
    if not session or session.user_id != user_id:
        raise ValueError("Invalid test session")

    session.finish_test()
    print(f"Simulating finishing test {test_id}")
    #  In real implementation, save test results to DB and perform analysis
    #  For now, just remove the session from the in-memory store
    # del test_sessions[test_id]
    return {"message": "Test finished", "results": "(Results will be calculated)"}



async def get_test_progress(test_id: str, user_id: str) -> Dict:
    session = test_sessions.get(test_id)
    if not session or session.user_id != user_id:
        raise ValueError("Invalid test session")
    
    elapsed_time = int(time.time() - session.start_time)
    return {"progress": session.progress, "elapsed_time": elapsed_time}


async def get_test_results(test_id: str, user_id: str) -> Dict:
    # This is a placeholder.  In a real app, fetch results from the database
    print(f"Simulating getting results for test {test_id}")
    return {"score": 85, "correct_answers": 17, "incorrect_answers": 3, "time_taken": 1200}  # Example results