from gino.ext.starlette import Gino
from .core.config import settings


db: Gino = Gino(
    dsn=settings.DATABASE_URI,
    pool_min_size=3,
    pool_max_size=20,
    retry_limit=1,
    retry_interval=1,
    ssl=None,
)
