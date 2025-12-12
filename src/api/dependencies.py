from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from datetime import datetime, timedelta
from src.storage.db.db import get_db
from src.storage.db.repositories import UserRepository
from config.settings import settings

API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

ALGORITHM = "HS256"


def create_access_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.GIT_SECRET, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Security(api_key_header),
    db: AsyncSession = Depends(get_db)
):

    if token.startswith("Bearer "):
        token = token[len("Bearer "):]

    repo = UserRepository(db)

    try:
        payload = jwt.decode(token, settings.GIT_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
