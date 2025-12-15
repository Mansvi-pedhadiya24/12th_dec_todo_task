from sqlalchemy.orm import Session
from models import Todo
from schema import TodoCreate
from datetime import datetime

def create_todo(db: Session, todo: TodoCreate):
    db_todo = Todo(
        name_todo=todo.name_todo,
        status=todo.status
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# def get_all_todos(db):
#     todos = db.query(Todo).filter(Todo.deleted_at == None).all()  
#     return todos

def get_all_todos(db:Session,page:int = 1 , limit:int = 10):
    offset = (page-1)*limit

    return(
        db.query(Todo).filter(Todo.deleted_at == None).offset(offset).limit(limit).all()
    )





def get_todo(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id,Todo.deleted_at==None).first()


# def delete_todo(db: Session, todo_id: int):
#     todo = get_todo(db, todo_id)
#     if todo:
#         db.delete(todo)
#         db.commit()
#         return True
#     return False

def soft_delete_todo(db:Session,todo_id:int):
    todo=db.query(Todo).filter(Todo.id==todo_id).first()
    if not todo:
        return False
    
    todo.deleted_at=datetime.now()
    db.commit()
    return True

#Search

def search_todo(db: Session, query: str):
    return db.query(Todo).filter(Todo.name_todo.ilike(f"%{query}%"),Todo.deleted_at==None).all()
