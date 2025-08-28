from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.repositories.user_repo import UserRepo
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut)
async def create_user(
    user: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepo(db)
    service = UserService(repo)
    user = await service.register_user(user)
    if not user:
        raise HTTPException(status_code=400, detail="User creation failed")
    return user

@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int, db: AsyncSession = Depends(get_db)):
    repo = UserRepo(db)
    service = UserService(repo)
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepo(db)
    service = UserService(repo)
    updated_user = await service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found or update failed")
    return updated_user

@router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: int, db: AsyncSession = Depends(get_db)):
    repo = UserRepo(db)
    service = UserService(repo)
    success = await service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found or deletion failed")
    return {"detail": "User deleted successfully"}