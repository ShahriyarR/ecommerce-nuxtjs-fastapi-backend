import pytest
from backend.users import auth_service
from backend.users.schemas import UserCreate, UserInDB
from backend import app
from httpx import AsyncClient


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


@pytest.yield_fixture
async def client():
    async with AsyncClient(app=app, base_url='http://localhost:8000/') as async_client:
        yield async_client


@pytest.yield_fixture
def user_to_create():
    yield UserCreate(
            email="test_client@example.com",
            username="test_client",
            password="testclientpassword"
    )