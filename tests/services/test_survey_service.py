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
    assert db.query(survey_model.Survey).filter(survey_model.Survey.id == created_survey.id).first().name == "test survey name"
    db.close()

def test_create_survey_with_blank_name():
    user = testing_utils.create_user()
    db = SessionLocal()
    survey = survey_schema.SurveyCreate(name="")
    with pytest.raises(HTTPException) as exception:
        created_survey = survey_service.create_survey(user=user, db=db, survey=survey)
        assert exception.detail == "Name cannot be blank"
    db.close()

def test_user_surveys_with_single_survey():
    user = testing_utils.create_user()
    db = SessionLocal()
    survey = survey_schema.SurveyCreate(name="test")
    survey_service.create_survey(user=user, db=db, survey=survey)
    user_surveys = survey_service.get_user_surveys(user=user, db=db)
    assert survey.name == user_surveys[0].name

def test_user_surveys_with_multiple_surveys():
    user = testing_utils.create_user()
    db = SessionLocal()
    survey = survey_schema.SurveyCreate(name="test")
    for n in range(3):
        survey_service.create_survey(user=user, db=db, survey=survey)
    user_surveys = survey_service.get_user_surveys(user=user, db=db)
    assert len(user_surveys) == 3
