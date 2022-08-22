import logging
import pytest
from asgi_lifespan import LifespanManager
from async_asgi_testclient import TestClient
from fastapi import (
    FastAPI,
)
from services.main import factory
from misc import (
    db,
)

logger = logging.getLogger(__name__)


@pytest.fixture
async def app():
    instance = factory()
    async with LifespanManager(instance):
        yield instance


@pytest.fixture
async def client(app: FastAPI):
    return TestClient(app)


@pytest.fixture
async def db_pool(app: FastAPI):
    return app.state.db_pool


@pytest.fixture
async def resetdb(db_pool: db.Connection):
    await db_pool.execute('TRUNCATE data CASCADE')
