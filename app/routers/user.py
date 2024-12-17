from fastapi import APIRouter, Depends, status, HTTPException    # Сессия БД
from sqlalchemy.orm import Session
                                          # Функция подключения к БД
from app.backend.db_depends import get_db
                                          # Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models.user import User
from app.schemas import CreateUser, UpdateUser
                                           # Функции работы с записями.
from sqlalchemy import insert, select, update, delete
                                           # Функция создания slug-строки
from slugify import slugify



from app.models.user import User
from app.models.task import Task

router = APIRouter(prefix="/user", tags=["user"])



@router.get("/all_users")
async def get_all_users(db:Annotated[Session,Depends(get_db)]):
    users = db.scalar(select(User).where(User.username is not None)).all()
    return users


@router.get("/user_id")
async def user_by_id(db:Annotated[Session,Depends(get_db)],user_id:int):
    user = db.scalar(select(User).where(user_id == User.id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user




@router.post("/create")
async def create_user(db: Annotated[Session,Depends(get_db)],create_user:CreateUser):
    db.execute(insert(User).values(username  = create_user.username,
                                   firstname = create_user.firstname,
                                   lastname  = create_user.lastname,
                                   age       = create_user.age,
                                   slug      = slugify(create_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,'transaction':'Successful'}







@router.put("/update_user")
async def update_user(db:Annotated[Session,Depends(get_db)], user_id:int, update_user:UpdateUser):
    user = db.scalar(select(User).where(user_id == User.id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')

    db.execute(update(User).where(user_id == User.id).values(username  = update_user.username,
                                                             firstname = update_user.firstname,
                                                             lastname  = update_user.lastname,
                                                             age       = update_user.age,
                                                             slug      = slugify(update_user.username)))
    db.commit()
    return {'status_code': status.HTTP_200_OK,'transaction':'User update is successful'}




@router.delete("/delete")
async def delete_user(db:Annotated[Session,Depends(get_db)],user_id:int):
    user = db.scalar(select(User).where(user_id == User.id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')

    db.execute(delete(User).where(user_id == User.id))
    db.execute(delete(Task).where(user_id == Task.user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful'}

@router.get ("/user_id/tasks")
async def tasks_by_user_id(db:Annotated[Session,Depends(get_db)],user_id:int):
    tasks = db.scalar(select(Task).where(user_id == Task.user_id))
    if tasks is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return (tasks)

