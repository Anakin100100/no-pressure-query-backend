"""add name columns to survey

Revision ID: fa5237c546b0
Revises: fa770e1b7f1c
Create Date: 2022-06-25 00:58:42.999531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa5237c546b0'
down_revision = 'fa770e1b7f1c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("surveys", sa.Column('name', sa.Text, nullable=False) )


def downgrade():
    op.drop_column("surveys", "name")
