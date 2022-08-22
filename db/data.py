import logging
from typing import (
    Optional,
)

from misc import (
    db,
)
from models import (
    data as model_data,
)

TABLE = 'data'
logger = logging.getLogger(__name__)


async def create(
        data: model_data.DataNew,
        conn: db.Connection,
) -> Optional[model_data.Data]:
    data = data.dict()
    values = list(data.values())
    query = f'''INSERT INTO {TABLE} ({", ".join(list(data.keys()))}) 
            VALUES ({", ".join([f"${i + 1}" for i in range(len(values))])}) RETURNING *'''
    result = await conn.fetchrow(query, *values)
    return db.record_to_model(model_data.Data, result)


async def get(
        filename: str,
        conn: db.Connection,
) -> Optional[model_data.Data]:
    values = [filename]
    query = f'SELECT * FROM {TABLE} WHERE filename = $1'
    result = await conn.fetchrow(query, *values)
    return db.record_to_model(model_data.Data, result)


async def get_by_id(
        idx: int,
        conn: db.Connection,
) -> Optional[model_data.Data]:
    values = [idx]
    query = f'SELECT * FROM {TABLE} WHERE id = $1'
    result = await conn.fetchrow(query, *values)
    return db.record_to_model(model_data.Data, result)


async def set_status(
        idx: int,
        status: model_data.DataStatusEnum,
        conn: db.Connection,
) -> Optional[model_data.Data]:
    values = [idx, status]
    query = f'UPDATE {TABLE} set status = $2 WHERE id = $1'
    result = await conn.fetchrow(query, *values)
    return db.record_to_model(model_data.Data, result)


async def set_summ(
        idx: int,
        summ: float,
        status: model_data.DataStatusEnum,
        conn: db.Connection,
) -> Optional[model_data.Data]:
    values = [idx, status, summ]
    query = f"UPDATE {TABLE} set summ = $3, status = $2, atime = (NOW() at time zone 'utc') WHERE id = $1"
    result = await conn.fetchrow(query, *values)
    return db.record_to_model(model_data.Data, result)


async def get_done(
        idx: int,
        conn: db.Connection,
) -> Optional[model_data.Data]:
    values = [idx]
    query = f'SELECT * FROM {TABLE} WHERE id = $1'
    result = await conn.fetchrow(query, *values)
    return db.record_to_model(model_data.Data, result)
