import sys

sys.path.append("../no-pressure-query-backend")

from main import app
from fastapi.testclient import TestClient
import uuid

from database_utils import SessionLocal
from datetime import datetime
import db_models.user_model as user_model


def test_create_user_with_correct_data():
    db = SessionLocal()
    client = TestClient(app)
    email = f"email_{datetime.now().strftime('%H%M%S%f')}@gmail.com"
    number_of_users_before = db.query(user_model.User).count()
    response = client.post(
        "/users/",
        json={"email": email, "password": "test_password", "first_name": "test", "last_name": "test"},
    )
    number_of_users_after = db.query(user_model.User).count()
    db.close()
    assert number_of_users_after - number_of_users_before == 1
    assert response.status_code == 200
    assert response.json()["email"] == email
    assert response.json()["id"] >= 0
    assert response.json()["first_name"] == "test"
    assert response.json()["last_name"] == "test"


def test_create_user_with_incorrect_password():
    db = SessionLocal()
    client = TestClient(app)
    email = f"email_{datetime.now().strftime('%H:%M:%S:%f')}"
    number_of_users_before = db.query(user_model.User).count()
    response = client.post(
        "/users/",
        json={"email": email, "password": "", "first_name": "test", "last_name": "test"},
    )
    number_of_users_after = db.query(user_model.User).count()
    assert number_of_users_after - number_of_users_before == 0
    assert response.status_code == 400
    assert response.json()["detail"] == "Password must be at least 8 characters"
    db.close()


def test_create_user_with_incorrect_email():
    db = SessionLocal()
    client = TestClient(app)
    email = f"email{datetime.now().strftime('%H:%M:%S:%f')}_wrong_email"
    number_of_users_before = db.query(user_model.User).count()
    response = client.post(
        "/users/",
        json={"email": email, "password": "test_password", "first_name": "test", "last_name": "test"},
    )
    number_of_users_after = db.query(user_model.User).count()
    assert number_of_users_after - number_of_users_before == 0
    assert response.status_code == 400
    assert response.json()["detail"] == "Email must be a valid email address"
    db.close()

def test_create_user_with_invalid_first_name():
    db = SessionLocal()
    client = TestClient(app)
    email =  f"{uuid.uuid4()}@gmail.com".replace("-", "")
    number_of_users_before = db.query(user_model.User).count()
    response = client.post(
        "/users/",
        json={"email": email, "password": "test_password", "first_name": "", "last_name": "test"},
    )
    number_of_users_after = db.query(user_model.User).count()
    assert number_of_users_after - number_of_users_before == 0
    assert response.status_code == 400
    assert response.json()["detail"] == "First name must be at least 2 characters"
    db.close()

def test_create_user_with_invalid_last_name():
    db = SessionLocal()
    client = TestClient(app)
    email =  f"{uuid.uuid4()}@gmail.com".replace("-", "")
    number_of_users_before = db.query(user_model.User).count()
    response = client.post(
        "/users/",
        json={"email": email, "password": "test_password", "first_name": "test", "last_name": ""},
    )
    number_of_users_after = db.query(user_model.User).count()
    assert number_of_users_after - number_of_users_before == 0
    assert response.status_code == 400
    assert response.json()["detail"] == "Last name must be at least 2 characters"
    db.close()
