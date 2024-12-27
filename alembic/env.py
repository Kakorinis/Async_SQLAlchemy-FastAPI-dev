import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from settings import app_settings
from src.models import Base
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url', app_settings.SQL_DSN)

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


def include_name_filter(name, type_, parent_names) -> bool:
    """
    Вызываемая функция, которой предоставляется возможность возвращать `True` или `False` для любой отображаемой базы
    данных объект на основе его имени, включая имена схем базы данных.

    :param name: Имя объекта, например, имя схемы или имя таблицы.
    :param type_: Строка, описывающая тип объекта; в настоящее время 'schema', 'table', 'column', 'index',
    'unique_constraint' или 'foreign_key_constraint'.
    :param parent_names: Словарь родительских имен объектов, относящихся к заданному имени.  Ключи в этом словаре могут
    быть: 'schema_name', 'table_name' или 'schema_qualified_table_name'.
    :return: Логическое значение.
    """
    if type_ == 'schema':
        return name == app_settings.SQL_SCHEMA  # type: ignore[no-any-return]

    return True


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
        version_table_schema=app_settings.SQL_SCHEMA,
        render_as_batch=True,
        include_schemas=True,
        include_name=include_name_filter
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table_schema=app_settings.SQL_SCHEMA,
        render_as_batch=True,
        include_schemas=True,
        include_name=include_name_filter

    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
