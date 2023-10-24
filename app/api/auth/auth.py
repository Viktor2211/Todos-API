from datetime import timedelta
from fastapi import APIRouter, Depends, status
from models import User
from schemas import UserRequest, Token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from api.auth.services import AuthService, oauth2_bearer, bcrypt_context
from database import db_dependency


router = APIRouter()



@router.post("/auth/", status_code=status.HTTP_201_CREATED)
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


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    
    user = AuthService().authenticate_user(form_data.username, form_data.password, db=db)
    if not user:
        return {'access_token': 'Failed authentication', 'token_type': 'bearer'}
    token = AuthService().create_access_token(user.username, user.id, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
