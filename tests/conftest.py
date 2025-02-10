import pytest
from unittest.mock import AsyncMock
from decimal import Decimal

from httpx import ASGITransport, AsyncClient

from ..main import app, lifespan
from ..db import get_session, init_db, drop_test_db

"""
This module contains pytest fixtures for testing an application that uses the Tron blockchain.
"""

@pytest.fixture
def anyio_backend():
    """
    Returns the AnyIO backend to use for the tests.

    :return: The AnyIO backend.
    """
    return "asyncio"

@pytest.fixture
def base_url():
    """
    Returns the base URL for the test client.

    :return: The base URL.
    """
    return "http://test"

@pytest.fixture
async def test_db():
    """
    Initializes and yields a test database, then drops it after the tests.

    Raises:
        pytest.fail: If an error occurs during database initialization or dropping.
    """
    try:
        await init_db()
    except Exception as e:
        pytest.fail(f"Error initializing database: {e}")
    yield
    try:
        await drop_test_db()
    except Exception as e:
        pytest.fail(f"Error dropping test database: {e}")


@pytest.fixture
async def db_session():
    """
    Yields an asynchronous database session.

    Yields:
        AsyncSession: An asynchronous database session.
    """
    async for sess in get_session():
        yield sess


@pytest.fixture
async def client(monkeypatch, base_url):
    """
    Returns an asynchronous client with mock responses for bandwidth, energy, and account balance.

    Args:
        monkeypatch (MonkeyPatch): The pytest monkeypatch fixture.
        base_url (str): The base URL for the test client.

    Returns:
        AsyncClient: An asynchronous client.
    """
    async def get_bandwidth(*_args, **_kwargs) -> int:
        return 100

    async def get_energy(*_args, **_kwargs) -> int:
        return 6000

    async def get_account_balance(*_args, **_kwargs) -> Decimal:
        return Decimal(2)

    monkeypatch.setattr("tronpy.async_tron.AsyncTron.get_bandwidth", get_bandwidth)
    monkeypatch.setattr("tronpy.async_tron.AsyncTron.get_energy", get_energy)
    monkeypatch.setattr(
        "tronpy.async_tron.AsyncTron.get_account_balance",
        get_account_balance,
    )
    async with lifespan(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url=base_url
        ) as client:
            yield client
