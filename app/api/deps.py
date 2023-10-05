
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.config import app_settings
from app.crud.user import user
from app.db.db import get_session
from app.schemas.user import UserTokenData

reuseable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="v1/auth/token",
)


async def get_current_user(
    db: AsyncSession = Depends(get_session),
    token: str = Depends(reuseable_oauth2),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            app_settings.secret_key,
            algorithms=[app_settings.algorithm],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = UserTokenData(username=username)
    except JWTError:
        raise credentials_exception
    user_object = await user.get_by_username(db, username=token_data.username)
    if user_object is None:
        raise credentials_exception
    return user_object