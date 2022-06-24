from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from utils.database_utils import Base


class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(Text, nullable=False)
    user = relationship("User", back_populates="surveys")
    survey_questions = relationship("SurveyQuestion", back_populates="survey")
