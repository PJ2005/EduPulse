# Content Management API

This module defines the API endpoints for managing learning content within the EduPulse Learning Dashboard.

## General Description

This API provides functionality for users to upload, process, organize, and retrieve their learning materials. It supports various file formats, including PDFs, images, audio recordings, presentations, and videos. Uploaded content is processed to extract relevant information (e.g., text from PDFs or images, transcriptions from audio/video), and users can then organize their content into folders, add tags, and track their reading progress.

## File Upload

*   `POST /api/content/upload`: Uploads a file to the user's content library.

    **Supported File Formats:**  PDF, JPEG, PNG, GIF, MP3, WAV, PPT, PPTX, MP4, MOV. See `app/services/content/upload_service.py` for the most up-to-date list and validation.

    **File Size Limit:** 100MB (configurable in `app/services/content/upload_service.py`).

    **Data Flow:** Frontend sends file -> API endpoint calls `upload_service.upload_file` -> Service validates file, uploads to cloud storage (simulated for now), extracts metadata, saves content information to the database (simulated for now) -> Returns content ID and metadata.

    **Example Request:**
```
    POST /api/content/upload
    Headers:
      Authorization: Bearer <JWT_TOKEN>
    Body (form-data):
      file: <file_to_upload>
    
```
**Example Response:**
```
json
    {
      "content_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
      "message": "File uploaded successfully",
      "metadata": {
        "pages": 10,
        "author": "John Doe"
      }
    }
    
```
## Content Processing

*   `POST /api/content/{content_id}/process`: Triggers the processing pipeline for the uploaded content. Processing happens asynchronously in the background.

    **Data Flow:** Frontend requests processing -> API endpoint calls `processing_service.process_content` (as a background task) -> Service determines file type and calls the appropriate processor in `app/services/content/file_processing/` -> Processor extracts content (text, etc.) -> Service updates content information in the database (simulated for now) with processed data.

*   `GET /api/content/{content_id}/status`: Retrieves the processing status of a content item.

    **Data Flow:** Frontend requests status -> API endpoint calls `processing_service.get_processing_status` -> Service retrieves status (simulated for now) -> Returns status information.

    **Example Request:**
```
    GET /api/content/a1b2c3d4-e5f6-7890-1234-567890abcdef/status
    Headers:
      Authorization: Bearer <JWT_TOKEN>
    
```
**Example Response:**