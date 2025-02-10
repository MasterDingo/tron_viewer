import os
from typing import AsyncIterator
import logging

from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from .settings import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_async_engine(settings.database_url, echo=True)

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")

async def drop_test_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
        logger.info("Test database dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping test database: {e}")

async def get_session() -> AsyncIterator[AsyncSession]:
    async with engine.begin():
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            yield session
