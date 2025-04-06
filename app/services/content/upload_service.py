from fastapi import UploadFile, HTTPException, status
from typing import Dict
import os
import uuid
from app.models.content import Content, FileUpload
# Assuming database client 'db' and cloud storage client 'storage_client' are available
#  Also assuming 'extract_metadata' function exists and a function to check if file type is allowed

ALLOWED_FILE_TYPES = [
    "application/pdf",
    "image/jpeg", "image/png", "image/gif",
    "audio/mpeg", "audio/wav",
    "application/vnd.ms-powerpoint", "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "video/mp4", "video/quicktime"
]

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

async def upload_file(user_id: str, file: UploadFile) -> Dict:
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid file type: {file.content_type}")
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")

    file_extension = file.filename.split(".")[-1] if "." in file.filename else "unknown"
    file_uuid = str(uuid.uuid4())
    file_name = f"{file_uuid}.{file_extension}"
    # In a real application, use a more robust path construction and ensure the directory exists
    upload_dir = "uploads"
    file_path = os.path.join(upload_dir, user_id, file_name)  # Example local path
    gcs_path = f"uploads/{user_id}/{file_name}"  # Example path for Google Cloud Storage

    try:
        #  Create directory if it doesn't exist - for local storage simulation
        os.makedirs(os.path.join(upload_dir, user_id), exist_ok=True)

        # Save to local storage (for simulation - replace with cloud storage in real app)
        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        print(f"Simulating saving to local storage at: {file_path}")

        # In a real application, upload to cloud storage:
        # await storage_client.upload_fileobj(file.file, bucket="your-bucket-name", blob_name=gcs_path)
        # print(f"Uploaded to cloud storage: {gcs_path}")

        file_upload = FileUpload(file_name=file_name, file_type=file.content_type, file_size=file.size)
        content = Content(user_id=user_id, original_upload=file_upload)

        # Extract metadata
        content.metadata = await extract_metadata(file_path, file_extension)  # Pass file_path
        print(f"Extracted metadata: {content.metadata}")

        # Save content data to database
        # await db.collection("Content").document(content.content_id).set(content.dict())
        print(f"Simulating saving content to DB: {content.dict()}")

        return {"content_id": content.content_id, "message": "File uploaded successfully", "metadata": content.metadata}
    except Exception as e:
        print(f"Error during file upload: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"File upload failed: {e}")

async def extract_metadata(file_path: str, file_extension: str) -> Dict:
    # Implement metadata extraction based on file type
    metadata = {}
    if file_extension == "pdf":
        #  In a real implementation, use a library like PyPDF2
        # with open(file_path, "rb") as f:
        #     reader = PyPDF2.PdfReader(f)
        #     metadata["pages"] = len(reader.pages)
        print(f"Simulating extracting PDF metadata from: {file_path}")
        metadata["pages"] = 10  # Placeholder
    elif file_extension in ["jpg", "jpeg", "png", "gif"]:
        # In a real implementation, use a library like Pillow
        # from PIL import Image
        # with Image.open(file_path) as img:
        #     metadata["resolution"] = f"{img.width}x{img.height}"
        print(f"Simulating extracting image metadata from: {file_path}")
        metadata["resolution"] = "1024x768"  # Placeholder
    # ... other file types
    return metadata