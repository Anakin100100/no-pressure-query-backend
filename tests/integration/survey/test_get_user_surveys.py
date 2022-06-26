from main import app
from fastapi.testclient import TestClient
from utils import testing_utils
from services import survey_service
from utils.database_utils import SessionLocal
from schemas.survey_schema import SurveyCreate
import uuid


def test_get_user_surveys_one_survey():
    client = TestClient(app)
    user = testing_utils.create_user()
    token = testing_utils.get_token(user)
    db = SessionLocal()
    survey_create = SurveyCreate(name="test")
    survey = survey_service.create_survey(user=user, db=db, survey=survey_create)
    r = client.get("/surveys/get_user_surveys",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert r.json()[0]["name"] == survey.name

def test_get_user_surveys_multiple_surveys():
    client = TestClient(app)
    user = testing_utils.create_user()
    token = testing_utils.get_token(user)
    db = SessionLocal()
    iter = 3
    survey_create_list = [SurveyCreate(name=f"survey{uuid.uuid4()}") for n in range(iter)]
    for n in range(iter):
        _ = survey_service.create_survey(user=user, db=db, survey=survey_create_list[n])
    r = client.get("/surveys/get_user_surveys",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    response = r.json()
    assert len(r.json()) == 3   
    for i in range(iter):
        found = False
        for j in range(iter):
            if response[i]["name"] == survey_create_list[j].name:
                found = True
                break 
        if found == False:
            joined_expected_survey_name = " and ".join([s.name for s in survey_create_list])
            raise Exception(f"The survey with name {survey_create_list[j].name} was not found among {joined_expected_survey_name}")

def test_get_user_surveys_one_survey_unathenticated():
    client = TestClient(app)
    user = testing_utils.create_user()
    db = SessionLocal()
    survey_create = SurveyCreate(name="test")
    _ = survey_service.create_survey(user=user, db=db, survey=survey_create)
    r = client.get("/surveys/get_user_surveys",
        headers={
            "Authorization": "Bearer incorrect_token"
        }
    )
    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid token"
