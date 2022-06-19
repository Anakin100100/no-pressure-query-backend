"""add question_answers table

Revision ID: 415514445818
Revises: 8e98a4da59c5
Create Date: 2022-06-19 09:38:41.381999

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '415514445818'
down_revision = '8e98a4da59c5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "question_answers",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("available_answer_id", sa.Integer, sa.ForeignKey("available_answers.id"), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("answer", sa.Text, nullable=False),
    )


def downgrade():
    op.drop_table("question_answers")
