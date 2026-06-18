import pytest
import os

os.environ['DATABASE_URL'] = 'postgresql+asyncpg://postgres:postgres@localhost:5433/test_products'


from httpx import AsyncClient, ASGITransport
from main import app
from db import engine, Base
from redis_client import redis_client

@pytest.fixture(autouse=True)
async def setup_and_clean_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    await redis_client.aclose()


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac