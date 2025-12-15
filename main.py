from fastapi import FastAPI, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from models import Base
import crud 
from crud import soft_delete_todo
from schema import TodoCreate, TodoResponse, TodoUpdate

Base.metadata.create_all(bind=engine)

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



# READ ALL with pagination
@app.get("/todo/",response_model=list[TodoResponse])
def read_all(page : int=Query(1,ge=1),limit : int=Query(10,ge=1,le=100),db:Session=Depends(get_db)):
    return crud.get_all_todos(db,page,limit)


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

#Search
@app.get("/todo-list/search", response_model=list[TodoResponse])
def search_todo(query: str, db: Session = Depends(get_db)):
    return crud.search_todo(db, query)

 