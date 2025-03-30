"""migrate_to_sqlite

Revision ID: 9deea113f2f9
Revises: 1a31ce608336
Create Date: 2025-03-30 13:26:27.325036

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
import uuid


# revision identifiers, used by Alembic.
revision = '9deea113f2f9'
down_revision = '1a31ce608336'
branch_labels = None
depends_on = None


def upgrade():
    # Create SQLite tables
    
    # Create user table
    op.create_table(
        'user',
        sa.Column('id', sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
        sa.Column('email', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, default=False),
        sa.Column('full_name', sa.String(255), nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
    )
    
    # Create item table
    op.create_table(
        'item',
        sa.Column('id', sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4())),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.String(255), nullable=True),
        sa.Column('owner_id', sa.String(36), sa.ForeignKey('user.id'), nullable=False),
    )


def downgrade():
    op.drop_table('item')
    op.drop_table('user')
