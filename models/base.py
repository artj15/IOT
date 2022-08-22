from typing import (
    Optional,
    List,
    Any
)

from pydantic import BaseModel


class ValidationError(BaseModel):
    field: str
    message: str


class SuccessResponse(BaseModel):
    success: bool = True
    data: Optional[Any]


class ListData(BaseModel):
    total: int
    limit: int
    page: int
    items: List[Any]


class ErrorResponse(BaseModel):
    success: bool = False
    error: Optional[str]
    validation_error: Optional[List[ValidationError]]
    debug: Optional[str]


class UpdateErrorResponse(BaseModel):
    success: bool = False
    errors: List[Any]
