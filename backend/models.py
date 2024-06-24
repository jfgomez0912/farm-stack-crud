from typing import Annotated

from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class Task(BaseModel):
    id: PyObjectId | None = Field(alias="_id", default=None)
    title: str
    description: str | None = None
    completed: bool = False
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class UpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )


class TaskCollection(BaseModel):
    """
    A container holding a list of `Task` instances.

    This exists because providing a top-level array in a JSON response
    can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    tasks: list[Task]
