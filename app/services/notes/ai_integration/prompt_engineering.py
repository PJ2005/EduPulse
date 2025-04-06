from typing import Dict, Optional

def create_note_prompt(content: str, user_preferences: Optional[Dict] = None, learning_mode: Optional[str] = None) -> str:
    """
    Create an effective prompt for note generation.
    
    Args:
        content: The source content to generate notes from
        user_preferences: User preferences for note style and tone
        learning_mode: Learning mode (socratic, example, visual, auditory, exam_prep)
        
    Returns:
        A well-crafted prompt string
    """
    prompt = f"Generate concise and well-structured notes from the following content:\n\n{content}\n\n"

    if user_preferences:
        style = user_preferences.get("style", "clear and concise")
        tone = user_preferences.get("tone", "neutral")
        prompt += f"Format the notes in a {style} style with a {tone} tone. "

    if learning_mode:
        if learning_mode == "socratic":
            prompt += "Incorporate questions to encourage active recall and critical thinking. "
        elif learning_mode == "example":
            prompt += "Include relevant examples and analogies to illustrate key concepts. "
        elif learning_mode == "visual":
            prompt += "Suggest diagrams or visual aids to represent the information. "
        elif learning_mode == "auditory":
            prompt += "Structure the notes in a way that is easy to understand when read aloud. "
        elif learning_mode == "exam_prep":
            prompt += "Highlight key concepts and provide practice questions suitable for exam preparation. "

    prompt += "Focus on the most important information and use appropriate headings and subheadings."
    return prompt