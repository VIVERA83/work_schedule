from contextlib import asynccontextmanager

from core.logger import setup_logging
from fastapi import FastAPI
from store.db.postgres.accessor import PostgresAccessor
from store.store import Store

store = Store(PostgresAccessor(setup_logging()), setup_logging())


@asynccontextmanager
async def lifespan(_: FastAPI):
    await store.connect()
    yield
    await store.disconnect()
