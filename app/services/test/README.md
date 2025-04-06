# EduPulse Test Dashboard System

## Overview

The EduPulse Test Dashboard system provides a comprehensive platform for creating, taking, and analyzing tests. It features adaptive testing capabilities, personalized feedback, and tools to help students improve their learning. The system is composed of the following key components:

*   **Question Repository Management:** Allows for the creation, management, and organization of a diverse set of questions.
*   **Test Generation Engine:** Generates tests based on specified topics, difficulty levels, and other criteria, with adaptive algorithms for personalized assessments.
*   **Test-Taking Services:** Manages the process of taking a test, including answer submission, timer management, and progress tracking.
*   **Performance Analytics:** Analyzes test results to provide insights into student performance, identify areas of weakness, and track progress over time.
*   **Adaptive Learning Algorithms:** Uses performance data to adapt future tests, personalize explanations, and recommend study areas.

## System Architecture

The system is structured into services and APIs. Services handle the core logic of each component, while APIs provide endpoints for interacting with the system. The key services and their corresponding APIs are detailed below.

## 1. Question Repository Management

### Purpose

Manages the storage and retrieval of test questions.

### Functionality

*   **CRUD Operations:** Supports creating, reading, updating, and deleting questions.
*   **Question Types:** Handles different question formats:
    *   Theoretical
    *   Numerical
    *   Multiple Choice
    *   Descriptive
*   **Categorization:** Organizes questions by topic and subtopic.
*   **Difficulty Levels:** Classifies questions into Easy, Medium, and Hard.
*   **Metadata:** Allows for tagging questions with additional information (e.g., source, keywords).
*   **Past Year Question Management:** Tracks in which years a question has appeared previously.

### API Endpoints (`app/api/questions.py`)

*   **`POST /questions/`**: Create a new question (Admin only).
    *   **Request Body:** JSON object representing a `Question` (see `app/models/questions.py`).
    *   **Response:** Question ID (string).
    *   **Example Request:**
```
json
        {
          "question_type": "multiple_choice",
          "topic": "Math",
          "difficulty": "medium",
          "text": "What is 2+2?",
          "options": [{"text": "3", "is_correct": false}, {"text": "4", "is_correct": true}]
        }
        
```
*   **Example Response:** `"a1b2c3d4-e5f6-7890-1234-567890abcdef"`

*   **`GET /questions/{question_id}`**: Get a question by ID.
    *   **Response:** `Question` object (JSON).
    *   **Example Response:**
```
json
        {
          "question_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
          "question_type": "multiple_choice",
          "topic": "Math",
          "difficulty": "medium",
          "text": "What is 2+2?",
          "options": [{"text": "3", "is_correct": false}, {"text": "4", "is_correct": true}]
        }
        
```
*   **`PUT /questions/{question_id}`**: Update a question (Admin only).
    *   **Request Body:** JSON object with fields to update.
    *   **Response:** `True` if successful, `False` otherwise.

*   **`DELETE /questions/{question_id}`**: Delete a question (Admin only).
    *   **Response:** `True` if successful, `False` otherwise.

*   **`GET /questions/`**: List questions, optionally filtered by topic, subtopic, or difficulty.
    *   **Query Parameters:** `topic` (string), `subtopic` (string), `difficulty` (string - easy, medium, hard).
    *   **Response:** List of `Question` objects.
    *   **Example Request:** `/questions/?topic=Physics&difficulty=easy`

### Service Logic (`app/services/test/question_service.py`)

Handles database interactions for question CRUD operations.

## 2. Test Generation Engine

### Purpose

Creates tests based on specified criteria.

### Functionality

*   **Adaptive Test Creation:** Adjusts the difficulty and content of tests based on user performance (not yet fully implemented in the provided code).
*   **Difficulty Balancing:** Allows specifying the desired distribution of easy, medium, and hard questions.
*   **Topic Coverage:** Ensures questions cover the specified topic effectively.
*   **Time Estimation:** Provides an estimated time required to complete the test.
*   **Configuration Options:** Allows specifying number of questions and difficulty distribution.

### API Endpoints (`app/api/tests.py`)

*   **`POST /tests/generate`**: Generate a new test.
    *   **Query Parameters:**
        *   `topic` (string, required): Topic of the test.
        *   `num_questions` (integer, default=10, >0): Number of questions in the test.
        *   `easy` (integer, >=0, optional): Number of easy questions.
        *   `medium` (integer, >=0, optional): Number of medium questions.
        *   `hard` (integer, >=0, optional): Number of hard questions.
        *   If `easy`, `medium`, or `hard` are not provided, the test will have an even distribution of difficulties.  If they *are* provided, their sum must equal `num_questions`.
    *   **Response:** Test data (JSON) including test ID, questions (with ID, text, and options for multiple choice), and estimated time.
    *   **Example Request:** `/tests/generate?topic=Math&num_questions=15&easy=5&medium=5&hard=5`
    *   **Example Response:**
```
json
        {
          "test_id": "f1e2d3c4-b5a6-9087-6543-210987fedcba",
          "topic": "Math",
          "questions": [
            {"question_id": "q1", "text": "What is 1+1?", "options": [{"text": "1", "is_correct": false}, {"text": "2", "is_correct": true}]},
            {"question_id": "q2", "text": "Solve for x: 2x = 4", "options": [{"text": "1", "is_correct": false}, {"text": "2", "is_correct": true}]},
            // ... more questions
          ],
          "estimated_time": 900,
          "num_questions": 15
        }
        
```
### Service Logic (`app/services/test/test_generation_service.py`)

*   Fetches questions from the question repository based on the provided criteria.
*   Implements the logic for balancing difficulty and ensuring topic coverage.
*   Estimates the time required to complete the test (currently a simple calculation, could be improved).

## 3. Test Taking Services

### Purpose

Manages the process of a user taking a test.

### Functionality

*   **Answer Submission and Validation:** Records user answers to individual questions, but currently does *not* validate them for correctness in this service (validation would typically occur during result analysis).
*   **Timer Management:** Tracks the elapsed time during the test.
*   **Progress Tracking:** Monitors the user's progress through the test (percentage of questions answered).
*   **Partial Save and Resume:** Allows users to leave a test and return later to continue (implemented using an in-memory `test_sessions` dictionary; a database would be needed for persistent storage).
*   **Response Recording:** Stores user responses for later analysis.

### API Endpoints (`app/api/tests.py`)

*   **`POST /tests/{topic}/start`**: Start a new test session.
    *   **Query Parameters:** Same as `/tests/generate` (topic, num_questions, easy, medium, hard).
    *   **Response:** Test session data (JSON) including test ID, questions, estimated time, and a success message.
    *   **Example Response:**
```
json
        {
          "test_id": "98765432-10fe-dcba-4321-0987654321fe",
          "questions": [
            {"question_id": "q3", "text": "What is the capital of France?", "options": [{"text": "London", "is_correct": false}, {"text": "Paris", "is_correct": true}]},
            // ... more questions
          ],
          "estimated_time": 600,
          "message": "Test started"
        }
        
```
*   **`POST /tests/{test_id}/submit`**: Submit an answer to a question.
    *   **Path Parameter:** `test_id` (string): ID of the test.
    *   **Request Body:** JSON object with `question_id` (string) and `answer` (string).  The `answer` should be the user's response (text for descriptive/theoretical, solution for numerical, selected option for multiple choice).
    *   **Response:** Success message and current test progress (percentage).
    *   **Example Request:**
```
json
        {
          "question_id": "q3",
          "answer": "Paris"
        }
        
```
*   **Example Response:**
```
json
        {
          "message": "Answer submitted",
          "progress": 25
        }
        
```
*   **`POST /tests/{test_id}/finish`**: Finish the test.
    *   **Path Parameter:** `test_id` (string): ID of the test.
    *   **Response:** Success message and a placeholder for results (results calculation not yet implemented).
    *   **Example Response:**
```
json
        {
          "message": "Test finished",
          "results": "(Results will be calculated)"
        }
        
```
*   **`GET /tests/{test_id}/progress`**: Get the current progress of a test.
    *   **Path Parameter:** `test_id` (string): ID of the test.
    *   **Response:** Current progress (percentage) and elapsed time (in seconds).
    *   **Example Response:**
```
json
        {
          "progress": 60,
          "elapsed_time": 720
        }
        
```
*   **`GET /tests/{test_id}/results`**: Get test results (placeholder – returns dummy data).  In a full implementation, this would return detailed results after the test is finished.
    *   **Path Parameter:** `test_id` (string): ID of the test.
    *   **Response:** Test results (score, number of correct/incorrect answers, time taken).
    *   **Example Response:**
```
json
        {
          "score": 85,
          "correct_answers": 17,
          "incorrect_answers": 3,
          "time_taken": 1200
        }
        
```
### Service Logic (`app/services/test/test_taking_service.py`)

*   Manages test sessions using the `TestSession` class.
*   Tracks user answers, progress, and time.
*   Provides functions for starting, submitting answers, finishing, and getting progress of a test.
*   Uses an in-memory dictionary `test_sessions` to store active tests (replace with database in production).

## 4. Performance Analytics

### Purpose

Analyzes test results to provide insights into student performance.

### Functionality

*   **Time-per-Question Analysis:** Calculates the average time spent on each question.
*   **Difficulty Level Assessment:** Evaluates performance across different difficulty levels.
*   **Answer Accuracy Evaluation:** Determines overall and per-question accuracy.
*   **Pattern Recognition in Mistakes:** Identifies common types of errors.
*   **Historical Performance Tracking:** Tracks performance over time.
*   **Data Preparation for Visualization:** Transforms analysis results into a format suitable for frontend charts.

### API Endpoints (`app/api/analytics.py`)

*   **`GET /analytics/tests/{test_id}`**: Get analysis of a specific test.
    *   **Path Parameter:** `test_id` (string): ID of the test.
    *   **Response:** Analysis results (JSON) including accuracy, average time per question, difficulty stats, and mistake patterns.
    *   **Example Response:**
```
json
        {
          "accuracy": 75.0,
          "average_time_per_question": 60.0,
          "difficulty_stats": {
            "EASY": {"correct": 5, "incorrect": 0},
            "MEDIUM": {"correct": 7, "incorrect": 3},
            "HARD": {"correct": 3, "incorrect": 2}
          },
          "mistake_patterns": [{"type": "Conceptual errors in Physics", "count": 2}],
          "overall_feedback": "Good performance, but review areas with conceptual errors."
        }
        
```
*   **`GET /analytics/history`**: Get historical performance data for the user.
    *   **Response:** List of historical test results (JSON), each including test ID, date, score, and accuracy.
    *   **Example Response:**
```
json
        [
          {"test_id": "test1", "date": "2024-01-15", "score": 75, "accuracy": 75.0},
          {"test_id": "test2", "date": "2024-02-20", "score": 82, "accuracy": 82.0}
        ]
        
```
*   **`GET /analytics/dashboard`**: Get data for the analytics dashboard (combines recent and historical data).
    *   **Response:** Data (JSON) formatted for visualization, including overall performance, difficulty breakdown, mistake patterns, and historical performance trend.
    *   **Example Response:**
```
json
        {
          "overall_performance": {
            "accuracy": 80.0,
            "average_time_per_question": 55.0
          },
          "difficulty_breakdown": [
            {"difficulty": "EASY", "correct": 5, "incorrect": 0},
            {"difficulty": "MEDIUM", "correct": 8, "incorrect": 2},
            {"difficulty": "HARD", "correct": 2, "incorrect": 3}
          ],
          "mistake_patterns": [{"type": "Calculation errors", "count": 3}],
          "historical_performance": [
            {"date": "2024-03-01", "accuracy": 70.0},
            {"date": "2024-03-08", "accuracy": 80.0}
          ]
        }
        
```
### Service Logic (`app/services/test/analytics_service.py`)

*   Calculates accuracy and average time per question.
*   Analyzes performance based on difficulty levels and identifies mistake patterns (currently uses placeholder logic, needs improvement).
*   Retrieves historical performance data (currently simulated, needs database integration).
*   Prepares data for frontend visualization.

## 5. Adaptive Learning Algorithms

### Purpose

Personalizes the learning experience by adapting to the user's performance.

### Functionality

*   **Dynamic Difficulty Adjustment:** Suggests adjusting the difficulty of future tests based on past performance.
*   **Spaced Repetition Scheduling:** Schedules review of incorrectly answered questions using a spaced repetition algorithm (not yet fully implemented).
*   **Personalized Explanation Generation:** Provides tailored explanations for incorrect answers (placeholder - needs improvement).
*   **Recommendation Engine for Improvement Areas:** Recommends topics or subtopics for further study based on performance analysis.
*   **Study Focus Suggestions:** Provides specific suggestions for areas to focus on (placeholder).

### API Endpoints (`app/api/adaptive_learning.py`)

*   **`GET /adaptive/difficulty/{topic}`**: Get the suggested difficulty level for the next test in a given topic.
    *   **Path Parameter:** `topic` (string): Topic for which to adjust difficulty.
    *   **Response:** Suggested difficulty level (string - EASY, MEDIUM, or HARD).
    *   **Example Response:** `"HARD"`

*   **`POST /adaptive/repetition`**: Get a list of questions for spaced repetition review (based on previously incorrect answers).
    *   **Request Body:** A list of dictionaries, each with a `question_id`.
    *   **Response:** A list of dictionaries, each with a `question_id` and a `review_in` field indicating when to review the question.
    *   **Example Request:** `[{"question_id": "q5"}, {"question_id": "q7"}]`
    *   **Example Response:** `[{"question_id": "q5", "review_in": "3 days"}, {"question_id": "q7", "review_in": "7 days"}]`

*   **`GET /adaptive/explanation/{question_id}`**: Get a personalized explanation for an incorrectly answered question.
    *   **Path Parameter:** `question_id` (string): ID of the question.
    *   **Query Parameter:** `incorrect_answer` (string): The user's incorrect answer.
    *   **Response:** Personalized explanation (string).
    *   **Example Request:** `/adaptive/explanation/q5?incorrect_answer=incorrectOption`
    *   **Example Response:** `"The correct answer to question q5 is ...  It seems you might have been thinking about ...  Here's a more detailed explanation..."`

*   **`GET /adaptive/recommendations`**: Get personalized study focus recommendations.
    *   **Response:** A list of study recommendations (strings).
    *   **Example Response:** `["Focus on reviewing concepts in Physics related to Mechanics.", "Practice more numerical problems in Calculus."]`

### Service Logic (`app/services/test/adaptive_learning_service.py`)

*   Determines suggested difficulty levels based on historical performance.
*   Manages spaced repetition scheduling for incorrect answers (currently a placeholder).
*   Generates personalized explanations for incorrect answers (currently a placeholder).
*   Recommends study areas based on performance patterns (currently a placeholder).

## Future Improvements

*   **Database Integration:** Replace in-memory storage with a persistent database for questions, test sessions, and user performance data.
*   **Adaptive Testing:** Implement more sophisticated algorithms for dynamically adjusting test difficulty during test generation.
*   **Question Validation:** Implement answer validation logic during test-taking.
*   **Result Calculation:** Implement detailed test result calculation, including correctness and performance metrics per question.
*   **Improved Analytics:** Enhance analytics algorithms for more accurate pattern recognition and personalized feedback.
*   **Personalized Explanations:** Integrate with an LLM or a knowledge base to provide more detailed and tailored explanations for incorrect answers.
*   **Spaced Repetition:** Implement a robust spaced repetition algorithm (e.g., SM-2) for scheduling review of incorrect answers.
*   **User Interface:** Develop a user-friendly interface for interacting with the Test Dashboard system.
*   **Security:** Implement proper authentication and authorization mechanisms.

## Conclusion

The EduPulse Test Dashboard system provides a solid foundation for adaptive and personalized assessment. The current implementation includes core functionalities for question management, test generation, test-taking, performance analysis, and adaptive learning. Further development, particularly in areas like database integration and improved algorithms, will enhance the system's capabilities and provide a richer learning experience for students.