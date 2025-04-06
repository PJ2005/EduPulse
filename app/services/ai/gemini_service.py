import google.generativeai as genai
from typing import List, Dict, Any, Optional
import logging
from app.core.config import settings

# Configure logger
logger = logging.getLogger(__name__)

class GeminiService:
    """
    Service for interacting with Google's Gemini API.
    Provides methods for text generation and other AI capabilities.
    """
    
    def __init__(self):
        """Initialize the Gemini service with API key from environment variables."""
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set. Gemini AI functionality will be limited.")
        
        # Configure the Gemini API client
        genai.configure(api_key=self.api_key)
        
        # Default model for text generation
        self.default_model = "gemini-1.5-pro"
    
    async def generate_text(self, prompt: str, 
                           temperature: float = 0.7, 
                           max_tokens: int = 800,
                           model: Optional[str] = None) -> str:
        """
        Generate text based on a prompt using Gemini API.
        
        Args:
            prompt: The text prompt to generate from
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            model: Model to use (defaults to gemini-1.5-pro)
            
        Returns:
            Generated text as a string
        """
        try:
            # Use specified model or default
            model_to_use = model or self.default_model
            
            # Get the generative model
            generative_model = genai.GenerativeModel(model_to_use)
            
            # Set generation config
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                "top_p": 0.95,
                "top_k": 40
            }
            
            # Generate content
            response = generative_model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Return the generated text
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating text with Gemini: {str(e)}")
            # Return a fallback response to avoid breaking the application
            return "I couldn't generate content for this prompt. Please try again later."
    
    async def generate_structured_content(self, prompt: str, 
                                        structure_type: str,
                                        context: Optional[Dict[str, Any]] = None,
                                        temperature: float = 0.3) -> Dict[str, Any]:
        """
        Generate structured content (like study notes, test questions, explanations)
        
        Args:
            prompt: Base prompt for generation
            structure_type: Type of content to generate (notes, questions, explanation)
            context: Additional context to include in the prompt
            temperature: Controls randomness (lower for more focused outputs)
            
        Returns:
            Dictionary containing the structured content
        """
        try:
            # Build a more specific prompt based on the structure type
            enhanced_prompt = self._build_structured_prompt(prompt, structure_type, context)
            
            # Generate content with lower temperature for more focused output
            generative_model = genai.GenerativeModel(self.default_model)
            
            # Generate content
            response = generative_model.generate_content(
                enhanced_prompt,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": 1500,
                    "top_p": 0.95,
                    "top_k": 40
                }
            )
            
            # Parse the response based on structure type
            if structure_type == "notes":
                # Extract structured notes
                return {
                    "content": response.text,
                    "structure_type": structure_type,
                    "success": True
                }
            elif structure_type == "questions":
                # For test questions, attempt to parse as structured data
                # This would require more sophisticated parsing in a real implementation
                return {
                    "questions": response.text.split("\n\n"),
                    "structure_type": structure_type,
                    "success": True
                }
            else:
                # Default case
                return {
                    "content": response.text,
                    "structure_type": structure_type,
                    "success": True
                }
                
        except Exception as e:
            logger.error(f"Error generating structured content with Gemini: {str(e)}")
            return {
                "content": "Failed to generate content. Please try again later.",
                "structure_type": structure_type,
                "success": False,
                "error": str(e)
            }
    
    def _build_structured_prompt(self, base_prompt: str, structure_type: str, 
                               context: Optional[Dict[str, Any]] = None) -> str:
        """
        Build a specific prompt based on the desired structure type and context.
        
        Args:
            base_prompt: The core prompt text
            structure_type: Type of content (notes, questions, explanation)
            context: Additional context like user preferences, learning style
            
        Returns:
            Enhanced prompt string
        """
        # Start with the base prompt
        enhanced_prompt = base_prompt
        
        # Add structure-specific instructions
        if structure_type == "notes":
            enhanced_prompt = f"""Generate well-structured study notes based on the following content:

{base_prompt}

Please organize the notes with clear headings, bullet points, and highlight key concepts.
Include a brief summary at the beginning and focus on the most important information.
"""
            
            # Add learning style customization if available in context
            if context and "learning_style" in context:
                learning_style = context["learning_style"]
                if learning_style == "visual":
                    enhanced_prompt += "\nInclude descriptions of diagrams or visual aids that would help illustrate these concepts."
                elif learning_style == "auditory":
                    enhanced_prompt += "\nStructure the notes in a conversational style that would be easy to understand when read aloud."
                elif learning_style == "socratic":
                    enhanced_prompt += "\nInclude thought-provoking questions throughout to encourage deeper understanding of the material."
        
        elif structure_type == "questions":
            enhanced_prompt = f"""Create test questions based on the following content:

{base_prompt}

Generate a mix of multiple-choice and short-answer questions that test understanding of key concepts.
For each multiple-choice question, provide 4 options with one correct answer clearly indicated.
"""
            
            # Add difficulty customization if available in context
            if context and "difficulty" in context:
                difficulty = context["difficulty"]
                enhanced_prompt += f"\nThe questions should be at a {difficulty} difficulty level."
        
        elif structure_type == "explanation":
            enhanced_prompt = f"""Provide a clear explanation of the following concept:

{base_prompt}

Break down complex ideas into simpler terms. Use analogies where helpful.
"""
        
        # Add any additional context-based customizations
        if context and "tone" in context:
            enhanced_prompt += f"\nPlease use a {context['tone']} tone in your response."
            
        return enhanced_prompt

# Create global instance
gemini_service = GeminiService()
