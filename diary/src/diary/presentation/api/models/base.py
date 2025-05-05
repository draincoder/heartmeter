from enum import Enum
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

TData = TypeVar("TData")


class Status(str, Enum):
    success = "success"
    error = "error"


class Response(BaseModel):
    status: Status
    message: str | None = None

    class Config:
        frozen = True


class SuccessResponse(Response, Generic[TData]):
    status: Status = Status.success
    data: TData | None = None


class ErrorResponse(Response):
    status: Status = Status.error


class SuccessListResponse(Response, Generic[TData]):
    data: list[TData]
    status: Status = Status.success


class ValidationData(BaseModel):
    message: str
    location: Any


class ValidationErrorResponse(BaseModel):
    status: Status = Status.error
    errors: list[ValidationData] = Field(default_factory=list)
