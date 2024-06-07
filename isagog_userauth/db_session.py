"""
Database configuration and session management.

This module sets up the SQLAlchemy engine and session factory for connecting
to the SQLite database specified in the environment variables. It also provides
a function to generate database sessions for use in context managers, ensuring
that sessions are properly closed after use.

Functions:
    get_db(): Generate a database session for use in context managers.

Environment Variables:
    USER_DB_URL (str): The database URL for connecting to the SQLite database.
"""

import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("USER_DB_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Generate a database session for use in context managers.

    This function creates a new SQLAlchemy session and yields it for use
    in database operations. The session is automatically closed after use.

    Yields:
        Session: An SQLAlchemy database session.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
