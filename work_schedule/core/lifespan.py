from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.logger import setup_logging
# from store.db.postgres_db.accessor import PostgresAccessor
# from store.product.brand.accessor import BrandAccessor
# from store.product.category.accessor import CategoryAccessor
# from store.product.product.accessor import ProductAccessor

loger = setup_logging()
# postgres_accessor = PostgresAccessor(loger)
#
# brand_accessor = BrandAccessor(postgres_accessor, loger)
# category_accessor = CategoryAccessor(postgres_accessor, loger)
# product_accessor = ProductAccessor(postgres_accessor, loger)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # await postgres_accessor.connect()
    yield
    # await postgres_accessor.disconnect()
