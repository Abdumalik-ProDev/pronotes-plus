from app.schemas.user import UserCreate
from app.repositories.user_repo import UserRepo
from app.models.user import User

class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def register_user(self, user_create: UserCreate) -> User:
        existing_user = await self.user_repo.get_user_by_email(user_create.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        new_user = await self.user_repo.create_user(
            username=user_create.username,
            email=user_create.email
        )
        return new_user
    
    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.user_repo.get_user_by_id(user_id)
    
    async def update_user(self, user_id: int, user_update: UserCreate) -> User | None:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            return None
        updated_user = await self.user_repo.update_user(
            user_id,
            username=user_update.username,
            email=user_update.email
        )
        return updated_user
    
    async def delete_user(self, user_id: int) -> bool:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            return False
        await self.user_repo.delete_user(user_id)
        return True