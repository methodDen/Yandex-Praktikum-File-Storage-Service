from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.config import app_settings
from app.crud.user import user
from app.db.db import get_session
from app.schemas.user import (
    UserRegisterRequestSchema,
    UserRegisterResponseSchema,
    AccessTokenResponse,
    UserLoginRequestSchema,
)
from app.services.auth import authenticate_user, create_access_token

router = APIRouter(tags=['Auth'])


@router.post(
    '/register/',
    response_model=UserRegisterResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description='User registration',
)
async def register(
    *,
    db: AsyncSession = Depends(get_session),
    user_in: UserRegisterRequestSchema,
):
    user_object = await user.get_by_username(db=db, username=user_in.username,)
    if user_object:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with such username already exists',
        )
    user_object = await user.create(db=db, obj_in=user_in,)
    return user_object


@router.post(
    '/login/',
    response_model=AccessTokenResponse,
    status_code=status.HTTP_200_OK,
    description='Get access token',
)
async def authentication(
    *,
    db: AsyncSession = Depends(get_session),
    user_in: UserLoginRequestSchema,
):
    username, password = user_in.username, user_in.password
    user_object = await authenticate_user(db, username, password)
    if not user_object:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=app_settings.token_expire_minutes)
    access_token = create_access_token(
        data={'sub': user_object.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token}
