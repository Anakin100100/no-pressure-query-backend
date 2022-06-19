"""add surveys table

Revision ID: 4bee8c7d0404
Revises: fb85de9b33ce
Create Date: 2022-06-19 09:11:03.883808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bee8c7d0404'
down_revision = 'fb85de9b33ce'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "surveys",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    )


def downgrade():
    op.drop_table("surveys")
