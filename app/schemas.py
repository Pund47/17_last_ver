from pydantic import BaseModel

class CreateUser(BaseModel):
#   id = int
    username: str
    firstname: str
    lastname: str
    age: int
    slug : str
    tasks : str
    class Config:
        orm_mode = True  # Указывает, что объект может быть преобразован из ORM (например, SQLAlchemy)

class UpdateUser(BaseModel):
#    id = int
    username: str
    firstname: str
    lastname: str
    age: int
    slug: str
    tasks: str
    class Config:
        orm_mode = True  # Указывает, что объект может быть преобразован из ORM (например, SQLAlchemy)

class CreateTask(BaseModel):
#    id: int
    title: str
    content: str
    priority: int
    completed: bool
    user_id : int
    slug : str
    class Config:
        orm_mode = True  # Указывает, что объект может быть преобразован из ORM (например, SQLAlchemy)

class UpdateTask(BaseModel):
#    id: int
    title: str
    content: str
    priority: int
    completed: bool
    user_id: int
    slug: str
class Config:
        orm_mode = True  # Указывает, что объект может быть преобразован из ORM (например, SQLAlchemy)