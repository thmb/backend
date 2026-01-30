'''Alembic environment configuration.'''
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from restapi.config import get_settings
from restapi.database import Base
from restapi.models import product  # noqa: F401 - Import models to register them

# Alembic Config object
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Model metadata for autogenerate
target_metadata = Base.metadata


def get_url() -> str:
    '''Get database URL from application settings.'''
    return get_settings().database_url


def run_migrations_offline() -> None:
    '''Run migrations in offline mode (generates SQL script).'''
    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    '''Run migrations in online mode (connects to database).'''
    configuration = config.get_section(config.config_ini_section, {})
    configuration['sqlalchemy.url'] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
