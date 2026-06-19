from logging.config import fileConfig
from db import Base, url as real_url
from sqlalchemy import engine_from_config
from sqlalchemy import pool
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    pass

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )
    with context.begin_transaction():
        context.run_migrations()
async def run_migrations_online_async() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = real_url
    connectable = create_async_engine(real_url)
    async with connectable.connect() as conn:
        await conn.run_sync(do_run_migrations)
def run_migrations_online() -> None:
    import asyncio
    asyncio.run(run_migrations_online_async())
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
