from contextlib import asynccontextmanager
from fastapi import FastAPI
from core.logger import setup_logging

from store.db.utils import DB
from store.db.postgres.accessor import PostgresAccessor

db = DB(PostgresAccessor(setup_logging()), setup_logging())


@asynccontextmanager
async def lifespan(_: FastAPI):
    await db.connect()
    yield
    await db.disconnect()
