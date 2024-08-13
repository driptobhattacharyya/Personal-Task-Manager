from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    tasks = relationship("Task", back_populates="assigned_to")

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    due_date = Column(DateTime)
    status = Column(String(50), nullable=False, default="pending")
    assigned_to_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    dependencies = relationship("TaskDependency", back_populates="task")
    assigned_to = relationship("User", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")

class TaskDependency(Base):
    __tablename__ = 'task_dependencies'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    depends_on_task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    task = relationship("Task", foreign_keys=[task_id], back_populates="dependencies")
    depends_on_task = relationship("Task", foreign_keys=[depends_on_task_id])
