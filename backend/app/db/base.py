from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

# Define a naming convention for constraints for Alembic migrations
# This helps in generating predictable and consistent migration scripts.
# See: https://alembic.sqlalchemy.org/en/latest/naming.html
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
Base = declarative_base(metadata=metadata)

# Import all models here to ensure they are registered with Base.metadata
# This is crucial for Alembic auto-generation of migrations.
# Example:
# from app.models.user import User
# from app.models.item import Item # if you have other models

# For now, this will be empty and models will be imported in env.py for Alembic,
# or you can explicitly import them here as they are created.
# Let's defer specific model imports until they are defined to avoid circular dependencies
# during file creation. Alembic's env.py will handle imports for migrations.

# However, to ensure Alembic autogenerate works reliably, models should be imported
# somewhere that ensures they are registered with Base.metadata before env.py accesses it.
# Importing them here is one way.
# from app.models.user import User  # Reverted: Causes circular imports
# from app.models.course import Course, Module, Lesson # Reverted: Causes circular imports
