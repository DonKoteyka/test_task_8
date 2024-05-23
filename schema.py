import pydantic
from abc import ABC
from typing import Optional


class CreateTask(pydantic.BaseModel):
    '''Класс валидации для создания записей'''
    title: str
    description: str


class UpdateTask(pydantic.BaseModel):
    '''Класс валидации для обновления записей'''
    title: Optional[str]
    description: Optional[str]