from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks, Query
from typing import Dict, List, Optional
from app.services.content import upload_service, processing_service, organization_service, retrieval_service  # Import new services
from app.core.middleware import get_current_user  # Add this import

router = APIRouter()

@router.post("/upload", response_model=Dict)
async def upload_content(file: UploadFile = File(...), user = Depends(get_current_user)):
    return await upload_service.upload_file(user["user_id"], file)

@router.post("/{content_id}/process")
async def process_uploaded_content(content_id: str, background_tasks: BackgroundTasks, user = Depends(get_current_user)):
    #  In real implementation, check if the content belongs to the user
    background_tasks.add_task(processing_service.process_content, content_id)
    return {"message": f"Content {content_id} processing started in the background"}

@router.get("/{content_id}/status")
async def get_processing_status(content_id: str, user = Depends(get_current_user)):
    # In real implementation, check if the content belongs to the user
    return await processing_service.get_processing_status(content_id)

@router.post("/folders")
async def create_folder(folder_name: str, parent_folder_id: Optional[str] = None, user = Depends(get_current_user)):
    #  Create a new folder
    return await organization_service.create_folder(user["user_id"], folder_name, parent_folder_id)

@router.get("/folders/{folder_id}/contents")  # Or /folders/{folder_id}, using a query param to differentiate folder vs contents
async def get_folder_contents(folder_id: Optional[str] = None, user = Depends(get_current_user)):
    # Get contents of a folder (or root if no folder_id)
    return await organization_service.get_folder_contents(user["user_id"], folder_id)

@router.put("/contents/{content_id}/folder")
async def move_content(content_id: str, new_folder_id: str, user = Depends(get_current_user)):
    #  Move content to a different folder
    return await organization_service.move_content(user["user_id"], content_id, new_folder_id)

@router.post("/contents/{content_id}/tags")
async def add_tags(content_id: str, tags: List[str] = Query(...), user = Depends(get_current_user)):
    # Add tags to content
    return await organization_service.add_tags(user["user_id"], content_id, tags)

@router.put("/contents/{content_id}/yet_to_read")
async def update_yet_to_read(content_id: str, yet_to_read: bool, user = Depends(get_current_user)):
    # Update the "yet to read" status of content
    return await organization_service.update_yet_to_read(user["user_id"], content_id, yet_to_read)

@router.get("/{content_id}")
async def get_content(content_id: str, user = Depends(get_current_user)):
    #  Get content details
    return await retrieval_service.get_content(user["user_id"], content_id)

@router.get("/")
async def list_contents(page: int = 1, page_size: int = 10, folder_id: Optional[str] = None, search_query: Optional[str] = None, user = Depends(get_current_user)):
    #  List contents (with pagination, filtering, search)
    return await retrieval_service.list_contents(user["user_id"], page, page_size, folder_id, search_query)

@router.get("/{content_id}/reading_time")
async def estimate_reading_time(content_id: str, user = Depends(get_current_user)):
    #  Estimate reading time
    return await retrieval_service.estimate_reading_time(content_id)

@router.post("/{content_id}/access")
async def track_access(content_id: str, user = Depends(get_current_user)):
    # Track content access
    return await retrieval_service.track_recent_access(user["user_id"], content_id)