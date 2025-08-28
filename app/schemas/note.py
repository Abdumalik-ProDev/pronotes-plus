from app.schemas.base import BaseSchema

class NoteCreate(BaseSchema):
    title: str
    content: str

class NoteOut(BaseSchema):
    id: int
    title: str
    content: str
    owner_id: int