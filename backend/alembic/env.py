from __future__ import annotations

import asyncio
import logging
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from app.core.config import settings
from app.db.session import engine
from app import models  # noqa: F401  # ensure models are imported for metadata


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

logger = logging.getLogger("alembic.env")

config.set_main_option("sqlalchemy.url", settings.db_url)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    with engine.connect() as connection:
        do_run_migrations(connection)


def run_async_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def do_run():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(do_run())


if context.is_offline_mode():
    run_migrations_offline()
else:
    if engine.url.drivername.startswith("sqlite+aiosqlite"):
        run_async_migrations_online()
    else:
        run_migrations_online()
