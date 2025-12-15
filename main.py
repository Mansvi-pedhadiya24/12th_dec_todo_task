from fastapi import FastAPI, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from db import SessionLocal, engine 
from models import Base
from datetime import datetime
import crud , math
from crud import soft_delete_todo
from schema import TodoCreate, TodoResponse, TodoUpdate , TodoListResponse


# Base.metadata.create_all(bind=engine)

app = FastAPI(title="ToDo project")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return {"message": "FastAPI working fine!"}


# CREATE
@app.post("/todo/", response_model=TodoResponse)
def create(todo: TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

# READ ALL
# @app.get("/todo/", response_model=list[TodoResponse])
# def read_all(db: Session = Depends(get_db)):
#     return crud.get_all_todos(db)



#read and search with pegination
@app.get("/todo/", response_model=TodoListResponse)
def get_todo_with_search(
    page: int = 1,
    limit: int = 5,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    todos, total_pages = crud.get_todos_with_search(db, page, limit, search)

    return {
        "status": True,
        "message": "Todo list fetched successfully",
        "total_pages": total_pages,
        "current_page": page,
        "search": search,
        "data": todos
    }



# READ ONE
@app.get("/todo/{todo_id}", response_model=TodoResponse)
def read_one(todo_id: int, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# DELETE
# @app.delete("/todo/{todo_id}")
# def delete(todo_id: int, db: Session = Depends(get_db)):
#     deleted = crud.delete_todo(db, todo_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Todo not found")
#     return {"message": "Todo deleted successfully"}

@app.delete("/todo/{todo_id}")
def soft_delete(todo_id:int,db:Session=Depends(get_db)):
    deleted=soft_delete_todo(db,todo_id)
    if not deleted:
        raise HTTPException(status_code=404,detail="Todo not found")
    return {"Message": "Todo soft deleted successfully"}


#UPDATE
@app.put("/todo/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, updated_data: TodoUpdate, db: Session = Depends(get_db)):

    todo = crud.get_todo(db ,todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update only provided fields
    if updated_data.name_todo is not None:
        todo.name_todo = updated_data.name_todo

    db.commit()
    db.refresh(todo)

    return todo

# #Search
# @app.get("/todo-list/search", response_model=list[TodoResponse])
# def search_todo(query: str, db: Session = Depends(get_db)):
#     return crud.search_todo(db, query)

 