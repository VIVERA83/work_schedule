from contextlib import asynccontextmanager

from core.logger import setup_logging
from fastapi import FastAPI

from manager.manager import Manager
from store.db.postgres.accessor import PostgresAccessor
from store.store import Store

logger = setup_logging()
store = Store(PostgresAccessor(logger), logger)
manager = Manager(store, logger)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await store.connect()
    yield
    await store.disconnect()
