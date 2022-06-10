import sys

sys.path.append("../no-pressure-query-backend")

from main import app
from fastapi.testclient import TestClient

import test_utils


def test_create_jwt():
    client = TestClient(app)
    user = test_utils.create_user()
    response_token = client.post(
        "/api/token", data={"username": user.email, "password": "test_password"}
    )
    assert response_token.status_code == 200
    assert len(response_token.json()["access_token"]) > 50
    assert response_token.json()["token_type"] == "bearer"


def test_create_jwt_with_wrong_password():
    client = TestClient(app)
    user = test_utils.create_user()
    response_token = client.post(
        "/api/token", data={"username": user.email, "password": "wrong_password"}
    )
    print(response_token.json())
    assert response_token.json()["status_code"] == 401
    assert response_token.json()["detail"] == "Invalid credentials"


def test_create_jwt_with_wrong_email():
    client = TestClient(app)
    user = test_utils.create_user()
    response_token = client.post(
        "/api/token",
        data={
            "username": "email_that_cannot_be_in_the_db",
            "password": "some_password",
        },
    )
    print(response_token.json())
    assert response_token.json()["status_code"] == 401
    assert response_token.json()["detail"] == "Invalid credentials"
