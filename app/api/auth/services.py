import datetime
from database import db_dependency
from jose import jwt
from passlib.context import CryptContext
from models import User
from fastapi.security import OAuth2PasswordBearer


bcrypt_context = CryptContext(schemes=['bcrypt'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')


SECRET_KEY = 'ldghl304skfj304ifl'
ALGORITHM = 'HS256'


class AuthService:
    def authenticate_user(self, username: str, password: str, db: db_dependency):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return False
        if not bcrypt_context.verify(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, username: str, user_id: int, expires_delta: datetime.timedelta):
        encode = {'sub': username, 'id': user_id}
        expires = datetime.datetime.now()+expires_delta
        encode.update({'exp': expires})
        return jwt.encode(claims=encode, key=SECRET_KEY, algorithm=ALGORITHM)
