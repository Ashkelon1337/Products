import redis.asyncio as redis
import json
from schemas import ProductResponse
from db import Products

redis_client = redis.from_url('redis://localhost')

async def get_cache(name: str):
    cached = await redis_client.get(name)
    return json.loads(cached) if cached else None

async def get_cached_product_by_id(product_id):
    cached = await redis_client.get(f'products:{product_id}')
    return json.loads(cached) if cached else None

async def set_cached_products(products_data_sqlalchemy: list, ttl: int = 10):
    products_data_pydantic = [ProductResponse.model_validate(product, from_attributes=True) for product in products_data_sqlalchemy]
    products_data_dict = [product.model_dump() for product in products_data_pydantic]
    await redis_client.setex('products:all', ttl, json.dumps(products_data_dict))

async def set_cached_product(product_data_sqlalchemy: Products, ttl: int = 10):
    product_data_pydantic = ProductResponse.model_validate(product_data_sqlalchemy, from_attributes=True)
    product_data_dict = product_data_pydantic.model_dump()
    await redis_client.setex(f'products:{product_data_dict['id']}', ttl, json.dumps(product_data_dict))


async def invalidate_cache(name:str = 'products:all'):
    await redis_client.delete(name)

