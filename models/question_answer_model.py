from sqlalchemy import Column, ForeignKey, Integer 
from sqlalchemy.orm import relationship
from utils.database_utils import Base


class QuestionAnswer(Base):
    __tablename__ = "question_answers"

    id = Column(Integer, primary_key=True, index=True)
    available_answer_id = Column(Integer, ForeignKey("available_answers.id"), nullable=False)
    available_answer = relationship("AvailableAnswer", back_populates="question_answers")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="question_answers")
