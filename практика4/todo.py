from sqlalchemy import Column, Integer, String, Boolean
from database import Base
from pydantic import BaseModel

class TodoModel(Base):
    __tablename__ = "todos"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)

class TodoInput(BaseModel):
    title: str
    completed: bool = False

class Todo(TodoInput):
    id: int