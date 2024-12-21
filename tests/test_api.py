import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_tron_api(test_db, client: AsyncClient):
    mock_address = "0123456789"
    # Send request
    response = await client.post("/tron", json={"address": mock_address})
    assert response.status_code == 200
    json = response.json()

    # Check response values
    assert json.get("address") == mock_address
    assert float(json.get("trx")) == 2.0
    assert json.get("bandwidth") == 100
    assert json.get("energy") == 6000


@pytest.mark.anyio
async def test_db_records(test_db, db_session, client: AsyncClient):
    mock_address = "0123456789"
    # Send POST request
    response = await client.post("/tron", json={"address": mock_address})
    assert response.status_code == 200

    # Get created object
    stored_json = response.json()

    # Send GET response
    response = await client.get("/tron")
    assert response.status_code == 200

    json = response.json()

    # Check response values
    assert json.get("total") == 1
    assert json.get("page") == 1
    assert json.get("size") == 50
    assert json.get("pages") == 1

    items = json.get("items")

    assert len(items) == 1
    assert items[0] == stored_json
