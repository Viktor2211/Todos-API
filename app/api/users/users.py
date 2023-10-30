from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from app.models import User
from app.schemas import UserVerification, UpdatePhone
from typing import Annotated
from app.api.auth.services import bcrypt_context, AuthService
from app.database import db_dependency


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
    current_user = db.query(User).filter(User.id == user.get("id")).first()
    if not bcrypt_context.verify(user_verification.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=401, detail="Текущий пароль введен неверно"
        )
    current_user.hashed_password = bcrypt_context.hash(
        user_verification.new_password)
    db.add(current_user)
    db.commit()


@router.put("/update_phone/", status_code=status.HTTP_202_ACCEPTED)
async def update_phone_number(user: user_dependency, db: db_dependency, update_phone: UpdatePhone):
    current_user = db.query(User).filter(User.id == user.get("id")).first()
    current_user.phone_number = update_phone.new_number
    db.add(current_user)
    db.commit()
