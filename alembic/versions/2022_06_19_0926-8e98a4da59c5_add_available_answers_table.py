"""add available_answers table

Revision ID: 8e98a4da59c5
Revises: d8de0266f2dd
Create Date: 2022-06-19 09:26:25.046146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e98a4da59c5'
down_revision = 'd8de0266f2dd'
branch_labels = None
depends_on = None



def upgrade():
    op.create_table(
        "available_answers",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("survey_question_id", sa.Integer, sa.ForeignKey("survey_questions.id"), nullable=False),
        sa.Column("weight", sa.Integer, nullable=False, default=1),
    )


def downgrade():
    op.drop_table("available_answers")
