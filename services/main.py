import asyncio
import logging
import os

from fastapi import (
    FastAPI,
)

from misc import (
    ctrl,
    config,
    db,
    redis,
)
from models.base import (
    ErrorResponse,
    UpdateErrorResponse,
)
from services.handlers import (
    register_exception_handler,
)
from services.iot_app_processing import (
    init as state_init,
    close,
)

logger = logging.getLogger(__name__)


def factory():
    app = ctrl.main_with_parses(main)
    if not app:
        raise RuntimeError
    return app


def main(app_config):
    root_path = app_config.get('rot_path', None)
    app = FastAPI(
        title='Fastapi IOT REST API',
        debug=app_config.get('debug', False),
        root_path=root_path,
        responses=responses(),
    )
    app.config = app_config
    check_folders(app_config)
    register_exception_handler(app)
    register_routers(app)
    register_startup(app)
    register_shutdown(app)
    return app


def register_startup(app):
    @app.on_event("startup")
    async def handler_startup():
        logger.info('Startup called')
        try:
            await startup(app)
            logger.info(f"REST API app startup executed")
        except:
            logger.exception('Startup crashed')


def register_shutdown(app):
    @app.on_event("shutdown")
    async def handler_shutdown():
        logger.info('Shutdown called')
        try:
            await shutdown(app)
            logger.info(f"REST API app shutdown executed")
        except:
            logger.exception('Shutdown crashed')


async def startup(app: FastAPI):
    loop = asyncio.get_event_loop()
    state = state_init(
        loop=loop,
        db_pool=await db.init(app.config['db']),
        redis_pool=await redis.init(app.config['redis']),
    )
    app.state = state
    return app


async def shutdown(app):
    if app.state.db_pool:
        await db.close(app.state.db_pool)
    if app.state.redis_pool:
        await redis.close(app.state.redis_pool)
    if app.state:
        await close(app.state)


def register_routers(app):
    from . import routers
    return routers.register_routers(app)


def check_folders(conf):
    if not os.path.exists(config.template_files_folder(conf)):
        os.makedirs(config.template_files_folder(conf))


def responses():
    return {
        409: {
            "model": UpdateErrorResponse
        },
        400: {
            "model": ErrorResponse
        },
        401: {
            "model": ErrorResponse
        },
        404: {
            "model": ErrorResponse
        },
        422: {
            "model": ErrorResponse
        },
        500: {
            "model": ErrorResponse
        },
    }
