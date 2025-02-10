import uuid
import decimal
from datetime import datetime as dt
from datetime import timezone as tz

from sqlmodel import SQLModel, Field


class RequestBase(SQLModel):
    address: str


class Request(RequestBase, table=True):
    __tablename__ = "requests"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: dt = Field(default_factory=lambda: dt.now(tz.utc), index=True)
    trx: decimal.Decimal
    bandwidth: int
    energy: int


class RequestCreate(RequestBase):
    pass
