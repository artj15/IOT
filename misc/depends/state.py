import logging

import fastapi

from misc import db

logger = logging.getLogger(__name__)


async def get(request: fastapi.Request) -> db.Connection:
    try:
        return request.app.state
    except AttributeError:
        raise RuntimeError('Application has no state')
