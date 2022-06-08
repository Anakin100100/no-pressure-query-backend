import sys

sys.path.append("../no-pressure-query-backend")

from main import app
from fastapi.testclient import TestClient
import models
from database import SessionLocal
import random


def test_create_user():
    db = SessionLocal()
    client = TestClient(app)
    email = f"email_that_hasnt_been_used{sum([random.choice([1,2,3,4,5,6,7,8,9]) * 10 ^ n for n in range(10)])}"
    number_of_users_before = db.query(models.User).count()
    response = client.post(
        "/users/",
        json={"email": email, "password": "test_password"},
    )
    number_of_users_after = db.query(models.User).count()
    db.close()
    assert number_of_users_after - number_of_users_before == 1
    assert response.status_code == 200
    assert response.json()["email"] == email
    assert response.json()["id"] >= 0
    assert response.json()["is_active"] is True


def test_create_jwt():
    client = TestClient(app)
    email = f"email_that_hasnt_been_used{sum([random.choice([1,2,3,4,5,6,7,8,9]) * 10 ^ n for n in range(10)])}"
    response_registration = client.post(
        "/users/",
        json={"email": email, "password": "test_password"},
    )
    response_token = client.post(
        "/api/token", data={"username": email, "password": "test_password"}
    )
    print(response_token.json())
    assert response_token.status_code == 200
    assert len(response_token.json()["access_token"]) > 50
    assert response_token.json()["token_type"] == "bearer"


def test_create_jwt_with_wrong_password():
    client = TestClient(app)
    email = f"email_that_hasnt_been_used{sum([random.choice([1,2,3,4,5,6,7,8,9]) * 10 ^ n for n in range(10)])}"
    response_registration = client.post(
        "/users/",
        json={"email": email, "password": "test_password"},
    )
    response_token = client.post(
        "/api/token", data={"username": email, "password": "wrong_password"}
    )
    print(response_token.json())
    assert response_token.json()["status_code"] == 401
    assert response_token.json()["detail"] == "Invalid credentials"
