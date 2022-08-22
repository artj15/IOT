from fastapi import (
    FastAPI,
    APIRouter,
)

from . import data


def register_routers(app: FastAPI):
    router = APIRouter(
        prefix='/api/v1'
    )
    router.include_router(
        router=data.router
    )
    app.include_router(
        router=router
    )
    return app
