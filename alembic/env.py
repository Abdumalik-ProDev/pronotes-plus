from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context

from app.models.base import Base
from app.models.user import User
from app.models.note import Note

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

DATABASE_URL = config.get_main_option("sqlalchemy.url")
if not DATABASE_URL:
    raise RuntimeError("sqlalchemy.url is not set in alembic.ini or env")

def run_migrations_online():
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    def do_run_migrations(connection: Connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            render_as_batch=True,
        )
        with context.begin_transaction():
            context.run_migrations()

    import asyncio

    async def async_migrations():
        async with connectable.connect() as conn:
            await conn.run_sync(do_run_migrations)

    asyncio.run(async_migrations())

run_migrations_online()