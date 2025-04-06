from typing import Dict, Optional
import logging
from app.services.ai.gemini_service import gemini_service
from app.core.config import settings

# Configure logger
logger = logging.getLogger(__name__)

async def generate_note_content(prompt: str, user_preferences: Optional[Dict] = None, learning_mode: Optional[str] = None) -> str:
    """
    Generate note content using Google's Gemini AI.
    
    Args:
        prompt: The prompt to generate notes from
        user_preferences: User preferences for note style and tone
        learning_mode: Learning mode (socratic, example, visual, auditory, exam_prep)
        
    Returns:
        Generated note content as a string
    """
    try:
        # Create context dictionary for structured prompt
        context = {}
        
        if user_preferences:
            context.update(user_preferences)
        
        if learning_mode:
            context["learning_style"] = learning_mode
        
        # Generate structured content
        result = await gemini_service.generate_structured_content(
            prompt=prompt,
            structure_type="notes",
            context=context,
            temperature=0.4  # Lower temperature for more focused educational content
        )
        
        if result["success"]:
            return result["content"]
        else:
            logger.error(f"Failed to generate note content: {result.get('error', 'Unknown error')}")
            return "Note generation failed. Please try again later."
            
    except Exception as e:
        logger.error(f"Error in generate_note_content: {str(e)}")
        return "An error occurred while generating notes. Please try again later."
