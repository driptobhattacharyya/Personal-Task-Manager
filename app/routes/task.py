from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app import database
from app.models.models import Task, TaskDependency
from app.crud import task_crud, task_dependency_crud
from app.models import schemas

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = task_crud.create_task(db=db, task=task)
    if db_task:
        return db_task
    raise HTTPException(status_code=400, detail="Task creation failed")

@router.get("/tasks/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_crud.get_task(db=db, task_id=task_id)
    if db_task:
        return db_task
    raise HTTPException(status_code=404, detail="Task not found")

@router.get("/tasks/", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = task_crud.get_tasks(db=db, skip=skip, limit=limit)
    return tasks

@router.put("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task: schemas.UpdateTask, db: Session = Depends(get_db)):
    db_task = task_crud.update_task(db=db, task_id=task_id, task=task)
    if db_task:
        return db_task
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/tasks/{task_id}", response_model=schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_crud.delete_task(db=db, task_id=task_id)
    if db_task:
        return db_task
    raise HTTPException(status_code=404, detail="Task not found")

@router.post("/task_dependencies/", response_model=schemas.TaskDependency)
def create_task_dependency(task_dependency: schemas.TaskDependencyCreate, db: Session = Depends(get_db)):
    db_task_dependency = task_dependency_crud.create_task_dependency(db=db, task_dependency=task_dependency)
    if db_task_dependency:
        return db_task_dependency
    raise HTTPException(status_code=400, detail="Task Dependency creation failed")

@router.get("/task_dependencies/{task_id}", response_model=List[schemas.TaskDependency])
def read_task_dependencies(task_id: int, db: Session = Depends(get_db)):
    task_dependencies = task_dependency_crud.get_task_dependencies(db=db, task_id=task_id)
    return task_dependencies
