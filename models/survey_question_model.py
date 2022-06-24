from sqlalchemy import Column, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from utils.database_utils import Base
import enum

class SurveyQuestionEnum(enum.Enum):
    single_choice_question = 1
    multiple_choice_question = 2
    text_question = 3
    weighted_ranking = 4



class SurveyQuestion(Base):
    __tablename__ = "survey_questions"

    id = Column(Integer, primary_key=True, index=True)
    question_type = Column(Enum(SurveyQuestionEnum) )
    question_text = Column(Text, nullable=False)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    survey = relationship("Survey", back_populates="survey_questions")
    available_answers = relationship("AvailableAnswer", back_populates="survey_question")
