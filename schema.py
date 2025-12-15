from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class TodoCreate(BaseModel):
    name_todo: str
    status:int=1

# class TodoResponse(BaseModel):
#     id: int
#     name_todo: str
#     status:int = 1

#     model_config = {"from_attributes": True}
   
class TodoUpdate(BaseModel):
    name_todo:str | None = None
    status:int | None=None

# class Config:
#         orm_mode = True

class TodoResponse(BaseModel):
    id:int
    name_todo:str
    status:int
    created_at:datetime

    class  Config:
        from_attributes= True


class TodoListResponse(BaseModel):
    status: bool
    message:str
    total_pages:int
    current_page:int
    search:Optional[str]
    data:List[TodoResponse]

