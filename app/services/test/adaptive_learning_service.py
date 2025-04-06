import logging
from typing import List, Dict, Any
from app.services.ai.gemini_service import gemini_service
from app.services.test.question_service import get_question

# Configure logger
logger = logging.getLogger(__name__)

# This would be a database interaction in a real implementation
user_performance_history = {}

async def adjust_difficulty(user_id: str, topic: str) -> str:
    """
    Determine the appropriate difficulty level for a user based on performance history.
    
    Args:
        user_id: The ID of the user
        topic: The topic to adjust difficulty for
        
    Returns:
        String indicating the suggested difficulty level (EASY, MEDIUM, or HARD)
    """
    # In a real implementation, this would fetch from a performance database
    # For now, use mock data
    if user_id in user_performance_history and topic in user_performance_history[user_id]:
        accuracy = user_performance_history[user_id][topic].get("accuracy", 0)
        
        if accuracy < 40:
            return "EASY"
        elif accuracy < 75:
            return "MEDIUM"
        else:
            return "HARD"
    
    # Default to MEDIUM if no history
    return "MEDIUM"

async def spaced_repetition(user_id: str, incorrect_questions: List[Dict]) -> List[Dict]:
    """
    Schedule spaced repetition for incorrectly answered questions.
    
    Args:
        user_id: The ID of the user
        incorrect_questions: List of dictionaries containing question_id
        
    Returns:
        List of dictionaries with question_id and review_in field
    """
    # Simple spaced repetition algorithm - in a real implementation, this would be more sophisticated
    result = []
    
    for idx, question in enumerate(incorrect_questions):
        question_id = question.get("question_id", "")
        # Simple algorithm: review more recent mistakes sooner
        review_in = f"{(idx % 3) + 1} days"  # 1, 2, or 3 days
        
        result.append({
            "question_id": question_id,
            "review_in": review_in
        })
    
    return result

async def generate_personalized_explanations(question_id: str, incorrect_answer: str) -> str:
    """
    Generate a personalized explanation for an incorrectly answered question using Gemini AI.
    
    Args:
        question_id: The ID of the question
        incorrect_answer: The user's incorrect answer
        
    Returns:
        Personalized explanation string
    """
    try:
        # Get the question details
        question = await get_question(question_id)
        
        if not question:
            return "Question not found. Please try again."
        
        # For multiple choice questions, identify the correct answer
        correct_answer = None
        if question.get("question_type") == "multiple_choice":
            options = question.get("options", [])
            for option in options:
                if option.get("is_correct", False):
                    correct_answer = option.get("text", "")
                    break
        
        # Create a prompt for Gemini
        prompt = f"""Generate a personalized explanation for this educational question:

Question: {question.get('text', '')}

Student's incorrect answer: {incorrect_answer}

Correct answer: {correct_answer or "Not provided"}

Please explain why the student's answer is incorrect and provide a clear explanation of the correct answer.
Include analogies or examples if they would help with understanding.
Be encouraging and supportive in your explanation.
"""

        # Generate explanation using Gemini
        explanation = await gemini_service.generate_text(
            prompt=prompt,
            temperature=0.3,  # Lower temperature for more focused educational content
            max_tokens=500
        )
        
        return explanation
        
    except Exception as e:
        logger.error(f"Error generating personalized explanation: {str(e)}")
        return "I couldn't generate a personalized explanation at the moment. Please try again later."

async def recommend_study_focus(user_id: str) -> List[str]:
    """
    Generate study focus recommendations based on user performance.
    
    Args:
        user_id: The ID of the user
        
    Returns:
        List of study recommendations
    """
    # In a real implementation, this would analyze performance data
    # For now, return sample recommendations
    return [
        "Focus on reviewing concepts in Physics related to Mechanics.",
        "Practice more numerical problems in Calculus.",
        "Review the definitions and theorems in Linear Algebra."
    ]