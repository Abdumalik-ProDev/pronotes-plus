from sqlalchemy import select
from app.models.note import Note
from sqlalchemy.ext.asyncio import AsyncSession

class NoteRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_note(self, title: str, content: str, owner_id: int) -> Note:
        new_note = Note(title=title, content=content, owner_id=owner_id)
        self.session.add(new_note)
        await self.session.commit()
        await self.session.refresh(new_note)
        return new_note
    
    async def list_by_owner(self, owner_id: int) -> list[Note]:
        result = await self.session.execute(
            select(Note).where(Note.owner_id == owner_id))
        return result.scalars().all()