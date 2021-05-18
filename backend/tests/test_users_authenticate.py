import pytest
from jose import jwt
from backend.app.core.config import settings


@pytest.mark.usefixtures('auth_obj')
@pytest.mark.usefixtures('dummy_user')
class TestAuthenticate:

    def test_create_salt_and_hashed_password(self, auth_obj):
        test_password = '123456789'
        first_password = auth_obj.create_salt_and_hashed_password(plaintext_password=test_password)
        second_password = auth_obj.create_salt_and_hashed_password(plaintext_password=test_password)
        assert first_password.password is not second_password.password

    def test_create_access_token_for_user(self, auth_obj, dummy_user):
        token = auth_obj.create_access_token_for_user(user=dummy_user)
        print(token)
        decoded = jwt.decode(token,
                             str(settings.SECRET_KEY),
                             audience=settings.JWT_AUDIENCE,
                             algorithms=settings.JWT_ALGORITHM)
        print(decoded)
