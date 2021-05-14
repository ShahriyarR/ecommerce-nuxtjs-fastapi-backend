from fastapi import APIRouter, status, Body
from fastapi.responses import JSONResponse
from ..schemas import UserCreate, UserInDB, UserPublic

router = APIRouter()


@router.post(
    "/create",
    tags=["user registration"],
    description="Register the User",
    response_model=UserPublic,
)
async def user_create(user: UserCreate) -> UserInDB:
    from backend.app.main import auth_service

    return auth_service.register_new_user(user)
