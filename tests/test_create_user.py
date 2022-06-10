import sys

sys.path.append("../no-pressure-query-backend")

from main import app
from fastapi.testclient import TestClient
import models
from database import SessionLocal
from datetime import datetime


def test_create_user_with_correct_data():
    db = SessionLocal()
    client = TestClient(app)
    email = f"email_{datetime.now().strftime('%H%M%S%f')}@gmail.com"
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


def test_create_user_with_incorrect_password():
    db = SessionLocal()
    client = TestClient(app)
    email = f"email_{datetime.now().strftime('%H:%M:%S:%f')}"
    number_of_users_before = db.query(models.User).count()
    response = client.post(
        "/users/",
        json={"email": email, "password": ""},
    )
    number_of_users_after = db.query(models.User).count()
    assert number_of_users_after - number_of_users_before == 0
    assert response.status_code == 400
    assert response.json()["detail"] == "Password must be at least 8 characters"
    db.close()


def test_create_user_with_incorrect_email():
    db = SessionLocal()
    client = TestClient(app)
    email = f"email_{datetime.now().strftime('%H:%M:%S:%f')}_wrong_email"
    number_of_users_before = db.query(models.User).count()
    response = client.post(
        "/users/",
        json={"email": email, "password": "test_password"},
    )
    number_of_users_after = db.query(models.User).count()
    assert number_of_users_after - number_of_users_before == 0
    assert response.status_code == 400
    assert response.json()["detail"] == "Email must be a valid email address"
    db.close()
