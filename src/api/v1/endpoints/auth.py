from fastapi import APIRouter

router = APIRouter(tags=['Auth'])


@router.post('/register/')
async def register():
    pass


@router.post('/login/')
async def authentication():
    pass
