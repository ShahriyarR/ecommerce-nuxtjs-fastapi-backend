import bcrypt
import gino
from passlib.context import CryptContext
from backend.users.schemas import UserPasswordUpdate, UserCreate, UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Authenticate:
    def __init__(self, db: gino.Gino):
        self.db = db

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

    async def register_new_user(self, new_user: UserCreate) -> UserInDB:
        from backend.users.models import User

        new_password = self.create_salt_and_hashed_password(plaintext_password=new_user.password)
        new_user_params = new_user.copy(update=new_password.dict())
        created_user = User(**new_user_params)
        self.db.add(created_user)
        self.db.commit()
        self.db.refresh(created_user)
        return UserInDB(created_user.dict())
