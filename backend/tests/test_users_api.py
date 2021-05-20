import pytest
from backend.users.models import User
from asyncpg.exceptions import UniqueViolationError
from pydantic.error_wrappers import ValidationError
from backend.users.schemas import UserCreate
from . import init_db


class TestAPI:

    @pytest.mark.asyncio
    async def teardown_method(self, user_to_create):
        test_user = await User.query.where(User.username == user_to_create.username).gino.first()
        await test_user.delete()

    @pytest.mark.asyncio
    async def test_user_create(self, client, init_db, user_to_create):
        response = await client.post('users/create', json=user_to_create.dict())
        assert response.status_code == 200
        data = response.json()
        assert data['username'] == user_to_create.username
        await self.teardown_method(user_to_create=user_to_create)

    @pytest.mark.asyncio
    async def test_user_create_twice(self, client, init_db, user_to_create):
        with pytest.raises(UniqueViolationError) as db_error:
            await client.post('users/create', json=user_to_create.dict())
            await client.post('users/create', json=user_to_create.dict())

        assert 'duplicate key value violates unique constraint' in str(db_error.value)
        await self.teardown_method(user_to_create=user_to_create)

    @pytest.mark.asyncio
    async def test_user_create_wrong_email_format(self, client, init_db):
        wrong_user = UserCreate(
            email="wrong_format_email",
            username="wrong_user",
            password="wrong_user_password"
        )
        with pytest.raises(ValidationError) as validation_error:
            await client.post('users/create', json=wrong_user.dict())

        print("Heyyyyy", str(validation_error.value))

        assert 'pydantic.error_wrappers.ValidationError' in str(validation_error.value)


