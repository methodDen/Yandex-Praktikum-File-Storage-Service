from fastapi import APIRouter, Query, UploadFile, File, Depends
from starlette import status

from app.api.deps import get_current_user
from app.schemas.file import FileResponseSchema
from app.schemas.user import CurrentUserSchema

router = APIRouter(tags=['File'])


@router.post(
    '/upload/',
    response_model=FileResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description='Upload file',
)
async def upload(
    *,
    path_to_save: str = Query(..., description='Path to save file'),
    file: UploadFile = File(..., description='File to upload'),
    current_user: CurrentUserSchema = Depends(get_current_user),
):
    pass


@router.get('/')
async def get_files_data():
    pass


@router.get('/download/')
async def download():
    pass
