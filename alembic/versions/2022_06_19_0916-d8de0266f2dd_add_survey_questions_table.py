"""add survey_questions table

Revision ID: d8de0266f2dd
Revises: 4bee8c7d0404
Create Date: 2022-06-19 09:16:05.424094

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8de0266f2dd'
down_revision = '4bee8c7d0404'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "survey_questions",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("survey_id", sa.Integer, sa.ForeignKey("surveys.id"), nullable=False),
        sa.Column("question_type", sa.Enum(
            "single_choice_question",
            "multiple_choice_question",
            "text_question",
            "weighted_ranking",
            name="question_type_enum"
        ), nullable=False)
    )


def downgrade():
    op.drop_table("survey_questions")
    op.execute("DROP TYPE question_type_enum")

