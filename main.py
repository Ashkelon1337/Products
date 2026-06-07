from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException

from db import engine, Base, SessionDep
import services
from schemas import CreateProduct, ProductResponse





async def get_product_or_404(session, product_id):
    product = await services.get_product(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail='Product not founded')
    return product

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)


@app.get('/products', response_model=List[ProductResponse])
async def get_products(session: SessionDep):
    return await services.get_products(session)

@app.post('/products', response_model=ProductResponse)
async def create_product(session: SessionDep, product: CreateProduct):
    return await services.create_product(session, product)


@app.get('/products/{product_id}', response_model=ProductResponse)
async def get_product(session: SessionDep, product_id: int):
    product = await get_product_or_404(session, product_id)
    return product

@app.put('/products/{product_id}', response_model=ProductResponse)
async def update_product(session: SessionDep, product_id: int, product_data: CreateProduct):
    await get_product_or_404(session, product_id)
    product = await services.update_product(session, product_data, product_id)
    return product
@app.delete('/products/{product_id}')
async def delete_product(session: SessionDep, product_id: int):
    await get_product_or_404(session, product_id)
    deleted_product = await services.delete_product(session, product_id)
    return {"is_deleted": True,
            "was_deleted": deleted_product}
