import pydantic
from abc import ABC
from typing import Optional


class CreateTask(pydantic.BaseModel):
    title: str
    description: str


class UpdateTask(pydantic.BaseModel):
    title: Optional[str]
    description: Optional[str]