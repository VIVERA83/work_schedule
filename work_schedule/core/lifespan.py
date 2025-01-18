from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.logger import setup_logging

from store.db.postgres.accessor import PostgresAccessor
from store.ws.store import DB

db = DB(PostgresAccessor(setup_logging()), setup_logging())


@asynccontextmanager
async def lifespan(_: FastAPI):
    await db.connect()
    yield
    await db.disconnect()
