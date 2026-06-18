from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException
from redis_client import get_cache, set_cached_products, invalidate_cache, get_cached_product_by_id, set_cached_product
from db import engine, Base, SessionDep
import services
from schemas import CreateProduct, ProductResponse

async def get_product_or_404(session, product_id):
    product = await services.get_product(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    return product

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)


@app.get('/products', response_model=List[ProductResponse])
async def get_products(session: SessionDep):
    cached = await get_cache('products:all')
    if cached:
        return cached
    products = await services.get_products(session)
    await set_cached_products(products, 60)
    return products

@app.post('/products', response_model=ProductResponse)
async def create_product(session: SessionDep, product: CreateProduct):
    new_product = await services.create_product(session, product)
    await invalidate_cache()
    await set_cached_product(new_product, 60)
    return new_product



@app.get('/products/{product_id}', response_model=ProductResponse)
async def get_product(session: SessionDep, product_id: int):
    cached = await get_cached_product_by_id(product_id)
    if cached:
        return cached
    product = await get_product_or_404(session, product_id)
    await set_cached_product(product, 60)
    return product

@app.put('/products/{product_id}', response_model=ProductResponse)
async def update_product(session: SessionDep, product_id: int, product_data: CreateProduct):
    await get_product_or_404(session, product_id)
    product = await services.update_product(session, product_data, product_id)
    await invalidate_cache()
    await invalidate_cache(f'products:{product_id}')
    await set_cached_product(product, 60)
    return product

@app.delete('/products/{product_id}')
async def delete_product(session: SessionDep, product_id: int):
    await get_product_or_404(session, product_id)
    deleted_product = await services.delete_product(session, product_id)
    await invalidate_cache(f'products:{product_id}')
    await invalidate_cache()
    return {"is_deleted": True,
            "was_deleted": deleted_product}
