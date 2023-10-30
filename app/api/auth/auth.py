from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import Token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.api.auth.services import bcrypt_context, AuthService
from app.database import db_dependency


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

user_dependency = Annotated[dict, Depends(AuthService().get_current_user)]


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
