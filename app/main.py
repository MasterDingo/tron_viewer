import os
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlmodel import paginate

from sqlmodel import select, col
from sqlmodel.ext.asyncio.session import AsyncSession

from tronpy import AsyncTron
import decimal

from .db import init_db, get_session
from .models import Request, RequestCreate
from .utils import make_tron_params


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

tron_params = make_tron_params(os.environ)
tron = AsyncTron(**tron_params)


@app.get("/tron", response_model=Page[Request])
async def request_list(
    session: AsyncSession = Depends(get_session),
):
    records = await paginate(
        session, select(Request).order_by(col(Request.created_at).desc())
    )

    return records


@app.post("/tron", response_model=Request)
async def query_address(
    req: RequestCreate, *, session: AsyncSession = Depends(get_session)
):
    address = req.address

    trx, bandwidth, energy = await asyncio.gather(
        tron.get_account_balance(address),
        tron.get_bandwidth(address),
        tron.get_energy(address),
    )

    request = Request(address=address, trx=trx, bandwidth=bandwidth, energy=energy)
    session.add(request)
    await session.commit()
    await session.refresh(request)

    return request


add_pagination(app)