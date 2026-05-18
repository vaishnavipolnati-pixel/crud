"""
PYDANTIC SCHEMAS (Data Validation)
==================================
Schemas define the structure and validation rules for API requests/responses.

Key Concepts:
- Pydantic: Data validation library (separate from database models)
- Schemas validate input data and ensure type safety
- Separation of concerns: Database models (database structure) vs Schemas (API contracts)

Why separate from models?
- Frontend might send different data than what's stored
- Validation rules may differ from database constraints
- Response might exclude sensitive fields
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """
    Base schema with common fields.
    Used as parent for Create and Update schemas.
    """
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description")
    completed: bool = Field(False, description="Task completion status")


class TaskCreate(TaskBase):
    """
    Schema for creating a new task.
    Frontend sends this data to POST /api/tasks/
    """
    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating a task.
    Only include fields that can be updated.
    All fields are optional (partial updates).
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """
    Schema for API responses.
    Includes all fields from TaskBase plus metadata.
    """
    id: int = Field(..., description="Unique task identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True  # Allows converting SQLAlchemy models to this schema


class TaskListResponse(BaseModel):
    """Schema for listing multiple tasks"""
    total: int
    tasks: list[TaskResponse]


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    error: str
    detail: Optional[str] = None
