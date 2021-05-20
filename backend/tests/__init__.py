import pytest
import asyncio
from backend import db
from backend.app.core.config import settings


@pytest.fixture
async def init_db():
    conn = await db.set_bind(settings.DATABASE_URI)
    return conn
