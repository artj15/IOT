import pytest

from db import (
    data as db_data,
)
from misc import (
    db,
)
from models import (
    data as model_data,
)


@pytest.fixture
async def data(db_pool: db.Connection) -> list[model_data.Data]:
    data_1 = await db_data.create(
        data=model_data.DataNew(
            filename='data_1.csv',
            data_path='./data/data_1.csv',
        ),
        conn=db_pool,
    )
    data_2 = await db_data.create(
        data=model_data.DataNew(
            filename='data_2.csv',
            data_path='./data/data_2.csv',
        ),
        conn=db_pool,
    )
    data_3 = await db_data.create(
        data=model_data.DataNew(
            filename='data_3.csv',
            data_path='./data/data_3.csv',
        ),
        conn=db_pool,
    )
    return [data_1, data_2, data_3]
