import asyncio
import os
import sys
from logging.config import fileConfig

import dotenv
from sqlalchemy import pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from alembic_utils.replaceable_entity import register_entities

sys.path.insert(1, os.path.join(os.getcwd(), "work_schedule"))
dotenv.load_dotenv()

from work_schedule.core.settings import PostgresSettings
from work_schedule.store.ws.models import Base
from store.functions import f1, f2, my_trigger_function, my_trigger

config = context.config

settings = PostgresSettings()  # noqa
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

config.set_main_option("sqlalchemy.url", settings.dsn(True))
register_entities([my_trigger_function])


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    current_tenant = settings.postgres_schema
    async with connectable.connect() as connection:
        await connection.execute(
            text("CREATE SCHEMA IF NOT EXISTS %s" % current_tenant)
        )
        await connection.execute(text(f1))
        await connection.execute(text(f2))
        await connection.execute(text('set search_path to "%s"' % current_tenant))
        await connection.commit()
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
