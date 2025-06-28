from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class BaseTask(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    completed: Optional[bool] = False


class Task(BaseTask):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
