"""
Creates a base class for ORM models using SQLAlchemy's declarative system.

Usage:
    from base import Base
    from sqlalchemy import Column, Integer, String

    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        username = Column(String, unique=True)
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
