from sqlalchemy.future import select
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create_user(self, username: str, email: str) -> User:
        new_user = User(username=username, email=email)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user