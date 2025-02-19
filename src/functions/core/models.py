from enum import Enum

from pydantic import BaseModel


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class TaskCreateModel(BaseModel):
    title: str
    description: str
    status: TaskStatus


class TaskUpdateModel(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None


class TaskGetModel(BaseModel):
    taskId: str
    title: str
    description: str
    status: TaskStatus
