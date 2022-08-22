import asyncio
import logging
from asyncio import Queue

import pandas as pd

from db import (
    data as db_data,
)
from misc import (
    db,
    redis,
)
from models import (
    data as model_data,
)

logger = logging.getLogger(__name__)


class State:
    def __init__(self, db_pool: db.Connection, loop: asyncio.BaseEventLoop, redis_pool: redis.Redis):
        self.loop: asyncio.BaseEventLoop = loop
        self.stopping: bool = False
        self.queue: Queue = Queue()
        self.db_pool: db.Connection = db_pool
        self.redis_pool: redis.Redis = redis_pool
        self.task: asyncio.Task = asyncio.create_task(handler(self))


def init(db_pool: db.Connection, loop: asyncio.BaseEventLoop, redis_pool: redis.Redis) -> State:
    state = State(
        loop=loop,
        db_pool=db_pool,
        redis_pool=redis_pool,
    )
    return state


async def close(state: State):
    state.stopping = True
    await state.queue.put(None)
    if state.task and not state.task.done():
        try:
            await asyncio.wait([state.task], timeout=10)
        except TimeoutError:
            logger.error('Iot app processing task not stopped')
        except asyncio.CancelledError:
            pass
        except:
            logger.exception('Processing task failed')


async def handle_iot(idx: int, instance: State) -> None:
    await instance.queue.put(idx)


async def handler(state: State):
    logger.info('Template processing handler started')
    db_pool = state.db_pool
    queue = state.queue
    while not state.stopping:
        idx = await queue.get()
        if idx is None:
            continue
        async with db_pool.acquire() as conn:
            file = await db_data.get_by_id(
                idx=idx,
                conn=conn,
            )
            await db_data.set_status(
                idx=idx,
                status=model_data.DataStatusEnum.PENDING,
                conn=conn,
            )
            async with conn.transaction():
                df = pd.read_csv(file.data_path, sep=r'\s*,\s*', engine='python')
                df['""col10""'] = df['""col10""'].apply(to_float)
                summ = df['""col10""'].sum()
                await db_data.set_summ(
                    idx=idx,
                    summ=summ,
                    status=model_data.DataStatusEnum.DONE,
                    conn=conn,
                )
        queue.task_done()


def to_float(value):
    value = value.replace('"', '')
    if not value:
        return 0.0
    return float(value)
