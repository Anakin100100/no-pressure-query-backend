"""add users

Revision ID: 1dd485cd6a63
Revises: 
Create Date: 2022-06-08 14:19:25.345457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1dd485cd6a63"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("email", sa.String(50), nullable=False, index=True),
        sa.Column("hashed_password", sa.String(128, nullable=False)),
        sa.Column("first_name", sa.String(32, nullable=False)),
        sa.Column("last_name", sa.String(32, nullable=False))
    )


def downgrade():
    op.drop_table("users")
