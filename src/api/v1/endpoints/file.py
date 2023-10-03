from fastapi import APIRouter

router = APIRouter(tags=['File'])


@router.post('/upload/')
async def upload():
    pass


@router.get('/')
async def get_files_data():
    pass


@router.get('/download/')
async def download():
    pass
