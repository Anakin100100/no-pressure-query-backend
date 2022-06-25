from sqlalchemy.orm import Session
import schemas.survey_schema as survey_schema
import schemas.user_schema as user_schema
import models.survey_model as survey_model
from fastapi import HTTPException


def create_survey(user: user_schema.User, db: Session, survey: survey_schema.SurveyCreate) -> survey_model.Survey:
    pass
