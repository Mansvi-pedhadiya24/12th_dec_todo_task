from pydantic import BaseModel


class TodoCreate(BaseModel):
    name_todo: str
    status:int=1

class TodoResponse(BaseModel):
    id: int
    name_todo: str
    status:int = 1

    model_config = {"from_attributes": True}
   
class TodoUpdate(BaseModel):
    name_todo:str | None = None
    status:int | None=None

# class Config:
#         orm_mode = True


