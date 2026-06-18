from httpx import AsyncClient

async def create_test_product(client: AsyncClient):
    response = await client.post('/products', json={
        "name": "Тестовый товар",
        "price": 1000,
        "quantity": 5
    })
    return response