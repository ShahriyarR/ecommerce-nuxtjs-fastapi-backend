import pytest
from backend.users import auth_service
from backend.users.schemas import UserCreate, UserInDB


@pytest.fixture(scope="class")
def auth_obj():
    return auth_service


@pytest.fixture(scope="class")
def dummy_user() -> UserInDB:
    new_user = UserCreate(
        email="dummy_user@example.com",
        username="dummy_user",
        password="dummyuserswesomepass"
    )
    new_password = auth_service.create_salt_and_hashed_password(plaintext_password=new_user.password)
    new_user_params = new_user.copy(update=new_password.dict())
    return UserInDB(**new_user_params.dict())
