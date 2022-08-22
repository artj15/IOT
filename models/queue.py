from models.base import (
    SuccessResponse,
)


class QueueSizeSuccessResponse(SuccessResponse):
    data: int
