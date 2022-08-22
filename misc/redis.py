import logging

from aioredis import from_url, Redis

logger = logging.getLogger(__name__)


async def init(config: dict) -> Redis:
    dsn = config.get('dsn')
    if not dsn:
        raise RuntimeError('Redis connection parameters not defined')
    maxsize = config.get('maxsize', 10)
    return await from_url(
        url=dsn,
        max_connections=maxsize
    )


async def close(pool: Redis):
    await pool.close()
