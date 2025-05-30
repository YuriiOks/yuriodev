from logging.config import fileConfig
import os # For environment variables

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Import Base and your models for 'autogenerate' support
from app.db.base import Base # Adjusted import path
from app.models.user import User # Example: import your User model
# Add other models here:
# from app.models.your_other_model import YourOtherModel


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target_metadata to your Base.metadata
target_metadata = Base.metadata

# Get DATABASE_URL from environment variable
# This will override the sqlalchemy.url from alembic.ini if present,
# making it more flexible for different environments (dev, test, prod).
db_url = os.getenv('DATABASE_URL')
if db_url:
    config.set_main_option('sqlalchemy.url', db_url)
else:
    # Fallback to alembic.ini's sqlalchemy.url if DATABASE_URL is not set
    # Ensure alembic.ini has a default or this will fail if DATABASE_URL is not set.
    # For this project, DATABASE_URL is expected to be set via docker-compose.
    pass


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


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
        # Include naming convention for offline mode if needed for consistency with online
        # See: https://alembic.sqlalchemy.org/en/latest/naming.html#the-importance-of-naming-conventions
        # This ensures that constraint names are generated correctly even in offline mode.
        # However, offline generation is less common for autogenerate.
        # For autogenerate, online mode is typically used.
        # For consistency with Base metadata:
        include_object=lambda obj, name, type_, reflected, compare_to: \
            not (type_ == "table" and obj.info.get("skip_autogenerate", False)),
        render_as_batch=True, # For SQLite compatibility if used in tests
        naming_convention=Base.metadata.naming_convention,

    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        # Pass the URL directly if overridden by environment variable
        url=config.get_main_option('sqlalchemy.url')
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # For consistency with Base metadata:
            render_as_batch=True, # For SQLite compatibility if used in tests
            naming_convention=Base.metadata.naming_convention,
            # Compare type for enums and other types not natively supported by backend
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
