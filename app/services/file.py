from aioshutil import copyfileobj
from fastapi import File


async def write_to_file(
    file_obj: File,
    full_file_path: str,
):
    with open(full_file_path, 'wb') as buffer:
        await copyfileobj(file_obj.file, buffer)
