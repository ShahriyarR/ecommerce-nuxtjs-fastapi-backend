from fastapi import HTTPException
from .schemas import UserCreate, UserInDB
from backend.users import auth_service
from .models import User


async def create_user(new_user: UserCreate) -> UserInDB:
    new_password = auth_service.create_salt_and_hashed_password(plaintext_password=new_user.password)
    new_user_params = new_user.copy(update=new_password.dict())
    new_user_updated = UserInDB(**new_user_params.dict())
    created_user = await User.create(**new_user_updated.dict())

    return UserInDB.from_orm(created_user)


async def get_user_by_username(user_name: str) -> UserInDB:
    found_user = await User.query.where(User.username == user_name).gino.first()
    if found_user:
        return UserInDB.from_orm(found_user)
    raise HTTPException(status_code=404, detail="User with given username not found")
