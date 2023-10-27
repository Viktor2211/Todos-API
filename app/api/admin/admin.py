from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from models import User, Todos
from schemas import UserRequest, Token
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from api.auth.services import oauth2_bearer, bcrypt_context, AuthService
from database import db_dependency


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


user_dependency = Annotated[dict, Depends(AuthService().get_current_user)]


@router.get("/todos/", status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency, db:db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='У вас нет прав админа')
    return db.query(Todos).all()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency, db:db_dependency, todo_id:int):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='У вас нет прав админа')
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()