# EduPulse Note Generation System

## Overview

The EduPulse Note Generation System leverages AI to create personalized and effective study notes from user-provided content. It integrates with Vertex AI to process content, extract key information, and structure it into concise, well-organized notes. The system adapts to user preferences and learning styles, offering features for various learning modes and exam preparation. It seamlessly integrates with the EduPulse content management system, allowing users to generate notes from their uploaded materials.

## System Architecture

The system is composed of the following key components:

*   **API Endpoints (`app/api/notes.py`):** Defines the API routes for interacting with the note generation system, including note generation, retrieval, updating, and customization.
*   **Services (`app/services/notes/`):** Contains the core logic for note generation and management.
    *   **Generation Service (`generation_service.py`):** Orchestrates the note generation process, from content retrieval to AI processing and note creation.
    *   **Management Service (`management_service.py`):** Handles note storage, retrieval, versioning, and collaborative editing (if implemented).
    *   **Customization Service (`customization_service.py`):** Provides functionality for customizing notes, including formatting, structure modification, and saving updates.
    *   **Adaptation Service (`adaptation_service.py`):** Adapts notes to different learning styles and enhances them for exam preparation.
    *   **AI Integration (`ai_integration/`):** Manages the interaction with Vertex AI.
        *   **Vertex AI Service (`vertex_ai_service.py`):** Handles communication with the Vertex AI API for text generation.
        *   **Prompt Engineering (`prompt_engineering.py`):** Defines strategies for crafting effective prompts to guide the AI model.
    *   **Content Analysis (`content_analysis/`):** Performs analysis on the content to aid in note generation.
        *   **Summarization (`summarization.py`):** Summarizes the input content.
        *   **Structuring (`structuring.py`):** Structures the content logically (e.g., headings, bullet points).
        *   **Supplementary Material Generation (`supplementary.py`):** Generates flashcards, diagrams (using Mermaid syntax), and practice questions.
        *   **Highlighting (`highlighting.py`):** Identifies and highlights important content for exam prep.
    *   **Learning Modes (`learning_modes/`):** Implements adaptation strategies for different learning styles.
        *   **Socratic (`socratic.py`):** Adds questions to encourage active recall.
        *   **Examples (`examples.py`):** Includes relevant examples and analogies.
        *   **Visual (`visual.py`):** Emphasizes visual aids and suggests diagrams.
        *   **Auditory (`auditory.py`):** Structures notes for easy comprehension when read aloud.
*   **Models (`app/models/notes.py`):** Defines the data models for notes and note versions.

## Vertex AI Integration

### Setup and Authentication

1.  **Install the Vertex AI SDK:**
```
bash
    pip install google-cloud-aiplatform
    
```
2.  **Set up Google Cloud Credentials:** Ensure that you have a Google Cloud project with the Vertex AI API enabled.  Authenticate using one of the following methods:

    *   **Application Default Credentials (ADC):** If running on a Google Cloud environment (e.g., Compute Engine, Cloud Run), ADC will likely handle authentication automatically.
    *   **Service Account:** For local development or non-Google Cloud environments, create a service account with the necessary permissions and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of the service account key file:
```
bash
        export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service_account_key.json"
        
```
3.  **Configure Project and Location:** Set the `VERTEX_AI_PROJECT` and `VERTEX_AI_LOCATION` environment variables to your Google Cloud project ID and the region where you want to use Vertex AI (e.g., `us-central1`):
```
bash
    export VERTEX_AI_PROJECT="your-project-id"
    export VERTEX_AI_LOCATION="us-central1"
    
```
### Prompt Engineering

Effective prompt engineering is crucial for generating high-quality notes. The system employs the following strategies (see `app/services/notes/ai_integration/prompt_engineering.py`):

*   **Clear Instructions:** The prompt clearly instructs the AI to generate concise and well-structured notes from the provided content.
*   **Context Provision:** The entire content is included in the prompt, providing the necessary context for note generation.
*   **Style and Tone Guidance:** User preferences for note style (e.g., bullet points, paragraphs) and tone (e.g., formal, informal) are incorporated into the prompt to tailor the output.
*   **Learning Mode Adaptation:** The prompt is modified based on the selected learning mode to guide the AI towards generating notes that are suitable for that mode (e.g., adding questions for Socratic, suggesting diagrams for visual learners).
*   **Focus and Structure:** The prompt emphasizes focusing on the most important information and using appropriate headings and subheadings.

**Example Prompt (from `prompt_engineering.py`):**
```
python
def create_note_prompt(content: str, user_preferences: Optional[Dict] = None, learning_mode: Optional[str] = None) -> str:
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
```
## Note Generation Algorithm

The note generation process involves several steps, as orchestrated by the `generation_service.py`:

1.  **Content Retrieval:** The input content is retrieved from the content management system.  (In the current implementation, this is simulated with placeholder content).
2.  **Prompt Creation:** A prompt is generated using the `prompt_engineering.py` module, incorporating the retrieved content, user preferences, and the selected learning mode.
3.  **AI Processing:** The prompt is sent to Vertex AI via the `vertex_ai_service.py` module. The AI model generates the initial note content.
4.  **Content Analysis and Structuring:**  The generated content undergoes further analysis and structuring (currently simulated in the `content_analysis` modules):
    *   **Summarization (`summarization.py`):** The AI-generated text is summarized to ensure conciseness.
    *   **Structuring (`structuring.py`):** Headings, bullet points, and other structural elements are added based on the content type and user preferences.
    *   **Supplementary Material Generation (`supplementary.py`):**  Based on the learning mode, supplementary materials like flashcards, diagrams (using Mermaid syntax), or practice questions are generated.

        **Diagram Generation:** Diagrams are represented using Mermaid syntax, allowing for rendering on the frontend.  (Currently, example Mermaid diagrams are placeholders).
5.  **Note Creation and Storage:** A `Note` object is created with the processed content, metadata, and user information.  The note is then saved to the database (simulated in the current implementation).
6.  **Supplementary Material Delivery:**  (This step is currently simulated and would ideally be handled asynchronously after note saving). If the learning mode requires supplementary materials, the generated materials are associated with the note and made available to the user.

## Learning Mode Adaptation

The system adapts notes to cater to different learning styles (implemented in the `app/services/notes/learning_modes/` directory):

*   **Socratic Method (`socratic.py`):**  Questions are strategically inserted within the note content to promote active recall and critical thinking. These questions encourage users to engage with the material and reflect on its implications.
*   **Example/Analogy-Based (`examples.py`):**  Relevant examples and analogies are added to illustrate complex concepts, making them more relatable and easier to understand.
*   **Visual Learning (`visual.py`):** Suggestions for diagrams, flowcharts, or other visual representations are included to cater to visual learners.  Alternatively (or additionally), the system could directly embed Mermaid diagrams or provide textual descriptions of visuals.
*   **Auditory Learning (`auditory.py`):**  The note structure is optimized for auditory comprehension.  This involves using clear headings, shorter sentences, and transitional phrases to create a natural flow when reading aloud.
*   **Exam Prep (`adaptation_service.py` and `content_analysis/highlighting.py`):** Notes are enhanced for exam preparation by:

    *   **Highlighting Important Content:** Key concepts and crucial information are highlighted using techniques like keyword extraction or importance scoring.
    *   **Integrating Past Year Questions:**  (If a database of past exam questions is available) Relevant past year questions are integrated into the notes to provide practice and familiarize users with exam formats.

The core adaptation logic resides in the `adaptation_service.py` module, which calls the relevant functions from the learning mode modules and the highlighting module.  User preferences regarding formatting are applied in this module as well.

## API Endpoints

The following API endpoints (defined in `app/api/notes.py`) provide access to the note generation functionality:

*   **`POST /api/notes/generate`:** Generates notes from a specified content ID.  Accepts `content_id`, optional `user_preferences` (JSON object), and `learning_mode` (string) in the request body.  Returns a JSON object with the generated `note_id` and a success message.

    **Example Request:**
```
json
    {
      "content_id": "your_content_id",
      "user_preferences": {
        "style": "bullet points",
        "tone": "formal"
      },
      "learning_mode": "example"
    }
    
```
**Example Response:**
```
json
    {
      "note_id": "generated_note_id",
      "message": "Note generated successfully"
    }
    
```
*   **`GET /api/notes/{note_id}`:** Retrieves a specific note by its ID. Returns a JSON representation of the `Note` object.

    **Example Request:**
```
    GET /api/notes/your_note_id
    
```
**Example Response:** (See `Note` model in `app/models/notes.py` for the full structure)
```
json
    {
      "note_id": "your_note_id",
      "content_id": "source_content_id",
      "user_id": "user_id",
      "title": "Notes for Content X",
      "content": "The generated note content...",
      "version": 1,
      "created_at": "2024-01-26T12:00:00",
      "updated_at": "2024-01-26T12:00:00",
      "format_options": { ... },
      "learning_mode": "example"
    }
    
```
*   **`GET /api/notes/`:** Lists notes for the authenticated user, optionally filtered by `content_id` or `topic_id` (using query parameters). Returns a list of `Note` objects.

    **Example Request (no filters):**
```
    GET /api/notes/
    
```
**Example Request (filter by content):**
```
    GET /api/notes/?content_id=your_content_id
    
```
**Example Response:**
```
json
    [
      { ... Note object 1 ... },
      { ... Note object 2 ... },
      ...
    ]
    
```
*   **`PUT /api/notes/{note_id}`:** Updates the content and/or formatting of a note. Accepts `content` (string) and optional `format_options` (JSON object) in the request body. Returns a JSON object with a success message and the new version number.

    **Example Request:**
```
json
    {
      "content": "Updated note content...",
      "format_options": {
        "font": "Arial",
        "fontSize": 14
      }
    }
    
```
**Example Response:**
```
json
    {
      "message": "Note updated",
      "version": 2
    }
    
```
*   **`GET /api/notes/{note_id}/versions`:** Retrieves all versions of a note.  Returns a list of `NoteVersion` objects.

    **Example Request:**
```
    GET /api/notes/your_note_id/versions
    
```
**Example Response:**
```
json
    [
      {
        "note_id": "your_note_id",
        "version": 1,
        "content": "Original note content...",
        "updated_at": "2024-01-26T12:00:00"
      },
      {
        "note_id": "your_note_id",
        "version": 2,
        "content": "Updated note content...",
        "updated_at": "2024-01-26T12:30:00"
      }
    ]
    
```
*   **`PUT /api/notes/{note_id}/formatting`:** Updates only the formatting options of a note. Accepts a `format_options` (JSON object) in the request body. Returns a JSON object with a success message and the updated format options.

    **Example Request:**
```
json
    {
      "format_options": {
        "font": "Times New Roman"
      }
    }
    
```
**Example Response:**
```
json
    {
      "message": "Formatting updated",
      "format_options": {
        "font": "Times New Roman"
      }
    }
    
```
*   **`PUT /api/notes/{note_id}/restructure`:** Restructures the note content based on a specified `structure_type` (provided as a query parameter, e.g., `bullet_points`, `tables`). Returns a JSON object with a success message and the restructured content.

    **Example Request:**
```
    PUT /api/notes/your_note_id/restructure?structure_type=bullet_points
    
```
**Example Response:**
```
json
    {
      "message": "Content restructured",
      "new_content": "Restructured content in bullet points format..."
    }
    
```
*   **`PUT /api/notes/{note_id}/save`:** Saves the current content of a note. Accepts `content` (string) in the request body. Returns a JSON object with a success message and the saved content.

    **Example Request:**
```
json
    {
      "content": "Final version of the note content..."
    }
    
```
**Example Response:**
```
json
    {
      "message": "Note saved",
      "content": "Final version of the note content..."
    }
    
```
*   **`POST /api/notes/{note_id}/export`:** Exports a note to a specified `format` (provided as a query parameter, e.g., `markdown`, `pdf`). Returns a JSON object with a success message and, potentially, a file content or a download link (depending on the implementation).

    **Example Request:**
```
    POST /api/notes/your_note_id/export?format=markdown
    
```
**Example Response:**
```
json
    {
      "message": "Note exported to markdown",
      "file_content": "# Note Title\n\nNote content in Markdown format..."
    }
    
```
## Integration with Content Management System

The Note Generation System tightly integrates with the EduPulse Content Management System. Users can select any content they have uploaded and request note generation for it. The system retrieves the content using the provided `content_id` (although this is currently simulated) and uses it as the basis for generating notes. The generated notes are then linked to the original content, allowing users to easily access and manage their notes within the context of their study materials.

## Further Development

*   **Real Content Retrieval:** Replace the simulated content retrieval in `generation_service.py` with actual integration with the Content Management System.
*   **Database Integration:** Connect the services to a database (e.g., PostgreSQL, Firestore) to persist notes, note versions, and user preferences.  This will require updating the simulated database interactions throughout the services.
*   **Robust Error Handling:** Implement comprehensive error handling throughout the system, including error handling for API calls, content processing, and database interactions.
*   **Advanced Content Analysis:**  Enhance the content analysis modules with more sophisticated techniques for summarization, structuring, and supplementary material generation. Explore more advanced NLP models and approaches.
*   **Improved Diagram Generation:**  Integrate with a Mermaid rendering service or library to directly embed diagrams in the notes instead of just providing Mermaid syntax.
*   **User Preference Management:** Implement a system to store and manage user preferences (formatting, learning styles) in user profiles.
*   **Collaborative Editing:** (Optional) Add support for collaborative note editing, including conflict resolution and version control mechanisms.
*   **Comment and Annotation Services:** (Optional) Allow users to add comments and annotations to their notes.
*   **Search and Filtering:** Implement robust search and filtering capabilities for notes, allowing users to easily find the notes they need.
*   **Rate Limiting and Quotas:**  Implement rate limiting and quotas for the Vertex AI API to manage usage and costs.
*   **Asynchronous Processing:** For long-running tasks like content processing and supplementary material generation, consider using a task queue (e.g., Celery, Redis Queue) to handle them asynchronously and improve API responsiveness.
*   **Security:**  Implement appropriate security measures, including input validation and sanitization, to prevent vulnerabilities.
*   **Testing:**  Write comprehensive unit and integration tests to ensure the system's functionality and reliability.