from typing import Any, Mapping

from bson import ObjectId
from decouple import config
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument

from models import Task, TaskCollection, UpdateTask

client = AsyncIOMotorClient(config("MONGODB_URL"))
db = client.get_database("tasks_database")
tasks_collection = db.get_collection("tasks")


async def get_all_tasks() -> TaskCollection:
    return TaskCollection(tasks=await tasks_collection.find().to_list(1000))


async def create_task(task: Task) -> Mapping[str, Any] | None:
    result = await tasks_collection.insert_one(
        task.model_dump(by_alias=True, exclude={"id"})
    )
    return await tasks_collection.find_one({"_id": result.inserted_id})


async def get_task(task_id: ObjectId) -> Mapping[str, Any] | None:
    return await tasks_collection.find_one({"_id": task_id})


async def get_task_by_title(title: str) -> Mapping[str, Any] | None:
    return await tasks_collection.find_one({"title": title})


async def update_task(task_id: ObjectId, data: UpdateTask) -> Mapping[str, Any] | None:
    task_dict = {
        k: v for k, v in data.model_dump(by_alias=True).items() if v is not None
    }
    return await tasks_collection.find_one_and_update(
        {"_id": task_id}, {"$set": task_dict}, return_document=ReturnDocument.AFTER
    )


async def delete_task(task_id: ObjectId) -> bool:
    result = await tasks_collection.delete_one({"_id": task_id})
    return result.deleted_count == 1
