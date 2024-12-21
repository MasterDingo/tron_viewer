import pytest
from unittest.mock import AsyncMock
from decimal import Decimal

from httpx import ASGITransport, AsyncClient

from ..main import app, lifespan
from ..db import get_session, init_db, drop_test_db


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def test_db():
    await init_db()
    yield
    await drop_test_db()


@pytest.fixture
async def db_session():
    async for sess in get_session():
        yield sess


@pytest.fixture
async def client(monkeypatch):
    monkeypatch.setattr(
        "tronpy.async_tron.AsyncTron.get_bandwidth", AsyncMock(return_value=100)
    )
    monkeypatch.setattr(
        "tronpy.async_tron.AsyncTron.get_energy", AsyncMock(return_value=6000)
    )
    monkeypatch.setattr(
        "tronpy.async_tron.AsyncTron.get_account_balance",
        AsyncMock(return_value=Decimal(2)),
    )
    async with lifespan(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            yield client
