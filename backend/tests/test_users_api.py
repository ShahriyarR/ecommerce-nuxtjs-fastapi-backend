import pytest
from backend.users.models import User
from asyncpg.exceptions import UniqueViolationError
from backend.users.schemas import UserCreate, UserLogin
from . import init_db


class TestAPI:

    async def remove_user(self, user_to_create):
        test_user = await User.query.where(User.username == user_to_create.username).gino.first()
        await test_user.delete()

    @pytest.mark.asyncio
    async def test_user_create(self, client, init_db, user_to_create):
        response = await client.post('users/create', json=user_to_create.dict())
        assert response.status_code == 200
        data = response.json()
        assert data['username'] == user_to_create.username
        await self.remove_user(user_to_create=user_to_create)

    @pytest.mark.asyncio
    async def test_user_create_twice(self, client, init_db, user_to_create):
        with pytest.raises(UniqueViolationError) as db_error:
            await client.post('users/create', json=user_to_create.dict())
            await client.post('users/create', json=user_to_create.dict())

        assert 'duplicate key value violates unique constraint' in str(db_error.value)
        await self.remove_user(user_to_create=user_to_create)

    @pytest.mark.asyncio
    async def test_user_create_wrong_email_format(self, client, init_db, user_to_create):
        wrong_user = UserCreate(
            email="wrong.user@gmail.com",
            username="wrong_user",
            password="wrong_user_password"
        )

        wrong_user.email = 'wrong_email'
        res = await client.post('users/create', json=wrong_user.dict())
        print(res.json())
        assert 'value is not a valid email address' == res.json()['detail'][0]['msg']

    @pytest.mark.asyncio
    async def test_user_create_wrong_username_format(self, client, init_db, user_to_create):
        wrong_user = UserCreate(
            email="wrong.user@gmail.com",
            username="wrong_user",
            password="wrong_user_password"
        )

        wrong_user.username = 'asd_sad$?'
        res = await client.post('users/create', json=wrong_user.dict())
        print(res.json())
        assert 'Invalid characters in username.' == res.json()['detail'][0]['msg']

    @pytest.mark.asyncio
    async def test_user_create_wrong_password_format(self, client, init_db, user_to_create):
        wrong_user = UserCreate(
            email="wrong.user@gmail.com",
            username="wrong_user",
            password="wrong_user_password"
        )

        wrong_user.password = '13'
        res = await client.post('users/create', json=wrong_user.dict())
        print(res.json())
        assert 'ensure this value has at least 7 characters' == res.json()['detail'][0]['msg']

    @pytest.mark.asyncio
    async def test_user_login_with_non_existing_username(self, client, init_db):
        fake_user = UserLogin(
            username="non-existing-username",
            password="fake-password"
        )
        res = await client.post('users/login', json=fake_user.dict())
        assert res.status_code == 404
        assert res.json()['detail'] == "User with given username not found"

    @pytest.mark.asyncio
    async def test_user_login_with_wrong_password(self, client, init_db, user_to_create):
        # Create the user
        res = await client.post('users/create', json=user_to_create.dict())
        assert res.json()['username'] == user_to_create.username

        # Try to login with wrong password
        fake_user = UserLogin(
            username="test_client",
            password="fake-password"
        )
        res = await client.post('users/login', json=fake_user.dict())
        assert res.status_code == 401
        assert res.json()['detail'] == 'Incorrect password provided'
        await self.remove_user(user_to_create=user_to_create)

    @pytest.mark.asyncio
    async def test_user_login_with_success(self, client, init_db, user_to_create):
        # Create the user
        res = await client.post('users/create', json=user_to_create.dict())
        assert res.json()['username'] == user_to_create.username

        # Try to login with wrong password
        valid_user = UserLogin(
            username="test_client",
            password="testclientpassword"
        )
        res = await client.post('users/login', json=valid_user.dict())
        assert res.status_code == 200
        assert res.json()['access_token']
        await self.remove_user(user_to_create=user_to_create)
