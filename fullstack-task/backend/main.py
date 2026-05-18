"""
FASTAPI MAIN APPLICATION
========================
This is the main FastAPI application with all REST API endpoints.

Key Concepts:
- FastAPI: Modern web framework for building APIs
- Routes: URL paths that handle HTTP requests
- Dependency Injection: get_db provides database session to routes
- HTTP Methods: GET (read), POST (create), PUT/PATCH (update), DELETE (delete)

REST API Best Practices:
- Use nouns for resources: /api/tasks (not /api/getTasks)
- Use HTTP methods for actions: GET, POST, PUT, DELETE
- Status codes: 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found), 500 (Server Error)
- Error responses: Include error messages and status codes
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pathlib import Path

# Import our modules
from .database import Base, engine, get_db
from .models import Task
from .schemas import (
    TaskCreate, TaskResponse, TaskUpdate, TaskListResponse, ErrorResponse
)
from . import crud

# Initialize FastAPI app
app = FastAPI(
    title="Task Manager API",
    description="A learning project for full-stack development",
    version="1.0.0"
)

# ==================== DATABASE SETUP ====================

# Create all tables on startup
# (In production, use Alembic for migrations)
@app.on_event("startup")
def startup():
    """
    Runs on application startup.
    Creates database tables if they don't exist.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized")


# ==================== CORS CONFIGURATION ====================

# CORS: Cross-Origin Resource Sharing
# Allows frontend (running on different port) to make API calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("✅ CORS enabled for frontend integration")


# ==================== ROUTES ====================

# Health Check
@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    Use this to verify API is running.
    """
    return {"status": "healthy", "message": "API is running"}


# ==================== TASK ENDPOINTS ====================

# GET ALL TASKS
@app.get("/api/tasks", response_model=TaskListResponse, tags=["Tasks"])
def get_tasks(
    skip: int = 0,
    limit: int = 100,
    completed: bool | None = None,
    db: Session = Depends(get_db)
):
    """
    Get all tasks with optional filtering.
    
    Query Parameters:
    - skip: Number of tasks to skip (pagination)
    - limit: Maximum number of tasks to return
    - completed: Filter by status (true/false)
    
    Returns:
    - total: Total number of tasks
    - tasks: List of Task objects
    
    Example: GET /api/tasks?skip=0&limit=10
    """
    if completed is not None:
        tasks = crud.get_tasks_by_status(db, completed)
    else:
        tasks = crud.get_all_tasks(db, skip=skip, limit=limit)
    
    return {
        "total": crud.count_tasks(db),
        "tasks": tasks
    }


# GET SINGLE TASK
@app.get("/api/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Get a specific task by ID.
    
    Path Parameter:
    - task_id: The ID of the task
    
    Returns:
    - Task object
    
    Errors:
    - 404: Task not found
    
    Example: GET /api/tasks/1
    """
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


# CREATE TASK
@app.post("/api/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["Tasks"])
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.
    
    Request Body (JSON):
    {
        "title": "My Task",
        "description": "Task description (optional)",
        "completed": false
    }
    
    Returns:
    - Created Task object with id and timestamps
    
    Status Code:
    - 201: Task created successfully
    
    Example: POST /api/tasks
    """
    # Validation happens automatically via Pydantic schema
    created_task = crud.create_task(db=db, task=task)
    return created_task


# UPDATE TASK
@app.put("/api/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update an existing task.
    
    Path Parameter:
    - task_id: The ID of the task to update
    
    Request Body (JSON) - All fields optional:
    {
        "title": "Updated title",
        "description": "Updated description",
        "completed": true
    }
    
    Returns:
    - Updated Task object
    
    Errors:
    - 404: Task not found
    
    Example: PUT /api/tasks/1
    """
    updated_task = crud.update_task(db, task_id, task_update)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return updated_task


# DELETE TASK
@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task.
    
    Path Parameter:
    - task_id: The ID of the task to delete
    
    Status Code:
    - 204: Task deleted successfully (no content in response)
    
    Errors:
    - 404: Task not found
    
    Example: DELETE /api/tasks/1
    """
    success = crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return None


# ==================== STATISTICS ENDPOINT ====================

@app.get("/api/stats", tags=["Statistics"])
def get_stats(db: Session = Depends(get_db)):
    """
    Get task statistics.
    
    Returns:
    - total_tasks: Total number of tasks
    - completed_tasks: Number of completed tasks
    - pending_tasks: Number of pending tasks
    """
    total = crud.count_tasks(db)
    completed = crud.count_completed_tasks(db)
    pending = total - completed
    
    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "completion_percentage": round((completed / total * 100) if total > 0 else 0, 2)
    }


# ==================== DOCUMENTATION ====================

if __name__ == "__main__":
    """
    To run this application:
    
    1. Install dependencies:
       pip install -r requirements.txt
    
    2. Run the server:
       python -m uvicorn backend.main:app --reload
    
    3. Access the API:
       - HTTP API: http://localhost:8000
       - Swagger UI (Interactive docs): http://localhost:8000/docs
       - ReDoc (Alternative docs): http://localhost:8000/redoc
    
    The --reload flag enables auto-restart when code changes (development only).
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
