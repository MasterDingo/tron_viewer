import pytest

from ..models import Request


@pytest.mark.anyio
async def test_write_db(test_db, db_session):

    # Generate test data
    request = Request(address="12345", trx=10, bandwidth=600, energy=15)

    try:
        db_session.add(request)
        await db_session.commit()
        await db_session.refresh(request)
    except Exception as e:
        pytest.fail(f"Error writing to database: {e}")

    # Retrieve the request from the database
    req = await db_session.get(Request, request.id)

    assert req == request
