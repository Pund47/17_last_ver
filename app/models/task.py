#from enum import unique
from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
#from user import User


class Task(Base):
    __tablename__ = 'tasks'                                                       # __tablename__ = 'tasks'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer,primary_key=True,index=True)                              #id - целое число, первичный ключ, с индексом.
    title = Column(String)                                                        #title - строка.
    content = Column(String)                                                      #content - строка.
    priority = Column(Integer,default=0)                                          #priority - целое число, по умолчанию 0.
    completed = Column(Boolean,default=False)                                     #completed - булевое значение, по умолчанию False.
    user_id = Column(Integer,ForeignKey('users.id'),nullable=False,index=True)    #user_id - целое число, внешний ключ на id из таблицы 'users', не NULL, с индексом.
    slug = Column(String,unique=True,index=True)                                  #slug - строка, уникальная, с индексом.
    user = relationship('User',back_populates='tasks')                   #user - объект связи с таблицей с таблицей User, где back_populates='tasks'.

#    class Config:
#        orm_mode = True  # Указывает, что объект может быть преобразован из ORM (например, SQLAlchemy)




#from sqlalchemy.schema import CreateTable
#print(CreateTable(Task.__table__))

