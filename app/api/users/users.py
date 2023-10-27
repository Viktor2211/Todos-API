from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from models import User
from schemas import UserVerification
from typing import Annotated
from api.auth.services import bcrypt_context, AuthService
from database import db_dependency


router = APIRouter(
    prefix='/user',
    tags=['user']
)

user_dependency = Annotated[dict, Depends(AuthService().get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'])


@router.get("/")
async def get_current_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    return db.query(User).filter(User.id == user.get("id")).first()


@router.put("/change_password/", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    current_user = db.query(User).filter(User.id == user.get("id")).first()
    if not bcrypt_context.verify(user_verification.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=401, detail="Текущий пароль введен неверно"
        )
    current_user.hashed_password = bcrypt_context.hash(
        user_verification.new_password)
    db.add(current_user)
    db.commit()
