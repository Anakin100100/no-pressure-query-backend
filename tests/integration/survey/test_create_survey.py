from main import app
from fastapi.testclient import TestClient
from utils import testing_utils


def test_create_survey_correctly():
    client = TestClient(app)
    user = testing_utils.create_user()
    token = testing_utils.get_token(user)
    r = client.post(
        "/surveys/create", 
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "correct survey name"
        }
    )
    assert r.status_code == 200
    assert r.json()["name"] == "correct survey name"

def test_create_survey_unauthorised():
    client = TestClient(app)
    user = testing_utils.create_user()
    r = client.post(
        "/surveys/create", 
        headers={
            "Authorization": "Bearer incorrect_token"
        },
        json={
            "name": "correct survey name"
        }
    )
    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid token"

def test_create_survey_with_blank_name():
    client = TestClient(app)
    user = testing_utils.create_user()
    token = testing_utils.get_token(user)
    r = client.post(
        "/surveys/create", 
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": ""
        }
    )
    assert r.status_code == 400
    assert r.json()["detail"] == "Name cannot be blank" 
