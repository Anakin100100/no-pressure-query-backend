from sqlalchemy.orm import Session
import schemas.survey_schema as survey_schema
import schemas.user_schema as user_schema
import models.survey_model as survey_model
from fastapi import HTTPException


def create_survey(user: user_schema.User, db: Session, survey: survey_schema.SurveyCreate) -> survey_model.Survey:
    if survey.name == "":
        raise HTTPException(detail="Name cannot be blank", status_code=400)
    db_survey = survey_model.Survey(user_id=user.id, name=survey.name)
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey
