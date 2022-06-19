from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:123cc123@localhost/no_pressure_query"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

from models.survey_model import Survey
#This import is needed to make SQLAlchemy work with models in multiple files
#I don't know why we don't have to import User model but it throws an error when we try to import it

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

