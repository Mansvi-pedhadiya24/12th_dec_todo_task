from sqlalchemy import Column, String, Integer,DateTime
from db import Base

class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    name_todo = Column(String(50))
    status=Column(Integer,default=1)
    deleted_at=Column(DateTime,nullable=True)
