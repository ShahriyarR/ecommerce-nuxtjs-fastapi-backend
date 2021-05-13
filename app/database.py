from gino.ext.starlette import Gino
from .core.config import settings


db = Gino(
    dsn=settings.DATABASE_URI
)