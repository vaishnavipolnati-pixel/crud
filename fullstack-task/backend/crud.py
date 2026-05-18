"""
CRUD OPERATIONS
==============
CRUD stands for: Create, Read, Update, Delete
These functions encapsulate all database operations.

Key Concepts:
- Separation of concerns: Database logic separate from API logic
- Reusability: CRUD functions can be used from multiple places
- Testability: Easy to test database operations independently
- SQLAlchemy Session: Manages transactions and queries
"""

from sqlalchemy.orm import Session
from .models import Task
from .schemas import TaskCreate, TaskUpdate


# ==================== CREATE ====================

def create_task(db: Session, task: TaskCreate) -> Task:
    """
    Create a new task in the database.
    
    Args:
        db: Database session
        task: TaskCreate schema with task data
        
    Returns:
        Created Task model instance
        
    Process:
    1. Create Task instance from schema
    2. Add to database session
    3. Commit changes (save to database)
    4. Refresh to get auto-generated fields (id, timestamps)
    """
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)  # Get id and timestamps from database
    return db_task


# ==================== READ ====================

def get_task(db: Session, task_id: int) -> Task | None:
    """
    Retrieve a single task by ID.
    
    Args:
        db: Database session
        task_id: Task ID to find
        
    Returns:
        Task model or None if not found
    """
    return db.query(Task).filter(Task.id == task_id).first()


def get_all_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[Task]:
    """
    Retrieve all tasks with pagination.
    
    Args:
        db: Database session
        skip: Number of tasks to skip (for pagination)
        limit: Maximum number of tasks to return
        
    Returns:
        List of Task models
        
    Pagination:
    - skip=0, limit=10: First 10 tasks
    - skip=10, limit=10: Next 10 tasks
    - Important for performance with large datasets
    """
    return db.query(Task).offset(skip).limit(limit).all()


def get_tasks_by_status(db: Session, completed: bool) -> list[Task]:
    """
    Retrieve tasks filtered by completion status.
    
    Args:
        db: Database session
        completed: Filter by completion status
        
    Returns:
        List of Task models matching the filter
    """
    return db.query(Task).filter(Task.completed == completed).all()


# ==================== UPDATE ====================

def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Task | None:
    """
    Update an existing task.
    
    Args:
        db: Database session
        task_id: Task ID to update
        task_update: TaskUpdate schema with fields to update
        
    Returns:
        Updated Task model or None if not found
        
    Process:
    1. Find task in database
    2. Update only fields that are provided (not None)
    3. Commit changes
    4. Refresh to get updated_at timestamp
    """
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    
    # Update only provided fields
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


# ==================== DELETE ====================

def delete_task(db: Session, task_id: int) -> bool:
    """
    Delete a task from the database.
    
    Args:
        db: Database session
        task_id: Task ID to delete
        
    Returns:
        True if deleted, False if task not found
        
    Process:
    1. Find task
    2. Delete from session
    3. Commit changes
    """
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True


# ==================== UTILITY ====================

def count_tasks(db: Session) -> int:
    """Get total number of tasks"""
    return db.query(Task).count()


def count_completed_tasks(db: Session) -> int:
    """Get number of completed tasks"""
    return db.query(Task).filter(Task.completed == True).count()


def delete_all_tasks(db: Session) -> int:
    """
    Delete all tasks (useful for testing/reset).
    
    Returns:
        Number of deleted tasks
    """
    count = db.query(Task).count()
    db.query(Task).delete()
    db.commit()
    return count
