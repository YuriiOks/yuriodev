"""manual_create_user_table

Revision ID: a7e22c434ab9
Revises:
Create Date: 2025-05-30 02:38:41.583053 # Timestamp will vary

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7e22c434ab9'
down_revision: Union[str, None] = None # This should be empty if it's the first migration
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('provider', sa.String(), nullable=True),
    sa.Column('provider_user_id', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True, default=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_full_name'), 'users', ['full_name'], unique=False)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False) # Index on PK is usually automatic, but explicit for op.f naming
    op.create_index('ix_users_provider_provider_user_id', 'users', ['provider', 'provider_user_id'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_users_provider_provider_user_id', table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_full_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
