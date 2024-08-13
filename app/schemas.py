from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = "pending"
    project_id: int
    assigned_to_id: Optional[int] = None

    @validator('due_date', always=True)
    def due_date_not_past(cls, v):
        if v and v < datetime.now():
            raise ValueError('Due date cannot be in the past')
        return v

class TaskCreate(TaskBase):
    pass

class UpdateTask(TaskBase):
    pass

class Task(TaskBase):
    id: int
    dependencies: List[int] = []
    class Config:
        orm_mode = True

class TaskDependencyBase(BaseModel):
    task_id: int
    depends_on_task_id: int

class TaskDependencyCreate(TaskDependencyBase):
    pass

class TaskDependency(TaskDependencyBase):
    id: int
    class Config:
        orm_mode = True
