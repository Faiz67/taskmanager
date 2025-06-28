"""
Authentication and User Management Utilities

This module provides functions for user registration, authentication, token management, and session handling using FastAPI, PostgreSQL, and Redis.

Functions:
- insert_in_redis(user_details): Stores user details in Redis with a generated token as the key.
- register_user(user_details): Registers a new user in the PostgreSQL database.
- authenticate_user(login_details): Authenticates a user and returns a session token if successful.
- get_token_details(token): Retrieves user details from Redis using the session token.
- is_authenticated(func): Decorator to enforce authentication on FastAPI endpoints.

Dependencies:
- FastAPI for HTTP exception handling and request context.
- PostgreSQL for persistent user data storage.
- Redis for session and token management.
- JSON for serialization of user data.
- internal.db for database and token utility functions.
"""

from fastapi import HTTPException, Request
import json
from functools import wraps

from internal.db import connection, redis_connection, generate_token, is_token_valid


async def insert_in_redis(user_details):
    """
    Stores user details in Redis with a generated token as the key.
    The token is set to expire in 1 hour (3600 seconds).
    Args:
        user_details (dict): The user information to store.
    Returns:
        str: The generated session token.
    Raises:
        Exception: If an error occurs during Redis operation or token generation.
    """
    with redis_connection() as r:
        try:
            token = await generate_token(user_details)
            r.set(token.lower(), json.dumps(user_details, default=str), ex=3600)
            return token
        except Exception as e:
            print("An error occured", e)
            raise


async def register_user(user_details):
    """
    Registers a new user in the PostgreSQL database.
    Args:
        user_details (dict): The user information to insert (user_name, email_id, password).
    Raises:
        Exception: If an error occurs during database operation.
    """
    with connection() as conn:
        try:
            query = "INSERT INTO users (user_name, email_id, password) VALUES (%(user_name)s, %(email_id)s, %(password)s)"
            conn.execute(query, user_details)
            conn.commit()

        except Exception as e:
            print("An error occured", e)
            raise


async def authenticate_user(login_details):
    """
    Authenticates a user by verifying credentials against the database.
    If valid, generates and stores a session token in Redis.
    Args:
        login_details (dict): The login credentials (user_name, password).
    Returns:
        str: The session token if authentication is successful.
    Raises:
        HTTPException: If credentials are invalid.
        Exception: For other errors during authentication.
    """
    with connection() as conn:
        try:
            query = "SELECT * FROM users WHERE user_name=%(user_name)s AND password=%(password)s"
            user_row = conn.execute(query, login_details).fetchone()

            if not user_row:
                raise HTTPException(403, "Invalid Username/Password!")

            cookie_token = await insert_in_redis(user_row)

            return cookie_token
        except Exception as e:
            print("An error occured", e)
            raise


async def get_token_details(token: str):
    """
    Retrieves user details from Redis using the session token.
    Args:
        token (str): The session token.
    Returns:
        dict: The user information if token is valid.
    Raises:
        HTTPException: If the token is expired or not found.
    """
    with redis_connection() as r:
        user_info = r.get(token.lower())
        if not user_info:
            raise HTTPException(401, "Token has expired please relogin!")

        return json.loads(user_info)


def is_authenticated(func):
    """
    Decorator to enforce authentication on FastAPI endpoints.
    Checks for a valid session token in the request cookies and retrieves user info from Redis.
    Args:
        func (Callable): The endpoint function to wrap.
    Returns:
        Callable: The wrapped function with authentication enforced.
    Raises:
        HTTPException: If the user is unauthorized or token is invalid.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(args, kwargs)
        request: Request = kwargs.get("request")
        current_session = request.cookies.get("x-session-token")
        print("Current Session Token:", current_session)
        if not current_session:
            raise HTTPException(401, "Unauthorized User!")
        if not await is_token_valid(current_session):
            raise HTTPException(401, "Invalid or expired session token!")

        token_details = await get_token_details(current_session)
        wrapper.user_info = token_details
        return await func(*args, **kwargs)

    return wrapper
