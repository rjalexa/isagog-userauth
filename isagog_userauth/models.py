"""
User model definition for SQLAlchemy ORM.

This module defines the User model, which represents the structure of the 'users' table
in the database. The table name is configured via an environment variable. The User model
includes fields for the user's ID, username, email, password, role, and creation timestamp.

Environment Variables:
    USER_TABLE_NAME (str): The name of the table to use for the User model.

Attributes:
    id (int): The primary key of the user.
    username (str): The unique username of the user.
    email (str): The unique email address of the user.
    password (str): The hashed password of the user.
    role (str): The role of the user, defaults to 'basic'.
    created_ts (datetime): The timestamp when the user was created,
    defaults to the current time in UTC.
"""

import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Integer, String

from .base import Base

# Load environment variables
load_dotenv()
USER_TABLE_NAME = os.getenv("USER_TABLE_NAME", "users")


class User(Base):
    """
    SQLAlchemy ORM model for the 'users' table.

    This class defines the structure of the 'users' table in the database
    using SQLAlchemy's declarative base. Each instance of this class
    represents a row in the table.

    Attributes:
        id (int): The primary key of the user.
        username (str): The unique username of the user, with a maximum length of 30 characters.
        email (str): The unique email address of the user, with a maximum length of 120 characters.
        password (str): The hashed password of the user.
        role (str): The role of the user, either 'admin' or 'basic'. Defaults to 'basic'.
        created_ts (datetime): The timestamp when the user was created, defaults to
                               the current time in UTC.
    """

    __tablename__ = USER_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    email = Column(String(120), unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(String, default="basic")
    created_ts = Column(DateTime, default=lambda: datetime.now(timezone.utc))
