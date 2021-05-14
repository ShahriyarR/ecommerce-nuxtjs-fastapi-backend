import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .database import db

sys.path.append('..')

from backend.users.api.controller import router as user_router
from backend.users.authentication import Authenticate


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Init the database connection
    db.init_app(_app)

    # Register routes here
    _app.include_router(user_router, prefix='/users')
    
    return _app


# Init the Authentication service here
auth_service = Authenticate(db=db)

app = get_application()
