# Home Page Services

    This directory contains the service implementations for the EduPulse Home Page features.

    ## Reminder Service (`reminder_service.py`)

    Provides functionality for managing reminders, including:

    *   `get_topics_to_read(user_id)`: Retrieves a list of reminders for the user, ordered by priority and due date.  (Currently returns sample data).
    *   `calculate_priority(reminder)`:  Calculates the priority of a reminder based on its due date and other factors. (Currently a placeholder implementation).
    *   `update_reminder_status(reminder_id, status)`: Updates the status of a reminder (e.g., "completed", "snoozed"). (Currently a placeholder).
    *   `get_notification_preferences(user_id)`: Retrieves the user's notification preferences for reminders. (Currently returns placeholder data).
    *   `update_notification_preferences(user_id, preferences)`: Updates the user's notification preferences. (Currently a placeholder).

    ## To-Do Service (`todo_service.py`)

    Provides functionality for managing daily to-do lists:

    *   `create_todo_item(user_id, task, due_date, priority)`: Creates a new to-do item. (Currently a placeholder).
    *   `get_todo_items(user_id, for_date=today)`: Retrieves to-do items for a specific date (defaults to today). (Currently returns sample data).
    *   `update_todo_item(item_id, **kwargs)`: Updates the details of a to-do item. (Currently a placeholder).
    *   `delete_todo_item(item_id)`: Deletes a to-do item. (Currently a placeholder).

    ## Subject Service (`subject_service.py`)

    Provides functionality for retrieving subject and topic information:

    *   `get_subject_hierarchy(user_id)`: Retrieves the hierarchical structure of subjects and topics for the user. (Currently returns placeholder data).
    *   `get_subject_progress(user_id, subject_id)`: Retrieves progress tracking data for a specific subject. (Currently returns placeholder data).
    *   `get_recent_activity(user_id, limit=5)`: Retrieves a summary of recent learning activities. (Currently returns placeholder data).

    ## Spotify Service (`spotify_service.py`)

    Provides (mock) integration with the Spotify API:

    *   `get_spotify_oauth()`: Returns a `SpotifyOAuth` object for authentication (using environment variables for credentials).
    *   `authenticate_spotify(auth_code)`: Handles authentication with Spotify and retrieves an access token. (Currently returns a mock token).
    *   `get_music_preferences(user_id)`: Retrieves the user's music preferences. (Currently returns placeholder data).
    *   `update_music_preferences(user_id, preferences)`: Updates the user's music preferences. (Currently a placeholder).
    *   `get_study_playlist(user_id, activity)`: Recommends a playlist based on the study activity (e.g., "reading", "coding"). (Currently returns mock playlist data).
    *   `control_playback(user_id, action)`: Controls Spotify playback (e.g., "play", "pause"). (Currently a placeholder).

    **Note:** The Spotify integration is a mock implementation. To enable full functionality, you would need to:

    1.  Install the `spotipy` library:  `pip install spotipy`
    2.  Replace the mock implementation in `spotify_service.py` with actual Spotify API calls using the `spotipy` library.
    3.  Set the required environment variables: `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, and `SPOTIPY_REDIRECT_URI`. You can obtain these values by creating a Spotify Developer application.

    ## Data Flow

    (Since the API endpoints are not fully defined, a detailed data flow diagram is not possible. However, the general data flow for each feature is described in the service documentation above.)

    ## Algorithm Explanations

    *   **Reminder Priority Calculation:** The `calculate_priority` function in `reminder_service.py` currently uses a simple algorithm based on the due date of the reminder.  Reminders with closer due dates have higher priorities.  A more sophisticated algorithm could incorporate factors such as:
        *   User-defined importance for the topic.
        *   The subject the topic belongs to (e.g., prioritize topics in subjects with upcoming exams).
        *   User's past performance in the subject/topic.
        *   Time required to complete the reading.

    ## Required Environment Variables

    The Spotify integration (when fully implemented) requires the following environment variables:

    *   `SPOTIPY_CLIENT_ID`: Your Spotify application's client ID.
    *   `SPOTIPY_CLIENT_SECRET`: Your Spotify application's client secret.
    *   `SPOTIPY_REDIRECT_URI`: The redirect URI for your Spotify application.  This should match the URI configured in your Spotify Developer dashboard.

    ## Relationship to Database Schema

    The services in this directory interact with the database to store and retrieve data.  The specific database schema is not defined here, but the services assume the existence of collections or tables for:

    *   **Reminders:**  To store reminder information (user ID, topic ID, title, description, due date, priority, status).
    *   **Todos:** To store to-do items (user ID, task, due date, completed status, priority).
    *   **Subjects:** To store the hierarchical structure of subjects and topics for each user.
    *   **Progress:** To track user progress within subjects and topics.
    *   **ActivityLog:** To log recent learning activities (subject, topic, activity type, timestamp).
    *   **(Potentially) Spotify:** To store Spotify access tokens (encrypted) and potentially user's music preferences.
