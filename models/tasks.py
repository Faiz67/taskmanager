from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class BaseTask(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str


class Task(BaseTask):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    completed: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
