import datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from app.database import db_dependency
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.models import User
from fastapi.security import OAuth2PasswordBearer
from app.database import SECRET_KEY, ALGORITHM


bcrypt_context = CryptContext(schemes=['bcrypt'])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class AuthService:

    def authenticate_user(self, username: str, password: str, db: db_dependency):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return False
        if not bcrypt_context.verify(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, username: str, user_id: int, role: str, expires_delta: datetime.timedelta):
        encode = {'sub': username, 'id': user_id, 'role': role}
        expires = datetime.datetime.now()+expires_delta
        encode.update({'exp': expires})
        return jwt.encode(claims=encode, key=SECRET_KEY, algorithm=ALGORITHM)

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_bearer)]):
        print("get_current_user")
        try:
            payload = jwt.decode(
                token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            user_id: int = payload.get("id")
            role: str = payload.get("role")
            if username is None or user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
            return {'username': username, 'id': user_id, 'role': role}
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        
