from fastapi import FastAPI
import models
from database import engine
from api.auth import auth
from api.todos import todos

app = FastAPI()


# runs only if todos.db does not exist
models.Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(todos.router)
