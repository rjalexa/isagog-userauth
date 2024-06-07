"""
Custom exceptions for the FastAPI application.

This module defines custom HTTP exceptions used throughout the FastAPI application.
These exceptions provide more specific error handling for common scenarios such as
missing authentication tokens and insufficient permissions.

Classes:
    MissingTokenException: Exception raised when no JWT token is provided.
    ForbiddenException: Exception raised when a user lacks sufficient permissions.

Example usage:
    if not token:
        raise MissingTokenException()

    if not user.has_permission(resource):
        raise ForbiddenException()
"""

from fastapi import HTTPException, status


class MissingTokenException(HTTPException):
    """
    Exception raised when no JWT token is provided in the request.

    This exception is used to indicate that the authentication token is missing,
    which is required for accessing protected resources.

    Inherits from:
    HTTPException: FastAPI's HTTPException class.

    Attributes:
    status_code (int): HTTP status code for the response.
    detail (str): Description of the error.

    Example:
    ```
    if not token:
        raise MissingTokenException()
    ```
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token."
        )


class ForbiddenException(HTTPException):
    """
    Exception raised when a user does not have sufficient permissions to access a resource.

    This exception is used to indicate that the user is authenticated but does not
    have the necessary permissions to perform the requested action.

    Inherits from:
    HTTPException: FastAPI's HTTPException class.

    Attributes:
    status_code (int): HTTP status code for the response.
    detail (str): Description of the error.

    Example:
    ```
    if not user.has_permission(resource):
        raise ForbiddenException()
    ```
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions."
        )
