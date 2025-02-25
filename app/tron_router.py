import logging
import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate

from sqlmodel import select, col
from sqlmodel.ext.asyncio.session import AsyncSession

from tronpy import AsyncTron

from .db import get_session
from .models import Request, RequestCreate
from .settings import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tron_router = APIRouter()

tron = AsyncTron(**settings.get_tron_params())


@tron_router.get("/tron", response_model=Page[Request])
async def request_list(
    session: AsyncSession = Depends(get_session),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Page size"),
):
    logger.info("Getting requests")
    records = await paginate(
        session,
        select(Request)
        .limit(page_size)
        .offset(page_size * (page - 1))
        .order_by(col(Request.created_at).desc()),
    )

    return records


@tron_router.post("/tron", response_model=Request)
async def query_address(
    req: RequestCreate, *, session: AsyncSession = Depends(get_session)
):
    address = req.address
    logger.info(f"Querying address {address}")

    try:
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
    except Exception as e:
        logger.error(f"Error querying address {address}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
