import logging

from fastapi import (
    APIRouter,
    Depends,
)

from db import (
    data as db_data,
)
from misc import (
    db,
    redis,
)
from misc.depends.db import get as get_db
from misc.depends.redis import get as get_redis
from misc.depends.state import get as get_state
from models import (
    data as model_data,
    queue as model_queue,
)
from services.handlers import (
    error_404,
    error_202,
)
from services.iot_app_processing import (
    handle_iot,
    State,
)

router = APIRouter(
    tags=['IOT API']
)
logger = logging.getLogger(__name__)


@router.post('/file', response_model=model_data.DataSuccessResponse)
async def post_file_name(
        filename: str,
        conn: db.Connection = Depends(get_db),
        state: State = Depends(get_state),
):
    file = await db_data.get(
        filename=filename,
        conn=conn,
    )
    if not file:
        return await error_404('File not found.')
    await handle_iot(
        idx=file.id,
        instance=state,
    )
    return model_data.DataSuccessResponse(
        data=file.id
    )


@router.get('/file/{idx}', response_model=model_data.DataModelSuccessResponse)
async def get(
        idx: int,
        conn: db.Connection = Depends(get_db),
        rds: redis.Redis = Depends(get_redis),
):
    result = await db_data.get_done(
        idx=idx,
        conn=conn,
    )
    redis_data = await rds.get(idx.to_bytes(2, byteorder='little'))
    if redis_data:
        return model_data.DataModelSuccessResponse(
            data=redis_data,
        )
    if not result:
        return await error_404('Data not found.')
    if result.status != model_data.DataStatusEnum.DONE:
        return await error_202('File not ready.')
    await rds.set(
        name=idx.to_bytes(2, byteorder='little'),
        value=result.json(),
        ex=3600,
    )
    return model_data.DataModelSuccessResponse(
        data=result,
    )


@router.get('/len', response_model=model_queue.QueueSizeSuccessResponse)
async def post_file_name(
        state: State = Depends(get_state),
):
    return model_queue.QueueSizeSuccessResponse(
        data=state.queue.qsize(),
    )
