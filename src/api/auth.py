from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserCreate, UserRead
from src.schemas.token import Token
from src.storage.db.db import get_db
from src.storage.db.repositories import UserRepository
from src.api.dependencies import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=UserRead)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    existing = await repo.get_user_by_username(user.username)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    created = await repo.create_user(username=user.username, email=user.email)
    return created



@router.post("/login", response_model=Token)
async def login(username: str, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token)
