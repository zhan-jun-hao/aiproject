from typing import Generic, TypeVar
from pydantic import BaseModel


T = TypeVar("T")

class Result(BaseModel, Generic[T]):
    code: int
    msg: str
    data: T | None = None