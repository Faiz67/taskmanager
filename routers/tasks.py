from fastapi import APIRouter, HTTPException, Request

from models.tasks import Task, BaseTask
from internal.logic import (
    get_all_tasks,
    add_new_task,
    edit_existing_task,
    delete_existing_task,
    get_task_details,
)
from internal.auth import is_authenticated

tasks = APIRouter()


@tasks.get("", response_model=list[Task])
@is_authenticated
async def get_tasks(
    request: Request, limit: int = 10, page: int = 1, show_completed: bool = False
):
    try:
        user_id = get_tasks.user_info["id"]
        tasks_list = await get_all_tasks(user_id, limit, page, show_completed)
        return tasks_list

    except HTTPException as http_execption:
        raise http_execption

    except Exception as e:
        raise HTTPException(500, e)


@tasks.get("/{id}")
@is_authenticated
async def task_details(request: Request, id: int):
    try:
        user_id = task_details.user_info["id"]
        task_obj = await get_task_details(id, user_id)
        return task_obj

    except HTTPException as http_execption:
        raise http_execption

    except Exception as e:
        raise HTTPException(500, e)


@tasks.post("")
@is_authenticated
async def add_task(request: Request, task: BaseTask):
    try:
        user_id = add_task.user_info["id"]
        task_dict = task.model_dump()
        task_dict.update({"userid": user_id})
        tasks_list = await add_new_task(task_dict)
        return tasks_list

    except Exception as e:
        raise HTTPException(500, e)


@tasks.put("/{id}")
@is_authenticated
async def edit_task(request: Request, task: BaseTask, id: int):
    try:
        user_id = edit_task.user_info["id"]
        task_dict = task.model_dump()
        task_dict.update({"id": id, "userid": user_id})
        tasks_list = await edit_existing_task(task_dict)
        return tasks_list

    except Exception as e:
        raise HTTPException(500, e)


@tasks.delete("/{id}")
@is_authenticated
async def delete_task(request: Request, id: int):
    try:
        user_id = delete_task.user_info["id"]
        tasks_list = await delete_existing_task(id, user_id)
        return tasks_list

    except Exception as e:
        raise HTTPException(500, e)
