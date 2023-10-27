from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from models import User
from schemas import UserRequest, Token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from api.auth.services import bcrypt_context, AuthService
from database import db_dependency


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

user_dependency = Annotated[dict, Depends(AuthService().get_current_user)]


@router.post("/create_user/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: UserRequest):
    user = User(
        email=user_request.email,
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        role=user_request.role,
        hashed_password=bcrypt_context.hash(user_request.password),
        is_active=True
    )
    db.add(user)
    db.commit()


@router.post("/all_users/")
async def get_all_users(db: db_dependency):
    return db.query(User).all()


@router.post("/token/", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):

    user = AuthService().authenticate_user(
        form_data.username, form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    token = AuthService().create_access_token(
        user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
