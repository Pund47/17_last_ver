from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.schemas import CreateTask, UpdateTask, CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify
from app.models.task import Task
from app.models.user  import User

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/all_tasks")
async def get_all_tasks(db:Annotated[Session,Depends(get_db)]):
    tasks = db.scalar(select(Task).where(Task.completed == False)).all()
    return tasks


@router.get("/task_id")
async def task_by_id(db:Annotated[Session,Depends(get_db)],task_id:int):
    task = db.scalar(select(Task).where(task_id == Task.id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    return task

@router.post("/create")
async def create_task(db: Annotated[Session,Depends(get_db)],create_task:CreateTask,user_id:int):
    user = db.scalar(select(User).where(user_id == User.id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    db.execute(insert(Task).values(title     = create_task.title,
                                   content   = create_task.content,
                                   priority  = create_task.priority,
                                   completed = create_task.completed,
                                   user_id   = user_id,
                                   slug      = slugify(create_task.title)))

    db.execute(update(User).where(user_id == User.id).values(task = Task))

    db.commit()
    return {'status_code': status.HTTP_201_CREATED,'transaction':'Successful'}



@router.put("/update_task")
async def update_task(db:Annotated[Session,Depends(get_db)], task_id:int, update_task:UpdateTask):
    task = db.scalar(select(Task).where(task_id == Task.id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Task not found')

    db.execute(update(Task).where(task_id == Task.id).values(title     = update_task.title,
                                                             content   = update_task.content,
                                                             priority  = update_task.priority,
                                                             completed = update_task.completed,
                                                             slug      = slugify(update_task.title)))
    db.commit()
    return {'status_code': status.HTTP_200_OK,'transaction':'User update is successful'}





@router.delete("/delete")
async def delete_task(db:Annotated[Session,Depends(get_db)],task_id:int):
    task = db.scalar(select(Task).where(task_id == Task.id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Task not found')

    db.execute(delete(Task).where(task_id == Task.id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task delete is successful'}