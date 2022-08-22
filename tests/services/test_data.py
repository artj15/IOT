import asyncio
import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_data_error(resetdb, client, data):
    result = await client.post('/api/v1/file', query_string={'filename': 'data.csv'})
    assert result.status_code == 404, f'Error with send file name {result.text=}'
    assert result.json()['error'] == 'File not found.'


@pytest.mark.asyncio
async def test_data_done(resetdb, client, data, db_pool):
    result = await client.post('/api/v1/file', query_string={'filename': 'data_1.csv'})
    assert result.status_code == 200, f'Error with send file name {result.text=}'
    assert result.json()['data'] == data[0].id
    result_data = await client.get(f'/api/v1/file/{data[0].id}')
    if result_data.status_code != 200:
        for i in range(10):
            result_data = await client.get(f'/api/v1/file/{data[0].id}')
            if result_data.status_code == 200:
                break
            await asyncio.sleep(i * 2)
    assert result_data.status_code == 200, f'Error with send file name {result.text=}'
    assert result_data.json()['data']['status'] == 'done'
    assert result_data.json()['data']['summ'] == 85.5182181544557


@pytest.mark.asyncio
async def test_data_len_queue(resetdb, client, data):
    result = await client.post('/api/v1/file', query_string={'filename': 'data_1.csv'})
    assert result.status_code == 200, f'Error with send file name {result.text=}'
    result = await client.post('/api/v1/file', query_string={'filename': 'data_2.csv'})
    assert result.status_code == 200, f'Error with send file name {result.text=}'
    result = await client.post('/api/v1/file', query_string={'filename': 'data_3.csv'})
    assert result.status_code == 200, f'Error with send file name {result.text=}'
    result = await client.get('/api/v1/len')
    assert result.status_code == 200, f'Error with get queue size {result.text=}'
    assert result.json()['data'] == 2
