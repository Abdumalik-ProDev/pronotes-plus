from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.note import NoteCreate, NoteOut
from app.repositories.note_repo import NoteRepo
from app.services.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteOut)
async def create_note(
    note: NoteCreate, db: AsyncSession = Depends(get_db)):
    repo = NoteRepo(db)
    service = NoteService(repo)
    note = await service.create_note(note)
    if not note:
        raise HTTPException(status_code=400, detail="Note creation failed")
    return note

@router.get("/{note_id}", response_model=NoteOut)
async def get_note(
    note_id: int, db: AsyncSession = Depends(get_db)):
    repo = NoteRepo(db)
    service = NoteService(repo)
    note = await service.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteOut)
async def update_note(
    note_id: int, note: NoteCreate, db: AsyncSession = Depends(get_db)):
    repo = NoteRepo(db)
    service = NoteService(repo)
    updated_note = await service.update_note(note_id, note)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found or update failed")
    return updated_note

@router.delete("/{note_id}", response_model=dict)
async def delete_note(
    note_id: int, db: AsyncSession = Depends(get_db)):
    repo = NoteRepo(db)
    service = NoteService(repo)
    success = await service.delete_note(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found or deletion failed")
    return {"detail": "Note deleted successfully"}