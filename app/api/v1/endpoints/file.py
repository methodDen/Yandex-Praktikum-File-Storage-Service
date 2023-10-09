import os.path
from typing import Annotated

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    Query,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import FileResponse

from app.api.deps import get_current_user
from app.core.config import app_settings
from app.db.db import get_session
from app.schemas.file import (
    FileResponseSchema,
    FileListResponseSchema,
)
from app.schemas.user import CurrentUserSchema
from app.crud.file import file


router = APIRouter(tags=['File'])


@router.post(
    '/upload',
    response_model=FileResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description='Upload file',
)
async def upload_file(
    *,
    file_to_be_saved: UploadFile = File(..., description='File to upload'),
    current_user: CurrentUserSchema = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    if not os.path.isdir(app_settings.file_folder):
        os.mkdir(app_settings.file_folder)

    file_path = os.path.join(app_settings.file_folder, file_to_be_saved.filename)

    file_object = await file.create_or_override_file(
        db=db,
        file_owner_id=current_user.id,
        file_to_save=file_to_be_saved,
        path_to_save=file_path
    )
    return file_object


@router.get(
    '/list',
    response_model=FileListResponseSchema,
    description='Get files list data of current user',
)
async def get_files_data(
    *,
    db: AsyncSession = Depends(get_session),
    current_user: CurrentUserSchema = Depends(get_current_user),
    max_results: Annotated[int, Query(description="Pagination page size", ge=1)] = 10,
    offset: Annotated[int, Query(description="Pagination page offset", ge=0)] = 0,
):
    files = await file.get_file_list_by_user_id(db=db, user_id=current_user.id, skip=offset, limit=max_results)
    return {
        'files': files
    }


@router.get('/download', status_code=status.HTTP_200_OK, description='Download file')
async def download_file(
    path: str | int = Query(..., description='Path or id of file'),
    db: AsyncSession = Depends(get_session),
    current_user: CurrentUserSchema = Depends(get_current_user),
):
    if path.find('/') != -1:
        file_object = await file.get_file_by_path(
            db=db,
            file_path=path,
            user_id=current_user.id,
        )
    else:
        file_object = await file.get_file_by_id(
            db=db,
            file_id=int(path),
            user_id=current_user.id,
        )

    if not file_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not found'
        )

    if not file_object.is_downloadable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You can not download this file'
        )

    if not os.path.isfile(file_object.path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File path is not reachable on server'
        )

    return FileResponse(
        path=file_object.path,
        media_type='application/octet-stream',
        filename=file_object.name
    )


