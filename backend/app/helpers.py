import os
import aiofiles
import uuid
from io import BytesIO
from PIL import Image
from fastapi import HTTPException, UploadFile
from typing import Tuple


BASEDIR = os.path.dirname(__file__)


async def file_operations(file: UploadFile) -> Tuple[bytes, str, str]:
    _, ext = os.path.splitext(file.filename)
    img_dir = os.path.join(BASEDIR, 'statics/media/')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    content = await file.read()
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")
    return content, ext, img_dir


def make_thumbnail(file: str, size: tuple = (300, 200)) -> BytesIO:
    img = Image.open(file)
    rgb_im = img.convert('RGB')
    rgb_im.thumbnail(size)

    thumb_io = BytesIO()
    rgb_im.save(thumb_io, format='PNG', quality=85)
    thumb_io.seek(0)
    return thumb_io


async def handle_file_upload(file: UploadFile) -> Tuple[str, str]:
    content, ext, img_dir = await file_operations(file)
    file_name = f'{uuid.uuid4().hex}{ext}'
    async with aiofiles.open(os.path.join(img_dir, file_name), mode='wb') as f:
        await f.write(content)

    new_file = os.path.join(BASEDIR, f'statics/media/{file_name}')
    thumbnail_name = f'thumb_{file_name}'
    thumbnail_content = make_thumbnail(new_file)

    async with aiofiles.open(os.path.join(img_dir, thumbnail_name), mode='wb') as f:
        await f.write(thumbnail_content.read())
        thumbnail_content.close()

    return file_name, thumbnail_name
