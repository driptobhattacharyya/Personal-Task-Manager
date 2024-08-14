from sqlalchemy.orm import Session
from . import models, schemas
import datetime

# Create a new task
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        status=task.status,
        project_id=task.project_id,
        assigned_to_id=task.assigned_to_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Get a task by ID
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

# Get all tasks with optional filtering by project, user, or status
def get_tasks(db: Session, project_id: int = None, assigned_to_id: int = None, status: str = None):
    query = db.query(models.Task)
    if project_id:
        query = query.filter(models.Task.project_id == project_id)
    if assigned_to_id:
        query = query.filter(models.Task.assigned_to_id == assigned_to_id)
    if status:
        query = query.filter(models.Task.status == status)
    return query.all()

# Update a task
def update_task(db: Session, task_id: int, task_update: schemas.UpdateTask):
    db_task = get_task(db, task_id)
    if db_task:
        for key, value in task_update.dict(exclude_unset=True).items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

# Delete a task
def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

# Create a task dependency
def create_task_dependency(db: Session, dependency: schemas.TaskDependencyCreate):
    db_dependency = models.TaskDependency(
        task_id=dependency.task_id,
        depends_on_task_id=dependency.depends_on_task_id
    )
    db.add(db_dependency)
    db.commit()
    db.refresh(db_dependency)
    return db_dependency

# Get task dependencies for a task
def get_task_dependencies(db: Session, task_id: int):
    return db.query(models.TaskDependency).filter(models.TaskDependency.task_id == task_id).all()

# Check if a user is available on a specific date for assigning a task
def is_user_available(db: Session, user_id: int, date: datetime):
    tasks = db.query(models.Task).filter(
        models.Task.assigned_to_id == user_id,
        models.Task.due_date == date
    ).all()
    return len(tasks) == 0
