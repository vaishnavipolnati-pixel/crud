"""
DATABASE CONFIGURATION
======================
This module sets up the SQLite database connection using SQLAlchemy.

Key Concepts:
- SQLAlchemy ORM: Maps Python classes to database tables
- SQLite: Lightweight, file-based database (perfect for learning)
- Session: Manages database transactions and queries
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path

# Get the directory where this file is located
BASE_DIR = Path(__file__).resolve().parent.parent

# Define database file path
DATABASE_URL = f"sqlite:///{BASE_DIR}/tasks.db"

# Create engine
# - echo=True: Logs all SQL queries (useful for debugging)
# - connect_args: SQLite needs check_same_thread=False for FastAPI async
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Set to True for debugging
)

# SessionLocal: A factory for creating new database sessions
# Each request gets its own session to ensure isolation
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base: Parent class for all ORM models
Base = declarative_base()


def get_db():
    """
    Dependency injection function for FastAPI.
    Provides a database session to route handlers.
    
    Usage in routes:
        @app.get("/tasks")
        def get_tasks(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
