from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import passlib.hash as hash
from utils.database_utils import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    surveys = relationship("Survey", back_populates="user")
    question_answers = relationship("QuestionAnswer", back_populates="user")

    def verify_password(self, password: str):
        return hash.bcrypt.verify(password, self.hashed_password)
