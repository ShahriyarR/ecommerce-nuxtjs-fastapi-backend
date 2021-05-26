import os
from fastapi import HTTPException, UploadFile
import aiofiles
import uuid

BASEDIR = os.path.dirname(__file__)


async def handle_file_upload(file: UploadFile) -> str:
    _, ext = os.path.splitext(file.filename)
    img_dir = os.path.join(BASEDIR, 'statics/media/')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    content = await file.read()
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")
    file_name = f'{uuid.uuid4().hex}{ext}'
    async with aiofiles.open(os.path.join(img_dir, file_name), mode='wb') as f:
        await f.write(content)

    return file_name
