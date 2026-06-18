from tests.supporting_functions import create_test_product
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_all_products(client: AsyncClient):
    await create_test_product(client)
    response = await client.get('/products')
    assert response.status_code == 200
    data = response.json()
    print('GET', data)
@pytest.mark.asyncio
async def test_set_product(client: AsyncClient):
    response = await create_test_product(client)
    assert response.status_code == 200
    data = response.json()
    print('POST', data)
@pytest.mark.asyncio
async def test_put_product(client: AsyncClient):
    create_response = await create_test_product(client)
    product_id = create_response.json()['id']
    response = await client.put(f'/products/{product_id}', json={
        "name": "Новый товар",
        "price": 777,
        "quantity": 3
    })
    assert response.status_code == 200
    print("PUT", response.json())
@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient):
    create_response = await create_test_product(client)
    product_id = create_response.json()['id']
    response = await client.delete(f'/products/{product_id}')
    assert response.status_code == 200
    print("DELETE", response.json())