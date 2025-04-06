# EduPulse Scheduler Dashboard - Service Documentation

## Overview

The EduPulse Scheduler Dashboard provides a comprehensive system for managing and optimizing study schedules. It integrates calendar management, task prioritization, break scheduling, AI-powered planning, and a study plan generation tool to help users effectively allocate their time and achieve their learning goals.

## Architecture

The Scheduler Dashboard consists of the following key components:

*   **Calendar Management:** Handles the creation, retrieval, updating, and deletion of tasks and events within a user's calendar.
*   **Task Management:** Focuses on task-related operations, including priority calculation, status tracking, postponement, redistribution, and deadline management.
*   **Break Management:** Implements break scheduling, including the Pomodoro technique, and provides break reminders.
*   **AI-Powered Planning Services:** Uses AI, including LLMs, to analyze tasks, balance workloads, and recommend schedule adjustments.
*   **Study Planner:** Generates customized study plans tailored to individual users, considering their exams, syllabus, performance, and other factors.

## Component Details

### 1. Calendar Management

This component manages the user's calendar, allowing them to organize their time effectively.

*   **Functionality:**
    *   **Task and Event Management:** Creates, retrieves, updates, and deletes tasks and events.  Each task has a title, description, subject, topic, status (pending, in-progress, completed), priority, deadline, estimated time, and recurrence rules. Events have a title, description, start time, and end time.
    *   **Calendar View Preparation:** Prepares calendar data for display, organizing tasks and events by date.
    *   **Date-Based Filtering:** Enables users to view their schedule for specific dates.
    *   **Recurring Task Support:** Allows tasks to be set up with recurrence rules (e.g., weekly, monthly), using the iCalendar RRULE format.

*   **Key Algorithms/Techniques:**
    *   Date and time handling using Python's `datetime` module.
    *   Data modeling with Pydantic for data validation and serialization.

### 2. Task Management

This component provides functionalities for managing individual tasks and their properties.

*   **Functionality:**
    *   **Priority Calculation:** Calculates task priority based on factors like deadline proximity, estimated time, and subject importance.  (The current implementation uses a basic algorithm; this is an area for significant improvement with AI).
    *   **Task Categorization:** Allows tasks to be categorized by subject and topic for better organization.
    *   **Status Tracking:** Tracks task status (pending, in-progress, completed).
    *   **Postponement:** Allows users to postpone tasks by changing their deadlines.
    *   **Task Redistribution:** (Placeholder) Aims to redistribute tasks from a specific day to other days.  The current implementation is a placeholder and requires a more sophisticated scheduling algorithm.
    *   **Deadline Management:** Helps users keep track of task deadlines.

*   **Key Algorithms/Techniques:**
    *   Priority calculation algorithm (currently rule-based, can be enhanced with ML).
    *   Status tracking using an Enum for predefined states.

### 3. Break Management

This component focuses on break scheduling and helps users incorporate breaks into their study sessions.

*   **Functionality:**
    *   **Pomodoro Technique:** Implements the Pomodoro Technique (25 minutes of work followed by a short break). The work and break durations are configurable.
    *   **Break Scheduling Algorithms:** (To be implemented)  Future functionality to schedule breaks intelligently based on task duration, complexity, user work patterns, and time of day.
    *   **Long and Short Break Allocation:** Supports both short breaks (e.g., 5 minutes after a Pomodoro) and longer breaks.
    *   **Break Reminders:** (To be implemented)  Will provide reminders for breaks, potentially integrating with a notification system.
    *   **Break Compliance Tracking:** (To be implemented)  Will track break-taking behavior to monitor adherence to schedules and potentially provide feedback or adjust schedules.

*   **Key Algorithms/Techniques:**
    *   Timer management using `datetime` and `timedelta`.
    *   State management to track active work/break periods (currently using an in-memory dictionary, should be replaced with a database for persistence).

### 4. AI-Powered Planning Services

This component leverages AI to provide intelligent planning assistance.

*   **Functionality:**
    *   **LLM-Powered Task Analysis:** (Placeholder)  Uses an LLM (Large Language Model) to analyze task descriptions and extract information such as estimated time, complexity, suggested priority, and relevant topics.  The current implementation simulates an LLM call; a real implementation would integrate with an LLM API (e.g., Vertex AI).
    *   **Workload Balancing:** (Placeholder)  Balances the workload across available time slots, considering task complexity, estimated time, user performance patterns, and energy level predictions (if available). The current implementation provides a very basic even distribution; this is a key area for AI-driven optimization.
    *   **Schedule Adjustment Recommendations:** (Placeholder)  Analyzes the current schedule and recommends adjustments to improve efficiency, considering factors like task grouping, user preferences, and potential overloads.  Could use an LLM to generate human-readable and personalized recommendations.

*   **Key Algorithms/Techniques:**
    *   Integration with LLM APIs (to be implemented).
    *   Optimization algorithms for workload balancing (to be implemented, could involve constraint satisfaction, heuristic search, or other techniques).
    *   Analysis of user performance data (integration with the analytics service).

### 5. Study Planner

This component helps users create and manage customized study plans.

*   **Functionality:**
    *   **Study Plan Generation:** Generates customized study plans based on:
        *   Exam date.
        *   Syllabus (list of topics).
        *   User's past performance (integration with the analytics service).
        *   Topic priority based on past year questions (integration with the test system).
    *   **Plan Adjustment:** Allows users to adjust existing study plans (e.g., reschedule sessions, change topic allocations).
    *   **Progress Tracking:** Tracks progress against a study plan, including completed sessions, topics covered, and upcoming sessions.
    *   **Plan Visualization:** Prepares data for visualizing the study plan and progress (e.g., timeline of sessions, progress bars).

*   **Key Algorithms/Techniques:**
    *   Prioritization of topics based on multiple factors (syllabus importance, past year question frequency, user performance).
    *   Time allocation algorithms to distribute study sessions across the available time.
    *   Data transformation for frontend visualization.

## API Endpoints

The following API endpoints are available for interacting with the Scheduler Dashboard:

### Calendar Management (`app/api/calendar.py`)

*   `POST /calendar/tasks/`: Create a new task.
    *   Example Request:
```
json
        {
          "title": "Study Calculus",
          "subject": "Math",
          "topic": "Integration",
          "deadline": "2024-12-31",
          "estimated_time": 3600,  // in seconds
          "recurring": false
        }
        
```
*   Example Response: `"task_id_123"` (string - the ID of the created task)
*   `GET /calendar/tasks/{task_id}`: Get a task by ID.
    *   Example Response:
```
json
        {
          "task_id": "task_id_123",
          "title": "Study Calculus",
          "subject": "Math",
          "topic": "Integration",
          "status": "pending",
          "priority": 5,
          "deadline": "2024-12-31",
          "estimated_time": 3600,
          "recurring": false,
          "recurrence_rule": null,
          "user_id": "user_id_456"
        }
        
```
*   `PUT /calendar/tasks/{task_id}`: Update a task.
    *   Example Request (to update the title):
```
json
        {
          "title": "Study Advanced Calculus"
        }
        
```
*   Example Response: `true` (boolean - indicates success)
*   `DELETE /calendar/tasks/{task_id}`: Delete a task.
    *   Example Response: `true`
*   `POST /calendar/events/`: Create a new event.
    *   Example Request:
```
json
        {
          "title": "Math Tutoring Session",
          "start_time": "2024-10-27T14:00:00",
          "end_time": "2024-10-27T15:00:00"
        }
        
```
*   Example Response: `"event_id_789"`
*   `GET /calendar/events/{event_id}`: Get an event by ID.
    *   Example Response:  (Similar structure to create event request, but with event_id)
*   `PUT /calendar/events/{event_id}`: Update an event.
    *   Example Response: `true`
*   `DELETE /calendar/events/{event_id}`: Delete an event.
    *   Example Response: `true`
*   `GET /calendar/view/{date_str}`: Get the calendar view for a specific date (YYYY-MM-DD).
    *   Example Request: `/calendar/view/2024-10-27`
    *   Example Response:
```
json
        {
          "date": "2024-10-27",
          "events": [
            {
              "event_id": "event_id_789",
              "title": "Math Tutoring Session",
              "start_time": "2024-10-27T14:00:00",
              "end_time": "2024-10-27T15:00:00",
              "description": null,
              "user_id": "user_id_456"
            }
          ],
          "tasks": [
            {
                "task_id": "task_id_123",
                "title": "Study Calculus",
                "description": null,
                "subject": "Math",
                "topic": "Integration",
                "status": "pending",
                "priority": 5,
                "deadline": "2024-10-27",
                "estimated_time": null,
                "recurring": false,
                "recurrence_rule": null,
                "user_id": "user_id_456"
            }
          ]
        }
        
```
### Task Management (`app/api/tasks.py`)

*   `PUT /tasks/{task_id}/status/{status}`: Update the status of a task.
    *   Example Request: `/tasks/task_id_123/status/in_progress`
    *   Example Response: `true`
*   `PUT /tasks/{task_id}/postpone/{new_deadline_str}`: Postpone a task to a new deadline (YYYY-MM-DD).
    *   Example Request: `/tasks/task_id_123/postpone/2024-11-15`
    *   Example Response: `true`
*   `POST /tasks/redistribute/{day_str}`: Redistribute tasks for a specific day (YYYY-MM-DD).
    *   Example Request: `/tasks/redistribute/2024-10-28`
    *   Example Response: (Currently returns an empty list; a real implementation would return the redistributed tasks).

### Break Management (`app/api/breaks.py`)

*   `POST /breaks/pomodoro/start`: Start a Pomodoro timer.
    *   Example Response:
```
json
        {
          "message": "Pomodoro started",
          "work_duration": 1500.0,  // seconds (25 minutes)
          "end_time": "2024-10-27T10:25:00"
        }
        
```
*   `GET /breaks/status`: Check the current break status.
    *   Example Responses:
        *   Work in progress:
```
json
            {
              "status": "work",
              "remaining": 600.0  // seconds remaining
            }
            
```
*   Short break:
```
json
            {
              "status": "short_break",
              "remaining": 200.0
            }
            
```
*   Idle:
```
json
            {
              "status": "idle"
            }
            
```
*   Break over:
```
json
            {
              "status": "break_over"
            }
            
```
*   `POST /breaks/pomodoro/stop`: Stop the current Pomodoro timer or break.
    *   Example Response:
```
json
        {
          "message": "Pomodoro stopped"
        }
        
```
### AI Planning (`app/api/ai_planning.py`)

*   `POST /ai_planning/analyze_task`: Analyze a task description using an LLM.
    *   Example Request:
```
json
        {
          "task_description": "Complete the integration exercises in Chapter 5 of the Calculus textbook."
        }
        
```
*   Example Response (simulated):
```
json
        {
          "estimated_time": 5400.0,  // seconds (1.5 hours)
          "complexity": "medium",
          "suggested_priority": 5,
          "topics": ["Calculus", "Integration"]
        }
        
```
*   `POST /ai_planning/balance_workload`: Balance workload across available time.
    *   Example Request:
```
json
        {
          "tasks": [
            {"task_id": "task_1", "title": "Task A"},
            {"task_id": "task_2", "title": "Task B"}
          ],
          "available_time": {
            "2024-10-28": 28800,  // seconds (8 hours)
            "2024-10-29": 18000   // seconds (5 hours)
          }
        }
        
```
*   Example Response:
```
json
        {
          "2024-10-28": [
            {"task_id": "task_1", "title": "Task A"}
          ],
          "2024-10-29": [
            {"task_id": "task_2", "title": "Task B"}
          ]
        }
        
```
*   `POST /ai_planning/recommend_adjustments`: Recommend schedule adjustments.
    *   Example Request:
```
json
        {
          "current_schedule": {
            "2024-10-28": [
              {"task_id": "task_1", "title": "Task A", "estimated_time": 7200},
              {"task_id": "task_2", "title": "Task B", "estimated_time": 10800}
            ],
            "2024-10-29": [
              {"task_id": "task_3", "title": "Task C", "estimated_time": 14400}
            ]
          }
        }
        
```
*   Example Response (simulated):
```
json
        [
          "Consider moving shorter tasks to the morning when you have more energy.",
          "Break down the larger 'Project X' task into smaller subtasks.",
          "Schedule a review session for Calculus topics before the Integration task."
        ]
        
```
### Study Planner (`app/api/study_planner.py`)

*   `POST /study_planner/generate`: Generate a study plan.
    *   Example Request:
```
json
        {
          "exam_date_str": "2025-05-15",
          "syllabus": ["Calculus", "Linear Algebra", "Differential Equations", "Probability"],
          "title": "Math Exam Prep",
          "description": "Comprehensive study plan for the upcoming math exam."
        }
        
```
*   Example Response: (A JSON representation of the generated study plan, including daily allocations of topics/tasks)
*   `PUT /study_planner/{plan_id}`: Adjust an existing study plan.
    *   Example Request (to update description):
```
json
        {
          "adjustments": {
            "new_description": "Updated plan focusing on problem-solving."
          }
        }
        
```
*   Example Response: (The updated study plan).
*   `GET /study_planner/{plan_id}/progress`: Get study plan progress.
    *   Example Response:
```
json
        {
          "percentage_completed": 30,
          "topics_covered": ["Calculus", "Linear Algebra"],
          "topics_remaining": ["Differential Equations", "Probability"],
          "upcoming_sessions": [
            {
              "date": "2024-10-28",
              "topic": "Differential Equations",
              "duration": 14400  // seconds (4 hours)
            }
          ]
        }
        
```
*   `GET /study_planner/{plan_id}/visualization`: Get data for visualizing a study plan.
    *   Example Response:  (Data formatted for a frontend charting library, including a timeline of sessions, progress indicators, etc.)

## Intelligent and Adaptive Planning

The EduPulse Scheduler Dashboard offers intelligent and adaptive planning through several mechanisms:

*   **AI-Powered Task Prioritization:** The system can leverage LLMs (in the future) to analyze task descriptions and provide more accurate priority assessments, going beyond simple rule-based calculations.
*   **Dynamic Workload Balancing:**  AI algorithms (to be implemented) can distribute tasks across available time, taking into account factors such as task complexity, user energy levels (if tracked), and deadlines.
*   **Personalized Schedule Adjustments:** The system (in the future) can provide recommendations for optimizing schedules based on user performance patterns and preferences, potentially using LLMs to generate tailored suggestions.
*   **Adaptive Study Plans:** The Study Planner generates personalized plans that consider a user's exam timeframe, syllabus, past performance, and the importance of topics (e.g., based on past exam questions). These plans can be adjusted based on ongoing progress.
*   **Integration with Other Components:** The scheduler integrates with other parts of the EduPulse application:
    *   **Test Dashboard:** Uses data about past year questions and user performance on tests to prioritize topics in study plans and potentially adjust schedules.
    *   **Analytics:** Accesses user performance data to inform task prioritization, workload balancing, and study plan generation.

## Future Improvements

*   **LLM Integration:** Integrate with an LLM API (like Vertex AI) for more sophisticated task analysis and schedule recommendations.
*   **Advanced Scheduling Algorithms:** Implement more robust algorithms for workload balancing and task redistribution, considering a wider range of factors.
*   **User Energy Level Tracking:**  Potentially integrate with user activity data or other sources to estimate user energy levels and optimize schedules accordingly.
*   **Improved Break Scheduling:** Develop more intelligent break scheduling algorithms.
*   **Notification System:** Implement a notification system for break reminders and other schedule-related alerts.
*   **Database Persistence:** Replace in-memory data storage (for breaks and potentially other components) with a persistent database.

## Getting Started

To run the Scheduler Dashboard services:

1.  Ensure you have the required dependencies installed (e.g., FastAPI).
2.  **(To be implemented) Configure any necessary API keys (e.g., for the LLM integration).**
3.  **(To be implemented) Set up the database connection.**
4.  Run the FastAPI application (e.g., using uvicorn).