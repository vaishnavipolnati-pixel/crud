"""
DATABASE MODELS (ORM)
====================
SQLAlchemy models define the structure of our database tables.

Key Concepts:
- Models are Python classes that map to database tables
- Columns define table fields with types and constraints
- Relationships define connections between tables (not used here, but important for larger apps)

This project: Task Management Application
- Each Task has: id, title, description, completed status, timestamps
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from datetime import datetime
from .database import Base


class Task(Base):
    """
    Task Model
    
    Maps to 'tasks' table in SQLite database.
    Each row represents one task item.
    
    Fields:
    - id: Unique identifier (Primary Key)
    - title: Task title (required)
    - description: Detailed description
    - completed: Boolean flag (True = done, False = pending)
    - created_at: Timestamp when created (auto-set)
    - updated_at: Timestamp when last modified (auto-updated)
    """
    
    __tablename__ = "tasks"

    # Primary Key: Unique identifier for each task
    id = Column(Integer, primary_key=True, index=True)
    
    # Business Logic Fields
    title = Column(String(200), nullable=False, index=True)  # Indexed for faster searches
    description = Column(Text, nullable=True)  # Optional detailed description
    completed = Column(Boolean, default=False)  # Task status
    
    # Timestamp Fields: Auto-managed by database
    created_at = Column(DateTime, server_default=func.now())  # Set on creation
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())  # Auto-update on changes
    
    def __repr__(self):
        """String representation for debugging"""
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
