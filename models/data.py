import datetime
from enum import (
    Enum,

)

from pydantic import (
    BaseModel,
    Field,
)

from models.base import (
    SuccessResponse,
)


class DataStatusEnum(str, Enum):
    ADD = 'add'
    PENDING = 'pending'
    DONE = 'done'


class DataNew(BaseModel):
    filename: str
    data_path: str
    status: DataStatusEnum = DataStatusEnum.ADD


class Data(BaseModel):
    id: int
    filename: str
    data_path: str
    status: DataStatusEnum
    summ: float = None
    ctime: datetime.datetime = Field(None)
    atime: datetime.datetime = Field(None)
    dtime: datetime.datetime = Field(None)


class DataSuccessResponse(SuccessResponse):
    data: int


class DataModelSuccessResponse(SuccessResponse):
    data: Data
