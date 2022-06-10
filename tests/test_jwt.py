import sys

sys.path.append("../no-pressure-query-backend")

from main import app
from fastapi.testclient import TestClient

import testing_utils


def test_create_jwt():
    """
    We first create a user then acquire a token for him and later validate that the token
    is correct by accessing the token protected endpoint which returns the user data from
    token
    """
    client = TestClient(app)
    user = testing_utils.create_user()
    response_create_token = client.post(
        "/api/token", data={"username": user.email, "password": "test_password"}
    )
    assert response_create_token.status_code == 200
    assert len(response_create_token.json()["access_token"]) > 50
    assert response_create_token.json()["token_type"] == "bearer"
    response_validate_token = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {response_create_token.json()['access_token']}"
        },
    )
    assert response_validate_token.status_code == 200
    assert response_validate_token.json()["email"] == user.email
    assert response_validate_token.json()["id"] == user.id
    assert response_validate_token.json()["is_active"] is True


def test_access_user_info_with_wrong_token():
    client = TestClient(app)
    user = testing_utils.create_user()
    response_token = client.post(
        "/api/token", data={"username": user.email, "password": "test_password"}
    )
    response_token_wrong = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {response_token.json()['access_token']}wrong_token"
        },
    )
    assert response_token_wrong.status_code == 401
    assert response_token_wrong.json()["detail"] == "Invalid token"


def test_create_jwt_with_wrong_password():
    client = TestClient(app)
    user = testing_utils.create_user()
    response_token = client.post(
        "/api/token", data={"username": user.email, "password": "wrong_password"}
    )
    print(response_token.json())
    assert response_token.json()["status_code"] == 401
    assert response_token.json()["detail"] == "Invalid credentials"


def test_create_jwt_with_wrong_email():
    client = TestClient(app)
    user = testing_utils.create_user()
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
