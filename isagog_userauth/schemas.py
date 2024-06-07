"""
Schema definitions for user-related operations.

This module defines the Pydantic models used for various user-related operations,
such as signup, login, deleting a user, and changing a user's password. These models
are used to validate and serialize/deserialize data in the application.

Classes:
    SignupModel: Schema for user signup requests.
    SignupResponseModel: Schema for user signup responses.
    DeleteUserModel: Schema for user deletion requests.
    PasswordChangeModel: Schema for changing a user's password.
"""

from pydantic import BaseModel, EmailStr, Field


class SignupModel(BaseModel):
    """
    Schema for user signup requests.

    Attributes:
        email (EmailStr): The user's email address.
        username (str): The user's unique username, with a maximum length of 30 characters.
        password (str): The user's password, with a maximum length of 30 characters.
        role (str): The user's role, defaulting to 'basic'.
    """

    email: EmailStr
    username: str = Field(..., max_length=30)
    password: str = Field(..., max_length=30)
    role: str = Field(default="basic")


class SignupResponseModel(BaseModel):
    """
    Schema for user signup responses.

    Attributes:
        email (EmailStr): The user's email address.
        username (str): The user's unique username, with a maximum length of 30 characters.
        role (str): The user's role.
    """

    email: EmailStr
    username: str = Field(..., max_length=30)
    role: str


class DeleteUserModel(BaseModel):
    """
    Schema for user deletion requests.

    Attributes:
        id (int): The ID of the user to be deleted.
    """

    id: int


class PasswordChangeModel(BaseModel):
    """
    Schema for changing a user's password.

    Attributes:
        email (EmailStr): The user's email address.
        new_password (str): The new password for the user, with a maximum length of 30 characters.
    """

    email: EmailStr
    new_password: str = Field(..., max_length=30)
