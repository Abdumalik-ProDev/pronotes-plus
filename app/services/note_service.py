from app.repositories.note_repo import NoteRepo
from app.models.note import Note
from app.schemas.note import NoteCreate

class NoteService:
    def __init__(self, note_repo: NoteRepo):
        self.note_repo = note_repo

    async def create_note(self, note_create: NoteCreate, owner_id: int) -> Note:
        new_note = await self.note_repo.create_note(
            title=note_create.title,
            content=note_create.content,
            owner_id=owner_id
        )
        return new_note
    
    async def get_note_by_id(self, note_id: int) -> Note | None:
        return await self.note_repo.get_note_by_id(note_id)
    
    async def update_note(self, note_id: int, note_update: NoteCreate) -> Note | None:
        note = await self.note_repo.get_note_by_id(note_id)
        if not note:
            return None
        updated_note = await self.note_repo.update_note(
            note_id,
            title=note_update.title,
            content=note_update.content
        )
        return updated_note
    
    async def delete_note(self, note_id: int) -> bool:
        note = await self.note_repo.get_note_by_id(note_id)
        if not note:
            return False
        await self.note_repo.delete_note(note_id)
        return True