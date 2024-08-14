from fastapi import FastAPI
from app.api import tasks, users
from app.core.database import engine
from app.models.models import task, user
from .routes import users, tasks, projects

# Create all database tables (only needed for the first time or in testing environments)
task.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Personal Task Manager",
    description="A task management API for organizations to handle tasks collaboratively.",
    version="1.0.0"
)

# Include routes
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Personal Task Manager API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
