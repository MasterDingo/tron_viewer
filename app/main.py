# import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from .db import init_db
from .tron_router import tron_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)

app.include_router(tron_router)
add_pagination(app)
