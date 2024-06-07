"""
Authentication and security utility functions.

This module provides utility functions for password hashing, token creation,
and user authentication using JWT. It includes functions for verifying passwords,
creating access and refresh tokens, and retrieving the current user and admin user
from the token.

Environment Variables:
    BCRYPT_PEPPER (str): A secret string added to passwords before hashing.
    JWT_SECRET (str): The secret key used to encode and decode JWT tokens.
    ACCESS_TOKEN_LIFETIME (int): The lifetime of an access token in minutes.
    REFRESH_TOKEN_LIFETIME (int): The lifetime of a refresh token in days.

Functions:
    verify_password(plain_password, hashed_password): Verify a password against its hash.
    get_password_hash(password): Hash a password using bcrypt with a pepper.
    create_access_token(data, expires_delta): Create a JWT access token.
    create_refresh_token(data): Create a JWT refresh token.
    get_current_user(token, db): Retrieve the current user from the JWT token.
    get_admin_user(current_user): Ensure the current user has admin privileges.
"""

from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import (
    BCRYPT_PEPPER,
    JWT_SECRET,
    ACCESS_TOKEN_LIFETIME,
    REFRESH_TOKEN_LIFETIME,
)
from .db_session import get_db
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


def verify_password(plain_password, hashed_password):
    """
    Verify a password against its hash.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(BCRYPT_PEPPER + plain_password, hashed_password)


def get_password_hash(password):
    """
    Hash a password using bcrypt with a pepper.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(BCRYPT_PEPPER + password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT access token.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta, optional): The lifetime of the token.
        Defaults to ACCESS_TOKEN_LIFETIME minutes.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_LIFETIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
    return encoded_jwt


def create_refresh_token(data: dict):
    """
    Create a JWT refresh token.

    Args:
        data (dict): The data to encode in the token.

    Returns:
        str: The encoded JWT token.
    """
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_LIFETIME)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Retrieve the current user from the JWT token.

    Args:
        token (str): The JWT token.
        db (Session): The database session.

    Returns:
        User: The user object corresponding to the token.

    Raises:
        HTTPException: If the token is invalid or has expired.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(User).filter(User.id == payload["id"]).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=401, detail="Token has expired") from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc


def get_admin_user(current_user: User = Depends(get_current_user)):
    """
    Ensure the current user has admin privileges.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        User: The current user if they have admin privileges.

    Raises:
        HTTPException: If the current user does not have admin privileges.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
