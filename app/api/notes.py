from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Optional
from app.services.notes import generation_service, management_service, customization_service
from app.models.notes import Note, NoteVersion
# Assuming authentication middleware 'get_current_user' provides user info

router = APIRouter()

@router.post("/generate", response_model=Dict)
async def generate_notes(content_id: str, user_preferences: Optional[Dict] = None, learning_mode: Optional[str] = None, user = Depends(get_current_user)):
    return await generation_service.generate_notes(content_id, user["user_id"], user_preferences, learning_mode)

@router.get("/{note_id}", response_model=Note)
async def get_note(note_id: str, user = Depends(get_current_user)):
    note = await management_service.get_note(note_id, user["user_id"])
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.get("/", response_model=List[Note])
async def list_notes(content_id: Optional[str] = None, topic_id: Optional[str] = None, user = Depends(get_current_user)):
    return await management_service.list_notes(user["user_id"], content_id, topic_id)

@router.put("/{note_id}", response_model=Dict)
async def update_note(note_id: str, content: str, format_options: Optional[Dict] = None, user = Depends(get_current_user)):
    return await management_service.update_note(note_id, user["user_id"], content, format_options)

@router.get("/{note_id}/versions", response_model=List[NoteVersion])
async def get_note_versions(note_id: str, user = Depends(get_current_user)):
    return await management_service.get_note_versions(note_id, user["user_id"])

@router.put("/{note_id}/formatting", response_model=Dict)
async def update_formatting(note_id: str, format_options: Dict, user = Depends(get_current_user)):
    return await customization_service.update_formatting(note_id, user["user_id"], format_options)

@router.put("/{note_id}/restructure", response_model=Dict)
async def restructure_content(note_id: str, structure_type: str = Query(...), user = Depends(get_current_user)):
    return await customization_service.restructure_content(note_id, user["user_id"], structure_type)

@router.put("/{note_id}/save", response_model=Dict)
async def save_note(note_id: str, content: str, user = Depends(get_current_user)):
    return await customization_service.save_note(note_id, user["user_id"], content)

@router.post("/{note_id}/export", response_model=Dict)
async def export_note(note_id: str, format: str = Query(...), user = Depends(get_current_user)):
    return await customization_service.export_note(note_id, user["user_id"], format)