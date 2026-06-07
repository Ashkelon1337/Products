from sqlalchemy.ext.asyncio import AsyncSession
from db import Products
from sqlalchemy import select, update, delete
from schemas import CreateProduct

async def create_product(session: AsyncSession, product_data: CreateProduct):
    new_product = Products(**product_data.model_dump())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product


async def get_products(session: AsyncSession):
    products = await session.scalars(select(Products))
    return products.all()

async def get_product(session: AsyncSession, product_id: int):
    product = await session.scalar(select(Products).where(Products.id == product_id))
    return product
async def update_product(session: AsyncSession, product_data: CreateProduct, product_id: int):
    stmt = ( update(Products)
            .where(Products.id == product_id)
            .values(**product_data.model_dump())
            .returning(Products)
    )
    result = await session.execute(stmt)
    product = result.scalar()
    await session.commit()
    return product
async def delete_product(session: AsyncSession, product_id: int):
    result = await session.execute(delete(Products).where(Products.id == product_id).returning(Products))
    product = result.scalar()
    await session.commit()
    return product