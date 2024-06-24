import asyncio
from typing import Any, Mapping

import bson.errors
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Response, status

import database
from models import Task, TaskCollection, UpdateTask

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get(
    "/",
    response_model=TaskCollection,
    response_model_by_alias=False,
)
async def get_tasks() -> TaskCollection:
    return await database.get_all_tasks()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Task)
async def create_task(task: Task) -> Mapping[str, Any]:
    if await database.get_task_by_title(task.title) is not None:
        raise HTTPException(409, "Task already exists")

    if (response := await database.create_task(task)) is None:
        raise HTTPException(500, "Something went wrong")

    return response


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str) -> Mapping[str, Any]:
    try:
        if (response := await database.get_task(ObjectId(task_id))) is None:
            raise HTTPException(404, "Task not found")

    except bson.errors.InvalidId as exc:
        raise HTTPException(400, "Invalid task id") from exc

    return response


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: str, task: UpdateTask) -> Mapping[str, Any]:
    try:
        if (response := await database.update_task(ObjectId(task_id), task)) is None:
            raise HTTPException(404, "Task not found")

    except bson.errors.InvalidId as exc:
        raise HTTPException(400, "Invalid task id") from exc

    return response


@router.delete("/{task_id}")
async def delete_task(task_id: str) -> Response:
    try:
        if not await database.delete_task(ObjectId(task_id)):
            raise HTTPException(404, "Task not found")

    except bson.errors.InvalidId as exc:
        raise HTTPException(400, "Invalid task id") from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/")
async def delete_tasks() -> Response:
    task_collection = await database.get_all_tasks()
    task_ids = (ObjectId(task.id) for task in task_collection.tasks)

    await asyncio.gather(*map(database.delete_task, task_ids))

    return Response(status_code=status.HTTP_204_NO_CONTENT)
