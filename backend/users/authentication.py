import bcrypt
from passlib.context import CryptContext
from backend.app.core.config import settings
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from pydantic import ValidationError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from .schemas import UserPasswordUpdate, UserInDB, JWTMeta, JWTCreds, JWTPayload, TokenData


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Authenticate:
    def create_salt_and_hashed_password(self, *, plaintext_password: str) -> UserPasswordUpdate:
        salt = self.generate_salt()
        hashed_password = self.hash_password(password=plaintext_password, salt=salt)
        return UserPasswordUpdate(salt=salt, password=hashed_password)

    @staticmethod
    def generate_salt() -> str:
        return bcrypt.gensalt().decode()

    @staticmethod
    def hash_password(*, password: str, salt: str) -> str:
        return pwd_context.hash(password + salt)

    @staticmethod
    def verify_password(*, password: str, salt: str, hashed_pw: str) -> bool:
        return pwd_context.verify(password + salt, hashed_pw)

    @staticmethod
    def create_access_token_for_user(
        *,
        user: UserInDB,
        secret_key: str = str(settings.SECRET_KEY),
        audience: str = settings.JWT_AUDIENCE,
        expires_in: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    ) -> Optional[str]:
        if not user or not isinstance(user, UserInDB):
            return None
        jwt_meta = JWTMeta(
            aud=audience,
            iat=datetime.timestamp(datetime.now()),
            exp=datetime.timestamp(datetime.now() + timedelta(minutes=expires_in)),
        )
        jwt_creds = JWTCreds(sub=user.email, username=user.username)
        token_payload = JWTPayload(
            **jwt_meta.dict(),
            **jwt_creds.dict(),
        )
        return jwt.encode(
            token_payload.dict(), secret_key, algorithm=settings.JWT_ALGORITHM
        )

    @staticmethod
    def get_username_from_token(*,
                                token: str,
                                secret_key: str = str(settings.SECRET_KEY)) -> Optional[str]:
        try:
            decoded_token = jwt.decode(token, str(secret_key),
                                       audience=settings.JWT_AUDIENCE,
                                       algorithms=[settings.JWT_ALGORITHM])
            payload = JWTPayload(**decoded_token)
        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload.username

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> UserInDB:
        from backend.users.crud import get_user_by_username

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            username = self.get_username_from_token(token=token)
            token_data = TokenData(username=username)
        except jwt.JWTError:
            raise credentials_exception
        user = await get_user_by_username(user_name=token_data.username)
        if user is None:
            raise credentials_exception
        return user


async def get_current_active_user(current_user: UserInDB = Depends(Authenticate().get_current_user)) -> UserInDB:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def check_if_user_is_admin(current_user: UserInDB = Depends(get_current_active_user)) -> UserInDB:
    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="You have not enough privileges")
    return current_user
