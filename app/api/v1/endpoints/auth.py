from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.crud.user import user
from app.db.db import get_session
from app.schemas.user import (
    UserRegisterRequestSchema,
    UserRegisterResponseSchema,
)

router = APIRouter(tags=['Auth'])


@router.post(
    '/register/',
    response_model=UserRegisterResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description='User registration'
)
async def register(
    *,
    db: AsyncSession = Depends(get_session),
    user_in: UserRegisterRequestSchema
):
    user_object = await user.get_by_username(db=db, username=user_in.username)
    if user_object:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with such username already exists'
        )
    user_object = await user.create(db=db, obj_in=user_in)
    return user_object


@router.post('/login/')
async def authentication():
    pass
