from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from app.models import User, Todos
from typing import Annotated
from app.api.auth.services import AuthService
from app.database import db_dependency
from app.schemas import UserRequest
from app.api.auth.services import bcrypt_context


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


user_dependency = Annotated[dict, Depends(AuthService().get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'])


@router.get("/todos/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='У вас нет прав админа')
    return db.query(Todos).all()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='У вас нет прав админа')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()


@router.get("/users/", status_code=status.HTTP_200_OK)
async def retrieve_all_users(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='У вас нет прав админа')
    return db.query(User).all()


@router.post("/create_user/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user:user_dependency, user_request: UserRequest):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail='У вас нет прав админа')
    user = User(
        email=user_request.email,
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        phone_number = user_request.phone_number, 
        role=user_request.role,
        hashed_password=bcrypt_context.hash(user_request.password),
        is_active=True
    )
    db.add(user)
    db.commit()