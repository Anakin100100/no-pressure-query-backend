from main import app
from fastapi.testclient import TestClient
from utils import testing_utils

def test_create_survey_question_correctly_authenticated():
    client = TestClient(app)
    user = testing_utils.create_user()
    token = testing_utils.get_token(user)
    r = client.post("/survey_questions/create", 
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "question_text": "correct question text",
            "question_type": "single_choice_question"
        }
    )
    assert r.status_code == 200
    assert r.json()["question_text"] == "correct question text"
    assert r.json()["question_type"] == "single_choice_question"

def test_create_survey_question_correctly_unauthenticated():
    client = TestClient(app)
    r = client.post("/survey_questions/create", 
        headers={
            "Authorization": f"Bearer invalid_token"
        },
        json={
            "question_text": "correct question text",
            "question_type": "single_choice_question"
        }
    )
    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid token"

def test_create_survey_question_with_incorrect_question_text_authenticated():
    client = TestClient(app)
    user = testing_utils.create_user()
    token = testing_utils.get_token(user)
    r = client.post("/survey_questions/create", 
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "question_text": "",
            "question_type": "single_choice_question"
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Question text has to be a valid string, provided: "

def test_create_survey_question_with_incorrect_question_type_authenticated():
    client = TestClient(app)
    user = testing_utils.create_user()
    token = testing_utils.get_token(user)
    r = client.post("/survey_questions/create", 
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "question_text": "correct question text",
            "question_type": ""
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Invalid question type"
