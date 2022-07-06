from main import app
from fastapi.testclient import TestClient
from utils import testing_utils
from utils.database_utils import SessionLocal

def test_create_survey_question_correctly_authenticated():
    client = TestClient(app)
    user = testing_utils.create_user()
    token = testing_utils.get_token(user)
    db = SessionLocal()
    survey = testing_utils.create_survey(user=user, db=db)
    r = client.post("/survey_questions/create", 
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "question_text": "correct question text",
            "question_type": 1
        },
        params= {
            "survey_id": survey.id
        }
    )
    print(r.json())
    assert r.status_code == 200
    assert r.json()["question_text"] == "correct question text"
    assert r.json()["question_type"] == 1

def test_create_survey_question_correctly_unauthenticated():
    client = TestClient(app)
    db = SessionLocal()
    user = testing_utils.create_user()
    survey = testing_utils.create_survey(user=user, db=db)
    r = client.post("/survey_questions/create", 
        headers={
            "Authorization": f"Bearer invalid_token"
        },
        json={
            "question_text": "correct question text",
            "question_type": 1
        },
        params= {
            "survey_id": survey.id
        }
    )
    print(r.json())
    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid token"

def test_create_survey_question_with_incorrect_question_text_authenticated():
    client = TestClient(app)
    user = testing_utils.create_user()
    token = testing_utils.get_token(user)
    db = SessionLocal()
    survey = testing_utils.create_survey(user=user, db=db)
    r = client.post("/survey_questions/create", 
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "question_text": "",
            "question_type": 1
        },
        params= {
            "survey_id": survey.id
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Question text has to be a valid string, provided: "

def test_create_survey_question_with_incorrect_question_type_authenticated():
    client = TestClient(app)
    user = testing_utils.create_user()
    token = testing_utils.get_token(user)
    db = SessionLocal()
    survey = testing_utils.create_survey(user=user, db=db)
    r = client.post("/survey_questions/create", 
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "question_text": "correct question text",
            "question_type": -1
        },
        params= {
            "survey_id": survey.id
        }
    )
    print(r.json())
    assert r.status_code == 422
    assert r.json()['detail'][0]['msg'] == 'value is not a valid enumeration member; permitted: 1, 2, 3, 4'
