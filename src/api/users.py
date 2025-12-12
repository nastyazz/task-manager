from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserRead, UserCreate
from src.storage.db.db import get_db
from src.storage.db.repositories import UserRepository
from src.api.dependencies import get_current_user
from fastapi.exceptions import HTTPException

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: str, user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.update_user(user_id, username=user_data.username, email=user_data.email)
    return user

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    await repo.delete_user(user_id)

