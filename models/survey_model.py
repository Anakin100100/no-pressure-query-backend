from sqlalchemy import Column, ForeignKey, Integer 
from sqlalchemy.orm import relationship
from utils.database_utils import Base


class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="surveys")
