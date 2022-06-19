from sqlalchemy import Column, Enum, ForeignKey, Integer 
from sqlalchemy.orm import relationship
from utils.database_utils import Base


class AvailableAnswer(Base):
    __tablename__ = "available_answers"

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Integer, nullable=False, default=1)
    survey_question_id = Column(Integer, ForeignKey("survey_questions.id"), nullable=False)
    survey_question = relationship("SurveyQuestion", back_populates="available_answers")
