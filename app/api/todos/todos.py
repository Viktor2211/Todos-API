from fastapi import HTTPException, status, Path, APIRouter
import models
from schemas import TodoRequest
from database import db_dependency


router = APIRouter()


@router.get("/todos/", status_code=status.HTTP_200_OK)
async def get_all_todos(db: db_dependency):
    return db.query(models.Todos).all()


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id=Path(gt=0)):
    todo_model = db.query(models.Todos).filter(
        models.Todos.id == todo_id).first()
    if todo_model:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')


@router.post("/todos/create/", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = models.Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()


@router.put("/todos/update/{todo_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(models.Todos).filter(
        models.Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    todo_model.title = todo_request.title
    todo_model.desciption = todo_request.desciption
    todo_model.priority = todo_request.priority
    todo_model.completed = todo_request.completed
    db.add(todo_model)
    db.commit()


@router.delete("/todos/delete/{todo_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(models.Todos).filter(
        models.Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Запись не найдена')
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()
