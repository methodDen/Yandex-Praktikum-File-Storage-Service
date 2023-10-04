from fastapi import APIRouter

router = APIRouter(tags=['Health Check'])


@router.post('/ping/')
async def ping():
    pass