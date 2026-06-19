import redis.asyncio as redis
import json
from schemas import ProductResponse
from db import Products
from pydantic import TypeAdapter
from typing import List
redis_client = redis.from_url('redis://redis:6379')

async def get_cache(name: str):
    cached = await redis_client.get(name)
    return json.loads(cached) if cached else None

async def get_cached_product_by_id(product_id):
    cached = await redis_client.get(f'products:{product_id}')
    return json.loads(cached) if cached else None

async def set_cached_products(products_data_sqlalchemy: list, ttl: int = 10):
    adapter = TypeAdapter(List[ProductResponse])
    product_data_pydantic = adapter.validate_python(products_data_sqlalchemy, from_attributes=True)
    products_json = adapter.dump_json(product_data_pydantic)
    await redis_client.set(f'products:all', products_json, ex=ttl)

async def set_cached_product(product_data_sqlalchemy: Products, ttl: int = 10):
    product_data_pydantic = ProductResponse.model_validate(product_data_sqlalchemy, from_attributes=True)
    product_json = product_data_pydantic.model_dump_json()
    await redis_client.set(f'products:{product_data_pydantic.id}', product_json, ex=ttl)


async def invalidate_cache(name:str = 'products:all'):
    await redis_client.delete(name)

