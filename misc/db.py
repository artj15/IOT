import logging
from typing import (
    Union,
    Type,
    Optional
)

import asyncpg
from pydantic import (
    BaseModel,
)

logger = logging.getLogger(__name__)
Connection = asyncpg.Connection


async def init(config: dict) -> asyncpg.Pool:
    dsn = config.get('dsn')
    if not dsn:
        raise RuntimeError('DB connection parameters not defined')
    return await asyncpg.create_pool(
        dsn,
        **{k: v for k, v in config.items() if k != 'dsn'}
    )


async def close(db: Union[asyncpg.Pool, asyncpg.Connection]):
    await db.close()


def record_to_model(model_cls: Type[BaseModel], record: Optional[asyncpg.Record]) -> Union[BaseModel, None]:
    if record:
        return model_cls.parse_obj(record)
    return
