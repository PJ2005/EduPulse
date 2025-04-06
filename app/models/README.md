# EduPulse Database Schema

This document provides a detailed overview of the EduPulse database schema, which is designed for Firebase and follows a document-oriented approach.

## Models

### Users

*   **Purpose:** Stores user profile information, authentication details, preferences, and educational background.
*   **Fields:**
    *   `user_id` (string, PK, index): Unique identifier for the user (matches Firebase Auth UID).
    *   `profile` (object):
        *   `first_name` (string)
        *   `last_name` (string)
        *   `email` (string, unique, index)
        *   `photo_url` (string, optional): Profile picture URL
        *   `created_at` (timestamp): When the user account was created
        *   `updated_at` (timestamp): When the user profile was last updated
        *   ...other profile fields...
    *   `auth` (object):  # Additional auth info supplementing Firebase Auth
        *   `provider` (string): Auth provider (e.g., "google.com", "password")
        *   `email_verified` (boolean): Whether the user's email is verified
        *   `last_login` (timestamp): Last login timestamp
        *   `disabled` (boolean): Whether the user account is disabled
    *   `preferences` (object):
        *   `note_formatting` (object)
        *   `learning_styles` (array of strings)
        *   ...other preferences...
    *   `education` (object):
        *   `level` (string)
        *   `subject_interests` (array of strings)

### Content

*   **Purpose:** Manages uploaded learning materials, processed notes, and related metadata.
*   **Fields:**
    *   `content_id` (string, PK, index): Unique identifier for the content.
    *   `user_id` (string, FK to Users, index):  ID of the user who uploaded the content.
    *   `original_upload` (object):
        *   `file_name` (string)
        *   `file_type` (string)
        *   `gcs_path` (string): Path to the file in Google Cloud Storage.
        *   ...other metadata...
    *   `processed_notes` (array of objects):
        *   `note_id` (string, unique within content)
        *   `text` (string)
        *   `topic_id` (string, FK to Topics, index)
        *   `version` (integer)
        *   ...other note fields...
    *   `yet_to_read` (boolean, default: true)
    *   `created_at` (timestamp)
    *   `updated_at` (timestamp)

### Topics

*   **Purpose:** Organizes learning content into a hierarchical structure of subjects, topics, and subtopics.
*   **Fields:**
    *   `topic_id` (string, PK, index): Unique identifier for the topic.
    *   `name` (string, index)
    *   `parent_topic_id` (string, FK to Topics, index, optional): ID of the parent topic (for hierarchical structure).
    *   `subject` (string, index)
    *   `difficulty` (integer): 1-5 scale.
    *   `priority` (integer): 1-5 scale.
    *   `time_estimate` (integer): Estimated time in minutes.
    *   ...other topic fields...

### Tests

*   **Purpose:** Contains a repository of test questions with varying formats and difficulty levels.
*   **Fields:**
    *   `question_id` (string, PK, index): Unique identifier for the question.
    *   `topic_id` (string, FK to Topics, index): ID of the topic the question belongs to.
    *   `question_format` (string): e.g., `multiple_choice`, `short_answer`, `true_false`.
    *   `question_text` (string)
    *   `answer` (object): Structure depends on `question_format`.
    *   `difficulty` (integer): 1-5 scale.
    *   `past_year` (boolean, default: false)
    *   ...other question fields...

### UserTests

*   **Purpose:** Stores user-specific test attempts, responses, and results.
*   **Fields:**
    *   `user_id` (string, PK, FK to Users, index): ID of the user who took the test.
    *   `test_id` (string, PK, FK to Tests, index):  ID of the test taken.
    *   `responses` (array of objects):
        *   `question_id` (string, FK to Tests.question_id)
        *   `answer` (object): User's answer.
        *   `correct` (boolean)
        *   ...other response data...
    *   `score` (float)
    *   `time_taken` (integer): In seconds.
    *   `completed_at` (timestamp)
    *   ...other test attempt data...

### PerformanceMetrics

*   **Purpose:** Tracks user progress, test scores, time spent learning, and other performance-related data.
*   **Fields:**
    *   `user_id` (string, PK, FK to Users, index): ID of the user.
    *   `test_results` (array of objects):
        *   `test_id` (string, FK to Tests, index)
        *   `score` (float)
        *   ...other test result data...
    *   `learning_progress` (object):  # Structure to track progress through topics/content
        *   ...
    *   `time_tracking` (array of objects):
        *   `activity` (string): e.g., `studying`, `testing`
        *   `topic_id` (string, FK to Topics, index, optional)
        *   `time_spent` (integer): In seconds.
        *   ...other time tracking data...
    *   `difficulty_handling` (object):  # Analysis of performance vs. difficulty
        *   ...
    *   ...other metrics...

## Relationships

The database entities have the following relationships:

*   **Users** have a one-to-many relationship with **Content**: Each user can upload and manage multiple content items. This is represented by the `user_id` field in the `Content` collection, which references the `user_id` in the `Users` collection.
*   **Users** have a one-to-many relationship with **UserTests**: Each user can take multiple tests, and their attempts/results are stored in the `UserTests` collection. The `UserTests` collection has a composite primary key consisting of `user_id` (referencing `Users`) and `test_id` (referencing `Tests`).
*   **Users** have a one-to-one relationship with **PerformanceMetrics**: Each user has a corresponding entry in the `PerformanceMetrics` collection to track their overall learning progress. The `PerformanceMetrics` collection uses the `user_id` (referencing `Users`) as its primary key.
*   **Content** has a many-to-many relationship with **Topics** through **processed_notes**: Each content item can have multiple processed notes, and each note can be associated with a specific topic. This is represented within the `Content` documents by the `processed_notes` array, where each note object contains a `topic_id` that references the `Topics` collection.
*   **Topics** can have a hierarchical relationship with themselves: Topics can be organized into subjects, topics, and subtopics. This is achieved through the optional `parent_topic_id` field in the `Topics` collection, which references another `topic_id` within the same collection.
*   **Topics** have a one-to-many relationship with **Tests**: Each topic can have multiple test questions associated with it. The `Tests` collection includes a `topic_id` field that references the `Topics` collection.
*   **Tests** have a many-to-many relationship with **Users** through **UserTests** as described above.

## Indexing Strategy

(To be completed with details on indexed fields)

## Query Optimization

(To be completed with considerations for efficient data retrieval)

(To be completed with a strategy for handling schema changes)

## Indexing Strategy

To optimize query performance, the following fields are indexed in the EduPulse database:

*   **Users:**
    *   `user_id` (Primary Key):  For fast lookups of individual users.
    *   `email` (Unique): For efficient user retrieval by email (e.g., during login).

*   **Content:**
    *   `content_id` (Primary Key): For fast lookups of individual content items.
    *   `user_id` (Foreign Key): To efficiently retrieve content associated with a specific user.

*   **Topics:**
    *   `topic_id` (Primary Key): For fast lookups of individual topics.
    *   `name`: To allow efficient searching or filtering of topics by name.
    *   `parent_topic_id` (Foreign Key): To enable efficient retrieval of hierarchical topic structures.
    *   `subject`: To allow efficient filtering of topics by subject.

*   **Tests:**
    *   `question_id` (Primary Key): For fast lookups of individual questions.
    *   `topic_id` (Foreign Key): To efficiently retrieve questions related to a specific topic.

*   **UserTests:**
    *   `user_id` (Composite Primary Key and Foreign Key):  As part of the composite key, it allows efficient retrieval of all test results for a user.  Also used to efficiently retrieve test results for a specific user.
    *   `test_id` (Composite Primary Key and Foreign Key): As part of the composite key, it allows efficient retrieval of results for a specific test.  Also used to efficiently retrieve results for a specific test.

*   **PerformanceMetrics:**
    *   `user_id` (Primary Key and Foreign Key): To efficiently retrieve performance metrics for a specific user.

These indexing choices are based on the expected query patterns of the application, prioritizing efficient retrieval of data based on user, content, topic, and test relationships.

## Schema Evolution

Since Firebase is a schema-less NoSQL database, we handle schema evolution at the application level. Our strategy focuses on maintaining backward compatibility and providing mechanisms for data migration when necessary.

*   **Backward Compatibility:** When introducing changes to the data model, we strive to maintain backward compatibility whenever possible. This means ensuring that existing code can still read and interpret data even with the new schema. For example, when adding a new field, we can set a default value for existing documents or handle the absence of the field gracefully in the code.

*   **Versioning:** For significant schema changes that are difficult to handle with backward compatibility alone, we can consider a versioning approach. This might involve adding a version field to documents and adapting the application code to handle different schema versions. However, we will aim to minimize the need for versioning due to its complexity.

*   **Data Migration:** When schema changes require modifications to existing data, we will implement data migration strategies. This might involve:
    *   **Background Tasks:** Using background tasks or scripts to update documents in batches, adding new fields, transforming data, or restructuring documents.
    *   **Asynchronous Updates:** For non-critical data, we might use asynchronous updates, modifying data as it is accessed or used by the application.
    *   **Data Transformation Layer:** Introducing a data transformation layer in the application to map between different schema versions, allowing for a gradual transition.

*   **Testing:** Thoroughly test any schema changes and data migration procedures to ensure data integrity and application functionality.

*   **Documentation:**  Maintain clear documentation of all schema changes, including the rationale, the steps taken, and any implications for the application code.

Our approach to schema evolution will be cautious and incremental, prioritizing backward compatibility and minimizing disruptions to the application and its users. We will carefully evaluate the need for each schema change and choose the most appropriate migration strategy based on the scope and impact of the change.