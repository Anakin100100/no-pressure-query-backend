import pytest
from fastapi import HTTPException
from utils import testing_utils
from utils.database_utils import SessionLocal
import schemas.survey_question_schema as survey_question_schema
import services.survey_question_service as survey_question_service 
from models.survey_question_model import SurveyQuestionEnum

def test_create_survey_question_with_valid_data():
    user = testing_utils.create_user()
    db = SessionLocal()
    survey_question_create = survey_question_schema.SurveyQuestionCreate(question_text="test", question_type=SurveyQuestionEnum.text_question)
    survey = testing_utils.create_survey(user=user, db=db)
    survey_question = survey_question_service.create_survey_question(db=db, user=user, survey=survey, survey_question_create=survey_question_create)
    assert survey_question.question_text == "test"
    assert survey_question.question_type == SurveyQuestionEnum.text_question
    assert survey_question.survey_id == survey.id 


def test_create_survey_question_with_invalid_question_text():
    user = testing_utils.create_user()
    db = SessionLocal()
    survey_question_create = survey_question_schema.SurveyQuestionCreate(question_text="", question_type=SurveyQuestionEnum.text_question)
    survey = testing_utils.create_survey(user=user, db=db)
    with pytest.raises(HTTPException) as exception:
        survey_question = survey_question_service.create_survey_question(db=db, user=user, survey=survey, survey_question_create=survey_question_create)
        assert exception.detail == "Question text has to be a valid string, provided: "
