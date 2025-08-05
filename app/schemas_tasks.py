from pydantic import BaseModel

#Basic Task info used for user (Creation and update)
class TaskBase(BaseModel):
    title: str
    description:str = ""

# Task creation schema
class TaskCreate(TaskBase):
    pass

# Task update schema (same as create)
class TaskUpdate(TaskBase):
    pass

# Task response schema (includes DB fields)
class TaskOut(TaskBase):
    id: int
    owner_id: int

    # Allows reading SQLAlchemy objects as dictionaries
    class Config:
        orm_mode = True 