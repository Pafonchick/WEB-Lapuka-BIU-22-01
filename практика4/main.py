from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from model.todo import Todo, TodoInput
from repository.todo import TodoRepository
from database import get_db, migrate

app = FastAPI()

migrate()

@app.get("/todos", response_model=List[Todo])
def get_todos(db: Session = Depends(get_db)):
    return TodoRepository.get_all(db)

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: TodoInput, db: Session = Depends(get_db)):
    return TodoRepository.create(db, todo)

@app.get("/todos/{id}", response_model=Todo)
def get_todo(id: int, db: Session = Depends(get_db)):
    todo = TodoRepository.get_by_id(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{id}", response_model=Todo)
def update_todo(id: int, todo_data: TodoInput, db: Session = Depends(get_db)):
    todo = TodoRepository.update(db, id, todo_data)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.delete("/todos/{id}", status_code=204)
def delete_todo(id: int, db: Session = Depends(get_db)):
    if not TodoRepository.delete(db, id):
        raise HTTPException(status_code=404, detail="Todo not found")