import asyncio
from typing import Generator

import pytest_asyncio
from httpx import AsyncClient

from app.main import app


@pytest_asyncio.fixture(scope='session')
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000/api/v1") as client:
        yield client


@pytest_asyncio.fixture
async def async_client_auth():
    async with AsyncClient(app=app, base_url="http://127.0.0.1/api/v1") as client:
        await client.post(
            "/auth/register",
            json={"username": "test_1", "password": "testtest"},
        )
        response = await client.post(
            "/auth/token",
            data={"username": "test_1", "password": "testtest"},
        )
        token = response.json()["access_token"]
        client.headers["Authorization"] = f"Bearer {token}"
        yield client