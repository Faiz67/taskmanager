"""
Task Management Logic

This module provides core logic for managing tasks, including CRUD operations for tasks in the database.

Functions:
- get_all_tasks(userid): Retrieve all tasks for a user.
- get_task_details(id, userid): Retrieve details of a specific task for a user.
- add_new_task(task_details): Add a new task for a user.
- edit_existing_task(task_details): Edit an existing task for a user.
- delete_existing_task(id, userid): Delete a task for a user.

Dependencies:
- FastAPI for HTTP exception handling.
- PostgreSQL for persistent task data storage.
- internal.db for database connection management.
- models.tasks for task data models.
"""

from fastapi import HTTPException

from models.tasks import Task
from internal.db import connection


async def get_all_tasks(userid, limit=10, page=1, show_only_completed=False):
    """
    Retrieve all tasks for a given user.
    Args:
        userid (int): The ID of the user whose tasks are to be fetched.
    Returns:
        list: A list of task records for the user.
    Raises:
        HTTPException: If a database error occurs.
    """
    try:
        with connection() as conn:
            query = "SELECT * FROM tasks WHERE userid=%(userid)s"
            if (
                show_only_completed
            ):  # If show_only_completed is False, filter out completed tasks
                query += " AND completed = true"
            query += " LIMIT %(limit)s OFFSET %(offset)s"

            cur = conn.execute(
                query,
                {"userid": userid, "limit": limit, "offset": (page - 1) * limit},
            ).fetchall()
            return cur
    except Exception as e:
        print(e)
        raise HTTPException(500, e)


async def get_task_details(id, userid):
    """
    Retrieve details of a specific task for a user.
    Args:
        id (int): The ID of the task.
        userid (int): The ID of the user.
    Returns:
        dict: The task record if found.
    Raises:
        HTTPException: If the task is not found or a database error occurs.
    """
    try:
        with connection() as conn:
            cur = conn.execute(
                "SELECT * FROM tasks where id=%(id)s AND userid=%(userid)s",
                params={"id": id, "userid": userid},
            ).fetchone()

            if not cur:
                raise HTTPException(404, f"Task with id {id} not found")
            return cur
    except Exception as e:
        print(e)
        raise


async def add_new_task(task_details):
    """
    Add a new task for a user.
    Args:
        task_details (dict): The details of the task to add (title, description, userid).
    Returns:
        str: Success message with the new task ID.
    Raises:
        Exception: If a database error occurs.
    """
    with connection() as conn:
        try:
            query = "INSERT INTO tasks (title, description, userid) VALUES (%(title)s, %(description)s, %(userid)s) RETURNING id"

            curr = conn.execute(query, params=task_details).fetchone()
            conn.commit()
            if curr and "id" in curr:
                return f"Task successfully created with id={curr['id']}"
            else:
                return "Task successfully created, but could not retrieve ID."
        except Exception as e:
            print("Some error occured", e)
            raise e


async def edit_existing_task(task_details):
    """
    Edit an existing task for a user.
    Args:
        task_details (dict): The updated details of the task (id, title, description, userid).
    Returns:
        str: Success message if the update is successful.
    Raises:
        Exception: If a database error occurs.
    """
    with connection() as conn:
        try:
            query = "UPDATE tasks set title=%(title)s, description=%(description)s, updated_at=now() WHERE id=%(id)s and userid=%(userid)s"

            conn.execute(query, params=task_details)
            conn.commit()

            return "Task Updated Successfully"
        except Exception as e:
            print("Some error occured", e)
            raise


async def delete_existing_task(id, userid):
    """
    Delete a task for a user.
    Args:
        id (int): The ID of the task to delete.
        userid (int): The ID of the user.
    Returns:
        str: Success message if the deletion is successful.
    Raises:
        Exception: If a database error occurs.
    """
    with connection() as conn:
        try:
            query = "DELETE FROM tasks WHERE id=%(id)s AND userid=%(userid)s"

            conn.execute(query, params={"id": id, "userid": userid})
            conn.commit()

            return "Task Deleted Successfully"
        except Exception as e:
            print("Some error occured", e)
            raise
