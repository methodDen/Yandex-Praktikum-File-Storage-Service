from fastapi import APIRouter

router = APIRouter()


@router.post('/ping')
async def ping():
    pass