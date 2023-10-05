from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from app.db.db import get_session
from app.schemas.base import MessageResponseSchema
from app.services.health_check import ping_database

router = APIRouter(tags=['Health Check'])


@router.get('/ping', response_model=MessageResponseSchema, status_code=status.HTTP_200_OK)
async def check_db_health(
    *,
    db: AsyncSession = Depends(get_session),
):
    is_db_healthy = await ping_database(db=db)
    if not is_db_healthy:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Database is not healthy',
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={'message': 'Database is healthy'},
    )