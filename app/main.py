import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .database import db
from backend.users.api.controller import router as user_router

sys.path.append('..')

app = FastAPI(title=settings.PROJECT_NAME)
db.init_app(app)


@app.on_event("startup")
async def startup():
    print("app started")


@app.on_event("shutdown")
async def shutdown():
    print("SHUTDOWN")


app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(user_router)