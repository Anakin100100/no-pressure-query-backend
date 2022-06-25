import pytest
from fastapi import HTTPException
from services import survey_service
from schemas import survey_schema
from utils import testing_utils
from models import survey_model
from utils.database_utils import SessionLocal

def test_create_survey_correctly():
    user = testing_utils.create_user()
    db = SessionLocal()
    survey = survey_schema.SurveyCreate(name="test survey name")
    created_survey = survey_service.create_survey(user=user, db=db, survey=survey)
    assert db.query(survey_model.Survey).filter(survey_model.Survey.id == created_survey).first().name == "test survey name"

def test_create_survey_with_blank_name():
    user = testing_utils.create_user()
    db = SessionLocal()
    survey = survey_schema.SurveyCreate(name="")
    with pytest.raises(HTTPException) as exception:
        created_survey = survey_service.create_survey(user=user, db=db, survey=survey)
        assert exception.detail == "Name cannot be blank"
