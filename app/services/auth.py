from datetime import (
    datetime,
    timedelta,
)
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import app_settings
from app.crud.user import user
from app.services.password import verify_password


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user_object = await user.get_by_username(db=db, username=username)
    if not user_object:
        return False
    if not verify_password(password, user_object.password):
        return False
    return user_object


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, app_settings.secret_key, algorithm=app_settings.algorithm)
    return encoded_jwt