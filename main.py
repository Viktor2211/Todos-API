from fastapi import FastAPI
from app.models import Base
from app.database import engine
from app.api.auth import auth
from app.api.todos import todos
from app.api.admin import admin
from app.api.users import users

app = FastAPI()


# runs only if todos.db does not exist
Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
