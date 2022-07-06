from sqlalchemy.orm import Session
import schemas.survey_schema as survey_schema
import schemas.user_schema as user_schema
import models.survey_model as survey_model
from fastapi import HTTPException
from typing import List


def create_survey(user: user_schema.User, db: Session, survey: survey_schema.SurveyCreate) -> survey_model.Survey:
    if survey.name == "":
        raise HTTPException(detail="Name cannot be blank", status_code=400)
    db_survey = survey_model.Survey(user_id=user.id, name=survey.name)
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey

def get_user_surveys(user: user_schema.User, db: Session) -> List[survey_model.Survey]:
    return db.query(survey_model.Survey).filter(survey_model.Survey.user_id == user.id).all()


def get_survey(survey_id: int, db: Session) -> survey_model.Survey:
    return db.query(survey_model.Survey).filter(survey_model.Survey.id == survey_id).first()
